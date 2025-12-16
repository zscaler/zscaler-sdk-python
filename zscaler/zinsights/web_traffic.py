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
from zscaler.zinsights.models.inputs import WebEntriesFilterBy, WebOrderBy
from zscaler.errors.graphql_error import is_graphql_error_response, GraphQLAPIError


class WebTrafficAPI(APIClient):
    """
    A Client object for the Z-Insights WEB_TRAFFIC domain.

    Provides access to web traffic analytics and reports including:
    - Traffic by location
    - Traffic by user
    - Protocol distribution
    - Threat categories
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
        """
        Extract data from GraphQL response and handle errors.

        Args:
            response: The HTTP response object
            api_url: The API URL for error reporting
            domain: The GraphQL domain (e.g., "WEB_TRAFFIC")
            field: The field to extract (e.g., "location", "protocols")

        Returns:
            Tuple of (entries, response, error)
        """
        try:
            body = response.get_body() if response else {}

            # Check for GraphQL errors in the response
            if is_graphql_error_response(body):
                error = GraphQLAPIError(
                    url=api_url,
                    response_details=response._response,
                    response_body=body,
                    service_type="zins"
                )
                return (None, response, error)

            # Extract the data
            data = body.get("data", {}) if isinstance(body, dict) else {}
            entries = data.get(domain, {}).get(field, {}).get("entries", [])
            return (entries, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_traffic_by_location(
        self,
        start_time: int,
        end_time: int,
        traffic_unit: str = "TRANSACTIONS",
        include_trend: bool = False,
        trend_interval: Optional[str] = None,
        limit: Optional[int] = None,
        filter_by: Optional[WebEntriesFilterBy] = None,
        order_by: Optional[List[WebOrderBy]] = None,
    ) -> tuple:
        """
        Get web traffic data grouped by location.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            traffic_unit: Either "TRANSACTIONS" or "BYTES".
            include_trend: Whether to include trend data.
            trend_interval: Trend interval (e.g., "HOURLY", "DAILY").
            limit: Maximum number of entries to return.
            filter_by: Filter options using WebEntriesFilterBy.
            order_by: Ordering options using list of WebOrderBy.

        Returns:
            tuple: (entries_list, response, error)

        Examples:
            >>> entries, _, err = client.zinsights.web_traffic.get_traffic_by_location(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     traffic_unit="TRANSACTIONS",
            ...     limit=10
            ... )
            >>>
            >>> # With trend data
            >>> entries, _, err = client.zinsights.web_traffic.get_traffic_by_location(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     traffic_unit="TRANSACTIONS",
            ...     include_trend=True,
            ...     trend_interval="HOURLY"
            ... )
        """
        query = """
            query WebTrafficByLocation(
                $startTime: Long!, $endTime: Long!, $trafficUnit: WebTrafficUnits!,
                $includeTrend: Boolean, $trendInterval: TrendInterval, $limit: Int,
                $filter_by: WebEntriesFilterBy, $order_by: [WebOrderBy]
            ) {
                WEB_TRAFFIC {
                    location(
                        start_time: $startTime,
                        end_time: $endTime,
                        traffic_unit: $trafficUnit,
                        include_trend: $includeTrend,
                        trend_interval: $trendInterval
                    ) {
                        obfuscated
                        entries(limit: $limit, filter_by: $filter_by, order_by: $order_by) {
                            name
                            total
                            trend {
                                trend_start_time
                                trend_interval
                                trend_values
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "startTime": start_time,
            "endTime": end_time,
            "trafficUnit": traffic_unit,
            "includeTrend": include_trend,
            "trendInterval": trend_interval,
            "limit": limit,
            "filter_by": filter_by.as_dict() if filter_by else None,
            "order_by": [o.as_dict() for o in order_by] if order_by else None,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "WebTrafficByLocation",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "WEB_TRAFFIC", "location")

    def get_no_grouping(
        self,
        start_time: int,
        end_time: int,
        traffic_unit: str = "TRANSACTIONS",
        dlp_engine_filter: Optional[str] = None,
        action_filter: Optional[str] = None,
        include_trend: bool = False,
        trend_interval: Optional[str] = None,
        limit: Optional[int] = None,
        filter_by: Optional[WebEntriesFilterBy] = None,
        order_by: Optional[List[WebOrderBy]] = None,
    ) -> tuple:
        """
        Get web traffic data without grouping (overall traffic).

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            traffic_unit: Either "TRANSACTIONS" or "BYTES".
            dlp_engine_filter: DLP engine filter.
            action_filter: Action filter (e.g., "ALLOW", "BLOCK").
            include_trend: Whether to include trend data.
            trend_interval: Trend interval (e.g., "HOURLY", "DAILY").
            limit: Maximum number of entries to return.
            filter_by: Filter options using WebEntriesFilterBy.
            order_by: Ordering options using list of WebOrderBy.

        Returns:
            tuple: (entries_list, response, error)
        """
        query = """
            query WebTrafficNoGrouping(
                $startTime: Long!, $endTime: Long!, $trafficUnit: WebTrafficUnits!,
                $dlpEngineFilter: DlpEngineFilter, $actionFilter: ActionStatus,
                $includeTrend: Boolean, $trendInterval: TrendInterval, $limit: Int,
                $filter_by: WebEntriesFilterBy, $order_by: [WebOrderBy]
            ) {
                WEB_TRAFFIC {
                    no_grouping(
                        start_time: $startTime,
                        end_time: $endTime,
                        traffic_unit: $trafficUnit,
                        dlp_engine_filter: $dlpEngineFilter,
                        action_filter: $actionFilter,
                        include_trend: $includeTrend,
                        trend_interval: $trendInterval
                    ) {
                        obfuscated
                        entries(limit: $limit, filter_by: $filter_by, order_by: $order_by) {
                            name
                            total
                            trend {
                                trend_start_time
                                trend_interval
                                trend_values
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "startTime": start_time,
            "endTime": end_time,
            "trafficUnit": traffic_unit,
            "dlpEngineFilter": dlp_engine_filter,
            "actionFilter": action_filter,
            "includeTrend": include_trend,
            "trendInterval": trend_interval,
            "limit": limit,
            "filter_by": filter_by.as_dict() if filter_by else None,
            "order_by": [o.as_dict() for o in order_by] if order_by else None,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "WebTrafficNoGrouping",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "WEB_TRAFFIC", "no_grouping")

    def get_protocols(
        self,
        start_time: int,
        end_time: int,
        traffic_unit: str = "TRANSACTIONS",
        limit: Optional[int] = None,
        filter_by: Optional[WebEntriesFilterBy] = None,
        order_by: Optional[List[WebOrderBy]] = None,
    ) -> tuple:
        """
        Get web traffic protocol distribution.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            traffic_unit: Either "TRANSACTIONS" or "BYTES".
            limit: Maximum number of entries to return.
            filter_by: Filter options using WebEntriesFilterBy.
            order_by: Ordering options using list of WebOrderBy.

        Returns:
            tuple: (entries_list, response, error)
        """
        query = """
            query WebProtocols(
                $startTime: Long!, $endTime: Long!, $trafficUnit: WebTrafficUnits!,
                $limit: Int, $filter_by: WebEntriesFilterBy, $order_by: [WebOrderBy]
            ) {
                WEB_TRAFFIC {
                    protocols(start_time: $startTime, end_time: $endTime, traffic_unit: $trafficUnit) {
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
            "trafficUnit": traffic_unit,
            "limit": limit,
            "filter_by": filter_by.as_dict() if filter_by else None,
            "order_by": [o.as_dict() for o in order_by] if order_by else None,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "WebProtocols",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "WEB_TRAFFIC", "protocols")

    def get_threat_super_categories(
        self,
        start_time: int,
        end_time: int,
        traffic_unit: str = "TRANSACTIONS",
        limit: Optional[int] = None,
        filter_by: Optional[WebEntriesFilterBy] = None,
        order_by: Optional[List[WebOrderBy]] = None,
    ) -> tuple:
        """
        Get web traffic data grouped by threat super categories.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            traffic_unit: Either "TRANSACTIONS" or "BYTES".
            limit: Maximum number of entries to return.
            filter_by: Filter options using WebEntriesFilterBy.
            order_by: Ordering options using list of WebOrderBy.

        Returns:
            tuple: (entries_list, response, error)
        """
        query = """
            query WebThreatSuperCategories(
                $startTime: Long!, $endTime: Long!, $trafficUnit: WebTrafficUnits!,
                $limit: Int, $filter_by: WebEntriesFilterBy, $order_by: [WebOrderBy]
            ) {
                WEB_TRAFFIC {
                    threat_super_categories(
                        start_time: $startTime, end_time: $endTime, traffic_unit: $trafficUnit
                    ) {
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
            "trafficUnit": traffic_unit,
            "limit": limit,
            "filter_by": filter_by.as_dict() if filter_by else None,
            "order_by": [o.as_dict() for o in order_by] if order_by else None,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "WebThreatSuperCategories",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "WEB_TRAFFIC", "threat_super_categories")

    def get_threat_class(
        self,
        start_time: int,
        end_time: int,
        traffic_unit: str = "TRANSACTIONS",
        limit: Optional[int] = None,
        filter_by: Optional[WebEntriesFilterBy] = None,
        order_by: Optional[List[WebOrderBy]] = None,
    ) -> tuple:
        """
        Get web traffic data grouped by threat class.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            traffic_unit: Either "TRANSACTIONS" or "BYTES".
            limit: Maximum number of entries to return.
            filter_by: Filter options using WebEntriesFilterBy.
            order_by: Ordering options using list of WebOrderBy.

        Returns:
            tuple: (entries_list, response, error)
        """
        query = """
            query WebThreatClass(
                $startTime: Long!, $endTime: Long!, $trafficUnit: WebTrafficUnits!,
                $limit: Int, $filter_by: WebEntriesFilterBy, $order_by: [WebOrderBy]
            ) {
                WEB_TRAFFIC {
                    threat_class(
                        start_time: $startTime, end_time: $endTime, traffic_unit: $trafficUnit
                    ) {
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
            "trafficUnit": traffic_unit,
            "limit": limit,
            "filter_by": filter_by.as_dict() if filter_by else None,
            "order_by": [o.as_dict() for o in order_by] if order_by else None,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "WebThreatClass",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "WEB_TRAFFIC", "threat_class")
