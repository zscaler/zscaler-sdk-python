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


class WebPolicy(ZscalerObject):
    """
    A class for WebPolicy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the WebPolicy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.description = config["description"] if "description" in config else None
            self.allow_unreachable_pac = config["allowUnreachablePac"] if "allowUnreachablePac" in config else None
            self.android_policy = config["androidPolicy"] if "androidPolicy" in config else None
            self.device_type = config["device_type"] if "device_type" in config else None
            self.enable_device_groups = config["enableDeviceGroups"] if "enableDeviceGroups" in config else None
            self.forwarding_profile_id = config["forwardingProfileId"] if "forwardingProfileId" in config else None
            self.group_all = config["groupAll"] if "groupAll" in config else None
            self.highlight_active_control = config["highlightActiveControl"] if "highlightActiveControl" in config else None
            self.id = config["id"] if "id" in config else None
            self.ios_policy = config["iosPolicy"] if "iosPolicy" in config else None
            self.linux_policy = config["linuxPolicy"] if "linuxPolicy" in config else None
            self.log_file_size = config["logFileSize"] if "logFileSize" in config else None
            self.log_level = config["logLevel"] if "logLevel" in config else None
            self.log_mode = config["logMode"] if "logMode" in config else None
            self.mac_policy = config["macPolicy"] if "macPolicy" in config else None
            self.name = config["name"] if "name" in config else None
            self.pac_url = config["pac_url"] if "pac_url" in config else None
            self.reactivate_web_security_minutes = (
                config["reactivateWebSecurityMinutes"] if "reactivateWebSecurityMinutes" in config else None
            )
            self.reauth_period = config["reauth_period"] if "reauth_period" in config else None
            self.rule_order = config["ruleOrder"] if "ruleOrder" in config else None
            self.send_disable_service_reason = (
                config["sendDisableServiceReason"] if "sendDisableServiceReason" in config else None
            )
            self.tunnel_zapp_traffic = config["tunnelZappTraffic"] if "tunnelZappTraffic" in config else None
            self.windows_policy = config["windowsPolicy"] if "windowsPolicy" in config else None
            self.zia_posture_config_id = config["ziaPostureConfigId"] if "ziaPostureConfigId" in config else None

            self.app_identity_names = ZscalerCollection.form_list(
                config["appIdentityNames"] if "appIdentityNames" in config else [], str
            )
            self.app_service_ids = ZscalerCollection.form_list(
                config["appServiceIds"] if "appServiceIds" in config else [], str
            )
            self.app_service_names = ZscalerCollection.form_list(
                config["appServiceNames"] if "appServiceNames" in config else [], str
            )
            self.bypass_app_ids = ZscalerCollection.form_list(config["bypassAppIds"] if "bypassAppIds" in config else [], str)
            self.bypass_custom_app_ids = ZscalerCollection.form_list(
                config["bypassCustomAppIds"] if "bypassCustomAppIds" in config else [], str
            )

            self.device_group_ids = ZscalerCollection.form_list(
                config["deviceGroupIds"] if "deviceGroupIds" in config else [], str
            )
            self.device_group_names = ZscalerCollection.form_list(
                config["deviceGroupNames"] if "deviceGroupNames" in config else [], str
            )

            self.group_ids = ZscalerCollection.form_list(config["groupIds"] if "groupIds" in config else [], str)
            self.group_names = ZscalerCollection.form_list(config["groupNames"] if "groupNames" in config else [], str)

            self.user_ids = ZscalerCollection.form_list(config["userIds"] if "userIds" in config else [], str)
            self.user_names = ZscalerCollection.form_list(config["userNames"] if "userNames" in config else [], str)

            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], Users
            )

            if "policyExtension" in config:
                if isinstance(config["policyExtension"], PolicyExtension):
                    self.policy_extension = config["policyExtension"]
                elif config["policyExtension"] is not None:
                    self.policy_extension = PolicyExtension(config["policyExtension"])
                else:
                    self.policy_extension = None
            else:
                self.policy_extension = None

            if "disasterRecovery" in config:
                if isinstance(config["disasterRecovery"], DisasterRecovery):
                    self.disaster_recovery = config["disasterRecovery"]
                elif config["disasterRecovery"] is not None:
                    self.disaster_recovery = DisasterRecovery(config["disasterRecovery"])
                else:
                    self.disaster_recovery = None
            else:
                self.disaster_recovery = None

            if "onNetPolicy" in config:
                if isinstance(config["onNetPolicy"], OnNetPolicy):
                    self.on_net_policy = config["onNetPolicy"]
                elif config["onNetPolicy"] is not None:
                    self.on_net_policy = OnNetPolicy(config["onNetPolicy"])
                else:
                    self.on_net_policy = None
            else:
                self.on_net_policy = None
        else:
            self.active = None
            self.allow_unreachable_pac = None
            self.android_policy = None
            self.app_identity_names = ZscalerCollection.form_list([], str)
            self.app_service_ids = ZscalerCollection.form_list([], str)
            self.app_service_names = ZscalerCollection.form_list([], str)
            self.bypass_app_ids = ZscalerCollection.form_list([], str)
            self.bypass_custom_app_ids = ZscalerCollection.form_list([], str)
            self.description = None
            self.device_group_ids = ZscalerCollection.form_list([], str)
            self.device_group_names = ZscalerCollection.form_list([], str)
            self.device_type = None
            self.disaster_recovery = None
            self.enable_device_groups = None
            self.forwarding_profile_id = None
            self.group_all = None
            self.group_ids = ZscalerCollection.form_list([], str)
            self.group_names = ZscalerCollection.form_list([], str)
            self.highlight_active_control = None
            self.id = None
            self.ios_policy = None
            self.linux_policy = None
            self.log_file_size = None
            self.log_level = None
            self.log_mode = None
            self.mac_policy = None
            self.name = None
            self.pac_url = None
            self.policy_extension = None
            self.reactivate_web_security_minutes = None
            self.reauth_period = None
            self.rule_order = None
            self.send_disable_service_reason = None
            self.tunnel_zapp_traffic = None
            self.user_ids = ZscalerCollection.form_list([], str)
            self.user_names = ZscalerCollection.form_list([], str)
            self.windows_policy = None
            self.zia_posture_config_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "allowUnreachablePac": self.allow_unreachable_pac,
            "androidPolicy": self.android_policy,
            "appIdentityNames": self.app_identity_names,
            "appServiceIds": self.app_service_ids,
            "appServiceNames": self.app_service_names,
            "bypassAppIds": self.bypass_app_ids,
            "bypassCustomAppIds": self.bypass_custom_app_ids,
            "description": self.description,
            "deviceGroupIds": self.device_group_ids,
            "deviceGroupNames": self.device_group_names,
            "device_type": self.device_type,
            "disasterRecovery": self.disaster_recovery,
            "enableDeviceGroups": self.enable_device_groups,
            "forwardingProfileId": self.forwarding_profile_id,
            "groupAll": self.group_all,
            "groupIds": self.group_ids,
            "groupNames": self.group_names,
            "highlightActiveControl": self.highlight_active_control,
            "id": self.id,
            "iosPolicy": self.ios_policy,
            "linuxPolicy": self.linux_policy,
            "logFileSize": self.log_file_size,
            "logLevel": self.log_level,
            "logMode": self.log_mode,
            "macPolicy": self.mac_policy,
            "name": self.name,
            "pac_url": self.pac_url,
            "policyExtension": self.policy_extension,
            "reactivateWebSecurityMinutes": self.reactivate_web_security_minutes,
            "reauth_period": self.reauth_period,
            "ruleOrder": self.rule_order,
            "sendDisableServiceReason": self.send_disable_service_reason,
            "tunnelZappTraffic": self.tunnel_zapp_traffic,
            "userIds": self.user_ids,
            "userNames": self.user_names,
            "windowsPolicy": self.windows_policy,
            "ziaPostureConfigId": self.zia_posture_config_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PolicyExtension(ZscalerObject):
    """
    A class for PolicyExtension objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PolicyExtension model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.source_port_based_bypasses = config["sourcePortBasedBypasses"] \
                if "sourcePortBasedBypasses" in config else None
            self.vpn_gateways = config["vpnGateways"] \
                if "vpnGateways" in config else None
            self.packet_tunnel_exclude_list = config["packetTunnelExcludeList"] \
                if "packetTunnelExcludeList" in config else None
            self.packet_tunnel_include_list = config["packetTunnelIncludeList"] \
                if "packetTunnelIncludeList" in config else None
            self.packet_tunnel_dns_include_list = config["packetTunnelDnsIncludeList"] \
                if "packetTunnelDnsIncludeList" in config else None
            self.packet_tunnel_dns_exclude_list = config["packetTunnelDnsExcludeList"] \
                if "packetTunnelDnsExcludeList" in config else None
            self.nonce = config["nonce"] \
                if "nonce" in config else None
            self.machine_idp_auth = config["machineIdpAuth"] \
                if "machineIdpAuth" in config else None
            self.exit_password = config["exitPassword"] \
                if "exitPassword" in config else None
            self.use_v8_js_engine = config["useV8JsEngine"] \
                if "useV8JsEngine" in config else None
            self.zdx_disable_password = config["zdxDisablePassword"] \
                if "zdxDisablePassword" in config else None
            self.zd_disable_password = config["zdDisablePassword"] \
                if "zdDisablePassword" in config else None
            self.zpa_disable_password = config["zpaDisablePassword"] \
                if "zpaDisablePassword" in config else None
            self.zdp_disable_password = config["zdpDisablePassword"] \
                if "zdpDisablePassword" in config else None
            self.follow_routing_table = config["followRoutingTable"] \
                if "followRoutingTable" in config else None
            self.use_wsa_poll_for_zpa = config["useWsaPollForZpa"] \
                if "useWsaPollForZpa" in config else None
            self.use_default_adapter_for_dns = config["useDefaultAdapterForDNS"] \
                if "useDefaultAdapterForDNS" in config else None
            self.use_zscaler_notification_framework = config["useZscalerNotificationFramework"] \
                if "useZscalerNotificationFramework" in config else None
            self.switch_focus_to_notification = config["switchFocusToNotification"] \
                if "switchFocusToNotification" in config else None
            self.fallback_to_gateway_domain = config["fallbackToGatewayDomain"] \
                if "fallbackToGatewayDomain" in config else None
            self.enable_zcc_revert = config["enableZCCRevert"] \
                if "enableZCCRevert" in config else None
            self.zcc_revert_password = config["zccRevertPassword"] \
                if "zccRevertPassword" in config else None
            self.zpa_auth_exp_on_sleep = config["zpaAuthExpOnSleep"] \
                if "zpaAuthExpOnSleep" in config else None
            self.zpa_auth_exp_on_sys_restart = config["zpaAuthExpOnSysRestart"] \
                if "zpaAuthExpOnSysRestart" in config else None
            self.zpa_auth_exp_on_net_ip_change = config["zpaAuthExpOnNetIpChange"] \
                if "zpaAuthExpOnNetIpChange" in config else None
            self.zpa_auth_exp_on_win_logon_session = config["zpaAuthExpOnWinLogonSession"] \
                if "zpaAuthExpOnWinLogonSession" in config else None
            self.zpa_auth_exp_on_win_session_lock = config["zpaAuthExpOnWinSessionLock"] \
                if "zpaAuthExpOnWinSessionLock" in config else None
            self.zpa_auth_exp_session_lock_state_min_time_in_second = config["zpaAuthExpSessionLockStateMinTimeInSecond"] \
                if "zpaAuthExpSessionLockStateMinTimeInSecond" in config else None
            self.packet_tunnel_exclude_list_for_ipv6 = config["packetTunnelExcludeListForIPv6"] \
                if "packetTunnelExcludeListForIPv6" in config else None
            self.packet_tunnel_include_list_for_ipv6 = config["packetTunnelIncludeListForIPv6"] \
                if "packetTunnelIncludeListForIPv6" in config else None
            self.enable_set_proxy_on_vpn_adapters = config["enableSetProxyOnVPNAdapters"] \
                if "enableSetProxyOnVPNAdapters" in config else None
            self.disable_dns_route_exclusion = config["disableDNSRouteExclusion"] \
                if "disableDNSRouteExclusion" in config else None
            self.advance_zpa_reauth = config["advanceZpaReauth"] \
                if "advanceZpaReauth" in config else None
            self.use_proxy_port_for_t1 = config["useProxyPortForT1"] \
                if "useProxyPortForT1" in config else None
            self.use_proxy_port_for_t2 = config["useProxyPortForT2"] \
                if "useProxyPortForT2" in config else None
            self.intercept_zia_traffic_all_adapters = config["interceptZIATrafficAllAdapters"] \
                if "interceptZIATrafficAllAdapters" in config else None
            self.enable_anti_tampering = config["enableAntiTampering"] \
                if "enableAntiTampering" in config else None
            self.override_a_t_cmd_by_policy = config["overrideATCmdByPolicy"] \
                if "overrideATCmdByPolicy" in config else None
            self.reactivate_anti_tampering_time = config["reactivateAntiTamperingTime"] \
                if "reactivateAntiTamperingTime" in config else None
            self.enforce_split_dns = config["enforceSplitDNS"] \
                if "enforceSplitDNS" in config else None
            self.drop_quic_traffic = config["dropQuicTraffic"] \
                if "dropQuicTraffic" in config else None
            self.enable_zdp_service = config["enableZdpService"] \
                if "enableZdpService" in config else None
            self.update_dns_search_order = config["updateDnsSearchOrder"] \
                if "updateDnsSearchOrder" in config else None
            self.truncate_large_udpdns_response = config["truncateLargeUDPDNSResponse"] \
                if "truncateLargeUDPDNSResponse" in config else None
            self.prioritize_dns_exclusions = config["prioritizeDnsExclusions"] \
                if "prioritizeDnsExclusions" in config else None
            self.purge_kerberos_preferred_dc_cache = config["purgeKerberosPreferredDCCache"] \
                if "purgeKerberosPreferredDCCache" in config else None
            self.delete_dhcp_option121_routes = config["deleteDHCPOption121Routes"] \
                if "deleteDHCPOption121Routes" in config else None
            self.generate_cli_password_contract = config["generateCliPasswordContract"] \
                if "generateCliPasswordContract" in config else None
            self.zdx_lite_config_obj = config["zdxLiteConfigObj"] \
                if "zdxLiteConfigObj" in config else None
            self.ddil_config = config["ddilConfig"] \
                if "ddilConfig" in config else None
            self.zcc_fail_close_settings_exit_uninstall_password = config
            ["zccFailCloseSettingsExitUninstallPassword"] \
                if "zccFailCloseSettingsExitUninstallPassword" in config else None
            self.zcc_fail_close_settings_lockdown_on_tunnel_process_exit = config
            ["zccFailCloseSettingsLockdownOnTunnelProcessExit"] \
                if "zccFailCloseSettingsLockdownOnTunnelProcessExit" in config else None
            self.zcc_fail_close_settings_lockdown_on_firewall_error = config
            ["zccFailCloseSettingsLockdownOnFirewallError"] \
                if "zccFailCloseSettingsLockdownOnFirewallError" in config else None
            self.zcc_fail_close_settings_lockdown_on_driver_error = config
            ["zccFailCloseSettingsLockdownOnDriverError"] \
                if "zccFailCloseSettingsLockdownOnDriverError" in config else None
            self.zcc_fail_close_settings_thumb_print = config["zccFailCloseSettingsThumbPrint"] \
                if "zccFailCloseSettingsThumbPrint" in config else None
            self.zcc_app_fail_open_policy = config["zccAppFailOpenPolicy"] \
                if "zccAppFailOpenPolicy" in config else None
            self.zcc_tunnel_fail_policy = config["zccTunnelFailPolicy"] \
                if "zccTunnelFailPolicy" in config else None
            self.follow_global_for_partner_login = config["followGlobalForPartnerLogin"] \
                if "followGlobalForPartnerLogin" in config else None
            self.user_allowed_to_add_partner = config["userAllowedToAddPartner"] \
                if "userAllowedToAddPartner" in config else None
            self.allow_client_cert_caching_for_web_view2 = config["allowClientCertCachingForWebView2"] \
                if "allowClientCertCachingForWebView2" in config else None
            self.show_confirmation_dialog_for_cached_cert = config["showConfirmationDialogForCachedCert"] \
                if "showConfirmationDialogForCachedCert" in config else None
            self.enable_flow_based_tunnel = config["enableFlowBasedTunnel"] \
                if "enableFlowBasedTunnel" in config else None

        else:
            self.source_port_based_bypasses = None
            self.vpn_gateways = None
            self.packet_tunnel_exclude_list = None
            self.packet_tunnel_include_list = None
            self.packet_tunnel_dns_include_list = None
            self.packet_tunnel_dns_exclude_list = None
            self.nonce = None
            self.machine_idp_auth = None
            self.exit_password = None
            self.use_v8_js_engine = None
            self.zdx_disable_password = None
            self.zd_disable_password = None
            self.zpa_disable_password = None
            self.zdp_disable_password = None
            self.follow_routing_table = None
            self.use_wsa_poll_for_zpa = None
            self.use_default_adapter_for_dns = None
            self.use_zscaler_notification_framework = None
            self.switch_focus_to_notification = None
            self.fallback_to_gateway_domain = None
            self.enable_zcc_revert = None
            self.zcc_revert_password = None
            self.zpa_auth_exp_on_sleep = None
            self.zpa_auth_exp_on_sys_restart = None
            self.zpa_auth_exp_on_net_ip_change = None
            self.zpa_auth_exp_on_win_logon_session = None
            self.zpa_auth_exp_on_win_session_lock = None
            self.zpa_auth_exp_session_lock_state_min_time_in_second = None
            self.packet_tunnel_exclude_list_for_ipv6 = None
            self.packet_tunnel_include_list_for_ipv6 = None
            self.enable_set_proxy_on_vpn_adapters = None
            self.disable_dns_route_exclusion = None
            self.advance_zpa_reauth = None
            self.use_proxy_port_for_t1 = None
            self.use_proxy_port_for_t2 = None
            self.intercept_zia_traffic_all_adapters = None
            self.enable_anti_tampering = None
            self.override_a_t_cmd_by_policy = None
            self.reactivate_anti_tampering_time = None
            self.enforce_split_dns = None
            self.drop_quic_traffic = None
            self.enable_zdp_service = None
            self.update_dns_search_order = None
            self.truncate_large_udpdns_response = None
            self.prioritize_dns_exclusions = None
            self.purge_kerberos_preferred_d_c_cache = None
            self.delete_dhcp_option121_routes = None
            self.generate_cli_password_contract = None
            self.zdx_lite_config_obj = None
            self.ddil_config = None
            self.zcc_fail_close_settings_exit_uninstall_password = None
            self.zcc_fail_close_settings_lockdown_on_tunnel_process_exit = None
            self.zcc_fail_close_settings_lockdown_on_firewall_error = None
            self.zcc_fail_close_settings_lockdown_on_driver_error = None
            self.zcc_fail_close_settings_thumb_print = None
            self.zcc_app_fail_open_policy = None
            self.zcc_tunnel_fail_policy = None
            self.follow_global_for_partner_login = None
            self.user_allowed_to_add_partner = None
            self.allow_client_cert_caching_for_web_view2 = None
            self.show_confirmation_dialog_for_cached_cert = None
            self.enable_flow_based_tunnel = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "sourcePortBasedBypasses": self.source_port_based_bypasses,
            "vpnGateways": self.vpn_gateways,
            "packetTunnelExcludeList": self.packet_tunnel_exclude_list,
            "packetTunnelIncludeList": self.packet_tunnel_include_list,
            "packetTunnelDnsIncludeList": self.packet_tunnel_dns_include_list,
            "packetTunnelDnsExcludeList": self.packet_tunnel_dns_exclude_list,
            "nonce": self.nonce,
            "machineIdpAuth": self.machine_idp_auth,
            "exitPassword": self.exit_password,
            "useV8JsEngine": self.use_v8_js_engine,
            "zdxDisablePassword": self.zdx_disable_password,
            "zdDisablePassword": self.zd_disable_password,
            "zpaDisablePassword": self.zpa_disable_password,
            "zdpDisablePassword": self.zdp_disable_password,
            "followRoutingTable": self.follow_routing_table,
            "useWsaPollForZpa": self.use_wsa_poll_for_zpa,
            "useDefaultAdapterForDNS": self.use_default_adapter_for_dns,
            "useZscalerNotificationFramework": self.use_zscaler_notification_framework,
            "switchFocusToNotification": self.switch_focus_to_notification,
            "fallbackToGatewayDomain": self.fallback_to_gateway_domain,
            "enableZCCRevert": self.enable_zcc_revert,
            "zccRevertPassword": self.zcc_revert_password,
            "zpaAuthExpOnSleep": self.zpa_auth_exp_on_sleep,
            "zpaAuthExpOnSysRestart": self.zpa_auth_exp_on_sys_restart,
            "zpaAuthExpOnNetIpChange": self.zpa_auth_exp_on_net_ip_change,
            "zpaAuthExpOnWinLogonSession": self.zpa_auth_exp_on_win_logon_session,
            "zpaAuthExpOnWinSessionLock": self.zpa_auth_exp_on_win_session_lock,
            "zpaAuthExpSessionLockStateMinTimeInSecond": self.zpa_auth_exp_session_lock_state_min_time_in_second,
            "packetTunnelExcludeListForIPv6": self.packet_tunnel_exclude_list_for_ipv6,
            "packetTunnelIncludeListForIPv6": self.packet_tunnel_include_list_for_ipv6,
            "enableSetProxyOnVPNAdapters": self.enable_set_proxy_on_vpn_adapters,
            "disableDNSRouteExclusion": self.disable_dns_route_exclusion,
            "advanceZpaReauth": self.advance_zpa_reauth,
            "useProxyPortForT1": self.use_proxy_port_for_t1,
            "useProxyPortForT2": self.use_proxy_port_for_t2,
            "interceptZIATrafficAllAdapters": self.intercept_zia_traffic_all_adapters,
            "enableAntiTampering": self.enable_anti_tampering,
            "overrideATCmdByPolicy": self.override_a_t_cmd_by_policy,
            "reactivateAntiTamperingTime": self.reactivate_anti_tampering_time,
            "enforceSplitDNS": self.enforce_split_dns,
            "dropQuicTraffic": self.drop_quic_traffic,
            "enableZdpService": self.enable_zdp_service,
            "updateDnsSearchOrder": self.update_dns_search_order,
            "truncateLargeUDPDNSResponse": self.truncate_large_udpdns_response,
            "prioritizeDnsExclusions": self.prioritize_dns_exclusions,
            "purgeKerberosPreferredDCCache": self.purge_kerberos_preferred_d_c_cache,
            "deleteDHCPOption121Routes": self.delete_dhcp_option121_routes,
            "generateCliPasswordContract": self.generate_cli_password_contract,
            "zdxLiteConfigObj": self.zdx_lite_config_obj,
            "ddilConfig": self.ddil_config,
            "zccFailCloseSettingsExitUninstallPassword": self.zcc_fail_close_settings_exit_uninstall_password,
            "zccFailCloseSettingsLockdownOnTunnelProcessExit": self.zcc_fail_close_settings_lockdown_on_tunnel_process_exit,
            "zccFailCloseSettingsLockdownOnFirewallError": self.zcc_fail_close_settings_lockdown_on_firewall_error,
            "zccFailCloseSettingsLockdownOnDriverError": self.zcc_fail_close_settings_lockdown_on_driver_error,
            "zccFailCloseSettingsThumbPrint": self.zcc_fail_close_settings_thumb_print,
            "zccAppFailOpenPolicy": self.zcc_app_fail_open_policy,
            "zccTunnelFailPolicy": self.zcc_tunnel_fail_policy,
            "followGlobalForPartnerLogin": self.follow_global_for_partner_login,
            "userAllowedToAddPartner": self.user_allowed_to_add_partner,
            "allowClientCertCachingForWebView2": self.allow_client_cert_caching_for_web_view2,
            "showConfirmationDialogForCachedCert": self.show_confirmation_dialog_for_cached_cert,
            "enableFlowBasedTunnel": self.enable_flow_based_tunnel,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DisasterRecovery(ZscalerObject):
    """
    A class for DisasterRecovery objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DisasterRecovery model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.enable_zia_dr = config["enableZiaDR"] \
                if "enableZiaDR" in config else None
            self.enable_zpa_dr = config["enableZpaDR"] \
                if "enableZpaDR" in config else None
            self.zia_dr_method = config["ziaDRMethod"] \
                if "ziaDRMethod" in config else None
            self.zia_custom_db_url = config["ziaCustomDbUrl"] \
                if "ziaCustomDbUrl" in config else None
            self.use_zia_global_db = config["useZiaGlobalDb"] \
                if "useZiaGlobalDb" in config else None
            self.zia_global_db_url = config["ziaGlobalDbUrl"] \
                if "ziaGlobalDbUrl" in config else None
            self.zia_global_db_urlv2 = config["ziaGlobalDbUrlv2"] \
                if "ziaGlobalDbUrlv2" in config else None
            self.zia_domain_name = config["ziaDomainName"] \
                if "ziaDomainName" in config else None
            self.zia_rsa_pub_key_name = config["ziaRSAPubKeyName"] \
                if "ziaRSAPubKeyName" in config else None
            self.zia_rsa_pub_key = config["ziaRSAPubKey"] \
                if "ziaRSAPubKey" in config else None
            self.zpa_domain_name = config["zpaDomainName"] \
                if "zpaDomainName" in config else None
            self.zpa_rsa_pub_key_name = config["zpaRSAPubKeyName"] \
                if "zpaRSAPubKeyName" in config else None
            self.zpa_rsa_pub_key = config["zpaRSAPubKey"] \
                if "zpaRSAPubKey" in config else None
            self.allow_zia_test = config["allowZiaTest"] \
                if "allowZiaTest" in config else None
            self.allow_zpa_test = config["allowZpaTest"] \
                if "allowZpaTest" in config else None
        else:
            self.enable_zia_dr = None
            self.enable_zpa_dr = None
            self.zia_dr_method = None
            self.zia_custom_db_url = None
            self.use_zia_global_db = None
            self.zia_global_db_url = None
            self.zia_global_db_urlv2 = None
            self.zia_domain_name = None
            self.zia_rsa_pub_key_name = None
            self.zia_rsa_pub_key = None
            self.zpa_domain_name = None
            self.zpa_rsa_pub_key_name = None
            self.zpa_rsa_pub_key = None
            self.allow_zia_test = None
            self.allow_zpa_test = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "enableZiaDR": self.enable_zia_dr,
            "enableZpaDR": self.enable_zpa_dr,
            "ziaDRMethod": self.zia_dr_method,
            "ziaCustomDbUrl": self.zia_custom_db_url,
            "useZiaGlobalDb": self.use_zia_global_db,
            "ziaGlobalDbUrl": self.zia_global_db_url,
            "ziaGlobalDbUrlv2": self.zia_global_db_urlv2,
            "ziaDomainName": self.zia_domain_name,
            "ziaRSAPubKeyName": self.zia_rsa_pub_key_name,
            "ziaRSAPubKey": self.zia_rsa_pub_key,
            "zpaDomainName": self.zpa_domain_name,
            "zpaRSAPubKeyName": self.zpa_rsa_pub_key_name,
            "zpaRSAPubKey": self.zpa_rsa_pub_key,
            "allowZiaTest": self.allow_zia_test,
            "allowZpaTest": self.allow_zpa_test
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class OnNetPolicy(ZscalerObject):
    """
    A class for OnNetPolicy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the OnNetPolicy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.condition_type = config["conditionType"] \
                if "conditionType" in config else None
            self.predefined_trusted_networks = config["predefinedTrustedNetworks"] \
                if "predefinedTrustedNetworks" in config else None
            self.predefined_tn_all = config["predefinedTnAll"] \
                if "predefinedTnAll" in config else None
        else:
            self.id = None
            self.name = None
            self.condition_type = None
            self.predefined_trusted_networks = None
            self.predefined_tn_all = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "conditionType": self.condition_type,
            "predefinedTrustedNetworks": self.predefined_trusted_networks,
            "predefinedTnAll": self.predefined_tn_all
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Users(ZscalerObject):
    """
    A class for Users objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Users model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.login_name = config["loginName"] \
                if "loginName" in config else None
            self.last_modification = config["lastModification"] \
                if "lastModification" in config else None
            self.active = config["active"] \
                if "active" in config else None
            self.company_id = config["companyId"] \
                if "companyId" in config else None
        else:
            self.id = None
            self.login_name = None
            self.last_modification = None
            self.active = None
            self.company_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "loginName": self.login_name,
            "lastModification": self.last_modification,
            "active": self.active,
            "companyId": self.company_id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
