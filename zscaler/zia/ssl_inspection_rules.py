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

from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url, transform_common_id_fields, reformat_params
from zscaler.api_client import APIClient
from zscaler.zia.models.ssl_inspection_rules import SSLInspectionRules


class SSLInspectionAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists ssl inspection rules in your organization.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of ssl inspection rules instances, Response, error).

        Examples:
        >>> rules, response, error = zia.ssl_inspection.list_rules()
        ...    pprint(rule)

        >>> rules, response, error = zia.ssl_inspection.list_rules(
            query_params={"search": "SSL_Inspection_Rule01"})
        ...    pprint(rule)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sslInspectionRules
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(SSLInspectionRules(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_rule(
        self,
        rule_id: int,
    ) -> tuple:
        """
        Returns information for the specified ssl inspection filter rule.

        Args:
            rule_id (str): The unique identifier for the ssl inspection filter rule.

        Returns:
            tuple: A tuple containing (ssl inspection rule instance, Response, error).

        Example:
            Retrieve a ssl inspection rule by its ID:

            >>> rule, response, error = zia.ssl_inspection_rules.get_rule(rule_id=123456)
            >>> if not error:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sslInspectionRules/{rule_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SSLInspectionRules)

        if error:
            return (None, response, error)

        try:
            result = SSLInspectionRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        **kwargs,
    ) -> tuple:
        """
        Adds a new ssl inspection filter rule.

        Args:
            name (str): Name of the rule, max 31 chars.
            ba_rule_action (str): Action to take place if the traffic matches the rule criteria

        Keyword Args:
            description (str): Additional information about the rule
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule. Supported values 1-7
            state (bool): The rule state. Accepted values are True and False.
            road_warrior_for_kerberos (bool): The rule is applied to remote users that use PAC with Kerberos authentication.
            predefined (bool): Indicates that the rule is predefined by using a true value
            default_rule (bool): Indicates whether the rule is the Default Cloud SSL Inspection Rule or not
            device_trust_levels (list): List of device trust levels for which the rule must be applied. Accepted values are:
                `ANY`, `UNKNOWN_DEVICETRUSTLEVEL`, `LOW_TRUST`, `MEDIUM_TRUST`, and `HIGH_TRUST`
            user_agent_types (list): User Agent types on which this rule will be applied. Accepted values are:
                `OPERA`, `FIREFOX`, `MSIE`, `MSEDGE`, `CHROME`, `SAFARI`, `OTHER`, `MSCHREDGE`
            platforms (list): List of device trust levels for which the rule must be applied. Accepted values are:
                `SCAN_IOS`, `SCAN_ANDROID`, `SCAN_MACOS`, `SCAN_WINDOWS`, `NO_CLIENT_CONNECTOR`, `SCAN_LINUX`
            cloud_applications (list): Cloud applications for which the SSL inspection rule is applied.
            url_categories (list): List of URL categories for which rule must be applied
            dest_ip_groups (list): IDs for destination IP groups.
            source_ip_groups (list): IDs for source IP groups.
            devices (list): IDs for devices managed by Zscaler Client Connector.
            device_groups (list): IDs for device groups managed by Zscaler Client Connector.
            groups (list): The IDs for the groups that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            proxy_gateways (list): The proxy chaining gateway for which this rule is applicable.
            time_windows (list): IDs for time windows the rule applies to.
            workload_groups (list): List of workload groups for which this rule is applicable
            zpa_app_segments (list): List of Source IP Anchoring-enabled ZPA Application Segments

        Returns:
            :obj:`Tuple`: New ssl inspection rule resource record.

        Example:
            Add a ssl inspection rule to block specific file types:

            >>> zia.ssl_inspection_rules.add_rule(
            ...    name='SSL_Inspection_Rule-01',
            ...    description='SSL_Inspection_Rule-01',
            ...    state=True
            ...    order=1,
            ...    rank=7,
            ...    road_warrior_for_kerberos=True,
            ...    cloud_appliications=['CHATGPT_AI', 'ANDI'],
            ...    platforms=['SCAN_IOS', 'SCAN_ANDROID', 'SCAN_MACOS', 'SCAN_WINDOWS', 'NO_CLIENT_CONNECTOR', 'SCAN_LINUX'],
            ...    groups=['95016183']
            ...    users=['95016194']
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sslInspectionRules
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SSLInspectionRules)
        if error:
            return (None, response, error)

        try:
            result = SSLInspectionRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> tuple:
        """
        Updates an existing ssl inspection filter rule.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): Name of the rule, max 31 chars.
            description (str): Additional information about the rule
            ba_rule_action (str): Action to take place if the traffic matches the rule criteria
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule. Supported values 1-7
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            first_time_enable (str): Indicates whether a First-Time Action is specifically configured for the rule
            first_time_operation (str): Action that must take place when users download unknown files for the first time
            ml_action_enabled (bool): Indicates whether to enable or disable the AI Instant Verdict option.
            by_threat_score (int): Minimum threat score can be set between 40 to 70.
            groups (list): The IDs for the groups that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            file_types (list): The file types to which the rule applies.
            protocols (list): The protocol criteria for the rule.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.

        Returns:
            tuple: Updated sandbox filter rule resource record.

        Example:
            Update an existing rule to change its name and action:

            >>> zia.ssl_inspection_rules.update_rule(
            ...    rule_id='8566183'
            ...    name='SSL_Inspection_Rule-01',
            ...    description='SSL_Inspection_Rule-01',
            ...    state=True
            ...    order=1,
            ...    rank=7,
            ...    road_warrrior_for_kerberos=True,
            ...    cloud_appliications=['CHATGPT_AI', 'ANDI'],
            ...    platforms=['SCAN_IOS', 'SCAN_ANDROID', 'SCAN_MACOS', 'SCAN_WINDOWS', 'NO_CLIENT_CONNECTOR', 'SCAN_LINUX'],
            ...    groups=['95016183']
            ...    users=['95016194']
            ... )
            >>> if error:
            ...     print(f"Error updating rule: {error}")
            ...     return
            ... print(f"Rule updated successfully: {updated_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sslInspectionRules/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SSLInspectionRules)
        if error:
            return (None, response, error)

        try:
            result = SSLInspectionRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> tuple:
        """
        Deletes the specified ssl inspection filter rule.

        Args:
            rule_id (str): The unique identifier for the ssl inspection rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, error = client.zia.ssl_inspection_rules.delete_rule('5458')
            >>> if error:
            ...     print(f"Error deleting rule: {error}")
            ...     return
            ... print(f"Rule with ID {'5458'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sslInspectionRules/{rule_id}
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
