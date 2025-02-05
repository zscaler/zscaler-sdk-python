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

    def list_servers(self, query_params=None) -> tuple:
        """
        Enumerates application servers in your organization with pagination.
        A subset of application servers can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.
                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            tuple: A tuple containing (list of ApplicationServer instances, Response, error)

        Example:
            >>> servers = zpa.servers.list_servers(
                query_params={"search": "Example100", "pagesize": 100}
                microtenant_id="216199618143464722")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /server
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        # Prepare request
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(AppServers(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_server(self, server_id: str, query_params=None) -> tuple:
        """
        Gets information on the specified server.

        Args:
            server_id (str): The unique identifier of the server.

        Returns:
            AppServers: The corresponding server object.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /server/{server_id}
        """)

        # Handle optional query parameters
        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, AppServers)
        if error:
            return (None, response, error)

        try:
            result = AppServers(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_server(self, **kwargs) -> tuple:
        """
        Add a new application server.

        Args:
            **name (str): The name of the server.
            **description (str): The name of the server.
            **address (str): The IP address of the server.
            **enabled (bool): Enable the server. Defaults to True.
            **app_server_group_ids (list):
                The list of unique identifiers for the Server Group.
            **config_space (str): The configuration space. Accepted values are `DEFAULT` or `SIEM`.
            **microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /server""")

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, AppServers)
        if error:
            return (None, response, error)

        try:
            result = AppServers(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_server(self, server_id: str, **kwargs) -> tuple:
        """
        Updates the specified server.

        Args:
            server_id (str): The unique identifier for the server being updated.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /server/{server_id}
        """)

        # Start with an empty body or an existing resource's current data
        body = {}

        # Update the body with the fields passed in kwargs
        body.update(kwargs)

        # Use get instead of pop to keep microtenant_id in the body
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, AppServers)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (AppServers({"id": server_id}), None, None)

        # Parse the response into an AppConnectorGroup instance
        try:
            result = AppServers(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_server(self, server_id: str, microtenant_id: str = None) -> tuple:
        """
        Delete the specified server.

        Args:
            server_id (str): The unique identifier for the server to be deleted.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            int: Status code of the delete operation.
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /server/{server_id}
        """)

        # Handle microtenant_id in URL params if provided
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
