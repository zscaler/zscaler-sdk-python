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
from zscaler.zpa.models.service_edge_groups import ServiceEdgeGroup
from zscaler.utils import format_url


class ServiceEdgeGroupAPI(APIClient):
    """
    A Client object for the Service Edge Group resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_service_edge_groups(self, query_params: Optional[dict] = None) -> List[ServiceEdgeGroup]:
        """
        Enumerates service edge groups in your organization with pagination.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[ServiceEdgeGroup]: A list of ServiceEdgeGroup instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     groups = client.zpa.service_edge_group.list_service_edge_groups()
            ...     for group in groups:
            ...         print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdgeGroup")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ServiceEdgeGroup)

        return [ServiceEdgeGroup(self.form_response_body(item)) for item in response.get_results()]

    def get_service_edge_group(self, group_id: str, query_params: Optional[dict] = None) -> ServiceEdgeGroup:
        """
        Retrieves information about a specific service edge group.

        Args:
            group_id (str): The unique identifier of the service edge group.
            query_params (dict, optional): Map of query parameters.

        Returns:
            ServiceEdgeGroup: The service edge group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.service_edge_group.get_service_edge_group('999999')
            ...     print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdgeGroup/{group_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ServiceEdgeGroup)

        return ServiceEdgeGroup(self.form_response_body(response.get_body()))

    def add_service_edge_group(self, **kwargs) -> ServiceEdgeGroup:
        """
        Adds a new service edge group.

        Args:
            name (str): The name of the service edge group.
            latitude (str): The latitude of the physical location.
            longitude (str): The longitude of the physical location.
            location (str): The name of the location.
            **enabled (bool): Is the Service Edge Group enabled?
            **is_public (bool): Is the Service Edge publicly accessible?
            **service_edge_ids (list): List of Service Edge IDs.
            **trusted_network_ids (list): List of Trusted Network IDs.
            **upgrade_day (str): The day for upgrades.
            **upgrade_time_in_secs (str): The time for upgrades.

        Returns:
            ServiceEdgeGroup: The newly created service edge group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.service_edge_group.add_service_edge_group(
            ...         name="NewGroup",
            ...         latitude="37.3382082",
            ...         longitude="-121.8863286",
            ...         location="San Jose, CA, USA"
            ...     )
            ...     print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdgeGroup")

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "trusted_network_ids" in body:
            body["trustedNetworks"] = [{"id": nid} for nid in body.pop("trusted_network_ids")]

        if "service_edge_ids" in body:
            body["serviceEdges"] = [{"id": sid} for sid in body.pop("service_edge_ids")]

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, ServiceEdgeGroup)

        return ServiceEdgeGroup(self.form_response_body(response.get_body()))

    def update_service_edge_group(self, group_id: str, **kwargs) -> ServiceEdgeGroup:
        """
        Updates a specified service edge group.

        Args:
            group_id (str): The unique ID of the service edge group.
            **kwargs: Fields to update.

        Returns:
            ServiceEdgeGroup: The updated service edge group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.service_edge_group.update_service_edge_group(
            ...         '999999',
            ...         name="UpdatedGroup",
            ...         enabled=True
            ...     )
            ...     print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdgeGroup/{group_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "trusted_network_ids" in body:
            body["trustedNetworks"] = [{"id": nid} for nid in body.pop("trusted_network_ids")]

        if "service_edge_ids" in body:
            body["serviceEdges"] = [{"id": sid} for sid in body.pop("service_edge_ids")]

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, ServiceEdgeGroup)

        if response is None:
            return ServiceEdgeGroup({"id": group_id})

        return ServiceEdgeGroup(self.form_response_body(response.get_body()))

    def delete_service_edge_group(self, group_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified service edge group.

        Args:
            group_id (str): The unique ID of the service edge group.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.service_edge_group.delete_service_edge_group('999999')
            ...     print("Group deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/serviceEdgeGroup/{group_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
