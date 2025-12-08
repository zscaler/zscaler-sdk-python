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
from zscaler.zpa.models.app_connectors import AppConnectorController
from zscaler.utils import format_url


class AppConnectorControllerAPI(APIClient):
    """
    A Client object for the App Connectors resource.
    """

    reformat_params = [
        ("connector_ids", "connectors"),
        ("server_group_ids", "serverGroups"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_connectors(self, query_params: Optional[dict] = None) -> List[AppConnectorController]:
        """
        Enumerates app connectors in your organization with pagination.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[AppConnectorController]: A list of App Connector instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     connectors = client.zpa.app_connectors.list_connectors(
            ...         query_params={'search': 'Connector01'}
            ...     )
            ...     for connector in connectors:
            ...         print(connector.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/connector")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppConnectorController)

        return [AppConnectorController(self.form_response_body(item)) for item in response.get_results()]

    def get_connector(self, connector_id: str, query_params: Optional[dict] = None) -> AppConnectorController:
        """
        Returns information on the specified App Connector.

        Args:
            connector_id (str): The unique id for the ZPA App Connector.
            query_params (dict, optional): Map of query parameters.

        Returns:
            AppConnectorController: The specified App Connector resource record.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     connector = client.zpa.app_connectors.get_connector('999999')
            ...     print(connector.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/connector/{connector_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppConnectorController)

        return AppConnectorController(self.form_response_body(response.get_body()))

    def update_connector(self, connector_id: str, **kwargs) -> AppConnectorController:
        """
        Updates an existing ZPA App Connector.

        Args:
            connector_id (str): The unique id of the ZPA App Connector.
            **name (str): The name of the App Connector.
            **description (str): Additional information about the App Connector.
            **enabled (bool): True if the App Connector is enabled.

        Returns:
            AppConnectorController: The updated App Connector resource record.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     updated = client.zpa.app_connectors.update_connector(
            ...         '99999',
            ...         name="UpdatedConnector",
            ...         enabled=False
            ...     )
            ...     print(updated.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/connector/{connector_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, AppConnectorController)

        if response is None:
            return AppConnectorController({"id": connector_id})

        return AppConnectorController(self.form_response_body(response.get_body()))

    def delete_connector(self, connector_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified App Connector from ZPA.

        Args:
            connector_id (str): The unique id for the ZPA App Connector.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.app_connectors.delete_connector('999999')
            ...     print("Connector deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/connector/{connector_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)

    def bulk_delete_connectors(self, connector_ids: list, microtenant_id: str = None) -> None:
        """
        Deletes all specified App Connectors from ZPA.

        Args:
            connector_ids (list): List of unique ids for the App Connectors to delete.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.app_connectors.bulk_delete_connectors(
            ...         ['72058304855098016', '72058304855098017']
            ...     )
            ...     print("Connectors deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/connector/bulkDelete")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}
        payload = {"ids": connector_ids}

        request = self._request_executor.create_request(http_method, api_url, payload, params=params)
        self._request_executor.execute(request)
