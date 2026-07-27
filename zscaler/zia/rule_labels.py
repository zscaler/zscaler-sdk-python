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
from zscaler.zia.models.rule_labels import RuleLabels


class RuleLabelsAPI(APIClient):
    """
    A Client object for the Rule Labels resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_labels(self, query_params: Optional[dict] = None) -> APIResult[List[RuleLabels]]:
        """
        Lists the rule labels configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of RuleLabels instances, Response, error)

        Examples:
            List rule labels:

            >>> label_list, _, error = client.zia.rule_labels.list_labels()
            >>> if error:
            ...     print(f"Error listing rule labels: {error}")
            ...     return
            ... print(f"Total rule labels found: {len(label_list)}")
            ... for label in label_list:
            ...     print(label.as_dict())

            List rule labels using filters:

            >>> label_list, _, error = client.zia.rule_labels.list_labels(
            ...     query_params={'page': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing rule labels: {error}")
            ...     return
            ... print(f"Total rule labels found: {len(label_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels
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
                result.append(RuleLabels(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_label(self, label_id: int) -> APIResult[RuleLabels]:
        """
        Fetches a specific rule label by ID.

        Args:
            label_id (int): The unique identifier for the rule label.

        Returns:
            tuple: A tuple containing (RuleLabels instance, Response, error).

        Examples:
            Print a specific rule label:

            >>> fetched_label, _, error = client.zia.rule_labels.get_label(1013)
            >>> if error:
            ...     print(f"Error fetching rule label by ID: {error}")
            ...     return
            ... print(f"Fetched rule label by ID: {fetched_label.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RuleLabels)
        if error:
            return (None, response, error)

        try:
            result = RuleLabels(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_label(self, **kwargs) -> APIResult[RuleLabels]:
        """
        Creates a new rule label.

        Args:
            name (str): The name of the rule label.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the rule label.
            created_by (str): The created by for this rule label.
            referenced_rule_count (str): The referenced rule count for this rule label.

        Returns:
            tuple: A tuple containing the newly added RuleLabels instance, response, and error.

        Examples:
            Add a new rule label:

            >>> added_label, _, error = client.zia.rule_labels.add_label(
            ...     name=f"NewLabel_{random.randint(1000, 10000)}",
            ...     description=f"NewLabel_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding rule label: {error}")
            ...     return
            ... print(f"Rule label added successfully: {added_label.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RuleLabels)
        if error:
            return (None, response, error)

        try:
            result = RuleLabels(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_label(self, label_id: int, **kwargs) -> APIResult[RuleLabels]:
        """
        Updates information for the specified rule label.

        Args:
            label_id (int): The unique identifier for the rule label.

        Keyword Args:
            name (str): The name of the rule label.
            description (str): Additional information about the rule label.
            created_by (str): The created by for this rule label.
            referenced_rule_count (str): The referenced rule count for this rule label.

        Returns:
            tuple: A tuple containing the updated RuleLabels instance, response, and error.

        Examples:
            Update an existing rule label:

            >>> updated_label, _, error = client.zia.rule_labels.update_label(
            ...     label_id=1013,
            ...     name=f"UpdatedLabel_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedLabel_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating rule label: {error}")
            ...     return
            ... print(f"Rule label updated successfully: {updated_label.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RuleLabels)
        if error:
            return (None, response, error)

        try:
            result = RuleLabels(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_label(self, label_id: int) -> APIResult[None]:
        """
        Deletes the specified rule label.

        Args:
            label_id (int): The unique identifier for the rule label.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a rule label:

            >>> _, _, error = client.zia.rule_labels.delete_label(1013)
            >>> if error:
            ...     print(f"Error deleting rule label: {error}")
            ...     return
            ... print(f"Rule label deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_rule_type_label(self, rule_type: str, query_params: Optional[dict] = None) -> APIResult[List[RuleLabels]]:
        """
        Retrieves a list of rule labels based on the specified rule type.

        Args:
            rule_type (str): The type of rule to retrieve labels for.
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of RuleLabels instances, Response, error)

        Examples:
            List rule labels:

            >>> label_list, _, error = client.zia.rule_labels.get_rule_type_label('URL_FILTERING')
            >>> if error:
            ...     print(f"Error listing rule labels: {error}")
            ...     return
            ... print(f"Total rule labels found: {len(label_list)}")
            ... for label in label_list:
            ...     print(label.as_dict())

            List rule labels using filters:

            >>> label_list, _, error = client.zia.rule_labels.get_rule_type_label(
            ...     'URL_FILTERING', query_params={'page': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing rule labels: {error}")
            ...     return
            ... print(f"Total rule labels found: {len(label_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels/ruleType/{rule_type}
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
                result.append(RuleLabels(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
