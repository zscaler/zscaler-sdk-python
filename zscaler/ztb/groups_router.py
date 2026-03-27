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

from typing import Dict, Any, Optional, List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.groups_router import GroupsRouter


class GroupsRouterAPI(APIClient):
    """
    Client for the ZTB Groups Router resource.

    Provides CRUD operations for groups router in the
    Zero Trust Branch API.
    """

    _ztb_base_endpoint = "/ztb/api/v2"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_groups(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get all groups.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.refresh_token]`` (str): Available values : enabled

                ``[query_params.site_id]`` (str):

                ``[query_params.page]`` (int):

                ``[query_params.size]`` (int):

                ``[query_params.sort]`` (str):

                ``[query_params.sortdir]`` (str):

                ``[query_params.group_type]`` (str): List of group types to filter
                    If empty would list isolation types only for backward compatibility
                    Use all to list both Isolation and Access types

                ``[query_params.filter_hidden]`` (str): Available values : true

        Returns:
            tuple: A tuple containing (list of GroupsRouter instances, Response, error).

        Examples:
            List all groups:

            >>> group_list, _, error = client.ztb.groups_router.list_groups()
            >>> if error:
            ...     print(f"Error listing groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /groups
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
                result.append(GroupsRouter(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_group(self, group_id: str) -> APIResult:
        """
        Fetches a specific group by ID.

        Args:
            group_id (int): The unique identifier for the group.

        Returns:
            tuple: A tuple containing (GroupsRouter instance, Response, error).

        Examples:
            Print a specific Group:

            >>> fetched_group, _, error = client.ztb.groups_router.get_group('73459')
            >>> if error:
            ...     print(f"Error fetching group by ID: {error}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /groups/{group_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GroupsRouter)
        if error:
            return (None, response, error)

        try:
            result = GroupsRouter(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_group(self, **kwargs) -> APIResult:
        """
        Creates a new ZTB Group.

        Args:
            name (str): The name of the group.
            **kwargs: Optional keyword args.

        Keyword Args:
            display_name (str): The display name for the group.
            type (str): The group type (e.g. ``device``).
            autonomous (bool): Whether the group is autonomous.
            owner (str): The owner of the group.
            member_attributes (dict): Member attribute filters.

        Returns:
            tuple: A tuple containing the newly created Group, response, and error.

        Examples:
            Create a new Group:

            >>> created_group, _, error = client.ztb.groups_router.create_group(
            ...     name="Group01",
            ...     display_name="Group01",
            ...     type="device",
            ...     autonomous=True,
            ...     owner="user",
            ... )
            >>> if error:
            ...     print(f"Error creating group: {error}")
            ...     return
            ... print(f"Group created successfully: {created_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /groups
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GroupsRouter)
        if error:
            return (None, response, error)

        try:
            result = GroupsRouter(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group_patch(self, group_id: int, **kwargs) -> APIResult:
        """
        Updates information for the specified ZTB Group (PATCH).

        Args:
            group_id (int): The unique ID for the Group.
            **kwargs: Group fields to patch.

        Returns:
            tuple: A tuple containing the updated Group, response, and error.

        Examples:
            Patch an existing Group:

            >>> patched_group, _, error = client.ztb.groups_router.update_group_patch(
            ...     group_id='73459',
            ...     display_name="Group01_Patched",
            ... )
            >>> if error:
            ...     print(f"Error patching group: {error}")
            ...     return
            ... print(f"Group updated successfully (PATCH): {patched_group.as_dict()}")
        """
        http_method = "patch".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /groups/{group_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GroupsRouter)
        if error:
            return (None, response, error)

        try:
            result = GroupsRouter(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group_put(self, group_id: int, **kwargs) -> APIResult:
        """
        Updates information for the specified ZTB Group (PUT).

        Args:
            group_id (int): The unique ID for the Group.
            **kwargs: Full group replacement fields.

        Returns:
            tuple: A tuple containing the updated Group, response, and error.

        Examples:
            Update an existing Group:

            >>> updated_group, _, error = client.ztb.groups_router.update_group_put(
            ...     group_id='73459',
            ...     name="Group01",
            ...     display_name="Group01",
            ...     type="device",
            ...     autonomous=True,
            ...     owner="user",
            ... )
            >>> if error:
            ...     print(f"Error updating group: {error}")
            ...     return
            ... print(f"Group updated successfully (PUT): {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /groups/{group_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GroupsRouter)
        if error:
            return (None, response, error)

        try:
            result = GroupsRouter(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: int) -> APIResult[dict]:
        """
        Deletes the specified Group.

        Args:
            group_id (int): The unique identifier of the Group.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Group:

            >>> _, _, error = client.ztb.groups_router.delete_group('73459')
            >>> if error:
            ...     print(f"Error deleting group: {error}")
            ...     return
            ... print(f"Group with ID 73459 deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /groups/{group_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
