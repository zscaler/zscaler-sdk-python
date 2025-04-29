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
from zscaler.zia.models.user_management import UserManagement
from zscaler.zia.models.user_management import Department
from zscaler.zia.models.user_management import Groups
from zscaler.utils import format_url


class UserManagementAPI(APIClient):
    """
    A Client object for the User Management API resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_users(self, query_params=None) -> tuple:
        """
        Returns the list of users.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.dept]`` {str}: Filters by department name. This is a `starts with` match.
                ``[query_params.group]`` {str}: Filters by group name. This is a `starts with` match.
                ``[query_params.name]`` {str}: Filters by user name. This is a `starts with` match.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                                                    The default size is 100, but the maximum size is 1000.

        Returns:
            tuple: A tuple containing (list of UserManagement instances, Response, error)

        Examples:
            List users using default settings:

            >>> users_list, response, error = zia.users.list_users():
            ... if error:
            ...     print(f"Error listing users: {error}")
            ...     return
            ... for dept in department_list:
            ...     print(dept.as_dict())

            List users, limiting to a maximum of 10 items:

            >>> users_list, response, error = zia.users.list_users(query_params={'page_size': 10}):
            ... if error:
            ...     print(f"Error listing users: {error}")
            ...     return
            ... for dept in department_list:
            ...     print(dept.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /users
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
                result.append(UserManagement(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_user(self, user_id: int) -> tuple:
        """
        Returns the user information for the specified ID or email.

        Args:
            user_id (optional, str): The unique identifier for the requested user.

        Returns:
            :obj:`Tuple`: The resource record for the requested user.

        Examples
            >>> user, _, error = client.zia.user_management.get_group(updated_group.id)
            ... if error:
            ...     print(f"Error fetching group by ID: {error}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /users/{user_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserManagement)

        if error:
            return (None, response, error)

        try:
            result = UserManagement(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_user_references(self, query_params=None) -> tuple:
        """
        Returns the list of Name-ID pairs for all users in the ZIA Admin Portal
        that can be referenced in user criteria within policies.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.include_admin_users]`` {bool}: Include the administrator users when retrieving the list.
                ``[query_params.name]`` {str}: Filters by user name. This is a `starts with` match.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                                                    The default size is 100, but the maximum size is 1000.

        Returns:
            tuple: A tuple containing (list of UserManagement instances, Response, error)

        Examples:
            List users using default settings:

            >>> user_list, zscaler_resp, err = client.zia.user_management.list_users()
            ... if err:
            ...     print(f"Error listing users: {err}")
            ...     return
            ... print(f"Total users found: {len(user_list)}")
            ... for user in user_list:
            ...     print(user.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /users/references
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
                result.append(UserManagement(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_user(self, **kwargs) -> tuple:
        """
        Creates a new ZIA user.

        Args:
            name (str):
                User name.
            email (str):
                User email consists of a user name and domain name. It does not have to be a valid email address,
                but it must be unique and its domain must belong to the organisation.
            groups (list):
                List of Groups a user belongs to.
            department (dict):
                The department the user belongs to.

        Keyword Args:
            **comments (str):
                Additional information about this user.
            **tempAuthEmail (str):
                Temporary Authentication Email. If you enabled one-time tokens or links, enter the email address to
                which the Zscaler service sends the tokens or links. If this is empty, the service will send the
                email to the User email.
            **adminUser (bool):
                True if this user is an Admin user.
            **password (str):
                User's password. Applicable only when authentication type is Hosted DB. Password strength must follow
                what is defined in the auth settings.
            **type (str):
                User type. Provided only if this user is not an end user. Accepted values are SUPERADMIN, ADMIN,
                AUDITOR, GUEST, REPORT_USER and UNAUTH_TRAFFIC_DEFAULT.

        Returns:
            :obj:`Tuple`: The resource record for the new user.

        Examples:
            Add a user with the minimum required params:

            >>> user, _, err = zia.users.add_user(name='Jane Doe',
            ...    email='jane.doe@example.com',
            ...    groups=[{
            ...      'id': '49916183'}]
            ...    department={
            ...      'id': '49814321'})

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /users
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

        response, error = self._request_executor.execute(request, UserManagement)
        if error:
            return (None, response, error)

        try:
            result = UserManagement(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_user(self, user_id: str, **kwargs) -> tuple:
        """
        Updates the details for the specified user.

        Args:
            user_id (str): The unique identifier for the user.
            **kwargs: Optional parameters to update the user details.

        Keyword Args:
            **adminUser (bool): True if this user is an Admin user.
            **comments (str): Additional information about this user.
            **department (dict, optional): The updated department object.
            **email (str, optional): The updated email.
            **groups (list of dict, optional): The updated list of groups.
            **name (str, optional): The updated name.
            **password (str): User's password (for Hosted DB authentication).
            **tempAuthEmail (str): Temporary Authentication Email.
            **type (str): User type (SUPERADMIN, ADMIN, AUDITOR, GUEST, etc.).

        Returns:
            tuple: A tuple containing the updated user object, response, and any error.

        Examples:
            Update the user name:

            >>> zia.users.update_user('99999',
            ...      name='Joe Bloggs')

            Update the email and add a comment:

            >>> zia.users.update_user('99999',
            ...      name='Joe Bloggs',
            ...      comment='External auditor.')

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /users/{user_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserManagement)

        if error:
            return (None, response, error)

        try:
            result = UserManagement(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_user(self, user_id: str) -> tuple:
        """
        Deletes the specified user ID.

        Args:
            user_id (str): The unique identifier of the user that will be deleted.

        Returns:
            :obj:`int`: The response code for the request.

        Examples:
            >>> user = zia.users.delete_user('99999')
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /users/{user_id}
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

    def bulk_delete_users(self, user_ids: list) -> tuple:
        """
        Bulk delete ZIA users.

        Args:
            user_ids (list): List containing id int of each user that will be deleted.

        Returns:
            :obj:`Tuple`: Object containing list of users that were deleted.

        Examples:
            >>> bulk_delete_users = zia.users.bulk_delete_users(['99999', '88888', '77777'])

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /users/bulkDelete
        """
        )

        payload = {"ids": user_ids}

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        return (response.get_body(), response, None)

    def list_departments(self, query_params=None) -> tuple:
        """
        Returns the list of departments.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.limit_search]`` {bool}: Limits the search to match against the department name only.
                ``[query_params.search]`` {str}: Search string used to match against an admin/auditor user's Login ID or Name.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                                                    The default size is 100, but the maximum size is 1000.

                ``[query_params.sort_by]`` {str}: Sorts the departments based on available values.

                    Supported Values: `id`, `name`, `expiry`, `status`, `external_id`, `rank`

                ``[query_params.sort_order]`` {str}: Sorts the order of departments based on available values

                    Supported Values: `asc`, `desc`, `rule_execution`

        Returns:
            tuple: A tuple containing (list of AdminUser instances, Response, error)

        Examples:
            List of departments:

            >>> fetched_department, response, error = client.zia.user_management.get_department()
            ... if error:
            ...     print(f"Error fetching department by ID: {error}")
            ...     return
            ... print(f"Fetched department by ID: {fetched_department.as_dict()}")

            Search specific department by name:

            >>> fetched_department, response, error = client.zia.user_management.get_department(
                query_params={'search': 'Finance'})
            ... if error:
            ...     print(f"Error fetching department by ID: {error}")
            ...     return
            ... print(f"Fetched department by ID: {fetched_department.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /departments
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserManagement)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(UserManagement(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_department(self, department_id: str) -> tuple:
        """
        Returns information on the specified department id.

        Args:
            department_id (str): The unique identifier for the department.

        Returns:
            tuple: A tuple containing (UserManagement instance, Response, error)

        Examples:
            >>> department = zia.users.get_department('99999')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /departments/{department_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Department)

        if error:
            return (None, response, error)

        try:
            result = Department(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_department_lite(self, department_id: str) -> tuple:
        """
        Returns information on the specified department id.

        Args:
            department_id (str): The unique identifier for the department.

        Returns:
            tuple: A tuple containing (Department instance, Response, error)

        Examples:
            >>> department = zia.users.get_department('99999')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /departments/lite/{department_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Department)

        if error:
            return (None, response, error)

        try:
            result = Department(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_department(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Department.

        Args:
            label (dict or object):
                The label data to be sent in the request.

        Returns:
            tuple: A tuple containing the newly added Department, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /departments
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

        response, error = self._request_executor.execute(request, Department)
        if error:
            return (None, response, error)

        try:
            result = Department(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_department(self, department_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Department.

        Args:
            department_id (int): The unique ID for the RuDepartment.

        Returns:
            tuple: A tuple containing the updated Department, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /departments/{department_id}
        """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Department)
        if error:
            return (None, response, error)

        try:
            result = Department(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_department(self, deparment_id: int) -> tuple:
        """
        Deletes the specified Department.

        Args:
            deparment_id (str): The unique identifier of the Department.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Example:
            Delete department:

            >>> _, _, error = client.zia.user_management.delete_department('554458')
            ... if error:
            ...     print(f"Error deleting department: {error}")
            ...     return
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /departments/{deparment_id}
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

    def list_groups(self, query_params=None) -> tuple:
        """
        Returns the list of user groups.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string used to match against an admin/auditor user's Login ID or Name
                ``[query_params.defined_by]`` {str}: The string value defined by the group name or other applicable attributes
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                                                    The default size is 100, but the maximum size is 1000.

                ``[query_params.sort_by]`` {str}: Sorts the departments based on available values.

                    Supported Values: `id`, `name`, `expiry`, `status`, `external_id`, `rank`, `mod_time`

                ``[query_params.sort_order]`` {str}: Sorts the order of departments based on available values

                    Supported Values: `asc`, `desc`, `rule_execution`

        Returns:
            tuple: A tuple containing (list of Groups instances, Response, error)

        Examples:
            List groups using default settings:

            >>> group_list, response, error = client.zia.user_management.list_groups(
                query_params={'page_size': 2000})
            ... if error:
            ...     print(f"Error listing groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /groups
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request, Groups)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(Groups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_group(self, group_id: str) -> tuple:
        """
        Returns the user group details for a given user group.

        Args:
            group_id (str): The unique identifier for the user group.

        Returns:
            :obj:`Tuple`: The user group resource record.

        Examples:
            >>> fetched_department, _, error = client.zia.user_management.get_group('545225')
            ... if error:
            ...     print(f"Error fetching department by ID: {error}")
            ...     return
            ... print(f"Fetched department by ID: {fetched_department.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /groups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Groups)

        if error:
            return (None, response, error)

        try:
            result = Groups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_group_lite(self, query_params=None) -> tuple:
        """
        Returns the user group ID and Name.

        Args:
            query_params (dict, optional): Map of query parameters for the request.

                - ``limit_search`` (bool, optional): Limits the search to match against the department name only
                - ``search`` (str, optional): Search string used to match against an admin/auditor user's Login ID or Name
                - ``page`` (int, optional): Specifies the page offset.
                - ``page_size`` (int, optional): Specifies the page size.
                                                The default size is 100, but the maximum size is 1000.
                - ``sort_by`` (str, optional): Sorts the departments based on available values.

                    Supported Values: ``id``, ``name``, ``expiry``, ``status``, ``external_id``, ``rank``

                - ``sort_order`` (str, optional): Sorts the order of departments based on available values.

                    Supported Values: ``asc``, ``desc``, ``rule_execution``

        Returns:
            tuple: The user group resource record.

        Examples:
            >>> user_group = zia.users.get_group('99999')
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /groups/lite
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Groups)

        if error:
            return (None, response, error)

        try:
            result = Groups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_group(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Group.

        Args:
            label (dict or object):
                The label data to be sent in the request.

        Returns:
            tuple: A tuple containing the newly added Group, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
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

        response, error = self._request_executor.execute(request, Groups)
        if error:
            return (None, response, error)

        try:
            result = Groups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Group.

        Args:
            group_id (int): The unique ID for the Group.

        Returns:
            tuple: A tuple containing the updated Group, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /groups/{group_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Groups)
        if error:
            return (None, response, error)

        try:
            result = Groups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: int) -> tuple:
        """
        Deletes the specified Group.

        Args:
            group_id (str): The unique identifier of the Group.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
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

    def list_auditors(self, query_params=None) -> tuple:
        """
        Returns the list of auditor users.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.dept]`` {str}: Filters by department name. This is a `starts with` match.
                ``[query_params.group]`` {str}: Filters by group name. This is a `starts with` match.
                ``[query_params.name]`` {str}: Filters by user name. This is a `starts with` match.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                                                    The default size is 100, but the maximum size is 1000.

        Returns:
            tuple: A tuple containing (list of UserManagement instances, Response, error)

        Example:
            List all auditor users:

            >>> user_list, response, error = zia.user_management.list_rules(
            ...    query_params={'page': 1, "page_size": 10}
            ... )
            >>> for user in user_list:
            ...    print(user.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /users/auditors
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
                result.append(UserManagement(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
