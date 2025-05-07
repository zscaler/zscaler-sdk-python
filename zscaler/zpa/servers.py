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

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            :obj:`Tuple`: A tuple containing (list of ApplicationServer instances, Response, error)

        Examples:
            >>> server_list, _, err = client.zpa.servers.list_servers(
            ... query_params={'search': 'Server01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing application servers: {err}")
            ...     return
            ... print(f"Total application servers found: {len(server_list)}")
            ... for server in server_list:
            ...     print(server.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /server
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppServers)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(AppServers(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_server(self, server_id: str, query_params=None) -> tuple:
        """
        Gets information on the specified server.

        Args:
            server_id (str): The unique identifier of the server.

        Returns:
            :obj:`Tuple`: AppServers: The corresponding server object.

        Examples:
            >>> fetched_server, _, err = client.zpa.servers.get_server('999999')
            ... if err:
            ...     print(f"Error fetching app server by ID: {err}")
            ...     return
            ... print(f"Fetched app server by ID: {fetched_server.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /server/{server_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppServers)
        if error:
            return (None, response, error)

        try:
            result = AppServers(self.form_response_body(response.get_body()))
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

        Returns:
            :obj:`Tuple`: AppServers: The newly created portal object.

        Examples:
            >>> new_server, _, err = client.zpa.servers.add_server(
            ...     name="NewAppServer",
            ...     description="NewAppServer",
            ...     enabled=True,
            ...     app_server_group_ids=['99999'],
            ... )
            ... if err:
            ...     print(f"Error creating app server: {err}")
            ...     return
            ... print(f"app server created successfully: {new_portal.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /server"""
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppServers)
        if error:
            return (None, response, error)

        try:
            result = AppServers(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_server(self, server_id: str, **kwargs) -> tuple:
        """
        Updates the specified server.

        Args:
            server_id (str): The unique identifier for the server being updated.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            :obj:`Tuple`: AppServers: The updated application server object.

        Examples:
            >>> update_server, _, err = client.zpa.servers.update_server(
            ...     server_id="999999",
            ...     name="UdpateApplicationServer",
            ...     description="UdpateApplicationServer",
            ...     enabled=True,
            ... )
            ... if err:
            ...     print(f"Error creating application servers: {err}")
            ...     return
            ... print(f"application servers created successfully: {new_portal.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /server/{server_id}
        """
        )

        body = {}

        body.update(kwargs)

        # Use get instead of pop to keep microtenant_id in the body
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppServers)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (AppServers({"id": server_id}), None, None)

        try:
            result = AppServers(self.form_response_body(response.get_body()))
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

        Examples:
            >>> _, _, err = client.zpa.servers.delete_server(
            ...     server_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting application server: {err}")
            ...     return
            ... print(f"application server with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /server/{server_id}
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
