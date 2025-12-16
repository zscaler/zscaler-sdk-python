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
from zscaler.zinsights.models.inputs import ShadowITAppsFilterBy, ShadowITAppsOrderBy
from zscaler.errors.graphql_error import is_graphql_error_response, GraphQLAPIError


class ShadowItAPI(APIClient):
    """
    A Client object for the Z-Insights SHADOW_IT domain.

    Discover and manage shadow IT applications used by your organization's
    user, department, or location.
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

    def get_apps(
        self,
        start_time: int,
        end_time: int,
        limit: Optional[int] = None,
        filter_by: Optional[ShadowITAppsFilterBy] = None,
        order_by: Optional[List[ShadowITAppsOrderBy]] = None,
    ) -> tuple:
        """
        Get Shadow IT discovered applications with full details.

        AppsResponse fields:
            - application: The application name
            - application_category: The application category
            - risk_index: The risk index number
            - computed_risk_index: Computed risk index
            - sanctioned_state: Whether app is sanctioned/unsanctioned
            - integration: Number of potential integrations
            - data_consumed: Sum of upload and download bytes
            - data_uploaded: Uploaded bytes
            - data_downloaded: Downloaded bytes
            - authenticated_users: Number of authenticated users
            - unAuthenticated_location_count: Unauthenticated location count
            - last_access_time: Last access timestamp
            - vulnerability: Vulnerability information
            - undiscovered: Whether app is undiscovered
            - custom_risk_index: Custom risk index

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.
            limit: Maximum number of entries to return.
            filter_by: Filter options using ShadowITAppsFilterBy.
                       Supports filtering by application, application_category, sanctioned_state.
            order_by: Ordering options using list of ShadowITAppsOrderBy.

        Returns:
            tuple: (entries_list, response, error)

        Examples:
            >>> entries, _, err = client.zinsights.shadow_it.get_apps(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     limit=10
            ... )
            >>>
            >>> # With filtering
            >>> from zscaler.zinsights.models.inputs import ShadowITAppsFilterBy, StringFilter
            >>> filter_by = ShadowITAppsFilterBy(
            ...     application=StringFilter(eq="Dropbox")
            ... )
            >>> entries, _, err = client.zinsights.shadow_it.get_apps(
            ...     start_time=start_time,
            ...     end_time=end_time,
            ...     filter_by=filter_by
            ... )
        """
        query = """
            query ShadowITApps(
                $startTime: Long!, $endTime: Long!, $limit: Int,
                $filterBy: shadowITAppsSearchFilterBy, $orderBy: [ShadowITAppsOrderBy]
            ) {
                SHADOW_IT {
                    apps(start_time: $startTime, end_time: $endTime) {
                        entries(limit: $limit, filter_by: $filterBy, order_by: $orderBy) {
                            application
                            application_category
                            risk_index
                            computed_risk_index
                            sanctioned_state
                            integration
                            data_consumed
                            data_uploaded
                            data_downloaded
                            authenticated_users
                            unAuthenticated_location_count
                            last_access_time
                            vulnerability
                            undiscovered
                            custom_risk_index
                        }
                    }
                }
            }
        """

        variables = {
            "startTime": start_time,
            "endTime": end_time,
            "limit": limit,
            "filterBy": filter_by.as_dict() if filter_by else None,
            "orderBy": [o.as_dict() for o in order_by] if order_by else None,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ShadowITApps",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self._extract_graphql_response(response, api_url, "SHADOW_IT", "apps")

    def get_shadow_it_summary(
        self,
        start_time: int,
        end_time: int,
    ) -> tuple:
        """
        Get comprehensive Shadow IT summary with all groupings and statistics.

        Returns a complete summary including:
        - Top-level stats: total_upload_bytes, total_download_bytes, total_apps, total_bytes
        - group_by_app_cat_for_app: Apps grouped by category
        - group_by_app_cat_for_user_count: User counts grouped by category
        - group_by_app_cat_for_upload_bytes: Upload bytes grouped by category
        - group_by_app_cat_for_download_bytes: Download bytes grouped by category
        - group_by_app_cat_for_total_bytes: Total bytes grouped by category
        - group_by_risk_index_for_app: Apps grouped by risk index
        - group_by_provisioning_status_for_app: Apps grouped by provisioning status
        - group_by_access_for_app: Apps grouped by access type

        Args:
            start_time: Start time in epoch milliseconds.
            end_time: End time in epoch milliseconds.

        Returns:
            tuple: (summary_dict, response, error)
                   summary_dict contains all top-level fields and group_by results.

        Examples:
            >>> summary, _, err = client.zinsights.shadow_it.get_shadow_it_summary(
            ...     start_time=start_time,
            ...     end_time=end_time
            ... )
            >>> print(f"Total apps: {summary['total_apps']}")
            >>> print(f"Total bytes: {summary['total_bytes']}")
            >>> # Access group_by data
            >>> for entry in summary.get('group_by_app_cat_for_app', {}).get('entries', []):
            ...     print(f"Category: {entry['name']}, Total: {entry['total']}")
        """
        query = """
            query ShadowITSummary($startTime: Long!, $endTime: Long!) {
                SHADOW_IT {
                    shadow_it_summary(start_time: $startTime, end_time: $endTime) {
                        total_upload_bytes
                        total_download_bytes
                        total_apps
                        total_bytes
                        group_by_app_cat_for_app {
                            obfuscated
                            entries {
                                name
                                total
                                entries {
                                    name
                                    total
                                }
                            }
                        }
                        group_by_app_cat_for_user_count {
                            obfuscated
                            entries {
                                name
                                total
                                entries {
                                    name
                                    total
                                }
                            }
                        }
                        group_by_app_cat_for_upload_bytes {
                            obfuscated
                            entries {
                                name
                                total
                                entries {
                                    name
                                    total
                                }
                            }
                        }
                        group_by_app_cat_for_download_bytes {
                            obfuscated
                            entries {
                                name
                                total
                                entries {
                                    name
                                    total
                                }
                            }
                        }
                        group_by_app_cat_for_total_bytes {
                            obfuscated
                            entries {
                                name
                                total
                                entries {
                                    name
                                    total
                                }
                            }
                        }
                        group_by_risk_index_for_app {
                            obfuscated
                            entries {
                                name
                                total
                            }
                        }
                        group_by_provisioning_status_for_app {
                            obfuscated
                            entries {
                                name
                                total
                            }
                        }
                        group_by_access_for_app {
                            obfuscated
                            entries {
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
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ShadowITSummary",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

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

            # GraphQL responses have data wrapped in "data" key
            data = body.get("data", {}) if isinstance(body, dict) else {}
            summary = data.get("SHADOW_IT", {}).get("shadow_it_summary", {})
            return (summary, response, None)
        except Exception as ex:
            return (None, response, ex)
