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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url, zcc_param_mapper
from zscaler.zcc._serialize import zcc_to_wire
from zscaler.zcc.models.webpolicy import WebPolicy
from zscaler.types import APIResult


class WebPolicyAPI(APIClient):

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    @zcc_param_mapper
    def list_by_company(self, query_params: Optional[dict] = None) -> APIResult[List[WebPolicy]]:
        """
        Returns the list of Web Policy By Company ID in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.

                ``[query_params.device_type]`` {str}: Filter by device operating system type. Valid options are:
                    ios, android, windows, macos, linux.

                ``[query_params.search]`` {str}: The search string used to partially match.

                ``[query_params.search_type]`` {str}: The search string used to partially match.

        Returns:
            :obj:`list`: A list containing Web Policy By Company ID in the Client Connector Portal.

        Examples:
            Prints Web Policy By Company ID in the Client Connector Portal to the console:

            >>> policy_list, _, err = client.zcc.web_policy.list_by_company(query_params={'device_type': 'windows'})
            >>> if err:
            ...     print(f"Error listing company policies: {err}")
            ...     return
            ... for policy in policy_list:
            ...     print(policy.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /web/policy/listByCompany
        """)

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WebPolicy)
        if error:
            return (None, response, error)

        try:
            result = response.get_results()
        except Exception as error:
            return None, response, error

        return result, response, None

    @zcc_param_mapper
    def activate_web_policy(self, **kwargs) -> APIResult[dict]:
        """
        Enables or disables a policy or app profile for the company by platform (iOS, Android, Windows, macOS, and Linux).

        Args:
           device_type: (int):
           policy_id: (int):

        Returns:
            tuple: A tuple containing the updated Activation Web Policy, response, and error.

        Examples:
            Activate Web Policy in the Client Connector Portal to the console:

            >>> web_policy, _, error = client.zcc.web_policy.activate_web_policy(
            ...     device_type='3',
            ...     policy_id='1',
            ... )
            >>> if error:
            ...     print(f"Error activating web policy: {error}")
            ...     return
            ... print(f"web policy Info activated successfully: {web_policy.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /web/policy/activate
        """)
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WebPolicy)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = WebPolicy(self.form_response_body(response.get_body()))
            else:
                result = WebPolicy()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    # @zcc_param_mapper
    def web_policy_edit(self, **kwargs) -> APIResult[dict]:
        """
        Adds or updates a policy or app profile for the company by platform
        (iOS, Android, Windows, macOS, and Linux).

        All keyword arguments below are optional. Field names mirror the
        snake_case attributes returned by ``WebPolicy.as_dict()`` and the
        nested model classes (``PolicyExtension``, ``DisasterRecovery``,
        ``WindowsPolicy``, ``MacOSPolicy``, ``LinuxPolicy``, ``IOSPolicy``,
        ``AndroidPolicy``, ``OnNetPolicy``, ``Users``, ``Groups``).

        Keyword Args:
            id (int): The unique identifier of the web policy.
            name (str): The name of the web policy.
            description (str): The description of the web policy.
            active (int): Whether the policy is active. ``0`` = inactive,
                ``1`` = active.
            device_type (str): The device operating system. Friendly names
                accepted by ``zcc_param_mapper``: ``ios``, ``android``,
                ``windows``, ``macos``, ``linux``. The API enum
                (``DEVICE_TYPE_WINDOWS``, ``DEVICE_TYPE_MACOS``, etc.) is
                also accepted.
            pac_url (str): The PAC URL applied by the policy.
            allow_unreachable_pac (bool): Whether traffic is allowed when
                the PAC file is unreachable.
            rule_order (int): Rule ordinal/priority of the policy.
            log_mode (int): Log mode (e.g. ``-1`` disabled, ``0`` info,
                ``3`` debug).
            log_level (int): Log verbosity level.
            log_file_size (int): Maximum log file size in MB.
            reauth_period (str): Re-authentication period (in hours).
            reactivate_web_security_minutes (str): Minutes after which Web
                Security is reactivated when disabled by the user.
            highlight_active_control (int): ``0`` or ``1``.
            send_disable_service_reason (int): ``0`` or ``1``.
            tunnel_zapp_traffic (int): ``0`` or ``1``.
            enable_device_groups (int): ``0`` or ``1``.
            forwarding_profile_id (int): Forwarding profile ID associated
                with the policy.
            group_all (int): ``0`` or ``1`` — whether the policy applies
                to all groups.
            zia_posture_config_id (int): ZIA Posture profile ID.
            app_identity_names (list[str]): App Identity names assigned to
                the policy.
            app_service_ids (list[str]): App Service IDs assigned to the
                policy.
            app_service_names (list[str]): App Service names assigned to
                the policy.
            bypass_app_ids (list[str]): App IDs to bypass.
            bypass_custom_app_ids (list[str]): Custom App IDs to bypass.
            device_group_ids (list[str]): Device Group IDs scoped to the
                policy.
            device_group_names (list[str]): Device Group names scoped to
                the policy.
            group_ids (list[int]): Group IDs scoped to the policy. The
                ZCC edit endpoint expects a **flat list of integer IDs**
                here — not the ZIA/ZPA-style ``[{"id": <id>}]`` wrapping.
                The corresponding response field, ``groups``, is returned
                as a fully-hydrated list of ``Groups`` objects (id, name,
                auth_type, active, last_modification) and is read-only —
                do not echo it back on the request.
            group_names (list[str]): Group names scoped to the policy
                (response-only metadata; safe to omit on update).
            user_ids (list[str]): User IDs scoped to the policy. The ZCC
                edit endpoint expects a **flat list of string IDs** here.
                The corresponding response field, ``users``, is returned
                as a list of ``Users`` objects (id, login_name,
                last_modification, active, company_id) and is read-only —
                do not echo it back on the request.
            user_names (list[str]): User names scoped to the policy
                (response-only metadata; safe to omit on update).

            windows_policy (dict): Windows-specific overrides. Fields:

                * ``cache_system_proxy`` (int)
                * ``disable_password`` (str)
                * ``disable_loop_back_restriction`` (int)
                * ``remove_exempted_containers`` (int)
                * ``disable_parallel_ipv4and_ipv6`` (int)
                * ``flow_logger_config`` (str)
                * ``domain_profile_detection_config`` (str)
                * ``all_inbound_traffic_config`` (str)
                * ``install_ssl_certs`` (int)
                * ``trigger_domain_profle_detection`` (int)
                * ``logout_password`` (str)
                * ``override_wpad`` (int)
                * ``pac_data_path`` (str)
                * ``pac_type`` (int)
                * ``prioritize_i_pv4`` (int)
                * ``restart_win_http_svc`` (int)
                * ``sccm_config`` (str)
                * ``uninstall_password`` (str)
                * ``wfp_driver`` (int)
                * ``captive_portal_config`` (str) — JSON-encoded string.
                * ``install_windows_firewall_inbound_rule`` (int)
                * ``force_location_refresh_sccm`` (int)

            mac_policy (dict): macOS-specific overrides. Fields:

                * ``add_ifscope_route`` (int)
                * ``cache_system_proxy`` (int)
                * ``clear_arp_cache`` (int)
                * ``disable_password`` (str)
                * ``dns_priority_ordering`` (list[str])
                * ``dns_priority_ordering_for_trusted_dns_criteria`` (list[str])
                * ``enable_application_based_bypass`` (int)
                * ``enable_zscaler_firewall`` (str)
                * ``install_certs`` (int)
                * ``logout_password`` (str)
                * ``persistent_zscaler_firewall`` (int)
                * ``uninstall_password`` (str)

            linux_policy (dict): Linux-specific overrides. Fields:

                * ``disable_password`` (str)
                * ``install_ssl_certs`` (int)
                * ``logout_password`` (str)
                * ``uninstall_password`` (str)

            ios_policy (dict): iOS-specific overrides. Fields:

                * ``disable_password`` (str)
                * ``logout_password`` (str)
                * ``uninstall_password`` (str)
                * ``ipv6_mode`` (int)
                * ``passcode`` (str)
                * ``show_vpn_tun_notification`` (int)

            android_policy (dict): Android-specific overrides. Fields:

                * ``allowed_apps`` (str)
                * ``billing_day`` (str)
                * ``bypass_android_apps`` (list[str])
                * ``bypass_mms_apps`` (int)
                * ``custom_text`` (str)
                * ``disable_password`` (str)
                * ``enable_verbose_log`` (int)
                * ``enforced`` (int)
                * ``install_certs`` (int)
                * ``limit`` (str)
                * ``logout_password`` (str)
                * ``quota_roaming`` (int)
                * ``uninstall_password`` (str)
                * ``wifissid`` (str)

            policy_extension (dict): Advanced policy extension settings.
                Fields:

                * ``id`` (int)
                * ``source_port_based_bypasses`` (str)
                * ``vpn_gateways`` (str)
                * ``packet_tunnel_exclude_list`` (str) — comma-separated CIDRs.
                * ``packet_tunnel_include_list`` (str) — comma-separated CIDRs.
                * ``packet_tunnel_dns_include_list`` (str)
                * ``packet_tunnel_dns_exclude_list`` (str)
                * ``packet_tunnel_exclude_list_for_ipv6`` (str)
                * ``packet_tunnel_include_list_for_ipv6`` (str)
                * ``nonce`` (str)
                * ``machine_idp_auth`` (bool)
                * ``exit_password`` (str)
                * ``use_v8_js_engine`` (str) — ``"0"`` or ``"1"``.
                * ``zdx_disable_password`` (str)
                * ``zd_disable_password`` (str)
                * ``zpa_disable_password`` (str)
                * ``zdp_disable_password`` (str)
                * ``follow_routing_table`` (str) — ``"0"`` or ``"1"``.
                * ``use_wsa_poll_for_zpa`` (str) — ``"0"`` or ``"1"``.
                * ``use_default_adapter_for_dns`` (str) — ``"0"`` or ``"1"``.
                * ``use_zscaler_notification_framework`` (str)
                * ``switch_focus_to_notification`` (str)
                * ``fallback_to_gateway_domain`` (str) — ``"0"`` or ``"1"``.
                * ``enable_zcc_revert`` (str) — ``"0"`` or ``"1"``.
                * ``zcc_revert_password`` (str)
                * ``zpa_auth_exp_on_sleep`` (int)
                * ``zpa_auth_exp_on_sys_restart`` (int)
                * ``zpa_auth_exp_on_net_ip_change`` (int)
                * ``zpa_auth_exp_on_win_logon_session`` (int)
                * ``zpa_auth_exp_on_win_session_lock`` (int)
                * ``zpa_auth_exp_session_lock_state_min_time_in_second`` (int)
                * ``enable_set_proxy_on_vpn_adapters`` (int)
                * ``disable_dns_route_exclusion`` (int)
                * ``advance_zpa_reauth`` (bool)
                * ``use_proxy_port_for_t1`` (str) — ``"0"`` or ``"1"``.
                * ``use_proxy_port_for_t2`` (str) — ``"0"`` or ``"1"``.
                * ``intercept_zia_traffic_all_adapters`` (str)
                * ``enable_anti_tampering`` (str)
                * ``override_at_cmd_by_policy`` (str)
                * ``reactivate_anti_tampering_time`` (int)
                * ``enforce_split_dns`` (int)
                * ``drop_quic_traffic`` (int)
                * ``enable_zdp_service`` (str) — ``"0"`` or ``"1"``.
                * ``update_dns_search_order`` (int)
                * ``truncate_large_udpdns_response`` (int)
                * ``prioritize_dns_exclusions`` (int)
                * ``purge_kerberos_preferred_dc_cache`` (str)
                * ``delete_dhcp_option121_routes`` (str) — JSON-encoded string.
                * ``generate_cli_password_contract`` (dict) — Fields:
                  ``policy_id`` (int), ``enable_cli`` (bool),
                  ``allow_zpa_disable_without_password`` (bool),
                  ``allow_zia_disable_without_password`` (bool),
                  ``allow_zdx_disable_without_password`` (bool).
                * ``zdx_lite_config_obj`` (str) — JSON-encoded string.
                * ``ddil_config`` (str) — JSON-encoded string.
                * ``zcc_fail_close_settings_exit_uninstall_password`` (str)
                * ``zcc_fail_close_settings_lockdown_on_tunnel_process_exit`` (int)
                * ``zcc_fail_close_settings_lockdown_on_firewall_error`` (int)
                * ``zcc_fail_close_settings_lockdown_on_driver_error`` (int)
                * ``zcc_fail_close_settings_thumb_print`` (str)
                * ``zcc_app_fail_open_policy`` (int)
                * ``zcc_tunnel_fail_policy`` (int)
                * ``follow_global_for_partner_login`` (str)
                * ``user_allowed_to_add_partner`` (str)
                * ``allow_client_cert_caching_for_web_view2`` (str)
                * ``show_confirmation_dialog_for_cached_cert`` (str)
                * ``enable_flow_based_tunnel`` (int)

            disaster_recovery (dict): Disaster Recovery configuration.
                Fields:

                * ``enable_zia_dr`` (bool)
                * ``enable_zpa_dr`` (bool)
                * ``zia_dr_method`` (int)
                * ``zia_custom_db_url`` (str)
                * ``use_zia_global_db`` (bool)
                * ``zia_global_db_url`` (str)
                * ``zia_global_db_urlv2`` (str)
                * ``zia_domain_name`` (str)
                * ``zia_rsa_pub_key_name`` (str)
                * ``zia_rsa_pub_key`` (str)
                * ``zpa_domain_name`` (str)
                * ``zpa_rsa_pub_key_name`` (str)
                * ``zpa_rsa_pub_key`` (str)
                * ``allow_zia_test`` (bool)
                * ``allow_zpa_test`` (bool)

            on_net_policy (dict): On-Net policy binding. Fields:

                * ``id`` (int)
                * ``name`` (str)
                * ``condition_type`` (int)
                * ``predefined_trusted_networks`` (bool)
                * ``predefined_tn_all`` (bool)

        Returns:
            tuple: A tuple containing the updated Web Policy, response,
            and error.

        Examples:
            Update a Windows policy by passing each field as a keyword
            argument. The API consumes flat ``group_ids`` / ``user_ids``
            lists on the request, but populates nested ``groups`` and
            ``users`` arrays on the response — do not echo those nested
            arrays back on update.

            >>> updated, _, err = client.zcc.web_policy.web_policy_edit(
            ...     name="test",
            ...     device_type=3,
            ...     rule_order=1,
            ...     active="1",
            ...     description="",
            ...     group_ids=[62718389, 62718428, 62718420],
            ...     user_ids=["5807211"],
            ...     log_mode=-1,
            ...     log_level=0,
            ...     log_file_size=100,
            ...     reauth_period=8,
            ...     install_ssl_certs=1,
            ...     packet_tunnel_include_list=["0.0.0.0/0"],
            ...     packet_tunnel_exclude_list=[
            ...         "10.0.0.0/8",
            ...         "172.16.0.0/12",
            ...         "192.168.0.0/16",
            ...     ],
            ...     policy_extension={
            ...         "exit_password": "",
            ...         "follow_routing_table": "1",
            ...         "use_default_adapter_for_dns": "1",
            ...         "enforce_split_dns": 0,
            ...         "drop_quic_traffic": 0,
            ...         "use_v8_js_engine": "1",
            ...     },
            ...     windows_policy={
            ...         "install_ssl_certs": 1,
            ...         "install_windows_firewall_inbound_rule": "1",
            ...         "captive_portal_url_id": 1,
            ...     },
            ...     disaster_recovery={
            ...         "enable_zia_dr": False,
            ...         "enable_zpa_dr": False,
            ...         "zia_dr_method": 2,
            ...     },
            ... )
            >>> if err:
            ...     print(f"Error updating policy: {err}")
            ...     return
            ... print(f"Updated policy: {updated.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /web/policy/edit
        """)

        body = kwargs

        body = zcc_to_wire(body, WebPolicy)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WebPolicy)
        if error:
            return (None, response, error)

        try:
            result = WebPolicy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_web_policy(self, policy_id: int) -> APIResult[dict]:
        """
        Deletes the specified Web Policy.

        Args:
            policy_id (str): The unique identifier of the  Web Policy.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Web Policy:

            >>> _, _, error = client.zcc.web_policy.delete_web_policy('205187')
            >>> if error:
            ...     print(f"Error deleting Web Policy: {error}")
            ...     return
            ... print(f"Web Policy with ID {'205187' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /web/policy/{policy_id}/delete
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
