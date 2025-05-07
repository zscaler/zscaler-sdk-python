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

    def list_consoles(self, query_params=None) -> tuple:
        """
        Returns a list of all Privileged Remote Access (PRA) consoles.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            list: A list of `PrivilegedRemoteAccessConsole` instances.

        Examples:
            >>> consoles_list, _, err = client.zpa.pra_console.list_consoles(
            ... query_params={'search': 'pra_console01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing pra consoles: {err}")
            ...     return
            ... print(f"Total pra consoles found: {len(consoles_list)}")
            ... for pra in consoles_list:
            ...     print(pra.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praConsole
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PrivilegedRemoteAccessConsole(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_console(self, console_id: str, query_params=None) -> tuple:
        """
        Returns information on a specific PRA console.

        Args:
            console_id (str): The unique identifier for the PRA console.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: PrivilegedRemoteAccessConsole: The corresponding console object.

        Examples:
            >>> fetched_console, _, err = client.zpa.pra_console.get_console('999999')
            ... if err:
            ...     print(f"Error fetching console by ID: {err}")
            ...     return
            ... print(f"Fetched console by ID: {fetched_console.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /praConsole/{console_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessConsole(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_console_portal(self, portal_id: str, query_params=None) -> tuple:
        """
        Returns information on a Privileged Remote Consoles for Specified Portal.

        Args:
            console_id (str): The unique identifier for the PRA console.

        Returns:
            PrivilegedRemoteAccessConsole: The corresponding console object.

        Examples:
            >>> fetched_console, _, err = client.zpa.pra_console.get_console_portal('999999')
            ... if err:
            ...     print(f"Error fetching console by ID: {err}")
            ...     return
            ... print(f"Fetched console by ID: {fetched_console.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /praConsole/praPortal/{portal_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessConsole(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_console(self, **kwargs) -> tuple:
        """
        Adds a new Privileged Remote Access (PRA) console.

        Args:
            name (str): The name of the console.
            pra_application_id (str): The ID of the PRA application.
            pra_portal_ids (list[str]): A list of PRA portal IDs.
            enabled (bool): Whether the console is enabled.

        Keyword Args:
            description (str, optional): The description of the console.

        Returns:
            tuple: A tuple containing:
                - **PrivilegedRemoteAccessConsole**: The newly created console instance.
                - **Response**: The raw API response object.
                - **Error**: An error message, if applicable.

        Examples:
            >>> new_console, _, err = client.zpa.pra_console.add_console(
            ...     name=f"new_rdp_console_{random.randint(1000, 10000)}",
            ...     description=f"new_rdp_console_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     pra_application_id='72058304855096642',
            ...     pra_portal_ids=['72058304855093465'],
            ... )
            ... if err:
            ...     print(f"Error creating console: {err}")
            ...     return
            ... print(f"Console created successfully: {new_console.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praConsole
        """
        )

        body = kwargs

        pra_application_id = body.pop("pra_application_id", None) or kwargs.pop("pra_application_id", None)
        pra_portal_ids = body.pop("pra_portal_ids", None) or kwargs.pop("pra_portal_ids", None)

        if pra_application_id:
            body.update({"praApplication": {"id": pra_application_id}})
        if pra_portal_ids:
            body.update({"praPortals": [{"id": portal_id} for portal_id in pra_portal_ids]})

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create and send the request
        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessConsole(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_console(self, console_id: str, **kwargs) -> tuple:
        """
        Updates the specified PRA console.

        Args:
            console_id (str): The unique identifier for the console.
            pra_application_id (str, optional): The ID of the PRA application.
            pra_portal_ids (list, optional): List of PRA portal IDs.

        Returns:
            :obj:`Tuple`: PrivilegedRemoteAccessConsole: The updated console.

        Examples:
            >>> updated_console, _, err = client.zpa.pra_console.update_console(
            ...     console_id='999999',
            ...     name=f"update_rdp_console_{random.randint(1000, 10000)}",
            ...     description=f"update_rdp_console_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     pra_application_id='72058304855096642',
            ...     pra_portal_ids=['72058304855093465'],
            ... )
            ... if err:
            ...     print(f"Error updating console: {err}")
            ...     return
            ... print(f"console updated successfully: {updated_console.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praConsole/{console_id}
        """
        )

        body = {}

        body.update(kwargs)

        pra_application_id = body.pop("pra_application_id", None) or kwargs.pop("pra_application_id", None)
        pra_portal_ids = body.pop("pra_portal_ids", None) or kwargs.pop("pra_portal_ids", None)

        if pra_application_id:
            body.update({"praApplication": {"id": pra_application_id}})
        if pra_portal_ids:
            body.update({"praPortals": [{"id": portal_id} for portal_id in pra_portal_ids]})

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)
        if error:
            return (None, response, error)

        if response is None:
            return (PrivilegedRemoteAccessConsole({"id": console_id}), None, None)

        try:
            result = PrivilegedRemoteAccessConsole(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_console(self, console_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified PRA console.

        Args:
            console_id (str): The unique identifier for the console.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:
            int: The status code of the delete operation.

        Examples:
            >>> _, _, err = client.zpa.pra_console.delete_console(
            ...     console_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting pra console: {err}")
            ...     return
            ... print(f"PRA Console with ID {updated_console.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praConsole/{console_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def add_bulk_console(self, consoles: list, **kwargs) -> tuple:
        """
        Adds multiple Privileged Remote Access (PRA) consoles in bulk.

        Args:
            consoles (list[dict]): A list of dictionaries, each containing details for a console.

        Returns:
            tuple: A tuple containing:
                - **list[PrivilegedRemoteAccessConsole]**: A list of newly created PRA console instances.
                - **Response**: The raw API response object.
                - **Error**: An error message, if applicable.

        Examples:
            >>> added_consoles, _, err = client.zpa.pra_console.add_bulk_console(
            ...     consoles=[
            ...         dict(
            ...             name=f"rdp_console_{random.randint(1000, 10000)}",
            ...             description=f"rdp_console_desc_{random.randint(1000, 10000)}",
            ...             enabled=True,
            ...             pra_application_id="72058304855096642",
            ...             pra_portal_ids=["72058304855093465"],
            ...         ),
            ...         dict(
            ...             name=f"ssh_console_{random.randint(1000, 10000)}",
            ...             description=f"ssh_console_desc_{random.randint(1000, 10000)}",
            ...             enabled=True,
            ...             pra_application_id="72058304855097808",
            ...             pra_portal_ids=["72058304855093465", "72058304855097809"],
            ...         )
            ...     ]
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praConsole/bulk
        """
        )
        body = []
        for console in consoles:
            if isinstance(console, dict):
                console_data = console
            else:
                console_data = console.as_dict()

            body.append(
                {
                    "name": console_data.get("name"),
                    "enabled": console_data.get("enabled", True),
                    "praApplication": {"id": console_data.get("pra_application_id")},
                    "praPortals": [{"id": portal_id} for portal_id in console_data.get("pra_portal_ids", [])],
                    "description": console_data.get("description", ""),
                }
            )

        for entry in body:
            entry.update(kwargs)

        microtenant_id = kwargs.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=None,
            params=params,
        )
        if error:
            return (None, None, error)

        request["json"] = body

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [PrivilegedRemoteAccessConsole(self.form_response_body(console)) for console in response.get_body()]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
