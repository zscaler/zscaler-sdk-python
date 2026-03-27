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


class NoncesAPI(APIClient):
    """
    A Client object for the ZMS Nonces (Provisioning Keys) domain.

    Provides access to nonce operations including:
    - List nonces with pagination, search, and sorting
    - Get a single nonce by eyez ID
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_nonces(
        self,
        customer_id: str,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        sort_dir: Optional[str] = None,
    ) -> tuple:
        """
        Get a paginated list of nonces (provisioning keys) for a customer.

        Args:
            customer_id: The customer ID.
            page: Page number (default 1).
            page_size: Number of items per page (default 20).
            search: Search filter string.
            sort: Sort field.
            sort_dir: Sort direction (ASC or DESC).

        Returns:
            tuple: (nonces_connection dict, response, error)

        Examples:
            List nonces::

                >>> result, _, err = client.zms.nonces.list_nonces(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for nonce in result.get("nodes", []):
                ...     print(nonce.get("name"))
        """
        query = """
            query ListNonces(
                $customerId: ID!, $page: Int, $pageSize: Int,
                $search: String, $sort: String, $sortDir: SortDirection
            ) {
                nonces(
                    customerId: $customerId,
                    page: $page,
                    pageSize: $pageSize,
                    search: $search,
                    sort: $sort,
                    sortDir: $sortDir
                ) {
                    nodes {
                        eyezId
                        name
                        key
                        maxUsage
                        usageCount
                        agentGroupEyezId
                        agentGroupName
                        agentGroupType
                        product
                        creationTime
                        modifiedTime
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
            "page": page,
            "pageSize": page_size,
        }
        if search is not None:
            variables["search"] = search
        if sort is not None:
            variables["sort"] = sort
        if sort_dir is not None:
            variables["sortDir"] = sort_dir

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ListNonces",
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
            result = response.get_body().get("data", {}).get("nonces", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_nonce(
        self,
        customer_id: str,
        eyez_id: str,
    ) -> tuple:
        """
        Get a nonce by its eyez ID.

        Args:
            customer_id: The customer ID.
            eyez_id: The nonce eyez ID.

        Returns:
            tuple: (nonce_response dict, response, error)

        Examples:
            Get a nonce::

                >>> result, _, err = client.zms.nonces.get_nonce(
                ...     customer_id="123456789",
                ...     eyez_id="nonce-abc-123"
                ... )
                >>> if err:
                ...     print(err)
                >>> print(result.get("nonce", {}).get("name"))
        """
        query = """
            query GetNonce($customerId: ID!, $eyezId: String!) {
                nonce(customerId: $customerId, eyezId: $eyezId) {
                    nonce {
                        eyezId
                        name
                        key
                        maxUsage
                        usageCount
                        agentGroupEyezId
                        agentGroupName
                        agentGroupType
                        product
                        creationTime
                        modifiedTime
                    }
                }
            }
        """

        variables: Dict[str, Any] = {
            "customerId": customer_id,
            "eyezId": eyez_id,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "GetNonce",
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
            result = response.get_body().get("data", {}).get("nonce", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
