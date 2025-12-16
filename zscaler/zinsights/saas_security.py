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

from typing import Optional, List, Tuple, Any, Dict

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.zinsights.models.inputs import CasbEntriesFilterBy, CasbEntryOrderBy
from zscaler.errors.graphql_error import is_graphql_error_response, GraphQLAPIError


class SaasSecurityAPI(APIClient):
    """
    A Client object for the Z-Insights SAAS_SECURITY domain.

    Saas Security contains queries for CASB data. Cloud Access Security Broker (CASB)
    provides data and threat protection for data at rest in cloud services.
    """

    _zinsights_base_endpoint = "/zins/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def _extract_graphql_response(
        self,
        response,
        api_url: str,
        domain: str,
        field: str,
    ) -> Tuple[Optional[List[Dict[str, Any]]], Any, Optional[Exception]]:
        """Extract data from GraphQL response and handle errors."""
        try:
            body = response.get_body() if response else {}
            if is_graphql_error_response(body):
                error = GraphQLAPIError(
                    url=api_url,
                    response_details=response._response,
                    response_body=body,
                    service_type="zins"
                )
                return (None, response, error)
            data = body.get("data", {}) if isinstance(body, dict) else {}
            entries = data.get(domain, {}).get(field, {}).get("entries", [])
            return (entries, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_casb_app_report(
        self,
        start_time: int,
        end_time: int,
        limit: Optional[int] = None,
        filter_by: Optional[CasbEntriesFilterBy] = None,
        order_by: Optional[List[CasbEntryOrderBy]] = None,
    ) -> tuple:
        """
        Get CASB application report data.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            limit: Maximum number of entries to return.
            filter_by: Filter options using CasbEntriesFilterBy.
                       Supports filtering by name using StringFilter with eq, ne, in, nin.
            order_by: Ordering options using list of CasbEntryOrderBy.

        Returns:
            tuple: (entries_list, response, error)

        Examples:
            >>> entries, _, err = client.zinsights.saas_security.get_casb_app_report(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     limit=10
            ... )
            >>>
            >>> # With filtering
            >>> from zscaler.zinsights.models.inputs import CasbEntriesFilterBy, StringFilter
            >>> filter_by = CasbEntriesFilterBy(name=StringFilter(eq="AppName"))
            >>> entries, _, err = client.zinsights.saas_security.get_casb_app_report(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     filter_by=filter_by
            ... )
        """
        query = """
            query CasbAppReport(
                $startTime: Long!, $endTime: Long!, $limit: Int,
                $filter_by: CasbEntriesFilterBy, $order_by: [CasbEntryOrderBy]
            ) {
                SAAS_SECURITY {
                    casb_app(start_time: $startTime, end_time: $endTime) {
                        obfuscated
                        entries(limit: $limit, filter_by: $filter_by, order_by: $order_by) {
                            name
                            total
                        }
                    }
                }
            }
        """

        variables = {
            "startTime": start_time,
            "endTime": end_time,
            "limit": limit,
            "filter_by": filter_by.as_dict() if filter_by else None,
            "order_by": [o.as_dict() for o in order_by] if order_by else None,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "CasbAppReport",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "SAAS_SECURITY", "casb_app")
