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

from typing import List, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.endpoint_dlp_rules import EndpointDlpRules


class EndpointDLPRulesAPI(APIClient):
    """
    A Client object for the Endpoint DLP Rules resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(self, query_params: Optional[dict] = None) -> APIResult[List[EndpointDlpRules]]:
        """
        Lists the endpoint DLP rules configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of EndpointDlpRules instances, Response, error)

        Examples:
            List endpoint DLP rules:

            >>> rule_list, _, error = client.zia.endpoint_dlp_rules.list_rules()
            >>> if error:
            ...     print(f"Error listing endpoint DLP rules: {error}")
            ...     return
            ... print(f"Total endpoint DLP rules found: {len(rule_list)}")
            ... for rule in rule_list:
            ...     print(rule.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules
        """)

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
                result.append(EndpointDlpRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_rule(self, rule_id: int) -> APIResult[EndpointDlpRules]:
        """
        Fetches a specific endpoint DLP rule by ID.

        Args:
            rule_id (int): The unique identifier for the endpoint DLP rule.

        Returns:
            tuple: A tuple containing (EndpointDlpRules instance, Response, error).

        Examples:
            Print a specific endpoint DLP rule:

            >>> fetched_rule, _, error = client.zia.endpoint_dlp_rules.get_rule(1013)
            >>> if error:
            ...     print(f"Error fetching endpoint DLP rule by ID: {error}")
            ...     return
            ... print(f"Fetched endpoint DLP rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules/{rule_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndpointDlpRules)
        if error:
            return (None, response, error)

        try:
            result = EndpointDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(self, **kwargs) -> APIResult[EndpointDlpRules]:
        """
        Creates a new endpoint DLP rule.

        Args:
            name (str): The name of the endpoint DLP rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            state (str): The endpoint DLP rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            order (int): The order of the endpoint DLP rule, defaults to adding the endpoint DLP rule to the bottom of the list.
            rank (int): The admin rank of the endpoint DLP rule.
            file_types (str): The file types for this endpoint DLP rule. Accepted values include e.g. ``ANY``.
            data_transfer_method (str): The data transfer method for this endpoint DLP rule. Accepted values include e.g. ``NETWORK_DRIVE_TRANSFER``.
            description (str): Additional information about the endpoint DLP rule.
            min_size (int): The min size for this endpoint DLP rule.
            action (str): The action taken when traffic matches the endpoint DLP rule criteria.
            external_auditor_email (str): The email address of an external auditor to whom DLP email notifications are sent.
            parent_rule (int): The parent rule for this endpoint DLP rule.
            severity (str): The severity level assigned to the endpoint DLP rule.
            eun_enabled (bool): A Boolean value indicating whether eun is enabled for this endpoint DLP rule.
            eun_template_id (int): The eun template id for this endpoint DLP rule.
            uc_template_id (int): The uc template id for this endpoint DLP rule.
            network_type (str): The network type for this endpoint DLP rule. Accepted values include e.g. ``TRUSTED``.
            without_content_inspection (bool): A Boolean value indicating whether without content inspection applies to this endpoint DLP rule.
            dlp_engines (list): The IDs for the dlp engines that this endpoint DLP rule applies to.
            users (list): The IDs for the users that this endpoint DLP rule applies to.
            groups (list): The IDs for the groups that this endpoint DLP rule applies to.
            departments (list): The IDs for the departments that this endpoint DLP rule applies to.
            devices (list): The IDs for the devices that this endpoint DLP rule applies to.
            device_groups (list): The IDs for the device groups that this endpoint DLP rule applies to.
            device_trust_levels (list): The list of device trust levels for this endpoint DLP rule. Accepted values include e.g. ``ANY``.
            time_windows (list): The IDs for the time windows that this endpoint DLP rule applies to.
            labels (list): The IDs for the labels that this endpoint DLP rule applies to.
            end_point_applications (list): The list of end point applications for this endpoint DLP rule.
            end_point_application_groups (list): The list of end point application groups for this endpoint DLP rule.
            resources (list): The IDs for the resources that this endpoint DLP rule applies to.
            resource_groups (list): The IDs for the resource groups that this endpoint DLP rule applies to.
            user_risk_score_levels (list): The list of user risk score levels for this endpoint DLP rule. Accepted values include e.g. ``ANY``.
            sub_rules (list): The IDs for the sub rules that this endpoint DLP rule applies to.
            notification_template (dict): The ID of the notification template for this endpoint DLP rule, e.g. ``{'id': 12345}``.
            auditor (dict): The ID of the auditor for this endpoint DLP rule, e.g. ``{'id': 12345}``.
            receiver (dict): The ID of the receiver for this endpoint DLP rule, e.g. ``{'id': 12345}``.

        Returns:
            tuple: A tuple containing the newly added EndpointDlpRules instance, response, and error.

        Examples:
            Add a new endpoint DLP rule:

            >>> added_rule, _, error = client.zia.endpoint_dlp_rules.add_rule(
            ...     name=f"NewRule_{random.randint(1000, 10000)}",
            ...     description=f"NewRule_{random.randint(1000, 10000)}",
            ...     state='ENABLED',
            ...     action='ALLOW',
            ...     order=1,
            ...     rank=7,
            ...     device_trust_levels=['ANY'],
            ... )
            >>> if error:
            ...     print(f"Error adding endpoint DLP rule: {error}")
            ...     return
            ... print(f"Endpoint dlp rule added successfully: {added_rule.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndpointDlpRules)
        if error:
            return (None, response, error)

        try:
            result = EndpointDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> APIResult[EndpointDlpRules]:
        """
        Updates information for the specified endpoint DLP rule.

        Args:
            rule_id (int): The unique identifier for the endpoint DLP rule.

        Keyword Args:
            name (str): The name of the endpoint DLP rule.
            state (str): The endpoint DLP rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            order (int): The order of the endpoint DLP rule, defaults to adding the endpoint DLP rule to the bottom of the list.
            rank (int): The admin rank of the endpoint DLP rule.
            file_types (str): The file types for this endpoint DLP rule. Accepted values include e.g. ``ANY``.
            data_transfer_method (str): The data transfer method for this endpoint DLP rule. Accepted values include e.g. ``NETWORK_DRIVE_TRANSFER``.
            description (str): Additional information about the endpoint DLP rule.
            min_size (int): The min size for this endpoint DLP rule.
            action (str): The action taken when traffic matches the endpoint DLP rule criteria.
            external_auditor_email (str): The email address of an external auditor to whom DLP email notifications are sent.
            parent_rule (int): The parent rule for this endpoint DLP rule.
            severity (str): The severity level assigned to the endpoint DLP rule.
            eun_enabled (bool): A Boolean value indicating whether eun is enabled for this endpoint DLP rule.
            eun_template_id (int): The eun template id for this endpoint DLP rule.
            uc_template_id (int): The uc template id for this endpoint DLP rule.
            network_type (str): The network type for this endpoint DLP rule. Accepted values include e.g. ``TRUSTED``.
            without_content_inspection (bool): A Boolean value indicating whether without content inspection applies to this endpoint DLP rule.
            dlp_engines (list): The IDs for the dlp engines that this endpoint DLP rule applies to.
            users (list): The IDs for the users that this endpoint DLP rule applies to.
            groups (list): The IDs for the groups that this endpoint DLP rule applies to.
            departments (list): The IDs for the departments that this endpoint DLP rule applies to.
            devices (list): The IDs for the devices that this endpoint DLP rule applies to.
            device_groups (list): The IDs for the device groups that this endpoint DLP rule applies to.
            device_trust_levels (list): The list of device trust levels for this endpoint DLP rule. Accepted values include e.g. ``ANY``.
            time_windows (list): The IDs for the time windows that this endpoint DLP rule applies to.
            labels (list): The IDs for the labels that this endpoint DLP rule applies to.
            end_point_applications (list): The list of end point applications for this endpoint DLP rule.
            end_point_application_groups (list): The list of end point application groups for this endpoint DLP rule.
            resources (list): The IDs for the resources that this endpoint DLP rule applies to.
            resource_groups (list): The IDs for the resource groups that this endpoint DLP rule applies to.
            user_risk_score_levels (list): The list of user risk score levels for this endpoint DLP rule. Accepted values include e.g. ``ANY``.
            sub_rules (list): The IDs for the sub rules that this endpoint DLP rule applies to.
            notification_template (dict): The ID of the notification template for this endpoint DLP rule, e.g. ``{'id': 12345}``.
            auditor (dict): The ID of the auditor for this endpoint DLP rule, e.g. ``{'id': 12345}``.
            receiver (dict): The ID of the receiver for this endpoint DLP rule, e.g. ``{'id': 12345}``.

        Returns:
            tuple: A tuple containing the updated EndpointDlpRules instance, response, and error.

        Examples:
            Update an existing endpoint DLP rule:

            >>> updated_rule, _, error = client.zia.endpoint_dlp_rules.update_rule(
            ...     rule_id=1013,
            ...     name=f"UpdatedRule_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedRule_{random.randint(1000, 10000)}",
            ...     state='ENABLED',
            ...     action='ALLOW',
            ... )
            >>> if error:
            ...     print(f"Error updating endpoint DLP rule: {error}")
            ...     return
            ... print(f"Endpoint dlp rule updated successfully: {updated_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules/{rule_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndpointDlpRules)
        if error:
            return (None, response, error)

        try:
            result = EndpointDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> APIResult[None]:
        """
        Deletes the specified endpoint DLP rule.

        Args:
            rule_id (int): The unique identifier for the endpoint DLP rule.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a endpoint DLP rule:

            >>> _, _, error = client.zia.endpoint_dlp_rules.delete_rule(1013)
            >>> if error:
            ...     print(f"Error deleting endpoint DLP rule: {error}")
            ...     return
            ... print(f"Endpoint dlp rule deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules/{rule_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def list_file_type_categories(self, query_params: Optional[dict] = None) -> APIResult[list]:
        """
        Lists the file types available in the Endpoint DLP policy rule criteria.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.external]`` {bool}: When true, retrieves the file types available when DLP engines are used with Content Matching enabled; when false, the set available when DLP engines are not used.

        Returns:
            tuple: A tuple containing (list of endpoint DLP rules, Response, error)

        Examples:
            List endpoint DLP rules:

            >>> rule_list, _, error = client.zia.endpoint_dlp_rules.list_file_type_categories()
            >>> if error:
            ...     print(f"Error listing endpoint DLP rules: {error}")
            ...     return
            ... print(f"Total endpoint DLP rules found: {len(rule_list)}")
            ... for rule in rule_list:
            ...     print(rule.as_dict())

            List endpoint DLP rules using filters:

            >>> rule_list, _, error = client.zia.endpoint_dlp_rules.list_file_type_categories(
            ...     query_params={'external': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing endpoint DLP rules: {error}")
            ...     return
            ... print(f"Total endpoint DLP rules found: {len(rule_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules/fileTypeCategories
        """)

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
            result = response.get_results()
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
