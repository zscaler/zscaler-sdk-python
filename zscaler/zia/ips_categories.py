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
from zscaler.zia.models.ips_categories import IpsCategories


class IpsCategoriesAPI(APIClient):
    """
    A Client object for the IPS Categories resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_categories(self, query_params: Optional[dict] = None) -> APIResult[List[IpsCategories]]:
        """
        Lists the advanced threat categories (predefined and custom) against which network traffic can be monitored using the IPS Control policy.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size.

        Returns:
            tuple: A tuple containing (list of IpsCategories instances, Response, error)

        Examples:
            List IPS threat categories:

            >>> category_list, _, error = client.zia.ips_categories.list_categories()
            >>> if error:
            ...     print(f"Error listing IPS threat categories: {error}")
            ...     return
            ... print(f"Total IPS threat categories found: {len(category_list)}")
            ... for category in category_list:
            ...     print(category.as_dict())

            List IPS threat categories using filters:

            >>> category_list, _, error = client.zia.ips_categories.list_categories(
            ...     query_params={'page': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing IPS threat categories: {error}")
            ...     return
            ... print(f"Total IPS threat categories found: {len(category_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ipsCategories
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
                result.append(IpsCategories(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
