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
from zscaler.zpa.models.server_group import ServerGroup
from zscaler.utils import format_url, add_id_groups


class ServerGroupsAPI(APIClient):
    """
    A client object for the Server Groups resource.
    """

    reformat_params = [
        ("server_ids", "servers"),
        ("app_connector_group_ids", "appConnectorGroups"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_groups(self, query_params: Optional[dict] = None) -> List[ServerGroup]:
        """
        Enumerates server groups in your organization with pagination.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[ServerGroup]: A list of ServerGroup instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     groups = client.zpa.server_groups.list_groups()
            ...     for group in groups:
            ...         print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/serverGroup")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ServerGroup)

        return [ServerGroup(self.form_response_body(item)) for item in response.get_results()]

    def get_group(self, group_id: str, query_params: Optional[dict] = None) -> ServerGroup:
        """
        Provides information on the specified server group.

        Args:
            group_id (str): The unique id for the server group.
            query_params (dict, optional): Map of query parameters.

        Returns:
            ServerGroup: The server group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.server_groups.get_group('999999')
            ...     print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/serverGroup/{group_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ServerGroup)

        return ServerGroup(self.form_response_body(response.get_body()))

    def add_group(self, **kwargs) -> ServerGroup:
        """
        Adds a server group.

        Args:
            name (str): The name for the server group.
            app_connector_group_ids (list): A list of App connector IDs.
            **description (str): Additional information about the server group.
            **enabled (bool): Enable the server group.
            **ip_anchored (bool): Enable IP Anchoring.
            **dynamic_discovery (bool): Enable Dynamic Discovery.
            **server_ids (list): List of server IDs.
            **microtenant_id (str): The microtenant ID.

        Returns:
            ServerGroup: The created server group.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.server_groups.add_group(
            ...         name='new_server_group',
            ...         app_connector_group_ids=['99999']
            ...     )
            ...     print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/serverGroup")

        body = kwargs
        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "app_connector_group_ids" in body:
            body["appConnectorGroups"] = [{"id": gid} for gid in body.pop("app_connector_group_ids")]

        if "server_ids" in body:
            body["servers"] = [{"id": gid} for gid in body.pop("server_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, ServerGroup)

        return ServerGroup(self.form_response_body(response.get_body()))

    def update_group(self, group_id: str, **kwargs) -> ServerGroup:
        """
        Updates a server group.

        Args:
            group_id (str): The unique identifier for the server group.
            **kwargs: Fields to update.

        Returns:
            ServerGroup: The updated server group.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.server_groups.update_group(
            ...         "999999",
            ...         name='updated_server_group',
            ...         enabled=True
            ...     )
            ...     print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/serverGroup/{group_id}")

        # Fetch the existing group to preserve mandatory fields
        existing_group = self.get_group(group_id)
        body = existing_group.request_format()
        body.update(kwargs)

        if "dynamicDiscovery" not in body:
            body["dynamicDiscovery"] = True

        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "app_connector_group_ids" in body:
            body["appConnectorGroups"] = [{"id": gid} for gid in body.pop("app_connector_group_ids")]

        if "server_ids" in body:
            body["servers"] = [{"id": gid} for gid in body.pop("server_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, ServerGroup)

        if response is None:
            return ServerGroup({"id": group_id})

        return ServerGroup(self.form_response_body(response.get_body()))

    def delete_group(self, group_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified server group.

        Args:
            group_id (str): The unique id for the server group.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.server_groups.delete_group('999999')
            ...     print("Group deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/serverGroup/{group_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
