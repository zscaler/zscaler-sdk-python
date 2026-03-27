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
from zscaler.zms.models.inputs import (
    NamespaceFilter,
    NamespaceQueryOrderBy,
    TagKeyFilter,
    TagKeyQueryOrderBy,
    TagValueFilter,
    TagValueQueryOrderBy,
)


class TagsAPI(APIClient):
    """
    A Client object for the ZMS Tags domain.

    Provides access to tag management operations including:
    - List tag namespaces with filtering, ordering, and pagination
    - List tag keys within a namespace
    - List tag values within a tag key
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_tag_namespaces(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
        filter_by: Optional[NamespaceFilter] = None,
        order_by: Optional[NamespaceQueryOrderBy] = None,
    ) -> tuple:
        """
        Retrieve tag namespaces with support for filtering, ordering, and pagination.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).
            filter_by: Filter options using NamespaceFilter.
            order_by: Ordering options using NamespaceQueryOrderBy.

        Returns:
            tuple: (namespace_connection dict, response, error)

        Examples:
            List tag namespaces::

                >>> result, _, err = client.zms.tags.list_tag_namespaces(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for ns in result.get("nodes", []):
                ...     print(ns.get("name"), ns.get("origin"))
        """
        query = """
            query ListTagNamespaces(
                $customerId: ID!, $pageNum: Int, $pageSize: Int,
                $filter: NamespaceFilter, $orderBy: NamespaceQueryOrderBy
            ) {
                tagNamespaces(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize,
                    filter: $filter,
                    orderBy: $orderBy
                ) {
                    nodes {
                        id
                        name
                        description
                        origin
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
            "operationName": "ListTagNamespaces",
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
            result = response.get_body().get("data", {}).get("tagNamespaces", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_tag_keys(
        self,
        customer_id: str,
        namespace_id: str,
        page_num: int = 1,
        page_size: int = 20,
        filter_by: Optional[TagKeyFilter] = None,
        order_by: Optional[TagKeyQueryOrderBy] = None,
    ) -> tuple:
        """
        Retrieve tag keys within a specific namespace.

        Args:
            customer_id: The customer ID.
            namespace_id: The namespace ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).
            filter_by: Filter options using TagKeyFilter.
            order_by: Ordering options using TagKeyQueryOrderBy.

        Returns:
            tuple: (tag_key_connection dict, response, error)

        Examples:
            List tag keys::

                >>> result, _, err = client.zms.tags.list_tag_keys(
                ...     customer_id="123456789",
                ...     namespace_id="ns-abc-123"
                ... )
                >>> if err:
                ...     print(err)
                >>> for key in result.get("nodes", []):
                ...     print(key.get("name"))
        """
        query = """
            query ListTagKeys(
                $customerId: ID!, $namespaceId: String!,
                $pageNum: Int, $pageSize: Int,
                $filter: TagKeyFilter, $orderBy: TagKeyQueryOrderBy
            ) {
                tagKeys(
                    customerId: $customerId,
                    namespaceId: $namespaceId,
                    pageNum: $pageNum,
                    pageSize: $pageSize,
                    filter: $filter,
                    orderBy: $orderBy
                ) {
                    nodes {
                        id
                        name
                        description
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
            "namespaceId": namespace_id,
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
            "operationName": "ListTagKeys",
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
            result = response.get_body().get("data", {}).get("tagKeys", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_tag_values(
        self,
        customer_id: str,
        tag_id: str,
        namespace_origin: str,
        page_num: int = 1,
        page_size: int = 20,
        filter_by: Optional[TagValueFilter] = None,
        order_by: Optional[TagValueQueryOrderBy] = None,
    ) -> tuple:
        """
        Retrieve tag values for a specific tag key.

        Args:
            customer_id: The customer ID.
            tag_id: The tag key ID.
            namespace_origin: The namespace origin (CUSTOM, EXTERNAL, ML, UNKNOWN).
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).
            filter_by: Filter options using TagValueFilter.
            order_by: Ordering options using TagValueQueryOrderBy.

        Returns:
            tuple: (tag_value_connection dict, response, error)

        Examples:
            List tag values::

                >>> result, _, err = client.zms.tags.list_tag_values(
                ...     customer_id="123456789",
                ...     tag_id="tag-key-123",
                ...     namespace_origin="CUSTOM"
                ... )
                >>> if err:
                ...     print(err)
                >>> for val in result.get("nodes", []):
                ...     print(val.get("name"))
        """
        query = """
            query ListTagValues(
                $customerId: ID!, $tagId: String!, $namespaceOrigin: NamespaceOrigin!,
                $pageNum: Int, $pageSize: Int,
                $filter: TagValueFilter, $orderBy: TagValueQueryOrderBy
            ) {
                tagValues(
                    customerId: $customerId,
                    tagId: $tagId,
                    namespaceOrigin: $namespaceOrigin,
                    pageNum: $pageNum,
                    pageSize: $pageSize,
                    filter: $filter,
                    orderBy: $orderBy
                ) {
                    nodes {
                        id
                        name
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
            "tagId": tag_id,
            "namespaceOrigin": namespace_origin,
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
            "operationName": "ListTagValues",
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
            result = response.get_body().get("data", {}).get("tagValues", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
