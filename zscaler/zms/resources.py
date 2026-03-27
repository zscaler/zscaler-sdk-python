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
from zscaler.zms.models.inputs import ResourceQueryFilter, ResourceQueryOrderBy


class ResourcesAPI(APIClient):
    """
    A Client object for the ZMS Resources domain.

    Provides access to resource operations including:
    - List resources with filtering, ordering, and pagination
    - Resource protection status
    - Event metadata
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_resources(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
        include_deleted: bool = False,
        filter_by: Optional[ResourceQueryFilter] = None,
        order_by: Optional[ResourceQueryOrderBy] = None,
    ) -> tuple:
        """
        Get resources for a given list of filters.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).
            include_deleted: Whether to include deleted resources.
            filter_by: Filter options using ResourceQueryFilter.
            order_by: Ordering options using ResourceQueryOrderBy.

        Returns:
            tuple: (resources_connection dict, response, error)

        Examples:
            List resources::

                >>> result, _, err = client.zms.resources.list_resources(
                ...     customer_id="123456789",
                ...     page_num=1,
                ...     page_size=20
                ... )
                >>> if err:
                ...     print(err)
                >>> for resource in result.get("nodes", []):
                ...     print(resource.get("name"))
        """
        query = """
            query ListResources(
                $customerId: ID!, $pageNum: Int, $pageSize: Int,
                $includeDeleted: Boolean, $filter: ResourceQueryFilter,
                $orderBy: ResourceQueryOrderBy
            ) {
                resources(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize,
                    includeDeleted: $includeDeleted,
                    filter: $filter,
                    orderBy: $orderBy
                ) {
                    nodes {
                        id
                        name
                        resourceType
                        status
                        cloudProvider
                        cloudRegion
                        resourceHostname
                        platformOs
                        platformOsDistro
                        platformOsVersion
                        localIps
                        deleted
                        modifiedTime
                        agentId
                        appZoneIds
                        appZoneNames
                        appZoneMappingState
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
            "includeDeleted": include_deleted,
        }
        if filter_by is not None:
            variables["filter"] = filter_by.as_dict()
        if order_by is not None:
            variables["orderBy"] = order_by.as_dict()

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ListResources",
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
            result = response.get_body().get("data", {}).get("resources", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_resource_protection_status(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
    ) -> tuple:
        """
        Get resource protection status.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).

        Returns:
            tuple: (protection_status dict, response, error)

        Examples:
            Get resource protection status::

                >>> result, _, err = client.zms.resources.get_resource_protection_status(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
        """
        query = """
            query ResourceProtectionStatus(
                $customerId: ID!, $pageNum: Int, $pageSize: Int
            ) {
                resourceProtectionStatus(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize
                ) {
                    nodes {
                        protectedPercentage
                        protectedResourcesCount
                        unprotectedResourcesCount
                        totalResources
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

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ResourceProtectionStatus",
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
            result = response.get_body().get("data", {}).get("resourceProtectionStatus", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_metadata(
        self,
        customer_id: str,
    ) -> tuple:
        """
        Get event metadata for a customer.

        Args:
            customer_id: The customer ID.

        Returns:
            tuple: (metadata JSON, response, error)

        Examples:
            Get metadata::

                >>> result, _, err = client.zms.resources.get_metadata(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
        """
        query = """
            query GetMetadata($customerId: String!) {
                metadata(customerId: $customerId)
            }
        """

        variables: Dict[str, Any] = {
            "customerId": customer_id,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "GetMetadata",
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
            result = response.get_body().get("data", {}).get("metadata", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
