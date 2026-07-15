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
from zscaler.utils import format_url, zcell_params
from zscaler.zcell.models.audit_data_handling import AuditDataHandling, AuditMetadata


class AuditDataHandlingAPI(APIClient):

    _zcell_base_endpoint = "/zcell/config/api/v1"

    def __init__(self, request_executor: "RequestExecutor", config: dict = None) -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcell_customer_id = (config or {}).get("client", {}).get("zcellCustomerId")

    @zcell_params(start_key="startDate", end_key="endDate", target="body")
    def list_audit_customers_search(self, id: str = None, query_params=None, **kwargs) -> APIResult[List[AuditDataHandling]]:
        """
        Returns all audit log based on filters.

        The filter is sent as a flat JSON request **body** (not query params).
        Because the body carries a ``startDate`` / ``endDate`` epoch-seconds
        window, the ``days`` shorthand is supported and fills both accordingly.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            days (int): Convenience shorthand — sets a [now - days, now] startDate/endDate epoch-seconds body window.
            **kwargs: Request body fields (flat). Supported fields:
                ``[start_date]`` {int}: Start of the audit range (epoch seconds).
                ``[end_date]`` {int}: End of the audit range (epoch seconds).
                ``[operation_type]`` {str}: One of Create, Update, Delete, Export.
                ``[object_type]`` {str}: Object type filter.
                ``[object_name]`` {str}: Object name filter.
                ``[object_id]`` {int}: Object ID filter.
                ``[visibility]`` {str}: One of Customer, Root.
                ``[customer_id]`` {str}: Customer ID filter (ROOT only; ignored for non-root tenants).
                ``[modified_by_user_id]`` {str}: Modified-by user ID filter.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.page]`` {int}: Page number (0-based)
                ``[query_params.size]`` {int}: Page size (1-100)
                ``[query_params.sort_by]`` {str}: Field to sort by. Default: creationTime. Sortable fields:
                creationTime, auditOperationType, objectType, objectName, objectId, customerId, visibility
                ``[query_params.sort_dir]`` {str}: ASC or DESC. Default: DESC

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            Search audit entries for a customer over the last 14 days::

                >>> results, _, error = client.zcell.audit_data_handling.list_audit_customers_search(
                ...     id='gi754cvqb07r0',
                ...     days=14,
                ...     visibility='Customer',
                ... )
                >>> if error:
                ...     print(f"Error: {error}")
                ...     return
                >>> for item in results:
                ...     print(item.as_dict())

            Provide an explicit window instead of the ``days`` shorthand::

                >>> results, _, error = client.zcell.audit_data_handling.list_audit_customers_search(
                ...     id='gi754cvqb07r0',
                ...     start_date=1781296768,
                ...     end_date=1782506368,
                ...     visibility='Customer',
                ... )
        """
        http_method = "post".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(f"{self._zcell_base_endpoint}/audit/customers/{id}/search")

        query_params = query_params or {}

        body = kwargs
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
                result.append(AuditDataHandling(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_audit_metadata(self, query_params=None) -> APIResult[List[AuditMetadata]]:
        """
        Returns metadata for audit.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.audit_data_handling.list_audit_metadata()
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint}/audit/metadata")

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
                result.append(AuditMetadata(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
