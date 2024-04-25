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


class ForwardingControlAPI:
    # Forwarding Control filter rule keys that only require an ID to be provided.
    reformat_params = [
        ("app_service_groups", "appServiceGroups"),
        ("departments", "departments"),
        ("devices", "devices"),
        ("device_groups", "deviceGroups"),
        ("dest_ip_groups", "destIpGroups"),
        ("dest_ipv6_groups", "destIpv6Groups"),
        ("ec_groups", "ecGroups"),
        ("groups", "groups"),
        ("labels", "labels"),
        ("locations", "locations"),
        ("location_groups", "locationGroups"),
        ("nw_application_groups", "nwApplicationGroups"),
        ("nw_services", "nwServices"),
        ("nw_service_groups", "nwServiceGroups"),
        ("proxy_gateway", "proxyGateway"),
        ("src_ip_groups", "srcIpGroups"),
        ("src_ipv6_groups", "srcIpv6Groups"),
        ("users", "users"),
        ("zpa_gateway", "zpaGateway"),
        ("zpa_app_segments", "zpaAppSegments"),
        ("zpa_application_segments", "zpaApplicationSegments"),
        ("zpa_application_segment_groups", "zpaApplicationSegmentGroups"),
    ]

    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_rules(self) -> BoxList:
        """
        Returns a list of all forwarding control rules.

        Returns:
            :obj:`BoxList`: The list of forwarding control rules

        Examples:
            >>> for rule in zia.forwarding_control.list_rules():
            ...    pprint(rule)

        """
        response = self.rest.get("/forwardingRules")
        if isinstance(response, Response):
            return None
        return response

    def get_rule(self, rule_id: str) -> Box:
        """
        Returns information for the specified forwarding control filter rule.

        Args:
            rule_id (str): The unique identifier for the forwarding control filter rule.

        Returns:
            :obj:`Box`: The resource record for the forwarding control filter rule.

        Examples:
            >>> pprint(zia.forwarding_control.get_rule('431233'))

        """
        return self.rest.get(f"forwardingRules/{rule_id}")

    def add_rule(self, name: str, forward_method: str, **kwargs) -> Box:
        """
        Adds a new forwarding control filter rule.

        Args:
            name (str): Name of the rule, max 31 chars.
            forward_method (str): Traffic forwarding method. Options: 'INVALID', 'DIRECT',
                'PROXYCHAIN', 'ZIA', 'ZPA', 'ECZPA', 'ECSELF', 'DROP'.

        Keyword Args:
            order (str): Rule order, defaults to bottom.
            rank (str): Admin rank of the rule.
            state (str): Rule state ('ENABLED' or 'DISABLED').
            description (str): Rule description.
            src_ips (list): Source IPs for the rule, accepts IP addresses or CIDR.
            dest_addresses (list): Destination IPs for the rule, accepts IP addresses or CIDR.
            dest_ip_categories (list): IP address categories for the rule.
            dest_countries (list): Destination countries for the rule.
            enable_full_logging (bool): If True, enables full logging.
            nw_applications (list): Network service applications for the rule.
            app_services (list): IDs for application services for the rule.
            app_service_groups (list): IDs for application service groups.
            departments (list): IDs for departments the rule applies to.
            dest_ip_groups (list): IDs for destination IP groups the rule applies to.
            devices (list): IDs for Zscaler Client Connector managed devices.
            device_groups (list): IDs for device groups managed by Zscaler Client Connector.
            groups (list): IDs for groups the rule applies to.
            labels (list): IDs for labels the rule applies to.
            locations (list): IDs for locations the rule applies to.
            location_groups (list): IDs for location groups the rule applies to.
            nw_application_groups (list): IDs for network application groups.
            nw_services (list): IDs for network services the rule applies to.
            nw_service_groups (list): IDs for network service groups the rule applies to.
            time_windows (list): IDs for time windows the rule applies to.
            users (list): IDs for users the rule applies to.

        Returns:
            :obj:`Box`: New forwarding control filter rule resource.

        Examples:
            Forward all traffic to Google DNS:

            >>> zia.forwarding_control.add_rule(rank='7',
            ...    dest_addresses=['8.8.8.8', '8.8.4.4'],
            ...    name='FORWARD_ANY_TO_GOOG-DNS',
            ...    forward_method='DIRECT',
            ...    description='TT#1965432122')

            Block all traffic to Quad9 DNS for Finance Group:

            >>> zia.forwarding_control.add_rule(rank='7',
            ...    dest_addresses=['9.9.9.9'],
            ...    name='BLOCK_FIN_TO_Q9-DNS',
            ...    forward_method='DIRECT',
            ...    groups=['95016183'],
            ...    description='TT#1965432122')
        """
        # Convert enabled to API format if present
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        payload = {
            "name": name,
            "forwardMethod": forward_method,
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
        response = self.rest.post("forwardingRules", json=payload)
        if isinstance(response, Response):
            # Handle error response
            status_code = response.status_code
            if status_code != 200:
                raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_rule(self, rule_id: str, **kwargs) -> Box:
        """
        Updates an existing forwarding control  filter rule.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            description (str): Additional information about the rule
            src_ips (list): The source IPs that this rule applies to. Individual IP addresses or CIDR ranges accepted.
            dest_addresses (list): The destination IP addresses that this rule applies to. Individual IP addresses or
            CIDR ranges accepted.
            dest_ip_categories (list): The IP address categories that this rule applies to.
            dest_countries (list): The destination countries that this rule applies to.
            enable_full_logging (bool): Enables full logging if True.
            nw_applications (list): The network service applications that this rule applies to.
            app_services (list): The IDs for the application services that this rule applies to.
            app_service_groups (list): The IDs for the application service groups that this rule applies to.
            departments (list): The IDs for the departments that this rule applies to.
            dest_ip_groups (list): The IDs for the destination IP groups that this rule applies to.
            groups (list): The IDs for the groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            nw_application_groups (list): The IDs for the network application groups that this rule applies to.
            nw_services (list): The IDs for the network services that this rule applies to.
            nw_service_groups (list): The IDs for the network service groups that this rule applies to.
            time_windows (list): The IDs for the time windows that this rule applies to.
            users (list): The IDs for the users that this rule applies to.

        Returns:
            :obj:`Box`: The updated forwarding control filter rule resource record.

        Examples:
            Update the destination IP addresses for a rule:

            >>> zia.forwarding_control.update_rule('976598',
            ...    dest_addresses=['1.1.1.1'],
            ...    description="TT#1965232865")

            Update a rule description:

            >>> zia.forwarding_control.update_rule('976597',
            ...    description="TT#1965232866")

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

        response = self.rest.put(f"forwardingRules/{rule_id}", json=payload)
        if isinstance(response, Response) and not response.ok:
            # Handle error response
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

        # Return the updated object
        return self.get_rule(rule_id)

    def delete_rule(self, rule_id: str) -> int:
        """
        Deletes the specified forwarding control filter rule.

        Args:
            rule_id (str): The unique identifier for the forwarding control filter rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.forwarding_control.delete_rule('278454')

        """
        return self.rest.delete(f"forwardingRules/{rule_id}").status_code
