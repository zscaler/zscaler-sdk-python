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
from zscaler.zia.models.filetyperules import FileTypeControlRules


class FileTypeControlRuleAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists file type control rules rules in your organization with pagination.
        A subset of file type control rules rules  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of file type control rules rules instances, Response, error).

        Example:
            List all file type control rules rules with a specific page size:

            >>> rules_list, response, error = zia.file_type_control_rule.list_rules(
            ...    query_params={"pagesize": 50}
            ... )
            >>> for rule in rules_list:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /fileTypeRules
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(FileTypeControlRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_rule(
        self,
        rule_id: int,
    ) -> tuple:
        """
        Returns information for the specified file type control rules filter rule.

        Args:
            rule_id (str): The unique identifier for the file type control rules filter rule.

        Returns:
            tuple: A tuple containing (file type control rules rule instance, Response, error).

        Example:
            Retrieve a file type control rules rule by its ID:

            >>> rule, response, error = zia.file_type_control_rule.get_rule(rule_id=123456)
            >>> if not error:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /fileTypeRules/{rule_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, FileTypeControlRules)

        if error:
            return (None, response, error)

        try:
            result = FileTypeControlRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        **kwargs,
    ) -> tuple:
        """
        Adds a new file type control rules rule.

        Args:
            name (str): Name of the rule, max 31 chars.

        Keyword Args:
            description (str): Additional information about the rule.
            state (str): Rule state, either 'ENABLED' or 'DISABLED'.
            order (int): Order of policy execution with respect to other file-type policies.
            filtering_action (str): Action taken when traffic matches policy. Supported values: "BLOCK", "CAUTION", "ALLOW".
            time_quota (int): Time quota in minutes after which the policy must be applied.
            size_quota (int): Size quota in KB beyond which the policy must be applied.
            access_control (str): Access privilege based on admin's state.
            rank (int): Admin rank of the rule creator. Supported values: 1-7.
            capture_pcap (bool): Indicates whether packet capture (PCAP) is enabled.
            operation (str): File operation performed by the rule.
            active_content (bool): Checks whether the file contains active content.
            unscannable (bool): Indicates whether the file is unscannable.
            cloud_applications (list[str]): List of cloud applications to which the rule must be applied.
            file_types (list[str]): List of file types to which the rule must be applied.
            min_size (int): Minimum file size in KB for evaluation.
            max_size (int): Maximum file size in KB for evaluation.
            protocols (list[str]): Protocols covered by the rule.
            url_categories (list[str]): List of URL categories the rule must be applied to.
            last_modified_time (int): Timestamp of the last modification.
            last_modified_by (dict): Details of the user who last modified the rule.
            locations (list[dict]): Name-ID pairs of locations for rule application.
            location_groups (list[dict]): Name-ID pairs of location groups for rule application.
            groups (list[dict]): Name-ID pairs of groups for rule application.
            departments (list[dict]): Name-ID pairs of departments for rule application.
            users (list[dict]): Name-ID pairs of users for rule application.
            time_windows (list[dict]): Name-ID pairs of time intervals for rule enforcement.
            labels (list[dict]): Labels associated with the rule for logical grouping.
            device_groups (list[dict]): Device groups managed using Zscaler Client Connector.
            devices (list[dict]): Devices managed using Zscaler Client Connector.
            device_trust_levels (list[str]): Device trust levels based on posture configurations.
            zpa_app_segments (list[dict]): ZPA Application Segments applicable to the rule.

        Returns:
            tuple: Updated firewall dns filtering rule resource record.

        Example:
            Update an existing rule to change its name and action:

            >>> zia.file_type_control_rule.update_rule(
            ...    rule_id=123456,
            ...    name='UPDATED_RULE',
            ...    ba_rule_action='ALLOW',
            ...    description='Updated action for the rule'
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /fileTypeRules
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, FileTypeControlRules)
        if error:
            return (None, response, error)

        try:
            result = FileTypeControlRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> tuple:
        """
        Updates an existing file type control rules rule.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): Name of the rule, max 31 chars.
            description (str): Additional information about the rule.
            state (str): Rule state, either 'ENABLED' or 'DISABLED'.
            order (int): Order of policy execution with respect to other file-type policies.
            filtering_action (str): Action taken when traffic matches policy. Supported values: "BLOCK", "CAUTION", "ALLOW".
            time_quota (int): Time quota in minutes after which the policy must be applied.
            size_quota (int): Size quota in KB beyond which the policy must be applied.
            access_control (str): Access privilege based on admin's state.
            rank (int): Admin rank of the rule creator. Supported values: 1-7.
            capture_pcap (bool): Indicates whether packet capture (PCAP) is enabled.
            operation (str): File operation performed by the rule.
            active_content (bool): Checks whether the file contains active content.
            unscannable (bool): Indicates whether the file is unscannable.
            cloud_applications (list[str]): List of cloud applications to which the rule must be applied.
            file_types (list[str]): List of file types to which the rule must be applied.
            min_size (int): Minimum file size in KB for evaluation.
            max_size (int): Maximum file size in KB for evaluation.
            protocols (list[str]): Protocols covered by the rule.
            url_categories (list[str]): List of URL categories the rule must be applied to.
            last_modified_time (int): Timestamp of the last modification.
            last_modified_by (dict): Details of the user who last modified the rule.
            locations (list[dict]): Name-ID pairs of locations for rule application.
            location_groups (list[dict]): Name-ID pairs of location groups for rule application.
            groups (list[dict]): Name-ID pairs of groups for rule application.
            departments (list[dict]): Name-ID pairs of departments for rule application.
            users (list[dict]): Name-ID pairs of users for rule application.
            time_windows (list[dict]): Name-ID pairs of time intervals for rule enforcement.
            labels (list[dict]): Labels associated with the rule for logical grouping.
            device_groups (list[dict]): Device groups managed using Zscaler Client Connector.
            devices (list[dict]): Devices managed using Zscaler Client Connector.
            device_trust_levels (list[str]): Device trust levels based on posture configurations.
            zpa_app_segments (list[dict]): ZPA Application Segments applicable to the rule.

        Returns:
            tuple: Updated firewall dns filtering rule resource record.

        Example:
            Update an existing rule to change its name and action:

            >>> zia.file_type_control_rule.update_rule(
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
            /fileTypeRules/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, FileTypeControlRules)
        if error:
            return (None, response, error)

        try:
            result = FileTypeControlRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> tuple:
        """
        Deletes the specified file type control rules filter rule.

        Args:
            rule_id (str): The unique identifier for the file type control rules rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.file_type_control_rule.delete_rule('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /fileTypeRules/{rule_id}
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
