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
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.microtenant_id] {str}: ID of the microtenant, if applicable.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            list: A list of `PrivilegedRemoteAccessConsole` instances.
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

        response, error = self._request_executor.execute(request)
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

        Returns:
            PrivilegedRemoteAccessConsole: The corresponding console object.
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
            pra_portal_ids (list): A list of PRA portal IDs.
            enabled (bool): Whether the console is enabled.

        Keyword Args:
            description (str): The description of the console.

        Returns:
            PrivilegedRemoteAccessConsole: The newly created console.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praConsole
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Extract 'pra_application_id' and 'pra_portal_ids' from body or kwargs
        pra_application_id = body.pop("pra_application_id", None) or kwargs.pop("pra_application_id", None)
        pra_portal_ids = body.pop("pra_portal_ids", None) or kwargs.pop("pra_portal_ids", None)

        # Ensure these fields are included in the payload
        if pra_application_id:
            body.update({"praApplication": {"id": pra_application_id}})
        if pra_portal_ids:
            body.update({"praPortals": [{"id": portal_id} for portal_id in pra_portal_ids]})

        # Update the body with any additional kwargs
        body.update(kwargs)

        # Handle the microtenant_id if present
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
            PrivilegedRemoteAccessConsole: The updated console.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praConsole/{console_id}
        """
        )

        # Start with an empty body or an existing resource's current data
        body = {}

        # Update the body with the fields passed in kwargs
        body.update(kwargs)

        # Extract 'pra_application_id' and 'pra_portal_ids' from body or kwargs
        pra_application_id = body.pop("pra_application_id", None) or kwargs.pop("pra_application_id", None)
        pra_portal_ids = body.pop("pra_portal_ids", None) or kwargs.pop("pra_portal_ids", None)

        # Ensure these fields are included in the payload
        if pra_application_id:
            body.update({"praApplication": {"id": pra_application_id}})
        if pra_portal_ids:
            body.update({"praPortals": [{"id": portal_id} for portal_id in pra_portal_ids]})

        # Update the body with any additional kwargs
        body.update(kwargs)

        # Handle the microtenant_id if present
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create and send the request
        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessConsole)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
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

    def add_bulk_console(self, consoles: list, **kwargs) -> list:
        """
        Adds multiple Privileged Remote Access (PRA) consoles in bulk.

        Args:
            consoles (list): A list of dictionaries, each containing details for a console.

        Returns:
            list: A list of newly created PRA consoles.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praConsole/bulk
        """
        )

        # Build the payload from the list of consoles
        body = []
        for console in consoles:
            if isinstance(console, dict):
                console_data = console
            else:
                console_data = console.as_dict()

            # Construct each console object for the payload
            body.append(
                {
                    "name": console_data.get("name"),
                    "enabled": console_data.get("enabled", True),
                    "praApplication": {"id": console_data.get("pra_application_id")},
                    "praPortals": [{"id": portal_id} for portal_id in console_data.get("pra_portal_ids", [])],
                    "description": console_data.get("description", ""),
                }
            )

        # Add additional arguments from kwargs to the payload if needed
        for entry in body:
            entry.update(kwargs)

        # Check if microtenant_id is set in kwargs and add it to params
        microtenant_id = kwargs.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Locally handle the list case for body since create_request expects a dictionary
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=None,  # Pass `None` for the body since we'll handle the list separately
            params=params,
        )
        if error:
            return (None, None, error)

        # Directly pass the body (which is a list) to the HTTP client's execution method
        request["json"] = body  # Attach the list directly as JSON for bulk processing

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        # Parse the result from the response
        try:
            result = [PrivilegedRemoteAccessConsole(self.form_response_body(console)) for console in response.get_body()]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
