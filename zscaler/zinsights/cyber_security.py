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
from zscaler.errors.graphql_error import is_graphql_error_response, GraphQLAPIError


class CyberSecurityAPI(APIClient):
    """
    A Client object for the Z-Insights CYBER_SECURITY domain.

    Cybersecurity Insights provides a unified real-time visibility into critical
    security incidents and policy actions to understand the security efficacy of
    layered defense across Malware Protection, Advanced Threat Protection (ATP),
    Sandbox, Firewall, and Isolation for your organization.
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

    def get_incidents(
        self,
        start_time: int,
        end_time: int,
        categorize_by: List[str] = None,
        limit: Optional[int] = None,
    ) -> tuple:
        """
        Get cybersecurity incidents data grouped by category.

        Note: This query returns nested entries. Each entry may have sub-entries.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            categorize_by: List of categories to group by. Options:
                - THREAT_CATEGORY_ID
                - APP_ID
                - USER_ID
                - TIME
                - SRC_COUNTRY
                Default: ["THREAT_CATEGORY_ID"]
            limit: Maximum number of entries to return.

        Returns:
            tuple: (entries_list, response, error)

        Examples:
            >>> entries, _, err = client.zinsights.cyber_security.get_incidents(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     categorize_by=["THREAT_CATEGORY_ID"],
            ...     limit=10
            ... )
        """
        if categorize_by is None:
            categorize_by = ["THREAT_CATEGORY_ID"]

        query = """
            query CyberSecurityIncidents(
                $startTime: Long!, $endTime: Long!,
                $categorizeBy: [IncidentsGroupBy!]!, $limit: Int
            ) {
                CYBER_SECURITY {
                    incidents(
                        categorize_by: $categorizeBy,
                        start_time: $startTime,
                        end_time: $endTime
                    ) {
                        obfuscated
                        entries(limit: $limit) {
                            name
                            total
                            entries(limit: $limit) {
                                name
                                total
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "startTime": start_time,
            "endTime": end_time,
            "categorizeBy": categorize_by,
            "limit": limit,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "CyberSecurityIncidents",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "CYBER_SECURITY", "incidents")

    def get_incidents_by_location(
        self,
        start_time: int,
        end_time: int,
        categorize_by: str = "LOCATION_ID",
        limit: Optional[int] = None,
    ) -> tuple:
        """
        Get cybersecurity incidents grouped by location or other dimension.

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            categorize_by: Category to group by. Options:
                - LOCATION_ID (default)
                - APP_ID
                - USER_ID
                - DEPARTMENT_ID
            limit: Maximum number of entries to return.

        Returns:
            tuple: (entries_list, response, error)

        Examples:
            >>> entries, _, err = client.zinsights.cyber_security.get_incidents_by_location(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     categorize_by="LOCATION_ID",
            ...     limit=10
            ... )
        """
        query = """
            query CyberSecurityByLocation(
                $startTime: Long!, $endTime: Long!,
                $categorizeBy: IncidentsWithIdGroupBy!, $limit: Int
            ) {
                CYBER_SECURITY {
                    cyber_security_location(
                        categorize_by: $categorizeBy,
                        start_time: $startTime,
                        end_time: $endTime
                    ) {
                        obfuscated
                        entries(limit: $limit) {
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
            "categorizeBy": categorize_by,
            "limit": limit,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "CyberSecurityByLocation",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "CYBER_SECURITY", "cyber_security_location")
