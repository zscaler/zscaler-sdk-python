# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from box import Box, BoxList
from requests import Response

from zscaler.utils import (
    convert_keys,
    recursive_snake_to_camel,
    snake_to_camel,
    transform_common_id_fields,
)
from zscaler.zia import ZIAClient


class URLFilteringAPI:
    # URL Filtering Policy rule keys that only require an ID to be provided.
    reformat_params = [
        ("departments", "departments"),
        ("devices", "devices"),
        ("device_groups", "deviceGroups"),
        ("groups", "groups"),
        ("labels", "labels"),
        ("locations", "locations"),
        ("location_groups", "locationGroups"),
        ("override_users", "overrideUsers"),
        ("override_groups", "overrideGroups"),
        ("time_windows", "timeWindows"),
        ("users", "users"),
    ]

    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_rules(self) -> BoxList:
        """
        Returns the list of URL Filtering Policy rules

        Returns:
            :obj:`BoxList`: The list of URL Filtering Policy rules.

        Examples:
            >>> for rule in zia.url_filters.list_rules():
            ...    pprint(rule)

        """
        response = self.rest.get("urlFilteringRules")
        if isinstance(response, Response):
            return None
        return response

    def get_rule(self, rule_id: str) -> Box:
        """
        Returns information on the specified URL Filtering Policy rule.

        Args:
            rule_id (str): The unique ID for the URL Filtering Policy rule.

        Returns:
            :obj:`Box`: The URL Filtering Policy rule.

        Examples:
            >>> pprint(zia.url_filters.get_rule('977469'))

        """

        return self.rest.get(f"urlFilteringRules/{rule_id}")

    def add_rule(
        self,
        rank: str,
        name: str,
        action: str,
        protocols: list,
        # override_users: list,
        # override_groups: list,
        **kwargs,
    ) -> Box:
        """
        Adds a new URL Filtering Policy rule.

        Args:
            rank (str): The admin rank of the user who creates the rule.
            name (str): The name of the rule.
            action (str): Action taken when traffic matches rule criteria. Accepted values are:

                `ANY`, `NONE`, `BLOCK`, `CAUTION`, `ALLOW` and `ICAP_RESPONSE`

            device_trust_levels (list): List of device trust levels for which the rule must be applied. Accepted values are:
                `ANY`, `UNKNOWN_DEVICETRUSTLEVEL`, `LOW_TRUST`, `MEDIUM_TRUST`, and `HIGH_TRUST`

            protocols (list): The protocol criteria for the rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            block_override (bool): When set to true, a 'BLOCK' action triggered by the rule could be overridden.
                Defaults to `False`.
            ciparule (bool): The CIPA compliance rule is enabled if this is set to `True`. Defaults to `False`.
            departments (list): The IDs for the departments that this rule applies to.
            devices (list): The IDs for the devices that this rule applies to.
            device_groups (list): The IDs for the device groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            description (str): Additional information about the URL Filtering rule.
            end_user_notification_url (str): URL of end user notification page to be displayed when the rule is matched.
                Not applicable if either ``override_users`` or ``override_groups`` is specified.
            enforce_time_validity (bool): Enforce a set validity time period for the URL Filtering rule.
            groups (list): The IDs for the groups that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            order (str): Order of execution of rule with respect to other URL Filtering rules. Defaults to placing rule
                at the bottom of the list.
            override_users (:obj:`list` of :obj:`int`): The IDs of users that this rule can be overridden for.
                Only applies if ``block_override`` is True, ``action`` is `BLOCK` and ``override_groups`` is not set.
            override_groups (:obj:`list` of :obj:`int`): The IDs of groups that this rule can be overridden for.
                Only applies if ``block_override`` is True and ``action`` is `BLOCK`.
            request_methods (list): The request methods that this rule will apply to. If not specified, the rule will
                apply to all methods.
            size_quota (str): Size quota in KB for applying the URL Filtering rule.
            time_quota (str): Time quota in minutes elapsed after the URL Filtering rule is applied.
            time_windows (list): The IDs for the time windows that this rule applies to.
            url_categories (list): The names of URL categories that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The URL Filter rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`Box`: The newly created URL Filtering Policy rule.

        Examples:
            Add a rule with the minimum required parameters:

            >>> zia.url_filters.add_rule(rank='7',
            ...    name="Empty URL Filter",
            ...    action="ALLOW",
            ...    protocols=['ANY_RULE']

            Add a rule to block HTTP POST to Social Media sites for the Finance department.

            >>> zia.url_filters.add_rule(rank='7',
            ...    name="Block POST to Social Media",
            ...    action="BLOCK",
            ...    protocols=["HTTP_PROXY", "HTTP_RULE", "HTTPS_RULE"],
            ...    request_methods=['POST'],
            ...    departments=["95022175"],
            ...    url_categories=["SOCIAL_NETWORKING"])

        """
        # Convert enabled to API format if present
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        # Initialize the payload with required parameters
        payload = {
            "rank": rank,
            "name": name,
            "action": action,
            "protocols": protocols,
            "order": kwargs.pop("order", len(self.list_rules())),
        }

        # Transform ID fields in kwargs
        transform_common_id_fields(self.reformat_params, kwargs, payload)
        for key, value in kwargs.items():
            if value is not None:
                payload[snake_to_camel(key)] = value

        # Convert the entire payload's keys to camelCase before sending
        camel_payload = recursive_snake_to_camel(payload)
        for key, value in kwargs.items():
            if value is not None:
                camel_payload[snake_to_camel(key)] = value

        # Send POST request to create the rule
        response = self.rest.post("urlFilteringRules", json=payload)
        if isinstance(response, Response):
            # Handle error response
            status_code = response.status_code
            if status_code != 200:
                raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_rule(self, rule_id: str, **kwargs) -> Box:
        """
        Updates the specified URL Filtering Policy rule.

        Args:
            rule_id: The unique ID of the URL Filtering Policy rule to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the rule.
            action (str): Action taken when traffic matches rule criteria. Accepted values are:

                `ANY`, `NONE`, `BLOCK`, `CAUTION`, `ALLOW` and `ICAP_RESPONSE`

            device_trust_levels (list): List of device trust levels for which the rule must be applied. Accepted values are:
                `ANY`, `UNKNOWN_DEVICETRUSTLEVEL`, `LOW_TRUST`, `MEDIUM_TRUST`, and `HIGH_TRUST`

            protocols (list): The protocol criteria for the rule.
            block_override (bool): When set to true, a 'BLOCK' action triggered by the rule could be overridden.
                Defaults to `False`.
            ciparule (bool): The CIPA compliance rule is enabled if this is set to `True`. Defaults to `False`.
            departments (list): The IDs for the departments that this rule applies to.
            devices (list): The IDs for the devices that this rule applies to.
            device_groups (list): The IDs for the device groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            description (str): Additional information about the URL Filtering rule.
            end_user_notification_url (str): URL of end user notification page to be displayed when the rule is matched.
                Not applicable if either ``override_users`` or ``override_groups`` is specified.
            enforce_time_validity (bool): Enforce a set validity time period for the URL Filtering rule.
            groups (list): The IDs for the groups that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            order (str): Order of execution of rule with respect to other URL Filtering rules. Defaults to placing rule
                at the bottom of the list.
            override_users (:obj:`list` of :obj:`int`):
                The IDs of users that this rule can be overridden for.
                Only applies if ``block_override`` is True, ``action`` is `BLOCK` and ``override_groups`` is not set.
            override_groups (:obj:`list` of :obj:`int`):
                The IDs of groups that this rule can be overridden for.
                Only applies if ``block_override`` is True and ``action`` is `BLOCK`.
            request_methods (list): The request methods that this rule will apply to. If not specified, the rule will
                apply to all methods.
            size_quota (str): Size quota in KB for applying the URL Filtering rule.
            time_quota (str): Time quota in minutes elapsed after the URL Filtering rule is applied.
            time_windows (list): The IDs for the time windows that this rule applies to.
            url_categories (list): The names of URL categories that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The URL Filter rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`Box`: The updated URL Filtering Policy rule.

        Examples:
            Update the name of a URL Filtering Policy rule:

            >>> zia.url_filters.update_rule('977467',
            ...    name="Updated Name")

            Add GET to request methods and change action to ALLOW:

            >>> zia.url_filters.update_rule('977468',
            ...    request_methods=['POST', 'GET'],
            ...    action="ALLOW")

        """
        # Set payload to value of existing record and convert nested dict keys.
        payload = convert_keys(self.get_rule(rule_id))

        # Convert enabled to API format if present in kwargs
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        # Transform ID fields in kwargs
        transform_common_id_fields(self.reformat_params, kwargs, payload)

        # Add remaining optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.put(f"urlFilteringRules/{rule_id}", json=payload)
        if isinstance(response, Response) and not response.ok:
            # Handle error response
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

        # Return the updated object
        return self.get_rule(rule_id)

    def delete_rule(self, rule_id: str) -> int:
        """
        Deletes the specified URL Filtering Policy rule.

        Args:
            rule_id (str): The unique ID for the URL Filtering Policy rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.url_filters.delete_rule('977463')

        """
        return self.rest.delete(f"urlFilteringRules/{rule_id}").status_code
