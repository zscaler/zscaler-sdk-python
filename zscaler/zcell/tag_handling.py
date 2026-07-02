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

    def __init__(self, request_executor: "RequestExecutor", config: dict = None) -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcell_customer_id = (config or {}).get("client", {}).get("zcellCustomerId")

    def list_tag(self, id: str = None, query_params=None) -> APIResult[List[TagHandling]]:
        """
        Gets all tags for given customer.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
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
            List all tags for a customer::

                >>> fetched_status, _, error = client.zcell.tag_handling.list_tag(
                ...     id='gi754cvqb07r0',
                ... )
                >>> if error:
                ...     print(f"Error listing tags: {error}")
                ...     return
                >>> print(f"Total tags found: {len(fetched_status)}")
                >>> for tag in fetched_status:
                ...     print(tag.as_dict())
        """
        http_method = "get".upper()
        id = id or self._zcell_customer_id
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

    def create_tag(self, id: str = None, **kwargs) -> APIResult[CreateTag]:
        """
        Creates a new tag entry.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            **kwargs: Request body fields.

                ``name`` (str): The name of the tag to create.

        Returns:
            tuple: (result, Response, error)

        Examples:
            Create a new tag::

                >>> customer_id = 'gi754cvqb07r0'
                >>> created_name = f"TagHandling01_{random.randint(1000, 10000)}"
                >>> added_policy, _, error = client.zcell.tag_handling.create_tag(
                ...     id=customer_id,
                ...     name=created_name,
                ... )
                >>> if error:
                ...     print(f"Error adding tag: {error}")
                ...     return
                >>> print(f"Tag added successfully: {added_policy.as_dict()}")
        """
        http_method = "post".upper()
        id = id or self._zcell_customer_id
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
