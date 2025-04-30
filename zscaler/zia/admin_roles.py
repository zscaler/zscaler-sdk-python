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
from zscaler.zia.models.admin_roles import AdminRoles
from zscaler.zia.models.admin_roles import PasswordExpiry
from zscaler.utils import format_url


class AdminRolesAPI(APIClient):
    """
    A Client object for the Admin and Role resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_roles(self, query_params=None) -> tuple:
        """
        Return a list of the configured admin roles in ZIA.

        Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.include_auditor_role]`` {bool}: Include or exclude auditor user information in the list.

                ``[query_params.include_partner_role]`` {bool}: Include or exclude admin user information in the list.

                ``[query_params.include_api_role]`` {bool}: Include or exclude API role information in the list.

                ``[query_params.search]`` {str}: Search string for filtering results by admin role name.

        Returns:
            tuple: (list of AdminRoles instances, Response, error)

        Examples:
            Get a list of all admin roles:

            >>>  roles, response, error = client.zia.admin_roles.list_roles()
            ...  if error:
            ...     print(f"Error fetching roles: {error}")
            ...  return
            ...  print(f"Fetched roles: {[role.as_dict() for role in roles]}")

            Search for a specific admin role by name:

            >>>  role, response, error = client.zia.admin_roles.list_roles(
                query_params={"search": 'Super Admin'})
            ...  if error:
            ...     print(f"Error fetching role: {error}")
            ...  return
            ...  print(f"Fetched roles: {[role.as_dict() for role in role]}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminRoles/lite
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = [AdminRoles(self.form_response_body(item)) for item in response.get_results()]
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [role for role in results if lower_search in (role.name.lower() if role.name else "")]

        return (results, response, None)

    def get_role(self, role_id: int) -> tuple:
        """
        Fetches a specific admin role by ID.

        Args:
            role_id (int): The unique identifier for the admin role .

        Returns:
            tuple: A tuple containing (admin role  instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminRoles/{role_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdminRoles)
        if error:
            return (None, response, error)

        try:
            result = AdminRoles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_role(self, **kwargs) -> tuple:
        """
        Creates a new ZIA admin roles.

        Args:
            adminroles (dict or object):
                The admin roles data to be sent in the request.

        Returns:
            tuple: A tuple containing the newly added admin roles, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminRoles
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

        # Execute the request
        response, error = self._request_executor.execute(request, AdminRoles)
        if error:
            return (None, response, error)

        try:
            result = AdminRoles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_role(self, role_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA admin role.

        Args:
            role_id (int): The unique ID for the admin role.

        Returns:
            tuple: A tuple containing the updated admin role, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminRoles/{role_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdminRoles)
        if error:
            return (None, response, error)

        try:
            result = AdminRoles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_role(self, role_id: int) -> tuple:
        """
        Deletes the specified admin roles.

        Args:
            role_id (str): The unique identifier of the admin roles.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminRoles/{role_id}
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

    def get_password_expiry_settings(self) -> tuple:
        """
        Retrieves the password expiration information for all the admins

        Note: This method is not compatible with Zidentity enabled Tenants

        Returns:
            tuple: A tuple containing:
                - PasswordExpiry: The current password expiry settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieves the password expiration information for all the admins

            >>> settings, _, err = client.zia.admin_roles.get_password_expiry_settings()
            >>> if err:
            ...     print(f"Error fetching password expiry settings: {err}")
            ...     return
            ... print("Current password expiry settings fetched successfully.")
            ... print(settings)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /passwordExpiry/settings
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = PasswordExpiry(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_password_expiry_settings(self, **kwargs) -> tuple:
        """
        Updates the password expiration information for all the admins.

        Note: This method is not compatible with Zidentity enabled Tenants

        Args:
            Supported attributes:
                - password_expiration_enabled (bool): Specifies whether password expiration is enabled for the admin
                - password_expiry_days (int): Password expiration duration, calculated in days

        Returns:
            tuple: A tuple containing:
                - PasswordExpiry: The updated password expiry settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the update failed; otherwise, `None`.

        Examples:
            Update advanced threat protection settings by blocking specific threats:

            >>> settings, _, err = client.zia.admin_roles.update_password_expiry_settings(
            ...     password_expiration_enabled = True,
            ...     password_expiry_days = '90',
            ... )
            >>> if err:
            ...     print(f"Error fetching password expiry: {err}")
            ...     return
            ... print("Current password expiry fetched successfully.")
            ... print(settings)
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cyberThreatProtection/advancedThreatSettings
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PasswordExpiry)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = PasswordExpiry(self.form_response_body(response.get_body()))
            else:
                result = PasswordExpiry()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
