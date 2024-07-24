# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from typing import List, Dict, Any, Optional, Union
from requests import Response, utils
from zscaler.utils import snake_to_camel, convert_keys
from zscaler.zcon.client import ZCONClient

class AdminRoles:
    def __init__(
        self,
        id: int,
        rank: Optional[int] = None,
        name: Optional[str] = None,
        policy_access: Optional[str] = None,
        alerting_access: Optional[str] = None,
        dashboard_access: Optional[str] = None,
        report_access: Optional[str] = None,
        analysis_access: Optional[str] = None,
        username_access: Optional[str] = None,
        admin_acct_access: Optional[str] = None,
        device_info_access: Optional[str] = None,
        is_auditor: Optional[bool] = None,
        permissions: Optional[List[str]] = None,
        is_non_editable: Optional[bool] = None,
        logs_limit: Optional[str] = None,
        role_type: Optional[str] = None,
        feature_permissions: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.id = id
        self.rank = rank
        self.name = name
        self.policy_access = policy_access
        self.alerting_access = alerting_access
        self.dashboard_access = dashboard_access
        self.report_access = report_access
        self.analysis_access = analysis_access
        self.username_access = username_access
        self.admin_acct_access = admin_acct_access
        self.device_info_access = device_info_access
        self.is_auditor = is_auditor
        self.permissions = permissions
        self.is_non_editable = is_non_editable
        self.logs_limit = logs_limit
        self.role_type = role_type
        self.feature_permissions = feature_permissions

        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class AdminRolesService:
    admin_roles_endpoint = "/adminRoles"

    def __init__(self, client: ZCONClient):
        self.client = client

    def _check_response(self, response: Response) -> Union[None, dict]:
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                raise Exception(f"Request failed with status code: {status_code}")
        return response

    def get_role(self, admin_role_id: int) -> Optional[AdminRoles]:
        """
        getting: HTTP Status 405 - Method Not Allowed
        """
        response = self.list_roles()
        for r in response:
            if r.id == admin_role_id:
                return r
        raise Exception(f"Failed to get admin role by ID {admin_role_id}, not found")

    def get_by_name(self, admin_role_name: str) -> Optional[AdminRoles]:
        response = self.client.get(self.admin_roles_endpoint)
        data = self._check_response(response)
        admin_roles = [AdminRoles(**role) for role in data]
        for admin_role in admin_roles:
            if admin_role.name.lower() == admin_role_name.lower():
                return admin_role
        raise Exception(f"No admin role found with name: {admin_role_name}")

    def get_api_role(self, api_role: str, include_api_role: bool = True) -> Optional[AdminRoles]:
        """
        Retrieves a specific admin role by name, optionally including API role information.

        Args:
            api_role (str): The name of the API admin role to retrieve.
            include_api_role (bool): Flag to include API role information.

        Returns:
            AdminRoles: The API admin role if found, otherwise None.
        """
        response = self.client.get(f"{self.admin_roles_endpoint}?includeApiRole={include_api_role}")
        data = self._check_response(response)
        admin_roles = [AdminRoles(**role) for role in data]
        for admin_role in admin_roles:
            if admin_role.name.lower() == api_role.lower():
                return admin_role
        raise Exception(f"No API role found with name: {api_role}")


    def get_auditor_role(self, auditor_role: str, include_auditor_role: bool = True) -> Optional[AdminRoles]:
        """
        Retrieves a specific admin role that includes or excludes auditor role information.

        Args:
            auditor_role (str): The auditor admin role to retrieve.
            include_auditor_role (bool): Flag to include auditor role information.

        Returns:
            AdminRoles: The auditor admin role if found, otherwise None.

        Examples:
            >>> role = zcon.admin_roles.get_auditor_role('Auditor_Role')
            >>> print(role)
        """
        response = self.client.get(f"{self.admin_roles_endpoint}?includeAuditorRole={str(include_auditor_role).lower()}")
        data = self._check_response(response)
        admin_roles = [AdminRoles(**role) for role in data]
        for admin_role in admin_roles:
            if admin_role.name.lower() == auditor_role.lower():
                return admin_role
        raise Exception(f"No auditor role found with name: {auditor_role}")

    def get_partner_role(self, partner_role: str, include_partner_role: bool = True) -> Optional[AdminRoles]:
        """
        Retrieves a specific admin role by name, optionally including partner role information.

        Args:
            partner_role (str): The name of the partner admin role to retrieve.
            include_partner_role (bool): Flag to include partner role information.

        Returns:
            AdminRoles: The partner admin role if found, otherwise None.
        """
        response = self.client.get(f"{self.admin_roles_endpoint}?includePartnerRole={include_partner_role}")
        data = self._check_response(response)
        admin_roles = [AdminRoles(**role) for role in data]
        for admin_role in admin_roles:
            if admin_role.name.lower() == partner_role.lower():
                return admin_role
        raise Exception(f"No partner role found with name: {partner_role}")

    def list_roles(
        self,
        include_auditor_role: bool = False,
        include_partner_role: bool = False,
        include_api_roles: bool = False,
        ids: Optional[List[int]] = None
    ) -> List[AdminRoles]:
        """
        List all existing admin roles.

        Args:
            include_auditor_role (bool): Include / exclude auditor roles in the response.
            include_partner_role (bool): Include / exclude partner roles in the response.
            include_api_roles (bool): Include / exclude API roles in the response.
            ids (list): The IDs of the roles to include.

        Returns:
            :obj:`List[AdminRoles]`: The list of roles.

        Examples:
            Print all roles::

                for role in zcon.admin_roles.list_roles():
                    print(role)

            Print all roles with additional parameters::

                for role in zcon.admin_roles.list_roles(
                    include_auditor_role=True,
                    include_partner_role=True,
                    include_api_roles=True,
                ):
                    print(role)

        """
        params = {
            "includeAuditorRole": str(include_auditor_role).lower(),
            "includePartnerRole": str(include_partner_role).lower(),
            "includeApiRoles": str(include_api_roles).lower(),
        }

        if ids:
            params["id"] = ",".join(map(str, ids))

        response = self.client.get(self.admin_roles_endpoint, params=params)
        data = self._check_response(response)
        return [AdminRoles(**role) for role in data]

    def add_role(
        self,
        name: str,
        policy_access: str = "NONE",
        report_access: str = "NONE",
        username_access: str = "NONE",
        dashboard_access: str = "NONE",
        **kwargs,
    ) -> Optional[AdminRoles]:
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
            :obj:`AdminRoles`: The newly created role.

        Examples:
            Minimum required arguments::

                zcon.admin.add_role(name="NewRole")

            Including keyword arguments::

                zcon.admin_roles.add_role(
                    name="AdvancedRole",
                    policy_access="READ_ONLY",
                    feature_permissions_tuples=[
                        ("apikey_management", "READ_ONLY"),
                        ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE")
                    ],
                    alerting_access="READ_WRITE"
                )
        """
        payload = {
            "name": name,
            "role_type": "EDGE_CONNECTOR_ADMIN",
            "policy_access": policy_access,
            "report_access": report_access,
            "username_access": username_access,
            "dashboard_access": dashboard_access,
        }

        if feature_permissions_tuples := kwargs.pop("feature_permissions_tuples", None):
            payload["feature_permissions"] = {k: v for k, v in feature_permissions_tuples}

        # Add optional parameters to payload
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        # Convert snake to camel case, excluding feature_permissions
        payload = {k: (convert_keys(v) if k != "feature_permissions" else v) for k, v in payload.items()}

        response = self.client.post(self.admin_roles_endpoint, json=payload)
        data = self._check_response(response)
        return AdminRoles(**data)

    def update_role(self, role_id: int, admin_role: AdminRoles) -> Optional[AdminRoles]:
        """
        Update an existing admin role.

        Args:
            role_id (int): The ID of the role to update.
            admin_role (AdminRoles): The AdminRoles object containing updated role data.

        Returns:
            :obj:`AdminRoles`: The updated role.

        Examples:
            Update an existing role::

                role = zcon.admin_roles.get_role(12345)
                role.policy_access = "READ_ONLY"
                updated_role = zcon.admin_roles.update_role(role.id, role)
        """
        payload = admin_role.to_api_payload()

        if "feature_permissions" in payload:
            payload["feature_permissions"] = {k: v for k, v in payload["feature_permissions"].items()}

        payload = {k: (convert_keys(v) if k != "feature_permissions" else v) for k, v in payload.items()}

        response = self.client.put(f"{self.admin_roles_endpoint}/{role_id}", json=payload)
        data = self._check_response(response)
        return AdminRoles(**data)

    def delete(self, role_id: int) -> None:
        """
        Delete an existing admin role.

        Args:
            admin_role_id (int): The ID of the role to delete.

        Examples:
            Delete an existing role::

                zcon.admin_roles.delete_role(12345)
        """
        response = self.client.delete(f"{self.admin_roles_endpoint}/{role_id}")
        self._check_response(response)
