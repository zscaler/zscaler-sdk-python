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


class AgentGroupsAPI(APIClient):
    """
    A Client object for the ZMS Agent Groups domain.

    Provides access to agent group operations including:
    - List agent groups with pagination, search, and sorting
    - Get agent group TOTP secrets
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_agent_groups(
        self,
        customer_id: str,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        sort_dir: Optional[str] = None,
    ) -> tuple:
        """
        Get a paginated list of agent groups for a customer.

        Args:
            customer_id: The customer ID.
            page: Page number (default 1).
            page_size: Number of items per page (default 20).
            search: Search filter string.
            sort: Sort field.
            sort_dir: Sort direction (ASC or DESC).

        Returns:
            tuple: (agent_groups_connection dict, response, error)

        Examples:
            List agent groups::

                >>> result, _, err = client.zms.agent_groups.list_agent_groups(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for group in result.get("nodes", []):
                ...     print(group.get("name"))
        """
        query = """
            query ListAgentGroups(
                $customerId: ID!, $page: Int, $pageSize: Int,
                $search: String, $sort: String, $sortDir: SortDirection
            ) {
                agentGroups(
                    customerId: $customerId,
                    page: $page,
                    pageSize: $pageSize,
                    search: $search,
                    sort: $sort,
                    sortDir: $sortDir
                ) {
                    nodes {
                        name
                        eyezId
                        agentGroupType
                        cloudProvider
                        adminStatus
                        agentCount
                        description
                        policyStatus
                        upgradeStatus
                        tamperProtectionStatus
                        agentAutoUpgrade
                        agentDeletionTimeoutSeconds
                        timezone
                        upgradeDay
                        upgradeTime
                        versionProfileName
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
            "operationName": "ListAgentGroups",
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
            result = response.get_body().get("data", {}).get("agentGroups", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_agent_group_totp_secrets(
        self,
        customer_id: str,
        eyez_id: str,
    ) -> tuple:
        """
        Get TOTP secrets for a specific agent group.

        Args:
            customer_id: The customer ID.
            eyez_id: The agent group eyez ID.

        Returns:
            tuple: (totp_secrets dict, response, error)

        Examples:
            Get TOTP secrets::

                >>> result, _, err = client.zms.agent_groups.get_agent_group_totp_secrets(
                ...     customer_id="123456789",
                ...     eyez_id="abc-def-123"
                ... )
                >>> if err:
                ...     print(err)
                >>> print(result.get("totpSecret"))
        """
        query = """
            query GetAgentGroupTotpSecrets($customerId: ID!, $eyezId: String!) {
                agentGroupTotpSecrets(customerId: $customerId, eyezId: $eyezId) {
                    eyezId
                    totpSecret
                    totpQrCode
                    totpGenerationTimestamp
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
            "operationName": "GetAgentGroupTotpSecrets",
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
            result = response.get_body().get("data", {}).get("agentGroupTotpSecrets", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
