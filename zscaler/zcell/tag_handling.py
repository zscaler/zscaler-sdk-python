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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zcell.models.tag_handling import CreateTag, TagHandling


class TagHandlingAPI(APIClient):

    _zcell_base_endpoint_customer = "/zcell/config/api/v1/customers"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_tag(self, id: str, query_params=None) -> APIResult[List[TagHandling]]:
        """
        Gets all tags for given customer.

        Args:
            id (str): Path parameter.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.name]`` {str}
                ``[query_params.page]`` {int}: Page number (0-based)
                ``[query_params.size]`` {int}: Page size (1-100)
                ``[query_params.sort_by]`` {str}: Field to sort by. Default: name. Sortable fields: id, name
                ``[query_params.sort_dir]`` {str}: ASC or DESC. Default: ASC

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.tag_handling.list_tag(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/tag")

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
                result.append(TagHandling(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_tag(self, id: str, **kwargs) -> APIResult[CreateTag]:
        """
        Creates a new tag entry.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.tag_handling.create_tag(id='...', name='example')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/tag")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CreateTag)
        if error:
            return (None, response, error)
        try:
            result = CreateTag(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
