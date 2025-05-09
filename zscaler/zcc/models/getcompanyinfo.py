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


from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class GetCompanyInfo(ZscalerObject):
    """
    A class for GetCompanyInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the GetCompanyInfo model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.org_id = config["orgId"] \
                if "orgId" in config else None
            self.master_customer_id = config["masterCustomerId"] \
                if "masterCustomerId" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.business_name = config["businessName"] \
                if "businessName" in config else None
            self.business_contact_number = config["businessContactNumber"] \
                if "businessContactNumber" in config else None
            self.activation_recipient = config["activationRecipient"] \
                if "activationRecipient" in config else None
            self.activation_copy = config["activationCopy"] \
                if "activationCopy" in config else None
            self.mdm_status = config["mdmStatus"] \
                if "mdmStatus" in config else None
            self.send_email = config["sendEmail"] \
                if "sendEmail" in config else None
            self.proxy_enabled = config["proxyEnabled"] \
                if "proxyEnabled" in config else None
            self.zpn_enabled = config["zpnEnabled"] \
                if "zpnEnabled" in config else None
            self.upm_enabled = config["upmEnabled"] \
                if "upmEnabled" in config else None
            self.zad_enabled = config["zadEnabled"] \
                if "zadEnabled" in config else None
            self.enable_deception_for_all = config["enableDeceptionForAll"] \
                if "enableDeceptionForAll" in config else None
            self.dlp_enabled = config["dlpEnabled"] \
                if "dlpEnabled" in config else None
            self.tunnel_protocol_type = config["tunnelProtocolType"] \
                if "tunnelProtocolType" in config else None
            self.secure_agent_basic = config["secureAgentBasic"] \
                if "secureAgentBasic" in config else None
            self.secure_agent_advanced = config["secureAgentAdvanced"] \
                if "secureAgentAdvanced" in config else None
            self.support_admin_email = config["supportAdminEmail"] \
                if "supportAdminEmail" in config else None
            self.support_enabled = config["supportEnabled"] \
                if "supportEnabled" in config else None
            self.fetch_logs_for_admins_enabled = config["fetchLogsForAdminsEnabled"] \
                if "fetchLogsForAdminsEnabled" in config else None
            self.enable_rectify_utils = config["enableRectifyUtils"] \
                if "enableRectifyUtils" in config else None
            self.support_ticket_enabled = config["supportTicketEnabled"] \
                if "supportTicketEnabled" in config else None
            self.disable_logging_controls = config["disableLoggingControls"] \
                if "disableLoggingControls" in config else None
            self.default_auth_type = config["defaultAuthType"] \
                if "defaultAuthType" in config else None
            self.version = config["version"] \
                if "version" in config else None
            self.policy_activation_required = config["policyActivationRequired"] \
                if "policyActivationRequired" in config else None
            self.enable_autofill_username = config["enableAutofillUsername"] \
                if "enableAutofillUsername" in config else None
            self.auto_fill_using_login_hint = config["autoFillUsingLoginHint"] \
                if "autoFillUsingLoginHint" in config else None
            self.dc_service_read_only = config["dcServiceReadOnly"] \
                if "dcServiceReadOnly" in config else None
            self.enable_tunnel_zapp_traffic_toggle = config["enableTunnelZappTrafficToggle"] \
                if "enableTunnelZappTrafficToggle" in config else None
            self.machine_idp_auth = config["machineIdpAuth"] \
                if "machineIdpAuth" in config else None
            self.linux_visibility = config["linuxVisibility"] \
                if "linuxVisibility" in config else None
            self.registry_path_for_pac = config["registryPathForPac"] \
                if "registryPathForPac" in config else None
            self.use_pollset_for_socket_reactor = config["usePollsetForSocketReactor"] \
                if "usePollsetForSocketReactor" in config else None
            self.enable_dtls_for_zpa = config["enableDtlsForZpa"] \
                if "enableDtlsForZpa" in config else None
            self.use_v8_js_engine = config["useV8JsEngine"] \
                if "useV8JsEngine" in config else None
            self.disable_parallel_ipv4_and_ipv6 = config["disableParallelIpv4AndIPv6"] \
                if "disableParallelIpv4AndIPv6" in config else None
            self.send64_bit_build = config["send64BitBuild"] \
                if "send64BitBuild" in config else None
            self.use_add_ifscope_route = config["useAddIfscopeRoute"] \
                if "useAddIfscopeRoute" in config else None
            self.use_clear_arp_cache = config["useClearArpCache"] \
                if "useClearArpCache" in config else None
            self.use_dns_priority_ordering = config["useDnsPriorityOrdering"] \
                if "useDnsPriorityOrdering" in config else None
            self.enable_browser_auth = config["enableBrowserAuth"] \
                if "enableBrowserAuth" in config else None
            self.enable_public_api = config["enablePublicAPI"] \
                if "enablePublicAPI" in config else None
            self.disable_reason_visibility = config["disableReasonVisibility"] \
                if "disableReasonVisibility" in config else None
            self.follow_routing_table = config["followRoutingTable"] \
                if "followRoutingTable" in config else None
            self.use_default_adapter_for_dns = config["useDefaultAdapterForDNS"] \
                if "useDefaultAdapterForDNS" in config else None
            self.enable_minimum_device_cleanup_as_one = config["enableMinimumDeviceCleanupAsOne"] \
                if "enableMinimumDeviceCleanupAsOne" in config else None
            self.dns_priority_ordering_for_trusted_dns_criteria = config["dnsPriorityOrderingForTrustedDnsCriteria"] \
                if "dnsPriorityOrderingForTrustedDnsCriteria" in config else None
            self.machine_tunnel_posture = config["machineTunnelPosture"] \
                if "machineTunnelPosture" in config else None
            self.zpa_partner_login = config["zpaPartnerLogin"] \
                if "zpaPartnerLogin" in config else None
            self.proxy_port = config["proxyPort"] \
                if "proxyPort" in config else None
            self.dns_cache_ttl_windows = config["dnsCacheTtlWindows"] \
                if "dnsCacheTtlWindows" in config else None
            self.dns_cache_ttl_mac = config["dnsCacheTtlMac"] \
                if "dnsCacheTtlMac" in config else None
            self.dns_cache_ttl_android = config["dnsCacheTtlAndroid"] \
                if "dnsCacheTtlAndroid" in config else None
            self.dns_cache_ttl_ios = config["dnsCacheTtlIos"] \
                if "dnsCacheTtlIos" in config else None
            self.dns_cache_ttl_linux = config["dnsCacheTtlLinux"] \
                if "dnsCacheTtlLinux" in config else None
            self.zpa_client_cert_exp_in_days = config["zpaClientCertExpInDays"] \
                if "zpaClientCertExpInDays" in config else None
            self.enable_flow_logger = config["enableFlowLogger"] \
                if "enableFlowLogger" in config else None
            self.flow_logging_buffer_limit = config["flowLoggingBufferLimit"] \
                if "flowLoggingBufferLimit" in config else None
            self.flow_logging_time_interval = config["flowLoggingTimeInterval"] \
                if "flowLoggingTimeInterval" in config else None
            self.posture_based_service = config["postureBasedService"] \
                if "postureBasedService" in config else None
            self.enable_posture_based_profile = config["enablePostureBasedProfile"] \
                if "enablePostureBasedProfile" in config else None
            self.disaster_recovery = config["disasterRecovery"] \
                if "disasterRecovery" in config else None
            self.zia_global_db_url_for_dr = config["ziaGlobalDbUrlForDR"] \
                if "ziaGlobalDbUrlForDR" in config else None
            self.enable_react_ui = config["enableReactUI"] \
                if "enableReactUI" in config else None
            self.launch_react_u_iby_default = config["launchReactUIbyDefault"] \
                if "launchReactUIbyDefault" in config else None
            self.dlp_notification = config["dlpNotification"] \
                if "dlpNotification" in config else None
            self.vpn_gateway_char_limit = config["vpnGatewayCharLimit"] \
                if "vpnGatewayCharLimit" in config else None
            self.device_groups_count = config["deviceGroupsCount"] \
                if "deviceGroupsCount" in config else None
            self.vpn_bypass_refresh_interval = config["vpnBypassRefreshInterval"] \
                if "vpnBypassRefreshInterval" in config else None
            self.dest_include_exclude_char_limit = config["destIncludeExcludeCharLimit"] \
                if "destIncludeExcludeCharLimit" in config else None
            self.ip_v6_support_for_tunnel2 = config["ipV6SupportForTunnel2"] \
                if "ipV6SupportForTunnel2" in config else None
            self.dest_include_exclude_char_limit_for_ipv6 = config["destIncludeExcludeCharLimitForIpv6"] \
                if "destIncludeExcludeCharLimitForIpv6" in config else None
            self.enable_set_proxy_on_vpn_adapters = config["enableSetProxyOnVPNAdapters"] \
                if "enableSetProxyOnVPNAdapters" in config else None
            self.disable_dns_route_exclusion = config["disableDNSRouteExclusion"] \
                if "disableDNSRouteExclusion" in config else None
            self.show_vpn_tun_notification = config["showVPNTunNotification"] \
                if "showVPNTunNotification" in config else None
            self.add_app_bypass_to_vpn_gateway = config["addAppBypassToVPNGateway"] \
                if "addAppBypassToVPNGateway" in config else None
            self.enable_zscaler_firewall = config["enableZscalerFirewall"] \
                if "enableZscalerFirewall" in config else None
            self.persistent_zscaler_firewall = config["persistentZscalerFirewall"] \
                if "persistentZscalerFirewall" in config else None
            self.clear_mup_cache = config["clearMupCache"] \
                if "clearMupCache" in config else None
            self.execute_gpo_update = config["executeGpoUpdate"] \
                if "executeGpoUpdate" in config else None
            self.enable_port_based_zpa_filter = config["enablePortBasedZPAFilter"] \
                if "enablePortBasedZPAFilter" in config else None
            self.enable_anti_tampering = config["enableAntiTampering"] \
                if "enableAntiTampering" in config else None
            self.zpa_reauth_enabled = config["zpaReauthEnabled"] \
                if "zpaReauthEnabled" in config else None
            self.zpa_auto_reauth_timeout = config["zpaAutoReauthTimeout"] \
                if "zpaAutoReauthTimeout" in config else None
            self.enable_zpa_auth_user_name = config["enableZpaAuthUserName"] \
                if "enableZpaAuthUserName" in config else None
            self.configure_tunnel2fallback_for_zia = config["configureTunnel2fallbackForZia"] \
                if "configureTunnel2fallbackForZia" in config else None
            self.enable_install_web_view2 = config["enableInstallWebView2"] \
                if "enableInstallWebView2" in config else None
            self.enable_custom_proxy_ports = config["enableCustomProxyPorts"] \
                if "enableCustomProxyPorts" in config else None
            self.intercept_zia_traffic_all_adapters = config["interceptZIATrafficAllAdapters"] \
                if "interceptZIATrafficAllAdapters" in config else None
            self.swagger_link = config["swaggerLink"] \
                if "swaggerLink" in config else None
            self.enable_one_id_admin = config["enableOneIdAdmin"] \
                if "enableOneIdAdmin" in config else None
            self.enable_one_id_user = config["enableOneIdUser"] \
                if "enableOneIdUser" in config else None
            self.restrict_admin_access = config["restrictAdminAccess"] \
                if "restrictAdminAccess" in config else None
            self.enable_zia_user_department_sync = config["enableZiaUserDepartmentSync"] \
                if "enableZiaUserDepartmentSync" in config else None
            self.enable_udp_transport_selection = config["enableUDPTransportSelection"] \
                if "enableUDPTransportSelection" in config else None
            self.compute_device_groups_for_zia = config["computeDeviceGroupsForZIA"] \
                if "computeDeviceGroupsForZIA" in config else None
            self.compute_device_groups_for_zpa = config["computeDeviceGroupsForZPA"] \
                if "computeDeviceGroupsForZPA" in config else None
            self.compute_device_groups_for_z_d_x = config["computeDeviceGroupsForZDX"] \
                if "computeDeviceGroupsForZDX" in config else None
            self.compute_device_groups_for_zad = config["computeDeviceGroupsForZAD"] \
                if "computeDeviceGroupsForZAD" in config else None
            self.use_tunnel2_sme_for_tunnel1 = config["useTunnel2SmeForTunnel1"] \
                if "useTunnel2SmeForTunnel1" in config else None
            self.ma_cloud_name = config["maCloudName"] \
                if "maCloudName" in config else None
            self.zia_cloud_name = config["ziaCloudName"] \
                if "ziaCloudName" in config else None
            self.zt2_health_probe_interval = config["zt2HealthProbeInterval"] \
                if "zt2HealthProbeInterval" in config else None
            self.device_posture_frequency = ZscalerCollection.form_list(
                config["devicePostureFrequency"] if "devicePostureFrequency" in config else [], str
            )
            self.zdx_manual_rollout = config["zdxManualRollout"] \
                if "zdxManualRollout" in config else None
            self.win_zdx_lite_enabled = config["winZdxLiteEnabled"] \
                if "winZdxLiteEnabled" in config else None

            if "webAppConfig" in config:
                if isinstance(config["webAppConfig"], WebAppConfig):
                    self.web_app_config = config["webAppConfig"]
                elif config["webAppConfig"] is not None:
                    self.web_app_config = WebAppConfig(config["webAppConfig"])
                else:
                    self.web_app_config = None
            else:
                self.web_app_config = None

            self.device_posture_frequency = ZscalerCollection.form_list(
                config["devicePostureFrequency"] if "devicePostureFrequency" in config else [], DevicePostureFrequency
            )
        else:
            self.org_id = None
            self.master_customer_id = None
            self.name = None
            self.business_name = None
            self.business_contact_number = None
            self.activation_recipient = None
            self.activation_copy = None
            self.mdm_status = None
            self.send_email = None
            self.proxy_enabled = None
            self.zpn_enabled = None
            self.upm_enabled = None
            self.zad_enabled = None
            self.enable_deception_for_all = None
            self.dlp_enabled = None
            self.tunnel_protocol_type = None
            self.secure_agent_basic = None
            self.secure_agent_advanced = None
            self.support_admin_email = None
            self.support_enabled = None
            self.fetch_logs_for_admins_enabled = None
            self.enable_rectify_utils = None
            self.support_ticket_enabled = None
            self.disable_logging_controls = None
            self.default_auth_type = None
            self.version = None
            self.policy_activation_required = None
            self.enable_autofill_username = None
            self.auto_fill_using_login_hint = None
            self.dc_service_read_only = None
            self.enable_tunnel_zapp_traffic_toggle = None
            self.machine_idp_auth = None
            self.linux_visibility = None
            self.registry_path_for_pac = None
            self.use_pollset_for_socket_reactor = None
            self.enable_dtls_for_zpa = None
            self.use_v8_js_engine = None
            self.disable_parallel_ipv4_and_ipv6 = None
            self.send64_bit_build = None
            self.use_add_ifscope_route = None
            self.use_clear_arp_cache = None
            self.use_dns_priority_ordering = None
            self.enable_browser_auth = None
            self.enable_public_api = None
            self.disable_reason_visibility = None
            self.follow_routing_table = None
            self.use_default_adapter_for_dns = None
            self.enable_minimum_device_cleanup_as_one = None
            self.dns_priority_ordering_for_trusted_dns_criteria = None
            self.machine_tunnel_posture = None
            self.zpa_partner_login = None
            self.proxy_port = None
            self.dns_cache_ttl_windows = None
            self.dns_cache_ttl_mac = None
            self.dns_cache_ttl_android = None
            self.dns_cache_ttl_ios = None
            self.dns_cache_ttl_linux = None
            self.zpa_client_cert_exp_in_days = None
            self.enable_flow_logger = None
            self.flow_logging_buffer_limit = None
            self.flow_logging_time_interval = None
            self.posture_based_service = None
            self.enable_posture_based_profile = None
            self.disaster_recovery = None
            self.zia_global_db_url_for_dr = None
            self.enable_react_ui = None
            self.launch_react_u_iby_default = None
            self.dlp_notification = None
            self.vpn_gateway_char_limit = None
            self.device_groups_count = None
            self.vpn_bypass_refresh_interval = None
            self.dest_include_exclude_char_limit = None
            self.ip_v6_support_for_tunnel2 = None
            self.dest_include_exclude_char_limit_for_ipv6 = None
            self.enable_set_proxy_on_vpn_adapters = None
            self.disable_dns_route_exclusion = None
            self.show_vpn_tun_notification = None
            self.add_app_bypass_to_vpn_gateway = None
            self.enable_zscaler_firewall = None
            self.persistent_zscaler_firewall = None
            self.clear_mup_cache = None
            self.execute_gpo_update = None
            self.enable_port_based_zpa_filter = None
            self.enable_anti_tampering = None
            self.zpa_reauth_enabled = None
            self.zpa_auto_reauth_timeout = None
            self.enable_zpa_auth_user_name = None
            self.configure_tunnel2fallback_for_zia = None
            self.web_app_config = None
            self.enable_install_web_view2 = None
            self.enable_custom_proxy_ports = None
            self.intercept_zia_traffic_all_adapters = None
            self.swagger_link = None
            self.enable_one_id_admin = None
            self.enable_one_id_user = None
            self.restrict_admin_access = None
            self.enable_zia_user_department_sync = None
            self.enable_u_d_p_transport_selection = None
            self.compute_device_groups_for_zia = None
            self.compute_device_groups_for_zpa = None
            self.compute_device_groups_for_zdx = None
            self.compute_device_groups_for_zad = None
            self.use_tunnel2_sme_for_tunnel1 = None
            self.ma_cloud_name = None
            self.zia_cloud_name = None
            self.zt2_health_probe_interval = None
            self.device_posture_frequency = []
            self.zdx_manual_rollout = None
            self.win_zdx_lite_enabled = None

    def request_format(self):
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
            "disableParallelIpv4AndIPv6": self.disable_parallel_ipv4_and_ipv6,
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
            "winZdxLiteEnabled": self.win_zdx_lite_enabled
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class WebAppConfig(ZscalerObject):
    """
    A class for WebAppConfig objects.
    """

    def __init__(self, config=None):
        """
        Initialize the WebAppConfig model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.enable_fips_mode = config["enableFipsMode"] \
                if "enableFipsMode" in config else None
            self.device_cleanup = config["deviceCleanup"] \
                if "deviceCleanup" in config else None
            self.sync_time_hours = config["syncTimeHours"] \
                if "syncTimeHours" in config else None
            self.hide_non_fed_settings = config["hideNonFedSettings"] \
                if "hideNonFedSettings" in config else None
            self.hide_audit_logs = config["hideAuditLogs"] \
                if "hideAuditLogs" in config else None
            self.activate_policy = config["activatePolicy"] \
                if "activatePolicy" in config else None
            self.trusted_network = config["trustedNetwork"] \
                if "trustedNetwork" in config else None
            self.process_postures = config["processPostures"] \
                if "processPostures" in config else None
            self.zpa_reauth = config["zpaReauth"] \
                if "zpaReauth" in config else None
            self.inactive_device_cleanup = config["inactiveDeviceCleanup"] \
                if "inactiveDeviceCleanup" in config else None
            self.zpa_auth_username = config["zpaAuthUsername"] \
                if "zpaAuthUsername" in config else None
            self.machine_tunnel = config["machineTunnel"] \
                if "machineTunnel" in config else None
            self.cache_system_proxy = config["cacheSystemProxy"] \
                if "cacheSystemProxy" in config else None
            self.hide_dtls_support_settings = config["hideDTLSSupportSettings"] \
                if "hideDTLSSupportSettings" in config else None
            self.machine_token = config["machineToken"] \
                if "machineToken" in config else None
            self.application_bypass_info = config["applicationBypassInfo"] \
                if "applicationBypassInfo" in config else None
            self.tunnel_two_for_android_devices = config["tunnelTwoForAndroidDevices"] \
                if "tunnelTwoForAndroidDevices" in config else None
            self.tunnel_two_fori_os_devices = config["tunnelTwoForiOSDevices"] \
                if "tunnelTwoForiOSDevices" in config else None
            self.ownership_variable_posture = config["ownershipVariablePosture"] \
                if "ownershipVariablePosture" in config else None
            self.block_unreachable_domains_traffic_flag = config["blockUnreachableDomainsTrafficFlag"] \
                if "blockUnreachableDomainsTrafficFlag" in config else None
            self.prioritize_ipv4_over_ipv6 = config["prioritizeIPv4OverIpv6"] \
                if "prioritizeIPv4OverIpv6" in config else None
            self.crowd_strike_zta_score_visibility = config["crowdStrikeZTAScoreVisibility"] \
                if "crowdStrikeZTAScoreVisibility" in config else None
            self.notification_for_zpa_reauth_visibility = config["notificationForZPAReauthVisibility"] \
                if "notificationForZPAReauthVisibility" in config else None
            self.crl_check_visibility_flag = config["crlCheckVisibilityFlag"] \
                if "crlCheckVisibilityFlag" in config else None
            self.dedicated_proxy_ports_visibility = config["dedicatedProxyPortsVisibility"] \
                if "dedicatedProxyPortsVisibility" in config else None
            self.remote_fetch_logs = config["remoteFetchLogs"] \
                if "remoteFetchLogs" in config else None
            self.ms_defender_posture_visibility = config["msDefenderPostureVisibility"] \
                if "msDefenderPostureVisibility" in config else None
            self.exit_password_visibility = config["exitPasswordVisibility"] \
                if "exitPasswordVisibility" in config else None
            self.collect_zdx_location_visibility = config["collectZdxLocationVisibility"] \
                if "collectZdxLocationVisibility" in config else None
            self.use_v8_js_engine_visibility = config["useV8JsEngineVisibility"] \
                if "useV8JsEngineVisibility" in config else None
            self.zdx_disable_password_visibility = config["zdxDisablePasswordVisibility"] \
                if "zdxDisablePasswordVisibility" in config else None
            self.zad_disable_password_visibility = config["zadDisablePasswordVisibility"] \
                if "zadDisablePasswordVisibility" in config else None
            self.zpa_disable_password_visibility = config["zpaDisablePasswordVisibility"] \
                if "zpaDisablePasswordVisibility" in config else None
            self.default_protocol_for_zpa = config["defaultProtocolForZPA"] \
                if "defaultProtocolForZPA" in config else None
            self.drop_ipv6_traffic_visibility = config["dropIpv6TrafficVisibility"] \
                if "dropIpv6TrafficVisibility" in config else None
            self.mac_cache_system_proxy_visibility = config["macCacheSystemProxyVisibility"] \
                if "macCacheSystemProxyVisibility" in config else None
            self.use_wsa_poll_for_zpa = config["useWsaPollForZpa"] \
                if "useWsaPollForZpa" in config else None
            self.enable64_bit_feature = config["enable64BitFeature"] \
                if "enable64BitFeature" in config else None
            self.antivirus_posture_visibility = config["antivirusPostureVisibility"] \
                if "antivirusPostureVisibility" in config else None
            self.system_proxy_on_any_network_change_visibility = config["systemProxyOnAnyNetworkChangeVisibility"] \
                if "systemProxyOnAnyNetworkChangeVisibility" in config else None
            self.device_posture_os_version_visibility = config["devicePostureOsVersionVisibility"] \
                if "devicePostureOsVersionVisibility" in config else None
            self.sccm_config_visibility = config["sccmConfigVisibility"] \
                if "sccmConfigVisibility" in config else None
            self.browser_auth_flag_visibility = config["browserAuthFlagVisibility"] \
                if "browserAuthFlagVisibility" in config else None
            self.install_web_view2_flag_visibility = config["installWebView2FlagVisibility"] \
                if "installWebView2FlagVisibility" in config else None
            self.allow_web_view2_to_follow_s_p_visibility = config["allowWebView2ToFollowSPVisibility"] \
                if "allowWebView2ToFollowSPVisibility" in config else None
            self.auth_server_allow_list_imprivata_visibility = config
            ["authServerAllowListImprivataVisibility"] \
                if "authServerAllowListImprivataVisibility" in config else None
            self.enable_ipv6_resolution_for_zscaler_domains_visibility = config
            ["enableIpv6ResolutionForZscalerDomainsVisibility"] \
                if "enableIpv6ResolutionForZscalerDomainsVisibility" in config else None
            self.disable_reason_visibility = config["disableReasonVisibility"] \
                if "disableReasonVisibility" in config else None
            self.follow_routing_table_visibility = config["followRoutingTableVisibility"] \
                if "followRoutingTableVisibility" in config else None
            self.zia_device_posture_visibility = config["ziaDevicePostureVisibility"] \
                if "ziaDevicePostureVisibility" in config else None
            self.use_custom_dns = config["useCustomDNS"] \
                if "useCustomDNS" in config else None
            self.use_default_adapter_for_dns_visibility = config
            ["useDefaultAdapterForDNSVisibility"] \
                if "useDefaultAdapterForDNSVisibility" in config else None
            self.t2_fallback_block_all_traffic_and_tls_fallback = config
            ["t2FallbackBlockAllTrafficAndTlsFallback"] \
                if "t2FallbackBlockAllTrafficAndTlsFallback" in config else None
            self.override_t2_protocol_setting = config["overrideT2ProtocolSetting"] \
                if "overrideT2ProtocolSetting" in config else None
            self.grant_access_to_zscaler_log_folder_visibility = config
            ["grantAccessToZscalerLogFolderVisibility"] \
                if "grantAccessToZscalerLogFolderVisibility" in config else None
            self.admin_management_visibility = config["adminManagementVisibility"] \
                if "adminManagementVisibility" in config else None
            self.redirect_web_traffic_to_zcc_listening_proxy_visibility = config
            ["redirectWebTrafficToZccListeningProxyVisibility"] \
                if "redirectWebTrafficToZccListeningProxyVisibility" in config else None
            self.use_ztunnel2_0_for_proxied_web_traffic_visibility = config
            ["useZtunnel2_0ForProxiedWebTrafficVisibility"] \
                if "useZtunnel2_0ForProxiedWebTrafficVisibility" in config else None
            self.split_vpn_visibility = config["splitVpnVisibility"] \
                if "splitVpnVisibility" in config else None
            self.evaluate_trusted_network_visibility = config["evaluateTrustedNetworkVisibility"] \
                if "evaluateTrustedNetworkVisibility" in config else None
            self.vpn_adapters_configuration_visibility = config["vpnAdaptersConfigurationVisibility"] \
                if "vpnAdaptersConfigurationVisibility" in config else None
            self.vpn_services_visibility = config["vpnServicesVisibility"] \
                if "vpnServicesVisibility" in config else None
            self.skip_trusted_criteria_match_visibility = config["skipTrustedCriteriaMatchVisibility"] \
                if "skipTrustedCriteriaMatchVisibility" in config else None
            self.external_device_id_visibility = config["externalDeviceIdVisibility"] \
                if "externalDeviceIdVisibility" in config else None
            self.flow_logger_loopback_type_visibility = config["flowLoggerLoopbackTypeVisibility"] \
                if "flowLoggerLoopbackTypeVisibility" in config else None
            self.flow_logger_zpa_type_visibility = config["flowLoggerZPATypeVisibility"] \
                if "flowLoggerZPATypeVisibility" in config else None
            self.flow_logger_vpn_type_visibility = config["flowLoggerVPNTypeVisibility"] \
                if "flowLoggerVPNTypeVisibility" in config else None
            self.flow_logger_vpn_tunnel_type_visibility = config["flowLoggerVPNTunnelTypeVisibility"] \
                if "flowLoggerVPNTunnelTypeVisibility" in config else None
            self.flow_logger_direct_type_visibility = config["flowLoggerDirectTypeVisibility"] \
                if "flowLoggerDirectTypeVisibility" in config else None
            self.use_zscaler_notification_framework = config["useZscalerNotificationFramework"] \
                if "useZscalerNotificationFramework" in config else None
            self.fallback_to_gateway_domain = config["fallbackToGatewayDomain"] \
                if "fallbackToGatewayDomain" in config else None
            self.zcc_revert_visibility = config["zccRevertVisibility"] \
                if "zccRevertVisibility" in config else None
            self.force_zcc_revert_visibility = config["forceZccRevertVisibility"] \
                if "forceZccRevertVisibility" in config else None
            self.disaster_recovery_visibility = config["disasterRecoveryVisibility"] \
                if "disasterRecoveryVisibility" in config else None
            self.device_group_visibility = config["deviceGroupVisibility"] \
                if "deviceGroupVisibility" in config else None
            self.ip_v6_support_for_tunnel2 = config["ipV6SupportForTunnel2"] \
                if "ipV6SupportForTunnel2" in config else None
            self.path_mtu_discovery = config["pathMtuDiscovery"] \
                if "pathMtuDiscovery" in config else None
            self.posture_disc_encryption_visibility_for_linux = config["postureDiscEncryptionVisibilityForLinux"] \
                if "postureDiscEncryptionVisibilityForLinux" in config else None
            self.posture_ms_defender_visibility_for_linux = config["postureMsDefenderVisibilityForLinux"] \
                if "postureMsDefenderVisibilityForLinux" in config else None
            self.posture_os_version_visibility_for_linux = config["postureOsVersionVisibilityForLinux"] \
                if "postureOsVersionVisibilityForLinux" in config else None
            self.posture_crowd_strike_zta_score_visibility_for_linux = config
            ["postureCrowdStrikeZTAScoreVisibilityForLinux"] \
                if "postureCrowdStrikeZTAScoreVisibilityForLinux" in config else None
            self.flow_logger_zcc_blocked_traffic_visibility = config["flowLoggerZCCBlockedTrafficVisibility"] \
                if "flowLoggerZCCBlockedTrafficVisibility" in config else None
            self.flow_logger_intranet_traffic_visibility = config["flowLoggerIntranetTrafficVisibility"] \
                if "flowLoggerIntranetTrafficVisibility" in config else None
            self.custom_mtu_for_zpa_visibility = config["customMTUForZpaVisibility"] \
                if "customMTUForZpaVisibility" in config else None
            self.zpa_auto_reauth_timeout_visibility = config["zpaAutoReauthTimeoutVisibility"] \
                if "zpaAutoReauthTimeoutVisibility" in config else None
            self.force_zpa_auth_expire_visibility = config["forceZpaAuthExpireVisibility"] \
                if "forceZpaAuthExpireVisibility" in config else None
            self.enable_set_proxy_on_vpn_adapters_visibility = config
            ["enableSetProxyOnVPNAdaptersVisibility"] \
                if "enableSetProxyOnVPNAdaptersVisibility" in config else None
            self.dns_server_route_exclusion_visibility = config["dnsServerRouteExclusionVisibility"] \
                if "dnsServerRouteExclusionVisibility" in config else None
            self.enable_separate_otp_for_device = config["enableSeparateOtpForDevice"] \
                if "enableSeparateOtpForDevice" in config else None
            self.uninstall_password_for_profile_visibility = config["uninstallPasswordForProfileVisibility"] \
                if "uninstallPasswordForProfileVisibility" in config else None
            self.zpa_advance_reauth_visibility = config["zpaAdvanceReauthVisibility"] \
                if "zpaAdvanceReauthVisibility" in config else None
            self.latency_based_zen_enablement_visibility = config["latencyBasedZenEnablementVisibility"] \
                if "latencyBasedZenEnablementVisibility" in config else None
            self.dynamic_zpa_service_edge_assignmentt_visibility = config
            ["dynamicZPAServiceEdgeAssignmenttVisibility"] \
                if "dynamicZPAServiceEdgeAssignmenttVisibility" in config else None
            self.custom_proxy_ports_visibility = config["customProxyPortsVisibility"] \
                if "customProxyPortsVisibility" in config else None
            self.domain_inclusion_exclusion_for_dns_request_visibility = config
            ["domainInclusionExclusionForDNSRequestVisibility"] \
                if "domainInclusionExclusionForDNSRequestVisibility" in config else None
            self.app_notification_config_visibility = config["appNotificationConfigVisibility"] \
                if "appNotificationConfigVisibility" in config else None
            self.enable_anti_tampering_visibility = config["enableAntiTamperingVisibility"] \
                if "enableAntiTamperingVisibility" in config else None
            self.strict_enforcement_status_visibility = config["strictEnforcementStatusVisibility"] \
                if "strictEnforcementStatusVisibility" in config else None
            self.anti_tampering_otp_support_visibility = config["antiTamperingOtpSupportVisibility"] \
                if "antiTamperingOtpSupportVisibility" in config else None
            self.override_at_cmd_by_policy_visibility = config["overrideATCmdByPolicyVisibility"] \
                if "overrideATCmdByPolicyVisibility" in config else None
            self.device_trust_level_visibility = config["deviceTrustLevelVisibility"] \
                if "deviceTrustLevelVisibility" in config else None
            self.source_port_based_bypasses_visibility = config["sourcePortBasedBypassesVisibility"] \
                if "sourcePortBasedBypassesVisibility" in config else None
            self.process_based_application_bypass_visibility = config["processBasedApplicationBypassVisibility"] \
                if "processBasedApplicationBypassVisibility" in config else None
            self.custom_based_application_bypass_visibility = config["customBasedApplicationBypassVisibility"] \
                if "customBasedApplicationBypassVisibility" in config else None
            self.client_certificate_template_visibility = config["clientCertificateTemplateVisibility"] \
                if "clientCertificateTemplateVisibility" in config else None
            self.supported_zcc_version_chart_visibility = config["supportedZccVersionChartVisibility"] \
                if "supportedZccVersionChartVisibility" in config else None
            self.ios_ipv6_mode_visibility = config["iosIpv6ModeVisibility"] \
                if "iosIpv6ModeVisibility" in config else None
            self.device_group_multiple_postures_visibility = config["deviceGroupMultiplePosturesVisibility"] \
                if "deviceGroupMultiplePosturesVisibility" in config else None
            self.drop_non_zscaler_packets_visibility = config["dropNonZscalerPacketsVisibility"] \
                if "dropNonZscalerPacketsVisibility" in config else None
            self.zcc_synthetic_ip_range_visibility = config["zccSyntheticIPRangeVisibility"] \
                if "zccSyntheticIPRangeVisibility" in config else None
            self.device_posture_frequency_visibility = config["devicePostureFrequencyVisibility"] \
                if "devicePostureFrequencyVisibility" in config else None
            self.enforce_split_dns_visibility = config["enforceSplitDNSVisibility"] \
                if "enforceSplitDNSVisibility" in config else None
            self.data_protection_visibility = config["dataProtectionVisibility"] \
                if "dataProtectionVisibility" in config else None
            self.drop_quic_traffic_visibility = config["dropQuicTrafficVisibility"] \
                if "dropQuicTrafficVisibility" in config else None
            self.truncate_large_udpdns_response_visibility = config["truncateLargeUDPDNSResponseVisibility"] \
                if "truncateLargeUDPDNSResponseVisibility" in config else None
            self.prioritize_dns_exclusions_visibility = config["prioritizeDnsExclusionsVisibility"] \
                if "prioritizeDnsExclusionsVisibility" in config else None
            self.fetch_log_configuration_option_visibility = config["fetchLogConfigurationOptionVisibility"] \
                if "fetchLogConfigurationOptionVisibility" in config else None
            self.enable_serial_number_visibility = config["enableSerialNumberVisibility"] \
                if "enableSerialNumberVisibility" in config else None
            self.support_multiple_pwl_postures = config["supportMultiplePWLPostures"] \
                if "supportMultiplePWLPostures" in config else None
            self.restrict_remote_packet_capture_visibility = config["restrictRemotePacketCaptureVisibility"] \
                if "restrictRemotePacketCaptureVisibility" in config else None
            self.enable_application_based_bypass_for_mac_visibility = config
            ["enableApplicationBasedBypassForMacVisibility"] \
                if "enableApplicationBasedBypassForMacVisibility" in config else None
            self.remove_exempted_containers_visibility = config["removeExemptedContainersVisibility"] \
                if "removeExemptedContainersVisibility" in config else None
            self.captive_portal_detection_visibility = config["captivePortalDetectionVisibility"] \
                if "captivePortalDetectionVisibility" in config else None
            self.device_group_in_profile_visibility = config["deviceGroupInProfileVisibility"] \
                if "deviceGroupInProfileVisibility" in config else None
            self.update_dns_search_order = config["updateDnsSearchOrder"] \
                if "updateDnsSearchOrder" in config else None
            self.install_activity_based_monitoring_driver_visibility = config
            ["installActivityBasedMonitoringDriverVisibility"] \
                if "installActivityBasedMonitoringDriverVisibility" in config else None
            self.slow_rollout_zcc = config["slowRolloutZCC"] \
                if "slowRolloutZCC" in config else None
            self.zcc_tunnel_version_visibility = config["zccTunnelVersionVisibility"] \
                if "zccTunnelVersionVisibility" in config else None
            self.anti_tampering_status_visibility = config["antiTamperingStatusVisibility"] \
                if "antiTamperingStatusVisibility" in config else None
            self.lbb_threshold_rank_to_percent_mapping = config["lbbThresholdRankToPercentMapping"] \
                if "lbbThresholdRankToPercentMapping" in config else None
            self.remove_zscaler_ssl_cert_url = config["removeZscalerSslCertUrl"] \
                if "removeZscalerSslCertUrl" in config else None
            self.lbz_threshold_rank_to_percent_mapping = config["lbzThresholdRankToPercentMapping"] \
                if "lbzThresholdRankToPercentMapping" in config else None
            self.splash_screen_url = config["splashScreenUrl"] \
                if "splashScreenUrl" in config else None
            self.splash_screen_visibility = config["splashScreenVisibility"] \
                if "splashScreenVisibility" in config else None
            self.trusted_network_range_criteria_visibility = config["trustedNetworkRangeCriteriaVisibility"] \
                if "trustedNetworkRangeCriteriaVisibility" in config else None
            self.trusted_egress_ips_visibility = config["trustedEgressIpsVisibility"] \
                if "trustedEgressIpsVisibility" in config else None
            self.domain_profile_detection_visibility = config["domainProfileDetectionVisibility"] \
                if "domainProfileDetectionVisibility" in config else None
            self.all_inbound_traffic_visibility = config["allInboundTrafficVisibility"] \
                if "allInboundTrafficVisibility" in config else None
            self.export_logs_for_non_admin_visibility = config["exportLogsForNonAdminVisibility"] \
                if "exportLogsForNonAdminVisibility" in config else None
            self.enable_auto_log_snippet_visibility = config["enableAutoLogSnippetVisibility"] \
                if "enableAutoLogSnippetVisibility" in config else None
            self.enable_cli_visibility = config["enableCliVisibility"] \
                if "enableCliVisibility" in config else None
            self.zcc_user_type_visibility = config["zccUserTypeVisibility"] \
                if "zccUserTypeVisibility" in config else None
            self.install_windows_firewall_inbound_rule = config["installWindowsFirewallInboundRule"] \
                if "installWindowsFirewallInboundRule" in config else None
            self.retry_after_in_seconds = config["retryAfterInSeconds"] \
                if "retryAfterInSeconds" in config else None
            self.azure_a_d_posture_visibility = config["azureADPostureVisibility"] \
                if "azureADPostureVisibility" in config else None
            self.server_cert_posture_visibility = config["serverCertPostureVisibility"] \
                if "serverCertPostureVisibility" in config else None
            self.auto_fill_using_login_hint_visibility = config["autoFillUsingLoginHintVisibility"] \
                if "autoFillUsingLoginHintVisibility" in config else None
            self.send_default_policy_for_invalid_policy_token = config
            ["sendDefaultPolicyForInvalidPolicyToken"] \
                if "sendDefaultPolicyForInvalidPolicyToken" in config else None
            self.enable_zcc_password_settings = config["enableZccPasswordSettings"] \
                if "enableZccPasswordSettings" in config else None
            self.cli_password_expiry_minutes = config["cliPasswordExpiryMinutes"] \
                if "cliPasswordExpiryMinutes" in config else None
            self.sso_using_windows_primary_account = config["ssoUsingWindowsPrimaryAccount"] \
                if "ssoUsingWindowsPrimaryAccount" in config else None
            self.enable_verbose_log = config["enableVerboseLog"] \
                if "enableVerboseLog" in config else None
            self.zpa_auth_exp_on_win_logon_session = config["zpaAuthExpOnWinLogonSession"] \
                if "zpaAuthExpOnWinLogonSession" in config else None
            self.zpa_auth_exp_on_win_session_lock_visibility = config["zpaAuthExpOnWinSessionLockVisibility"] \
                if "zpaAuthExpOnWinSessionLockVisibility" in config else None
            self.enable_zcc_slow_rollout_by_default = config["enableZccSlowRolloutByDefault"] \
                if "enableZccSlowRolloutByDefault" in config else None
            self.purge_kerberos_preferred_dc_cache_visibility = config["purgeKerberosPreferredDCCacheVisibility"] \
                if "purgeKerberosPreferredDCCacheVisibility" in config else None
            self.posture_jamf_detection_visibility = config["postureJamfDetectionVisibility"] \
                if "postureJamfDetectionVisibility" in config else None
            self.posture_jamf_device_risk_visibility = config["postureJamfDeviceRiskVisibility"] \
                if "postureJamfDeviceRiskVisibility" in config else None
            self.windows_ap_captive_portal_detection_visibility = config["windowsAPCaptivePortalDetectionVisibility"] \
                if "windowsAPCaptivePortalDetectionVisibility" in config else None
            self.windows_ap_enable_fail_open_visibility = config["windowsAPEnableFailOpenVisibility"] \
                if "windowsAPEnableFailOpenVisibility" in config else None
            self.automatic_capture_duration = config["automaticCaptureDuration"] \
                if "automaticCaptureDuration" in config else None
            self.force_location_refresh_sccm = config["forceLocationRefreshSccm"] \
                if "forceLocationRefreshSccm" in config else None
            self.enable_posture_failure_dashboard = config["enablePostureFailureDashboard"] \
                if "enablePostureFailureDashboard" in config else None
            self.enable_one_id_phase2_changes = config["enableOneIDPhase2Changes"] \
                if "enableOneIDPhase2Changes" in config else None
            self.drop_ipv6_traffic_in_ipv6_network_visibility = config["dropIpv6TrafficInIpv6NetworkVisibility"] \
                if "dropIpv6TrafficInIpv6NetworkVisibility" in config else None
            self.enable_postures_for_partner = config["enablePosturesForPartner"] \
                if "enablePosturesForPartner" in config else None
            self.enable_partner_config_in_primary_policy = config["enablePartnerConfigInPrimaryPolicy"] \
                if "enablePartnerConfigInPrimaryPolicy" in config else None
            self.enable_one_id_admin_migration_changes = config["enableOneIDAdminMigrationChanges"] \
                if "enableOneIDAdminMigrationChanges" in config else None
            self.ddil_config_visibility = config["ddilConfigVisibility"] \
                if "ddilConfigVisibility" in config else None
            self.add_zdx_service_entitlement = config["addZDXServiceEntitlement"] \
                if "addZDXServiceEntitlement" in config else None
            self.use_zcdn = config["useZcdn"] \
                if "useZcdn" in config else None
            self.delete_dhcp_option121_routes_visibility = config["deleteDHCPOption121RoutesVisibility"] \
                if "deleteDHCPOption121RoutesVisibility" in config else None
            self.zdx_rollout_control_visibility = config["zdxRolloutControlVisibility"] \
                if "zdxRolloutControlVisibility" in config else None
            self.show_m365_services_in_app_bypasses = config["showM365ServicesInAppBypasses"] \
                if "showM365ServicesInAppBypasses" in config else None
            self.allow_web_view2_ignore_client_cert_errors = config["allowWebView2IgnoreClientCertErrors"] \
                if "allowWebView2IgnoreClientCertErrors" in config else None
            self.linux_rpm_build_visibility = config["linuxRPMBuildVisibility"] \
                if "linuxRPMBuildVisibility" in config else None
            self.help_banner_data_visibility = config["helpBannerDataVisibility"] \
                if "helpBannerDataVisibility" in config else None
            self.zpa_only_device_cleanup_visibility = config["zpaOnlyDeviceCleanupVisibility"] \
                if "zpaOnlyDeviceCleanupVisibility" in config else None
            self.app_profile_fail_open_policy_visibility = config["appProfileFailOpenPolicyVisibility"] \
                if "appProfileFailOpenPolicyVisibility" in config else None
            self.show_registry_option_in_enforce_and_none = config["showRegistryOptionInEnforceAndNone"] \
                if "showRegistryOptionInEnforceAndNone" in config else None
            self.strict_enforcement_notification_visibility = config["strictEnforcementNotificationVisibility"] \
                if "strictEnforcementNotificationVisibility" in config else None
            self.crowd_strike_zta_os_score_visibility = config["crowdStrikeZTAOsScoreVisibility"] \
                if "crowdStrikeZTAOsScoreVisibility" in config else None
            self.crowd_strike_zta_sensor_config_score_visibility = config["crowdStrikeZTASensorConfigScoreVisibility"] \
                if "crowdStrikeZTASensorConfigScoreVisibility" in config else None
            self.resize_window_to_fit_to_page_visibility = config["resizeWindowToFitToPageVisibility"] \
                if "resizeWindowToFitToPageVisibility" in config else None
            self.enable_zcc_fail_close_settings_for_se_mode = config["enableZCCFailCloseSettingsForSEMode"] \
                if "enableZCCFailCloseSettingsForSEMode" in config else None
        else:
            self.enable_fips_mode = None
            self.device_cleanup = None
            self.sync_time_hours = None
            self.hide_non_fed_settings = None
            self.hide_audit_logs = None
            self.activate_policy = None
            self.trusted_network = None
            self.process_postures = None
            self.zpa_reauth = None
            self.inactive_device_cleanup = None
            self.zpa_auth_username = None
            self.machine_tunnel = None
            self.cache_system_proxy = None
            self.hide_dtls_support_settings = None
            self.machine_token = None
            self.application_bypass_info = None
            self.tunnel_two_for_android_devices = None
            self.tunnel_two_fori_os_devices = None
            self.ownership_variable_posture = None
            self.block_unreachable_domains_traffic_flag = None
            self.prioritize_i_pv4_over_ipv6 = None
            self.crowd_strike_zta_score_visibility = None
            self.notification_for_zpa_reauth_visibility = None
            self.crl_check_visibility_flag = None
            self.dedicated_proxy_ports_visibility = None
            self.remote_fetch_logs = None
            self.ms_defender_posture_visibility = None
            self.exit_password_visibility = None
            self.collect_zdx_location_visibility = None
            self.use_v8_js_engine_visibility = None
            self.zdx_disable_password_visibility = None
            self.zad_disable_password_visibility = None
            self.zpa_disable_password_visibility = None
            self.default_protocol_for_zpa = None
            self.drop_ipv6_traffic_visibility = None
            self.mac_cache_system_proxy_visibility = None
            self.use_wsa_poll_for_zpa = None
            self.enable64_bit_feature = None
            self.antivirus_posture_visibility = None
            self.system_proxy_on_any_network_change_visibility = None
            self.device_posture_os_version_visibility = None
            self.sccm_config_visibility = None
            self.browser_auth_flag_visibility = None
            self.install_web_view2_flag_visibility = None
            self.allow_web_view2_to_follow_s_p_visibility = None
            self.auth_server_allow_list_imprivata_visibility = None
            self.enable_ipv6_resolution_for_zscaler_domains_visibility = None
            self.disable_reason_visibility = None
            self.follow_routing_table_visibility = None
            self.zia_device_posture_visibility = None
            self.use_custom_dns = None
            self.use_default_adapter_for_dns_visibility = None
            self.t2_fallback_block_all_traffic_and_tls_fallback = None
            self.override_t2_protocol_setting = None
            self.grant_access_to_zscaler_log_folder_visibility = None
            self.admin_management_visibility = None
            self.redirect_web_traffic_to_zcc_listening_proxy_visibility = None
            self.use_ztunnel2_0_for_proxied_web_traffic_visibility = None
            self.split_vpn_visibility = None
            self.evaluate_trusted_network_visibility = None
            self.vpn_adapters_configuration_visibility = None
            self.vpn_services_visibility = None
            self.skip_trusted_criteria_match_visibility = None
            self.external_device_id_visibility = None
            self.flow_logger_loopback_type_visibility = None
            self.flow_logger_zpa_type_visibility = None
            self.flow_logger_vpn_type_visibility = None
            self.flow_logger_vpn_tunnel_type_visibility = None
            self.flow_logger_direct_type_visibility = None
            self.use_zscaler_notification_framework = None
            self.fallback_to_gateway_domain = None
            self.zcc_revert_visibility = None
            self.force_zcc_revert_visibility = None
            self.disaster_recovery_visibility = None
            self.device_group_visibility = None
            self.ip_v6_support_for_tunnel2 = None
            self.path_mtu_discovery = None
            self.posture_disc_encryption_visibility_for_linux = None
            self.posture_ms_defender_visibility_for_linux = None
            self.posture_os_version_visibility_for_linux = None
            self.posture_crowd_strike_zta_score_visibility_for_linux = None
            self.flow_logger_zcc_blocked_traffic_visibility = None
            self.flow_logger_intranet_traffic_visibility = None
            self.custom_mtu_for_zpa_visibility = None
            self.zpa_auto_reauth_timeout_visibility = None
            self.force_zpa_auth_expire_visibility = None
            self.enable_set_proxy_on_v_p_n_adapters_visibility = None
            self.dns_server_route_exclusion_visibility = None
            self.enable_separate_otp_for_device = None
            self.uninstall_password_for_profile_visibility = None
            self.zpa_advance_reauth_visibility = None
            self.latency_based_zen_enablement_visibility = None
            self.dynamic_zpa_service_edge_assignmentt_visibility = None
            self.custom_proxy_ports_visibility = None
            self.domain_inclusion_exclusion_for_dns_request_visibility = None
            self.app_notification_config_visibility = None
            self.enable_anti_tampering_visibility = None
            self.strict_enforcement_status_visibility = None
            self.anti_tampering_otp_support_visibility = None
            self.override_at_cmd_by_policy_visibility = None
            self.device_trust_level_visibility = None
            self.source_port_based_bypasses_visibility = None
            self.process_based_application_bypass_visibility = None
            self.custom_based_application_bypass_visibility = None
            self.client_certificate_template_visibility = None
            self.supported_zcc_version_chart_visibility = None
            self.ios_ipv6_mode_visibility = None
            self.device_group_multiple_postures_visibility = None
            self.drop_non_zscaler_packets_visibility = None
            self.zcc_synthetic_i_p_range_visibility = None
            self.device_posture_frequency_visibility = None
            self.enforce_split_dns_visibility = None
            self.data_protection_visibility = None
            self.drop_quic_traffic_visibility = None
            self.truncate_large_udp_dns_response_visibility = None
            self.prioritize_dns_exclusions_visibility = None
            self.fetch_log_configuration_option_visibility = None
            self.enable_serial_number_visibility = None
            self.support_multiple_pwl_postures = None
            self.restrict_remote_packet_capture_visibility = None
            self.enable_application_based_bypass_for_mac_visibility = None
            self.remove_exempted_containers_visibility = None
            self.captive_portal_detection_visibility = None
            self.device_group_in_profile_visibility = None
            self.update_dns_search_order = None
            self.install_activity_based_monitoring_driver_visibility = None
            self.slow_rollout_zcc = None
            self.zcc_tunnel_version_visibility = None
            self.anti_tampering_status_visibility = None
            self.lbb_threshold_rank_to_percent_mapping = None
            self.remove_zscaler_ssl_cert_url = None
            self.lbz_threshold_rank_to_percent_mapping = None
            self.splash_screen_url = None
            self.splash_screen_visibility = None
            self.trusted_network_range_criteria_visibility = None
            self.trusted_egress_ips_visibility = None
            self.domain_profile_detection_visibility = None
            self.all_inbound_traffic_visibility = None
            self.export_logs_for_non_admin_visibility = None
            self.enable_auto_log_snippet_visibility = None
            self.enable_cli_visibility = None
            self.zcc_user_type_visibility = None
            self.install_windows_firewall_inbound_rule = None
            self.retry_after_in_seconds = None
            self.azure_ad_posture_visibility = None
            self.server_cert_posture_visibility = None
            self.auto_fill_using_login_hint_visibility = None
            self.send_default_policy_for_invalid_policy_token = None
            self.enable_zcc_password_settings = None
            self.cli_password_expiry_minutes = None
            self.sso_using_windows_primary_account = None
            self.enable_verbose_log = None
            self.zpa_auth_exp_on_win_logon_session = None
            self.zpa_auth_exp_on_win_session_lock_visibility = None
            self.enable_zcc_slow_rollout_by_default = None
            self.purge_kerberos_preferred_dc_cache_visibility = None
            self.posture_jamf_detection_visibility = None
            self.posture_jamf_device_risk_visibility = None
            self.windows_a_p_captive_portal_detection_visibility = None
            self.windows_a_p_enable_fail_open_visibility = None
            self.automatic_capture_duration = None
            self.force_location_refresh_sccm = None
            self.enable_posture_failure_dashboard = None
            self.enable_one_id_phase2_changes = None
            self.drop_ipv6_traffic_in_ipv6_network_visibility = None
            self.enable_postures_for_partner = None
            self.enable_partner_config_in_primary_policy = None
            self.enable_one_id_admin_migration_changes = None
            self.ddil_config_visibility = None
            self.add_zdx_service_entitlement = None
            self.use_zcdn = None
            self.delete_dhcp_option121_routes_visibility = None
            self.zdx_rollout_control_visibility = None
            self.show_m365_services_in_app_bypasses = None
            self.allow_web_view2_ignore_client_cert_errors = None
            self.linux_rpm_build_visibility = None
            self.help_banner_data_visibility = None
            self.zpa_only_device_cleanup_visibility = None
            self.app_profile_fail_open_policy_visibility = None
            self.show_registry_option_in_enforce_and_none = None
            self.strict_enforcement_notification_visibility = None
            self.crowd_strike_zta_os_score_visibility = None
            self.crowd_strike_zta_sensor_config_score_visibility = None
            self.resize_window_to_fit_to_page_visibility = None
            self.enable_zcc_fail_close_settings_for_se_mode = None

    def request_format(self):
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
            "allowWebView2ToFollowSPVisibility": self.allow_web_view2_to_follow_s_p_visibility,
            "authServerAllowListImprivataVisibility": self.auth_server_allow_list_imprivata_visibility,
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
            "enableSetProxyOnVPNAdaptersVisibility": self.enable_set_proxy_on_v_p_n_adapters_visibility,
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
            "zccSyntheticIPRangeVisibility": self.zcc_synthetic_i_p_range_visibility,
            "devicePostureFrequencyVisibility": self.device_posture_frequency_visibility,
            "enforceSplitDNSVisibility": self.enforce_split_dns_visibility,
            "dataProtectionVisibility": self.data_protection_visibility,
            "dropQuicTrafficVisibility": self.drop_quic_traffic_visibility,
            "truncateLargeUDPDNSResponseVisibility": self.truncate_large_udp_dns_response_visibility,
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
            "azureADPostureVisibility": self.azure_a_d_posture_visibility,
            "serverCertPostureVisibility": self.server_cert_posture_visibility,
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
            "windowsAPCaptivePortalDetectionVisibility": self.windows_a_p_captive_portal_detection_visibility,
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
            "enableZCCFailCloseSettingsForSEMode": self.enable_zcc_fail_close_settings_for_se_mode
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DevicePostureFrequency(ZscalerObject):
    """
    A class for DevicePostureFrequency objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DevicePostureFrequency model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.posture_id = config["postureId"] \
                if "postureId" in config else None
            self.posture_name = config["postureName"] \
                if "postureName" in config else None
            self.ios_value = config["iosValue"] \
                if "iosValue" in config else None
            self.android_value = config["androidValue"] \
                if "androidValue" in config else None
            self.windows_value = config["windowsValue"] \
                if "windowsValue" in config else None
            self.mac_value = config["macValue"] \
                if "macValue" in config else None
            self.linux_value = config["linuxValue"] \
                if "linuxValue" in config else None
            self.default_value = config["defaultValue"] \
                if "defaultValue" in config else None
        else:
            self.posture_id = None
            self.posture_name = None
            self.ios_value = None
            self.android_value = None
            self.windows_value = None
            self.mac_value = None
            self.linux_value = None
            self.default_value = None

    def request_format(self):
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
            "defaultValue": self.default_value
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
