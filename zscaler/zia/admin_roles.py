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
from zscaler.utils import format_url


class AdminRolesAPI(APIClient):
    """
    A Client object for the Admin and Role resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_roles(
        self,
        query_params=None,
    ) -> tuple:
        """
        Return a list of the configured admin roles in ZIA.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.include_auditor_role] {bool}: Include or exclude auditor user information in the list.
                [query_params.include_partner_role] {bool}: Include or exclude admin user information in the list. Default is True.
                [query_params.search] {str}: The search string used to partially match against an admin/auditor user's Login ID or Name.
                [query_params.page] {int}: Specifies the page offset.
                [query_params.pagesize] {int}: Specifies the page size. The default size is 100, but the maximum size is 1000.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of AdminRole instances, Response, error)


        Examples:
            Get a list of all configured admin roles:
            >>> roles = zia.admin_and_management_roles.list_roles()

        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/adminRoles/lite")
        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(
            http_method,
            api_url,
            body,
            headers,
            params=query_params,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, AdminRoles)

        if error:
            return (None, response, error)

        # Parse the response into AdminUser instances
        try:
            result = []
            # this endpoint does not support pagination
            for item in response.get_results():
                result.append(AdminRoles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_roles_by_name(self, name):
        """
        Retrieves a specific admin roles by its name.

        Args:
            name (str): The name of the admin roles  to retrieve.

        Returns:
            :obj:`Box`: The admin roles  if found, otherwise None.

        Examples:
            >>> role = zia.admin_and_role_management.get_roles_by_name('Super Admin')
            ...    print(role)
        """
        roles = self.list_roles()
        for role in roles:
            if role.get("name") == name:
                return role
        return None

    def get_roles_by_id(self, role_id):
        """
        Retrieves a specific admin roles by its ID.

        Args:
            name (str): The ID of the admin roles  to retrieve.

        Returns:
            :obj:`Box`: The admin roles  if found, otherwise None.

        Examples:
            >>> role = zia.admin_and_role_management.get_roles_by_id('123456789')
            ...    print(role)
        """
        roles = self.list_roles()
        for role in roles:
            if role.get("id") == role_id:
                return role
        return None
