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


class AgentsAPI(APIClient):
    """
    A Client object for the ZMS Agents domain.

    Provides access to agent operations including:
    - List agents with pagination, search, and sorting
    - Agent connection status statistics
    - Agent version statistics
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_agents(
        self,
        customer_id: str,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        sort_dir: Optional[str] = None,
    ) -> tuple:
        """
        Get a paginated list of agents for a customer.

        Args:
            customer_id: The customer ID.
            page: Page number (default 1).
            page_size: Number of items per page (default 20).
            search: Search filter string.
            sort: Sort field.
            sort_dir: Sort direction (ASC or DESC).

        Returns:
            tuple: (agents_connection dict, response, error)

        Examples:
            List agents::

                >>> result, _, err = client.zms.agents.list_agents(
                ...     customer_id="123456789",
                ...     page=1,
                ...     page_size=20
                ... )
                >>> if err:
                ...     print(err)
                >>> for agent in result.get("nodes", []):
                ...     print(agent.get("name"))
        """
        query = """
            query ListAgents(
                $customerId: ID!, $page: Int, $pageSize: Int,
                $search: String, $sort: String, $sortDir: SortDirection
            ) {
                agents(
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
                        connectionStatus
                        agentType
                        hostOs
                        currentSoftwareVersion
                        upgradeStatus
                        description
                        cloudProvider
                        publicIp
                        privateIps
                        adminStatus
                        agentGroupName
                        agentGroupType
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
            "operationName": "ListAgents",
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
            result = response.get_body().get("data", {}).get("agents", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_agent_connection_status_statistics(
        self,
        customer_id: str,
        search: Optional[str] = None,
    ) -> tuple:
        """
        Retrieve aggregated statistics for agent connection statuses.

        Args:
            customer_id: The customer ID.
            search: Optional search filter.

        Returns:
            tuple: (statistics dict, response, error)

        Examples:
            Get connection status stats::

                >>> result, _, err = client.zms.agents.get_agent_connection_status_statistics(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> print(result.get("totalCount"))
        """
        query = """
            query AgentConnectionStatusStats($customerId: ID!, $search: String) {
                agentConnectionStatusStatistics(
                    customerId: $customerId,
                    search: $search
                ) {
                    totalCount
                    totalPercentage
                    agentStatuses {
                        agentType
                        connectionStatus
                        count
                        percentage
                    }
                }
            }
        """

        variables: Dict[str, Any] = {"customerId": customer_id}
        if search is not None:
            variables["search"] = search

        body = {
            "query": query,
            "variables": variables,
            "operationName": "AgentConnectionStatusStats",
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
            result = response.get_body().get("data", {}).get("agentConnectionStatusStatistics", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_agent_version_statistics(
        self,
        customer_id: str,
        search: Optional[str] = None,
    ) -> tuple:
        """
        Retrieve aggregated statistics for agent versions.

        Args:
            customer_id: The customer ID.
            search: Optional search filter.

        Returns:
            tuple: (statistics dict, response, error)

        Examples:
            Get agent version stats::

                >>> result, _, err = client.zms.agents.get_agent_version_statistics(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for v in result.get("agentVersions", []):
                ...     print(v.get("version"), v.get("count"))
        """
        query = """
            query AgentVersionStats($customerId: ID!, $search: String) {
                agentVersionStatistics(
                    customerId: $customerId,
                    search: $search
                ) {
                    totalCount
                    totalPercentage
                    agentVersions {
                        agentType
                        version
                        count
                        percentage
                    }
                }
            }
        """

        variables: Dict[str, Any] = {"customerId": customer_id}
        if search is not None:
            variables["search"] = search

        body = {
            "query": query,
            "variables": variables,
            "operationName": "AgentVersionStats",
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
            result = response.get_body().get("data", {}).get("agentVersionStatistics", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
