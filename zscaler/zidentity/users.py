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
from zscaler.zidentity.models.users import Users
from zscaler.zidentity.models.users import UserRecord
from zscaler.utils import format_url


class UsersAPI(APIClient):
    """
    A Client object for the Users API resource.
    """

    _zidentity_base_endpoint = "/admin/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_users(self, query_params=None) -> tuple:
        """
        Retrieves a list of users with optional query parameters for pagination and filtering

        See the `Zidentity Users API reference <https://help.zscaler.com/zidentity/users#/users-get>`_
        for further detail on optional keyword parameter structures.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.offset]`` {str}: The starting point for pagination, with the
                number of records that can be skipped before fetching
                ``[query_params.login_name]`` {str}: Filters results by one or multiple login
                names.
                ``[query_params.limit]`` {str}: The maximum number of records to return per
                request. Minimum: 0, Maximum: 1000
                ``[query_params.login_name[like]]`` {str}: Filters results by group name using a
                case-insensitive partial match.
                ``[query_params.display_name[like]]`` {str}: Filters results by display name
                using a case-insensitive partial match.
                ``[query_params.primary_email[like]]`` {str}: Filter results by primary email
                using a case-insensitive partial match.
                ``[query_params.domain_name]`` {[str]list}: Filter results by primary email
                using a case-insensitive partial match.
                ``[query_params.idp_name]`` {[str]list}: Filters results by one or more
                identity provider names.

        Returns:
            tuple: A tuple containing (list of Users instances, Response, error)

        Examples:
            List users using default settings:

            >>> user_list, response, error = client.zidentity.users.list_users():
            ... if error:
            ...     print(f"Error listing users: {error}")
            ...     return
            ... for user in user_list.records:
            ...     print(user.as_dict())

            List users, limiting to a maximum of 10 items:

            >>> user_list, response, error = client.zidentity.users.list_users(query_params={'limit': 10}):
            ... if error:
            ...     print(f"Error listing users: {error}")
            ...     return
            ... for user in user_list.records:
            ...     print(user.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
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
            result = Users(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_user(self, user_id: str) -> tuple:
        """
        Retrieves detailed information about a specific user using the provided user ID.

        Args:
            user_id (int): Unique identifier of the user to retrieve.

        Returns:
            tuple: A tuple containing Users instance, Response, error).

        Examples:
            Print a specific User

            >>> fetched_user, _, error = client.zidentity.users.get_user(
                'ihlmch6ikg7m1')
            >>> if error:
            ...     print(f"Error fetching User by ID: {error}")
            ...     return
            ... print(f"Fetched User by ID: {fetched_user.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /users/{user_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserRecord)
        if error:
            return (None, response, error)

        try:
            result = UserRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_user(self, **kwargs) -> tuple:
        """
        Creates a new Zidentity User.

        Args:
            **kwargs: Keyword arguments for the user attributes.

        Keyword Args:
            login_name (str): Unique login name of the user.
            display_name (str): Display name of the user.
            first_name (str, optional): First name of the user.
            last_name (str, optional): Last name of the user.
            primary_email (str): Primary email address of the user.
            secondary_email (str, optional): Secondary email address of the user.
            department (dict, optional): The department to which the user is associated.
            status (bool): Indicates whether the user is active (True) or disabled (False).

            custom_attrs_info (dict, optional): User-defined set of custom attributes represented
                as key-value pairs used to store additional information.

            id (str): Unique identifier ID of the user.
            source (str): The source type where the user was created. Possible values: "UI", "API", "SCIM", "JIT".
            idp (dict): Identity provider information containing id, name, and displayName.

        Returns:
            tuple: A tuple containing the newly added User, response, and error.

        Examples:
            Add a new user:

            >>> added_user, _, error = client.zidentity.users.add_user(
            ...     login_name="john.doe@example.com",
            ...     display_name="John Doe",
            ...     first_name="John",
            ...     last_name="Doe",
            ...     primary_email="john.doe@example.com",
            ...     status=True,
            ...     id="user123",
            ...     source="API",
            ...     idp={"id": "idp123"}
            ... )
            >>> if error:
            ...     print(f"Error adding user: {error}")
            ...     return
            ... print(f"User added successfully: {added_user.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
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

        response, error = self._request_executor.execute(request, UserRecord)
        if error:
            return (None, response, error)

        try:
            result = UserRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_user(self, user_id: str, **kwargs) -> tuple:
        """
        Updates information for the specified Zidentity User.

        Args:
            user_id (int): The unique ID for the User.

        Returns:
            tuple: A tuple containing the updated User, response, and error.

        Examples:
            Update an existing User :

            >>> update_user, _, error = client.zidentity.users.update_user(
            ...     user_id='1524566'
            ...     login_name="john.doe@example.com",
            ...     display_name="John Doe",
            ...     first_name="John",
            ...     last_name="Doe",
            ...     primary_email="john.doe@example.com",
            ...     status=True,
            ...     id="user123",
            ...     source="API",
            ...     idp={"id": "idp123"}
            ... )
            >>> if error:
            ...     print(f"Error adding user: {error}")
            ...     return
            ... print(f"User added successfully: {added_user.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /users/{user_id}
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

        response, error = self._request_executor.execute(request, UserRecord)
        if error:
            return (None, response, error)

        try:
            result = UserRecord(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_user(self, user_id: str) -> tuple:
        """
        Deletes the specified User.

        Args:
            user_id (str): The unique identifier of the User.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a User:

            >>> _, _, error = client.zidentity.users.delete_user(user_id='73459')
            >>> if error:
            ...     print(f"Error deleting User: {error}")
            ...     return
            ... print(f"User with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
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

    def list_user_group_details(self, user_id: str, query_params=None) -> tuple:
        """
        Retrieves a paginated list of groups associated with a specific user ID.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.offset]`` {str}: The starting point for pagination, with the
                number of records that can be skipped before fetching
                ``[query_params.limit]`` {str}: The maximum number of records to return per
                request. Minimum: 0, Maximum: 1000

        Returns:
            tuple: A tuple containing (list of Users instances, Response, error)

        Examples:
            List users using default settings:

            >>> groups_user_list, response, error = zia.users.list_user_group_details():
            ... if error:
            ...     print(f"Error listing users: {error}")
            ...     return
            ... for user in groups_user_list:
            ...     print(user.as_dict())

            >>> groups_user_list, response, error = zia.users.list_user_group_details(
            ... query_params={"limit": '10'}
            )
            ... if error:
            ...     print(f"Error listing users: {error}")
            ...     return
            ... for user in groups_user_list:
            ...     print(user.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /users/{user_id}/groups
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
                result.append(UserRecord(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
