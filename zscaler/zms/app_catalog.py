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
from zscaler.zms.models.inputs import AppCatalogQueryFilter, AppCatalogQueryOrderBy


class AppCatalogAPI(APIClient):
    """
    A Client object for the ZMS App Catalog domain.

    Provides access to app catalog operations including:
    - List app catalog entries with filtering, ordering, and pagination
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_app_catalog(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
        filter_by: Optional[AppCatalogQueryFilter] = None,
        order_by: Optional[AppCatalogQueryOrderBy] = None,
    ) -> tuple:
        """
        Get application catalog entries for a given customer.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).
            filter_by: Filter options using AppCatalogQueryFilter.
            order_by: Ordering options using AppCatalogQueryOrderBy.

        Returns:
            tuple: (app_catalog_connection dict, response, error)

        Examples:
            List app catalog::

                >>> result, _, err = client.zms.app_catalog.list_app_catalog(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for app in result.get("nodes", []):
                ...     print(app.get("name"), app.get("category"))
        """
        query = """
            query ListAppCatalog(
                $customerId: ID!, $pageNum: Int, $pageSize: Int,
                $filter: AppCatalogQueryFilter, $orderBy: AppCatalogQueryOrderBy
            ) {
                appCatalog(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize,
                    filter: $filter,
                    orderBy: $orderBy
                ) {
                    nodes {
                        id
                        name
                        category
                        creationTime
                        modifiedTime
                        details {
                            portAndProtocol {
                                protocol
                                portRanges {
                                    startPort
                                    endPort
                                }
                            }
                            processes
                        }
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
            "operationName": "ListAppCatalog",
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
            result = response.get_body().get("data", {}).get("appCatalog", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
