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
from zscaler.zia.models.admin_users import AdminUser
from zscaler.zia.models.user_management import UserManagement
from zscaler.utils import format_url, transform_common_id_fields, reformat_params


class AdminUsersAPI(APIClient):
    """
    A Client object for the Admin and Role resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_admin_users(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns a list of admin users.

        `Note:` For tenants migrated to Zidentity this endpoint will return an empty list.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.include_auditor_users]`` {bool}: Include or exclude auditor user information in the list.

                ``[query_params.include_admin_users]`` {bool}: Include or exclude admin user information in the list.

                ``[query_params.search]`` {str}: Search string to partially match an admin/auditor user's Login ID or Name.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 100, but the maximum size is 1000.

        Returns:
            tuple: A tuple containing (list of AdminUser instances, Response, error)

        Examples:

        List All Admin users
            >>> list_users, _, error = client.zia.admin_users.list_admin_users()
            >>>     if error:
            ...         print(f"Error listing admin users: {error}")
            ...         return
            ...     print(f"Total admin users found: {len(list_users)}")
            ...     for users in list_users:
            ...         print(users.as_dict())

        List All Admin users Including auditor users
            >>> list_users, _, error = client.zia.admin_users.list_admin_users(
                query_params={'include_auditor_users': True}
            )
            >>>     if error:
            ...         print(f"Error listing admin users: {error}")
            ...         return
            ...     print(f"Total admin users found: {len(list_users)}")
            ...     for users in list_users:
            ...         print(users.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/adminUsers")
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
                result.append(AdminUser(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_admin_user(self, user_id: str) -> tuple:
        """
        Returns information on the specified admin user id.

        Args:
            user_id (str): The unique id of the admin user.
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (AdminUser instance, Response, error)

        Examples:
            >>> fetched_user, _, error = client.zia.admin_users.get_admin_user(143783113)
            >>> if error:
            ...     print(f"Error fetching admin user by ID: {error}")
            ...     return
            ... print(f"Fetched Admin user by ID: {fetched_user.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/adminUsers/{user_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdminUser)

        if error:
            return (None, response, error)

        try:
            result = AdminUser(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_admin_user(
        self,
        name: str,
        login_name: str,
        email: str,
        password: str,
        **kwargs
    ) -> tuple:
        """
        Adds a new admin user to ZIA.

        Args:
            name (str): The user's full name.
            login_name (str):
                The name that the admin user will use to login to ZIA in email format, i.e. `user@domain.tld.`
            email (str): The email address for the admin user.
            password (str): The password for the admin user.
            associate_with_existing_admin (bool): This field is set to true to update an admin user that already exists.

        Keyword Args:
            admin_scope_type (str): The scope of the admin's permissions, accepted values are:
                ``ORGANIZATION``, ``DEPARTMENT``, ``LOCATION``, ``LOCATION_GROUP``
            comments (str): Additional information about the admin user.
            disabled (bool): Set to ``True`` if you want the account disabled upon creation.
            is_password_login_allowed (bool): Set to ``True`` to allow password login.
            is_security_report_comm_enabled (bool):
                Set to ``True`` to allow ZIA Security Update emails to be sent to the admin user.
            is_service_update_comm_enabled (bool):
                Set to ``True`` to allow ZIA Service Update emails to be sent to the admin user.
            is_product_update_comm_enabled (bool):
                Set to ``True`` to allow ZIA Product Update emails to be sent to the admin user.
            is_password_expired (bool):
                Set to ``True`` to expire the admin user's password upon creation.
            is_exec_mobile_app_enabled (bool):
                Set to ``True`` to enable to executive insights mobile application for the admin user.
            role_id (int): The unique id for the admin role being assigned to the admin user.
            scope_entity_ids (list):
                A list of entity ids for the admin user's scope. e.g. if the admin user has admin_scope set to
                ``department`` then you will need to provide a list of department ids.
                **NOTE**: This param doesn't need to
                be provided if the admin user's scope is set to ``ORGANIZATION``.

        Returns:
            :obj:`Tuple`: The newly created admin user resource record.

        Examples:

            Add an admin user with the minimum required params:
                >>> add_admin_user, _, error = client.zia.admin_users.add_admin_user(
                ...    name="Jim Bob",
                ...    login_name="jim@example.com",
                ...    password="*********",
                ...    email="jim@example.com")
                ...     )
                >>>     if error:
                ...         print(f"Error adding admin user: {error}")
                ...         return
                ...     print(f"Admin User added successfully: {add_admin_user.as_dict()}")

            Add an admin user with a department admin scope type:
                >>> add_admin_user, _, error = client.zia.admin_users.add_admin_user(
                ...    name="Jane Bob",
                ...    login_name="jane@example.com",
                ...    password="*********",
                ...    email="jane@example.com,
                ...    role_id=84546,
                ...    admin_scope_type="DEPARTMENT",
                ...    scope_entity_ids = ['376542', '245688']
                ...     )
                >>>     if error:
                ...         print(f"Error adding admin user: {error}")
                ...         return
                ...     print(f"Admin User added successfully: {add_admin_user.as_dict()}")

            Add an auditor user:
                >>> add_admin_user = zia.admin_users.add_admin_user(
                ...    name="Head Bob",
                ...    login_name="head@example.com",
                ...    password="*********",
                ...    email="head@example.com,
                ...    is_auditor=True,
                ...     )
                >>>     if error:
                ...         print(f"Error adding admin user: {error}")
                ...         return
                ...     print(f"Admin User added successfully: {add_admin_user.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminUsers
        """
        )

        payload = {
            "userName": name,
            "loginName": login_name,
            "email": email,
            "password": password,
        }

        body = {**payload, **kwargs}

        if "role_id" in body:
            body["role"] = {"id": body.pop("role_id")}

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdminUser)

        if error:
            return (None, response, error)

        try:
            result = AdminUser(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_admin_user(self, user_id: str, **kwargs) -> tuple:
        """
        Update an admin user.

        Args:
            user_id (str): The unique id of the admin user to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            admin_scope_type (str): The scope of the admin's permissions, accepted values are:
                ``ORGANIZATION``, ``DEPARTMENT``, ``LOCATION``, ``LOCATION_GROUP``
            comments (str): Additional information about the admin user.
            disabled (bool): Set to ``True`` if you want the account disabled upon creation.
            email (str): The email address for the admin user.
            is_password_login_allowed (bool): Set to ``True`` to allow password login.
            is_security_report_comm_enabled (bool):
                Set to ``True`` to allow ZIA Security Update emails to be sent to the admin user.
            is_service_update_comm_enabled (bool):
                Set to ``True`` to allow ZIA Service Update emails to be sent to the admin user.
            is_product_update_comm_enabled (bool):
                Set to ``True`` to allow ZIA Product Update emails to be sent to the admin user.
            is_password_expired (bool):
                Set to ``True`` to expire the admin user's password upon creation.
            is_exec_mobile_app_enabled (bool):
                Set to ``True`` to enable to executive insights mobile application for the admin user.
            name (str): The user's full name.
            password (str): The password for the admin user.
            role_id (int): The unique id for the admin role being assigned to the admin user.
            scope_entity_ids (list):
                A list of entity ids for the admin user's scope. e.g. if the admin user has admin_scope set to
                ``department`` then you will need to provide a list of department ids.
                **NOTE**: This param doesn't need to
                be provided if the admin user's scope is set to ``ORGANIZATION``.

        Returns:
            :obj:`dict`: The updated admin user resource record.

        Examples:

            Update an admin user with the minimum required params:
                >>> update_admin_user, _, error = client.zia.admin_users.update_admin_user(
                ...    user_id=143783113,
                ...    name="Jim Bob",
                ...    login_name="jim@example.com",
                ...    password="*********",
                ...    email="jim@example.com")
                ...     )
                >>>     if error:
                ...         print(f"Error adding admin user: {error}")
                ...         return
                ...     print(f"Admin User added successfully: {update_admin_user.as_dict()}")

            Update an admin user with a department admin scope type:
                >>> update_admin_user, _, error = client.zia.admin_users.update_admin_user(
                ...    user_id=143783113,
                ...    name="Jane Bob",
                ...    login_name="jane@example.com",
                ...    password="*********",
                ...    email="jane@example.com,
                ...    role_id=84546,
                ...    admin_scope_type="DEPARTMENT",
                ...    scope_entity_ids = ['376542', '245688']
                ...     )
                >>>     if error:
                ...         print(f"Error adding admin user: {error}")
                ...         return
                ...     print(f"Admin User added successfully: {add_admin_user.as_dict()}")

            Update an auditor user:
                >>> update_admin_user = zia.admin_users.add_admin_user(
                ...    user_id=143783113,
                ...    name="Head Bob",
                ...    login_name="head@example.com",
                ...    password="*********",
                ...    email="head@example.com,
                ...    is_auditor=True,
                ...     )
                >>>     if error:
                ...         print(f"Error adding admin user: {error}")
                ...         return
                ...     print(f"Admin User added successfully: {add_admin_user.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminUsers/{user_id}
        """
        )

        body = kwargs

        if "role_id" in body:
            body["role"] = {"id": body.pop("role_id")}

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdminUser)
        if error:
            return (None, response, error)

        try:
            result = AdminUser(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_admin_user(self, user_id: int) -> tuple:
        """
        Deletes the specified admin user by id.

        Args:
            user_id (str): The unique id of the admin user.

        Returns:
            :obj:`int`: The response code for the request.

        Examples:
            >>> _, _, error = client.zia.admin_users.delete_admin_user(143783113)
            >>> if error:
            ...     print(f"Error deleting admin user: {error}")
            ...     return
            ... print(f"Admin User with ID {143783113} deleted successfully")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminUsers/{user_id}
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

    def convert_to_user(self, user_id: str, query_params=None, **kwargs) -> tuple:
        """
        Removes admin privileges for a user while retaining them as a regular user
        of your organization in the ZIA Admin Portal.
        This can be used as an alternative to the `delete_admin_user` method.

        Args:
            user_id (int): The unique ID for the User.
            name (str): User name. This appears when choosing users for policies.
                The name field allows values containing UTF-8 characters up to a maximum of 127 characters.

            email (str): User email consists of a user name and domain name.

            groups (list): List of Groups a user belongs to. Groups are used in policies.
            department (dict): Department a user belongs to

        Keyword Args:
            comments (str): Additional information about this user.
            **tempAuthEmail (str): Temporary Authentication Email.
                If you enabled one-time tokens or links, enter the email address to
                which the Zscaler service sends the tokens or links. If this is empty, the service will send the
                email to the User email.
            **adminUser (bool):
                True if this user is an Admin user.
            **password (str):
                User's password. Applicable only when authentication type is Hosted DB. Password strength must follow
                what is defined in the auth settings.

        Returns:
            :obj:`Tuple`: The resource record for the converted user.

        Examples:
            Add a user with the minimum required params:

            >>> user, zscaler_resp, err = zia.users.convert_to_user(name='Jane Doe',
            ...    user_id=99999
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
            /adminUsers/{user_id}/convertToUser
        """
        )

        query_params = query_params or {}

        headers = {}

        body = kwargs

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=body, headers=headers, params=query_params
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
