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

        Note: This API endpoint can be accessed only through Zscaler OneAPI with the correct access
        token included in the request's Authorization header.

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

        Note: This API endpoint can be accessed only through Zscaler OneAPI with the correct access
        token included in the request's Authorization header.

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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

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

        Note: This API endpoint can be accessed only through Zscaler OneAPI with the correct access
        token included in the request's Authorization header.

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

        Note: This API endpoint can be accessed only through Zscaler OneAPI with the correct access
        token included in the request's Authorization header.

        Args:
            name (str): Name of the rule, max 31 chars.

        Keyword Args:
            order (str): Rule order, defaults to bottom of the list.
            rank (str): Admin rank for the rule. Supported values 1-7.
            enabled (bool): Whether the rule is enabled or disabled.
            description (str): Additional description for the rule.
            default_rule (bool): Whether the rule is the default bandwidth control rule.
            bandwidth_class_ids (list): IDs of bandwidth classes this rule applies to.
            max_bandwidth (int): Maximum % of location bandwidth for each selected class (upload + download).
            min_bandwidth (int): Minimum % of location bandwidth guaranteed for each selected class (upload + download).
            protocols (list): Protocols to which the rule applies.
            labels (list): IDs of labels this rule applies to.
            locations (list): IDs of locations this rule applies to.
            location_groups (list): IDs of location groups this rule applies to.
            time_windows (list): IDs of time windows this rule applies to.

        Returns:
            :obj:`tuple`: New bandwidth control rule resource record.

        Example:
            Add a bandwidth control rule:

            >>> added_rule, _, error = client.zia.bandwidth_control_rules.add_rule(
            ...     name=f"NewBWDRule_{random.randint(1000, 10000)}",
            ...     description=f"NewBWDRule_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     order=1,
            ...     max_bandwidth='100',
            ...     min_bandwidth='20',
            ...     bandwidth_class_ids=['4', '8'],
            ...     protocols=[ "WEBSOCKETSSL_RULE", "WEBSOCKET_RULE", "DOHTTPS_RULE"],
                )
            >>> if error:
            ...     print(f"Error adding rule: {error}")
            ...     return
            ... print(f"Rule added successfully: {added_rule.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthControlRules
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
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

        Note: This API endpoint can be accessed only through Zscaler OneAPI with the correct access
        token included in the request's Authorization header.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            order (str): Rule order, defaults to bottom of the list.
            rank (str): Admin rank for the rule. Supported values 1-7.
            enabled (bool): Whether the rule is enabled or disabled.
            description (str): Additional description for the rule.
            default_rule (bool): Whether the rule is the default bandwidth control rule.
            bandwidth_class_ids (list): IDs of bandwidth classes this rule applies to.
            max_bandwidth (int): Maximum % of location bandwidth for each selected class (upload + download).
            min_bandwidth (int): Minimum % of location bandwidth guaranteed for each selected class (upload + download).
            protocols (list): Protocols to which the rule applies.
            labels (list): IDs of labels this rule applies to.
            locations (list): IDs of locations this rule applies to.
            location_groups (list): IDs of location groups this rule applies to.
            time_windows (list): IDs of time windows this rule applies to.

        Returns:
            tuple: Updated bandwidth control rule resource record.

        Example:
            Add a bandwidth control rule:

            >>> updated_rule, _, error = client.zia.bandwidth_control_rules.add_rule(
            ...     rule_id='15545'
            ...     name=f"UpdateBWDRule_{random.randint(1000, 10000)}",
            ...     description=f"UpdateBWDRule_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     order=1,
            ...     max_bandwidth='100',
            ...     min_bandwidth='20',
            ...     bandwidth_class_ids=['4', '8'],
            ...     protocols=[ "WEBSOCKETSSL_RULE", "WEBSOCKET_RULE", "DOHTTPS_RULE"],
                )
            >>> if error:
            ...     print(f"Error adding rule: {error}")
            ...     return
            ... print(f"Rule added successfully: {updated_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthControlRules/{rule_id}
        """
        )

        body = kwargs
        body["id"] = rule_id

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

        Note: This API endpoint can be accessed only through Zscaler OneAPI with the correct access
        token included in the request's Authorization header.

        Args:
            rule_id (str): The unique identifier for the bandwidth control rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Delete a Bandwidth rule:

            >>> _, _, error = client.zia.bandwidth_control_rules.delete_delete_ruled_class('125454')
            >>>     if error:
            ...         print(f"Error deleting Bandwidth rule: {error}")
            ...         return
            ...     print(f"Bandwidth rule with ID {'125454'} deleted successfully.")
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
