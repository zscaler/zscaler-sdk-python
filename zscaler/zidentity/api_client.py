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
from zscaler.zidentity.models.api_client import APIClients
from zscaler.zidentity.models.api_client import APIClientRecords
from zscaler.zidentity.models.api_client import APIClientSecrets
from zscaler.utils import format_url


class APIClientAPI(APIClient):
    """
    A Client object for the API Client API resource.
    """

    _zidentity_base_endpoint = "/admin/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_api_clients(self, query_params=None) -> tuple:
        """
        Retrieves a paginated list of API clients
        providing details such as total records, current page offset, and links for pagination navigation

        See the `Zidentity API Client API reference <https://help.zscaler.com/zidentity/api-clients#/api-clients-get>`_
        for further detail on optional keyword parameter structures.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.offset]`` {int}: The starting point for pagination,
                    with the number of records that can be skipped before fetching results.

                ``[query_params.limit]`` {str}: The maximum number of records to return per request. Minimum: 0, Maximum: 1000
                ``[query_params.name[like]]`` {str}: Filters results by name using a partial match.

        Returns:
            tuple: A tuple containing (list of ApiClientSecrets instances, Response, error)

        Examples:
            List api clients using default settings:

            >>> client_list, response, error = zidentity.api_client.list_api_clients():
            ... if error:
            ...     print(f"Error listing clients: {error}")
            ...     return
            ... for client in client_list.records:
            ...     print(client.as_dict())

            List clients, limiting to a maximum of 10 items:

            >>> client_list, response, error = zidentity.api_client.list_api_clients(query_params={'limit': 10}):
            ... if error:
            ...     print(f"Error listing clients: {error}")
            ...     return
            ... for client in client_list.records:
            ...     print(client.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /api-clients
        """
        )
        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = APIClients(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_api_client(self, client_id: str) -> tuple:
        """
        Retrieves detailed information about a specific API client using its ID.

        Args:
            client_id (int): Unique identifier of the API client to be retrieved.

        Returns:
            tuple: A tuple containing ApiClients instance, Response, error).

        Examples:
            Print a specific api client

            >>> fetched_client, _, error = client.zidentity.api_client.get_api_client(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching client by ID: {error}")
            ...     return
            ... print(f"Fetched client by ID: {fetched_client.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /api-clients/{client_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, APIClientRecords)
        if error:
            return (None, response, error)

        try:
            result = APIClientRecords(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_api_client(self, **kwargs) -> tuple:
        """
        Creates a new API client with authentication settings and assigned roles.

        Args:
            name (str): The name of the OAuth2 client.
            description (str, optional): A description of the client.
            status (bool, optional): The status of the API client (enabled/disabled).
            access_token_life_time (int, optional): Whether the client is active (true) or inactive (false).
            client_authentication (dict, optional): Configuration details for the client authentication.

                - auth_type (str, optional): The method of client authentication (e.g., "SECRET", "PUBKEYCERT", "JWKS").
                - client_jw_ks_url (str, optional): URL for the JSON Web Keys used for authentication.
                - public_keys (list, optional): A list of public key information objects.
                    - key_name (str, optional): The name of the public key.
                    - key_value (str, optional): The value of the public key.
                - client_certificates (list, optional): Certificate information for the client.
                    - cert_content (str, optional): The content of the certificate in a string format.

            client_resources (list, optional): A list of resources associated with the client,
                along with scopes selected for each resource.

                - id (str, optional): Unique identifier for the resource.
                - name (str, optional): The name of the resource.
                - default_api (bool, optional): Whether this resource is the default API for the client.
                - selected_scopes (list, optional): A list of scopes that are selected or enabled for this resource.
                    - id (str, optional): Unique identifier for the scope.
                    - name (str, optional): Unique name for the scope.

        Returns:
            tuple: A tuple containing the newly added API Client, response, and error.

        Examples:
            Add a new API Client:

            >>> add_api_client, _, error = client.zidentity.api_client.add_api_client(
            ...     name="API_Client01",
            ...     description="API_Client01",
            ...     status=True,
            ...     access_token_life_time=86400,
            ...     client_authentication={
            ...         "auth_type": "SECRET"
            ...     },
            ...     client_resources=[
            ...         {
            ...             "id": "jhlm44rd107q7",
            ...             "name": "Zscaler APIs",
            ...             "default_api": True,
            ...             "selected_scopes": [
            ...                 {
            ...                     "id": "hhlm44raf07ps::hpopqi71j075n",
            ...                     "name": "zs:config:zia.zscalerbeta.net:8061240:config:33860:ZIA_API_Role01"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rapg7pu::hplm45bg207mu",
            ...                     "name": "zs:config:zcc.zscalerbeta.net:8061240:config:1:Super Admin"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rap07pt::hplm45bc8g7n6",
            ...                     "name": "zs:config:cloud_connector.zscalerbeta.net:8061240:config:18350:Super Admin"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rd307qf::9h6p7ebv903k4",
            ...                     "name": "zs:config:ziam:0:config:9h6p7ebv903k4:Super Admin"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rat07pv::hplm45bc707m5",
            ...                      "name": "zs:config:zdx.zscalerbeta.net:8061240:config:18347:ZDX Super Admin"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rae07ib:mplm44rqi07jb:hplm44rqvg7n5",
            ...                     "name": "zs:config:zpa.zpabeta.net:72058304855015424:config:Default:Default:28:FullAccess"
            ...                 }
            ...             ]
            ...         }
            ...     ],
            ... )
            >>> if error:
            ...     print(f"Error adding API Client: {error}")
            ...     return
            ... print(f"API Client added successfully: {added_client.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /api-clients
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, APIClientRecords)
        if error:
            return (None, response, error)

        try:
            result = APIClientRecords(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_api_client(self, client_id: str, **kwargs) -> tuple:
        """
        Updates the existing API client details based on the provided ID.
        This allows modification of attributes such as name, authentication settings, and assigned roles.

        Args:
            client_id (int): Unique identifier of the API client to be updated.

        Returns:
            tuple: A tuple containing the updated APIClient, response, and error.

        Examples:
            Update an existing api client :

            >>> update_client, _, error = client.zidentity.api_client.update_api_client(
            ...     client_id='1524566'
            ...     name="API_Client01",
            ...     description="API_Client01",
            ...     status=True",
            ...     access_token_life_time=86400,
            ...     client_authentication={
            ...         "auth_type": "SECRET"
            ...     },
            ...     client_resources=[
            ...         {
            ...             "id": "jhlm44rd107q7",
            ...             "name": "Zscaler APIs",
            ...             "default_api": True,
            ...             "selected_scopes": [
            ...                 {
            ...                     "id": "hhlm44raf07ps::hpopqi71j075n",
            ...                     "name": "zs:config:zia.zscalerbeta.net:8061240:config:33860:ZIA_API_Role01"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rapg7pu::hplm45bg207mu",
            ...                     "name": "zs:config:zcc.zscalerbeta.net:8061240:config:1:Super Admin"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rap07pt::hplm45bc8g7n6",
            ...                     "name": "zs:config:cloud_connector.zscalerbeta.net:8061240:config:18350:Super Admin"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rd307qf::9h6p7ebv903k4",
            ...                     "name": "zs:config:ziam:0:config:9h6p7ebv903k4:Super Admin"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rat07pv::hplm45bc707m5",
            ...                      "name": "zs:config:zdx.zscalerbeta.net:8061240:config:18347:ZDX Super Admin"
            ...                 },
            ...                 {
            ...                     "id": "hhlm44rae07ib:mplm44rqi07jb:hplm44rqvg7n5",
            ...                     "name": "zs:config:zpa.zpabeta.net:72058304855015424:config:Default:Default:28:Full Access"
            ...                 }
            ...             ]
            ...         }
            ...     ],
            ... )
            >>> if error:
            ...     print(f"Error adding API Client: {error}")
            ...     return
            ... print(f"API Client added successfully: {added_client.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /api-clients/{client_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, APIClientRecords)
        if error:
            return (None, response, error)

        try:
            result = APIClientRecords(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_api_client(self, client_id: str) -> tuple:
        """
        Removes an existing API client from the system.
        After deletion, the API client cannot be recovered.

        Args:
            client_id (str): Unique identifier of the API client to be deleted.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a API Client:

            >>> _, _, error = client.zidentity.api_client.delete_api_client('73459')
            >>> if error:
            ...     print(f"Error deleting API Client: {error}")
            ...     return
            ... print(f"API Client with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /api-clients/{client_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_api_client_secret(self, client_id: str) -> tuple:
        """
        Retrieves a list of secrets associated with a specific API client using its ID.

        Args:
            client_id (str): The API client ID to retrieve the client secrets.

        Returns:
            tuple: A tuple containing ApiClientSecrets instance, Response, error).

        Examples:
            Print a specific api client secret

            >>> fetched_client, _, error = client.zidentity.api_client.get_api_client_secret(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching api client secret by ID: {error}")
            ...     return
            ... print(f"Fetched api client secret by ID: {fetched_client.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /api-clients/{client_id}/secrets
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, APIClientSecrets)
        if error:
            return (None, response, error)

        try:
            result = APIClientSecrets(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_api_client_secret(self, client_id: str, **kwargs) -> tuple:
        """
       Creates and associates a new secret with a specified API client ID.
       This secret can be used for authentication with ZIdentity.

        This API is applicable only when the authentication type is SECRET.

        Args:
            client_id (str): Unique identifier of the API client to which the secret is added.

        Keyword Args:
            description (str): Additional notes or information

        Returns:
            tuple: A tuple containing the newly added API Client Secret, response, and error.

        Examples:
            Add a new API client secret:

            >>> added_client_secret, _, error = client.zidentity.api_client.add_api_client_secret(
            ...     client_id='iq3bd7e90066i',,
            ...     expires_at='1785643102',
            ... )
            >>> if error:
            ...     print(f"Error adding client secret: {error}")
            ...     return
            ... print(f"Client secret added successfully: {added_client_secret.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /api-clients/{client_id}/secrets
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, APIClientSecrets)
        if error:
            return (None, response, error)

        try:
            result = APIClientSecrets(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_api_client_secret(self, client_id: str, secret_id: str) -> tuple:
        """
        Removes an existing API client from the system.
        After deletion, the API client cannot be recovered.

        Args:
            client_id (str): Unique identifier of the API client.
            secret_id (str): Unique identifier of the secret to be deleted.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a API Client secret:

            >>> _, _, error = client.zidentity.api_client.delete_api_client_secret(
            ...     client_id='iq3bejj1g06bq',
            ...     secret_id='g000000009pk0'
            ... )
            >>> if error:
            ...     print(f"Error deleting API Client secret: {error}")
            ...     return
            ... print(f"API Client secret with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /api-clients/{client_id}/secrets/{secret_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
