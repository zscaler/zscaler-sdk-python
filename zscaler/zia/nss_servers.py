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
from zscaler.zia.models.nss_servers import Nssservers
from zscaler.utils import format_url


class NssServersAPI(APIClient):
    """
    A Client object for the nss servers resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_nss_servers(self, query_params=None) -> tuple:
        """
        Lists NSS servers in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.type]`` {str}: Filtering results by type.
                The most common key is "type", which filters NSS servers by type.
                Supported values include:
                - NONE
                - SOFTWARE_AA_FLAG
                - NSS_FOR_WEB
                - NSS_FOR_FIREWALL
                - VZEN
                - VZEN_SME
                - VZEN_SMLB
                - PINNED_NSS
                - MD5_CAPABLE
                - ADP
                - ZIRSVR
                - NSS_FOR_ZPA

        Returns:
            tuple: A tuple containing a list of NSS server instances, the raw response, and any error.

        Examples:
            List all NSS servers:

                >>> nss_list, _, error = client.zia.nss_servers.list_nss_servers()
                >>> if error:
                ...     print(f"Error listing NSS servers: {error}")
                ... else:
                ...     print(f"Total NSS servers found: {len(nss_list)}")
                ...     for nss in nss_list:
                ...         print(nss.as_dict())

            Filter NSS servers by type:

                >>> nss_list, _, error = client.zia.nss_servers.list_nss_servers(
                ...     query_params={'type': 'NSS_FOR_FIREWALL'})
                >>> if error:
                ...     print(f"Error listing NSS servers: {error}")
                ... else:
                ...     for nss in nss_list:
                ...         print(nss.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssServers
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
            result = []
            for item in response.get_results():
                result.append(Nssservers(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_nss_server(self, nss_id: int) -> tuple:
        """
        Fetches a specific nss servers by ID.

        Args:
            nss_id (int): The unique identifier for the nss server.

        Returns:
            tuple: A tuple containing (nss server instance, Response, error).

        Examples:
            Print a specific nss server

            >>> fetched_nss_server, _, error = client.zia.nss_servers.get_nss_server(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching nss server by ID: {error}")
            ...     return
            ... print(f"Fetched nss server by ID: {fetched_nss_server.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssServers/{nss_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Nssservers)
        if error:
            return (None, response, error)

        try:
            result = Nssservers(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_nss_server(self, **kwargs) -> tuple:
        """
        Creates a new ZIA NSS server.

        Args:
            name (str): The name of the NSS server.
            **kwargs: Optional keyword arguments.

        Keyword Args:
            status (str): Enables or disables the status of the NSS server.
                Supported values: `ENABLED`, `DISABLED`, `DISABLED_BY_SERVICE_PROVIDER`,
                `NOT_PROVISIONED_IN_SERVICE_PROVIDER`, `IN_TRIAL`
            type (str): The type of the NSS server.
                Supported values: `NONE`, `SOFTWARE_AA_FLAG`, `NSS_FOR_WEB`,
                `NSS_FOR_FIREWALL`, `VZEN`, `VZEN_SME`, `VZEN_SMLB`, `PINNED_NSS`,
                `MD5_CAPABLE`, `ADP`, `ZIRSVR`, `NSS_FOR_ZPA`

        Returns:
            tuple: A tuple containing the newly added NSS server, response, and error.

        Examples:
            Add a new NSS server:

            >>> added_server, _, error = client.zia.nss_servers.add_nss_server(
            ...     name=f"NSSServer_{random.randint(1000, 10000)}",
            ...     status='ENABLED',
            ...     type='NSS_FOR_FIREWALL',
            ... )
            >>> if error:
            ...     print(f"Error adding NSS server: {error}")
            ... else:
            ...     print(f"NSS server added successfully: {added_server.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssServers
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

        response, error = self._request_executor.execute(request, Nssservers)
        if error:
            return (None, response, error)

        try:
            result = Nssservers(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_nss_server(self, nss_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA nss server.

        Args:
            nss_id (int): The unique ID for the nss server.

        Returns:
            tuple: A tuple containing the updated nss server, response, and error.

        Examples:
            Update a existing nss server :

            >>> updated_server, _, error = client.zia.nss_servers.update_nss_server(
            ... nss_id='12343',
            ... name=f"UpdateNSSServer_{random.randint(1000, 10000)}",
            ... status='ENABLED',
            ... type='NSS_FOR_FIREWALL',
            ... )
            >>> if error:
            ...     print(f"Error updating nss server: {error}")
            ...     return
            ... print(f"nss server updated successfully: {added_server.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssServers/{nss_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Nssservers)
        if error:
            return (None, response, error)

        try:
            result = Nssservers(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_nss_server(self, nss_id: int) -> tuple:
        """
        Deletes the specified nss server.

        Args:
            nss_id (str): The unique identifier of the nss server.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            List nss server:

            >>> _, _, error = client.zia.nss_servers.delete_nss_server('73459')
            >>> if error:
            ...     print(f"Error deleting nss server: {error}")
            ...     return
            ... print(f"nss server with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssServers/{nss_id}
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
