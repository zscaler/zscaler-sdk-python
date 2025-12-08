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

from typing import Dict, List, Optional, Any, Union
from zscaler.request_executor import RequestExecutor
from zscaler.api_client import APIClient
from zscaler.ztw.models.ip_source_groups import IPSourceGroup
from zscaler.utils import format_url


class IPSourceGroupsAPI(APIClient):

    _zia_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_ip_source_groups(
        self,
        query_params: Optional[dict] = None,
    ) -> List[IPSourceGroup]:
        """
            List IP Source Groups in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:

        Examples:
            List all IP Source Groups:

            >>> group_list, response, error = ztw.ip_source_groups.list_ip_source_groups():
            ... if error:
            ...     print(f"Error listing IP Source Groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP Source Groups.

            >>> group_list, response, error = ztw.ip_source_groups.list_ip_source_groups(query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing IP Source Groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        # Execute the request
        response = self._request_executor.execute(request)

        result = []
        for item in response.get_results():
            result.append(IPSourceGroup(self.form_response_body(item)))
        return result

    def list_ip_source_groups_lite(
        self,
        query_params: Optional[dict] = None,
    ) -> List[IPSourceGroup]:
        """
        Lists IP Source Groups name and ID  all IP Source Groups.
        This endpoint retrieves only IPv4 source address groups.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: The search string used to match against
                    a group's name or description attributes.

        Returns:

        Examples:
            Gets a list of all IP source groups.

            >>> group_list, response, error = ztw.ip_source_groups.list_ip_source_groups_lite():
            ... if error:
            ...     print(f"Error listing IP source groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP source groups name and ID.

            >>> group_list, response, error = (
            ...     ztw.ip_source_groups.list_ip_source_groups_lite(
            ...         query_params={"search": 'Group01'}
            ...     )
            ... ):
            ... if error:
            ...     print(f"Error listing IP source groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/lite
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        response = self._request_executor.execute(request)
        results = []
        for item in response.get_results():
            results.append(IPSourceGroup(self.form_response_body(item)))
        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def add_ip_source_group(self, **kwargs) -> IPSourceGroup:
        """
        Adds a new IP Source Group.

        Args:
            name (str): The name of the IP Source Group.
            ip_addresses (str): The list of IP addresses for the IP Source Group.
            description (str): Additional information for the IP Source Group.

        Returns:

        Examples:
            Add a new IP Source Group:

            >>> ztw.ip_source_groups.add_ip_source_group(name='My IP Source Group',
            ...    ip_addresses=['198.51.100.0/24', '192.0.2.1'],
            ...    description='Contains the IP addresses for the local network.')

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups
        """
        )

        body = kwargs

        request = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        # Execute the request
        response = self._request_executor.execute(request, IPSourceGroup)
        result = IPSourceGroup(self.form_response_body(response.get_body()))
        return result

    def delete_ip_source_group(self, group_id: int) -> None:
        """
        Deletes an IP Source Group.

        Args:
            group_id (str): The unique ID of the IP Source Group to be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, response, error = client.ztw.ip_source_groups.delete_ip_source_group(updated_group.id)
            ... if error:
            ...     print(f"Error deleting group: {error}")
            ... return

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/{group_id}
        """
        )

        params = {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None
