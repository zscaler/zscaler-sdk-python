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
from zscaler.zia.models.sandboxrules import SandboxRules


class SandboxRulesAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists sandbox rules in your organization with pagination.
        A subset of sandbox rules  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of sandbox rules instances, Response, error).

        Example:
            List all sandbox rules with a specific page size:

            >>> rules_list, response, error = zia.sandbox_rules.list_rules()
            >>> for rule in rules_list:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sandboxRules
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
                results.append(SandboxRules(self.form_response_body(item)))
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
        Returns information for the specified sandbox filter rule.

        Args:
            rule_id (str): The unique identifier for the sandbox filter rule.

        Returns:
            tuple: A tuple containing (sandbox rule instance, Response, error).

        Example:
            Retrieve a sandbox rule by its ID:

            >>> fetched_rule, _, error = client.zia.sandbox_rules.get_rule('5422385')
            >>> if error:
            ...     print(f"Error fetching rule by ID: {error}")
            ...     return
            ... print(f"Fetched rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sandboxRules/{rule_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SandboxRules)

        if error:
            return (None, response, error)

        try:
            result = SandboxRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        **kwargs,
    ) -> tuple:
        """
        Adds a new sandbox filter rule.

        Args:
            name (str): Name of the rule, max 31 chars.
            ba_rule_action (str): Action to take place if the traffic matches the rule criteria

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule. Supported values 1-7
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            description (str): Additional information about the rule
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
            :obj:`Tuple`: New sandbox rule resource record.

        Example:
            Add a sandbox rule to block specific file types:

            >>> added_rule, _, error = client.zia.sandbox_rules.add_rule(
            ...     name=f"NewRule {random.randint(1000, 10000)}",
            ...     description=f"NewRule {random.randint(1000, 10000)}",
            ...     ba_rule_action='BLOCK',
            ...     state="ENABLED",
            ...     order=1,
            ...     rank=7,
            ...     first_time_enable=True,
            ...     ml_action_enabled=True,
            ...     first_time_operation="ALLOW_SCAN",
            ...     url_categories = ["OTHER_ADULT_MATERIAL"],
            ...     protocols=["FOHTTP_RULE", "FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
            ...     ba_policy_categories=["ADWARE_BLOCK", "BOTMAL_BLOCK", "ANONYP2P_BLOCK",
            ...     "RANSOMWARE_BLOCK", "OFFSEC_TOOLS_BLOCK", "SUSPICIOUS_BLOCK"],
            ...     file_types=["FTCATEGORY_BZIP2", "FTCATEGORY_P7Z"],
            ...     by_threat_score=40,
            ...     groups=['12006601'],
            ...     departments=['15616629'],
            ... )
            >>> if error:
            ...     print(f"Error adding rule: {error}")
            ...     return
            ... print(f"Rule added successfully: {added_rule.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sandboxRules
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

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

        response, error = self._request_executor.execute(request, SandboxRules)
        if error:
            return (None, response, error)

        try:
            result = SandboxRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> tuple:
        """
        Updates an existing sandbox filter rule.

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

            >>> updated_rule, _, error = client.zia.sandbox_rules.update_rule(
            ...     name=f"UpdateRule_{random.randint(1000, 10000)}",
            ...     description=f"UpdateRule_{random.randint(1000, 10000)}",
            ...     ba_rule_action='BLOCK',
            ...     state="ENABLED",
            ...     order=1,
            ...     rank=7,
            ...     first_time_enable=True,
            ...     ml_action_enabled=True,
            ...     first_time_operation="ALLOW_SCAN",
            ...     url_categories = ["OTHER_ADULT_MATERIAL"],
            ...     protocols=["FOHTTP_RULE", "FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
            ...     ba_policy_categories=["ADWARE_BLOCK", "BOTMAL_BLOCK", "ANONYP2P_BLOCK",
            ...     "RANSOMWARE_BLOCK", "OFFSEC_TOOLS_BLOCK", "SUSPICIOUS_BLOCK"],
            ...     file_types=["FTCATEGORY_BZIP2", "FTCATEGORY_P7Z"],
            ...     by_threat_score=40,
            ...     groups=['12006601'],
            ...     departments=['15616629'],
            ... )
            >>> if error:
            ...     print(f"Error adding rule: {error}")
            ...     return
            ... print(f"Rule added successfully: {updated_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sandboxRules/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

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

        response, error = self._request_executor.execute(request, SandboxRules)
        if error:
            return (None, response, error)

        try:
            result = SandboxRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> tuple:
        """
        Deletes the specified sandbox filter rule.

        Args:
            rule_id (str): The unique identifier for the sandbox rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, error = client.zia.sandbox_rules.delete_rule('544852')
            >>> if error:
            ...     print(f"Error deleting rule: {error}")
            ...     return
            ... print(f"Rule with ID {'544852'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sandboxRules/{rule_id}
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
