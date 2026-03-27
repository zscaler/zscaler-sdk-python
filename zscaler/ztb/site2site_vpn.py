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

from typing import Dict, Any, Optional, List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.site2site_vpn import (
    CloudGatewayHub,
    S2SConnection,
    S2SDeleteRequest,
    S2SHubs,
    ClusterGatewayWithInterfaces,
    S2SHubItem,
)


class Site2SiteVPNAPI(APIClient):
    """
    Client for the ZTB Site2Site VPN (Cloud Gateway) resource.

    Provides operations for managing cloud gateways, S2S VPN connections,
    and S2S hubs in the Zero Trust Branch API.
    """

    _ztb_base_endpoint = "/ztb/api/v3"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_hubs(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get list of cloud gateways used as a hub.

        Args:
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.search]`` (str): Search string for filtering results.
                ``[query_params.page]`` (int): Page number for pagination.
                ``[query_params.limit]`` (int): Page size / limit.
                ``[query_params.sort]`` (str): Sort field. Available values:
                location, region, sites, public_ip, gateway_name,
                operational_state, updated_at, created_at.
                ``[query_params.sortdir]`` (str): Sort direction. Available values:
                asc, desc. Default: desc.

        Returns:
            tuple: (list of CloudGatewayHub instances, Response, error).

        Examples:
            >>> hubs, _, error = client.ztb.site2site_vpn.list_hubs()
            >>> if error:
            ...     print(f"Error listing hubs: {error}")
            ...     return
            >>> for hub in hubs:
            ...     print(hub.as_dict())

            With pagination and search:
            >>> hubs, _, error = client.ztb.site2site_vpn.list_hubs(
            ...     query_params={"search": "prod", "page": 1, "limit": 25, "sort": "region", "sortdir": "asc"}
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /CloudGateway/hubs
        """)
        query_params = query_params or {}
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CloudGatewayHub(self.form_response_body(item)))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_s2s_connections(self, cluster_id: int) -> APIResult:
        """
        Get cluster S2S VPN connections.

        Args:
            cluster_id (int): The cluster ID.

        Returns:
            tuple: (S2SConnection instance, Response, error).

        Examples:
            >>> conn, _, error = client.ztb.site2site_vpn.get_s2s_connections(12345)
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(conn.as_dict())
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /CloudGateway/s2s/{cluster_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            payload = response.get_body()
            if payload and "result" in payload:
                result = S2SConnection(self.form_response_body(payload))
            else:
                result = S2SConnection({})
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def create_s2s_connections(self, cluster_id: int, connection: S2SConnection) -> APIResult:
        """
        Create cluster S2S VPN connections.

        Args:
            cluster_id (int): The cluster ID.
            connection (S2SConnection): Connection payload (connect_to_hub, gateways, hubs).

        Returns:
            tuple: (created S2SConnection or None, Response, error).

        Examples:
            >>> conn = S2SConnection()
            >>> conn.connect_to_hub = True
            >>> conn.gateways = [...]
            >>> conn.hubs = S2SHubs({"primary_id": 1, "secondary_id": 2})
            >>> result, _, error = client.ztb.site2site_vpn.create_s2s_connections(12345, conn)
        """
        http_method = "POST"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /CloudGateway/s2s/{cluster_id}
        """)
        body = connection.request_format() if connection else {}
        headers = {"Content-Type": "application/json"}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            payload = response.get_body()
            result = S2SConnection(self.form_response_body(payload)) if payload else None
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def update_s2s_connections(self, cluster_id: int, connection: S2SConnection) -> APIResult:
        """
        Update existing cluster S2S VPN connections.

        Args:
            cluster_id (int): The cluster ID.
            connection (S2SConnection): Full connection payload including gateway ids.

        Returns:
            tuple: (updated S2SConnection or None, Response, error).
        """
        http_method = "PUT"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /CloudGateway/s2s/{cluster_id}
        """)
        body = connection.request_format() if connection else {}
        headers = {"Content-Type": "application/json"}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            payload = response.get_body()
            result = S2SConnection(self.form_response_body(payload)) if payload else None
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def delete_s2s_connections(self, cluster_id: int, gateway_ids: List[str]) -> APIResult:
        """
        Delete cluster S2S VPN connections by gateway IDs.

        Args:
            cluster_id (int): The cluster ID.
            gateway_ids (list): List of gateway IDs to remove from S2S.

        Returns:
            tuple: (None, Response, error).

        Examples:
            >>> _, resp, error = client.ztb.site2site_vpn.delete_s2s_connections(
            ...     12345, ["gw-1", "gw-2"]
            ... )
        """
        http_method = "DELETE"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /CloudGateway/s2s/{cluster_id}
        """)
        req = S2SDeleteRequest({"gateway_ids": gateway_ids})
        body = req.request_format()
        headers = {"Content-Type": "application/json"}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_s2s_gateways(self, cluster_id: int) -> APIResult:
        """
        Get list of cluster gateways with their interfaces.

        Args:
            cluster_id (int): The cluster ID.

        Returns:
            tuple: (list of ClusterGatewayWithInterfaces, Response, error).

        Examples:
            >>> gateways, _, error = client.ztb.site2site_vpn.get_s2s_gateways(12345)
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for gw in gateways:
            ...     print(gw.as_dict())
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /CloudGateway/s2s/{cluster_id}/gateways
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            payload = response.get_body()
            raw = (payload or {}).get("result") or []
            result = [ClusterGatewayWithInterfaces(self.form_response_body(item)) for item in raw]
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def list_s2s_hubs(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get S2S VPN hub list (cloud hubs for S2S VPN).

        Args:
            query_params (dict, optional): Query parameters.
                ``[query_params.provider]`` (str): Filter by provider. Available: aws, vultr.

        Returns:
            tuple: (list of S2SHubItem instances, Response, error).

        Examples:
            >>> hubs, _, error = client.ztb.site2site_vpn.list_s2s_hubs()
            >>> hubs, _, error = client.ztb.site2site_vpn.list_s2s_hubs(
            ...     query_params={"provider": "aws"}
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /CloudGateway/s2s_hubs
        """)
        query_params = query_params or {}
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            payload = response.get_body()
            raw = (payload or {}).get("result") or []
            result = [S2SHubItem(self.form_response_body(item)) for item in raw]
        except Exception as err:
            return (None, response, err)
        return (result, response, None)
