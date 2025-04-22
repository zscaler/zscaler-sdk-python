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
from zscaler.ztw.models.admin_users import AdminUsers
from zscaler.utils import format_url


class AdminUsersAPI(APIClient):
    """
    A Client object for the Admin and Role resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def change_password(self, username: str, old_password: str, new_password: str, **kwargs) -> tuple:
        """
        Change the password for the specified admin user.

        Args:
            username (str): The username of the admin user.
            old_password (str): The current password of the admin user.
            new_password (str): The new password for the admin user.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Change a password::

                ztw.admin.change_password("jdoe", "oldpassword123", "newpassword123")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /passwordChange
        """
        )

        # Define the fixed payload
        payload = {
            "userName": username,
            "oldPassword": old_password,
            "newPassword": new_password,
        }

        # Merge the fixed payload with any additional kwargs
        body = {**payload, **kwargs}

        # Create the request with the merged body
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_admins(self, query_params=None) -> tuple:
        """
        List all existing admin users.

        Keyword Args:
            include_auditor_users (bool): Include / exclude auditor users in the response.
            include_admin_users (bool): Include / exclude admin users in the response.
            include_api_roles (bool): Include / exclude API roles in the response.
            search (str): The search string to filter by.
            page (int): The page offset to return.
            page_size (int): The number of records to return per page.
            version (int): Specifies the admins from a backup version


        Returns:
            :obj:`Tuple`: The list of admin users.

        Examples:
            List all admins::

                for admin in ztw.admin.list_admins():
                    print(admin)

            List all admins with advanced features::

                for admin in ztw.admin.list_admins(
                    include_auditor_users=True,
                    include_admin_users=True,
                    include_api_roles=True,
                ):
                    print(admin)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}/adminUsers
            """
        )
        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(AdminUsers(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_admin(self, admin_id: str) -> tuple:
        """
        Get details for a specific admin user.

        Args:
            admin_id (str): The ID of the admin user to retrieve.

        Returns:
            :obj:`Tuple`: The admin user details.

        Examples:
            Print the details of an admin user::

                print(ztw.admin.get_admin("123456789")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}/adminUsers/{admin_id}
            """
        )

        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, AdminUsers)

        if error:
            return (None, response, error)

        # Parse the response
        try:
            result = AdminUsers(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_admin(self, user_name: str, login_name: str, role: str, email: str, password: str, **kwargs) -> tuple:
        """
        Create a new admin user.

        Args:
            user_name (str): The name of the admin user.
            login_name (str): The login name of the admin user.
            role (str): The role of the admin user.
            email (str): The email address of the admin user.
            password (str): The password for the admin user.

        Keyword Args:
            disabled (bool): Indicates whether the admin is disabled.
            new_location_create_allowed (bool): Indicates whether the admin can create new locations.
            admin_scope_type (str): The admin scope type.
            admin_scope_group_member_entity_ids (list): Applicable if the admin scope type is `LOCATION_GROUP`.
            is_default_admin (bool): Indicates whether the admin is the default admin.
            is_deprecated_default_admin (bool): Indicates whether this admin is deletable.
            is_auditor (bool): Indicates whether the admin is an auditor.
            is_security_report_comm_enabled (bool): Indicates whether the admin can receive security reports.
            is_service_update_comm_enabled (bool): Indicates whether the admin can receive service updates.
            is_password_login_allowed (bool): Indicates whether the admin can log in with a password.
            is_product_update_comm_enabled (bool): Indicates whether the admin can receive product updates.
            is_exec_mobile_app_enabled (bool): Indicates whether Executive Insights App access is enabled for the admin.
            send_mobile_app_invite (bool):
                Indicates whether to send an invitation email to download Executive Insights App to admin.
            send_zdx_onboard_invite (bool): Indicates whether to send an invitation email for ZDX onboarding to admin.
            comments (str): Comments for the admin user.
            name (str):
                Admin user's "friendly" name, e.g., "FirstName LastName" (this field typically matches userName.)

        Returns:
            Tuple: A Box object representing the newly created admin user.

        Examples:
            Create a new admin user with only the required parameters::

                ztw.admin.add_admin(
                    name="Jane Smith",
                    login_name="jsmith",
                    role="admin",
                    email="jsmith@example.com",
                    password="password123",
                    )

            Create a new admin with some additional parameters::

                ztw.admin.add_admin(
                    name="Jane Smith",
                    login_name="jsmith",
                    role="admin",
                    email="jsmith@example.com",
                    password="password123",
                    is_default_admin=False,
                    disabled=False,
                    comments="New admin user"

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /adminUsers
        """
        )

        payload = {
            "loginName": login_name,
            "userName": user_name,
            "email": email,
            "role": role,
            "password": password,
        }

        body = {**payload, **kwargs}

        # Create the request with no empty param handling logic
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, AdminUsers)
        if error:
            return (None, response, error)

        try:
            result = AdminUsers(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_admin(self, admin_id: str, **kwargs) -> tuple:
        """
        Update an existing admin user.

        Args:
            admin_id (str): The ID of the admin user to update.

        Keyword Args:
            role (str): The role of the admin user.
            email (str): The email address of the admin user.
            password (str): The password for the admin user.
            disabled (bool): Indicates whether the admin is disabled.
            new_location_create_allowed (bool): Indicates whether the admin can create new locations.
            admin_scope_type (str): The admin scope type.
            admin_scope_group_member_entity_ids (list): Applicable if the admin scope type is `LOCATION_GROUP`.
            is_default_admin (bool): Indicates whether the admin is the default admin.
            is_deprecated_default_admin (bool): Indicates whether this admin is deletable.
            is_auditor (bool): Indicates whether the admin is an auditor.
            is_security_report_comm_enabled (bool): Indicates whether the admin can receive security reports.
            is_service_update_comm_enabled (bool): Indicates whether the admin can receive service updates.
            is_password_login_allowed (bool): Indicates whether the admin can log in with a password.
            is_product_update_comm_enabled (bool): Indicates whether the admin can receive product updates.
            is_exec_mobile_app_enabled (bool): Indicates whether Executive Insights App access is enabled for the admin.
            send_mobile_app_invite (bool):
                Indicates whether to send an invitation email to download Executive Insights App to admin.
            send_zdx_onboard_invite (bool): Indicates whether to send an invitation email for ZDX onboarding to admin.
            comments (str): Comments for the admin user.
            name (str):
                Admin user's "friendly" name, e.g., "FirstName LastName" (this field typically matches userName.)

        Returns:
            Tuple: A Box object representing the updated admin user.

        Examples:
            Update an admin user::

                ztw.admin.update_admin(
                    admin_id="123456789",
                    admin_scope_type="LOCATION_GROUP",
                    comments="Updated admin user",
                )

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /adminUsers/{admin_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdminUsers)
        if error:
            return (None, response, error)

        try:
            result = AdminUsers(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_admin(self, admin_id: str) -> int:
        """
        Delete the specified admin user.

        Args:
            admin_id (str): The ID of the admin user to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Delete an admin user::

                ztw.admin.delete_admin("123456789")

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /adminUsers/{admin_id}
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
