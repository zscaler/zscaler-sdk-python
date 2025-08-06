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
from zscaler.zidentity.models.resource_servers import ResourceServers
from zscaler.zidentity.models.resource_servers import ResourceServersRecord
from zscaler.utils import format_url


class ResourceServersAPI(APIClient):
    """
    A Client object for the Resource Servers API resource.
    """

    _zidentity_base_endpoint = "/admin/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_resource_servers(self, query_params=None) -> tuple:
        """
        Retrieves a paginated list of resource servers with an optional query parameters
        for pagination

        See the `Zidentity Resource Servers API reference
        <https://help.zscaler.com/zidentity/resource-servers#/resource-servers-get>`_
        for further detail on optional keyword parameter structures.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.offset]`` {int}: The starting point for pagination,
                    with the number of records that can be skipped before fetching results.

                ``[query_params.limit]`` {str}: The maximum number of records to return per request.
                Minimum: 0, Maximum: 1000
                ``[query_params.name[like]]`` {str}: Filters results by group name using a
                case-insensitive partial match.

        Returns:
            tuple: A tuple containing (list of ResourceServers instances, Response, error)

        Examples:
            List resource servers using default settings:

            >>> resource_list, response, error = zidentity.resource_servers.list_resource_servers():
            ... if error:
            ...     print(f"Error listing resource servers: {error}")
            ...     return
            ... for resource in resource_list.records:
            ...     print(resource.as_dict())

            List resource servers, limiting to a maximum of 10 items:

            >>> resource_list, response, error = zidentity.resource_servers.list_resource_servers(query_params={'limit': 10}):
            ... if error:
            ...     print(f"Error listing resource servers: {error}")
            ...     return
            ... for resource in resource_list.records:
            ...     print(resource.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /resource-servers
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
            result = ResourceServers(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_resource_server(self, resource_id: str) -> tuple:
        """
        Retrieves details about a specific resource server using the server ID.

        Args:
            resource_id (int): Unique identifier of the resource server to retrieve.

        Returns:
            tuple: A tuple containing ResourceServersRecord instance, Response, error).

        Examples:
            Print a specific Resource Servers

            >>> fetched_resource, _, error = client.zidentity.resource_servers.get_resource_server(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching Resource Server by ID: {error}")
            ...     return
            ... print(f"Fetched Resource Server by ID: {fetched_resource.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /resource-servers/{resource_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ResourceServersRecord)
        if error:
            return (None, response, error)

        try:
            result = ResourceServersRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
