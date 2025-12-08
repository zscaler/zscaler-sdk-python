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
from zscaler.zpa.models.pra_console import PrivilegedRemoteAccessConsole
from zscaler.utils import format_url


class PRAConsoleAPI(APIClient):
    """
    A Client object for the Privileged Remote Access Console resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_consoles(self, query_params: Optional[dict] = None) -> List[PrivilegedRemoteAccessConsole]:
        """
        Returns a list of all PRA consoles.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[PrivilegedRemoteAccessConsole]: A list of PRA console instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     consoles = client.zpa.pra_console.list_consoles()
            ...     for console in consoles:
            ...         print(console.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/praConsole")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)

        return [PrivilegedRemoteAccessConsole(self.form_response_body(item)) for item in response.get_results()]

    def get_console(self, console_id: str, query_params: Optional[dict] = None) -> PrivilegedRemoteAccessConsole:
        """
        Returns information on a specific PRA console.

        Args:
            console_id (str): The unique identifier for the PRA console.
            query_params (dict, optional): Map of query parameters.

        Returns:
            PrivilegedRemoteAccessConsole: The console object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     console = client.zpa.pra_console.get_console('999999')
            ...     print(console.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/praConsole/{console_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)

        return PrivilegedRemoteAccessConsole(self.form_response_body(response.get_body()))

    def get_console_portal(self, portal_id: str, query_params: Optional[dict] = None) -> PrivilegedRemoteAccessConsole:
        """
        Returns information on PRA Consoles for specified Portal.

        Args:
            portal_id (str): The unique identifier for the PRA portal.
            query_params (dict, optional): Map of query parameters.

        Returns:
            PrivilegedRemoteAccessConsole: The console object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     console = client.zpa.pra_console.get_console_portal('999999')
            ...     print(console.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/praConsole/praPortal/{portal_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)

        return PrivilegedRemoteAccessConsole(self.form_response_body(response.get_body()))

    def add_console(self, **kwargs) -> PrivilegedRemoteAccessConsole:
        """
        Adds a new PRA console.

        Args:
            name (str): The name of the console.
            pra_application_id (str): The ID of the PRA application.
            pra_portal_ids (list): A list of PRA portal IDs.
            enabled (bool): Whether the console is enabled.

        Returns:
            PrivilegedRemoteAccessConsole: The newly created console.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     console = client.zpa.pra_console.add_console(
            ...         name="new_rdp_console",
            ...         enabled=True,
            ...         pra_application_id='72058304855096642',
            ...         pra_portal_ids=['72058304855093465']
            ...     )
            ...     print(console.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/praConsole")

        body = kwargs

        pra_application_id = body.pop("pra_application_id", None)
        pra_portal_ids = body.pop("pra_portal_ids", None)

        if pra_application_id:
            body["praApplication"] = {"id": pra_application_id}
        if pra_portal_ids:
            body["praPortals"] = [{"id": portal_id} for portal_id in pra_portal_ids]

        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)

        return PrivilegedRemoteAccessConsole(self.form_response_body(response.get_body()))

    def update_console(self, console_id: str, **kwargs) -> PrivilegedRemoteAccessConsole:
        """
        Updates the specified PRA console.

        Args:
            console_id (str): The unique identifier for the console.
            **kwargs: Fields to update.

        Returns:
            PrivilegedRemoteAccessConsole: The updated console.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     console = client.zpa.pra_console.update_console(
            ...         '999999',
            ...         name="updated_console",
            ...         enabled=True
            ...     )
            ...     print(console.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/praConsole/{console_id}")

        body = dict(kwargs)

        pra_application_id = body.pop("pra_application_id", None)
        pra_portal_ids = body.pop("pra_portal_ids", None)

        if pra_application_id:
            body["praApplication"] = {"id": pra_application_id}
        if pra_portal_ids:
            body["praPortals"] = [{"id": portal_id} for portal_id in pra_portal_ids]

        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)

        if response is None:
            return PrivilegedRemoteAccessConsole({"id": console_id})

        return PrivilegedRemoteAccessConsole(self.form_response_body(response.get_body()))

    def delete_console(self, console_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified PRA console.

        Args:
            console_id (str): The unique identifier for the console.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.pra_console.delete_console('999999')
            ...     print("Console deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/praConsole/{console_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)

    def add_bulk_console(self, consoles: list, **kwargs) -> List[PrivilegedRemoteAccessConsole]:
        """
        Adds multiple PRA consoles in bulk.

        Args:
            consoles (list): A list of dictionaries with console details.

        Returns:
            List[PrivilegedRemoteAccessConsole]: A list of created consoles.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     consoles = client.zpa.pra_console.add_bulk_console([
            ...         {"name": "console1", "enabled": True, "pra_application_id": "123", "pra_portal_ids": ["456"]}
            ...     ])
            ...     for console in consoles:
            ...         print(console.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/praConsole/bulk")

        body = []
        for console in consoles:
            console_data = console if isinstance(console, dict) else console.as_dict()
            body.append({
                "name": console_data.get("name"),
                "enabled": console_data.get("enabled", True),
                "praApplication": {"id": console_data.get("pra_application_id")},
                "praPortals": [{"id": pid} for pid in console_data.get("pra_portal_ids", [])],
                "description": console_data.get("description", ""),
            })

        microtenant_id = kwargs.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=None, params=params)
        request["json"] = body
        response = self._request_executor.execute(request)

        return [PrivilegedRemoteAccessConsole(self.form_response_body(console)) for console in response.get_body()]
