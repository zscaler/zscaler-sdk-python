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
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Page size for pagination.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of Rule Labels instances, Response, error)

        Examples:
            List Rule Labels using default settings:

            >>> label_list, _, error = client.zia.rule_labels.list_labels(
                query_params={'search': updated_label.name})
            >>> if error:
            ...     print(f"Error listing labels: {error}")
            ...     return
            ... print(f"Total labels found: {len(label_list)}")
            ... for label in label_list:
            ...     print(label.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ruleLabels
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

        Examples:
            Print a specific Rule Label

            >>> fetched_label, _, error = client.zia.rule_labels.get_label(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching Rule Label by ID: {error}")
            ...     return
            ... print(f"Fetched Rule Label by ID: {fetched_label.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
        """
        )

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

    def add_label(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Rule Label.

        Args:
            name (str): The name of the Proxy.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional notes or information

        Returns:
            tuple: A tuple containing the newly added Rule Label, response, and error.

        Examples:
            Add a new Rule Label :

            >>> added_label, _, error = client.zia.rule_labels.add_label(
            ... name=f"RuleLabel_{random.randint(1000, 10000)}",
            ... description=f"RuleLabel_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding Rule Label: {error}")
            ...     return
            ... print(f"Rule Label added successfully: {added_profile.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ruleLabels
        """
        )

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

    def update_label(self, label_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Rule Label.

        Args:
            label_id (int): The unique ID for the Rule Label.

        Returns:
            tuple: A tuple containing the updated Rule Label, response, and error.

        Examples:
            Add a new Rule Label :

            >>> updated_label, _, error = client.zia.rule_labels.add_label(
                label_id='1524566'
            ... name=f"UpdatedRuleLabel_{random.randint(1000, 10000)}",
            ... description=f"UpdatedRuleLabel_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating Rule Label: {error}")
            ...     return
            ... print(f"Rule Label updated successfully: {updated_label.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
        """
        )
        body = {}

        body.update(kwargs)

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

    def delete_label(self, label_id: int) -> tuple:
        """
        Deletes the specified Rule Label.

        Args:
            label_id (str): The unique identifier of the Rule Label.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            List Rule Label:

            >>> _, _, error = client.zia.rule_labels.delete_label('73459')
            >>> if error:
            ...     print(f"Error deleting Rule Label: {error}")
            ...     return
            ... print(f"Rule Label with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ruleLabels/{label_id}
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
