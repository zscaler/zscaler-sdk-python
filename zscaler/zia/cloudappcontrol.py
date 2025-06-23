"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.cloudappcontrol import CloudApplicationControl
from zscaler.utils import transform_common_id_fields, format_url, reformat_params


class CloudAppControlAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_available_actions(self, rule_type: str, cloud_apps: list) -> tuple:
        """
        Retrieves a list of granular actions supported for a specific rule type.

        Args:
            **rule_type (str): The type of rule for which actions should be retrieved.
            **cloud_apps (list): A list of cloud applications for filtering.

        Returns:
            tuple: A tuple containing:
                - result (list): A list of actions supported for the given rule type.
                - response (object): The full API response object.
                - error (object): Any error encountered during the request.

        Examples:
            Retrieve available actions for a specific rule type:
                >>> actions, response, error = zia.cloudappcontrol.list_available_actions(
                ...     rule_type='STREAMING_MEDIA',
                ...     cloud_apps=['DROPBOX']
                ... )
                >>> if actions:
                ...     for action in actions:
                ...         print(action)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /webApplicationRules/{rule_type}/availableActions
            """
        )

        body = {"cloudApps": cloud_apps}

        request, error = self._request_executor.create_request(http_method, api_url, body, {})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
            if not isinstance(result, list):
                raise ValueError("Unexpected response format: Expected a list.")
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_rules(
        self,
        rule_type: str,
        query_params=None,
    ) -> tuple:
        """
        Returns a list of all Cloud App Control rules for the specified rule type.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

                ``[query_params.rule_type]`` {str}: The type of rules to retrieve (e.g., "STREAMING_MEDIA").

        Returns:
            tuple: The list of Cloud App Control rules.

        Examples:
            List all rules for a specific type::

                >>> for rule in zia.cloudappcontrol.list_rules('STREAMING_MEDIA'):
                ...    pprint(rule)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /webApplicationRules/{rule_type}
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CloudApplicationControl(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_rule(self, rule_type: str, rule_id: str) -> tuple:
        """
        Returns information for the specified Cloud App Control rule under the specified rule type.

        Args:
            rule_type (str): The type of the rule (e.g., "STREAMING_MEDIA").
            rule_id (str): The unique identifier for the Cloud App Control rule.

        Returns:
            :obj:`Tuple`: The resource record for the Cloud App Control rule.

        Examples:
            Get a specific rule by ID and type::

                >>> pprint(zia.cloudappcontrol.get_rule('STREAMING_MEDIA', '431233'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /webApplicationRules/{rule_type}/{rule_id}
        """
        )

        body = {}
        headers = {}

        # Create the reques
        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, CloudApplicationControl)

        if error:
            return (None, response, error)

        # Parse the response
        try:
            result = CloudApplicationControl(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_rule_type_mapping(self) -> tuple:
        """
        Gets the backend keys that match the application type string.

        Returns:
            :obj:`Tuple`: The resource record for rule type mapping.

        Examples:
            Get a specific rule by ID and type::

                >>> pprint(zia.cloudappcontrol.get_rule_type_mapping()

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /webApplicationRules/ruleTypeMapping
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(self, rule_type: str, **kwargs) -> tuple:
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
            :obj:`Tuple`: New cloud app control filter rule resource.

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
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /webApplicationRules/{rule_type}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CloudApplicationControl)
        if error:
            return (None, response, error)

        try:
            result = CloudApplicationControl(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_rule(self, rule_type: str, rule_id: str, **kwargs) -> tuple:
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
            :obj:`Tuple`: New cloud app control filter rule resource.

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
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /webApplicationRules/{rule_type}/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = CloudApplicationControl(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_type: str, rule_id: int) -> tuple:
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
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /webApplicationRules/{rule_type}/{rule_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)

    def add_duplicate_rule(self, rule_type: str, rule_id: str, name: str, **kwargs) -> tuple:
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
            tuple: A tuple containing:
                - result (CloudApplicationControl): The newly duplicated cloud app control filter rule.
                - response (object): The full API response object.
                - error (object): Any error encountered during the request.

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
        http_method = "post".upper()
        params = {"name": name}
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /webApplicationRules/{rule_type}/duplicate/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CloudApplicationControl)
        if error:
            return (None, response, error)

        try:
            result = CloudApplicationControl(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
