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

            >>>  role, _, error = client.zia.admin_roles.list_roles(
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

        Examples:
            >>> fetched_role, _, error = client.zia.admin_roles.get_role(143783113)
            >>> if error:
            ...     print(f"Error fetching admin role by ID: {error}")
            ...     return
            ... print(f"Fetched Admin role by ID: {fetched_role.as_dict()}")
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
            name (str): Name of the admin role
            policy_access (str): Policy access permission. Accepted values are:
                ``NONE``, ``READ_ONLY``, ``READ_WRITE``
            alerting_access (str): Alerting access permission. Accepted values are:
                ``NONE``, ``READ_ONLY``, ``READ_WRITE``
            dashboard_access (str): Dashboard access permission. Accepted values are:
                ``NONE``, ``READ_ONLY``
            report_access (str): Report access permission. Accepted values are:
                ``NONE``, ``READ_ONLY``, ``READ_WRITE``
            analysis_access (str): Insights Logs access permission. Accepted values are:
                ``NONE``, ``READ_ONLY``
            username_access (str): Username access permission. When set to NONE, the username is obfuscated.
                Accepted values are: ``NONE``, ``READ_ONLY``
            device_info_access (str): Device information access permission. When set to NONE, the username is obfuscated.
                Accepted values are: ``NONE``, ``READ_ONLY``
            admin_acct_access (str): Admin and role management access permission.
                Accepted values are: ``NONE``, ``READ_WRITE``
            logs_limit (str): Enter the number of days an admin with this role can view logs
                Accepted values are: `UNRESTRICTED`, `MONTH_1`, `MONTH_2`, `MONTH_3`, `MONTH_4`, `MONTH_5`, `MONTH_6`
            role_type (str): The admin role type. This attribute is subject to change.
                Accepted values are: `ORG_ADMIN`, `EXEC_INSIGHT`, `EXEC_INSIGHT_AND_ORG_ADMIN`, `SDWAN`
            report_time_duration (int): Time duration allocated to the report dashboard.
                The default value of -1 indicates that no time restriction is applied to the report dashboard.
                Time Unit is in hours.
            is_non_editable (bool): Indicates whether or not this admin user is editable
            feature_permissions (dict): Feature access permission

                Supported Values:
                    - `SECURE_BROWSING`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `ADVANCED_THREAT_PROTECTION`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `CLOUD_SANDBOX`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `MALWARE_PROTECTION`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `IPS_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `MOBILE_MALWARE_PROTECTION`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `URL_CLOUD_APP_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `FIREWALL_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `DNS_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `NAT_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `FILE_TYPE_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `MOBILE_APP_STORE_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `BANDWIDTH_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `FTP_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `INLINE_DLP`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `END_POINT_DLP`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `SAAS_SECURITY_API`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `SAAS_SECURITY_POSTURE_MGMT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `DLP_DICTIONARIES_ENGINES`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `DLP_NOTIFICATION_TEMPLATES`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `SAAS_APPLICATION_TENANTS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `DLP_INCIDENT_RECEIVER`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `SSL_POLICY`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `INTERMEDIATE_CA_CERTIFICATES`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `THIRD_PARTY_SSL_ROOT_CERTS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `ZS_DEFINED_URL_CATEGORY_MGMT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `CUSTOM_URL_CAT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `OVERRIDE_EXISTING_CAT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `IP_FQDN_GROUPS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `BROWSER_ISOLATION`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `DEVICE_MANAGEMENT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `TIME_INTERVALS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `REPORTING_SECURITY`: Supported Values: "READ_ONLY",
                    - `REPORTING_WEB_DATA`: Supported Values: "READ_ONLY",
                    - `REPORTING_DLP`: Supported Values: "READ_ONLY",
                    - `REPORTING_FIREWALL`: Supported Values: "READ_ONLY",
                    - `REPORTING_URL_CATEGORIES`: Supported Values: "READ_ONLY",
                    - `REPORTING_IOT`: Supported Values: "READ_ONLY",
                    - `ADVANCED_SETTINGS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `ADMINISTRATOR_MANAGEMENT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `AUDIT_LOGS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `USER_MANAGEMENT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `REMOTE_ASSISTANCE_MANAGEMENT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `ALERTS_CONFIGURATION`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `AUTHENTICATION_SETTINGS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `IDENTITY_PROXY_SETTINGS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `ROLE_MANAGEMENT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `FORWARDING_CONTROL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `STATIC_IPS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `GRE_TUNNELS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `LOCATIONS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `VPN_CREDENTIALS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `HOSTED_PAC_FILES`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `PROXY_GATEWAY`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `CLIENT_CONNECTOR_PORTAL`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `SUBCLOUDS`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `ZIA_TRAFFIC_CAPTURE`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `MICROSOFT_CLOUD_APP_SECURITY`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `SD_WAN`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `AZURE_VIRTUAL_WAN`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `CROWDSTRIKE`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `MICROSOFT_DEFENDER_FOR_ENDPOINT`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `INCIDENT_WORKFLOW`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `NSS_CONFIGURATION`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `VZEN_CONFIGURATION`: Supported Values: `READ_WRITE`,  `READ_ONLY`
                    - `APIKEY_MANAGEMENT`: Supported Values: "READ_WRITE"

        Returns:
            tuple: A tuple containing the newly added admin roles, response, and error.

        Examples:

            Add an admin role:
                >>> add_role, _, error = client.zia.admin_roles.add_role(
                ...     name=f"NewRole_{random.randint(1000, 10000)}",
                ...     role_type='ORG_ADMIN',
                ...     policy_access='READ_WRITE',
                ...     alerting_access='READ_WRITE',
                ...     dashboard_access='READ_WRITE',
                ...     report_access='READ_WRITE',
                ...     analysis_access='READ_ONLY',
                ...     username_access='READ_ONLY',
                ...     device_info_access='READ_ONLY',
                ...     admin_acct_access='READ_WRITE',
                ...     is_auditor=False,
                ...     is_non_editable=False,
                ...     logs_limit='UNRESTRICTED',
                ...     report_time_duration=-1,
                ...     feature_permissions={
                ...         "SECURE_BROWSING": "READ_WRITE",
                ...         "ADVANCED_THREAT_PROTECTION": "READ_WRITE",
                ...         "CLOUD_SANDBOX": "READ_WRITE",
                ...         "MALWARE_PROTECTION": "READ_WRITE",
                ...         "IPS_CONTROL": "READ_WRITE",
                ...         "MOBILE_MALWARE_PROTECTION": "READ_WRITE",
                ...         "URL_CLOUD_APP_CONTROL": "READ_WRITE",
                ...         "FIREWALL_CONTROL": "READ_WRITE",
                ...         "DNS_CONTROL": "READ_WRITE",
                ...         "NAT_CONTROL": "READ_WRITE",
                ...         "FILE_TYPE_CONTROL": "READ_WRITE",
                ...         "MOBILE_APP_STORE_CONTROL": "READ_WRITE",
                ...         "BANDWIDTH_CONTROL": "READ_WRITE",
                ...         "FTP_CONTROL": "READ_WRITE",
                ...         "INLINE_DLP": "READ_WRITE",
                ...         "END_POINT_DLP": "READ_WRITE",
                ...         "SAAS_SECURITY_API": "READ_WRITE",
                ...         "SAAS_SECURITY_POSTURE_MGMT": "READ_WRITE",
                ...         "DLP_DICTIONARIES_ENGINES": "READ_WRITE",
                ...         "DLP_NOTIFICATION_TEMPLATES": "READ_WRITE",
                ...         "SAAS_APPLICATION_TENANTS": "READ_WRITE",
                ...         "DLP_INCIDENT_RECEIVER": "READ_WRITE",
                ...         "SSL_POLICY": "READ_WRITE",
                ...         "INTERMEDIATE_CA_CERTIFICATES": "READ_WRITE",
                ...         "THIRD_PARTY_SSL_ROOT_CERTS": "READ_WRITE",
                ...         "ZS_DEFINED_URL_CATEGORY_MGMT": "READ_WRITE",
                ...         "CUSTOM_URL_CAT": "READ_WRITE",
                ...         "OVERRIDE_EXISTING_CAT": "READ_WRITE",
                ...         "IP_FQDN_GROUPS": "READ_WRITE",
                ...         "BROWSER_ISOLATION": "READ_WRITE",
                ...         "DEVICE_MANAGEMENT": "READ_WRITE",
                ...         "TIME_INTERVALS": "READ_WRITE",
                ...         "REPORTING_SECURITY": "READ_ONLY",
                ...         "REPORTING_WEB_DATA": "READ_ONLY",
                ...         "REPORTING_DLP": "READ_ONLY",
                ...         "REPORTING_FIREWALL": "READ_ONLY",
                ...         "REPORTING_URL_CATEGORIES": "READ_ONLY",
                ...         "REPORTING_IOT": "READ_ONLY",
                ...         "ADVANCED_SETTINGS": "READ_WRITE",
                ...         "ADMINISTRATOR_MANAGEMENT": "READ_WRITE",
                ...         "AUDIT_LOGS": "READ_WRITE",
                ...         "USER_MANAGEMENT": "READ_WRITE",
                ...         "REMOTE_ASSISTANCE_MANAGEMENT": "READ_WRITE",
                ...         "ALERTS_CONFIGURATION": "READ_WRITE",
                ...         "AUTHENTICATION_SETTINGS": "READ_WRITE",
                ...         "IDENTITY_PROXY_SETTINGS": "READ_WRITE",
                ...         "ROLE_MANAGEMENT": "READ_WRITE",
                ...         "FORWARDING_CONTROL": "READ_WRITE",
                ...         "STATIC_IPS": "READ_WRITE",
                ...         "GRE_TUNNELS": "READ_WRITE",
                ...         "LOCATIONS": "READ_WRITE",
                ...         "VPN_CREDENTIALS": "READ_WRITE",
                ...         "HOSTED_PAC_FILES": "READ_WRITE",
                ...         "PROXY_GATEWAY": "READ_WRITE",
                ...         "CLIENT_CONNECTOR_PORTAL": "READ_WRITE",
                ...         "SUBCLOUDS": "READ_WRITE",
                ...         "ZIA_TRAFFIC_CAPTURE": "READ_WRITE",
                ...         "MICROSOFT_CLOUD_APP_SECURITY": "READ_WRITE",
                ...         "SD_WAN": "READ_WRITE",
                ...         "AZURE_VIRTUAL_WAN": "READ_WRITE",
                ...         "CROWDSTRIKE": "READ_WRITE",
                ...         "MICROSOFT_DEFENDER_FOR_ENDPOINT": "READ_WRITE",
                ...         "INCIDENT_WORKFLOW": "READ_WRITE",
                ...         "NSS_CONFIGURATION": "READ_WRITE",
                ...         "VZEN_CONFIGURATION": "READ_WRITE",
                ...         "APIKEY_MANAGEMENT": "READ_WRITE"
                ...     }
                ... )
                >>> if error:
                ...     print(f"Error adding role: {error}")
                ...     return
                ... print(f"Role added successfully: {add_role.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminRoles
        """
        )

        body = kwargs
        if "feature_permissions" in body and isinstance(body["feature_permissions"], dict):
            body["featurePermissions"] = body.pop("feature_permissions")

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

    def update_role(self, role_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA admin role.

        Args:
            role_id (int): The unique ID for the admin role.

        Returns:
            tuple: A tuple containing the updated admin role, response, and error.

        Examples:

            Update an admin role:
                >>> update_role, _, error = client.zia.admin_roles.update_role(
                ...     role_id=143783113,
                ...     name=f"NewRole_{random.randint(1000, 10000)}",
                ...     role_type='ORG_ADMIN',
                ...     policy_access='READ_WRITE',
                ...     alerting_access='READ_WRITE',
                ...     dashboard_access='READ_WRITE',
                ...     report_access='READ_WRITE',
                ...     analysis_access='READ_ONLY',
                ...     username_access='READ_ONLY',
                ...     device_info_access='READ_ONLY',
                ...     admin_acct_access='READ_WRITE',
                ...     is_auditor=False,
                ...     is_non_editable=False,
                ...     logs_limit='UNRESTRICTED',
                ...     report_time_duration=-1,
                ...     feature_permissions={
                ...         "SECURE_BROWSING": "READ_WRITE",
                ...         "ADVANCED_THREAT_PROTECTION": "READ_WRITE",
                ...         "CLOUD_SANDBOX": "READ_WRITE",
                ...         "MALWARE_PROTECTION": "READ_WRITE",
                ...         "IPS_CONTROL": "READ_WRITE",
                ...         "MOBILE_MALWARE_PROTECTION": "READ_WRITE",
                ...         "URL_CLOUD_APP_CONTROL": "READ_WRITE",
                ...         "FIREWALL_CONTROL": "READ_WRITE",
                ...         "DNS_CONTROL": "READ_WRITE",
                ...         "NAT_CONTROL": "READ_WRITE",
                ...         "FILE_TYPE_CONTROL": "READ_WRITE",
                ...         "MOBILE_APP_STORE_CONTROL": "READ_WRITE",
                ...         "BANDWIDTH_CONTROL": "READ_WRITE",
                ...         "FTP_CONTROL": "READ_WRITE",
                ...         "INLINE_DLP": "READ_WRITE",
                ...         "END_POINT_DLP": "READ_WRITE",
                ...         "SAAS_SECURITY_API": "READ_WRITE",
                ...         "SAAS_SECURITY_POSTURE_MGMT": "READ_WRITE",
                ...         "DLP_DICTIONARIES_ENGINES": "READ_WRITE",
                ...         "DLP_NOTIFICATION_TEMPLATES": "READ_WRITE",
                ...         "SAAS_APPLICATION_TENANTS": "READ_WRITE",
                ...         "DLP_INCIDENT_RECEIVER": "READ_WRITE",
                ...         "SSL_POLICY": "READ_WRITE",
                ...         "INTERMEDIATE_CA_CERTIFICATES": "READ_WRITE",
                ...         "THIRD_PARTY_SSL_ROOT_CERTS": "READ_WRITE",
                ...         "ZS_DEFINED_URL_CATEGORY_MGMT": "READ_WRITE",
                ...         "CUSTOM_URL_CAT": "READ_WRITE",
                ...         "OVERRIDE_EXISTING_CAT": "READ_WRITE",
                ...         "IP_FQDN_GROUPS": "READ_WRITE",
                ...         "BROWSER_ISOLATION": "READ_WRITE",
                ...         "DEVICE_MANAGEMENT": "READ_WRITE",
                ...         "TIME_INTERVALS": "READ_WRITE",
                ...         "REPORTING_SECURITY": "READ_ONLY",
                ...         "REPORTING_WEB_DATA": "READ_ONLY",
                ...         "REPORTING_DLP": "READ_ONLY",
                ...         "REPORTING_FIREWALL": "READ_ONLY",
                ...         "REPORTING_URL_CATEGORIES": "READ_ONLY",
                ...         "REPORTING_IOT": "READ_ONLY",
                ...         "ADVANCED_SETTINGS": "READ_WRITE",
                ...         "ADMINISTRATOR_MANAGEMENT": "READ_WRITE",
                ...         "AUDIT_LOGS": "READ_WRITE",
                ...         "USER_MANAGEMENT": "READ_WRITE",
                ...         "REMOTE_ASSISTANCE_MANAGEMENT": "READ_WRITE",
                ...         "ALERTS_CONFIGURATION": "READ_WRITE",
                ...         "AUTHENTICATION_SETTINGS": "READ_WRITE",
                ...         "IDENTITY_PROXY_SETTINGS": "READ_WRITE",
                ...         "ROLE_MANAGEMENT": "READ_WRITE",
                ...         "FORWARDING_CONTROL": "READ_WRITE",
                ...         "STATIC_IPS": "READ_WRITE",
                ...         "GRE_TUNNELS": "READ_WRITE",
                ...         "LOCATIONS": "READ_WRITE",
                ...         "VPN_CREDENTIALS": "READ_WRITE",
                ...         "HOSTED_PAC_FILES": "READ_WRITE",
                ...         "PROXY_GATEWAY": "READ_WRITE",
                ...         "CLIENT_CONNECTOR_PORTAL": "READ_WRITE",
                ...         "SUBCLOUDS": "READ_WRITE",
                ...         "ZIA_TRAFFIC_CAPTURE": "READ_WRITE",
                ...         "MICROSOFT_CLOUD_APP_SECURITY": "READ_WRITE",
                ...         "SD_WAN": "READ_WRITE",
                ...         "AZURE_VIRTUAL_WAN": "READ_WRITE",
                ...         "CROWDSTRIKE": "READ_WRITE",
                ...         "MICROSOFT_DEFENDER_FOR_ENDPOINT": "READ_WRITE",
                ...         "INCIDENT_WORKFLOW": "READ_WRITE",
                ...         "NSS_CONFIGURATION": "READ_WRITE",
                ...         "VZEN_CONFIGURATION": "READ_WRITE",
                ...         "APIKEY_MANAGEMENT": "READ_WRITE"
                ...     }
                ... )
                >>> if error:
                ...     print(f"Error adding role: {error}")
                ...     return
                ... print(f"Role added successfully: {add_role.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /adminRoles/{role_id}
        """
        )

        body = kwargs

        if "feature_permissions" in body and isinstance(body["feature_permissions"], dict):
            body["featurePermissions"] = body.pop("feature_permissions")

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

    def delete_role(self, role_id: int) -> tuple:
        """
        Deletes the specified admin roles.

        Args:
            role_id (str): The unique identifier of the admin roles.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            >>> _, _, error = client.zia.admin_roles.delete_role(143783113)
            >>> if error:
            ...     print(f"Error deleting admin role: {error}")
            ...     return
            ... print(f"Admin Role with ID {143783113} deleted successfully")
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
