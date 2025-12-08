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

from typing import List, Optional
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.service_edges import ServiceEdge
from zscaler.utils import format_url


class ServiceEdgeControllerAPI(APIClient):
    reformat_params = [
        ("service_edge_ids", "serviceEdges"),
        ("trusted_network_ids", "trustedNetworks"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_service_edges(self, query_params: Optional[dict] = None) -> List[ServiceEdge]:
        """
        Enumerates service edges in your organization with pagination.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[ServiceEdge]: A list of ServiceEdge instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     edges = client.zpa.service_edges.list_service_edges()
            ...     for edge in edges:
            ...         print(edge.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdge")

        query_params = query_params or {}
        if microtenant_id := query_params.pop("microtenant_id", None):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ServiceEdge)

        return [ServiceEdge(self.form_response_body(item)) for item in response.get_results()]

    def get_service_edge(self, service_edge_id: str, **kwargs) -> ServiceEdge:
        """
        Returns information on the specified Service Edge.

        Args:
            service_edge_id (str): The unique ID of the ZPA Service Edge.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            ServiceEdge: The corresponding Service Edge object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     edge = client.zpa.service_edges.get_service_edge('999999')
            ...     print(edge.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdge/{service_edge_id}")

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)

        return ServiceEdge(response.get_body())

    def update_service_edge(self, service_edge_id: str, **kwargs) -> ServiceEdge:
        """
        Updates the specified ZPA Service Edge.

        Args:
            service_edge_id (str): The unique ID of the Service Edge.
            **name (str): The name of the Service Edge.
            **description (str): Additional information about the Service Edge.
            **enabled (bool): True if the Service Edge is enabled.

        Returns:
            ServiceEdge: The updated Service Edge object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     updated = client.zpa.service_edges.update_service_edge(
            ...         '99999',
            ...         name="UpdatedEdge",
            ...         enabled=False
            ...     )
            ...     print(updated.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdge/{service_edge_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, ServiceEdge)

        if response is None:
            return ServiceEdge({"id": service_edge_id})

        return ServiceEdge(self.form_response_body(response.get_body()))

    def delete_service_edge(self, service_edge_id: str, **kwargs) -> None:
        """
        Deletes the specified ZPA Service Edge.

        Args:
            service_edge_id (str): The unique ID of the Service Edge.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.service_edges.delete_service_edge('999999')
            ...     print("Service Edge deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdge/{service_edge_id}")

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)

    def bulk_delete_service_edges(self, service_edge_ids: list, **kwargs) -> None:
        """
        Bulk deletes the specified Service Edges from ZPA.

        Args:
            service_edge_ids (list): A list of Service Edge IDs to delete.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.service_edges.bulk_delete_service_edges(['id1', 'id2'])
            ...     print("Service Edges deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdge/bulkDelete")

        payload = {"ids": service_edge_ids}
        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        self._request_executor.execute(request)
