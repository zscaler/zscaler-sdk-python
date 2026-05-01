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

from typing import Any, Dict, List, Optional
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class CompanyInfo(ZscalerObject):
    """
    A class for CompanyInfo objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the CompanyInfo model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.org_id: Optional[Any] = config["orgId"] if "orgId" in config else None
            self.master_customer_id: Optional[Any] = config["masterCustomerId"] if "masterCustomerId" in config else None
            self.name: Optional[Any] = config["name"] if "name" in config else None
            self.business_name: Optional[Any] = config["businessName"] if "businessName" in config else None
            self.business_contact_number: Optional[Any] = (
                config["businessContactNumber"] if "businessContactNumber" in config else None
            )
            self.activation_recipient: Optional[Any] = (
                config["activationRecipient"] if "activationRecipient" in config else None
            )
            self.activation_copy: Optional[Any] = config["activationCopy"] if "activationCopy" in config else None
            self.mdm_status: Optional[Any] = config["mdmStatus"] if "mdmStatus" in config else None
            self.send_email: Optional[Any] = config["sendEmail"] if "sendEmail" in config else None
            self.proxy_enabled: Optional[Any] = config["proxyEnabled"] if "proxyEnabled" in config else None
            self.zpn_enabled: Optional[Any] = config["zpnEnabled"] if "zpnEnabled" in config else None
            self.upm_enabled: Optional[Any] = config["upmEnabled"] if "upmEnabled" in config else None
            self.zad_enabled: Optional[Any] = config["zadEnabled"] if "zadEnabled" in config else None
            self.enable_deception_for_all: Optional[Any] = (
                config["enableDeceptionForAll"] if "enableDeceptionForAll" in config else None
            )
            self.dlp_enabled: Optional[Any] = config["dlpEnabled"] if "dlpEnabled" in config else None
            self.tunnel_protocol_type: Optional[Any] = config["tunnelProtocolType"] if "tunnelProtocolType" in config else None
            self.secure_agent_basic: Optional[Any] = config["secureAgentBasic"] if "secureAgentBasic" in config else None
            self.secure_agent_advanced: Optional[Any] = (
                config["secureAgentAdvanced"] if "secureAgentAdvanced" in config else None
            )
            self.support_admin_email: Optional[Any] = config["supportAdminEmail"] if "supportAdminEmail" in config else None
            self.support_enabled: Optional[Any] = config["supportEnabled"] if "supportEnabled" in config else None
            self.fetch_logs_for_admins_enabled: Optional[Any] = (
                config["fetchLogsForAdminsEnabled"] if "fetchLogsForAdminsEnabled" in config else None
            )
            self.enable_rectify_utils: Optional[Any] = config["enableRectifyUtils"] if "enableRectifyUtils" in config else None
            self.support_ticket_enabled: Optional[Any] = (
                config["supportTicketEnabled"] if "supportTicketEnabled" in config else None
            )
            self.disable_logging_controls: Optional[Any] = (
                config["disableLoggingControls"] if "disableLoggingControls" in config else None
            )
            self.default_auth_type: Optional[Any] = config["defaultAuthType"] if "defaultAuthType" in config else None
            self.version: Optional[Any] = config["version"] if "version" in config else None
            self.policy_activation_required: Optional[Any] = (
                config["policyActivationRequired"] if "policyActivationRequired" in config else None
            )
            self.enable_autofill_username: Optional[Any] = (
                config["enableAutofillUsername"] if "enableAutofillUsername" in config else None
            )
            self.auto_fill_using_login_hint: Optional[Any] = (
                config["autoFillUsingLoginHint"] if "autoFillUsingLoginHint" in config else None
            )
            self.dc_service_read_only: Optional[Any] = config["dcServiceReadOnly"] if "dcServiceReadOnly" in config else None
            self.enable_tunnel_zapp_traffic_toggle: Optional[Any] = (
                config["enableTunnelZappTrafficToggle"] if "enableTunnelZappTrafficToggle" in config else None
            )
            self.machine_idp_auth: Optional[Any] = config["machineIdpAuth"] if "machineIdpAuth" in config else None
            self.linux_visibility: Optional[Any] = config["linuxVisibility"] if "linuxVisibility" in config else None
            self.registry_path_for_pac: Optional[Any] = (
                config["registryPathForPac"] if "registryPathForPac" in config else None
            )
            self.use_pollset_for_socket_reactor: Optional[Any] = (
                config["usePollsetForSocketReactor"] if "usePollsetForSocketReactor" in config else None
            )
            self.enable_dtls_for_zpa: Optional[Any] = config["enableDtlsForZpa"] if "enableDtlsForZpa" in config else None
            self.use_v8_js_engine: Optional[Any] = config["useV8JsEngine"] if "useV8JsEngine" in config else None
            self.disable_parallel_ipv4_and_i_pv6: Optional[Any] = (
                config["disableParallelIpv4AndIPv6"] if "disableParallelIpv4AndIPv6" in config else None
            )
            self.send64_bit_build: Optional[Any] = config["send64BitBuild"] if "send64BitBuild" in config else None
            self.use_add_ifscope_route: Optional[Any] = (
                config["useAddIfscopeRoute"] if "useAddIfscopeRoute" in config else None
            )
            self.use_clear_arp_cache: Optional[Any] = config["useClearArpCache"] if "useClearArpCache" in config else None
            self.use_dns_priority_ordering: Optional[Any] = (
                config["useDnsPriorityOrdering"] if "useDnsPriorityOrdering" in config else None
            )
            self.enable_browser_auth: Optional[Any] = config["enableBrowserAuth"] if "enableBrowserAuth" in config else None
            self.enable_public_api: Optional[Any] = config["enablePublicAPI"] if "enablePublicAPI" in config else None
            self.disable_reason_visibility: Optional[Any] = (
                config["disableReasonVisibility"] if "disableReasonVisibility" in config else None
            )
            self.follow_routing_table: Optional[Any] = config["followRoutingTable"] if "followRoutingTable" in config else None
            self.use_default_adapter_for_dns: Optional[Any] = (
                config["useDefaultAdapterForDNS"] if "useDefaultAdapterForDNS" in config else None
            )
            self.enable_minimum_device_cleanup_as_one: Optional[Any] = (
                config["enableMinimumDeviceCleanupAsOne"] if "enableMinimumDeviceCleanupAsOne" in config else None
            )
            self.dns_priority_ordering_for_trusted_dns_criteria: Optional[Any] = (
                config["dnsPriorityOrderingForTrustedDnsCriteria"]
                if "dnsPriorityOrderingForTrustedDnsCriteria" in config
                else None
            )
            self.machine_tunnel_posture: Optional[Any] = (
                config["machineTunnelPosture"] if "machineTunnelPosture" in config else None
            )
            self.zpa_partner_login: Optional[Any] = config["zpaPartnerLogin"] if "zpaPartnerLogin" in config else None
            self.proxy_port: Optional[Any] = config["proxyPort"] if "proxyPort" in config else None
            self.dns_cache_ttl_windows: Optional[Any] = (
                config["dnsCacheTtlWindows"] if "dnsCacheTtlWindows" in config else None
            )
            self.dns_cache_ttl_mac: Optional[Any] = config["dnsCacheTtlMac"] if "dnsCacheTtlMac" in config else None
            self.dns_cache_ttl_android: Optional[Any] = (
                config["dnsCacheTtlAndroid"] if "dnsCacheTtlAndroid" in config else None
            )
            self.dns_cache_ttl_ios: Optional[Any] = config["dnsCacheTtlIos"] if "dnsCacheTtlIos" in config else None
            self.dns_cache_ttl_linux: Optional[Any] = config["dnsCacheTtlLinux"] if "dnsCacheTtlLinux" in config else None
            self.zpa_client_cert_exp_in_days: Optional[Any] = (
                config["zpaClientCertExpInDays"] if "zpaClientCertExpInDays" in config else None
            )
            self.enable_flow_logger: Optional[Any] = config["enableFlowLogger"] if "enableFlowLogger" in config else None
            self.flow_logging_buffer_limit: Optional[Any] = (
                config["flowLoggingBufferLimit"] if "flowLoggingBufferLimit" in config else None
            )
            self.flow_logging_time_interval: Optional[Any] = (
                config["flowLoggingTimeInterval"] if "flowLoggingTimeInterval" in config else None
            )
            self.posture_based_service: Optional[Any] = (
                config["postureBasedService"] if "postureBasedService" in config else None
            )
            self.enable_posture_based_profile: Optional[Any] = (
                config["enablePostureBasedProfile"] if "enablePostureBasedProfile" in config else None
            )
            self.disaster_recovery: Optional[Any] = config["disasterRecovery"] if "disasterRecovery" in config else None
            self.zia_global_db_url_for_dr: Optional[Any] = (
                config["ziaGlobalDbUrlForDR"] if "ziaGlobalDbUrlForDR" in config else None
            )
            self.enable_react_ui: Optional[Any] = config["enableReactUI"] if "enableReactUI" in config else None
            self.launch_react_u_iby_default: Optional[Any] = (
                config["launchReactUIbyDefault"] if "launchReactUIbyDefault" in config else None
            )
            self.dlp_notification: Optional[Any] = config["dlpNotification"] if "dlpNotification" in config else None
            self.vpn_gateway_char_limit: Optional[Any] = (
                config["vpnGatewayCharLimit"] if "vpnGatewayCharLimit" in config else None
            )
            self.device_groups_count: Optional[Any] = config["deviceGroupsCount"] if "deviceGroupsCount" in config else None
            self.vpn_bypass_refresh_interval: Optional[Any] = (
                config["vpnBypassRefreshInterval"] if "vpnBypassRefreshInterval" in config else None
            )
            self.dest_include_exclude_char_limit: Optional[Any] = (
                config["destIncludeExcludeCharLimit"] if "destIncludeExcludeCharLimit" in config else None
            )
            self.ip_v6_support_for_tunnel2: Optional[Any] = (
                config["ipV6SupportForTunnel2"] if "ipV6SupportForTunnel2" in config else None
            )
            self.dest_include_exclude_char_limit_for_ipv6: Optional[Any] = (
                config["destIncludeExcludeCharLimitForIpv6"] if "destIncludeExcludeCharLimitForIpv6" in config else None
            )
            self.enable_set_proxy_on_vpn_adapters: Optional[Any] = (
                config["enableSetProxyOnVPNAdapters"] if "enableSetProxyOnVPNAdapters" in config else None
            )
            self.disable_dns_route_exclusion: Optional[Any] = (
                config["disableDNSRouteExclusion"] if "disableDNSRouteExclusion" in config else None
            )
            self.show_vpn_tun_notification: Optional[Any] = (
                config["showVPNTunNotification"] if "showVPNTunNotification" in config else None
            )
            self.add_app_bypass_to_vpn_gateway: Optional[Any] = (
                config["addAppBypassToVPNGateway"] if "addAppBypassToVPNGateway" in config else None
            )
            self.enable_zscaler_firewall: Optional[Any] = (
                config["enableZscalerFirewall"] if "enableZscalerFirewall" in config else None
            )
            self.persistent_zscaler_firewall: Optional[Any] = (
                config["persistentZscalerFirewall"] if "persistentZscalerFirewall" in config else None
            )
            self.clear_mup_cache: Optional[Any] = config["clearMupCache"] if "clearMupCache" in config else None
            self.execute_gpo_update: Optional[Any] = config["executeGpoUpdate"] if "executeGpoUpdate" in config else None
            self.enable_port_based_zpa_filter: Optional[Any] = (
                config["enablePortBasedZPAFilter"] if "enablePortBasedZPAFilter" in config else None
            )
            self.enable_anti_tampering: Optional[Any] = (
                config["enableAntiTampering"] if "enableAntiTampering" in config else None
            )
            self.zpa_reauth_enabled: Optional[Any] = config["zpaReauthEnabled"] if "zpaReauthEnabled" in config else None
            self.zpa_auto_reauth_timeout: Optional[Any] = (
                config["zpaAutoReauthTimeout"] if "zpaAutoReauthTimeout" in config else None
            )
            self.enable_zpa_auth_user_name: Optional[Any] = (
                config["enableZpaAuthUserName"] if "enableZpaAuthUserName" in config else None
            )
            self.enable_global_zcc_telemetry: Optional[Any] = (
                config["enableGlobalZCCTelemetry"] if "enableGlobalZCCTelemetry" in config else None
            )
            self.configure_tunnel2fallback_for_zia: Optional[Any] = (
                config["configureTunnel2fallbackForZia"] if "configureTunnel2fallbackForZia" in config else None
            )
            if "webAppConfig" in config:
                if isinstance(config["webAppConfig"], WebAppConfig):
                    self.web_app_config: Optional[WebAppConfig] = config["webAppConfig"]
                elif config["webAppConfig"] is not None:
                    self.web_app_config = WebAppConfig(config["webAppConfig"])
                else:
                    self.web_app_config = None
            else:
                self.web_app_config: Optional[WebAppConfig] = None
            self.enable_install_web_view2: Optional[Any] = (
                config["enableInstallWebView2"] if "enableInstallWebView2" in config else None
            )
            self.enable_custom_proxy_ports: Optional[Any] = (
                config["enableCustomProxyPorts"] if "enableCustomProxyPorts" in config else None
            )
            self.intercept_zia_traffic_all_adapters: Optional[Any] = (
                config["interceptZIATrafficAllAdapters"] if "interceptZIATrafficAllAdapters" in config else None
            )
            self.swagger_link: Optional[Any] = config["swaggerLink"] if "swaggerLink" in config else None
            self.enable_one_id_admin: Optional[Any] = config["enableOneIdAdmin"] if "enableOneIdAdmin" in config else None
            self.enable_one_id_user: Optional[Any] = config["enableOneIdUser"] if "enableOneIdUser" in config else None
            self.restrict_admin_access: Optional[Any] = (
                config["restrictAdminAccess"] if "restrictAdminAccess" in config else None
            )
            self.enable_zia_user_department_sync: Optional[Any] = (
                config["enableZiaUserDepartmentSync"] if "enableZiaUserDepartmentSync" in config else None
            )
            self.enable_udp_transport_selection: Optional[Any] = (
                config["enableUDPTransportSelection"] if "enableUDPTransportSelection" in config else None
            )
            self.compute_device_groups_for_zia: Optional[Any] = (
                config["computeDeviceGroupsForZIA"] if "computeDeviceGroupsForZIA" in config else None
            )
            self.compute_device_groups_for_zpa: Optional[Any] = (
                config["computeDeviceGroupsForZPA"] if "computeDeviceGroupsForZPA" in config else None
            )
            self.compute_device_groups_for_zdx: Optional[Any] = (
                config["computeDeviceGroupsForZDX"] if "computeDeviceGroupsForZDX" in config else None
            )
            self.compute_device_groups_for_zad: Optional[Any] = (
                config["computeDeviceGroupsForZAD"] if "computeDeviceGroupsForZAD" in config else None
            )
            self.use_tunnel2_sme_for_tunnel1: Optional[Any] = (
                config["useTunnel2SmeForTunnel1"] if "useTunnel2SmeForTunnel1" in config else None
            )
            self.ma_cloud_name: Optional[Any] = config["maCloudName"] if "maCloudName" in config else None
            self.zia_cloud_name: Optional[Any] = config["ziaCloudName"] if "ziaCloudName" in config else None
            self.zt2_health_probe_interval: Optional[Any] = (
                config["zt2HealthProbeInterval"] if "zt2HealthProbeInterval" in config else None
            )
            self.device_posture_frequency: List[DevicePostureFrequency] = ZscalerCollection.form_list(
                config["devicePostureFrequency"] if "devicePostureFrequency" in config else [], DevicePostureFrequency
            )
            self.zdx_manual_rollout: Optional[Any] = config["zdxManualRollout"] if "zdxManualRollout" in config else None
            self.win_zdx_lite_enabled: Optional[Any] = config["winZdxLiteEnabled"] if "winZdxLiteEnabled" in config else None
            self.telemetry_default: Optional[Any] = config["telemetryDefault"] if "telemetryDefault" in config else None
        else:
            self.org_id: Optional[Any] = None
            self.master_customer_id: Optional[Any] = None
            self.name: Optional[Any] = None
            self.business_name: Optional[Any] = None
            self.business_contact_number: Optional[Any] = None
            self.activation_recipient: Optional[Any] = None
            self.activation_copy: Optional[Any] = None
            self.mdm_status: Optional[Any] = None
            self.send_email: Optional[Any] = None
            self.proxy_enabled: Optional[Any] = None
            self.zpn_enabled: Optional[Any] = None
            self.upm_enabled: Optional[Any] = None
            self.zad_enabled: Optional[Any] = None
            self.enable_deception_for_all: Optional[Any] = None
            self.dlp_enabled: Optional[Any] = None
            self.tunnel_protocol_type: Optional[Any] = None
            self.secure_agent_basic: Optional[Any] = None
            self.secure_agent_advanced: Optional[Any] = None
            self.support_admin_email: Optional[Any] = None
            self.support_enabled: Optional[Any] = None
            self.fetch_logs_for_admins_enabled: Optional[Any] = None
            self.enable_rectify_utils: Optional[Any] = None
            self.support_ticket_enabled: Optional[Any] = None
            self.disable_logging_controls: Optional[Any] = None
            self.default_auth_type: Optional[Any] = None
            self.version: Optional[Any] = None
            self.policy_activation_required: Optional[Any] = None
            self.enable_autofill_username: Optional[Any] = None
            self.auto_fill_using_login_hint: Optional[Any] = None
            self.dc_service_read_only: Optional[Any] = None
            self.enable_tunnel_zapp_traffic_toggle: Optional[Any] = None
            self.machine_idp_auth: Optional[Any] = None
            self.linux_visibility: Optional[Any] = None
            self.registry_path_for_pac: Optional[Any] = None
            self.use_pollset_for_socket_reactor: Optional[Any] = None
            self.enable_dtls_for_zpa: Optional[Any] = None
            self.use_v8_js_engine: Optional[Any] = None
            self.disable_parallel_ipv4_and_i_pv6: Optional[Any] = None
            self.send64_bit_build: Optional[Any] = None
            self.use_add_ifscope_route: Optional[Any] = None
            self.use_clear_arp_cache: Optional[Any] = None
            self.use_dns_priority_ordering: Optional[Any] = None
            self.enable_browser_auth: Optional[Any] = None
            self.enable_public_api: Optional[Any] = None
            self.disable_reason_visibility: Optional[Any] = None
            self.follow_routing_table: Optional[Any] = None
            self.use_default_adapter_for_dns: Optional[Any] = None
            self.enable_minimum_device_cleanup_as_one: Optional[Any] = None
            self.dns_priority_ordering_for_trusted_dns_criteria: Optional[Any] = None
            self.machine_tunnel_posture: Optional[Any] = None
            self.zpa_partner_login: Optional[Any] = None
            self.proxy_port: Optional[Any] = None
            self.dns_cache_ttl_windows: Optional[Any] = None
            self.dns_cache_ttl_mac: Optional[Any] = None
            self.dns_cache_ttl_android: Optional[Any] = None
            self.dns_cache_ttl_ios: Optional[Any] = None
            self.dns_cache_ttl_linux: Optional[Any] = None
            self.zpa_client_cert_exp_in_days: Optional[Any] = None
            self.enable_flow_logger: Optional[Any] = None
            self.flow_logging_buffer_limit: Optional[Any] = None
            self.flow_logging_time_interval: Optional[Any] = None
            self.posture_based_service: Optional[Any] = None
            self.enable_posture_based_profile: Optional[Any] = None
            self.disaster_recovery: Optional[Any] = None
            self.zia_global_db_url_for_dr: Optional[Any] = None
            self.enable_react_ui: Optional[Any] = None
            self.launch_react_u_iby_default: Optional[Any] = None
            self.dlp_notification: Optional[Any] = None
            self.vpn_gateway_char_limit: Optional[Any] = None
            self.device_groups_count: Optional[Any] = None
            self.vpn_bypass_refresh_interval: Optional[Any] = None
            self.dest_include_exclude_char_limit: Optional[Any] = None
            self.ip_v6_support_for_tunnel2: Optional[Any] = None
            self.dest_include_exclude_char_limit_for_ipv6: Optional[Any] = None
            self.enable_set_proxy_on_vpn_adapters: Optional[Any] = None
            self.disable_dns_route_exclusion: Optional[Any] = None
            self.show_vpn_tun_notification: Optional[Any] = None
            self.add_app_bypass_to_vpn_gateway: Optional[Any] = None
            self.enable_zscaler_firewall: Optional[Any] = None
            self.persistent_zscaler_firewall: Optional[Any] = None
            self.clear_mup_cache: Optional[Any] = None
            self.execute_gpo_update: Optional[Any] = None
            self.enable_port_based_zpa_filter: Optional[Any] = None
            self.enable_anti_tampering: Optional[Any] = None
            self.zpa_reauth_enabled: Optional[Any] = None
            self.zpa_auto_reauth_timeout: Optional[Any] = None
            self.enable_zpa_auth_user_name: Optional[Any] = None
            self.enable_global_zcc_telemetry: Optional[Any] = None
            self.configure_tunnel2fallback_for_zia: Optional[Any] = None
            self.web_app_config: Optional[WebAppConfig] = None
            self.enable_install_web_view2: Optional[Any] = None
            self.enable_custom_proxy_ports: Optional[Any] = None
            self.intercept_zia_traffic_all_adapters: Optional[Any] = None
            self.swagger_link: Optional[Any] = None
            self.enable_one_id_admin: Optional[Any] = None
            self.enable_one_id_user: Optional[Any] = None
            self.restrict_admin_access: Optional[Any] = None
            self.enable_zia_user_department_sync: Optional[Any] = None
            self.enable_udp_transport_selection: Optional[Any] = None
            self.compute_device_groups_for_zia: Optional[Any] = None
            self.compute_device_groups_for_zpa: Optional[Any] = None
            self.compute_device_groups_for_zdx: Optional[Any] = None
            self.compute_device_groups_for_zad: Optional[Any] = None
            self.use_tunnel2_sme_for_tunnel1: Optional[Any] = None
            self.ma_cloud_name: Optional[Any] = None
            self.zia_cloud_name: Optional[Any] = None
            self.zt2_health_probe_interval: Optional[Any] = None
            self.device_posture_frequency: List[DevicePostureFrequency] = []
            self.zdx_manual_rollout: Optional[Any] = None
            self.win_zdx_lite_enabled: Optional[Any] = None
            self.telemetry_default: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "orgId": self.org_id,
            "masterCustomerId": self.master_customer_id,
            "name": self.name,
            "businessName": self.business_name,
            "businessContactNumber": self.business_contact_number,
            "activationRecipient": self.activation_recipient,
            "activationCopy": self.activation_copy,
            "mdmStatus": self.mdm_status,
            "sendEmail": self.send_email,
            "proxyEnabled": self.proxy_enabled,
            "zpnEnabled": self.zpn_enabled,
            "upmEnabled": self.upm_enabled,
            "zadEnabled": self.zad_enabled,
            "enableDeceptionForAll": self.enable_deception_for_all,
            "dlpEnabled": self.dlp_enabled,
            "tunnelProtocolType": self.tunnel_protocol_type,
            "secureAgentBasic": self.secure_agent_basic,
            "secureAgentAdvanced": self.secure_agent_advanced,
            "supportAdminEmail": self.support_admin_email,
            "supportEnabled": self.support_enabled,
            "fetchLogsForAdminsEnabled": self.fetch_logs_for_admins_enabled,
            "enableRectifyUtils": self.enable_rectify_utils,
            "supportTicketEnabled": self.support_ticket_enabled,
            "disableLoggingControls": self.disable_logging_controls,
            "defaultAuthType": self.default_auth_type,
            "version": self.version,
            "policyActivationRequired": self.policy_activation_required,
            "enableAutofillUsername": self.enable_autofill_username,
            "autoFillUsingLoginHint": self.auto_fill_using_login_hint,
            "dcServiceReadOnly": self.dc_service_read_only,
            "enableTunnelZappTrafficToggle": self.enable_tunnel_zapp_traffic_toggle,
            "machineIdpAuth": self.machine_idp_auth,
            "linuxVisibility": self.linux_visibility,
            "registryPathForPac": self.registry_path_for_pac,
            "usePollsetForSocketReactor": self.use_pollset_for_socket_reactor,
            "enableDtlsForZpa": self.enable_dtls_for_zpa,
            "useV8JsEngine": self.use_v8_js_engine,
            "disableParallelIpv4AndIPv6": self.disable_parallel_ipv4_and_i_pv6,
            "send64BitBuild": self.send64_bit_build,
            "useAddIfscopeRoute": self.use_add_ifscope_route,
            "useClearArpCache": self.use_clear_arp_cache,
            "useDnsPriorityOrdering": self.use_dns_priority_ordering,
            "enableBrowserAuth": self.enable_browser_auth,
            "enablePublicAPI": self.enable_public_api,
            "disableReasonVisibility": self.disable_reason_visibility,
            "followRoutingTable": self.follow_routing_table,
            "useDefaultAdapterForDNS": self.use_default_adapter_for_dns,
            "enableMinimumDeviceCleanupAsOne": self.enable_minimum_device_cleanup_as_one,
            "dnsPriorityOrderingForTrustedDnsCriteria": self.dns_priority_ordering_for_trusted_dns_criteria,
            "machineTunnelPosture": self.machine_tunnel_posture,
            "zpaPartnerLogin": self.zpa_partner_login,
            "proxyPort": self.proxy_port,
            "dnsCacheTtlWindows": self.dns_cache_ttl_windows,
            "dnsCacheTtlMac": self.dns_cache_ttl_mac,
            "dnsCacheTtlAndroid": self.dns_cache_ttl_android,
            "dnsCacheTtlIos": self.dns_cache_ttl_ios,
            "dnsCacheTtlLinux": self.dns_cache_ttl_linux,
            "zpaClientCertExpInDays": self.zpa_client_cert_exp_in_days,
            "enableFlowLogger": self.enable_flow_logger,
            "flowLoggingBufferLimit": self.flow_logging_buffer_limit,
            "flowLoggingTimeInterval": self.flow_logging_time_interval,
            "postureBasedService": self.posture_based_service,
            "enablePostureBasedProfile": self.enable_posture_based_profile,
            "disasterRecovery": self.disaster_recovery,
            "ziaGlobalDbUrlForDR": self.zia_global_db_url_for_dr,
            "enableReactUI": self.enable_react_ui,
            "launchReactUIbyDefault": self.launch_react_u_iby_default,
            "dlpNotification": self.dlp_notification,
            "vpnGatewayCharLimit": self.vpn_gateway_char_limit,
            "deviceGroupsCount": self.device_groups_count,
            "vpnBypassRefreshInterval": self.vpn_bypass_refresh_interval,
            "destIncludeExcludeCharLimit": self.dest_include_exclude_char_limit,
            "ipV6SupportForTunnel2": self.ip_v6_support_for_tunnel2,
            "destIncludeExcludeCharLimitForIpv6": self.dest_include_exclude_char_limit_for_ipv6,
            "enableSetProxyOnVPNAdapters": self.enable_set_proxy_on_vpn_adapters,
            "disableDNSRouteExclusion": self.disable_dns_route_exclusion,
            "showVPNTunNotification": self.show_vpn_tun_notification,
            "addAppBypassToVPNGateway": self.add_app_bypass_to_vpn_gateway,
            "enableZscalerFirewall": self.enable_zscaler_firewall,
            "persistentZscalerFirewall": self.persistent_zscaler_firewall,
            "clearMupCache": self.clear_mup_cache,
            "executeGpoUpdate": self.execute_gpo_update,
            "enablePortBasedZPAFilter": self.enable_port_based_zpa_filter,
            "enableAntiTampering": self.enable_anti_tampering,
            "zpaReauthEnabled": self.zpa_reauth_enabled,
            "zpaAutoReauthTimeout": self.zpa_auto_reauth_timeout,
            "enableZpaAuthUserName": self.enable_zpa_auth_user_name,
            "enableGlobalZCCTelemetry": self.enable_global_zcc_telemetry,
            "configureTunnel2fallbackForZia": self.configure_tunnel2fallback_for_zia,
            "webAppConfig": self.web_app_config,
            "enableInstallWebView2": self.enable_install_web_view2,
            "enableCustomProxyPorts": self.enable_custom_proxy_ports,
            "interceptZIATrafficAllAdapters": self.intercept_zia_traffic_all_adapters,
            "swaggerLink": self.swagger_link,
            "enableOneIdAdmin": self.enable_one_id_admin,
            "enableOneIdUser": self.enable_one_id_user,
            "restrictAdminAccess": self.restrict_admin_access,
            "enableZiaUserDepartmentSync": self.enable_zia_user_department_sync,
            "enableUDPTransportSelection": self.enable_udp_transport_selection,
            "computeDeviceGroupsForZIA": self.compute_device_groups_for_zia,
            "computeDeviceGroupsForZPA": self.compute_device_groups_for_zpa,
            "computeDeviceGroupsForZDX": self.compute_device_groups_for_zdx,
            "computeDeviceGroupsForZAD": self.compute_device_groups_for_zad,
            "useTunnel2SmeForTunnel1": self.use_tunnel2_sme_for_tunnel1,
            "maCloudName": self.ma_cloud_name,
            "ziaCloudName": self.zia_cloud_name,
            "zt2HealthProbeInterval": self.zt2_health_probe_interval,
            "devicePostureFrequency": self.device_posture_frequency,
            "zdxManualRollout": self.zdx_manual_rollout,
            "winZdxLiteEnabled": self.win_zdx_lite_enabled,
            "telemetryDefault": self.telemetry_default,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DevicePostureFrequency(ZscalerObject):
    """
    A class for DevicePostureFrequency objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the DevicePostureFrequency model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.posture_id: Optional[Any] = config["postureId"] if "postureId" in config else None
            self.posture_name: Optional[Any] = config["postureName"] if "postureName" in config else None
            self.ios_value: Optional[Any] = config["iosValue"] if "iosValue" in config else None
            self.android_value: Optional[Any] = config["androidValue"] if "androidValue" in config else None
            self.windows_value: Optional[Any] = config["windowsValue"] if "windowsValue" in config else None
            self.mac_value: Optional[Any] = config["macValue"] if "macValue" in config else None
            self.linux_value: Optional[Any] = config["linuxValue"] if "linuxValue" in config else None
            self.default_value: Optional[Any] = config["defaultValue"] if "defaultValue" in config else None
        else:
            self.posture_id: Optional[Any] = None
            self.posture_name: Optional[Any] = None
            self.ios_value: Optional[Any] = None
            self.android_value: Optional[Any] = None
            self.windows_value: Optional[Any] = None
            self.mac_value: Optional[Any] = None
            self.linux_value: Optional[Any] = None
            self.default_value: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "postureId": self.posture_id,
            "postureName": self.posture_name,
            "iosValue": self.ios_value,
            "androidValue": self.android_value,
            "windowsValue": self.windows_value,
            "macValue": self.mac_value,
            "linuxValue": self.linux_value,
            "defaultValue": self.default_value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class WebAppConfig(ZscalerObject):
    """
    A class for WebAppConfig objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the WebAppConfig model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.enable_fips_mode: Optional[Any] = config["enableFipsMode"] if "enableFipsMode" in config else None
            self.device_cleanup: Optional[Any] = config["deviceCleanup"] if "deviceCleanup" in config else None
            self.sync_time_hours: Optional[Any] = config["syncTimeHours"] if "syncTimeHours" in config else None
            self.hide_non_fed_settings: Optional[Any] = (
                config["hideNonFedSettings"] if "hideNonFedSettings" in config else None
            )
            self.hide_audit_logs: Optional[Any] = config["hideAuditLogs"] if "hideAuditLogs" in config else None
            self.activate_policy: Optional[Any] = config["activatePolicy"] if "activatePolicy" in config else None
            self.trusted_network: Optional[Any] = config["trustedNetwork"] if "trustedNetwork" in config else None
            self.process_postures: Optional[Any] = config["processPostures"] if "processPostures" in config else None
            self.zpa_reauth: Optional[Any] = config["zpaReauth"] if "zpaReauth" in config else None
            self.inactive_device_cleanup: Optional[Any] = (
                config["inactiveDeviceCleanup"] if "inactiveDeviceCleanup" in config else None
            )
            self.zpa_auth_username: Optional[Any] = config["zpaAuthUsername"] if "zpaAuthUsername" in config else None
            self.machine_tunnel: Optional[Any] = config["machineTunnel"] if "machineTunnel" in config else None
            self.cache_system_proxy: Optional[Any] = config["cacheSystemProxy"] if "cacheSystemProxy" in config else None
            self.hide_dtls_support_settings: Optional[Any] = (
                config["hideDTLSSupportSettings"] if "hideDTLSSupportSettings" in config else None
            )
            self.machine_token: Optional[Any] = config["machineToken"] if "machineToken" in config else None
            self.application_bypass_info: Optional[Any] = (
                config["applicationBypassInfo"] if "applicationBypassInfo" in config else None
            )
            self.tunnel_two_for_android_devices: Optional[Any] = (
                config["tunnelTwoForAndroidDevices"] if "tunnelTwoForAndroidDevices" in config else None
            )
            self.tunnel_two_fori_os_devices: Optional[Any] = (
                config["tunnelTwoForiOSDevices"] if "tunnelTwoForiOSDevices" in config else None
            )
            self.ownership_variable_posture: Optional[Any] = (
                config["ownershipVariablePosture"] if "ownershipVariablePosture" in config else None
            )
            self.block_unreachable_domains_traffic_flag: Optional[Any] = (
                config["blockUnreachableDomainsTrafficFlag"] if "blockUnreachableDomainsTrafficFlag" in config else None
            )
            self.prioritize_i_pv4_over_ipv6: Optional[Any] = (
                config["prioritizeIPv4OverIpv6"] if "prioritizeIPv4OverIpv6" in config else None
            )
            self.crowd_strike_zta_score_visibility: Optional[Any] = (
                config["crowdStrikeZTAScoreVisibility"] if "crowdStrikeZTAScoreVisibility" in config else None
            )
            self.notification_for_zpa_reauth_visibility: Optional[Any] = (
                config["notificationForZPAReauthVisibility"] if "notificationForZPAReauthVisibility" in config else None
            )
            self.crl_check_visibility_flag: Optional[Any] = (
                config["crlCheckVisibilityFlag"] if "crlCheckVisibilityFlag" in config else None
            )
            self.dedicated_proxy_ports_visibility: Optional[Any] = (
                config["dedicatedProxyPortsVisibility"] if "dedicatedProxyPortsVisibility" in config else None
            )
            self.remote_fetch_logs: Optional[Any] = config["remoteFetchLogs"] if "remoteFetchLogs" in config else None
            self.ms_defender_posture_visibility: Optional[Any] = (
                config["msDefenderPostureVisibility"] if "msDefenderPostureVisibility" in config else None
            )
            self.exit_password_visibility: Optional[Any] = (
                config["exitPasswordVisibility"] if "exitPasswordVisibility" in config else None
            )
            self.collect_zdx_location_visibility: Optional[Any] = (
                config["collectZdxLocationVisibility"] if "collectZdxLocationVisibility" in config else None
            )
            self.use_v8_js_engine_visibility: Optional[Any] = (
                config["useV8JsEngineVisibility"] if "useV8JsEngineVisibility" in config else None
            )
            self.zdx_disable_password_visibility: Optional[Any] = (
                config["zdxDisablePasswordVisibility"] if "zdxDisablePasswordVisibility" in config else None
            )
            self.zad_disable_password_visibility: Optional[Any] = (
                config["zadDisablePasswordVisibility"] if "zadDisablePasswordVisibility" in config else None
            )
            self.zpa_disable_password_visibility: Optional[Any] = (
                config["zpaDisablePasswordVisibility"] if "zpaDisablePasswordVisibility" in config else None
            )
            self.default_protocol_for_zpa: Optional[Any] = (
                config["defaultProtocolForZPA"] if "defaultProtocolForZPA" in config else None
            )
            self.drop_ipv6_traffic_visibility: Optional[Any] = (
                config["dropIpv6TrafficVisibility"] if "dropIpv6TrafficVisibility" in config else None
            )
            self.mac_cache_system_proxy_visibility: Optional[Any] = (
                config["macCacheSystemProxyVisibility"] if "macCacheSystemProxyVisibility" in config else None
            )
            self.use_wsa_poll_for_zpa: Optional[Any] = config["useWsaPollForZpa"] if "useWsaPollForZpa" in config else None
            self.enable64_bit_feature: Optional[Any] = config["enable64BitFeature"] if "enable64BitFeature" in config else None
            self.antivirus_posture_visibility: Optional[Any] = (
                config["antivirusPostureVisibility"] if "antivirusPostureVisibility" in config else None
            )
            self.system_proxy_on_any_network_change_visibility: Optional[Any] = (
                config["systemProxyOnAnyNetworkChangeVisibility"]
                if "systemProxyOnAnyNetworkChangeVisibility" in config
                else None
            )
            self.device_posture_os_version_visibility: Optional[Any] = (
                config["devicePostureOsVersionVisibility"] if "devicePostureOsVersionVisibility" in config else None
            )
            self.sccm_config_visibility: Optional[Any] = (
                config["sccmConfigVisibility"] if "sccmConfigVisibility" in config else None
            )
            self.browser_auth_flag_visibility: Optional[Any] = (
                config["browserAuthFlagVisibility"] if "browserAuthFlagVisibility" in config else None
            )
            self.install_web_view2_flag_visibility: Optional[Any] = (
                config["installWebView2FlagVisibility"] if "installWebView2FlagVisibility" in config else None
            )
            self.allow_web_view2_to_follow_sp_visibility: Optional[Any] = (
                config["allowWebView2ToFollowSPVisibility"] if "allowWebView2ToFollowSPVisibility" in config else None
            )
            self.enable_ipv6_resolution_for_zscaler_domains_visibility: Optional[Any] = (
                config["enableIpv6ResolutionForZscalerDomainsVisibility"]
                if "enableIpv6ResolutionForZscalerDomainsVisibility" in config
                else None
            )
            self.disable_reason_visibility: Optional[Any] = (
                config["disableReasonVisibility"] if "disableReasonVisibility" in config else None
            )
            self.follow_routing_table_visibility: Optional[Any] = (
                config["followRoutingTableVisibility"] if "followRoutingTableVisibility" in config else None
            )
            self.zia_device_posture_visibility: Optional[Any] = (
                config["ziaDevicePostureVisibility"] if "ziaDevicePostureVisibility" in config else None
            )
            self.use_custom_dns: Optional[Any] = config["useCustomDNS"] if "useCustomDNS" in config else None
            self.use_default_adapter_for_dns_visibility: Optional[Any] = (
                config["useDefaultAdapterForDNSVisibility"] if "useDefaultAdapterForDNSVisibility" in config else None
            )
            self.t2_fallback_block_all_traffic_and_tls_fallback: Optional[Any] = (
                config["t2FallbackBlockAllTrafficAndTlsFallback"]
                if "t2FallbackBlockAllTrafficAndTlsFallback" in config
                else None
            )
            self.override_t2_protocol_setting: Optional[Any] = (
                config["overrideT2ProtocolSetting"] if "overrideT2ProtocolSetting" in config else None
            )
            self.grant_access_to_zscaler_log_folder_visibility: Optional[Any] = (
                config["grantAccessToZscalerLogFolderVisibility"]
                if "grantAccessToZscalerLogFolderVisibility" in config
                else None
            )
            self.admin_management_visibility: Optional[Any] = (
                config["adminManagementVisibility"] if "adminManagementVisibility" in config else None
            )
            self.redirect_web_traffic_to_zcc_listening_proxy_visibility: Optional[Any] = (
                config["redirectWebTrafficToZccListeningProxyVisibility"]
                if "redirectWebTrafficToZccListeningProxyVisibility" in config
                else None
            )
            self.use_ztunnel2_0_for_proxied_web_traffic_visibility: Optional[Any] = (
                config["useZtunnel2_0ForProxiedWebTrafficVisibility"]
                if "useZtunnel2_0ForProxiedWebTrafficVisibility" in config
                else None
            )
            self.split_vpn_visibility: Optional[Any] = config["splitVpnVisibility"] if "splitVpnVisibility" in config else None
            self.evaluate_trusted_network_visibility: Optional[Any] = (
                config["evaluateTrustedNetworkVisibility"] if "evaluateTrustedNetworkVisibility" in config else None
            )
            self.vpn_adapters_configuration_visibility: Optional[Any] = (
                config["vpnAdaptersConfigurationVisibility"] if "vpnAdaptersConfigurationVisibility" in config else None
            )
            self.vpn_services_visibility: Optional[Any] = (
                config["vpnServicesVisibility"] if "vpnServicesVisibility" in config else None
            )
            self.skip_trusted_criteria_match_visibility: Optional[Any] = (
                config["skipTrustedCriteriaMatchVisibility"] if "skipTrustedCriteriaMatchVisibility" in config else None
            )
            self.external_device_id_visibility: Optional[Any] = (
                config["externalDeviceIdVisibility"] if "externalDeviceIdVisibility" in config else None
            )
            self.flow_logger_loopback_type_visibility: Optional[Any] = (
                config["flowLoggerLoopbackTypeVisibility"] if "flowLoggerLoopbackTypeVisibility" in config else None
            )
            self.flow_logger_zpa_type_visibility: Optional[Any] = (
                config["flowLoggerZPATypeVisibility"] if "flowLoggerZPATypeVisibility" in config else None
            )
            self.flow_logger_vpn_type_visibility: Optional[Any] = (
                config["flowLoggerVPNTypeVisibility"] if "flowLoggerVPNTypeVisibility" in config else None
            )
            self.flow_logger_vpn_tunnel_type_visibility: Optional[Any] = (
                config["flowLoggerVPNTunnelTypeVisibility"] if "flowLoggerVPNTunnelTypeVisibility" in config else None
            )
            self.flow_logger_direct_type_visibility: Optional[Any] = (
                config["flowLoggerDirectTypeVisibility"] if "flowLoggerDirectTypeVisibility" in config else None
            )
            self.use_zscaler_notification_framework: Optional[Any] = (
                config["useZscalerNotificationFramework"] if "useZscalerNotificationFramework" in config else None
            )
            self.fallback_to_gateway_domain: Optional[Any] = (
                config["fallbackToGatewayDomain"] if "fallbackToGatewayDomain" in config else None
            )
            self.zcc_revert_visibility: Optional[Any] = (
                config["zccRevertVisibility"] if "zccRevertVisibility" in config else None
            )
            self.force_zcc_revert_visibility: Optional[Any] = (
                config["forceZccRevertVisibility"] if "forceZccRevertVisibility" in config else None
            )
            self.disaster_recovery_visibility: Optional[Any] = (
                config["disasterRecoveryVisibility"] if "disasterRecoveryVisibility" in config else None
            )
            self.device_group_visibility: Optional[Any] = (
                config["deviceGroupVisibility"] if "deviceGroupVisibility" in config else None
            )
            self.ip_v6_support_for_tunnel2: Optional[Any] = (
                config["ipV6SupportForTunnel2"] if "ipV6SupportForTunnel2" in config else None
            )
            self.path_mtu_discovery: Optional[Any] = config["pathMtuDiscovery"] if "pathMtuDiscovery" in config else None
            self.posture_disc_encryption_visibility_for_linux: Optional[Any] = (
                config["postureDiscEncryptionVisibilityForLinux"]
                if "postureDiscEncryptionVisibilityForLinux" in config
                else None
            )
            self.posture_ms_defender_visibility_for_linux: Optional[Any] = (
                config["postureMsDefenderVisibilityForLinux"] if "postureMsDefenderVisibilityForLinux" in config else None
            )
            self.posture_os_version_visibility_for_linux: Optional[Any] = (
                config["postureOsVersionVisibilityForLinux"] if "postureOsVersionVisibilityForLinux" in config else None
            )
            self.posture_crowd_strike_zta_score_visibility_for_linux: Optional[Any] = (
                config["postureCrowdStrikeZTAScoreVisibilityForLinux"]
                if "postureCrowdStrikeZTAScoreVisibilityForLinux" in config
                else None
            )
            self.flow_logger_zcc_blocked_traffic_visibility: Optional[Any] = (
                config["flowLoggerZCCBlockedTrafficVisibility"] if "flowLoggerZCCBlockedTrafficVisibility" in config else None
            )
            self.flow_logger_intranet_traffic_visibility: Optional[Any] = (
                config["flowLoggerIntranetTrafficVisibility"] if "flowLoggerIntranetTrafficVisibility" in config else None
            )
            self.custom_mtu_for_zpa_visibility: Optional[Any] = (
                config["customMTUForZpaVisibility"] if "customMTUForZpaVisibility" in config else None
            )
            self.zpa_auto_reauth_timeout_visibility: Optional[Any] = (
                config["zpaAutoReauthTimeoutVisibility"] if "zpaAutoReauthTimeoutVisibility" in config else None
            )
            self.force_zpa_auth_expire_visibility: Optional[Any] = (
                config["forceZpaAuthExpireVisibility"] if "forceZpaAuthExpireVisibility" in config else None
            )
            self.enable_set_proxy_on_vpn_adapters_visibility: Optional[Any] = (
                config["enableSetProxyOnVPNAdaptersVisibility"] if "enableSetProxyOnVPNAdaptersVisibility" in config else None
            )
            self.dns_server_route_exclusion_visibility: Optional[Any] = (
                config["dnsServerRouteExclusionVisibility"] if "dnsServerRouteExclusionVisibility" in config else None
            )
            self.enable_separate_otp_for_device: Optional[Any] = (
                config["enableSeparateOtpForDevice"] if "enableSeparateOtpForDevice" in config else None
            )
            self.uninstall_password_for_profile_visibility: Optional[Any] = (
                config["uninstallPasswordForProfileVisibility"] if "uninstallPasswordForProfileVisibility" in config else None
            )
            self.zpa_advance_reauth_visibility: Optional[Any] = (
                config["zpaAdvanceReauthVisibility"] if "zpaAdvanceReauthVisibility" in config else None
            )
            self.latency_based_zen_enablement_visibility: Optional[Any] = (
                config["latencyBasedZenEnablementVisibility"] if "latencyBasedZenEnablementVisibility" in config else None
            )
            self.dynamic_zpa_service_edge_assignmentt_visibility: Optional[Any] = (
                config["dynamicZPAServiceEdgeAssignmenttVisibility"]
                if "dynamicZPAServiceEdgeAssignmenttVisibility" in config
                else None
            )
            self.custom_proxy_ports_visibility: Optional[Any] = (
                config["customProxyPortsVisibility"] if "customProxyPortsVisibility" in config else None
            )
            self.domain_inclusion_exclusion_for_dns_request_visibility: Optional[Any] = (
                config["domainInclusionExclusionForDNSRequestVisibility"]
                if "domainInclusionExclusionForDNSRequestVisibility" in config
                else None
            )
            self.app_notification_config_visibility: Optional[Any] = (
                config["appNotificationConfigVisibility"] if "appNotificationConfigVisibility" in config else None
            )
            self.enable_anti_tampering_visibility: Optional[Any] = (
                config["enableAntiTamperingVisibility"] if "enableAntiTamperingVisibility" in config else None
            )
            self.strict_enforcement_status_visibility: Optional[Any] = (
                config["strictEnforcementStatusVisibility"] if "strictEnforcementStatusVisibility" in config else None
            )
            self.anti_tampering_otp_support_visibility: Optional[Any] = (
                config["antiTamperingOtpSupportVisibility"] if "antiTamperingOtpSupportVisibility" in config else None
            )
            self.override_at_cmd_by_policy_visibility: Optional[Any] = (
                config["overrideATCmdByPolicyVisibility"] if "overrideATCmdByPolicyVisibility" in config else None
            )
            self.device_trust_level_visibility: Optional[Any] = (
                config["deviceTrustLevelVisibility"] if "deviceTrustLevelVisibility" in config else None
            )
            self.source_port_based_bypasses_visibility: Optional[Any] = (
                config["sourcePortBasedBypassesVisibility"] if "sourcePortBasedBypassesVisibility" in config else None
            )
            self.process_based_application_bypass_visibility: Optional[Any] = (
                config["processBasedApplicationBypassVisibility"]
                if "processBasedApplicationBypassVisibility" in config
                else None
            )
            self.custom_based_application_bypass_visibility: Optional[Any] = (
                config["customBasedApplicationBypassVisibility"]
                if "customBasedApplicationBypassVisibility" in config
                else None
            )
            self.client_certificate_template_visibility: Optional[Any] = (
                config["clientCertificateTemplateVisibility"] if "clientCertificateTemplateVisibility" in config else None
            )
            self.supported_zcc_version_chart_visibility: Optional[Any] = (
                config["supportedZccVersionChartVisibility"] if "supportedZccVersionChartVisibility" in config else None
            )
            self.ios_ipv6_mode_visibility: Optional[Any] = (
                config["iosIpv6ModeVisibility"] if "iosIpv6ModeVisibility" in config else None
            )
            self.device_group_multiple_postures_visibility: Optional[Any] = (
                config["deviceGroupMultiplePosturesVisibility"] if "deviceGroupMultiplePosturesVisibility" in config else None
            )
            self.drop_non_zscaler_packets_visibility: Optional[Any] = (
                config["dropNonZscalerPacketsVisibility"] if "dropNonZscalerPacketsVisibility" in config else None
            )
            self.zcc_synthetic_ip_range_visibility: Optional[Any] = (
                config["zccSyntheticIPRangeVisibility"] if "zccSyntheticIPRangeVisibility" in config else None
            )
            self.device_posture_frequency_visibility: Optional[Any] = (
                config["devicePostureFrequencyVisibility"] if "devicePostureFrequencyVisibility" in config else None
            )
            self.enforce_split_dns_visibility: Optional[Any] = (
                config["enforceSplitDNSVisibility"] if "enforceSplitDNSVisibility" in config else None
            )
            self.data_protection_visibility: Optional[Any] = (
                config["dataProtectionVisibility"] if "dataProtectionVisibility" in config else None
            )
            self.drop_quic_traffic_visibility: Optional[Any] = (
                config["dropQuicTrafficVisibility"] if "dropQuicTrafficVisibility" in config else None
            )
            self.truncate_large_udpdns_response_visibility: Optional[Any] = (
                config["truncateLargeUDPDNSResponseVisibility"] if "truncateLargeUDPDNSResponseVisibility" in config else None
            )
            self.prioritize_dns_exclusions_visibility: Optional[Any] = (
                config["prioritizeDnsExclusionsVisibility"] if "prioritizeDnsExclusionsVisibility" in config else None
            )
            self.fetch_log_configuration_option_visibility: Optional[Any] = (
                config["fetchLogConfigurationOptionVisibility"] if "fetchLogConfigurationOptionVisibility" in config else None
            )
            self.enable_serial_number_visibility: Optional[Any] = (
                config["enableSerialNumberVisibility"] if "enableSerialNumberVisibility" in config else None
            )
            self.support_multiple_pwl_postures: Optional[Any] = (
                config["supportMultiplePWLPostures"] if "supportMultiplePWLPostures" in config else None
            )
            self.restrict_remote_packet_capture_visibility: Optional[Any] = (
                config["restrictRemotePacketCaptureVisibility"] if "restrictRemotePacketCaptureVisibility" in config else None
            )
            self.enable_application_based_bypass_for_mac_visibility: Optional[Any] = (
                config["enableApplicationBasedBypassForMacVisibility"]
                if "enableApplicationBasedBypassForMacVisibility" in config
                else None
            )
            self.remove_exempted_containers_visibility: Optional[Any] = (
                config["removeExemptedContainersVisibility"] if "removeExemptedContainersVisibility" in config else None
            )
            self.captive_portal_detection_visibility: Optional[Any] = (
                config["captivePortalDetectionVisibility"] if "captivePortalDetectionVisibility" in config else None
            )
            self.device_group_in_profile_visibility: Optional[Any] = (
                config["deviceGroupInProfileVisibility"] if "deviceGroupInProfileVisibility" in config else None
            )
            self.update_dns_search_order: Optional[Any] = (
                config["updateDnsSearchOrder"] if "updateDnsSearchOrder" in config else None
            )
            self.install_activity_based_monitoring_driver_visibility: Optional[Any] = (
                config["installActivityBasedMonitoringDriverVisibility"]
                if "installActivityBasedMonitoringDriverVisibility" in config
                else None
            )
            self.slow_rollout_zcc: Optional[Any] = config["slowRolloutZCC"] if "slowRolloutZCC" in config else None
            self.zcc_tunnel_version_visibility: Optional[Any] = (
                config["zccTunnelVersionVisibility"] if "zccTunnelVersionVisibility" in config else None
            )
            self.anti_tampering_status_visibility: Optional[Any] = (
                config["antiTamperingStatusVisibility"] if "antiTamperingStatusVisibility" in config else None
            )
            self.lbb_threshold_rank_to_percent_mapping: Optional[Any] = (
                config["lbbThresholdRankToPercentMapping"] if "lbbThresholdRankToPercentMapping" in config else None
            )
            self.remove_zscaler_ssl_cert_url: Optional[Any] = (
                config["removeZscalerSslCertUrl"] if "removeZscalerSslCertUrl" in config else None
            )
            self.lbz_threshold_rank_to_percent_mapping: Optional[Any] = (
                config["lbzThresholdRankToPercentMapping"] if "lbzThresholdRankToPercentMapping" in config else None
            )
            self.splash_screen_url: Optional[Any] = config["splashScreenUrl"] if "splashScreenUrl" in config else None
            self.splash_screen_visibility: Optional[Any] = (
                config["splashScreenVisibility"] if "splashScreenVisibility" in config else None
            )
            self.trusted_network_range_criteria_visibility: Optional[Any] = (
                config["trustedNetworkRangeCriteriaVisibility"] if "trustedNetworkRangeCriteriaVisibility" in config else None
            )
            self.trusted_egress_ips_visibility: Optional[Any] = (
                config["trustedEgressIpsVisibility"] if "trustedEgressIpsVisibility" in config else None
            )
            self.domain_profile_detection_visibility: Optional[Any] = (
                config["domainProfileDetectionVisibility"] if "domainProfileDetectionVisibility" in config else None
            )
            self.all_inbound_traffic_visibility: Optional[Any] = (
                config["allInboundTrafficVisibility"] if "allInboundTrafficVisibility" in config else None
            )
            self.export_logs_for_non_admin_visibility: Optional[Any] = (
                config["exportLogsForNonAdminVisibility"] if "exportLogsForNonAdminVisibility" in config else None
            )
            self.enable_auto_log_snippet_visibility: Optional[Any] = (
                config["enableAutoLogSnippetVisibility"] if "enableAutoLogSnippetVisibility" in config else None
            )
            self.enable_cli_visibility: Optional[Any] = (
                config["enableCliVisibility"] if "enableCliVisibility" in config else None
            )
            self.zcc_user_type_visibility: Optional[Any] = (
                config["zccUserTypeVisibility"] if "zccUserTypeVisibility" in config else None
            )
            self.install_windows_firewall_inbound_rule: Optional[Any] = (
                config["installWindowsFirewallInboundRule"] if "installWindowsFirewallInboundRule" in config else None
            )
            self.retry_after_in_seconds: Optional[Any] = (
                config["retryAfterInSeconds"] if "retryAfterInSeconds" in config else None
            )
            self.azure_ad_posture_visibility: Optional[Any] = (
                config["azureADPostureVisibility"] if "azureADPostureVisibility" in config else None
            )
            self.server_cert_posture_visibility: Optional[Any] = (
                config["serverCertPostureVisibility"] if "serverCertPostureVisibility" in config else None
            )
            self.perform_crl_check_server_posture_visibility: Optional[Any] = (
                config["performCRLCheckServerPostureVisibility"]
                if "performCRLCheckServerPostureVisibility" in config
                else None
            )
            self.auto_fill_using_login_hint_visibility: Optional[Any] = (
                config["autoFillUsingLoginHintVisibility"] if "autoFillUsingLoginHintVisibility" in config else None
            )
            self.send_default_policy_for_invalid_policy_token: Optional[Any] = (
                config["sendDefaultPolicyForInvalidPolicyToken"]
                if "sendDefaultPolicyForInvalidPolicyToken" in config
                else None
            )
            self.enable_zcc_password_settings: Optional[Any] = (
                config["enableZccPasswordSettings"] if "enableZccPasswordSettings" in config else None
            )
            self.cli_password_expiry_minutes: Optional[Any] = (
                config["cliPasswordExpiryMinutes"] if "cliPasswordExpiryMinutes" in config else None
            )
            self.sso_using_windows_primary_account: Optional[Any] = (
                config["ssoUsingWindowsPrimaryAccount"] if "ssoUsingWindowsPrimaryAccount" in config else None
            )
            self.enable_verbose_log: Optional[Any] = config["enableVerboseLog"] if "enableVerboseLog" in config else None
            self.zpa_auth_exp_on_win_logon_session: Optional[Any] = (
                config["zpaAuthExpOnWinLogonSession"] if "zpaAuthExpOnWinLogonSession" in config else None
            )
            self.zpa_auth_exp_on_win_session_lock_visibility: Optional[Any] = (
                config["zpaAuthExpOnWinSessionLockVisibility"] if "zpaAuthExpOnWinSessionLockVisibility" in config else None
            )
            self.enable_zcc_slow_rollout_by_default: Optional[Any] = (
                config["enableZccSlowRolloutByDefault"] if "enableZccSlowRolloutByDefault" in config else None
            )
            self.purge_kerberos_preferred_dc_cache_visibility: Optional[Any] = (
                config["purgeKerberosPreferredDCCacheVisibility"]
                if "purgeKerberosPreferredDCCacheVisibility" in config
                else None
            )
            self.posture_jamf_detection_visibility: Optional[Any] = (
                config["postureJamfDetectionVisibility"] if "postureJamfDetectionVisibility" in config else None
            )
            self.posture_jamf_device_risk_visibility: Optional[Any] = (
                config["postureJamfDeviceRiskVisibility"] if "postureJamfDeviceRiskVisibility" in config else None
            )
            self.windows_ap_captive_portal_detection_visibility: Optional[Any] = (
                config["windowsAPCaptivePortalDetectionVisibility"]
                if "windowsAPCaptivePortalDetectionVisibility" in config
                else None
            )
            self.windows_ap_enable_fail_open_visibility: Optional[Any] = (
                config["windowsAPEnableFailOpenVisibility"] if "windowsAPEnableFailOpenVisibility" in config else None
            )
            self.automatic_capture_duration: Optional[Any] = (
                config["automaticCaptureDuration"] if "automaticCaptureDuration" in config else None
            )
            self.force_location_refresh_sccm: Optional[Any] = (
                config["forceLocationRefreshSccm"] if "forceLocationRefreshSccm" in config else None
            )
            self.enable_posture_failure_dashboard: Optional[Any] = (
                config["enablePostureFailureDashboard"] if "enablePostureFailureDashboard" in config else None
            )
            self.enable_one_id_phase2_changes: Optional[Any] = (
                config["enableOneIDPhase2Changes"] if "enableOneIDPhase2Changes" in config else None
            )
            self.drop_ipv6_traffic_in_ipv6_network_visibility: Optional[Any] = (
                config["dropIpv6TrafficInIpv6NetworkVisibility"]
                if "dropIpv6TrafficInIpv6NetworkVisibility" in config
                else None
            )
            self.enable_postures_for_partner: Optional[Any] = (
                config["enablePosturesForPartner"] if "enablePosturesForPartner" in config else None
            )
            self.enable_partner_config_in_primary_policy: Optional[Any] = (
                config["enablePartnerConfigInPrimaryPolicy"] if "enablePartnerConfigInPrimaryPolicy" in config else None
            )
            self.enable_one_id_admin_migration_changes: Optional[Any] = (
                config["enableOneIDAdminMigrationChanges"] if "enableOneIDAdminMigrationChanges" in config else None
            )
            self.ddil_config_visibility: Optional[Any] = (
                config["ddilConfigVisibility"] if "ddilConfigVisibility" in config else None
            )
            self.add_zdx_service_entitlement: Optional[Any] = (
                config["addZDXServiceEntitlement"] if "addZDXServiceEntitlement" in config else None
            )
            self.use_zcdn: Optional[Any] = config["useZcdn"] if "useZcdn" in config else None
            self.delete_dhcp_option121_routes_visibility: Optional[Any] = (
                config["deleteDHCPOption121RoutesVisibility"] if "deleteDHCPOption121RoutesVisibility" in config else None
            )
            self.zdx_rollout_control_visibility: Optional[Any] = (
                config["zdxRolloutControlVisibility"] if "zdxRolloutControlVisibility" in config else None
            )
            self.show_m365_services_in_app_bypasses: Optional[Any] = (
                config["showM365ServicesInAppBypasses"] if "showM365ServicesInAppBypasses" in config else None
            )
            self.allow_web_view2_ignore_client_cert_errors: Optional[Any] = (
                config["allowWebView2IgnoreClientCertErrors"] if "allowWebView2IgnoreClientCertErrors" in config else None
            )
            self.linux_rpm_build_visibility: Optional[Any] = (
                config["linuxRPMBuildVisibility"] if "linuxRPMBuildVisibility" in config else None
            )
            self.help_banner_data_visibility: Optional[Any] = (
                config["helpBannerDataVisibility"] if "helpBannerDataVisibility" in config else None
            )
            self.zpa_only_device_cleanup_visibility: Optional[Any] = (
                config["zpaOnlyDeviceCleanupVisibility"] if "zpaOnlyDeviceCleanupVisibility" in config else None
            )
            self.app_profile_fail_open_policy_visibility: Optional[Any] = (
                config["appProfileFailOpenPolicyVisibility"] if "appProfileFailOpenPolicyVisibility" in config else None
            )
            self.show_registry_option_in_enforce_and_none: Optional[Any] = (
                config["showRegistryOptionInEnforceAndNone"] if "showRegistryOptionInEnforceAndNone" in config else None
            )
            self.strict_enforcement_notification_visibility: Optional[Any] = (
                config["strictEnforcementNotificationVisibility"]
                if "strictEnforcementNotificationVisibility" in config
                else None
            )
            self.crowd_strike_zta_os_score_visibility: Optional[Any] = (
                config["crowdStrikeZTAOsScoreVisibility"] if "crowdStrikeZTAOsScoreVisibility" in config else None
            )
            self.crowd_strike_zta_sensor_config_score_visibility: Optional[Any] = (
                config["crowdStrikeZTASensorConfigScoreVisibility"]
                if "crowdStrikeZTASensorConfigScoreVisibility" in config
                else None
            )
            self.resize_window_to_fit_to_page_visibility: Optional[Any] = (
                config["resizeWindowToFitToPageVisibility"] if "resizeWindowToFitToPageVisibility" in config else None
            )
            self.enable_zcc_fail_close_settings_for_se_mode: Optional[Any] = (
                config["enableZCCFailCloseSettingsForSEMode"] if "enableZCCFailCloseSettingsForSEMode" in config else None
            )
        else:
            self.enable_fips_mode: Optional[Any] = None
            self.device_cleanup: Optional[Any] = None
            self.sync_time_hours: Optional[Any] = None
            self.hide_non_fed_settings: Optional[Any] = None
            self.hide_audit_logs: Optional[Any] = None
            self.activate_policy: Optional[Any] = None
            self.trusted_network: Optional[Any] = None
            self.process_postures: Optional[Any] = None
            self.zpa_reauth: Optional[Any] = None
            self.inactive_device_cleanup: Optional[Any] = None
            self.zpa_auth_username: Optional[Any] = None
            self.machine_tunnel: Optional[Any] = None
            self.cache_system_proxy: Optional[Any] = None
            self.hide_dtls_support_settings: Optional[Any] = None
            self.machine_token: Optional[Any] = None
            self.application_bypass_info: Optional[Any] = None
            self.tunnel_two_for_android_devices: Optional[Any] = None
            self.tunnel_two_fori_os_devices: Optional[Any] = None
            self.ownership_variable_posture: Optional[Any] = None
            self.block_unreachable_domains_traffic_flag: Optional[Any] = None
            self.prioritize_i_pv4_over_ipv6: Optional[Any] = None
            self.crowd_strike_zta_score_visibility: Optional[Any] = None
            self.notification_for_zpa_reauth_visibility: Optional[Any] = None
            self.crl_check_visibility_flag: Optional[Any] = None
            self.dedicated_proxy_ports_visibility: Optional[Any] = None
            self.remote_fetch_logs: Optional[Any] = None
            self.ms_defender_posture_visibility: Optional[Any] = None
            self.exit_password_visibility: Optional[Any] = None
            self.collect_zdx_location_visibility: Optional[Any] = None
            self.use_v8_js_engine_visibility: Optional[Any] = None
            self.zdx_disable_password_visibility: Optional[Any] = None
            self.zad_disable_password_visibility: Optional[Any] = None
            self.zpa_disable_password_visibility: Optional[Any] = None
            self.default_protocol_for_zpa: Optional[Any] = None
            self.drop_ipv6_traffic_visibility: Optional[Any] = None
            self.mac_cache_system_proxy_visibility: Optional[Any] = None
            self.use_wsa_poll_for_zpa: Optional[Any] = None
            self.enable64_bit_feature: Optional[Any] = None
            self.antivirus_posture_visibility: Optional[Any] = None
            self.system_proxy_on_any_network_change_visibility: Optional[Any] = None
            self.device_posture_os_version_visibility: Optional[Any] = None
            self.sccm_config_visibility: Optional[Any] = None
            self.browser_auth_flag_visibility: Optional[Any] = None
            self.install_web_view2_flag_visibility: Optional[Any] = None
            self.allow_web_view2_to_follow_sp_visibility: Optional[Any] = None
            self.enable_ipv6_resolution_for_zscaler_domains_visibility: Optional[Any] = None
            self.disable_reason_visibility: Optional[Any] = None
            self.follow_routing_table_visibility: Optional[Any] = None
            self.zia_device_posture_visibility: Optional[Any] = None
            self.use_custom_dns: Optional[Any] = None
            self.use_default_adapter_for_dns_visibility: Optional[Any] = None
            self.t2_fallback_block_all_traffic_and_tls_fallback: Optional[Any] = None
            self.override_t2_protocol_setting: Optional[Any] = None
            self.grant_access_to_zscaler_log_folder_visibility: Optional[Any] = None
            self.admin_management_visibility: Optional[Any] = None
            self.redirect_web_traffic_to_zcc_listening_proxy_visibility: Optional[Any] = None
            self.use_ztunnel2_0_for_proxied_web_traffic_visibility: Optional[Any] = None
            self.split_vpn_visibility: Optional[Any] = None
            self.evaluate_trusted_network_visibility: Optional[Any] = None
            self.vpn_adapters_configuration_visibility: Optional[Any] = None
            self.vpn_services_visibility: Optional[Any] = None
            self.skip_trusted_criteria_match_visibility: Optional[Any] = None
            self.external_device_id_visibility: Optional[Any] = None
            self.flow_logger_loopback_type_visibility: Optional[Any] = None
            self.flow_logger_zpa_type_visibility: Optional[Any] = None
            self.flow_logger_vpn_type_visibility: Optional[Any] = None
            self.flow_logger_vpn_tunnel_type_visibility: Optional[Any] = None
            self.flow_logger_direct_type_visibility: Optional[Any] = None
            self.use_zscaler_notification_framework: Optional[Any] = None
            self.fallback_to_gateway_domain: Optional[Any] = None
            self.zcc_revert_visibility: Optional[Any] = None
            self.force_zcc_revert_visibility: Optional[Any] = None
            self.disaster_recovery_visibility: Optional[Any] = None
            self.device_group_visibility: Optional[Any] = None
            self.ip_v6_support_for_tunnel2: Optional[Any] = None
            self.path_mtu_discovery: Optional[Any] = None
            self.posture_disc_encryption_visibility_for_linux: Optional[Any] = None
            self.posture_ms_defender_visibility_for_linux: Optional[Any] = None
            self.posture_os_version_visibility_for_linux: Optional[Any] = None
            self.posture_crowd_strike_zta_score_visibility_for_linux: Optional[Any] = None
            self.flow_logger_zcc_blocked_traffic_visibility: Optional[Any] = None
            self.flow_logger_intranet_traffic_visibility: Optional[Any] = None
            self.custom_mtu_for_zpa_visibility: Optional[Any] = None
            self.zpa_auto_reauth_timeout_visibility: Optional[Any] = None
            self.force_zpa_auth_expire_visibility: Optional[Any] = None
            self.enable_set_proxy_on_vpn_adapters_visibility: Optional[Any] = None
            self.dns_server_route_exclusion_visibility: Optional[Any] = None
            self.enable_separate_otp_for_device: Optional[Any] = None
            self.uninstall_password_for_profile_visibility: Optional[Any] = None
            self.zpa_advance_reauth_visibility: Optional[Any] = None
            self.latency_based_zen_enablement_visibility: Optional[Any] = None
            self.dynamic_zpa_service_edge_assignmentt_visibility: Optional[Any] = None
            self.custom_proxy_ports_visibility: Optional[Any] = None
            self.domain_inclusion_exclusion_for_dns_request_visibility: Optional[Any] = None
            self.app_notification_config_visibility: Optional[Any] = None
            self.enable_anti_tampering_visibility: Optional[Any] = None
            self.strict_enforcement_status_visibility: Optional[Any] = None
            self.anti_tampering_otp_support_visibility: Optional[Any] = None
            self.override_at_cmd_by_policy_visibility: Optional[Any] = None
            self.device_trust_level_visibility: Optional[Any] = None
            self.source_port_based_bypasses_visibility: Optional[Any] = None
            self.process_based_application_bypass_visibility: Optional[Any] = None
            self.custom_based_application_bypass_visibility: Optional[Any] = None
            self.client_certificate_template_visibility: Optional[Any] = None
            self.supported_zcc_version_chart_visibility: Optional[Any] = None
            self.ios_ipv6_mode_visibility: Optional[Any] = None
            self.device_group_multiple_postures_visibility: Optional[Any] = None
            self.drop_non_zscaler_packets_visibility: Optional[Any] = None
            self.zcc_synthetic_ip_range_visibility: Optional[Any] = None
            self.device_posture_frequency_visibility: Optional[Any] = None
            self.enforce_split_dns_visibility: Optional[Any] = None
            self.data_protection_visibility: Optional[Any] = None
            self.drop_quic_traffic_visibility: Optional[Any] = None
            self.truncate_large_udpdns_response_visibility: Optional[Any] = None
            self.prioritize_dns_exclusions_visibility: Optional[Any] = None
            self.fetch_log_configuration_option_visibility: Optional[Any] = None
            self.enable_serial_number_visibility: Optional[Any] = None
            self.support_multiple_pwl_postures: Optional[Any] = None
            self.restrict_remote_packet_capture_visibility: Optional[Any] = None
            self.enable_application_based_bypass_for_mac_visibility: Optional[Any] = None
            self.remove_exempted_containers_visibility: Optional[Any] = None
            self.captive_portal_detection_visibility: Optional[Any] = None
            self.device_group_in_profile_visibility: Optional[Any] = None
            self.update_dns_search_order: Optional[Any] = None
            self.install_activity_based_monitoring_driver_visibility: Optional[Any] = None
            self.slow_rollout_zcc: Optional[Any] = None
            self.zcc_tunnel_version_visibility: Optional[Any] = None
            self.anti_tampering_status_visibility: Optional[Any] = None
            self.lbb_threshold_rank_to_percent_mapping: Optional[Any] = None
            self.remove_zscaler_ssl_cert_url: Optional[Any] = None
            self.lbz_threshold_rank_to_percent_mapping: Optional[Any] = None
            self.splash_screen_url: Optional[Any] = None
            self.splash_screen_visibility: Optional[Any] = None
            self.trusted_network_range_criteria_visibility: Optional[Any] = None
            self.trusted_egress_ips_visibility: Optional[Any] = None
            self.domain_profile_detection_visibility: Optional[Any] = None
            self.all_inbound_traffic_visibility: Optional[Any] = None
            self.export_logs_for_non_admin_visibility: Optional[Any] = None
            self.enable_auto_log_snippet_visibility: Optional[Any] = None
            self.enable_cli_visibility: Optional[Any] = None
            self.zcc_user_type_visibility: Optional[Any] = None
            self.install_windows_firewall_inbound_rule: Optional[Any] = None
            self.retry_after_in_seconds: Optional[Any] = None
            self.azure_ad_posture_visibility: Optional[Any] = None
            self.server_cert_posture_visibility: Optional[Any] = None
            self.perform_crl_check_server_posture_visibility: Optional[Any] = None
            self.auto_fill_using_login_hint_visibility: Optional[Any] = None
            self.send_default_policy_for_invalid_policy_token: Optional[Any] = None
            self.enable_zcc_password_settings: Optional[Any] = None
            self.cli_password_expiry_minutes: Optional[Any] = None
            self.sso_using_windows_primary_account: Optional[Any] = None
            self.enable_verbose_log: Optional[Any] = None
            self.zpa_auth_exp_on_win_logon_session: Optional[Any] = None
            self.zpa_auth_exp_on_win_session_lock_visibility: Optional[Any] = None
            self.enable_zcc_slow_rollout_by_default: Optional[Any] = None
            self.purge_kerberos_preferred_dc_cache_visibility: Optional[Any] = None
            self.posture_jamf_detection_visibility: Optional[Any] = None
            self.posture_jamf_device_risk_visibility: Optional[Any] = None
            self.windows_ap_captive_portal_detection_visibility: Optional[Any] = None
            self.windows_ap_enable_fail_open_visibility: Optional[Any] = None
            self.automatic_capture_duration: Optional[Any] = None
            self.force_location_refresh_sccm: Optional[Any] = None
            self.enable_posture_failure_dashboard: Optional[Any] = None
            self.enable_one_id_phase2_changes: Optional[Any] = None
            self.drop_ipv6_traffic_in_ipv6_network_visibility: Optional[Any] = None
            self.enable_postures_for_partner: Optional[Any] = None
            self.enable_partner_config_in_primary_policy: Optional[Any] = None
            self.enable_one_id_admin_migration_changes: Optional[Any] = None
            self.ddil_config_visibility: Optional[Any] = None
            self.add_zdx_service_entitlement: Optional[Any] = None
            self.use_zcdn: Optional[Any] = None
            self.delete_dhcp_option121_routes_visibility: Optional[Any] = None
            self.zdx_rollout_control_visibility: Optional[Any] = None
            self.show_m365_services_in_app_bypasses: Optional[Any] = None
            self.allow_web_view2_ignore_client_cert_errors: Optional[Any] = None
            self.linux_rpm_build_visibility: Optional[Any] = None
            self.help_banner_data_visibility: Optional[Any] = None
            self.zpa_only_device_cleanup_visibility: Optional[Any] = None
            self.app_profile_fail_open_policy_visibility: Optional[Any] = None
            self.show_registry_option_in_enforce_and_none: Optional[Any] = None
            self.strict_enforcement_notification_visibility: Optional[Any] = None
            self.crowd_strike_zta_os_score_visibility: Optional[Any] = None
            self.crowd_strike_zta_sensor_config_score_visibility: Optional[Any] = None
            self.resize_window_to_fit_to_page_visibility: Optional[Any] = None
            self.enable_zcc_fail_close_settings_for_se_mode: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "enableFipsMode": self.enable_fips_mode,
            "deviceCleanup": self.device_cleanup,
            "syncTimeHours": self.sync_time_hours,
            "hideNonFedSettings": self.hide_non_fed_settings,
            "hideAuditLogs": self.hide_audit_logs,
            "activatePolicy": self.activate_policy,
            "trustedNetwork": self.trusted_network,
            "processPostures": self.process_postures,
            "zpaReauth": self.zpa_reauth,
            "inactiveDeviceCleanup": self.inactive_device_cleanup,
            "zpaAuthUsername": self.zpa_auth_username,
            "machineTunnel": self.machine_tunnel,
            "cacheSystemProxy": self.cache_system_proxy,
            "hideDTLSSupportSettings": self.hide_dtls_support_settings,
            "machineToken": self.machine_token,
            "applicationBypassInfo": self.application_bypass_info,
            "tunnelTwoForAndroidDevices": self.tunnel_two_for_android_devices,
            "tunnelTwoForiOSDevices": self.tunnel_two_fori_os_devices,
            "ownershipVariablePosture": self.ownership_variable_posture,
            "blockUnreachableDomainsTrafficFlag": self.block_unreachable_domains_traffic_flag,
            "prioritizeIPv4OverIpv6": self.prioritize_i_pv4_over_ipv6,
            "crowdStrikeZTAScoreVisibility": self.crowd_strike_zta_score_visibility,
            "notificationForZPAReauthVisibility": self.notification_for_zpa_reauth_visibility,
            "crlCheckVisibilityFlag": self.crl_check_visibility_flag,
            "dedicatedProxyPortsVisibility": self.dedicated_proxy_ports_visibility,
            "remoteFetchLogs": self.remote_fetch_logs,
            "msDefenderPostureVisibility": self.ms_defender_posture_visibility,
            "exitPasswordVisibility": self.exit_password_visibility,
            "collectZdxLocationVisibility": self.collect_zdx_location_visibility,
            "useV8JsEngineVisibility": self.use_v8_js_engine_visibility,
            "zdxDisablePasswordVisibility": self.zdx_disable_password_visibility,
            "zadDisablePasswordVisibility": self.zad_disable_password_visibility,
            "zpaDisablePasswordVisibility": self.zpa_disable_password_visibility,
            "defaultProtocolForZPA": self.default_protocol_for_zpa,
            "dropIpv6TrafficVisibility": self.drop_ipv6_traffic_visibility,
            "macCacheSystemProxyVisibility": self.mac_cache_system_proxy_visibility,
            "useWsaPollForZpa": self.use_wsa_poll_for_zpa,
            "enable64BitFeature": self.enable64_bit_feature,
            "antivirusPostureVisibility": self.antivirus_posture_visibility,
            "systemProxyOnAnyNetworkChangeVisibility": self.system_proxy_on_any_network_change_visibility,
            "devicePostureOsVersionVisibility": self.device_posture_os_version_visibility,
            "sccmConfigVisibility": self.sccm_config_visibility,
            "browserAuthFlagVisibility": self.browser_auth_flag_visibility,
            "installWebView2FlagVisibility": self.install_web_view2_flag_visibility,
            "allowWebView2ToFollowSPVisibility": self.allow_web_view2_to_follow_sp_visibility,
            "enableIpv6ResolutionForZscalerDomainsVisibility": self.enable_ipv6_resolution_for_zscaler_domains_visibility,
            "disableReasonVisibility": self.disable_reason_visibility,
            "followRoutingTableVisibility": self.follow_routing_table_visibility,
            "ziaDevicePostureVisibility": self.zia_device_posture_visibility,
            "useCustomDNS": self.use_custom_dns,
            "useDefaultAdapterForDNSVisibility": self.use_default_adapter_for_dns_visibility,
            "t2FallbackBlockAllTrafficAndTlsFallback": self.t2_fallback_block_all_traffic_and_tls_fallback,
            "overrideT2ProtocolSetting": self.override_t2_protocol_setting,
            "grantAccessToZscalerLogFolderVisibility": self.grant_access_to_zscaler_log_folder_visibility,
            "adminManagementVisibility": self.admin_management_visibility,
            "redirectWebTrafficToZccListeningProxyVisibility": self.redirect_web_traffic_to_zcc_listening_proxy_visibility,
            "useZtunnel2_0ForProxiedWebTrafficVisibility": self.use_ztunnel2_0_for_proxied_web_traffic_visibility,
            "splitVpnVisibility": self.split_vpn_visibility,
            "evaluateTrustedNetworkVisibility": self.evaluate_trusted_network_visibility,
            "vpnAdaptersConfigurationVisibility": self.vpn_adapters_configuration_visibility,
            "vpnServicesVisibility": self.vpn_services_visibility,
            "skipTrustedCriteriaMatchVisibility": self.skip_trusted_criteria_match_visibility,
            "externalDeviceIdVisibility": self.external_device_id_visibility,
            "flowLoggerLoopbackTypeVisibility": self.flow_logger_loopback_type_visibility,
            "flowLoggerZPATypeVisibility": self.flow_logger_zpa_type_visibility,
            "flowLoggerVPNTypeVisibility": self.flow_logger_vpn_type_visibility,
            "flowLoggerVPNTunnelTypeVisibility": self.flow_logger_vpn_tunnel_type_visibility,
            "flowLoggerDirectTypeVisibility": self.flow_logger_direct_type_visibility,
            "useZscalerNotificationFramework": self.use_zscaler_notification_framework,
            "fallbackToGatewayDomain": self.fallback_to_gateway_domain,
            "zccRevertVisibility": self.zcc_revert_visibility,
            "forceZccRevertVisibility": self.force_zcc_revert_visibility,
            "disasterRecoveryVisibility": self.disaster_recovery_visibility,
            "deviceGroupVisibility": self.device_group_visibility,
            "ipV6SupportForTunnel2": self.ip_v6_support_for_tunnel2,
            "pathMtuDiscovery": self.path_mtu_discovery,
            "postureDiscEncryptionVisibilityForLinux": self.posture_disc_encryption_visibility_for_linux,
            "postureMsDefenderVisibilityForLinux": self.posture_ms_defender_visibility_for_linux,
            "postureOsVersionVisibilityForLinux": self.posture_os_version_visibility_for_linux,
            "postureCrowdStrikeZTAScoreVisibilityForLinux": self.posture_crowd_strike_zta_score_visibility_for_linux,
            "flowLoggerZCCBlockedTrafficVisibility": self.flow_logger_zcc_blocked_traffic_visibility,
            "flowLoggerIntranetTrafficVisibility": self.flow_logger_intranet_traffic_visibility,
            "customMTUForZpaVisibility": self.custom_mtu_for_zpa_visibility,
            "zpaAutoReauthTimeoutVisibility": self.zpa_auto_reauth_timeout_visibility,
            "forceZpaAuthExpireVisibility": self.force_zpa_auth_expire_visibility,
            "enableSetProxyOnVPNAdaptersVisibility": self.enable_set_proxy_on_vpn_adapters_visibility,
            "dnsServerRouteExclusionVisibility": self.dns_server_route_exclusion_visibility,
            "enableSeparateOtpForDevice": self.enable_separate_otp_for_device,
            "uninstallPasswordForProfileVisibility": self.uninstall_password_for_profile_visibility,
            "zpaAdvanceReauthVisibility": self.zpa_advance_reauth_visibility,
            "latencyBasedZenEnablementVisibility": self.latency_based_zen_enablement_visibility,
            "dynamicZPAServiceEdgeAssignmenttVisibility": self.dynamic_zpa_service_edge_assignmentt_visibility,
            "customProxyPortsVisibility": self.custom_proxy_ports_visibility,
            "domainInclusionExclusionForDNSRequestVisibility": self.domain_inclusion_exclusion_for_dns_request_visibility,
            "appNotificationConfigVisibility": self.app_notification_config_visibility,
            "enableAntiTamperingVisibility": self.enable_anti_tampering_visibility,
            "strictEnforcementStatusVisibility": self.strict_enforcement_status_visibility,
            "antiTamperingOtpSupportVisibility": self.anti_tampering_otp_support_visibility,
            "overrideATCmdByPolicyVisibility": self.override_at_cmd_by_policy_visibility,
            "deviceTrustLevelVisibility": self.device_trust_level_visibility,
            "sourcePortBasedBypassesVisibility": self.source_port_based_bypasses_visibility,
            "processBasedApplicationBypassVisibility": self.process_based_application_bypass_visibility,
            "customBasedApplicationBypassVisibility": self.custom_based_application_bypass_visibility,
            "clientCertificateTemplateVisibility": self.client_certificate_template_visibility,
            "supportedZccVersionChartVisibility": self.supported_zcc_version_chart_visibility,
            "iosIpv6ModeVisibility": self.ios_ipv6_mode_visibility,
            "deviceGroupMultiplePosturesVisibility": self.device_group_multiple_postures_visibility,
            "dropNonZscalerPacketsVisibility": self.drop_non_zscaler_packets_visibility,
            "zccSyntheticIPRangeVisibility": self.zcc_synthetic_ip_range_visibility,
            "devicePostureFrequencyVisibility": self.device_posture_frequency_visibility,
            "enforceSplitDNSVisibility": self.enforce_split_dns_visibility,
            "dataProtectionVisibility": self.data_protection_visibility,
            "dropQuicTrafficVisibility": self.drop_quic_traffic_visibility,
            "truncateLargeUDPDNSResponseVisibility": self.truncate_large_udpdns_response_visibility,
            "prioritizeDnsExclusionsVisibility": self.prioritize_dns_exclusions_visibility,
            "fetchLogConfigurationOptionVisibility": self.fetch_log_configuration_option_visibility,
            "enableSerialNumberVisibility": self.enable_serial_number_visibility,
            "supportMultiplePWLPostures": self.support_multiple_pwl_postures,
            "restrictRemotePacketCaptureVisibility": self.restrict_remote_packet_capture_visibility,
            "enableApplicationBasedBypassForMacVisibility": self.enable_application_based_bypass_for_mac_visibility,
            "removeExemptedContainersVisibility": self.remove_exempted_containers_visibility,
            "captivePortalDetectionVisibility": self.captive_portal_detection_visibility,
            "deviceGroupInProfileVisibility": self.device_group_in_profile_visibility,
            "updateDnsSearchOrder": self.update_dns_search_order,
            "installActivityBasedMonitoringDriverVisibility": self.install_activity_based_monitoring_driver_visibility,
            "slowRolloutZCC": self.slow_rollout_zcc,
            "zccTunnelVersionVisibility": self.zcc_tunnel_version_visibility,
            "antiTamperingStatusVisibility": self.anti_tampering_status_visibility,
            "lbbThresholdRankToPercentMapping": self.lbb_threshold_rank_to_percent_mapping,
            "removeZscalerSslCertUrl": self.remove_zscaler_ssl_cert_url,
            "lbzThresholdRankToPercentMapping": self.lbz_threshold_rank_to_percent_mapping,
            "splashScreenUrl": self.splash_screen_url,
            "splashScreenVisibility": self.splash_screen_visibility,
            "trustedNetworkRangeCriteriaVisibility": self.trusted_network_range_criteria_visibility,
            "trustedEgressIpsVisibility": self.trusted_egress_ips_visibility,
            "domainProfileDetectionVisibility": self.domain_profile_detection_visibility,
            "allInboundTrafficVisibility": self.all_inbound_traffic_visibility,
            "exportLogsForNonAdminVisibility": self.export_logs_for_non_admin_visibility,
            "enableAutoLogSnippetVisibility": self.enable_auto_log_snippet_visibility,
            "enableCliVisibility": self.enable_cli_visibility,
            "zccUserTypeVisibility": self.zcc_user_type_visibility,
            "installWindowsFirewallInboundRule": self.install_windows_firewall_inbound_rule,
            "retryAfterInSeconds": self.retry_after_in_seconds,
            "azureADPostureVisibility": self.azure_ad_posture_visibility,
            "serverCertPostureVisibility": self.server_cert_posture_visibility,
            "performCRLCheckServerPostureVisibility": self.perform_crl_check_server_posture_visibility,
            "autoFillUsingLoginHintVisibility": self.auto_fill_using_login_hint_visibility,
            "sendDefaultPolicyForInvalidPolicyToken": self.send_default_policy_for_invalid_policy_token,
            "enableZccPasswordSettings": self.enable_zcc_password_settings,
            "cliPasswordExpiryMinutes": self.cli_password_expiry_minutes,
            "ssoUsingWindowsPrimaryAccount": self.sso_using_windows_primary_account,
            "enableVerboseLog": self.enable_verbose_log,
            "zpaAuthExpOnWinLogonSession": self.zpa_auth_exp_on_win_logon_session,
            "zpaAuthExpOnWinSessionLockVisibility": self.zpa_auth_exp_on_win_session_lock_visibility,
            "enableZccSlowRolloutByDefault": self.enable_zcc_slow_rollout_by_default,
            "purgeKerberosPreferredDCCacheVisibility": self.purge_kerberos_preferred_dc_cache_visibility,
            "postureJamfDetectionVisibility": self.posture_jamf_detection_visibility,
            "postureJamfDeviceRiskVisibility": self.posture_jamf_device_risk_visibility,
            "windowsAPCaptivePortalDetectionVisibility": self.windows_ap_captive_portal_detection_visibility,
            "windowsAPEnableFailOpenVisibility": self.windows_ap_enable_fail_open_visibility,
            "automaticCaptureDuration": self.automatic_capture_duration,
            "forceLocationRefreshSccm": self.force_location_refresh_sccm,
            "enablePostureFailureDashboard": self.enable_posture_failure_dashboard,
            "enableOneIDPhase2Changes": self.enable_one_id_phase2_changes,
            "dropIpv6TrafficInIpv6NetworkVisibility": self.drop_ipv6_traffic_in_ipv6_network_visibility,
            "enablePosturesForPartner": self.enable_postures_for_partner,
            "enablePartnerConfigInPrimaryPolicy": self.enable_partner_config_in_primary_policy,
            "enableOneIDAdminMigrationChanges": self.enable_one_id_admin_migration_changes,
            "ddilConfigVisibility": self.ddil_config_visibility,
            "addZDXServiceEntitlement": self.add_zdx_service_entitlement,
            "useZcdn": self.use_zcdn,
            "deleteDHCPOption121RoutesVisibility": self.delete_dhcp_option121_routes_visibility,
            "zdxRolloutControlVisibility": self.zdx_rollout_control_visibility,
            "showM365ServicesInAppBypasses": self.show_m365_services_in_app_bypasses,
            "allowWebView2IgnoreClientCertErrors": self.allow_web_view2_ignore_client_cert_errors,
            "linuxRPMBuildVisibility": self.linux_rpm_build_visibility,
            "helpBannerDataVisibility": self.help_banner_data_visibility,
            "zpaOnlyDeviceCleanupVisibility": self.zpa_only_device_cleanup_visibility,
            "appProfileFailOpenPolicyVisibility": self.app_profile_fail_open_policy_visibility,
            "showRegistryOptionInEnforceAndNone": self.show_registry_option_in_enforce_and_none,
            "strictEnforcementNotificationVisibility": self.strict_enforcement_notification_visibility,
            "crowdStrikeZTAOsScoreVisibility": self.crowd_strike_zta_os_score_visibility,
            "crowdStrikeZTASensorConfigScoreVisibility": self.crowd_strike_zta_sensor_config_score_visibility,
            "resizeWindowToFitToPageVisibility": self.resize_window_to_fit_to_page_visibility,
            "enableZCCFailCloseSettingsForSEMode": self.enable_zcc_fail_close_settings_for_se_mode,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
