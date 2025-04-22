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


class ForwardingProfile(ZscalerObject):
    """
    A class for ForwardingProfile objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ForwardingProfile model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.condition_type = config["conditionType"] if "conditionType" in config else None
            self.dns_search_domains = config["dnsSearchDomains"] if "dnsSearchDomains" in config else None
            self.dns_servers = config["dnsServers"] if "dnsServers" in config else None
            self.enable_lwf_driver = config["enableLWFDriver"] if "enableLWFDriver" in config else None
            self.enable_split_vpn_t_n = config["enableSplitVpnTN"] if "enableSplitVpnTN" in config else None
            self.evaluate_trusted_network = config["evaluateTrustedNetwork"] if "evaluateTrustedNetwork" in config else None
            self.forwarding_profile_actions = ZscalerCollection.form_list(
                config["forwardingProfileActions"] if "forwardingProfileActions" in config else [], ForwardingProfileActions
            )
            self.forwarding_profile_zpa_actions = ZscalerCollection.form_list(
                config["forwardingProfileZpaActions"] if "forwardingProfileZpaActions" in config else [],
                ForwardingProfileZpaActions,
            )

            self.hostname = config["hostname"] if "hostname" in config else None
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.predefined_tn_all = config["predefinedTnAll"] if "predefinedTnAll" in config else None
            self.predefined_trusted_networks = (
                config["predefinedTrustedNetworks"] if "predefinedTrustedNetworks" in config else None
            )
            self.resolved_ips_for_hostname = config["resolvedIpsForHostname"] if "resolvedIpsForHostname" in config else None
            self.skip_trusted_criteria_match = (
                config["skipTrustedCriteriaMatch"] if "skipTrustedCriteriaMatch" in config else None
            )
            self.trusted_dhcp_servers = config["trustedDhcpServers"] if "trustedDhcpServers" in config else None
            self.trusted_egress_ips = config["trustedEgressIps"] if "trustedEgressIps" in config else None
            self.trusted_gateways = config["trustedGateways"] if "trustedGateways" in config else None
            self.trusted_network_ids = ZscalerCollection.form_list(
                config["trustedNetworkIds"] if "trustedNetworkIds" in config else [], str
            )
            self.trusted_networks = ZscalerCollection.form_list(
                config["trustedNetworks"] if "trustedNetworks" in config else [], str
            )
            self.trusted_subnets = config["trustedSubnets"] if "trustedSubnets" in config else None
        else:
            self.active = None
            self.condition_type = None
            self.dns_search_domains = None
            self.dns_servers = None
            self.enable_lwf_driver = None
            self.enable_split_vpn_t_n = None
            self.evaluate_trusted_network = None
            self.forwarding_profile_actions = ZscalerCollection.form_list([], str)
            self.forwarding_profile_zpa_actions = ZscalerCollection.form_list([], str)
            self.hostname = None
            self.id = None
            self.name = None
            self.predefined_tn_all = None
            self.predefined_trusted_networks = None
            self.resolved_ips_for_hostname = None
            self.skip_trusted_criteria_match = None
            self.trusted_dhcp_servers = None
            self.trusted_egress_ips = None
            self.trusted_gateways = None
            self.trusted_network_ids = ZscalerCollection.form_list([], str)
            self.trusted_networks = ZscalerCollection.form_list([], str)
            self.trusted_subnets = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "conditionType": self.condition_type,
            "dnsSearchDomains": self.dns_search_domains,
            "dnsServers": self.dns_servers,
            "enableLWFDriver": self.enable_lwf_driver,
            "enableSplitVpnTN": self.enable_split_vpn_t_n,
            "evaluateTrustedNetwork": self.evaluate_trusted_network,
            "forwardingProfileActions": self.forwarding_profile_actions,
            "forwardingProfileZpaActions": self.forwarding_profile_zpa_actions,
            "hostname": self.hostname,
            "id": self.id,
            "name": self.name,
            "predefinedTnAll": self.predefined_tn_all,
            "predefinedTrustedNetworks": self.predefined_trusted_networks,
            "resolvedIpsForHostname": self.resolved_ips_for_hostname,
            "skipTrustedCriteriaMatch": self.skip_trusted_criteria_match,
            "trustedDhcpServers": self.trusted_dhcp_servers,
            "trustedEgressIps": self.trusted_egress_ips,
            "trustedGateways": self.trusted_gateways,
            "trustedNetworkIds": self.trusted_network_ids,
            "trustedNetworks": self.trusted_networks,
            "trustedSubnets": self.trusted_subnets,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ForwardingProfileActions(ZscalerObject):
    """
    A class for ForwardingProfileActions objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ForwardingProfileActions model based on the JSON response.

        Args:
            config (dict): A dictionary representing the configuration (each item of 'forwardingProfileActions').
        """
        super().__init__(config)

        if config:
            self.dtls_timeout = config["DTLSTimeout"] if "DTLSTimeout" in config else None
            self.tls_timeout = config["TLSTimeout"] if "TLSTimeout" in config else None
            self.udp_timeout = config["UDPTimeout"] if "UDPTimeout" in config else None

            self.action_type = config["actionType"] if "actionType" in config else None
            self.allow_tls_fallback = config["allowTLSFallback"] if "allowTLSFallback" in config else None
            self.block_unreachable_domains_traffic = (
                config["blockUnreachableDomainsTraffic"] if "blockUnreachableDomainsTraffic" in config else None
            )
            self.custom_pac = config["customPac"] if "customPac" in config else None
            self.drop_ipv6_include_traffic_in_t2 = (
                config["dropIpv6IncludeTrafficInT2"] if "dropIpv6IncludeTrafficInT2" in config else None
            )
            self.drop_ipv6_traffic = config["dropIpv6Traffic"] if "dropIpv6Traffic" in config else None
            self.drop_ipv6_traffic_in_ipv6_network = (
                config["dropIpv6TrafficInIpv6Network"] if "dropIpv6TrafficInIpv6Network" in config else None
            )
            self.enable_packet_tunnel = config["enablePacketTunnel"] if "enablePacketTunnel" in config else None
            self.latency_based_zen_enablement = (
                config["latencyBasedZenEnablement"] if "latencyBasedZenEnablement" in config else None
            )
            self.mtu_for_zadapter = config["mtuForZadapter"] if "mtuForZadapter" in config else None
            self.network_type = config["networkType"] if "networkType" in config else None
            self.path_mtu_discovery = config["pathMtuDiscovery"] if "pathMtuDiscovery" in config else None
            self.primary_transport = config["primaryTransport"] if "primaryTransport" in config else None
            self.redirect_web_traffic = config["redirectWebTraffic"] if "redirectWebTraffic" in config else None
            self.system_proxy = config["systemProxy"] if "systemProxy" in config else None
            self.tunnel2_fallback = config["tunnel2Fallback"] if "tunnel2Fallback" in config else None
            self.use_tunnel2_for_proxied_web_traffic = (
                config["useTunnel2ForProxiedWebTraffic"] if "useTunnel2ForProxiedWebTraffic" in config else None
            )
            self.zen_probe_interval = config["zenProbeInterval"] if "zenProbeInterval" in config else None
            self.zen_probe_sample_size = config["zenProbeSampleSize"] if "zenProbeSampleSize" in config else None
            self.zen_threshold_limit = config["zenThresholdLimit"] if "zenThresholdLimit" in config else None

            # Parse systemProxyData as a nested dictionary, also in a defensive way
            if "systemProxyData" in config:
                spd = config["systemProxyData"] or {}
                self.system_proxy_data = {
                    "bypassProxyForPrivateIP": spd["bypassProxyForPrivateIP"] if "bypassProxyForPrivateIP" in spd else None,
                    "enableAutoDetect": spd["enableAutoDetect"] if "enableAutoDetect" in spd else None,
                    "enablePAC": spd["enablePAC"] if "enablePAC" in spd else None,
                    "enableProxyServer": spd["enableProxyServer"] if "enableProxyServer" in spd else None,
                    "pacDataPath": spd["pacDataPath"] if "pacDataPath" in spd else None,
                    "pacURL": spd["pacURL"] if "pacURL" in spd else None,
                    "performGPUpdate": spd["performGPUpdate"] if "performGPUpdate" in spd else None,
                    "proxyAction": spd["proxyAction"] if "proxyAction" in spd else None,
                    "proxyServerAddress": spd["proxyServerAddress"] if "proxyServerAddress" in spd else None,
                    "proxyServerPort": spd["proxyServerPort"] if "proxyServerPort" in spd else None,
                }
            else:
                self.system_proxy_data = None

        else:
            # Fallback if config is None
            self.dtls_timeout = None
            self.tls_timeout = None
            self.udp_timeout = None

            self.action_type = None
            self.allow_tls_fallback = None
            self.block_unreachable_domains_traffic = None
            self.custom_pac = None
            self.drop_ipv6_include_traffic_in_t2 = None
            self.drop_ipv6_traffic = None
            self.drop_ipv6_traffic_in_ipv6_network = None
            self.enable_packet_tunnel = None
            self.latency_based_zen_enablement = None
            self.mtu_for_zadapter = None
            self.network_type = None
            self.path_mtu_discovery = None
            self.primary_transport = None
            self.redirect_web_traffic = None
            self.system_proxy = None
            self.tunnel2_fallback_type = None
            self.use_tunnel2_for_proxied_web_traffic = None
            self.zen_probe_interval = None
            self.zen_probe_sample_size = None
            self.zen_threshold_limit = None
            self.system_proxy_data = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "DTLSTimeout": self.dtls_timeout,
            "TLSTimeout": self.tls_timeout,
            "UDPTimeout": self.udp_timeout,
            "actionType": self.action_type,
            "allowTLSFallback": self.allow_tls_fallback,
            "blockUnreachableDomainsTraffic": self.block_unreachable_domains_traffic,
            "customPac": self.custom_pac,
            "dropIpv6IncludeTrafficInT2": self.drop_ipv6_include_traffic_in_t2,
            "dropIpv6Traffic": self.drop_ipv6_traffic,
            "dropIpv6TrafficInIpv6Network": self.drop_ipv6_traffic_in_ipv6_network,
            "enablePacketTunnel": self.enable_packet_tunnel,
            "latencyBasedZenEnablement": self.latency_based_zen_enablement,
            "mtuForZadapter": self.mtu_for_zadapter,
            "networkType": self.network_type,
            "pathMtuDiscovery": self.path_mtu_discovery,
            "primaryTransport": self.primary_transport,
            "redirectWebTraffic": self.redirect_web_traffic,
            "systemProxy": self.system_proxy,
            "tunnel2Fallback": self.tunnel2_fallback,
            "useTunnel2ForProxiedWebTraffic": self.use_tunnel2_for_proxied_web_traffic,
            "zenProbeInterval": self.zen_probe_interval,
            "zenProbeSampleSize": self.zen_probe_sample_size,
            "zenThresholdLimit": self.zen_threshold_limit,
            "systemProxyData": self.system_proxy_data,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ForwardingProfileZpaActions(ZscalerObject):
    """
    A class for ForwardingProfileZpaActions objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ForwardingProfileZpaActions model based on API response.

        Args:
            config (dict): A dictionary representing one item of the 'forwardingProfileZpaActions' array.
        """
        super().__init__(config)

        if config:
            self.dtls_timeout = config["DTLSTimeout"] if "DTLSTimeout" in config else None
            self.tls_timeout = config["TLSTimeout"] if "TLSTimeout" in config else None
            self.action_type = config["actionType"] if "actionType" in config else None
            self.latency_based_server_mt_enablement = (
                config["latencyBasedServerMTEnablement"] if "latencyBasedServerMTEnablement" in config else None
            )
            self.latency_based_zpa_server_enablement = (
                config["latencyBasedZpaServerEnablement"] if "latencyBasedZpaServerEnablement" in config else None
            )
            self.lbs_zpa_probe_interval = config["lbsZpaProbeInterval"] if "lbsZpaProbeInterval" in config else None
            self.lbs_zpa_probe_sample_size = config["lbsZpaProbeSampleSize"] if "lbsZpaProbeSampleSize" in config else None
            self.lbs_zpa_threshold_limit = config["lbsZpaThresholdLimit"] if "lbsZpaThresholdLimit" in config else None
            self.mtu_for_zadapter = config["mtuForZadapter"] if "mtuForZadapter" in config else None
            self.network_type = config["networkType"] if "networkType" in config else None

            # Parse partnerInfo as nested dictionary (defensive)
            if "partnerInfo" in config:
                pi = config["partnerInfo"] or {}
                self.partner_info = {
                    "allowTlsFallback": pi["allowTlsFallback"] if "allowTlsFallback" in pi else None,
                    "mtuForZadapter": pi["mtuForZadapter"] if "mtuForZadapter" in pi else None,
                    "primaryTransport": pi["primaryTransport"] if "primaryTransport" in pi else None,
                }
            else:
                self.partner_info = None

            self.primary_transport = config["primaryTransport"] if "primaryTransport" in config else None
            self.send_trusted_network_result_to_zpa = (
                config["sendTrustedNetworkResultToZpa"] if "sendTrustedNetworkResultToZpa" in config else None
            )

        else:
            # If config is None, default everything
            self.dtls_timeout = None
            self.tls_timeout = None
            self.action_type = None
            self.latency_based_server_mt_enablement = None
            self.latency_based_zpa_server_enablement = None
            self.lbs_zpa_probe_interval = None
            self.lbs_zpa_probe_sample_size = None
            self.lbs_zpa_threshold_limit = None
            self.mtu_for_zadapter = None
            self.network_type = None
            self.partner_info = None
            self.primary_transport = None
            self.send_trusted_network_result_to_zpa = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "DTLSTimeout": self.dtls_timeout,
            "TLSTimeout": self.tls_timeout,
            "actionType": self.action_type,
            "latencyBasedServerMTEnablement": self.latency_based_server_mt_enablement,
            "latencyBasedZpaServerEnablement": self.latency_based_zpa_server_enablement,
            "lbsZpaProbeInterval": self.lbs_zpa_probe_interval,
            "lbsZpaProbeSampleSize": self.lbs_zpa_probe_sample_size,
            "lbsZpaThresholdLimit": self.lbs_zpa_threshold_limit,
            "mtuForZadapter": self.mtu_for_zadapter,
            "networkType": self.network_type,
            "partnerInfo": self.partner_info,  # nested dictionary as parsed
            "primaryTransport": self.primary_transport,
            "sendTrustedNetworkResultToZpa": self.send_trusted_network_result_to_zpa,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
