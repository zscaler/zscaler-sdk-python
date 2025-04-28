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
from zscaler.zia.models.bandwidth_control_rules import BandwidthControlRules


class BandwidthControlRulesAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        List bandwidth control rules in your organization.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:
            tuple: A tuple containing (list of sandbox rules instances, Response, error).

        Example:
            List all cloud bandwidth control rules:

            >>> rules_list, response, error = client.zia.bandwidth_control_rules.list_rules()
            ... if error:
            ...    print(f"Error listing bandwidth control rules: {error}")
            ...    return
            ... print(f"Total rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...    print(rule.as_dict())

            filtering rule results by rule name :

            >>> rules_list, response, error = client.zia.bandwidth_control_rules.list_rules(
                query_params={"search": Rule01}
            )
            ... if error:
            ...    print(f"Error listing bandwidth control rules: {error}")
            ...    return
            ... print(f"Total rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthControlRules
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
                results.append(BandwidthControlRules(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def list_rules_lite(self) -> tuple:
        """
        Fetches a specific bandwidth control rule lite.

        Args:
            bwd_id (int): The unique identifier for the Bandwidth control rule Lite.

        Returns:
            tuple: A tuple containing (Bandwidth Control Rules instance, Response, error).
            
        Example:
            List all cloud bandwidth control rules:

            >>> rules_list, response, error = client.zia.bandwidth_control_rules.list_rules_lite()
            ... if error:
            ...    print(f"Error listing bandwidth control rules: {error}")
            ...    return
            ... print(f"Total rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthControlRules/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BandwidthControlRules)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(BandwidthControlRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_rule(
        self,
        rule_id: int,
    ) -> tuple:
        """
        Returns information for the specified bandwidth control rule.

        Args:
            rule_id (str): The unique identifier for the bandwidth control rule.

        Returns:
            tuple: A tuple containing (bandwidth control rule instance, Response, error).

        Example:
            Retrieve a cloud bandwidth control rule by its ID:

        >>> fetched_rule, response, error = client.zia.bandwidth_control_rules.get_rule('960061')
        ... if error:
        ...     print(f"Error fetching rule by ID: {error}")
        ...     return
        ... print(f"Fetched rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthControlRules/{rule_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BandwidthControlRules)

        if error:
            return (None, response, error)

        try:
            result = BandwidthControlRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        **kwargs,
    ) -> tuple:
        """
        Adds a new cloud bandwidth control rule.

        Args:
            name (str): Name of the rule, max 31 chars.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule. Supported values 1-7
            enabled (bool): The rule state.
            description (str): Additional information about the rule
            default_rule (bool): Indicates whether the rule is the Default Cloud IPS Rule or not
            bandwidth_class_ids (list): The bandwidth classes to which you want to apply this rule.
                You first must add URLs or cloud applications to predefined or custom bandwidth classes.
            max_bandwidth (int): The maximum percentage of a location's bandwidth to be guaranteed for each selected bandwidth class.
                This percentage includes bandwidth for uploads and downloads.
            min_bandwidth (int): The minimum percentage of a location's bandwidth you want to be guaranteed for each selected bandwidth class.
                This percentage includes bandwidth for uploads and downloads.
            protocols (list): The protocol criteria for the rule.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): IDs for time windows the rule applies to.

        Returns:
            :obj:`tuple`: New bandwidth control rule resource record.

        Example:
            Add a bandwidth control rule to block specific file types:

            >>> zia.bandwidth_control_rules.add_rule(
            ...    name='BLOCK_EXE_FILES',
            ...    ba_rule_action='BLOCK',
            ...    file_types=['FTCATEGORY_EXE', 'FTCATEGORY_DLL'],
            ...    protocols=['HTTP_RULE', 'HTTPS_RULE'],
            ...    state='ENABLED'
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthControlRules
        """
        )

        body = kwargs

        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BandwidthControlRules)
        if error:
            return (None, response, error)

        try:
            result = BandwidthControlRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> tuple:
        """
        Updates an existing bandwidth control rule.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule. Supported values 1-7
            enabled (bool): The rule state.
            description (str): Additional information about the rule
            default_rule (bool): Indicates whether the rule is the Default Cloud IPS Rule or not
            bandwidth_classes (list): The bandwidth classes to which you want to apply this rule.
                You first must add URLs or cloud applications to predefined or custom bandwidth classes.
            max_bandwidth (int): The maximum percentage of a location's bandwidth to be guaranteed for each selected bandwidth class.
                This percentage includes bandwidth for uploads and downloads.
            min_bandwidth (int): The minimum percentage of a location's bandwidth you want to be guaranteed for each selected bandwidth class.
                This percentage includes bandwidth for uploads and downloads.
            protocols (list): The protocol criteria for the rule.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): IDs for time windows the rule applies to.

        Returns:
            tuple: Updated bandwidth control rule resource record.

        Example:
            Update an existing rule to change its name and action:

            >>> zia.bandwidth_control_rules.update_rule(
            ...    rule_id=123456,
            ...    name='UPDATED_RULE',
            ...    ba_rule_action='ALLOW',
            ...    description='Updated action for the rule'
            ... )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthControlRules/{rule_id}
        """
        )

        body = kwargs

        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BandwidthControlRules)
        if error:
            return (None, response, error)

        try:
            result = BandwidthControlRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> tuple:
        """
        Deletes the specified bandwidth control rule.

        Args:
            rule_id (str): The unique identifier for the bandwidth control rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.cloudBandwidthControlRules.delete_rule('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthControlRules/{rule_id}
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
