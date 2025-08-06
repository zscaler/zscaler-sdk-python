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
from zscaler.zidentity.models.groups import Groups
from zscaler.zidentity.models.groups import GroupRecord
from zscaler.utils import format_url


class GroupsAPI(APIClient):
    """
    A Client object for the Groups API resource.
    """

    _zidentity_base_endpoint = "/admin/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_groups(self, query_params=None) -> tuple:
        """
        Retrieves a paginated list of groups with optional query parameters
        for pagination and filtering by group name or dynamic group status.

        See the `Zidentity Groups API reference <https://help.zscaler.com/zidentity/groups#/groups-get>`_
        for further detail on optional keyword parameter structures.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.offset]`` {int}: The starting point for pagination,
                    with the number of records that can be skipped before fetching results.

                ``[query_params.limit]`` {str}: The maximum number of records to return per request. Minimum: 0, Maximum: 1000
                ``[query_params.name[like]]`` {str}: Filters results by group name using a case-insensitive partial match.
                ``[query_params.exclude_dynamic_groups]`` {bool}: Excludes dynamic groups from the results.

        Returns:
            tuple: A tuple containing (list of Groups instances, Response, error)

        Examples:
            List groups using default settings:

            >>> group_list, response, error = client.zidentity.groups.list_groups():
            ... if error:
            ...     print(f"Error listing groups: {error}")
            ...     return
            ... for resource in group_list.records:
            ...     print(group.as_dict())

            List groups, limiting to a maximum of 10 items:

            >>> group_list, response, error = client.zidentity.groups.list_groups(query_params={'limit': 10}):
            ... if error:
            ...     print(f"Error listing groups: {error}")
            ...     return
            ... for resource in group_list.records:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups
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
            result = Groups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_group(self, group_id: int) -> tuple:
        """
        Fetches a specific zidentity group by ID.

        Args:
            group_id (int): Unique identifier of the group to retrieve.

        Returns:
            tuple: A tuple containing Groups instance, Response, error).

        Examples:
            Print a specific Group

            >>> fetched_group, _, error = client.zidentity.groups.get_group(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching Group by ID: {error}")
            ...     return
            ... print(f"Fetched Group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GroupRecord)
        if error:
            return (None, response, error)

        try:
            result = GroupRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_group(self, **kwargs) -> tuple:
        """
        Creates a new Zidentity Group.

        Args:
            **kwargs: Keyword arguments for the group attributes.

        Keyword Args:
            name (str): The name of the group.
            id (str): Unique identifier for the group.
            source (str): The source type of the group (e.g., 'SCIM', 'MANUAL', etc.).
            is_dynamic_group (bool): Boolean flag indicating if the group is dynamic.
            admin_entitlement_enabled (bool): Whether the group supports admin entitlements.
            service_entitlement_enabled (bool): Whether the group supports service entitlements.
            description (str, optional): A description of the group.
            idp (dict, optional): Identity provider information associated with the group.

        Returns:
            tuple: A tuple containing the newly added Group, response, and error.

        Examples:
            Add a new Group:

            >>> added_group, _, error = client.zidentity.groups.add_group(
            ...     name="My Test Group",
            ...     id="group123",
            ...     source="SCIM",
            ...     is_dynamic_group=False,
            ...     admin_entitlement_enabled=True,
            ...     service_entitlement_enabled=True,
            ...     description="A test group for demonstration"
            ... )
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups
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

        response, error = self._request_executor.execute(request, GroupRecord)
        if error:
            return (None, response, error)

        try:
            result = GroupRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_id: str, **kwargs) -> tuple:
        """
        Updates information for the specified Zidentity Group.

        Args:
            group_id (str): The unique ID for the Group.

        Returns:
            tuple: A tuple containing the updated Group, response, and error.

        Examples:
            Update an existing Group :

            >>> updated_group, _, error = client.zidentity.groups.update_group(
            ...     group_id='ihlmch6ikg7m1',
            ...     name=f"ZidentityGroupUpdate_{random.randint(1000, 10000)}",
            ...     description=f"ZidentityGroup_{random.randint(1000, 10000)}",
            ...     source='SCIM',
            ...     admin_entitlement_enabled=True,
            ...     service_entitlement_enabled=True,
            ...     dynamic_group=False
            ... )
            >>> if error:
            ...     print(f"Error updating group: {error}")
            ...     return
            ... print(f"Group updated successfully: {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups/{group_id}
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

        response, error = self._request_executor.execute(request, GroupRecord)
        if error:
            return (None, response, error)

        try:
            result = GroupRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: str) -> tuple:
        """
        Deletes the specified Group.

        Args:
            group_id (str): The unique identifier of the Group.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Group:

            >>> _, _, error = client.zidentity.groups.delete_group('73459')
            >>> if error:
            ...     print(f"Error deleting Group: {error}")
            ...     return
            ... print(f"Group with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups/{group_id}
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

    def list_group_users_details(self, group_id: str, query_params=None) -> tuple:
        """
        Retrieves the list of users details for a specific group using the group ID.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.offset]`` {str}: The starting point for pagination, with the
                number of records that can be skipped before fetching
                ``[query_params.login_name]`` {str}: Filters results by one or multiple login names.
                ``[query_params.limit]`` {str}: The maximum number of records to return per request. Minimum: 0, Maximum: 1000
                ``[query_params.login_name[like]]`` {str}: Filters results by group name using a
                case-insensitive partial match.
                ``[query_params.display_name[like]]`` {str}: Filters results by display name using a
                case-insensitive partial match.
                ``[query_params.primary_email[like]]`` {str}: Filter results by primary email using a
                case-insensitive partial match.
                ``[query_params.domain_name]`` {[str]list}: Filter results by primary email using a
                case-insensitive partial match.
                ``[query_params.idp_name]`` {[str]list}: Filters results by one or more identity
                provider names.

        Returns:
            tuple: A tuple containing (list of Groups instances, Response, error)

        Examples:
            List users using default settings:

            >>> users_list, response, error = zidentity.groups.list_group_users_details():
            ... if error:
            ...     print(f"Error listing users: {error}")
            ...     return
            ... for user in users_list.records:
            ...     print(user.as_dict())

            List users, limiting to a maximum of 10 items:
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups/{group_id}/users
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
            result = Groups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_user_to_group(
        self,
        group_id: str,
        user_id: str,
        **kwargs
    ) -> tuple:
        """
        Adds a specific user to an existing group using the group ID and the user ID.

        Args:
            group_id (str): Unique identifier of the group to which the user needs to be added.
            user_id (str): Unique identifier of the user being added to the group.

        Returns:
            :obj:`Tuple[dict, Response, Exception]`:
                A tuple containing:
                - An empty dictionary `{}` on success,
                - The raw `Response` object,
                - Or an `Exception` if an error occurred.
                - This returns the client_secret attribute

        Examples:
            Adds a specific user to an existing group:

            >>> add_user_to_group, _, error = client.zidentity.groups.add_user_to_group(
            ... group_id='ia3b1ad9hg66g',
            ... user_id='ihln05leh07e2'
            ... )
            >>> if error:
            ...     print(f"Error updating Group: {error}")
            ...     return
            ... print(f"Group updated successfully: {add_user_to_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups/{group_id}/users/{user_id}
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

        response, error = self._request_executor.execute(request, GroupRecord)
        if error:
            return (None, response, error)

        try:
            result = GroupRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_users_to_group(self, group_id: str, **kwargs) -> tuple:
        """
        Adds users to an existing group using the unique identifier ID of the group.

        Args:
            group_id (str): The unique ID for the Group.
            **kwargs: Additional parameters including user IDs.

        Keyword Args:
            id (list): List of user IDs to add to the group. Can be passed as a simple list
                      of strings/integers which will be automatically transformed to the required format.

        Returns:
            :obj:`Tuple[dict, Response, Exception]`:
                A tuple containing:
                - An empty dictionary `{}` on success,
                - The raw `Response` object,
                - Or an `Exception` if an error occurred.
                - This returns the client_secret attribute

        Examples:
            Adds users to an existing group with simple ID list:

            >>> add_users_to_group, _, error = client.zidentity.groups.add_users_to_group(
            ...     group_id='ia3b1ad9hg66g',
            ...     id=['525455', '254545', 'ihln05ktj07ds']
            ... )
            >>> if error:
            ...     print(f"Error adding users to group: {error}")
            ...     return
            ... print(f"Users added successfully: {add_users_to_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups/{group_id}/users
        """
        )

        if 'id' in kwargs and isinstance(kwargs['id'], list):
            transformed_ids = []
            for user_id in kwargs['id']:
                transformed_ids.append({"id": user_id})
            body = transformed_ids
        else:
            body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GroupRecord)
        if error:
            return (None, response, error)

        try:
            result = GroupRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def replace_users_groups(self, group_id: str, **kwargs) -> tuple:
        """
        Replaces the list of users in a specific group using the group ID.
        This operation completely replaces all existing users in the group.

        Args:
            group_id (str): The unique ID for the Group.
            **kwargs: Additional parameters including user IDs.

        Keyword Args:
            id (list): List of user IDs to be replaced in the group. Can be passed as a simple list
                      of strings/integers which will be automatically transformed to the required format.

        Returns:
            :obj:`Tuple[dict, Response, Exception]`:
                A tuple containing:
                - An empty dictionary `{}` on success,
                - The raw `Response` object,
                - Or an `Exception` if an error occurred.
                - This returns the client_secret attribute

        Examples:
            Adds users to an existing group with simple ID list:

            >>> replace_users, _, error = client.zidentity.groups.replace_users_groups(
            ...     group_id='ia3b1ad9hg66g',
            ...     id=['ihln05ttj07ds', 'ihln05tfj07ds', 'ihln05ktj07ds']
            ... )
            >>> if error:
            ...     print(f"Error replacing users in group: {error}")
            ...     return
            ... print(f"Replacement of users successfully: {replace_users.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups/{group_id}/users
        """
        )

        if 'id' in kwargs and isinstance(kwargs['id'], list):
            transformed_ids = []
            for user_id in kwargs['id']:
                transformed_ids.append({"id": user_id})
            body = transformed_ids
        else:
            body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GroupRecord)
        if error:
            return (None, response, error)

        try:
            result = GroupRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def remove_user_from_group(self, group_id: str, user_id: str) -> tuple:
        """
        Deletes the specified Group.

        Args:
            group_id (str): Unique identifier of the group to which the user needs to be added.
            user_id (str): Unique identifier of the user being added to the group.

        Returns:
            :obj:`Tuple[dict, Response, Exception]`:
                A tuple containing:
                - An empty dictionary `{}` on success,
                - The raw `Response` object,
                - Or an `Exception` if an error occurred.
                - This returns the client_secret attribute

        Examples:
            Delete a Group:

            >>> _, _, error = client.zidentity.groups.remove_user_from_group(
            ...     group_id='ia3b1ad9hg66g',
            ...     user_id='ihln05ktj07ds'
            ... )
            >>> if error:
            ...     print(f"Error removing users to group: {error}")
            ...     return
            ... print(f"User removed from group successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /groups/{group_id}/users/{user_id}
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
