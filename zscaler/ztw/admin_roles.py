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
from zscaler.ztw.models.admin_roles import AdminRoles
from zscaler.utils import format_url


class AdminRolesAPI(APIClient):
    """
    A Client object for the Admin and Role resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_roles(self, query_params=None) -> tuple:
        """
        List all existing admin roles.

        Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.include_auditor_role]`` {bool}: Include or exclude auditor user information in the list.

                ``[query_params.include_partner_role]`` {bool}: Include or exclude admin user information in the list. Default is True.

                ``[query_params.include_api_roles]`` {bool}: Include or exclude API role information in the list. Default is True.

                ``[query_params.id]`` {list}: Include or exclude role ID information in the list.

        Returns:
            :obj:`Tuple`: The list of roles.

        Examples:
            Print all roles::

                for role in ztw.admin.list_roles():
                    print(role)

            Print all roles with additional parameters::

                for role in ztw.admin.list_roles(
                    include_auditor_role=True,
                    include_partner_role=True,
                    include_api_roles=True,
                ):
                    print(role)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /adminRoles
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

    def add_role(
        self,
        name: str,
        policy_access: str = "NONE",
        report_access: str = "NONE",
        username_access: str = "NONE",
        dashboard_access: str = "NONE",
        **kwargs,
    ) -> tuple:
        """
        Create a new admin role.

        Args:
            name (str): The name of the role.
            policy_access (str): The policy access level.
            report_access (str): The report access level.
            username_access (str): The username access level.
            dashboard_access (str): The dashboard access level.

        Keyword Args:
            feature_permissions_tuples (:obj:`List[Tuple[str, str]]`):
                A list of tuple pairs specifying the feature permissions. Each tuple contains the feature name
                (case-insensitive) and its access level.

                Accepted feature names (case-insensitive) are:

                - ``APIKEY_MANAGEMENT``
                - ``EDGE_CONNECTOR_CLOUD_PROVISIONING``
                - ``EDGE_CONNECTOR_LOCATION_MANAGEMENT``
                - ``EDGE_CONNECTOR_DASHBOARD``
                - ``EDGE_CONNECTOR_FORWARDING``
                - ``EDGE_CONNECTOR_TEMPLATE``
                - ``REMOTE_ASSISTANCE_MANAGEMENT``
                - ``EDGE_CONNECTOR_ADMIN_MANAGEMENT``
                - ``EDGE_CONNECTOR_NSS_CONFIGURATION``
            alerting_access (str): The alerting access level.
            analysis_access (str): The analysis access level.
            admin_acct_access (str): The admin account access level.
            device_info_access (str): The device info access level.

        Note:
            For access levels, the accepted values are:

            - ``NONE``
            - ``READ_ONLY``
            - ``READ_WRITE``


        Returns:
            :obj:`dict`: The newly created role.

        Examples:
            Minimum required arguments::

                ztw.admin.add_role(name="NewRole")

            Including keyword arguments::

                ztw.admin.add_role(
                    name="AdvancedRole",
                    policy_access="READ_ONLY",
                    feature_permissions_tuples=[
                        ("apikey_management", "read_only"),
                        ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE")
                    ],
                    alerting_access="READ_WRITE"
                )

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /adminRoles
        """
        )

        payload = {
            "name": name,
            "role_type": "EDGE_CONNECTOR_ADMIN",
            "policy_access": policy_access,
            "report_access": report_access,
            "username_access": username_access,
            "dashboard_access": dashboard_access,
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

        response, error = self._request_executor.execute(request, AdminRoles)
        if error:
            return (None, response, error)

        try:
            result = AdminRoles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_role(self, role_id: str, **kwargs) -> tuple:
        """
        Update an existing admin role.

        Args:
            role_id (str): The ID of the role to update.

        Keyword Args:
            name (str): The name of the role.
            policy_access (str): The policy access level.
            report_access (str): The report access level.
            username_access (str): The username access level.
            dashboard_access (str): The dashboard access level.
            feature_permissions (:obj:`List[Tuple[str, str]]`):
                A list of tuple pairs specifying the feature permissions. Each tuple contains the feature name
                (case-insensitive) and its access level.

                Accepted feature names (case-insensitive) are:

                - ``APIKEY_MANAGEMENT``
                - ``EDGE_CONNECTOR_CLOUD_PROVISIONING``
                - ``EDGE_CONNECTOR_LOCATION_MANAGEMENT``
                - ``EDGE_CONNECTOR_DASHBOARD``
                - ``EDGE_CONNECTOR_FORWARDING``
                - ``EDGE_CONNECTOR_TEMPLATE``
                - ``REMOTE_ASSISTANCE_MANAGEMENT``
                - ``EDGE_CONNECTOR_ADMIN_MANAGEMENT``
                - ``EDGE_CONNECTOR_NSS_CONFIGURATION``
            alerting_access (str): The alerting access level.
            analysis_access (str): The analysis access level.
            admin_acct_access (str): The admin account access level.
            device_info_access (str): The device info access level.

        Note:
            For access levels, the accepted values are:

            - ``NONE``
            - ``READ_ONLY``
            - ``READ_WRITE``

        Returns:
            :obj:`Tuple`: The updated role.

        Examples:
            Update a role::

                ztw.admin.update_role(
                    role_id="123456789",
                    policy_access="READ_ONLY",
                    feature_permissions=[
                        ("apikey_management", "read_only"),
                        ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE")
                    ],
                    alerting_access="READ_WRITE"
                )

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
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

    def delete_role(self, role_id: str) -> tuple:
        """
        Delete the specified admin role.

        Args:
            role_id (str): The ID of the role to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Delete a role::

                ztw.admin.delete_role("123456789")

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
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
