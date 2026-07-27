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
from zscaler.zia.models.endpoint_dlp_resource_groups import EndpointDlpResourceGroups


class EndpointDLPResourceGroupsAPI(APIClient):
    """
    A Client object for the Endpoint DLP Resource Groups resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def add_group(self, **kwargs) -> APIResult[EndpointDlpResourceGroups]:
        """
        Creates a new endpoint DLP resource group.

        Args:
            name (str): The name of the endpoint DLP resource group.
            **kwargs: Optional keyword args.

        Keyword Args:
            channel (str): The channel for this endpoint DLP resource group. Accepted values include e.g. ``NETWORK_DRIVE_TRANSFER``.
            description (str): Additional information about the endpoint DLP resource group.
            resource_count (int): The resource count for this endpoint DLP resource group.
            resources (list): The IDs for the resources that this endpoint DLP resource group applies to.

        Returns:
            tuple: A tuple containing the newly added EndpointDlpResourceGroups instance, response, and error.

        Examples:
            Add a new endpoint DLP resource group:

            >>> added_group, _, error = client.zia.endpoint_dlp_resource_groups.add_group(
            ...     name=f"NewGroup_{random.randint(1000, 10000)}",
            ...     description=f"NewGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding endpoint DLP resource group: {error}")
            ...     return
            ... print(f"Endpoint dlp resource group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpResourceGroups
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndpointDlpResourceGroups)
        if error:
            return (None, response, error)

        try:
            result = EndpointDlpResourceGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_id: int, **kwargs) -> APIResult[EndpointDlpResourceGroups]:
        """
        Updates information for the specified endpoint DLP resource group.

        Args:
            group_id (int): The unique identifier for the endpoint DLP resource group.

        Keyword Args:
            name (str): The name of the endpoint DLP resource group.
            channel (str): The channel for this endpoint DLP resource group. Accepted values include e.g. ``NETWORK_DRIVE_TRANSFER``.
            description (str): Additional information about the endpoint DLP resource group.
            resource_count (int): The resource count for this endpoint DLP resource group.
            resources (list): The IDs for the resources that this endpoint DLP resource group applies to.

        Returns:
            tuple: A tuple containing the updated EndpointDlpResourceGroups instance, response, and error.

        Examples:
            Update an existing endpoint DLP resource group:

            >>> updated_group, _, error = client.zia.endpoint_dlp_resource_groups.update_group(
            ...     group_id=1013,
            ...     name=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating endpoint DLP resource group: {error}")
            ...     return
            ... print(f"Endpoint dlp resource group updated successfully: {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpResourceGroups/{group_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndpointDlpResourceGroups)
        if error:
            return (None, response, error)

        try:
            result = EndpointDlpResourceGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: int) -> APIResult[None]:
        """
        Deletes the specified endpoint DLP resource group.

        Args:
            group_id (int): The unique identifier for the endpoint DLP resource group.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a endpoint DLP resource group:

            >>> _, _, error = client.zia.endpoint_dlp_resource_groups.delete_group(1013)
            >>> if error:
            ...     print(f"Error deleting endpoint DLP resource group: {error}")
            ...     return
            ... print(f"Endpoint dlp resource group deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpResourceGroups/{group_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_resource_group_tags(self, dlp_resource_id: int, query_params: Optional[dict] = None) -> APIResult[list]:
        """
        Retrieves the resource group tags associated with the specified DLP endpoint resource.

        Args:
            dlp_resource_id (int): The unique identifier for the DLP endpoint resource.
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of endpoint DLP resource groups, Response, error)

        Examples:
            List endpoint DLP resource groups:

            >>> group_list, _, error = client.zia.endpoint_dlp_resource_groups.get_resource_group_tags(1013)
            >>> if error:
            ...     print(f"Error listing endpoint DLP resource groups: {error}")
            ...     return
            ... print(f"Total endpoint DLP resource groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dlpEndpointResource/{dlp_resource_id}/groups
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
            result = response.get_results()
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_resource_group_tags(
        self, channel: str, query_params: Optional[dict] = None
    ) -> APIResult[List[EndpointDlpResourceGroups]]:
        """
        Lists the DLP resource tag groups configured for the specified channel.

        Args:
            channel (str): The DLP endpoint resource channel (e.g. ``PRINTING``).
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.name]`` {str}: Search string used to filter the list by DLP resource name or other fields.
                ``[query_params.sort_order]`` {str}: Sorting order for the list by ascending or descending order of the DLP resource tag names.
                ``[query_params.search_resources]`` {bool}: Must be set to true to include search strings via the name parameter.

        Returns:
            tuple: A tuple containing (list of EndpointDlpResourceGroups instances, Response, error)

        Examples:
            List endpoint DLP resource groups:

            >>> group_list, _, error = client.zia.endpoint_dlp_resource_groups.list_resource_group_tags('PRINTING')
            >>> if error:
            ...     print(f"Error listing endpoint DLP resource groups: {error}")
            ...     return
            ... print(f"Total endpoint DLP resource groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            List endpoint DLP resource groups using filters:

            >>> group_list, _, error = client.zia.endpoint_dlp_resource_groups.list_resource_group_tags(
            ...     'PRINTING', query_params={'name': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing endpoint DLP resource groups: {error}")
            ...     return
            ... print(f"Total endpoint DLP resource groups found: {len(group_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpResourceGroups/{channel}
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
                result.append(EndpointDlpResourceGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_dlp_resources_by_tag(
        self, group_id: int, query_params: Optional[dict] = None
    ) -> APIResult[List[DlpEndpointResource]]:
        """
        Lists the DLP resources associated with the specified tag group.

        Args:
            group_id (int): The unique identifier for the tag group.
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of DlpEndpointResource instances, Response, error)

        Examples:
            List endpoint DLP resource groups:

            >>> group_list, _, error = client.zia.endpoint_dlp_resource_groups.get_dlp_resources_by_tag(1013)
            >>> if error:
            ...     print(f"Error listing endpoint DLP resource groups: {error}")
            ...     return
            ... print(f"Total endpoint DLP resource groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpResourceGroups/{group_id}/resources
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

    def update_dlp_resources_by_tag(self, group_id: int, **kwargs) -> APIResult[dict]:
        """
        Associates DLP resources with, or removes them from, the specified tag group. Pass ``resources_to_be_added`` and/or ``resources_to_be_deleted`` lists of DLP resource IDs.

        Args:
            group_id (int): The unique identifier for the endpoint DLP resource group.

        Returns:
            tuple: A tuple containing (result, Response, error).

        Examples:
            >>> result, _, error = client.zia.endpoint_dlp_resource_groups.update_dlp_resources_by_tag(
            ...     1013,
            ... )
            >>> if error:
            ...     print(f"Error calling update_dlp_resources_by_tag: {error}")
            ...     return
            ... print(f"Result: {result}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpResourceGroups/{group_id}/resources
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
