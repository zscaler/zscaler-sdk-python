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
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class ApplicationProfile(ZscalerObject):
    """
    A class for ApplicationProfile objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ApplicationProfile model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.device_type = config["deviceType"] if "deviceType" in config else None
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.pac_url = config["pac_url"] if "pac_url" in config else None
            self.active = config["active"] if "active" in config else None
            self.rule_order = config["ruleOrder"] if "ruleOrder" in config else None
            self.log_mode = config["logMode"] if "logMode" in config else None
            self.log_level = config["logLevel"] if "logLevel" in config else None
            self.log_file_size = config["logFileSize"] if "logFileSize" in config else None
            self.reauth_period = config["reauth_period"] if "reauth_period" in config else None
            self.reactivate_web_security_minutes = (
                config["reactivateWebSecurityMinutes"] if "reactivateWebSecurityMinutes" in config else None
            )
            self.highlight_active_control = config["highlightActiveControl"] if "highlightActiveControl" in config else None
            self.send_disable_service_reason = (
                config["sendDisableServiceReason"] if "sendDisableServiceReason" in config else None
            )
            self.refresh_kerberos_token = config["refreshKerberosToken"] if "refreshKerberosToken" in config else None
            self.enable_device_groups = config["enableDeviceGroups"] if "enableDeviceGroups" in config else None

            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], ApplicationPolicyGroup)
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], ApplicationPolicyGroup
            )

            self.on_net_policy = config["onNetPolicy"] if "onNetPolicy" in config else None
            self.notification_template_contract = (
                config["notificationTemplateContract"] if "notificationTemplateContract" in config else None
            )
            self.notification_template_id = config["notificationTemplateId"] if "notificationTemplateId" in config else None
            self.forwarding_profile_id = config["forwardingProfileId"] if "forwardingProfileId" in config else None
            self.zia_posture_config_id = config["ziaPostureConfigId"] if "ziaPostureConfigId" in config else None
            self.policy_token = config["policyToken"] if "policyToken" in config else None
            self.tunnel_zapp_traffic = config["tunnelZappTraffic"] if "tunnelZappTraffic" in config else None
            self.group_all = config["groupAll"] if "groupAll" in config else None

            self.users = ZscalerCollection.form_list(config["users"] if "users" in config else [], ApplicationPolicyUser)

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

            self.zia_posture_config = config["ziaPostureConfig"] if "ziaPostureConfig" in config else None

            self.group_ids = ZscalerCollection.form_list(config["groupIds"] if "groupIds" in config else [], str)
            self.device_group_ids = ZscalerCollection.form_list(
                config["deviceGroupIds"] if "deviceGroupIds" in config else [], str
            )
            self.user_ids = ZscalerCollection.form_list(config["userIds"] if "userIds" in config else [], str)
            self.bypass_app_ids = ZscalerCollection.form_list(config["bypassAppIds"] if "bypassAppIds" in config else [], str)
            self.app_service_ids = ZscalerCollection.form_list(
                config["appServiceIds"] if "appServiceIds" in config else [], str
            )
            self.bypass_custom_app_ids = ZscalerCollection.form_list(
                config["bypassCustomAppIds"] if "bypassCustomAppIds" in config else [], str
            )

            self.bypass_apps = config["bypassApps"] if "bypassApps" in config else None
            self.bypass_custom_apps = config["bypassCustomApps"] if "bypassCustomApps" in config else None

            self.app_services = ZscalerCollection.form_list(
                config["appServices"] if "appServices" in config else [], AppService
            )

            self.passcode = config["passcode"] if "passcode" in config else None
            self.logout_password = config["logout_password"] if "logout_password" in config else None
            self.disable_password = config["disable_password"] if "disable_password" in config else None
            self.uninstall_password = config["uninstall_password"] if "uninstall_password" in config else None
            self.show_vpn_tun_notification = config["showVPNTunNotification"] if "showVPNTunNotification" in config else None
            self.use_tunnel_sdk4_3 = config["useTunnelSDK4_3"] if "useTunnelSDK4_3" in config else None
            self.ipv6_mode = config["ipv6Mode"] if "ipv6Mode" in config else None
        else:
            self.device_type = None
            self.id = None
            self.name = None
            self.description = None
            self.pac_url = None
            self.active = None
            self.rule_order = None
            self.log_mode = None
            self.log_level = None
            self.log_file_size = None
            self.reauth_period = None
            self.reactivate_web_security_minutes = None
            self.highlight_active_control = None
            self.send_disable_service_reason = None
            self.refresh_kerberos_token = None
            self.enable_device_groups = None
            self.groups = ZscalerCollection.form_list([], ApplicationPolicyGroup)
            self.device_groups = ZscalerCollection.form_list([], ApplicationPolicyGroup)
            self.on_net_policy = None
            self.notification_template_contract = None
            self.notification_template_id = None
            self.forwarding_profile_id = None
            self.zia_posture_config_id = None
            self.policy_token = None
            self.tunnel_zapp_traffic = None
            self.group_all = None
            self.users = ZscalerCollection.form_list([], ApplicationPolicyUser)
            self.policy_extension = None
            self.disaster_recovery = None
            self.zia_posture_config = None
            self.group_ids = ZscalerCollection.form_list([], str)
            self.device_group_ids = ZscalerCollection.form_list([], str)
            self.user_ids = ZscalerCollection.form_list([], str)
            self.bypass_app_ids = ZscalerCollection.form_list([], str)
            self.app_service_ids = ZscalerCollection.form_list([], str)
            self.bypass_custom_app_ids = ZscalerCollection.form_list([], str)
            self.bypass_apps = None
            self.bypass_custom_apps = None
            self.app_services = ZscalerCollection.form_list([], AppService)
            self.passcode = None
            self.logout_password = None
            self.disable_password = None
            self.uninstall_password = None
            self.show_vpn_tun_notification = None
            self.use_tunnel_sdk4_3 = None
            self.ipv6_mode = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "deviceType": self.device_type,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "pac_url": self.pac_url,
            "active": self.active,
            "ruleOrder": self.rule_order,
            "logMode": self.log_mode,
            "logLevel": self.log_level,
            "logFileSize": self.log_file_size,
            "reauth_period": self.reauth_period,
            "reactivateWebSecurityMinutes": self.reactivate_web_security_minutes,
            "highlightActiveControl": self.highlight_active_control,
            "sendDisableServiceReason": self.send_disable_service_reason,
            "refreshKerberosToken": self.refresh_kerberos_token,
            "enableDeviceGroups": self.enable_device_groups,
            "groups": self.groups,
            "deviceGroups": self.device_groups,
            "onNetPolicy": self.on_net_policy,
            "notificationTemplateContract": self.notification_template_contract,
            "notificationTemplateId": self.notification_template_id,
            "forwardingProfileId": self.forwarding_profile_id,
            "ziaPostureConfigId": self.zia_posture_config_id,
            "policyToken": self.policy_token,
            "tunnelZappTraffic": self.tunnel_zapp_traffic,
            "groupAll": self.group_all,
            "users": self.users,
            "policyExtension": self.policy_extension,
            "disasterRecovery": self.disaster_recovery,
            "ziaPostureConfig": self.zia_posture_config,
            "groupIds": self.group_ids,
            "deviceGroupIds": self.device_group_ids,
            "userIds": self.user_ids,
            "bypassAppIds": self.bypass_app_ids,
            "appServiceIds": self.app_service_ids,
            "bypassCustomAppIds": self.bypass_custom_app_ids,
            "bypassApps": self.bypass_apps,
            "bypassCustomApps": self.bypass_custom_apps,
            "appServices": self.app_services,
            "passcode": self.passcode,
            "logout_password": self.logout_password,
            "disable_password": self.disable_password,
            "uninstall_password": self.uninstall_password,
            "showVPNTunNotification": self.show_vpn_tun_notification,
            "useTunnelSDK4_3": self.use_tunnel_sdk4_3,
            "ipv6Mode": self.ipv6_mode,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationPolicyGroup(ZscalerObject):
    """
    A class for ApplicationPolicyGroup objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ApplicationPolicyGroup model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.auth_type = config["authType"] if "authType" in config else None
            self.active = config["active"] if "active" in config else None
            self.last_modification = config["lastModification"] if "lastModification" in config else None
        else:
            self.id = None
            self.name = None
            self.auth_type = None
            self.active = None
            self.last_modification = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "authType": self.auth_type,
            "active": self.active,
            "lastModification": self.last_modification,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationPolicyUser(ZscalerObject):
    """
    A class for ApplicationPolicyUser objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ApplicationPolicyUser model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.login_name = config["loginName"] if "loginName" in config else None
            self.last_modification = config["lastModification"] if "lastModification" in config else None
            self.active = config["active"] if "active" in config else None
            self.company_id = config["companyId"] if "companyId" in config else None
        else:
            self.id = None
            self.login_name = None
            self.last_modification = None
            self.active = None
            self.company_id = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "loginName": self.login_name,
            "lastModification": self.last_modification,
            "active": self.active,
            "companyId": self.company_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PolicyExtension(ZscalerObject):
    """
    A class for PolicyExtension objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the PolicyExtension model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.source_port_based_bypasses = (
                config["sourcePortBasedBypasses"] if "sourcePortBasedBypasses" in config else None
            )
            self.packet_tunnel_exclude_list = (
                config["packetTunnelExcludeList"] if "packetTunnelExcludeList" in config else None
            )
            self.packet_tunnel_include_list = (
                config["packetTunnelIncludeList"] if "packetTunnelIncludeList" in config else None
            )
            self.custom_dns = config["customDNS"] if "customDNS" in config else None
            self.exit_password = config["exitPassword"] if "exitPassword" in config else None
            self.use_v8_js_engine = config["useV8JsEngine"] if "useV8JsEngine" in config else None
            self.zdx_disable_password = config["zdxDisablePassword"] if "zdxDisablePassword" in config else None
            self.zd_disable_password = config["zdDisablePassword"] if "zdDisablePassword" in config else None
            self.zpa_disable_password = config["zpaDisablePassword"] if "zpaDisablePassword" in config else None
            self.zdp_disable_password = config["zdpDisablePassword"] if "zdpDisablePassword" in config else None
            self.follow_routing_table = config["followRoutingTable"] if "followRoutingTable" in config else None
            self.use_wsa_poll_for_zpa = config["useWsaPollForZpa"] if "useWsaPollForZpa" in config else None
            self.use_default_adapter_for_dns = (
                config["useDefaultAdapterForDNS"] if "useDefaultAdapterForDNS" in config else None
            )
            self.use_zscaler_notification_framework = (
                config["useZscalerNotificationFramework"] if "useZscalerNotificationFramework" in config else None
            )
            self.switch_focus_to_notification = (
                config["switchFocusToNotification"] if "switchFocusToNotification" in config else None
            )
            self.fallback_to_gateway_domain = (
                config["fallbackToGatewayDomain"] if "fallbackToGatewayDomain" in config else None
            )
            self.enable_zcc_revert = config["enableZCCRevert"] if "enableZCCRevert" in config else None
            self.zcc_revert_password = config["zccRevertPassword"] if "zccRevertPassword" in config else None
            self.zpa_auth_exp_on_sleep = config["zpaAuthExpOnSleep"] if "zpaAuthExpOnSleep" in config else None
            self.zpa_auth_exp_on_sys_restart = config["zpaAuthExpOnSysRestart"] if "zpaAuthExpOnSysRestart" in config else None
            self.zpa_auth_exp_on_net_ip_change = (
                config["zpaAuthExpOnNetIpChange"] if "zpaAuthExpOnNetIpChange" in config else None
            )
            self.instant_force_zpa_reauth_state_update = (
                config["instantForceZPAReauthStateUpdate"] if "instantForceZPAReauthStateUpdate" in config else None
            )
            self.zpa_auth_exp_on_win_logon_session = (
                config["zpaAuthExpOnWinLogonSession"] if "zpaAuthExpOnWinLogonSession" in config else None
            )
            self.zpa_auth_exp_on_win_session_lock = (
                config["zpaAuthExpOnWinSessionLock"] if "zpaAuthExpOnWinSessionLock" in config else None
            )
            self.zpa_auth_exp_session_lock_state_min_time_in_second = (
                config["zpaAuthExpSessionLockStateMinTimeInSecond"]
                if "zpaAuthExpSessionLockStateMinTimeInSecond" in config
                else None
            )
            self.packet_tunnel_exclude_list_for_ipv6 = (
                config["packetTunnelExcludeListForIPv6"] if "packetTunnelExcludeListForIPv6" in config else None
            )
            self.packet_tunnel_include_list_for_ipv6 = (
                config["packetTunnelIncludeListForIPv6"] if "packetTunnelIncludeListForIPv6" in config else None
            )
            self.enable_set_proxy_on_vpn_adapters = (
                config["enableSetProxyOnVPNAdapters"] if "enableSetProxyOnVPNAdapters" in config else None
            )
            self.disable_dns_route_exclusion = (
                config["disableDNSRouteExclusion"] if "disableDNSRouteExclusion" in config else None
            )
            self.advance_zpa_reauth = config["advanceZpaReauth"] if "advanceZpaReauth" in config else None
            self.use_proxy_port_for_t1 = config["useProxyPortForT1"] if "useProxyPortForT1" in config else None
            self.use_proxy_port_for_t2 = config["useProxyPortForT2"] if "useProxyPortForT2" in config else None
            self.allow_pac_exclusions_only = config["allowPacExclusionsOnly"] if "allowPacExclusionsOnly" in config else None
            self.intercept_zia_traffic_all_adapters = (
                config["interceptZIATrafficAllAdapters"] if "interceptZIATrafficAllAdapters" in config else None
            )
            self.enable_anti_tampering = config["enableAntiTampering"] if "enableAntiTampering" in config else None
            self.override_at_cmd_by_policy = config["overrideATCmdByPolicy"] if "overrideATCmdByPolicy" in config else None
            self.reactivate_anti_tampering_time = (
                config["reactivateAntiTamperingTime"] if "reactivateAntiTamperingTime" in config else None
            )
            self.enforce_split_dns = config["enforceSplitDNS"] if "enforceSplitDNS" in config else None
            self.drop_quic_traffic = config["dropQuicTraffic"] if "dropQuicTraffic" in config else None
            self.enable_zdp_service = config["enableZdpService"] if "enableZdpService" in config else None
            self.update_dns_search_order = config["updateDnsSearchOrder"] if "updateDnsSearchOrder" in config else None
            self.truncate_large_udpdns_response = (
                config["truncateLargeUDPDNSResponse"] if "truncateLargeUDPDNSResponse" in config else None
            )
            self.prioritize_dns_exclusions = config["prioritizeDnsExclusions"] if "prioritizeDnsExclusions" in config else None
            self.purge_kerberos_preferred_dc_cache = (
                config["purgeKerberosPreferredDCCache"] if "purgeKerberosPreferredDCCache" in config else None
            )
            self.delete_dhcp_option121_routes = (
                config["deleteDHCPOption121Routes"] if "deleteDHCPOption121Routes" in config else None
            )
            self.enable_location_policy_override = (
                config["enableLocationPolicyOverride"] if "enableLocationPolicyOverride" in config else None
            )
            self.enable_custom_theme = config["enableCustomTheme"] if "enableCustomTheme" in config else None

            if "locationRulesetPolicies" in config:
                if isinstance(config["locationRulesetPolicies"], LocationRulesetPolicies):
                    self.location_ruleset_policies = config["locationRulesetPolicies"]
                elif config["locationRulesetPolicies"] is not None:
                    self.location_ruleset_policies = LocationRulesetPolicies(config["locationRulesetPolicies"])
                else:
                    self.location_ruleset_policies = None
            else:
                self.location_ruleset_policies = None

            if "generateCliPasswordContract" in config:
                if isinstance(config["generateCliPasswordContract"], GenerateCliPasswordContract):
                    self.generate_cli_password_contract = config["generateCliPasswordContract"]
                elif config["generateCliPasswordContract"] is not None:
                    self.generate_cli_password_contract = GenerateCliPasswordContract(config["generateCliPasswordContract"])
                else:
                    self.generate_cli_password_contract = None
            else:
                self.generate_cli_password_contract = None

            self.zdx_lite_config_obj = config["zdxLiteConfigObj"] if "zdxLiteConfigObj" in config else None
            self.ddil_config = config["ddilConfig"] if "ddilConfig" in config else None
            self.zcc_fail_close_settings_ip_bypasses = (
                config["zccFailCloseSettingsIpBypasses"] if "zccFailCloseSettingsIpBypasses" in config else None
            )
            self.zcc_fail_close_settings_exit_uninstall_password = (
                config["zccFailCloseSettingsExitUninstallPassword"]
                if "zccFailCloseSettingsExitUninstallPassword" in config
                else None
            )
            self.zcc_fail_close_settings_lockdown_on_tunnel_process_exit = (
                config["zccFailCloseSettingsLockdownOnTunnelProcessExit"]
                if "zccFailCloseSettingsLockdownOnTunnelProcessExit" in config
                else None
            )
            self.zcc_fail_close_settings_lockdown_on_firewall_error = (
                config["zccFailCloseSettingsLockdownOnFirewallError"]
                if "zccFailCloseSettingsLockdownOnFirewallError" in config
                else None
            )
            self.zcc_fail_close_settings_lockdown_on_driver_error = (
                config["zccFailCloseSettingsLockdownOnDriverError"]
                if "zccFailCloseSettingsLockdownOnDriverError" in config
                else None
            )
            self.zcc_fail_close_settings_thumb_print = (
                config["zccFailCloseSettingsThumbPrint"] if "zccFailCloseSettingsThumbPrint" in config else None
            )
            self.zcc_app_fail_open_policy = config["zccAppFailOpenPolicy"] if "zccAppFailOpenPolicy" in config else None
            self.zcc_tunnel_fail_policy = config["zccTunnelFailPolicy"] if "zccTunnelFailPolicy" in config else None
            self.follow_global_for_partner_login = (
                config["followGlobalForPartnerLogin"] if "followGlobalForPartnerLogin" in config else None
            )
            self.user_allowed_to_add_partner = (
                config["userAllowedToAddPartner"] if "userAllowedToAddPartner" in config else None
            )
            self.allow_client_cert_caching_for_web_view2 = (
                config["allowClientCertCachingForWebView2"] if "allowClientCertCachingForWebView2" in config else None
            )
            self.show_confirmation_dialog_for_cached_cert = (
                config["showConfirmationDialogForCachedCert"] if "showConfirmationDialogForCachedCert" in config else None
            )
            self.enable_flow_based_tunnel = config["enableFlowBasedTunnel"] if "enableFlowBasedTunnel" in config else None
            self.enable_network_traffic_process_mapping = (
                config["enableNetworkTrafficProcessMapping"] if "enableNetworkTrafficProcessMapping" in config else None
            )
            self.enable_local_packet_capture = (
                config["enableLocalPacketCapture"] if "enableLocalPacketCapture" in config else None
            )
            self.one_id_mt_device_auth_enabled = (
                config["oneIdMTDeviceAuthEnabled"] if "oneIdMTDeviceAuthEnabled" in config else None
            )
            self.enable_custom_proxy_detection = (
                config["enableCustomProxyDetection"] if "enableCustomProxyDetection" in config else None
            )
            self.prevent_auto_reauth_during_device_lock = (
                config["preventAutoReauthDuringDeviceLock"] if "preventAutoReauthDuringDeviceLock" in config else None
            )
            self.use_end_point_location_for_dc_selection = (
                config["useEndPointLocationForDCSelection"] if "useEndPointLocationForDCSelection" in config else None
            )
            self.enable_crash_reporting = config["enableCrashReporting"] if "enableCrashReporting" in config else None
            self.recache_system_proxy = config["recacheSystemProxy"] if "recacheSystemProxy" in config else None
            self.enable_automatic_packet_capture = (
                config["enableAutomaticPacketCapture"] if "enableAutomaticPacketCapture" in config else None
            )
            self.enable_apc_for_critical_sections = (
                config["enableAPCforCriticalSections"] if "enableAPCforCriticalSections" in config else None
            )
            self.enable_apc_for_other_sections = (
                config["enableAPCforOtherSections"] if "enableAPCforOtherSections" in config else None
            )
            self.enable_pc_additional_space = (
                config["enablePCAdditionalSpace"] if "enablePCAdditionalSpace" in config else None
            )
            self.pc_additional_space = config["pcAdditionalSpace"] if "pcAdditionalSpace" in config else None
            self.client_connector_ui_language = (
                config["clientConnectorUiLanguage"] if "clientConnectorUiLanguage" in config else None
            )
            self.block_private_relay = config["blockPrivateRelay"] if "blockPrivateRelay" in config else None
            self.bypass_dns_traffic_using_udp_proxy = (
                config["bypassDNSTrafficUsingUDPProxy"] if "bypassDNSTrafficUsingUDPProxy" in config else None
            )
            self.reconnect_tun_on_wakeup = config["reconnectTunOnWakeup"] if "reconnectTunOnWakeup" in config else None
            self.browser_auth_type = config["browserAuthType"] if "browserAuthType" in config else None
            self.use_default_browser = config["useDefaultBrowser"] if "useDefaultBrowser" in config else None
        else:
            self.source_port_based_bypasses = None
            self.packet_tunnel_exclude_list = None
            self.packet_tunnel_include_list = None
            self.custom_dns = None
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
            self.instant_force_zpa_reauth_state_update = None
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
            self.allow_pac_exclusions_only = None
            self.intercept_zia_traffic_all_adapters = None
            self.enable_anti_tampering = None
            self.override_at_cmd_by_policy = None
            self.reactivate_anti_tampering_time = None
            self.enforce_split_dns = None
            self.drop_quic_traffic = None
            self.enable_zdp_service = None
            self.update_dns_search_order = None
            self.truncate_large_udpdns_response = None
            self.prioritize_dns_exclusions = None
            self.purge_kerberos_preferred_dc_cache = None
            self.delete_dhcp_option121_routes = None
            self.enable_location_policy_override = None
            self.enable_custom_theme = None
            self.location_ruleset_policies = None
            self.generate_cli_password_contract = None
            self.zdx_lite_config_obj = None
            self.ddil_config = None
            self.zcc_fail_close_settings_ip_bypasses = None
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
            self.enable_network_traffic_process_mapping = None
            self.enable_local_packet_capture = None
            self.one_id_mt_device_auth_enabled = None
            self.enable_custom_proxy_detection = None
            self.prevent_auto_reauth_during_device_lock = None
            self.use_end_point_location_for_dc_selection = None
            self.enable_crash_reporting = None
            self.recache_system_proxy = None
            self.enable_automatic_packet_capture = None
            self.enable_apc_for_critical_sections = None
            self.enable_apc_for_other_sections = None
            self.enable_pc_additional_space = None
            self.pc_additional_space = None
            self.client_connector_ui_language = None
            self.block_private_relay = None
            self.bypass_dns_traffic_using_udp_proxy = None
            self.reconnect_tun_on_wakeup = None
            self.browser_auth_type = None
            self.use_default_browser = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "sourcePortBasedBypasses": self.source_port_based_bypasses,
            "packetTunnelExcludeList": self.packet_tunnel_exclude_list,
            "packetTunnelIncludeList": self.packet_tunnel_include_list,
            "customDNS": self.custom_dns,
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
            "instantForceZPAReauthStateUpdate": self.instant_force_zpa_reauth_state_update,
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
            "allowPacExclusionsOnly": self.allow_pac_exclusions_only,
            "interceptZIATrafficAllAdapters": self.intercept_zia_traffic_all_adapters,
            "enableAntiTampering": self.enable_anti_tampering,
            "overrideATCmdByPolicy": self.override_at_cmd_by_policy,
            "reactivateAntiTamperingTime": self.reactivate_anti_tampering_time,
            "enforceSplitDNS": self.enforce_split_dns,
            "dropQuicTraffic": self.drop_quic_traffic,
            "enableZdpService": self.enable_zdp_service,
            "updateDnsSearchOrder": self.update_dns_search_order,
            "truncateLargeUDPDNSResponse": self.truncate_large_udpdns_response,
            "prioritizeDnsExclusions": self.prioritize_dns_exclusions,
            "purgeKerberosPreferredDCCache": self.purge_kerberos_preferred_dc_cache,
            "deleteDHCPOption121Routes": self.delete_dhcp_option121_routes,
            "enableLocationPolicyOverride": self.enable_location_policy_override,
            "enableCustomTheme": self.enable_custom_theme,
            "locationRulesetPolicies": self.location_ruleset_policies,
            "generateCliPasswordContract": self.generate_cli_password_contract,
            "zdxLiteConfigObj": self.zdx_lite_config_obj,
            "ddilConfig": self.ddil_config,
            "zccFailCloseSettingsIpBypasses": self.zcc_fail_close_settings_ip_bypasses,
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
            "enableNetworkTrafficProcessMapping": self.enable_network_traffic_process_mapping,
            "enableLocalPacketCapture": self.enable_local_packet_capture,
            "oneIdMTDeviceAuthEnabled": self.one_id_mt_device_auth_enabled,
            "enableCustomProxyDetection": self.enable_custom_proxy_detection,
            "preventAutoReauthDuringDeviceLock": self.prevent_auto_reauth_during_device_lock,
            "useEndPointLocationForDCSelection": self.use_end_point_location_for_dc_selection,
            "enableCrashReporting": self.enable_crash_reporting,
            "recacheSystemProxy": self.recache_system_proxy,
            "enableAutomaticPacketCapture": self.enable_automatic_packet_capture,
            "enableAPCforCriticalSections": self.enable_apc_for_critical_sections,
            "enableAPCforOtherSections": self.enable_apc_for_other_sections,
            "enablePCAdditionalSpace": self.enable_pc_additional_space,
            "pcAdditionalSpace": self.pc_additional_space,
            "clientConnectorUiLanguage": self.client_connector_ui_language,
            "blockPrivateRelay": self.block_private_relay,
            "bypassDNSTrafficUsingUDPProxy": self.bypass_dns_traffic_using_udp_proxy,
            "reconnectTunOnWakeup": self.reconnect_tun_on_wakeup,
            "browserAuthType": self.browser_auth_type,
            "useDefaultBrowser": self.use_default_browser,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LocationRulesetPolicies(ZscalerObject):
    """
    A class for LocationRulesetPolicies objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LocationRulesetPolicies model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            if "offTrusted" in config:
                if isinstance(config["offTrusted"], LocationPolicy):
                    self.off_trusted = config["offTrusted"]
                elif config["offTrusted"] is not None:
                    self.off_trusted = LocationPolicy(config["offTrusted"])
                else:
                    self.off_trusted = None
            else:
                self.off_trusted = None

            if "trusted" in config:
                if isinstance(config["trusted"], LocationPolicy):
                    self.trusted = config["trusted"]
                elif config["trusted"] is not None:
                    self.trusted = LocationPolicy(config["trusted"])
                else:
                    self.trusted = None
            else:
                self.trusted = None

            if "vpnTrusted" in config:
                if isinstance(config["vpnTrusted"], LocationPolicy):
                    self.vpn_trusted = config["vpnTrusted"]
                elif config["vpnTrusted"] is not None:
                    self.vpn_trusted = LocationPolicy(config["vpnTrusted"])
                else:
                    self.vpn_trusted = None
            else:
                self.vpn_trusted = None

            if "splitVpnTrusted" in config:
                if isinstance(config["splitVpnTrusted"], LocationPolicy):
                    self.split_vpn_trusted = config["splitVpnTrusted"]
                elif config["splitVpnTrusted"] is not None:
                    self.split_vpn_trusted = LocationPolicy(config["splitVpnTrusted"])
                else:
                    self.split_vpn_trusted = None
            else:
                self.split_vpn_trusted = None
        else:
            self.off_trusted = None
            self.trusted = None
            self.vpn_trusted = None
            self.split_vpn_trusted = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "offTrusted": self.off_trusted,
            "trusted": self.trusted,
            "vpnTrusted": self.vpn_trusted,
            "splitVpnTrusted": self.split_vpn_trusted,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LocationPolicy(ZscalerObject):
    """
    A class for LocationPolicy objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LocationPolicy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
        else:
            self.id = None
            self.name = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GenerateCliPasswordContract(ZscalerObject):
    """
    A class for GenerateCliPasswordContract objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the GenerateCliPasswordContract model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.policy_id = config["policyId"] if "policyId" in config else None
            self.enable_cli = config["enableCli"] if "enableCli" in config else None
            self.allow_zpa_disable_without_password = (
                config["allowZpaDisableWithoutPassword"] if "allowZpaDisableWithoutPassword" in config else None
            )
            self.allow_zia_disable_without_password = (
                config["allowZiaDisableWithoutPassword"] if "allowZiaDisableWithoutPassword" in config else None
            )
            self.allow_zdx_disable_without_password = (
                config["allowZdxDisableWithoutPassword"] if "allowZdxDisableWithoutPassword" in config else None
            )
        else:
            self.policy_id = None
            self.enable_cli = None
            self.allow_zpa_disable_without_password = None
            self.allow_zia_disable_without_password = None
            self.allow_zdx_disable_without_password = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "policyId": self.policy_id,
            "enableCli": self.enable_cli,
            "allowZpaDisableWithoutPassword": self.allow_zpa_disable_without_password,
            "allowZiaDisableWithoutPassword": self.allow_zia_disable_without_password,
            "allowZdxDisableWithoutPassword": self.allow_zdx_disable_without_password,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DisasterRecovery(ZscalerObject):
    """
    A class for DisasterRecovery objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the DisasterRecovery model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.policy_id = config["policyId"] if "policyId" in config else None
            self.enable_zia_dr = config["enableZiaDR"] if "enableZiaDR" in config else None
            self.enable_zpa_dr = config["enableZpaDR"] if "enableZpaDR" in config else None
            self.zia_dr_method = config["ziaDRMethod"] if "ziaDRMethod" in config else None
            self.zia_custom_db_url = config["ziaCustomDbUrl"] if "ziaCustomDbUrl" in config else None
            self.use_zia_global_db = config["useZiaGlobalDb"] if "useZiaGlobalDb" in config else None
            self.zia_global_db_url = config["ziaGlobalDbUrl"] if "ziaGlobalDbUrl" in config else None
            self.zia_global_db_urlv2 = config["ziaGlobalDbUrlv2"] if "ziaGlobalDbUrlv2" in config else None
            self.zia_domain_name = config["ziaDomainName"] if "ziaDomainName" in config else None
            self.zia_rsa_pub_key_name = config["ziaRSAPubKeyName"] if "ziaRSAPubKeyName" in config else None
            self.zia_rsa_pub_key = config["ziaRSAPubKey"] if "ziaRSAPubKey" in config else None
            self.zpa_domain_name = config["zpaDomainName"] if "zpaDomainName" in config else None
            self.zpa_rsa_pub_key_name = config["zpaRSAPubKeyName"] if "zpaRSAPubKeyName" in config else None
            self.zpa_rsa_pub_key = config["zpaRSAPubKey"] if "zpaRSAPubKey" in config else None
            self.allow_zia_test = config["allowZiaTest"] if "allowZiaTest" in config else None
            self.allow_zpa_test = config["allowZpaTest"] if "allowZpaTest" in config else None
        else:
            self.policy_id = None
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

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "policyId": self.policy_id,
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
            "allowZpaTest": self.allow_zpa_test,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppService(ZscalerObject):
    """
    A class for AppService objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the AppService model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.app_data_blob = ZscalerCollection.form_list(
                config["appDataBlob"] if "appDataBlob" in config else [], AppDataBlob
            )
        else:
            self.active = None
            self.app_data_blob = ZscalerCollection.form_list([], AppDataBlob)

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "appDataBlob": self.app_data_blob,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppDataBlob(ZscalerObject):
    """
    A class for AppDataBlob objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the AppDataBlob model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.fqdn = config["fqdn"] if "fqdn" in config else None
            self.ipaddr = config["ipaddr"] if "ipaddr" in config else None
            self.port = config["port"] if "port" in config else None
        else:
            self.fqdn = None
            self.ipaddr = None
            self.port = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "fqdn": self.fqdn,
            "ipaddr": self.ipaddr,
            "port": self.port,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
