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


class AdvancedSettings(ZscalerObject):
    """
    A class representing a Devices object.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.enable_dns_resolution_on_transparent_proxy = (
                config["enableDnsResolutionOnTransparentProxy"] if "enableDnsResolutionOnTransparentProxy" in config else False
            )
            self.enable_ipv6_dns_resolution_on_transparent_proxy = (
                config["enableIPv6DnsResolutionOnTransparentProxy"]
                if "enableIPv6DnsResolutionOnTransparentProxy" in config
                else False
            )
            self.enable_ipv6_dns_optimization_on_all_transparent_proxy = (
                config["enableIPv6DnsOptimizationOnAllTransparentProxy"]
                if "enableIPv6DnsOptimizationOnAllTransparentProxy" in config
                else False
            )
            self.enable_evaluate_policy_on_global_ssl_bypass = (
                config["enableEvaluatePolicyOnGlobalSSLBypass"] if "enableEvaluatePolicyOnGlobalSSLBypass" in config else False
            )
            self.enable_office365 = config["enableOffice365"] if "enableOffice365" in config else False
            self.log_internal_ip = config["logInternalIp"] if "logInternalIp" in config else False
            self.enforce_surrogate_ip_for_windows_app = (
                config["enforceSurrogateIpForWindowsApp"] if "enforceSurrogateIpForWindowsApp" in config else False
            )
            self.track_http_tunnel_on_http_ports = (
                config["trackHttpTunnelOnHttpPorts"] if "trackHttpTunnelOnHttpPorts" in config else False
            )
            self.block_http_tunnel_on_non_http_ports = (
                config["blockHttpTunnelOnNonHttpPorts"] if "blockHttpTunnelOnNonHttpPorts" in config else False
            )
            self.block_domain_fronting_on_host_header = (
                config["blockDomainFrontingOnHostHeader"] if "blockDomainFrontingOnHostHeader" in config else False
            )
            self.zscaler_client_connector1_and_pac_road_warrior_in_firewall = (
                config["zscalerClientConnector1AndPacRoadWarriorInFirewall"]
                if "zscalerClientConnector1AndPacRoadWarriorInFirewall" in config
                else False
            )
            self.cascade_url_filtering = config["cascadeUrlFiltering"] if "cascadeUrlFiltering" in config else False
            self.enable_policy_for_unauthenticated_traffic = (
                config["enablePolicyForUnauthenticatedTraffic"] if "enablePolicyForUnauthenticatedTraffic" in config else False
            )
            self.block_non_compliant_http_request_on_http_ports = (
                config["blockNonCompliantHttpRequestOnHttpPorts"]
                if "blockNonCompliantHttpRequestOnHttpPorts" in config
                else False
            )
            self.enable_admin_rank_access = config["enableAdminRankAccess"] if "enableAdminRankAccess" in config else False
            self.ui_session_timeout = config["uiSessionTimeout"] if "uiSessionTimeout" in config else None
            self.http2_nonbrowser_traffic_enabled = (
                config["http2NonbrowserTrafficEnabled"] if "http2NonbrowserTrafficEnabled" in config else False
            )
            self.ecs_for_all_enabled = config["ecsForAllEnabled"] if "ecsForAllEnabled" in config else False
            self.dynamic_user_risk_enabled = config["dynamicUserRiskEnabled"] if "dynamicUserRiskEnabled" in config else False
            self.block_connect_host_sni_mismatch = (
                config["blockConnectHostSniMismatch"] if "blockConnectHostSniMismatch" in config else False
            )
            self.prefer_sni_over_conn_host = config["preferSniOverConnHost"] if "preferSniOverConnHost" in config else False
            self.sipa_xff_header_enabled = config["sipaXffHeaderEnabled"] if "sipaXffHeaderEnabled" in config else False
            self.block_non_http_on_http_port_enabled = (
                config["blockNonHttpOnHttpPortEnabled"] if "blockNonHttpOnHttpPortEnabled" in config else False
            )

            self.auth_bypass_url_categories = ZscalerCollection.form_list(
                config["authBypassUrlCategories"] if "authBypassUrlCategories" in config else [], str
            )
            self.domain_fronting_bypass_url_categories = ZscalerCollection.form_list(
                config["domainFrontingBypassUrlCategories"] if "domainFrontingBypassUrlCategories" in config else [], str
            )
            self.auth_bypass_urls = ZscalerCollection.form_list(
                config["authBypassUrls"] if "authBypassUrls" in config else [], str
            )
            self.auth_bypass_apps = ZscalerCollection.form_list(
                config["authBypassApps"] if "authBypassApps" in config else [], str
            )
            self.kerberos_bypass_url_categories = ZscalerCollection.form_list(
                config["kerberosBypassUrlCategories"] if "kerberosBypassUrlCategories" in config else [], str
            )
            self.kerberos_bypass_urls = ZscalerCollection.form_list(
                config["kerberosBypassUrls"] if "kerberosBypassUrls" in config else [], str
            )
            self.kerberos_bypass_apps = ZscalerCollection.form_list(
                config["kerberosBypassApps"] if "kerberosBypassApps" in config else [], str
            )
            self.basic_bypass_url_categories = ZscalerCollection.form_list(
                config["basicBypassUrlCategories"] if "basicBypassUrlCategories" in config else [], str
            )
            self.basic_bypass_apps = ZscalerCollection.form_list(
                config["basicBypassApps"] if "basicBypassApps" in config else [], str
            )
            self.http_range_header_remove_url_categories = ZscalerCollection.form_list(
                config["httpRangeHeaderRemoveUrlCategories"] if "httpRangeHeaderRemoveUrlCategories" in config else [], str
            )
            self.digest_auth_bypass_url_categories = ZscalerCollection.form_list(
                config["digestAuthBypassUrlCategories"] if "digestAuthBypassUrlCategories" in config else [], str
            )
            self.digest_auth_bypass_urls = ZscalerCollection.form_list(
                config["digestAuthBypassUrls"] if "digestAuthBypassUrls" in config else [], str
            )
            self.digest_auth_bypass_apps = ZscalerCollection.form_list(
                config["digestAuthBypassApps"] if "digestAuthBypassApps" in config else [], str
            )
            self.dns_resolution_on_transparent_proxy_exempt_url_categories = ZscalerCollection.form_list(
                (
                    config["dnsResolutionOnTransparentProxyExemptUrlCategories"]
                    if "dnsResolutionOnTransparentProxyExemptUrlCategories" in config
                    else []
                ),
                str,
            )
            self.dns_resolution_on_transparent_proxy_ipv6_exempt_url_categories = ZscalerCollection.form_list(
                (
                    config["dnsResolutionOnTransparentProxyIPv6ExemptUrlCategories"]
                    if "dnsResolutionOnTransparentProxyIPv6ExemptUrlCategories" in config
                    else []
                ),
                str,
            )
            self.dns_resolution_on_transparent_proxy_exempt_urls = ZscalerCollection.form_list(
                (
                    config["dnsResolutionOnTransparentProxyExemptUrls"]
                    if "dnsResolutionOnTransparentProxyExemptUrls" in config
                    else []
                ),
                str,
            )
            self.dns_resolution_on_transparent_proxy_exempt_apps = ZscalerCollection.form_list(
                (
                    config["dnsResolutionOnTransparentProxyExemptApps"]
                    if "dnsResolutionOnTransparentProxyExemptApps" in config
                    else []
                ),
                str,
            )
            self.dns_resolution_on_transparent_proxy_ipv6_exempt_apps = ZscalerCollection.form_list(
                (
                    config["dnsResolutionOnTransparentProxyIPv6ExemptApps"]
                    if "dnsResolutionOnTransparentProxyIPv6ExemptApps" in config
                    else []
                ),
                str,
            )
            self.dns_resolution_on_transparent_proxy_url_categories = ZscalerCollection.form_list(
                (
                    config["dnsResolutionOnTransparentProxyUrlCategories"]
                    if "dnsResolutionOnTransparentProxyUrlCategories" in config
                    else []
                ),
                str,
            )
            self.dns_resolution_on_transparent_proxy_ipv6_url_categories = ZscalerCollection.form_list(
                (
                    config["dnsResolutionOnTransparentProxyIPv6UrlCategories"]
                    if "dnsResolutionOnTransparentProxyIPv6UrlCategories" in config
                    else []
                ),
                str,
            )
            self.dns_resolution_on_transparent_proxy_urls = ZscalerCollection.form_list(
                config["dnsResolutionOnTransparentProxyUrls"] if "dnsResolutionOnTransparentProxyUrls" in config else [], str
            )
            self.dns_resolution_on_transparent_proxy_apps = ZscalerCollection.form_list(
                config["dnsResolutionOnTransparentProxyApps"] if "dnsResolutionOnTransparentProxyApps" in config else [], str
            )
            self.dns_resolution_on_transparent_proxy_ipv6_apps = ZscalerCollection.form_list(
                (
                    config["dnsResolutionOnTransparentProxyIPv6Apps"]
                    if "dnsResolutionOnTransparentProxyIPv6Apps" in config
                    else []
                ),
                str,
            )
            self.block_domain_fronting_apps = ZscalerCollection.form_list(
                config["blockDomainFrontingApps"] if "blockDomainFrontingApps" in config else [], str
            )
            self.prefer_sni_over_conn_host_apps = ZscalerCollection.form_list(
                config["preferSniOverConnHostApps"] if "preferSniOverConnHostApps" in config else [], str
            )
            self.sni_dns_optimization_bypass_url_categories = ZscalerCollection.form_list(
                config["sniDnsOptimizationBypassUrlCategories"] if "sniDnsOptimizationBypassUrlCategories" in config else [],
                str,
            )
        else:
            self.enable_dns_resolution_on_transparent_proxy = False
            self.enable_ipv6_dns_resolution_on_transparent_proxy = False
            self.enable_ipv6_dns_optimization_on_all_transparent_proxy = False
            self.enable_evaluate_policy_on_global_ssl_bypass = False
            self.enable_office365 = False
            self.log_internal_ip = False
            self.enforce_surrogate_ip_for_windows_app = False
            self.track_http_tunnel_on_http_ports = False
            self.block_http_tunnel_on_non_http_ports = False
            self.block_domain_fronting_on_host_header = False
            self.zscaler_client_connector1_and_pac_road_warrior_in_firewall = False
            self.cascade_url_filtering = False
            self.enable_policy_for_unauthenticated_traffic = False
            self.block_non_compliant_http_request_on_http_ports = False
            self.enable_admin_rank_access = False
            self.ui_session_timeout = None
            self.http2_nonbrowser_traffic_enabled = False
            self.ecs_for_all_enabled = False
            self.dynamic_user_risk_enabled = False
            self.block_connect_host_sni_mismatch = False
            self.prefer_sni_over_conn_host = False
            self.sipa_xff_header_enabled = False
            self.block_non_http_on_http_port_enabled = False
            self.auth_bypass_url_categories = []
            self.domain_fronting_bypass_url_categories = []
            self.auth_bypass_urls = []
            self.auth_bypass_apps = []
            self.kerberos_bypass_url_categories = []
            self.kerberos_bypass_urls = []
            self.kerberos_bypass_apps = []
            self.basic_bypass_url_categories = []
            self.basic_bypass_apps = []
            self.http_range_header_remove_url_categories = []
            self.digest_auth_bypass_url_categories = []
            self.digest_auth_bypass_urls = []
            self.digest_auth_bypass_apps = []
            self.dns_resolution_on_transparent_proxy_exempt_url_categories = []
            self.dns_resolution_on_transparent_proxy_ipv6_exempt_url_categories = []
            self.dns_resolution_on_transparent_proxy_exempt_urls = []
            self.dns_resolution_on_transparent_proxy_exempt_apps = []
            self.dns_resolution_on_transparent_proxy_ipv6_exempt_apps = []
            self.dns_resolution_on_transparent_proxy_url_categories = []
            self.dns_resolution_on_transparent_proxy_ipv6_url_categories = []
            self.dns_resolution_on_transparent_proxy_urls = []
            self.dns_resolution_on_transparent_proxy_apps = []
            self.dns_resolution_on_transparent_proxy_ipv6_apps = []
            self.block_domain_fronting_apps = []
            self.prefer_sni_over_conn_host_apps = []
            self.sni_dns_optimization_bypass_url_categories = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "enableDnsResolutionOnTransparentProxy": self.enable_dns_resolution_on_transparent_proxy,
            "enableIPv6DnsResolutionOnTransparentProxy": self.enable_ipv6_dns_resolution_on_transparent_proxy,
            "enableIPv6DnsOptimizationOnAllTransparentProxy": self.enable_ipv6_dns_optimization_on_all_transparent_proxy,
            "enableEvaluatePolicyOnGlobalSSLBypass": self.enable_evaluate_policy_on_global_ssl_bypass,
            "enableOffice365": self.enable_office365,
            "logInternalIp": self.log_internal_ip,
            "enforceSurrogateIpForWindowsApp": self.enforce_surrogate_ip_for_windows_app,
            "trackHttpTunnelOnHttpPorts": self.track_http_tunnel_on_http_ports,
            "blockHttpTunnelOnNonHttpPorts": self.block_http_tunnel_on_non_http_ports,
            "blockDomainFrontingOnHostHeader": self.block_domain_fronting_on_host_header,
            "zscalerClientConnector1AndPacRoadWarriorInFirewall":
                self.zscaler_client_connector1_and_pac_road_warrior_in_firewall,
            "cascadeUrlFiltering": self.cascade_url_filtering,
            "enablePolicyForUnauthenticatedTraffic": self.enable_policy_for_unauthenticated_traffic,
            "blockNonCompliantHttpRequestOnHttpPorts": self.block_non_compliant_http_request_on_http_ports,
            "enableAdminRankAccess": self.enable_admin_rank_access,
            "uiSessionTimeout": self.ui_session_timeout,
            "http2NonbrowserTrafficEnabled": self.http2_nonbrowser_traffic_enabled,
            "ecsForAllEnabled": self.ecs_for_all_enabled,
            "dynamicUserRiskEnabled": self.dynamic_user_risk_enabled,
            "blockConnectHostSniMismatch": self.block_connect_host_sni_mismatch,
            "preferSniOverConnHost": self.prefer_sni_over_conn_host,
            "sipaXffHeaderEnabled": self.sipa_xff_header_enabled,
            "blockNonHttpOnHttpPortEnabled": self.block_non_http_on_http_port_enabled,
            "authBypassUrlCategories": self.auth_bypass_url_categories,
            "domainFrontingBypassUrlCategories": self.domain_fronting_bypass_url_categories,
            "authBypassUrls": self.auth_bypass_urls,
            "authBypassApps": self.auth_bypass_apps,
            "kerberosBypassUrlCategories": self.kerberos_bypass_url_categories,
            "kerberosBypassUrls": self.kerberos_bypass_urls,
            "kerberosBypassApps": self.kerberos_bypass_apps,
            "basicBypassUrlCategories": self.basic_bypass_url_categories,
            "basicBypassApps": self.basic_bypass_apps,
            "httpRangeHeaderRemoveUrlCategories": self.http_range_header_remove_url_categories,
            "digestAuthBypassUrlCategories": self.digest_auth_bypass_url_categories,
            "digestAuthBypassUrls": self.digest_auth_bypass_urls,
            "digestAuthBypassApps": self.digest_auth_bypass_apps,
            "dnsResolutionOnTransparentProxyExemptUrlCategories":
                self.dns_resolution_on_transparent_proxy_exempt_url_categories,
            "dnsResolutionOnTransparentProxyIPv6ExemptUrlCategories":
                self.dns_resolution_on_transparent_proxy_ipv6_exempt_url_categories,
            "dnsResolutionOnTransparentProxyExemptUrls": self.dns_resolution_on_transparent_proxy_exempt_urls,
            "dnsResolutionOnTransparentProxyExemptApps": self.dns_resolution_on_transparent_proxy_exempt_apps,
            "dnsResolutionOnTransparentProxyIPv6ExemptApps": self.dns_resolution_on_transparent_proxy_ipv6_exempt_apps,
            "dnsResolutionOnTransparentProxyUrlCategories": self.dns_resolution_on_transparent_proxy_url_categories,
            "dnsResolutionOnTransparentProxyIPv6UrlCategories": self.dns_resolution_on_transparent_proxy_ipv6_url_categories,
            "dnsResolutionOnTransparentProxyUrls": self.dns_resolution_on_transparent_proxy_urls,
            "dnsResolutionOnTransparentProxyApps": self.dns_resolution_on_transparent_proxy_apps,
            "dnsResolutionOnTransparentProxyIPv6Apps": self.dns_resolution_on_transparent_proxy_ipv6_apps,
            "blockDomainFrontingApps": self.block_domain_fronting_apps,
            "preferSniOverConnHostApps": self.prefer_sni_over_conn_host_apps,
            "sniDnsOptimizationBypassUrlCategories": self.sni_dns_optimization_bypass_url_categories,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
