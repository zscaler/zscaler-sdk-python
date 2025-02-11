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

    def list_roles(self, query_params=None) -> tuple:
        """
        Return a list of the configured admin roles in ZIA.

        Args:
            query_params {dict}: Optional query parameters.
            
                ``[query_params.include_auditor_role]`` {bool}: Include or exclude auditor user information in the list.
                
                ``[query_params.include_partner_role]`` {bool}: Include or exclude admin user information in the list. Default is True.
                
                ``[query_params.include_api_role]`` {bool}: Include or exclude API role information in the list. Default is True.
                
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

        request, error = self._request_executor.create_request(
            http_method, api_url, body, headers, params=query_params
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = [AdminRoles(
                self.form_response_body(item)) for item in response.get_results()
            ]
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [role for role in results if lower_search in (role.name.lower() if role.name else "")]

        return (results, response, None)