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
from zscaler.zia.models.rule_labels import RuleLabels
from zscaler.utils import format_url


class RuleLabelsAPI(APIClient):
    """
    A Client object for the Rule labels resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_labels(self, query_params=None) -> tuple:
        """
        Lists rule labels in your organization with pagination.
        A subset of rule labels  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of Rule Labels instances, Response, error)

        Examples:
            List Rule Labels using default settings:

            >>> for label in zia.labels.list_labels():
            ...   print(label)

            List labels, limiting to a maximum of 10 items:

            >>> for label in zia.labels.list_labels(max_items=10):
            ...    print(label)

            List labels, returning 200 items per page for a maximum of 2 pages:

            >>> for label in zia.labels.list_labels(page_size=200, max_pages=2):
            ...    print(label)

        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels
        """)

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(RuleLabels(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_label(self, label_id: int) -> tuple:
        """
        Fetches a specific rule labels by ID.

        Args:
            label_id (int): The unique identifier for the rule label.

        Returns:
            tuple: A tuple containing (Rule Label instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, RuleLabels)
        if error:
            return (None, response, error)

        try:
            result = RuleLabels(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_label(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Rule Label.

        Args:
            label (dict or object):
                The label data to be sent in the request.

        Returns:
            tuple: A tuple containing the newly added Rule Label, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ruleLabels
        """
        )

        body = kwargs

        # Create the request with no empty param handling logic
        request, error = self._request_executor\
            .create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, RuleLabels)
        if error:
            return (None, response, error)

        try:
            result = RuleLabels(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_label(self, label_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Rule Label.

        Args:
            label_id (int): The unique ID for the Rule Label.

        Returns:
            tuple: A tuple containing the updated Rule Label, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
        """)
        body = {}

        body.update(kwargs)

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, RuleLabels)
        if error:
            return (None, response, error)

        # Parse the response into a RuleLabels instance
        try:
            result = RuleLabels(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_label(self, label_id: int) -> tuple:
        """
        Deletes the specified Rule Label.

        Args:
            label_id (str): The unique identifier of the Rule Label.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
        """)

        params = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
