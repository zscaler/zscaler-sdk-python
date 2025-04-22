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
from zscaler.zia.models.advanced_settings import AdvancedSettings
from zscaler.utils import format_url


class AdvancedSettingsAPI(APIClient):
    """
    A Client object for the Advanced Settings resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_advanced_settings(self) -> tuple:
        """
        Retrieves the current advanced settings configured in the ZIA Admin Portal.

        This method makes a GET request to the ZIA Admin API and returns detailed advanced settings,
        including various bypass rules, DNS optimization configurations, and traffic control settings.

        Returns:
            tuple: A tuple containing:
                - AdvancedSettings: The current advanced settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current advanced settings:

            >>> settings, response, err = client.zia.advanced_settings.get_advanced_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /advancedSettings
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = AdvancedSettings(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_advanced_settings(self, **kwargs) -> tuple:
        """
        Updates advanced settings in the ZIA Admin Portal with the provided configuration.

        This method pushes updated advanced settings such as traffic control, DNS optimizations,
        authentication bypass rules, and session management configurations.

        Args:
            settings (:obj:`AdvancedSettings`):
                An instance of `AdvancedSettings` containing the updated configuration.

                **Supported attributes**:

                **Authentication and Bypass Rules**:
                - **auth_bypass_urls (list[str])**: Custom URLs exempted from cookie authentication.
                - **kerberos_bypass_urls (list[str])**: Custom URLs exempted from Kerberos authentication.
                - **digest_auth_bypass_urls (list[str])**: Custom URLs exempted from Digest authentication.
                - **dns_resolution_on_transparent_proxy_exempt_urls (list[str])**:
                URLs excluded from DNS optimization in transparent proxy mode.
                - **dns_resolution_on_transparent_proxy_urls (list[str])**:
                URLs where DNS optimization on transparent proxy mode applies.

                **DNS and Traffic Control**:
                - **enable_dns_resolution_on_transparent_proxy (bool)**:
                Enables DNS optimization for Z-Tunnel 2.0 traffic.
                - **enable_ipv6_dns_resolution_on_transparent_proxy (bool)**:
                Enables DNS optimization for IPv6 traffic.
                - **enable_ipv6_dns_optimization_on_all_transparent_proxy (bool)**:
                Enables DNS optimization for all IPv6 traffic.
                - **enable_evaluate_policy_on_global_ssl_bypass (bool)**:
                Enables policy evaluation for global SSL bypass traffic.

                **Application and URL Bypass Rules**:
                - **auth_bypass_apps (list[str])**: Applications exempted from cookie authentication.
                - **kerberos_bypass_apps (list[str])**: Applications exempted from Kerberos authentication.
                - **basic_bypass_apps (list[str])**: Applications exempted from Basic authentication.
                - **digest_auth_bypass_apps (list[str])**: Applications exempted from Digest authentication.
                - **dns_resolution_on_transparent_proxy_apps (list[str])**:
                Applications subject to DNS optimization in transparent proxy mode.
                - **dns_resolution_on_transparent_proxy_exempt_apps (list[str])**:
                Applications exempted from DNS optimization.

                **Session and Security Settings**:
                - **enable_office365 (bool)**:
                Enables Microsoft Office 365 One-Click configuration.
                - **log_internal_ip (bool)**:
                Logs internal IP addresses from X-Forwarded-For headers.
                - **enforce_surrogate_ip_for_windows_app (bool)**:
                Enforces Surrogate IP authentication for Windows apps.
                - **track_http_tunnel_on_http_ports (bool)**:
                Tracks tunneled HTTP traffic on port 80.
                - **block_http_tunnel_on_non_http_ports (bool)**:
                Blocks HTTP traffic on non-HTTP/HTTPS ports.
                - **block_domain_fronting_on_host_header (bool)**:
                Blocks HTTP transactions with FQDN mismatches.
                - **zscaler_client_connector_1and_pac_road_warrior_in_firewall (bool)**:
                Applies firewall rules to remote users using Z-Tunnel 1.0 or PAC files.
                - **cascade_url_filtering (bool)**:
                Applies URL filtering policies even when Cloud App Control allows traffic.
                - **enable_policy_for_unauthenticated_traffic (bool)**:
                Enables policy enforcement for unauthenticated traffic.
                - **block_non_compliant_http_request_on_http_ports (bool)**:
                Blocks non-compliant HTTP traffic on standard HTTP/HTTPS ports.
                - **enable_admin_rank_access (bool)**:
                Enables admin rank-based access control in policies.
                - **ui_session_timeout (int)**:
                Session timeout for ZIA Admin Portal login in seconds.

                **Advanced Security Features**:
                - **http2_nonbrowser_traffic_enabled (bool)**:
                Enables HTTP/2 for non-browser traffic.
                - **ecs_for_all_enabled (bool)**:
                Enables ECS option for all DNS queries.
                - **dynamic_user_risk_enabled (bool)**:
                Tracks risky user behavior in real time.
                - **block_connect_host_sni_mismatch (bool)**:
                Blocks requests where CONNECT host and SNI mismatch.
                - **prefer_sni_over_conn_host (bool)**:
                Prefers SNI over CONNECT host for DNS resolution.
                - **sipa_xff_header_enabled (bool)**:
                Inserts XFF headers in ZIA-to-ZPA traffic.
                - **block_non_http_on_http_port_enabled (bool)**:
                Blocks non-HTTP traffic on standard HTTP/HTTPS ports.

        Returns:
            tuple:
                - **AdvancedSettings**: The updated advanced settings object.
                - **Response**: The raw HTTP response returned by the API.
                - **error**: An error message if the update failed; otherwise, `None`.

        Examples:
            Update advanced settings by enabling Office365 and adjusting the session timeout:

            >>> settings, response, err = client.zia.advanced_settings.get_advanced_settings()
            >>> if not err:
            ...     settings.enable_office365 = True
            ...     settings.ui_session_timeout = 7200
            ...     updated_settings, response, err = client.zia.advanced_settings.update_advanced_settings(settings)
            ...     if not err:
            ...         print(f"Updated Enable Office365: {updated_settings.enable_office365}")
            ...     else:
            ...         print(f"Failed to update settings: {err}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /advancedSettings
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdvancedSettings)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = AdvancedSettings(self.form_response_body(response.get_body()))
            else:
                result = AdvancedSettings()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
