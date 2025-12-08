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
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.application_servers import AppServers
from zscaler.api_client import APIClient
from zscaler.utils import format_url


class AppServersAPI(APIClient):
    """
    A Client object for the Application Server resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_servers(self, query_params: Optional[dict] = None) -> List[AppServers]:
        """
        Enumerates application servers in your organization with pagination.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[AppServers]: A list of ApplicationServer instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     servers = client.zpa.servers.list_servers()
            ...     for server in servers:
            ...         print(server.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/server")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppServers)

        return [AppServers(self.form_response_body(item)) for item in response.get_results()]

    def list_servers_summary(self, query_params: Optional[dict] = None) -> List[AppServers]:
        """
        Retrieves all configured application servers Name and IDs.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[AppServers]: A list of ApplicationServer instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     servers = client.zpa.servers.list_servers_summary()
            ...     for server in servers:
            ...         print(server.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/server/summary")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppServers)

        return [AppServers(self.form_response_body(item)) for item in response.get_results()]

    def get_server(self, server_id: str, query_params: Optional[dict] = None) -> AppServers:
        """
        Gets information on the specified server.

        Args:
            server_id (str): The unique identifier of the server.
            query_params (dict, optional): Map of query parameters.

        Returns:
            AppServers: The corresponding server object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     server = client.zpa.servers.get_server('999999')
            ...     print(server.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/server/{server_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppServers)

        return AppServers(self.form_response_body(response.get_body()))

    def add_server(self, **kwargs) -> AppServers:
        """
        Add a new application server.

        Args:
            **name (str): The name of the server.
            **description (str): Description of the server.
            **address (str): The IP address of the server.
            **enabled (bool): Enable the server. Defaults to True.
            **app_server_group_ids (list): List of Server Group IDs.
            **config_space (str): Configuration space.
            **microtenant_id (str): The microtenant ID.

        Returns:
            AppServers: The newly created server object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     server = client.zpa.servers.add_server(
            ...         name="NewAppServer",
            ...         address="192.168.1.1",
            ...         enabled=True
            ...     )
            ...     print(server.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/server")

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, AppServers)

        return AppServers(self.form_response_body(response.get_body()))

    def update_server(self, server_id: str, **kwargs) -> AppServers:
        """
        Updates the specified server.

        Args:
            server_id (str): The unique identifier for the server.
            **kwargs: Fields to update.

        Returns:
            AppServers: The updated application server object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     server = client.zpa.servers.update_server(
            ...         "999999",
            ...         name="UpdatedServer",
            ...         enabled=True
            ...     )
            ...     print(server.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/server/{server_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, AppServers)

        if response is None:
            return AppServers({"id": server_id})

        return AppServers(self.form_response_body(response.get_body()))

    def delete_server(self, server_id: str, microtenant_id: str = None) -> None:
        """
        Delete the specified server.

        Args:
            server_id (str): The unique identifier for the server.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.servers.delete_server('999999')
            ...     print("Server deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/server/{server_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
