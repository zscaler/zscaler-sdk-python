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
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.dlp_endpoint_resource import DlpEndpointResource


class DLPEndpointResourceAPI(APIClient):
    """
    A Client object for the DLP Endpoint Resources resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def add_resource(self, **kwargs) -> APIResult[DlpEndpointResource]:
        """
        Creates a new DLP endpoint resource.

        Args:
            name (str): The name of the DLP endpoint resource.
            **kwargs: Optional keyword args.

        Keyword Args:
            channel (str): The channel for this DLP endpoint resource. Accepted values include e.g. ``NETWORK_DRIVE_TRANSFER``.
            is_predefined (bool): A Boolean value indicating whether is predefined applies to this DLP endpoint resource.
            network_drive_type (str): The network drive type for this DLP endpoint resource. Accepted values include e.g. ``ALL_DIRECTORIES``.
            description (str): Additional information about the DLP endpoint resource.
            server_name (str): The server name for this DLP endpoint resource.
            app_id (int): The app id for this DLP endpoint resource.
            network_drives (list): The list of network drives for this DLP endpoint resource.
            printer (dict): The printer configuration for this DLP endpoint resource.
            removable_storage (dict): The removable storage configuration for this DLP endpoint resource.
            application (dict): The application configuration for this DLP endpoint resource.

        Returns:
            tuple: A tuple containing the newly added DlpEndpointResource instance, response, and error.

        Examples:
            Add a new DLP endpoint resource:

            >>> added_resource, _, error = client.zia.dlp_endpoint_resource.add_resource(
            ...     name=f"NewResource_{random.randint(1000, 10000)}",
            ...     description=f"NewResource_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding DLP endpoint resource: {error}")
            ...     return
            ... print(f"Dlp endpoint resource added successfully: {added_resource.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dlpEndpointResource
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DlpEndpointResource)
        if error:
            return (None, response, error)

        try:
            result = DlpEndpointResource(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_resource(self, resource_id: int, **kwargs) -> APIResult[DlpEndpointResource]:
        """
        Updates information for the specified DLP endpoint resource.

        Args:
            resource_id (int): The unique identifier for the DLP endpoint resource.

        Keyword Args:
            name (str): The name of the DLP endpoint resource.
            channel (str): The channel for this DLP endpoint resource. Accepted values include e.g. ``NETWORK_DRIVE_TRANSFER``.
            is_predefined (bool): A Boolean value indicating whether is predefined applies to this DLP endpoint resource.
            network_drive_type (str): The network drive type for this DLP endpoint resource. Accepted values include e.g. ``ALL_DIRECTORIES``.
            description (str): Additional information about the DLP endpoint resource.
            server_name (str): The server name for this DLP endpoint resource.
            app_id (int): The app id for this DLP endpoint resource.
            network_drives (list): The list of network drives for this DLP endpoint resource.
            printer (dict): The printer configuration for this DLP endpoint resource.
            removable_storage (dict): The removable storage configuration for this DLP endpoint resource.
            application (dict): The application configuration for this DLP endpoint resource.

        Returns:
            tuple: A tuple containing the updated DlpEndpointResource instance, response, and error.

        Examples:
            Update an existing DLP endpoint resource:

            >>> updated_resource, _, error = client.zia.dlp_endpoint_resource.update_resource(
            ...     resource_id=1013,
            ...     name=f"UpdatedResource_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedResource_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating DLP endpoint resource: {error}")
            ...     return
            ... print(f"Dlp endpoint resource updated successfully: {updated_resource.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dlpEndpointResource/{resource_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DlpEndpointResource)
        if error:
            return (None, response, error)

        try:
            result = DlpEndpointResource(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_resource(self, resource_id: int) -> APIResult[None]:
        """
        Deletes the specified DLP endpoint resource.

        Args:
            resource_id (int): The unique identifier for the DLP endpoint resource.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a DLP endpoint resource:

            >>> _, _, error = client.zia.dlp_endpoint_resource.delete_resource(1013)
            >>> if error:
            ...     print(f"Error deleting DLP endpoint resource: {error}")
            ...     return
            ... print(f"Dlp endpoint resource deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dlpEndpointResource/{resource_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def list_resources_by_channel(
        self, channel: str, query_params: Optional[dict] = None
    ) -> APIResult[List[DlpEndpointResource]]:
        """
        Lists the DLP resources configured for the specified channel. Supported channels are PRINTING, REMOVABLE_DRIVE_TRANSFER, NETWORK_DRIVE_TRANSFER, and PERSONAL_CLOUD_STORAGE.

        Args:
            channel (str): The DLP endpoint resource channel (e.g. ``PRINTING``).
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.sort_order]`` {str}: Sorting order for the list by ascending or descending order of the DLP resource names.
                ``[query_params.name]`` {str}: Search string used to filter the list by DLP resource name and other fields.

        Returns:
            tuple: A tuple containing (list of DlpEndpointResource instances, Response, error)

        Examples:
            List DLP endpoint resources:

            >>> resource_list, _, error = client.zia.dlp_endpoint_resource.list_resources_by_channel('PRINTING')
            >>> if error:
            ...     print(f"Error listing DLP endpoint resources: {error}")
            ...     return
            ... print(f"Total DLP endpoint resources found: {len(resource_list)}")
            ... for resource in resource_list:
            ...     print(resource.as_dict())

            List DLP endpoint resources using filters:

            >>> resource_list, _, error = client.zia.dlp_endpoint_resource.list_resources_by_channel(
            ...     'PRINTING', query_params={'sort_order': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing DLP endpoint resources: {error}")
            ...     return
            ... print(f"Total DLP endpoint resources found: {len(resource_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dlpEndpointResource/{channel}
        """)

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
                result.append(DlpEndpointResource(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_resource_by_channel(self, channel: str, resource_id: int) -> APIResult[DlpEndpointResource]:
        """
        Fetches a single DLP resource with the specified ID for the given channel.

        Args:
            channel (str): The DLP endpoint resource channel (e.g. ``PRINTING``).
            resource_id (int): The unique identifier for the DLP endpoint resource.

        Returns:
            tuple: A tuple containing (DlpEndpointResource instance, Response, error).

        Examples:
            Print a specific DLP endpoint resource:

            >>> fetched_resource, _, error = client.zia.dlp_endpoint_resource.get_resource_by_channel('PRINTING', 1013)
            >>> if error:
            ...     print(f"Error fetching DLP endpoint resource by ID: {error}")
            ...     return
            ... print(f"Fetched DLP endpoint resource by ID: {fetched_resource.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dlpEndpointResource/{channel}/{resource_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DlpEndpointResource)
        if error:
            return (None, response, error)

        try:
            result = DlpEndpointResource(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
