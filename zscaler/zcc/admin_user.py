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
from zscaler.utils import format_url
from zscaler.zcc.models.admin_user import AdminUser, AdminUserSyncInfo
from zscaler.zcc.models.admin_roles import AdminRoles


class AdminUserAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def list_admin_users(self, query_params=None) -> tuple:
        """
        Returns the list of Admin Users enrolled in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.user_type]`` {str}: Filter based on type of user.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size.

        Returns:
            :obj:`list`: A list containing Admin Users in the Client Connector Portal.

        Examples:
            Prints all admins in the Client Connector Portal to the console:

            >>> user_list, _, err = client.zcc.admin_user.list_admin_users()
            >>> if err:
            ...     print(f"Error listing admin users: {err}")
            ...     return
            ... print(f"Total admin users found: {len(user_list)}")
            ... for user in user_list:
            ...     print(user.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getAdminUsers
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
                result.append(AdminUser(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_admin_user_sync_info(self) -> tuple:
        """
        Returns admin user sync information Client Connector Portal.

        Args:
            N/A

        Returns:
            :obj:`list`: A list containing Admin Users in the Client Connector Portal.

        Examples:
            Prints all admins in the Client Connector Portal to the console:

            >>> sync_info, _, error = client.zcc.admin_user.get_admin_user_sync_info()
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            ... print(sync_info.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getAdminUsersSyncInfo
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return None, None, error

        response, error = self._request_executor.execute(request)
        if error:
            return None, response, error

        try:
            result = AdminUserSyncInfo(self.form_response_body(response.get_body()))
        except Exception as error:
            return None, response, error

        return result, response, None

    def list_admin_roles(self, query_params=None) -> tuple:
        """
        Returns the list admin roles in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size.

        Returns:
            :obj:`list`: A list containing admin roles in the Client Connector Portal.

        Examples:
            Prints all admin roles in the Client Connector Portal to the console:

            >>> role_list, _, err = client.zcc.admin_user.list_admin_roles()
            >>>     if err:
            ...         print(f"Error listing admin roles: {err}")
            ...         return
            ...     print(f"Total admin roles found: {len(role_list)}")
            ...     for role in role_list:
            ...         print(role.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getAdminRoles
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
                result.append(AdminRoles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def sync_zia_zdx_admin_users(self) -> tuple:
        """
        Sync Admin Users Information for ZDX and ZIA Client Connector Portal.

        Args:
            N/A

        Returns:
            :obj:`list`: Returns Sync Admin Users Information for ZDX and ZIA.

        Examples:
            Prints Sync Admin Users Information in the Client Connector Portal to the console:

            >>> for sync in zcc.admin_user.sync_zia_zdx_admin_users():
            ...    print(sync)

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /syncZiaZdxAdminUsers
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append((self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def sync_zpa_admin_users(self) -> tuple:
        """
        Sync Admin Users Information for ZPA Client Connector Portal.

        Args:
            N/A

        Returns:
            :obj:`list`: Returns Sync Admin Users Information for ZPA.

        Examples:
            Prints Sync Admin Users Information in the Client Connector Portal to the console:

            >>> for sync in zcc.admin_user.sync_zpa_admin_users():
            ...    print(sync)

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /syncZpaAdminUsers
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append((self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
