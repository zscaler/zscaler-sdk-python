"""
Module contains different helper functions.
Module is independent from any zscaler modules.
"""

import re


def to_snake_case(string):
    """
    Converts camelCase or PascalCase to snake_case.
    Applies known field-specific corrections first.
    """
    FIELD_EXCEPTIONS = {
        "predefinedADPControls": "predefined_adp_controls",
        "surrogateIP": "surrogate_ip",
        "surrogateIPEnforcedForKnownBrowsers": "surrogate_ip_enforced_for_known_browsers",
        "capturePCAP": "capture_pcap",
        "internalIpRange": "internal_ip_range",
        "startIPAddress": "start_ip_address",
        "endIPAddress": "end_ip_address",
        "minTLSVersion": "min_tls_version",
        "minClientTLSVersion": "min_client_tls_version",
        "minServerTLSVersion": "min_server_tls_version",
        "pacWithStaticIPs": "pac_with_static_ips",
        "primaryGW": "primary_gw",
        "secondaryGW": "secondary_gw",
        "greTunnelIP": "gre_tunnel_ip",
        "tunID": "tun_id",
        "isIncompleteDRConfig": "is_incomplete_dr_config",
        "nameL10nTag": "name_l10n_tag",
        "isNameL10nTag": "is_name_l10n_tag",
        "routableIP": "routable_ip",
        "validSSLCertificate": "valid_ssl_certificate",
        "ecVMs": "ec_vms",
        "ipV6Enabled": "ipv6_enabled",
        "emailIds": "email_ids",
        "showEUN": "show_eun",
        "showEUNATP": "show_eunatp",
        "enableCIPACompliance": "enable_cipa_compliance",
        "enablePOEPrompt": "enable_poe_prompt",
        "cookieStealingPCAPEnabled": "cookie_stealing_pcap_enabled",
        "alertForUnknownOrSuspiciousC2Traffic": "alert_for_unknown_or_suspicious_c2_traffic",
        "enableIPv6DnsResolutionOnTransparentProxy": "enable_ipv6_dns_resolution_on_transparent_proxy",
        "enableEvaluatePolicyOnGlobalSSLBypass": "enable_evaluate_policy_on_global_ssl_bypass",
        "dnsResolutionOnTransparentProxyIPv6ExemptApps": "dns_resolution_on_transparent_proxy_ipv6_exempt_apps",
        "dnsResolutionOnTransparentProxyIPv6UrlCategories": "dns_resolution_on_transparent_proxy_ipv6_url_categories",
        "dnsResolutionOnTransparentProxyIPv6Apps": "dns_resolution_on_transparent_proxy_ipv6_apps",
        "enableIPv6DnsOptimizationOnAllTransparentProxy": "enable_ipv6_dns_optimization_on_all_transparent_proxy",
        "dnsResolutionOnTransparentProxyIPv6ExemptUrlCategories": "dns_resolution_on_transparent_proxy_ipv6_exempt_url_categories",
        "endPointDLPLogType": "end_point_dlp_log_type",
        "emailDLPLogType": "email_dlp_log_type",
        "extranetDNSList": "extranet_dns_list",
        "primaryDNSServer": "primary_dns_server",
        "secondaryDNSServer": "secondary_dns_server",
        
        # ZCC Edge Case Attributes
        "enableUDPTransportSelection": "enable_udp_transport_selection",
        "interceptZIATrafficAllAdapters": "intercept_zia_traffic_all_adapters",
        "enablePortBasedZPAFilter": "enable_port_based_zpa_filter",
        "addAppBypassToVPNGateway": "add_app_bypass_to_vpn_gateway",
        "showVPNTunNotification": "show_vpn_tun_notification",
        "enableSetProxyOnVPNAdapters": "enable_set_proxy_on_vpn_adapters",
        "disableDNSRouteExclusion": "disable_dns_route_exclusion",
        "enableReactUI": "enable_react_ui",
        "ziaGlobalDbUrlForDR": "zia_global_db_url_for_dr",
        "useDefaultAdapterForDNS": "use_default_adapter_for_dns",
        "enablePublicAPI": "enable_public_api",
        "launchReactUIbyDefault": "launch_react_u_iby_default",
        "addZDXServiceEntitlement": "add_zdx_service_entitlement",
        "computeDeviceGroupsForZIA": "compute_device_groups_for_zia",
        "computeDeviceGroupsForZPA": "compute_device_groups_for_zpa",
        "computeDeviceGroupsForZAD": "compute_device_groups_for_zad",
        "computeDeviceGroupsForZAD": "compute_device_groups_for_zad",
        "deleteDHCPOption121RoutesVisibility": "delete_dhcp_option121_routes_visibility",
        "deleteDHCPOption121Routes": "delete_dhcp_option121_routes",
        "enableOneIDAdminMigrationChanges": "enable_one_id_admin_migration_changes",
        "purgeKerberosPreferredDCCacheVisibility": "purge_kerberos_preferred_dc_cache_visibility",
        "slowRolloutZCC": "slow_rollout_zcc",
        "supportMultiplePWLPostures": "support_multiple_pwl_postures",
        "truncateLargeUDPDNSResponseVisibility": "truncate_large_udpdns_response_visibility",
        "enforceSplitDNSVisibility": "enforce_split_dns_visibility",
        "zccSyntheticIPRangeVisibility": "zcc_synthetic_ip_range_visibility",
        "enableSetProxyOnVPNAdaptersVisibility": "enable_set_proxy_on_vpn_adapters_visibility",
        "customMTUForZpaVisibility": "custom_mtu_for_zpa_visibility",
        "flowLoggerZCCBlockedTrafficVisibility": "flow_logger_zcc_blocked_traffic_visibility",
        "postureCrowdStrikeZTAScoreVisibilityForLinux": "posture_crowd_strike_zta_score_visibility_for_linux",
        "flowLoggerVPNTunnelTypeVisibility": "flow_logger_vpn_tunnel_type_visibility",
        "flowLoggerVPNTypeVisibility": "flow_logger_vpn_type_visibility",
        "flowLoggerZPATypeVisibility": "flow_logger_zpa_type_visibility",
        "useDefaultAdapterForDNSVisibility": "use_default_adapter_for_dns_visibility",
        "useCustomDNS": "use_custom_dns",
        "notificationForZPAReauthVisibility": "notification_for_zpa_reauth_visibility",
        "crowdStrikeZTAScoreVisibility": "crowd_strike_zta_score_visibility",
        "hideDTLSSupportSettings": "hide_dtls_support_settings",
        "dynamicZPAServiceEdgeAssignmenttVisibility": "dynamic_zpa_service_edge_assignmentt_visibility",
        "domainInclusionExclusionForDNSRequestVisibility": "domain_inclusion_exclusion_for_dns_request_visibility",
        "overrideATCmdByPolicyVisibility": "override_at_cmd_by_policy_visibility",
        "windowsAPCaptivePortalDetectionVisibility": "windows_ap_captive_portal_detection_visibility",
        "windowsAPEnableFailOpenVisibility": "windows_ap_enable_fail_open_visibility",
        "enableOneIDPhase2Changes": "enable_one_id_phase2_changes",
        "linuxRPMBuildVisibility": "linux_rpm_build_visibility",
        "crowdStrikeZTAOsScoreVisibility": "crowd_strike_zta_os_score_visibility",
        "crowdStrikeZTASensorConfigScoreVisibility": "crowd_strike_zta_sensor_config_score_visibility",
        "enableZCCFailCloseSettingsForSEMode": "enable_zcc_fail_close_settings_for_se_mode",
        "defaultProtocolForZPA": "default_protocol_for_zpa",
        "tunnelTwoForiOSDevices": "tunnel_two_fori_os_devices",
        "prioritizeIPv4OverIpv6": "prioritize_ipv4_over_ipv6",
        "disableParallelIpv4AndIPv6": "disable_parallel_ipv4_and_ipv6",
        "computeDeviceGroupsForZDX ": "compute_device_groups_for_zdx",
        "logoutZCCForZDXService": "logout_zcc_for_zdx_service",
        "enableZpaDR": "enable_zpa_dr",
        "ziaRSAPubKeyName": "zia_rsa_pub_key_name",
        "ziaRSAPubKey": "zia_rsa_pub_key",
        "zpaRSAPubKeyName": "zpa_rsa_pub_key_name",
        "zpaRSAPubKey": "zpa_rsa_pub_key",
        "truncate_large_udpdns_response": "truncateLargeUDPDNSResponse",
        "enableZCCRevert": "enable_zcc_revert",
        "enableZiaDR": "enable_zia_dr",
        "purgeKerberosPreferredDCCache": "purge_kerberos_preferred_dc_cache",
        
        # ZPA Edge Cases
        "serverGroupDTOs": "server_group_dtos",
        "extranetDTO": "extranet_dto",
        "locationGroupDTO": "location_group_dto",
        "locationDTO": "location_dto",
        "predefinedADPControls": "predefined_adp_controls"
    }

    if string in FIELD_EXCEPTIONS:
        return FIELD_EXCEPTIONS[string]

    # Generic fallback logic
    string = re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()
    return string.replace("__", "_").strip("_")


def to_lower_camel_case(string):
    """
    Converts snake_case to camelCase with support for known edge-case field mappings.

    Examples:
        "internal_ip_range" -> "internalIpRange"
        "surrogate_ip"      -> "surrogateIP"
        "capture_pcap"      -> "capturePCAP"
    """

    FIELD_EXCEPTIONS = {
        "predefined_adp_controls": "predefinedADPControls",
        "surrogate_ip": "surrogateIP",
        "internal_ip_range": "internalIpRange",
        "start_ip_address": "startIPAddress",
        "end_ip_address": "endIPAddress",
        "capture_pcap": "capturePCAP",
        "min_tls_version": "minTLSVersion",
        "min_client_tls_version": "minClientTLSVersion",
        "min_server_tls_version": "minServerTLSVersion",
        "pac_with_static_ips": "pacWithStaticIPs",
        "primary_gw": "primaryGW",
        "secondary_gw": "secondaryGW",
        "greTunnel_ip": "greTunnelIP",
        "tun_id": "tunID",
        "is_incomplete_dr_config": "isIncompleteDRConfig",
        "name_l10n_tag": "nameL10nTag",
        "is_name_l10n_tag": "isNameL10nTag",
        "routable_ip": "routableIP",
        "valid_ssl_certificate": "validSSLCertificate",
        "ec_vms": "ecVMs",
        "ipv6_enabled": "ipV6Enabled",
        "email_ids": "emailIds",
        "show_eun": "showEUN",
        "show_eunatp": "showEUNATP",
        "enable_cipa_compliance": "enableCIPACompliance",
        "enable_poe_prompt": "enablePOEPrompt",
        "cookie_stealing_pcap_enabled": "cookieStealingPCAPEnabled",
        "alert_for_unknown_or_suspicious_c2_traffic": "alertForUnknownOrSuspiciousC2Traffic",
        "enable_ipv6_dns_resolution_on_transparent_proxy": "enableIPv6DnsResolutionOnTransparentProxy",
        "enable_evaluate_policy_on_global_ssl_bypass": "enableEvaluatePolicyOnGlobalSSLBypass",
        "dns_resolution_on_transparent_proxy_ipv6_exempt_apps": "dnsResolutionOnTransparentProxyIPv6ExemptApps",
        "dns_resolution_on_transparent_proxy_ipv6_url_categories": "dnsResolutionOnTransparentProxyIPv6UrlCategories",
        "dns_resolution_on_transparent_proxy_ipv6_apps": "dnsResolutionOnTransparentProxyIPv6Apps",
        "enable_ipv6_dns_optimization_on_all_transparent_proxy": "enableIPv6DnsOptimizationOnAllTransparentProxy",
        "dns_resolution_on_transparent_proxy_ipv6_exempt_url_categories": "dnsResolutionOnTransparentProxyIPv6ExemptUrlCategories",
        "end_point_dlp_log_type": "endPointDLPLogType",
        "email_dlp_log_type": "emailDLPLogType",
        "extranet_dns_list": "extranetDNSList",
        "primary_dns_server": "primaryDNSServer",
        "secondary_dns_server": "secondaryDNSServer",
        
        # ZCC Edge Case Attributes
        "enable_udp_transport_selection": "enableUDPTransportSelection",
        "intercept_zia_traffic_all_adapters": "interceptZIATrafficAllAdapters",
        "enable_port_based_zpa_filter": "enablePortBasedZPAFilter",
        "add_app_bypass_to_vpn_gateway": "addAppBypassToVPNGateway",
        "show_vpn_tun_notification": "showVPNTunNotification",
        "enable_set_proxy_on_vpn_adapters": "enableSetProxyOnVPNAdapters",
        "disable_dns_route_exclusion": "disableDNSRouteExclusion",
        "enable_react_ui": "enableReactUI",
        "zia_global_db_url_for_dr": "ziaGlobalDbUrlForDR",
        "use_default_adapter_for_dns": "useDefaultAdapterForDNS",
        "enable_public_api": "enablePublicAPI",
        "launch_react_u_iby_default": "launchReactUIbyDefault",
        "add_zdx_service_entitlement": "addZDXServiceEntitlement",
        "compute_device_groups_for_zia": "computeDeviceGroupsForZIA",
        "compute_device_groups_for_zpa": "computeDeviceGroupsForZPA",
        "compute_device_groups_for_zad": "computeDeviceGroupsForZAD",
        "delete_dhcp_option121_routes_visibility": "deleteDHCPOption121RoutesVisibility",
        "enable_one_id_admin_migration_changes": "enableOneIDAdminMigrationChanges",
        "purge_kerberos_preferred_dc_cache_visibility": "purgeKerberosPreferredDCCacheVisibility",
        "slow_rollout_zcc": "slowRolloutZCC",
        "support_multiple_pwl_postures": "supportMultiplePWLPostures",
        "truncate_large_udpdns_response_visibility": "truncateLargeUDPDNSResponseVisibility",
        "enforce_split_dns_visibility": "enforceSplitDNSVisibility",
        "zcc_synthetic_ip_range_visibility": "zccSyntheticIPRangeVisibility",
        "enable_set_proxy_on_vpn_adapters_visibility": "enableSetProxyOnVPNAdaptersVisibility",
        "custom_mtu_for_zpa_visibility": "customMTUForZpaVisibility",
        "flow_logger_zcc_blocked_traffic_visibility": "flowLoggerZCCBlockedTrafficVisibility",
        "posture_crowd_strike_zta_score_visibility_for_linux": "postureCrowdStrikeZTAScoreVisibilityForLinux",
        "flow_logger_vpn_tunnel_type_visibility": "flowLoggerVPNTunnelTypeVisibility",
        "flow_logger_vpn_type_visibility": "flowLoggerVPNTypeVisibility",
        "flow_logger_zpa_type_visibility": "flowLoggerZPATypeVisibility",
        "use_default_adapter_for_dns_visibility": "useDefaultAdapterForDNSVisibility",
        "use_custom_dns": "useCustomDNS",
        "notification_for_zpa_reauth_visibility": "notificationForZPAReauthVisibility",
        "crowd_strike_zta_score_visibility": "crowdStrikeZTAScoreVisibility",
        "hide_dtls_support_settings": "hideDTLSSupportSettings",
        "dynamic_zpa_service_edge_assignmentt_visibility": "dynamicZPAServiceEdgeAssignmenttVisibility",
        "domain_inclusion_exclusion_for_dns_request_visibility": "domainInclusionExclusionForDNSRequestVisibility",
        "override_at_cmd_by_policy_visibility": "overrideATCmdByPolicyVisibility",
        "windows_ap_captive_portal_detection_visibility": "windowsAPCaptivePortalDetectionVisibility",
        "windows_ap_enable_fail_open_visibility": "windowsAPEnableFailOpenVisibility",
        "enable_one_id_phase2_changes": "enableOneIDPhase2Changes",
        "linux_rpm_build_visibility": "linuxRPMBuildVisibility",
        "crowd_strike_zta_os_score_visibility": "crowdStrikeZTAOsScoreVisibility",
        "crowd_strike_zta_sensor_config_score_visibility": "crowdStrikeZTASensorConfigScoreVisibility",
        "enable_zcc_fail_close_settings_for_se_mode": "enableZCCFailCloseSettingsForSEMode",
        "default_protocol_for_zpa": "defaultProtocolForZPA",
        "tunnelTwoForiOSDevices": "tunnel_two_fori_os_devices",
        "prioritize_ipv4_over_ipv6": "prioritizeIPv4OverIpv6",
        "disable_parallel_ipv4_and_ipv6": "disableParallelIpv4AndIPv6",
        "compute_device_groups_for_zdx": "computeDeviceGroupsForZDX",
        "logout_zcc_for_zdx_service ": "logoutZCCForZDXService",
        "enable_zpa_dr": "enableZpaDR",
        "zia_rsa_pub_key_name": "ziaRSAPubKeyName",
        "zia_rsa_pub_key": "ziaRSAPubKey",
        "zpa_rsa_pub_key_name": "zpaRSAPubKeyName",
        "zpa_rsa_pub_key": "zpaRSAPubKey",
        "truncateLargeUDPDNSResponse": "truncate_large_udpdns_response",
        "enable_zcc_revert": "enableZCCRevert",
        "delete_dhcp_option121_routes": "deleteDHCPOption121Routes",
        "enableZiaDR": "enable_zia_dr",
        "purgeKerberosPreferredDCCache": "purge_kerberos_preferred_dc_cache",
        
        # ZPA Edge Cases
        "server_group_dtos": "serverGroupDTOs",
        "extranet_dto": "extranetDTO",
        "location_group_dto": "locationGroupDTO",
        "location_dto": "locationDTO",
        "predefined_adp_controls": "predefinedADPControls"
    }

    if string in FIELD_EXCEPTIONS:
        return FIELD_EXCEPTIONS[string]

    if not string or "_" not in string:
        return string

    components = string.split("_")
    converted = []

    for i, comp in enumerate(components):
        lower = comp.lower()
        if i == 0:
            converted.append(lower)
        else:
            converted.append(comp.capitalize())

    return "".join(converted)


def convert_keys_to_snake_case(data):
    """
    Convert all keys in a dictionary or list to snake_case.
    """
    if isinstance(data, dict):
        return {to_snake_case(k): convert_keys_to_snake_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    else:
        return data


def convert_keys_to_camel_case(data):
    """
    Recursively convert all keys in a dictionary or list to camelCase.
    Handles nested lists and dictionaries.
    """
    if isinstance(data, dict):
        return {to_lower_camel_case(k): convert_keys_to_camel_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    else:
        return data
