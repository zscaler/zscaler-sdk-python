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
from zscaler.ztw.models.ip_groups import IPGroups
from zscaler.utils import format_url


class IPGroupsAPI(APIClient):

    _zia_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_ip_groups(
        self,
        query_params: Optional[dict] = None,
    ) -> List[IPGroups]:
        """
            List IP Groups in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:

        Examples:
            List all IP Groups:

            >>> group_list, response, error = ztw.ip_groups.list_ip_groups():
            ... if error:
            ...     print(f"Error listing IP Groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP Groups.

            >>> group_list, response, error = ztw.ip_groups.list_ip_groups(query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing IP Groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipGroups
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
            result.append(IPGroups(self.form_response_body(item)))
        return result

    def list_ip_groups_lite(
        self,
        query_params: Optional[dict] = None,
    ) -> List[IPGroups]:
        """
        Lists IP Groups name and ID  all IP Groups.
        This endpoint retrieves only IPv4 source address groups.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: The search string used to match against
                    a group's name or description attributes.

        Returns:

        Examples:
            Gets a list of all IP Groups.

            >>> group_list, response, error = ztw.ip_groups.list_ip_groups_lite():
            ... if error:
            ...     print(f"Error listing IP Groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP Groups name and ID.

            >>> group_list, response, error = ztw.ip_groups.list_ip_groups_lite(query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing IP Groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipGroups/lite
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
            results.append(IPGroups(self.form_response_body(item)))
        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def add_ip_group(self, **kwargs) -> IPGroups:
        """
        Adds a new IP Group.

        Args:
            name (str): The name of the IP Group.
            ip_addresses (str): The list of IP addresses for the IP Group.
            description (str): Additional information for the IP Group.

        Returns:

        Examples:
            Add a new IP Group:

            >>> ztw.ip_groups.add_ip_group(name='My IP Group',
            ...    ip_addresses=['198.51.100.0/24'],
            ...    description='Contains the IP addresses for the local network.')

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipGroups
        """
        )

        body = kwargs

        request = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        # Execute the request
        response = self._request_executor.execute(request, IPGroups)
        result = IPGroups(self.form_response_body(response.get_body()))
        return result

    def delete_ip_group(self, group_id: int) -> None:
        """
        Deletes an IP Group.

        Args:
            group_id (str): The unique ID of the IP Group to be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, response, error = client.ztw.ip_groups.delete_ip_group('545845')
            ... if error:
            ...     print(f"Error deleting group: {error}")
            ... return

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipGroups/{group_id}
        """
        )

        params = {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None
