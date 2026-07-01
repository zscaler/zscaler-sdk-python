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
from zscaler.zcell.models.customer_region_handling import (
    CustomerRegionHandling,
    ExtendedRegionStatus,
)


class CustomerRegionHandlingAPI(APIClient):

    _zcell_base_endpoint_customer = "/zcell/config/api/v1/customers"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_regions(self, id: str, query_params=None) -> APIResult[List[CustomerRegionHandling]]:
        """
        Gets the available and configured regions for the logged-in customer.

        Args:
            id (str): Path parameter.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.skip_sku_check]`` {bool}

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.customer_region_handling.list_regions(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/regions")

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
                result.append(CustomerRegionHandling(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_regions(self, id: str, regions: List[str]) -> APIResult:
        """
        Configure customer regions.

        The API expects a raw JSON array of region codes (e.g. ``["AMER"]``) as
        the request body. Although the request is sent via ``PUT``, the endpoint
        responds with ``201 Created`` and a raw scalar value (e.g. ``1``) rather
        than a JSON object — so the raw response body is returned as the result.

        Args:
            id (str): Path parameter. The customer ID.
            regions (list[str]): List of region codes to configure (e.g. ``["AMER", "EMEA", "APAC"]``).

        Returns:
            tuple: (result, Response, error)

        Examples:
            Configure the regions for a customer::

                >>> result, _, error = client.zcell.customer_region_handling.update_regions(
                ...     id='gi754cvqb07r0',
                ...     regions=['AMER'],
                ... )
                >>> if error:
                ...     print(f"Error configuring regions: {error}")
                ...     return
                >>> print(f"Regions configured successfully. Response: {result}")
        """
        http_method = "put".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/regions")

        body = regions

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (response.get_body(), response, None)

    def list_regions_operational_status(self, id: str, query_params=None) -> APIResult[List[ExtendedRegionStatus]]:
        """
        Gets the configured regions and their operational status for the logged-in customer.

        Args:
            id (str): Path parameter.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.bc_size]`` {str}

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.customer_region_handling.list_regions_operational_status(
            ...     id='...',
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/regions/operational-status")

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
                result.append(ExtendedRegionStatus(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
