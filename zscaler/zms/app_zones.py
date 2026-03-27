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

from typing import Optional, Any, Dict

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.zms.models.inputs import AppZoneFilter, AppZoneQueryOrderBy


class AppZonesAPI(APIClient):
    """
    A Client object for the ZMS App Zones domain.

    Provides access to app zone operations including:
    - List app zones with filtering, ordering, and pagination
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_app_zones(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
        filter_by: Optional[AppZoneFilter] = None,
        order_by: Optional[AppZoneQueryOrderBy] = None,
    ) -> tuple:
        """
        Get app zones for a given customer with optional filtering.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).
            filter_by: Filter options using AppZoneFilter.
            order_by: Ordering options using AppZoneQueryOrderBy.

        Returns:
            tuple: (app_zones_connection dict, response, error)

        Examples:
            List app zones::

                >>> result, _, err = client.zms.app_zones.list_app_zones(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for zone in result.get("nodes", []):
                ...     print(zone.get("appZoneName"))
        """
        query = """
            query ListAppZones(
                $customerId: ID!, $pageNum: Int, $pageSize: Int,
                $filter: AppZoneFilter, $orderBy: AppZoneQueryOrderBy
            ) {
                appZones(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize,
                    filter: $filter,
                    orderBy: $orderBy
                ) {
                    nodes {
                        id
                        appZoneName
                        description
                        memberCount
                        includeAllVpcs
                        includeAllSubnets
                    }
                    pageInfo {
                        pageNumber
                        pageSize
                        totalCount
                        totalPages
                    }
                }
            }
        """

        variables: Dict[str, Any] = {
            "customerId": customer_id,
            "pageNum": page_num,
            "pageSize": page_size,
        }
        if filter_by is not None:
            variables["filter"] = filter_by.as_dict()
        if order_by is not None:
            variables["orderBy"] = order_by.as_dict()

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ListAppZones",
        }

        http_method = "POST"
        api_url = format_url(self._zms_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = response.get_body().get("data", {}).get("appZones", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
