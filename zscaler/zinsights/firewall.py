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
from zscaler.zinsights.models.inputs import FirewallEntriesFilterBy, FirewallEntryOrderBy
from zscaler.errors.graphql_error import is_graphql_error_response, GraphQLAPIError


class FirewallAPI(APIClient):
    """
    A Client object for the Z-Insights ZERO_TRUST_FIREWALL domain.

    Zscaler Zero Trust Firewall protects web and non-web traffic for all users,
    applications, and locations with the industry's most comprehensive cloud-native
    security service edge (SSE) platform. This domain provides report data for
    specific type, like location, action.
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

    def get_traffic_by_action(
        self,
        start_time: int,
        end_time: int,
        limit: Optional[int] = None,
        filter_by: Optional[FirewallEntriesFilterBy] = None,
        order_by: Optional[List[FirewallEntryOrderBy]] = None,
    ) -> tuple:
        """
        Get Zero Trust Firewall traffic data grouped by action.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            limit: Maximum number of entries to return.
            filter_by: Filter options using FirewallEntriesFilterBy.
            order_by: Ordering options using list of FirewallEntryOrderBy.

        Returns:
            tuple: (entries_list, response, error)

        Examples:
            >>> entries, _, err = client.zinsights.firewall.get_traffic_by_action(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     limit=10
            ... )
        """
        query = """
            query FirewallByAction(
                $startTime: Long!, $endTime: Long!, $limit: Int,
                $filter_by: FirewallEntriesFilterBy, $order_by: [FirewallEntryOrderBy]
            ) {
                ZERO_TRUST_FIREWALL {
                    action(start_time: $startTime, end_time: $endTime) {
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
            "operationName": "FirewallByAction",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "ZERO_TRUST_FIREWALL", "action")

    def get_traffic_by_location(
        self,
        start_time: int,
        end_time: int,
        limit: Optional[int] = None,
        filter_by: Optional[FirewallEntriesFilterBy] = None,
        order_by: Optional[List[FirewallEntryOrderBy]] = None,
    ) -> tuple:
        """
        Get Zero Trust Firewall traffic data grouped by location.

        Returns FirewallReportDataId with fields: id, name, total.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            limit: Maximum number of entries to return.
            filter_by: Filter options using FirewallEntriesFilterBy.
                       Supports filtering by name using StringFilter with eq, ne, in, nin.
            order_by: Ordering options using list of FirewallEntryOrderBy.

        Returns:
            tuple: (entries_list, response, error)

        Examples:
            >>> from zscaler.zinsights.models.inputs import (
            ...     FirewallEntriesFilterBy, StringFilter, FirewallEntryOrderBy
            ... )
            >>> from zscaler.zinsights.models.enums import SortOrder
            >>>
            >>> # With filtering
            >>> filter_by = FirewallEntriesFilterBy(
            ...     name=StringFilter(eq="Location1")
            ... )
            >>> entries, _, err = client.zinsights.firewall.get_traffic_by_location(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     limit=10,
            ...     filter_by=filter_by
            ... )
            >>>
            >>> # With ordering
            >>> order_by = [FirewallEntryOrderBy(field_name="total", order=SortOrder.DESC)]
            >>> entries, _, err = client.zinsights.firewall.get_traffic_by_location(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     order_by=order_by
            ... )
        """
        query = """
            query FirewallByLocation(
                $startTime: Long!, $endTime: Long!, $limit: Int,
                $filter_by: FirewallEntriesFilterBy, $order_by: [FirewallEntryOrderBy]
            ) {
                ZERO_TRUST_FIREWALL {
                    location_firewall(start_time: $startTime, end_time: $endTime) {
                        obfuscated
                        entries(limit: $limit, filter_by: $filter_by, order_by: $order_by) {
                            id
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
            "operationName": "FirewallByLocation",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "ZERO_TRUST_FIREWALL", "location_firewall")

    def get_network_services(
        self,
        start_time: int,
        end_time: int,
        limit: Optional[int] = None,
        filter_by: Optional[FirewallEntriesFilterBy] = None,
        order_by: Optional[List[FirewallEntryOrderBy]] = None,
    ) -> tuple:
        """
        Get Zero Trust Firewall network services data.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            limit: Maximum number of entries to return.
            filter_by: Filter options using FirewallEntriesFilterBy.
            order_by: Ordering options using list of FirewallEntryOrderBy.

        Returns:
            tuple: (entries_list, response, error)
        """
        query = """
            query FirewallNetworkServices(
                $startTime: Long!, $endTime: Long!, $limit: Int,
                $filter_by: FirewallEntriesFilterBy, $order_by: [FirewallEntryOrderBy]
            ) {
                ZERO_TRUST_FIREWALL {
                    network_service(start_time: $startTime, end_time: $endTime) {
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
            "operationName": "FirewallNetworkServices",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "ZERO_TRUST_FIREWALL", "network_service")
