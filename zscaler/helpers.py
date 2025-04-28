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
