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

from typing import List
from box import Box, BoxList
from requests import Response

from zscaler.utils import (
    convert_keys,
    recursive_snake_to_camel,
    snake_to_camel,
    transform_common_id_fields,
)
from zscaler.zia import ZIAClient


class CloudAppControlAPI:
    # Cloud App Control filter rule keys that only require an ID to be provided.
    reformat_params = [
        ("cbi_profile", "cbiProfile"),
        ("departments", "departments"),
        ("devices", "devices"),
        ("device_groups", "deviceGroups"),
        ("groups", "groups"),
        ("labels", "labels"),
        ("locations", "locations"),
        ("time_windows", "timeWindows"),
        ("location_groups", "locationGroups"),
        ("tenancy_profile_ids", "tenancyProfileIds"),
        ("sharing_domain_profiles", "sharingDomainProfiles"),
        ("form_sharing_domain_profiles", "formSharingDomainProfiles"),
        ("users", "users"),
    ]

    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_available_actions(self, rule_type: str, cloud_apps: List[str]) -> BoxList:
        """
        Returns a list of granular actions supported for applications based on rule type.

        Args:
            rule_type (str): The type of rules to retrieve (e.g., "STREAMING_MEDIA").
            cloud_apps (list): The list of cloud applications to retrieve actions for.

        Returns:
            :obj:`BoxList`: The list of granular available actions.

        Examples:
            List all available actions for a specific rule type::

                >>> for actions in zia.cloudappcontrol.list_available_actions(
                ...     'STREAMING_MEDIA',
                ...     cloud_apps=['DROPBOX']
                ... ):
                ...    pprint(actions)

        """
        payload = {"cloudApps": cloud_apps}
        return self.rest.post(f"webApplicationRules/{rule_type}/availableActions", json=payload)

    def list_rules(self, rule_type: str) -> BoxList:
        """
        Returns a list of all Cloud App Control rules for the specified rule type.

        Args:
            rule_type (str): The type of rules to retrieve (e.g., "STREAMING_MEDIA").

        Returns:
            :obj:`BoxList`: The list of Cloud App Control rules.

        Examples:
            List all rules for a specific type::

                >>> for rule in zia.cloudappcontrol.list_rules('STREAMING_MEDIA'):
                ...    pprint(rule)

        """
        return self.rest.get(f"webApplicationRules/{rule_type}")

    def get_rule(self, rule_type: str, rule_id: str) -> Box:
        """
        Returns information for the specified Cloud App Control rule under the specified rule type.

        Args:
            rule_type (str): The type of the rule (e.g., "STREAMING_MEDIA").
            rule_id (str): The unique identifier for the Cloud App Control rule.

        Returns:
            :obj:`Box`: The resource record for the Cloud App Control rule.

        Examples:
            Get a specific rule by ID and type::

                >>> pprint(zia.cloudappcontrol.get_rule('STREAMING_MEDIA', '431233'))

        """
        return self.rest.get(f"webApplicationRules/{rule_type}/{rule_id}")

    def get_rule_by_name(self, rule_type: str, rule_name: str) -> Box:
        """
        Retrieves a specific Cloud App Control rule by its name and type.

        Args:
            rule_type (str): The type of rules to search within (e.g., "WEBMAIL").
            rule_name (str): The name of the rule to retrieve.

        Returns:
            :obj:`Box`: The Cloud App Control rule if found, otherwise None.

        Examples:
            >>> rule = zia.cloudappcontrol.get_rule_by_name('WEBMAIL', 'Webmail Rule-1')
            ...    print(rule)
        """
        rules = self.list_rules(rule_type)
        for rule in rules:
            if rule.get("name") == rule_name:
                return rule
        return None

    def add_rule(self, rule_type: str, name: str, **kwargs) -> Box:
        """
        Adds a new cloud app control filter rule.

        Args:
            rule_type (str): The type of the rule (e.g., "STREAMING_MEDIA").
            name (str): Name of the rule, max 31 chars.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            enabled (bool): The rule state.
            description (str): Additional information about the rule.
            applications (list): The IDs for the applications that this rule applies to.
            departments (list): The IDs for the departments that this rule applies to.
            groups (list): The IDs for the groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): The IDs for the time windows that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            enforce_time_validity (bool): Enforce a set validity time period for the cloud app control rule.
            size_quota (str): Size quota in KB for applying the Cloud App Control rule.
            time_quota (str): Time quota in minutes elapsed after the Cloud App Control rule is applied.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The Cloud App Control rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`Box`: New cloud app control filter rule resource.

        Examples:
            Allow Webmail Application::

                >>> zia.cloudappcontrol.add_rule('WEBMAIL', name='WEBMAIL_APP_CONTROL_RULE',
                ...    description='TT#1965432122',
                ...    type='WEBMAIL',
                ...    enabled=True,
                ...    rank=7,
                ...    actions=['ALLOW_WEBMAIL_VIEW', 'ALLOW_WEBMAIL_ATTACHMENT_SEND', 'ALLOW_WEBMAIL_SEND'],
                ...    applications=['GOOGLE_WEBMAIL', 'YAHOO_WEBMAIL'],
                ...    device_trust_levels=['UNKNOWN_DEVICETRUSTLEVEL', 'LOW_TRUST', 'MEDIUM_TRUST', 'HIGH_TRUST'],
                )

            Block all Webmail Application for Finance Group::

                >>> zia.cloudappcontrol.add_rule('WEBMAIL', name='WEBMAIL_APP_CONTROL_RULE',
                ...    description='TT#1965432122',
                ...    type='WEBMAIL',
                ...    enabled=True,
                ...    rank=7,
                ...    actions=['BLOCK_WEBMAIL_SEND'],
                ...    applications=['GOOGLE_WEBMAIL', 'YAHOO_WEBMAIL'],
                ...    device_trust_levels=['UNKNOWN_DEVICETRUSTLEVEL', 'LOW_TRUST', 'MEDIUM_TRUST', 'HIGH_TRUST'],
                ...    groups=['17994591'],
                )

        Rule Types and Actions:
            The following are the types and their respective actions:

            - **AI_ML**:
                - `ALLOW_AI_ML_WEB_USE`
                - `CAUTION_AI_ML_WEB_USE`
                - `DENY_AI_ML_WEB_USE`
                - `ISOLATE_AI_ML_WEB_USE`
            - **BUSINESS_PRODUCTIVITY**:
                - `ALLOW_BUSINESS_PRODUCTIVITY_APPS`
                - `BLOCK_BUSINESS_PRODUCTIVITY_APPS`
                - `CAUTION_BUSINESS_PRODUCTIVITY_APPS`
                - `ISOLATE_BUSINESS_PRODUCTIVITY_APPS`
            - **CONSUMER**:
                - `ALLOW_CONSUMER_APPS`
                - `BLOCK_CONSUMER_APPS`
                - `CAUTION_CONSUMER_APPS`
                - `ISOLATE_CONSUMER_APPS`
            - **DNS_OVER_HTTPS**:
                - `ALLOW_DNS_OVER_HTTPS_USE`
                - `DENY_DNS_OVER_HTTPS_USE`
            - **ENTERPRISE_COLLABORATION**:
                - `ALLOW_ENTERPRISE_COLLABORATION_APPS`
                - `BLOCK_ENTERPRISE_COLLABORATION_APPS`
                - `CAUTION_ENTERPRISE_COLLABORATION_APPS`
                - `ISOLATE_ENTERPRISE_COLLABORATION_APPS`
            - **FILE_SHARE**:
                - `ALLOW_FILE_SHARE_VIEW`
                - `ALLOW_FILE_SHARE_UPLOAD`
                - `CAUTION_FILE_SHARE_VIEW`
                - `DENY_FILE_SHARE_VIEW`
                - `DENY_FILE_SHARE_UPLOAD`
                - `ISOLATE_FILE_SHARE_VIEW`
            - **FINANCE**:
                - `ALLOW_FINANCE_USE`
                - `CAUTION_FINANCE_USE`
                - `DENY_FINANCE_USE`
                - `ISOLATE_FINANCE_USE`
            - **HEALTH_CARE**:
                - `ALLOW_HEALTH_CARE_USE`
                - `CAUTION_HEALTH_CARE_USE`
                - `DENY_HEALTH_CARE_USE`
                - `ISOLATE_HEALTH_CARE_USE`
            - **HOSTING_PROVIDER**:
                - `ALLOW_HOSTING_PROVIDER_USE`
                - `CAUTION_HOSTING_PROVIDER_USE`
                - `DENY_HOSTING_PROVIDER_USE`
                - `ISOLATE_HOSTING_PROVIDER_USE`
            - **HUMAN_RESOURCES**:
                - `ALLOW_HUMAN_RESOURCES_USE`
                - `CAUTION_HUMAN_RESOURCES_USE`
                - `DENY_HUMAN_RESOURCES_USE`
                - `ISOLATE_HUMAN_RESOURCES_USE`
            - **INSTANT_MESSAGING**:
                - `ALLOW_CHAT`
                - `ALLOW_FILE_TRANSFER_IN_CHAT`
                - `BLOCK_CHAT`
                - `BLOCK_FILE_TRANSFER_IN_CHAT`
                - `CAUTION_CHAT`
                - `ISOLATE_CHAT`
            - **IT_SERVICES**:
                - `ALLOW_IT_SERVICES_USE`
                - `CAUTION_LEGAL_USE`
                - `DENY_IT_SERVICES_USE`
                - `ISOLATE_IT_SERVICES_USE`
            - **LEGAL**:
                - `ALLOW_LEGAL_USE`
                - `DENY_DNS_OVER_HTTPS_USE`
                - `DENY_LEGAL_USE`
                - `ISOLATE_LEGAL_USE`
            - **SALES_AND_MARKETING**:
                - `ALLOW_SALES_MARKETING_APPS`
                - `BLOCK_SALES_MARKETING_APPS`
                - `CAUTION_SALES_MARKETING_APPS`
                - `ISOLATE_SALES_MARKETING_APPS`
            - **STREAMING_MEDIA**:
                - `ALLOW_STREAMING_VIEW_LISTEN`
                - `ALLOW_STREAMING_UPLOAD`
                - `BLOCK_STREAMING_UPLOAD`
                - `CAUTION_STREAMING_VIEW_LISTEN`
                - `ISOLATE_STREAMING_VIEW_LISTEN`
            - **SOCIAL_NETWORKING**:
                - `ALLOW_SOCIAL_NETWORKING_VIEW`
                - `ALLOW_SOCIAL_NETWORKING_POST`
                - `BLOCK_SOCIAL_NETWORKING_VIEW`
                - `BLOCK_SOCIAL_NETWORKING_POST`
                - `CAUTION_SOCIAL_NETWORKING_VIEW`
            - **SYSTEM_AND_DEVELOPMENT**:
                - `ALLOW_SYSTEM_DEVELOPMENT_APPS`
                - `ALLOW_SYSTEM_DEVELOPMENT_UPLOAD`
                - `BLOCK_SYSTEM_DEVELOPMENT_APPS`
                - `BLOCK_SYSTEM_DEVELOPMENT_UPLOAD`
                - `CAUTION_SYSTEM_DEVELOPMENT_APPS`
                - `ISOLATE_SYSTEM_DEVELOPMENT_APPS`
            - **WEBMAIL**:
                - `ALLOW_WEBMAIL_VIEW`
                - `ALLOW_WEBMAIL_ATTACHMENT_SEND`
                - `ALLOW_WEBMAIL_SEND`
                - `CAUTION_WEBMAIL_VIEW`
                - `BLOCK_WEBMAIL_VIEW`
                - `BLOCK_WEBMAIL_ATTACHMENT_SEND`
                - `BLOCK_WEBMAIL_SEND`
                - `ISOLATE_WEBMAIL_VIEW`
        """
        # Convert enabled to API format if present
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        payload = {
            "name": name,
            "type": rule_type,
            "order": kwargs.pop("order", len(self.list_rules(rule_type))),
        }

        # Transform ID fields in kwargs
        transform_common_id_fields(self.reformat_params, kwargs, payload)

        for key, value in kwargs.items():
            if value is not None:
                if key == "state" and isinstance(value, bool):
                    payload[key] = "ENABLED" if value else "DISABLED"
                else:
                    payload[key] = value

        # Convert the entire payload's keys to camelCase before sending
        camel_payload = recursive_snake_to_camel(payload)
        for key, value in kwargs.items():
            if value is not None:
                camel_payload[snake_to_camel(key)] = value

        response = self.rest.post(f"webApplicationRules/{rule_type}", json=camel_payload)
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_rule(self, rule_type: str, rule_id: str, **kwargs) -> Box:
        """
        Updates a new cloud app control filter rule.

        Args:
            rule_type (str): The type of the rule (e.g., "STREAMING_MEDIA").
            name (str): Name of the rule, max 31 chars.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            enabled (bool): The rule state.
            description (str): Additional information about the rule.
            applications (list): The IDs for the applications that this rule applies to.
            departments (list): The IDs for the departments that this rule applies to.
            groups (list): The IDs for the groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): The IDs for the time windows that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            enforce_time_validity (bool): Enforce a set validity time period for the cloud app control rule.
            size_quota (str): Size quota in KB for applying the Cloud App Control rule.
            time_quota (str): Time quota in minutes elapsed after the Cloud App Control rule is applied.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The Cloud App Control rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`Box`: New cloud app control filter rule resource.

        Examples:
            Allow Webmail Application::

                >>> zia.cloudappcontrol.add_rule('WEBMAIL', name='WEBMAIL_APP_CONTROL_RULE',
                ...    description='TT#1965432122',
                ...    type='WEBMAIL',
                ...    enabled=True,
                ...    rank=7,
                ...    actions=['ALLOW_WEBMAIL_VIEW', 'ALLOW_WEBMAIL_ATTACHMENT_SEND', 'ALLOW_WEBMAIL_SEND'],
                ...    applications=['GOOGLE_WEBMAIL', 'YAHOO_WEBMAIL'],
                ...    device_trust_levels=['UNKNOWN_DEVICETRUSTLEVEL', 'LOW_TRUST', 'MEDIUM_TRUST', 'HIGH_TRUST'],
                )

            Block all Webmail Application for Finance Group::

                >>> zia.cloudappcontrol.add_rule('WEBMAIL', name='WEBMAIL_APP_CONTROL_RULE',
                ...    description='TT#1965432122',
                ...    type='WEBMAIL',
                ...    enabled=True,
                ...    rank=7,
                ...    actions=['BLOCK_WEBMAIL_SEND'],
                ...    applications=['GOOGLE_WEBMAIL', 'YAHOO_WEBMAIL'],
                ...    device_trust_levels=['UNKNOWN_DEVICETRUSTLEVEL', 'LOW_TRUST', 'MEDIUM_TRUST', 'HIGH_TRUST'],
                ...    groups=['17994591'],
                )

        Rule Types and Actions:
            The following are the types and their respective actions:

            - **AI_ML**:
                - `ALLOW_AI_ML_WEB_USE`
                - `CAUTION_AI_ML_WEB_USE`
                - `DENY_AI_ML_WEB_USE`
                - `ISOLATE_AI_ML_WEB_USE`
            - **BUSINESS_PRODUCTIVITY**:
                - `ALLOW_BUSINESS_PRODUCTIVITY_APPS`
                - `BLOCK_BUSINESS_PRODUCTIVITY_APPS`
                - `CAUTION_BUSINESS_PRODUCTIVITY_APPS`
                - `ISOLATE_BUSINESS_PRODUCTIVITY_APPS`
            - **CONSUMER**:
                - `ALLOW_CONSUMER_APPS`
                - `BLOCK_CONSUMER_APPS`
                - `CAUTION_CONSUMER_APPS`
                - `ISOLATE_CONSUMER_APPS`
            - **DNS_OVER_HTTPS**:
                - `ALLOW_DNS_OVER_HTTPS_USE`
                - `DENY_DNS_OVER_HTTPS_USE`
            - **ENTERPRISE_COLLABORATION**:
                - `ALLOW_ENTERPRISE_COLLABORATION_APPS`
                - `BLOCK_ENTERPRISE_COLLABORATION_APPS`
                - `CAUTION_ENTERPRISE_COLLABORATION_APPS`
                - `ISOLATE_ENTERPRISE_COLLABORATION_APPS`
            - **FILE_SHARE**:
                - `ALLOW_FILE_SHARE_VIEW`
                - `ALLOW_FILE_SHARE_UPLOAD`
                - `CAUTION_FILE_SHARE_VIEW`
                - `DENY_FILE_SHARE_VIEW`
                - `DENY_FILE_SHARE_UPLOAD`
                - `ISOLATE_FILE_SHARE_VIEW`
            - **FINANCE**:
                - `ALLOW_FINANCE_USE`
                - `CAUTION_FINANCE_USE`
                - `DENY_FINANCE_USE`
                - `ISOLATE_FINANCE_USE`
            - **HEALTH_CARE**:
                - `ALLOW_HEALTH_CARE_USE`
                - `CAUTION_HEALTH_CARE_USE`
                - `DENY_HEALTH_CARE_USE`
                - `ISOLATE_HEALTH_CARE_USE`
            - **HOSTING_PROVIDER**:
                - `ALLOW_HOSTING_PROVIDER_USE`
                - `CAUTION_HOSTING_PROVIDER_USE`
                - `DENY_HOSTING_PROVIDER_USE`
                - `ISOLATE_HOSTING_PROVIDER_USE`
            - **HUMAN_RESOURCES**:
                - `ALLOW_HUMAN_RESOURCES_USE`
                - `CAUTION_HUMAN_RESOURCES_USE`
                - `DENY_HUMAN_RESOURCES_USE`
                - `ISOLATE_HUMAN_RESOURCES_USE`
            - **INSTANT_MESSAGING**:
                - `ALLOW_CHAT`
                - `ALLOW_FILE_TRANSFER_IN_CHAT`
                - `BLOCK_CHAT`
                - `BLOCK_FILE_TRANSFER_IN_CHAT`
                - `CAUTION_CHAT`
                - `ISOLATE_CHAT`
            - **IT_SERVICES**:
                - `ALLOW_IT_SERVICES_USE`
                - `CAUTION_LEGAL_USE`
                - `DENY_IT_SERVICES_USE`
                - `ISOLATE_IT_SERVICES_USE`
            - **LEGAL**:
                - `ALLOW_LEGAL_USE`
                - `DENY_DNS_OVER_HTTPS_USE`
                - `DENY_LEGAL_USE`
                - `ISOLATE_LEGAL_USE`
            - **SALES_AND_MARKETING**:
                - `ALLOW_SALES_MARKETING_APPS`
                - `BLOCK_SALES_MARKETING_APPS`
                - `CAUTION_SALES_MARKETING_APPS`
                - `ISOLATE_SALES_MARKETING_APPS`
            - **STREAMING_MEDIA**:
                - `ALLOW_STREAMING_VIEW_LISTEN`
                - `ALLOW_STREAMING_UPLOAD`
                - `BLOCK_STREAMING_UPLOAD`
                - `CAUTION_STREAMING_VIEW_LISTEN`
                - `ISOLATE_STREAMING_VIEW_LISTEN`
            - **SOCIAL_NETWORKING**:
                - `ALLOW_SOCIAL_NETWORKING_VIEW`
                - `ALLOW_SOCIAL_NETWORKING_POST`
                - `BLOCK_SOCIAL_NETWORKING_VIEW`
                - `BLOCK_SOCIAL_NETWORKING_POST`
                - `CAUTION_SOCIAL_NETWORKING_VIEW`
            - **SYSTEM_AND_DEVELOPMENT**:
                - `ALLOW_SYSTEM_DEVELOPMENT_APPS`
                - `ALLOW_SYSTEM_DEVELOPMENT_UPLOAD`
                - `BLOCK_SYSTEM_DEVELOPMENT_APPS`
                - `BLOCK_SYSTEM_DEVELOPMENT_UPLOAD`
                - `CAUTION_SYSTEM_DEVELOPMENT_APPS`
                - `ISOLATE_SYSTEM_DEVELOPMENT_APPS`
            - **WEBMAIL**:
                - `ALLOW_WEBMAIL_VIEW`
                - `ALLOW_WEBMAIL_ATTACHMENT_SEND`
                - `ALLOW_WEBMAIL_SEND`
                - `CAUTION_WEBMAIL_VIEW`
                - `BLOCK_WEBMAIL_VIEW`
                - `BLOCK_WEBMAIL_ATTACHMENT_SEND`
                - `BLOCK_WEBMAIL_SEND`
                - `ISOLATE_WEBMAIL_VIEW`
        """
        # Set payload to value of existing record and convert nested dict keys.
        payload = convert_keys(self.get_rule(rule_type, rule_id))

        # Convert enabled to API format if present in kwargs
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        # Transform ID fields in kwargs
        transform_common_id_fields(self.reformat_params, kwargs, payload)

        # Add remaining optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.put(f"webApplicationRules/{rule_type}/{rule_id}", json=payload)
        if isinstance(response, Response) and not response.ok:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
        return self.get_rule(rule_type, rule_id)

    def delete_rule(self, rule_type: str, rule_id: str) -> int:
        """
        Deletes the specified cloud app control filter rule.

        Args:
            rule_type (str): The type of the rule (e.g., "STREAMING_MEDIA").
            rule_id (str): The unique identifier for the cloud app control filter rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.cloudappcontrol.delete_rule('STREAMING_MEDIA', '278454')

        """
        return self.rest.delete(f"webApplicationRules/{rule_type}/{rule_id}").status_code

    def add_duplicate_rule(self, rule_type: str, rule_id: str, name: str, **kwargs) -> Box:
        """
        Adds a new duplicate cloud app control filter rule.

        Args:
            rule_type (str): The type of the rule (e.g., "STREAMING_MEDIA").
            rule_id (str): The ID of the rule to duplicate.
            name (str): Name of the rule, max 31 chars.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            enabled (bool): The rule state.
            description (str): Additional information about the rule.
            applications (list): The IDs for the applications that this rule applies to.
            departments (list): The IDs for the departments that this rule applies to.
            groups (list): The IDs for the groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): The IDs for the time windows that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            enforce_time_validity (bool): Enforce a set validity time period for the cloud app control rule.
            size_quota (str): Size quota in KB for applying the Cloud App Control rule.
            time_quota (str): Time quota in minutes elapsed after the Cloud App Control rule is applied.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The Cloud App Control rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`Box`: New cloud app control filter rule resource.

        Examples:
            Allow Webmail Application::

                >>> zia.cloudappcontrol.add_duplicate_rule('WEBMAIL', '123456',
                ...    name='WEBMAIL_APP_CONTROL_RULE_DUPLICATE',
                ...    description='Duplicated rule',
                ...    enabled=True,
                ...    rank=7,
                ...    actions=['ALLOW_WEBMAIL_VIEW', 'ALLOW_WEBMAIL_ATTACHMENT_SEND', 'ALLOW_WEBMAIL_SEND'],
                ...    applications=['GOOGLE_WEBMAIL', 'YAHOO_WEBMAIL'],
                ...    device_trust_levels=['UNKNOWN_DEVICETRUSTLEVEL', 'LOW_TRUST', 'MEDIUM_TRUST', 'HIGH_TRUST'],
                )

            Block all Webmail Application for Finance Group::

                >>> zia.cloudappcontrol.add_duplicate_rule('WEBMAIL', '123456',
                ...    name='WEBMAIL_APP_CONTROL_RULE_DUPLICATE',
                ...    description='Duplicated rule',
                ...    enabled=True,
                ...    rank=7,
                ...    actions=['BLOCK_WEBMAIL_SEND'],
                ...    applications=['GOOGLE_WEBMAIL', 'YAHOO_WEBMAIL'],
                ...    device_trust_levels=['UNKNOWN_DEVICETRUSTLEVEL', 'LOW_TRUST', 'MEDIUM_TRUST', 'HIGH_TRUST'],
                ...    groups=['17994591'],
                )
        """
        # Convert enabled to API format if present
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        payload = {
            "name": name,
            "type": rule_type,
            "order": kwargs.pop("order", len(self.list_rules(rule_type))),
        }

        # Transform ID fields in kwargs
        transform_common_id_fields(self.reformat_params, kwargs, payload)

        for key, value in kwargs.items():
            if value is not None:
                if key == "state" and isinstance(value, bool):
                    payload[key] = "ENABLED" if value else "DISABLED"
                else:
                    payload[key] = value

        # Convert the entire payload's keys to camelCase before sending
        camel_payload = recursive_snake_to_camel(payload)

        response = self.rest.post(f"webApplicationRules/{rule_type}/duplicate/{rule_id}?name={name}", json=camel_payload)
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response
