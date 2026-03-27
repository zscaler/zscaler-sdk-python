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
from zscaler.zms.models.inputs import ResourceGroupsFilter


class ResourceGroupsAPI(APIClient):
    """
    A Client object for the ZMS Resource Groups domain.

    Provides access to resource group operations including:
    - List resource groups with filtering and pagination
    - Get resource group members
    - Get resource group protection status
    - Get recommended resource groups (ML-based)
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_resource_groups(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
        filter_by: Optional[ResourceGroupsFilter] = None,
    ) -> tuple:
        """
        Get resource groups for a given customer with optional filtering.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).
            filter_by: Filter options using ResourceGroupsFilter.

        Returns:
            tuple: (resource_groups_connection dict, response, error)

        Examples:
            List resource groups::

                >>> result, _, err = client.zms.resource_groups.list_resource_groups(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for rg in result.get("nodes", []):
                ...     print(rg.get("name"))
        """
        query = """
            query ListResourceGroups(
                $customerId: ID!, $pageNum: Int, $pageSize: Int,
                $filter: ResourceGroupsFilter
            ) {
                resourceGroups(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize,
                    filter: $filter
                ) {
                    nodes {
                        ... on ManagedResourceGroup {
                            id
                            name
                            description
                            type
                            origin
                            resourceMemberCount
                            modifiedTime
                        }
                        ... on UnmanagedResourceGroup {
                            id
                            name
                            description
                            type
                            origin
                            resourceMemberCount
                            modifiedTime
                            cidrs
                            fqdns
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

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ListResourceGroups",
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
            result = response.get_body().get("data", {}).get("resourceGroups", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_resource_group_members(
        self,
        customer_id: str,
        group_id: str,
        page_num: int = 1,
        page_size: int = 20,
    ) -> tuple:
        """
        Get resources of a specific resource group.

        Args:
            customer_id: The customer ID.
            group_id: The resource group ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).

        Returns:
            tuple: (resources_connection dict, response, error)

        Examples:
            Get resource group members::

                >>> result, _, err = client.zms.resource_groups.get_resource_group_members(
                ...     customer_id="123456789",
                ...     group_id="rg-abc-123"
                ... )
                >>> if err:
                ...     print(err)
                >>> for resource in result.get("nodes", []):
                ...     print(resource.get("name"))
        """
        query = """
            query GetResourceGroupMembers(
                $customerId: ID!, $id: String!, $pageNum: Int, $pageSize: Int
            ) {
                resourceGroupMembers(
                    customerId: $customerId,
                    id: $id,
                    pageNum: $pageNum,
                    pageSize: $pageSize
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
            "id": group_id,
            "pageNum": page_num,
            "pageSize": page_size,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "GetResourceGroupMembers",
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
            result = response.get_body().get("data", {}).get("resourceGroupMembers", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_resource_group_protection_status(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
    ) -> tuple:
        """
        Get resource group protection status.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).

        Returns:
            tuple: (protection_status dict, response, error)

        Examples:
            Get protection status::

                >>> result, _, err = client.zms.resource_groups.get_resource_group_protection_status(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
        """
        query = """
            query ResourceGroupProtectionStatus(
                $customerId: ID!, $pageNum: Int, $pageSize: Int
            ) {
                resourceGroupProtectionStatus(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize
                ) {
                    nodes {
                        protectedPercentage
                        protectedResourceGroupsCount
                        unprotectedResourceGroupsCount
                        totalResourceGroups
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
            "operationName": "ResourceGroupProtectionStatus",
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
            result = response.get_body().get("data", {}).get("resourceGroupProtectionStatus", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
