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

# ZCC Forwarding Profile model.
#
# Every wire key in this file is the source of truth for ZCC's
# ``/zcc/papi/public/v1/webForwardingProfile/edit`` payload. The ZCC
# serializer (``zscaler/zcc/_serialize.py``) introspects each
# ``request_format`` below to translate snake_case input from callers
# into the exact wire casing the API expects (``UDPTimeout``,
# ``pacURL``, ``actionTypeZIA``, etc.) — so no entries in
# ``FIELD_EXCEPTIONS`` are required.

from typing import Dict, Optional, Any
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class SystemProxyData(ZscalerObject):
    """A class for the ``systemProxyData`` block."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.bypass_proxy_for_private_ip = (
                config["bypassProxyForPrivateIP"] if "bypassProxyForPrivateIP" in config else None
            )
            self.enable_auto_detect = config["enableAutoDetect"] if "enableAutoDetect" in config else None
            self.enable_pac = config["enablePAC"] if "enablePAC" in config else None
            self.enable_proxy_server = config["enableProxyServer"] if "enableProxyServer" in config else None
            self.pac_url = config["pacURL"] if "pacURL" in config else None
            self.pac_data_path = config["pacDataPath"] if "pacDataPath" in config else None
            self.perform_gp_update = config["performGPUpdate"] if "performGPUpdate" in config else None
            self.proxy_action = config["proxyAction"] if "proxyAction" in config else None
            self.proxy_server_address = config["proxyServerAddress"] if "proxyServerAddress" in config else None
            self.proxy_server_port = config["proxyServerPort"] if "proxyServerPort" in config else None
        else:
            self.bypass_proxy_for_private_ip = None
            self.enable_auto_detect = None
            self.enable_pac = None
            self.enable_proxy_server = None
            self.pac_url = None
            self.pac_data_path = None
            self.perform_gp_update = None
            self.proxy_action = None
            self.proxy_server_address = None
            self.proxy_server_port = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "bypassProxyForPrivateIP": self.bypass_proxy_for_private_ip,
            "enableAutoDetect": self.enable_auto_detect,
            "enablePAC": self.enable_pac,
            "enableProxyServer": self.enable_proxy_server,
            "pacURL": self.pac_url,
            "pacDataPath": self.pac_data_path,
            "performGPUpdate": self.perform_gp_update,
            "proxyAction": self.proxy_action,
            "proxyServerAddress": self.proxy_server_address,
            "proxyServerPort": self.proxy_server_port,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PartnerInfo(ZscalerObject):
    """A class for the ``partnerInfo`` block on a ZPA forwarding action."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.allow_tls_fallback = config["allowTlsFallback"] if "allowTlsFallback" in config else None
            self.mtu_for_zadapter = config["mtuForZadapter"] if "mtuForZadapter" in config else None
            self.primary_transport = config["primaryTransport"] if "primaryTransport" in config else None
        else:
            self.allow_tls_fallback = None
            self.mtu_for_zadapter = None
            self.primary_transport = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "primaryTransport": self.primary_transport,
            "mtuForZadapter": self.mtu_for_zadapter,
            "allowTlsFallback": self.allow_tls_fallback,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ForwardingProfileActions(ZscalerObject):
    """An entry inside ``forwardingProfileActions``."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.action_type = config["actionType"] if "actionType" in config else None
            self.enable_packet_tunnel = config["enablePacketTunnel"] if "enablePacketTunnel" in config else None
            self.block_unreachable_domains_traffic = (
                config["blockUnreachableDomainsTraffic"] if "blockUnreachableDomainsTraffic" in config else None
            )
            self.drop_ipv6_traffic = config["dropIpv6Traffic"] if "dropIpv6Traffic" in config else None
            self.drop_ipv6_traffic_in_ipv6_network = (
                config["dropIpv6TrafficInIpv6Network"] if "dropIpv6TrafficInIpv6Network" in config else None
            )
            self.primary_transport = config["primaryTransport"] if "primaryTransport" in config else None
            self.udp_timeout = config["UDPTimeout"] if "UDPTimeout" in config else None
            self.dtls_timeout = config["DTLSTimeout"] if "DTLSTimeout" in config else None
            self.tls_timeout = config["TLSTimeout"] if "TLSTimeout" in config else None
            self.mtu_for_zadapter = config["mtuForZadapter"] if "mtuForZadapter" in config else None
            self.allow_tls_fallback = config["allowTLSFallback"] if "allowTLSFallback" in config else None
            self.path_mtu_discovery = config["pathMtuDiscovery"] if "pathMtuDiscovery" in config else None
            self.tunnel2_fallback_type = config["tunnel2FallbackType"] if "tunnel2FallbackType" in config else None
            self.use_tunnel2_for_proxied_web_traffic = (
                config["useTunnel2ForProxiedWebTraffic"] if "useTunnel2ForProxiedWebTraffic" in config else None
            )
            self.use_tunnel2_for_unencrypted_web_traffic = (
                config["useTunnel2ForUnencryptedWebTraffic"]
                if "useTunnel2ForUnencryptedWebTraffic" in config
                else None
            )
            self.redirect_web_traffic = config["redirectWebTraffic"] if "redirectWebTraffic" in config else None
            self.drop_ipv6_include_traffic_in_t2 = (
                config["dropIpv6IncludeTrafficInT2"] if "dropIpv6IncludeTrafficInT2" in config else None
            )
            self.custom_pac = config["customPac"] if "customPac" in config else None
            self.system_proxy_data = SystemProxyData(config["systemProxyData"]) if "systemProxyData" in config else None
            self.latency_based_zen_enablement = (
                config["latencyBasedZenEnablement"] if "latencyBasedZenEnablement" in config else None
            )
            self.zen_probe_interval = config["zenProbeInterval"] if "zenProbeInterval" in config else None
            self.zen_probe_sample_size = config["zenProbeSampleSize"] if "zenProbeSampleSize" in config else None
            self.zen_threshold_limit = config["zenThresholdLimit"] if "zenThresholdLimit" in config else None
            self.latency_based_server_enablement = (
                config["latencyBasedServerEnablement"] if "latencyBasedServerEnablement" in config else None
            )
            self.lbs_probe_interval = config["lbsProbeInterval"] if "lbsProbeInterval" in config else None
            self.lbs_probe_sample_size = config["lbsProbeSampleSize"] if "lbsProbeSampleSize" in config else None
            self.lbs_threshold_limit = config["lbsThresholdLimit"] if "lbsThresholdLimit" in config else None
            self.latency_based_server_mt_enablement = (
                config["latencyBasedServerMTEnablement"] if "latencyBasedServerMTEnablement" in config else None
            )
            self.network_type = config["networkType"] if "networkType" in config else None
            self.is_same_as_on_trusted_network = (
                config["isSameAsOnTrustedNetwork"] if "isSameAsOnTrustedNetwork" in config else None
            )
            self.system_proxy = config["systemProxy"] if "systemProxy" in config else None
        else:
            self.action_type = None
            self.enable_packet_tunnel = None
            self.block_unreachable_domains_traffic = None
            self.drop_ipv6_traffic = None
            self.drop_ipv6_traffic_in_ipv6_network = None
            self.primary_transport = None
            self.udp_timeout = None
            self.dtls_timeout = None
            self.tls_timeout = None
            self.mtu_for_zadapter = None
            self.allow_tls_fallback = None
            self.path_mtu_discovery = None
            self.tunnel2_fallback_type = None
            self.use_tunnel2_for_proxied_web_traffic = None
            self.use_tunnel2_for_unencrypted_web_traffic = None
            self.redirect_web_traffic = None
            self.drop_ipv6_include_traffic_in_t2 = None
            self.custom_pac = None
            self.system_proxy_data = None
            self.latency_based_zen_enablement = None
            self.zen_probe_interval = None
            self.zen_probe_sample_size = None
            self.zen_threshold_limit = None
            self.latency_based_server_enablement = None
            self.lbs_probe_interval = None
            self.lbs_probe_sample_size = None
            self.lbs_threshold_limit = None
            self.latency_based_server_mt_enablement = None
            self.network_type = None
            self.is_same_as_on_trusted_network = None
            self.system_proxy = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "actionType": self.action_type,
            "enablePacketTunnel": self.enable_packet_tunnel,
            "blockUnreachableDomainsTraffic": self.block_unreachable_domains_traffic,
            "dropIpv6Traffic": self.drop_ipv6_traffic,
            "dropIpv6TrafficInIpv6Network": self.drop_ipv6_traffic_in_ipv6_network,
            "primaryTransport": self.primary_transport,
            "UDPTimeout": self.udp_timeout,
            "DTLSTimeout": self.dtls_timeout,
            "TLSTimeout": self.tls_timeout,
            "mtuForZadapter": self.mtu_for_zadapter,
            "allowTLSFallback": self.allow_tls_fallback,
            "pathMtuDiscovery": self.path_mtu_discovery,
            "tunnel2FallbackType": self.tunnel2_fallback_type,
            "useTunnel2ForProxiedWebTraffic": self.use_tunnel2_for_proxied_web_traffic,
            "useTunnel2ForUnencryptedWebTraffic": self.use_tunnel2_for_unencrypted_web_traffic,
            "redirectWebTraffic": self.redirect_web_traffic,
            "dropIpv6IncludeTrafficInT2": self.drop_ipv6_include_traffic_in_t2,
            "customPac": self.custom_pac,
            "systemProxyData": self.system_proxy_data,
            "latencyBasedZenEnablement": self.latency_based_zen_enablement,
            "zenProbeInterval": self.zen_probe_interval,
            "zenProbeSampleSize": self.zen_probe_sample_size,
            "zenThresholdLimit": self.zen_threshold_limit,
            "latencyBasedServerEnablement": self.latency_based_server_enablement,
            "lbsProbeInterval": self.lbs_probe_interval,
            "lbsProbeSampleSize": self.lbs_probe_sample_size,
            "lbsThresholdLimit": self.lbs_threshold_limit,
            "latencyBasedServerMTEnablement": self.latency_based_server_mt_enablement,
            "networkType": self.network_type,
            "isSameAsOnTrustedNetwork": self.is_same_as_on_trusted_network,
            "systemProxy": self.system_proxy,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ForwardingProfileZpaActions(ZscalerObject):
    """An entry inside ``forwardingProfileZpaActions``."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.action_type = config["actionType"] if "actionType" in config else None
            self.primary_transport = config["primaryTransport"] if "primaryTransport" in config else None
            self.dtls_timeout = config["DTLSTimeout"] if "DTLSTimeout" in config else None
            self.tls_timeout = config["TLSTimeout"] if "TLSTimeout" in config else None
            self.mtu_for_zadapter = config["mtuForZadapter"] if "mtuForZadapter" in config else None
            self.partner_info = PartnerInfo(config["partnerInfo"]) if "partnerInfo" in config else None
            self.latency_based_server_enablement = (
                config["latencyBasedServerEnablement"] if "latencyBasedServerEnablement" in config else None
            )
            self.lbs_probe_sample_size = config["lbsProbeSampleSize"] if "lbsProbeSampleSize" in config else None
            self.lbs_threshold_limit = config["lbsThresholdLimit"] if "lbsThresholdLimit" in config else None
            self.lbs_probe_interval = config["lbsProbeInterval"] if "lbsProbeInterval" in config else None
            self.latency_based_server_mt_enablement = (
                config["latencyBasedServerMTEnablement"] if "latencyBasedServerMTEnablement" in config else None
            )
            self.network_type = config["networkType"] if "networkType" in config else None
            self.is_same_as_on_trusted_network = (
                config["isSameAsOnTrustedNetwork"] if "isSameAsOnTrustedNetwork" in config else None
            )
            self.send_trusted_network_result_to_zpa = (
                config["sendTrustedNetworkResultToZpa"] if "sendTrustedNetworkResultToZpa" in config else None
            )
        else:
            self.action_type = None
            self.primary_transport = None
            self.dtls_timeout = None
            self.tls_timeout = None
            self.mtu_for_zadapter = None
            self.partner_info = None
            self.latency_based_server_enablement = None
            self.lbs_probe_sample_size = None
            self.lbs_threshold_limit = None
            self.lbs_probe_interval = None
            self.latency_based_server_mt_enablement = None
            self.network_type = None
            self.is_same_as_on_trusted_network = None
            self.send_trusted_network_result_to_zpa = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "actionType": self.action_type,
            "primaryTransport": self.primary_transport,
            "DTLSTimeout": self.dtls_timeout,
            "TLSTimeout": self.tls_timeout,
            "mtuForZadapter": self.mtu_for_zadapter,
            "partnerInfo": self.partner_info,
            "latencyBasedServerEnablement": self.latency_based_server_enablement,
            "lbsProbeSampleSize": self.lbs_probe_sample_size,
            "lbsThresholdLimit": self.lbs_threshold_limit,
            "lbsProbeInterval": self.lbs_probe_interval,
            "latencyBasedServerMTEnablement": self.latency_based_server_mt_enablement,
            "networkType": self.network_type,
            "isSameAsOnTrustedNetwork": self.is_same_as_on_trusted_network,
            "sendTrustedNetworkResultToZpa": self.send_trusted_network_result_to_zpa,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class UnifiedTunnel(ZscalerObject):
    """An entry inside ``unifiedTunnel``."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.block_unreachable_domains_traffic = (
                config["blockUnreachableDomainsTraffic"] if "blockUnreachableDomainsTraffic" in config else None
            )
            self.drop_ipv6_traffic = config["dropIpv6Traffic"] if "dropIpv6Traffic" in config else None
            self.primary_transport = config["primaryTransport"] if "primaryTransport" in config else None
            self.dtls_timeout = config["DTLSTimeout"] if "DTLSTimeout" in config else None
            self.tls_timeout = config["TLSTimeout"] if "TLSTimeout" in config else None
            self.mtu_for_zadapter = config["mtuForZadapter"] if "mtuForZadapter" in config else None
            self.allow_tls_fallback = config["allowTLSFallback"] if "allowTLSFallback" in config else None
            self.path_mtu_discovery = config["pathMtuDiscovery"] if "pathMtuDiscovery" in config else None
            self.tunnel2_fallback_type = config["tunnel2FallbackType"] if "tunnel2FallbackType" in config else None
            self.redirect_web_traffic = config["redirectWebTraffic"] if "redirectWebTraffic" in config else None
            self.drop_ipv6_include_traffic_in_t2 = (
                config["dropIpv6IncludeTrafficInT2"] if "dropIpv6IncludeTrafficInT2" in config else None
            )
            self.system_proxy_data = SystemProxyData(config["systemProxyData"]) if "systemProxyData" in config else None
            self.network_type = config["networkType"] if "networkType" in config else None
            self.same_as_on_trusted = config["sameAsOnTrusted"] if "sameAsOnTrusted" in config else None
            self.action_type_zia = config["actionTypeZIA"] if "actionTypeZIA" in config else None
            self.action_type_zpa = config["actionTypeZPA"] if "actionTypeZPA" in config else None
        else:
            self.block_unreachable_domains_traffic = None
            self.drop_ipv6_traffic = None
            self.primary_transport = None
            self.dtls_timeout = None
            self.tls_timeout = None
            self.mtu_for_zadapter = None
            self.allow_tls_fallback = None
            self.path_mtu_discovery = None
            self.tunnel2_fallback_type = None
            self.redirect_web_traffic = None
            self.drop_ipv6_include_traffic_in_t2 = None
            self.system_proxy_data = None
            self.network_type = None
            self.same_as_on_trusted = None
            self.action_type_zia = None
            self.action_type_zpa = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "blockUnreachableDomainsTraffic": self.block_unreachable_domains_traffic,
            "dropIpv6Traffic": self.drop_ipv6_traffic,
            "primaryTransport": self.primary_transport,
            "DTLSTimeout": self.dtls_timeout,
            "TLSTimeout": self.tls_timeout,
            "mtuForZadapter": self.mtu_for_zadapter,
            "allowTLSFallback": self.allow_tls_fallback,
            "pathMtuDiscovery": self.path_mtu_discovery,
            "tunnel2FallbackType": self.tunnel2_fallback_type,
            "redirectWebTraffic": self.redirect_web_traffic,
            "dropIpv6IncludeTrafficInT2": self.drop_ipv6_include_traffic_in_t2,
            "systemProxyData": self.system_proxy_data,
            "networkType": self.network_type,
            "sameAsOnTrusted": self.same_as_on_trusted,
            "actionTypeZIA": self.action_type_zia,
            "actionTypeZPA": self.action_type_zpa,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ForwardingProfile(ZscalerObject):
    """A class for ForwardingProfile objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.active = config["active"] if "active" in config else None
            self.add_condition = config["addCondition"] if "addCondition" in config else None
            self.condition = config["condition"] if "condition" in config else None
            self.condition_type = config["conditionType"] if "conditionType" in config else None
            self.dns_servers = config["dnsServers"] if "dnsServers" in config else None
            self.dns_search_domains = config["dnsSearchDomains"] if "dnsSearchDomains" in config else None
            self.hostname = config["hostname"] if "hostname" in config else None
            self.resolved_ips_for_hostname = (
                config["resolvedIpsForHostname"] if "resolvedIpsForHostname" in config else None
            )
            self.trusted_subnets = config["trustedSubnets"] if "trustedSubnets" in config else None
            self.trusted_gateways = config["trustedGateways"] if "trustedGateways" in config else None
            self.trusted_dhcp_servers = config["trustedDhcpServers"] if "trustedDhcpServers" in config else None
            self.trusted_egress_ips = config["trustedEgressIps"] if "trustedEgressIps" in config else None
            self.enable_unified_tunnel = config["enableUnifiedTunnel"] if "enableUnifiedTunnel" in config else None
            self.enable_lwf_driver = config["enableLWFDriver"] if "enableLWFDriver" in config else None
            self.enable_split_vpn_tn = config["enableSplitVpnTN"] if "enableSplitVpnTN" in config else None
            self.enable_all_default_adapters_tn = (
                config["enableAllDefaultAdaptersTN"] if "enableAllDefaultAdaptersTN" in config else None
            )
            self.skip_trusted_criteria_match = (
                config["skipTrustedCriteriaMatch"] if "skipTrustedCriteriaMatch" in config else None
            )
            self.evaluate_trusted_network = (
                config["evaluateTrustedNetwork"] if "evaluateTrustedNetwork" in config else None
            )
            self.predefined_trusted_networks = (
                config["predefinedTrustedNetworks"] if "predefinedTrustedNetworks" in config else None
            )
            self.predefined_tn_all = config["predefinedTnAll"] if "predefinedTnAll" in config else None
            self.predefined_trusted_network_option = (
                config["predefinedTrustedNetworkOption"] if "predefinedTrustedNetworkOption" in config else None
            )
            self.trusted_network_ids = ZscalerCollection.form_list(
                config["trustedNetworkIds"] if "trustedNetworkIds" in config else [], str
            )
            self.trusted_networks = ZscalerCollection.form_list(
                config["trustedNetworks"] if "trustedNetworks" in config else [], str
            )
            self.forwarding_profile_actions = ZscalerCollection.form_list(
                config["forwardingProfileActions"] if "forwardingProfileActions" in config else [],
                ForwardingProfileActions,
            )
            self.forwarding_profile_zpa_actions = ZscalerCollection.form_list(
                config["forwardingProfileZpaActions"] if "forwardingProfileZpaActions" in config else [],
                ForwardingProfileZpaActions,
            )
            self.unified_tunnel = ZscalerCollection.form_list(
                config["unifiedTunnel"] if "unifiedTunnel" in config else [], UnifiedTunnel
            )
        else:
            self.id = None
            self.name = None
            self.active = None
            self.add_condition = None
            self.condition = None
            self.condition_type = None
            self.dns_servers = None
            self.dns_search_domains = None
            self.hostname = None
            self.resolved_ips_for_hostname = None
            self.trusted_subnets = None
            self.trusted_gateways = None
            self.trusted_dhcp_servers = None
            self.trusted_egress_ips = None
            self.enable_unified_tunnel = None
            self.enable_lwf_driver = None
            self.enable_split_vpn_tn = None
            self.enable_all_default_adapters_tn = None
            self.skip_trusted_criteria_match = None
            self.evaluate_trusted_network = None
            self.predefined_trusted_networks = None
            self.predefined_tn_all = None
            self.predefined_trusted_network_option = None
            self.trusted_network_ids = ZscalerCollection.form_list([], str)
            self.trusted_networks = ZscalerCollection.form_list([], str)
            self.forwarding_profile_actions = ZscalerCollection.form_list([], ForwardingProfileActions)
            self.forwarding_profile_zpa_actions = ZscalerCollection.form_list([], ForwardingProfileZpaActions)
            self.unified_tunnel = ZscalerCollection.form_list([], UnifiedTunnel)

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "addCondition": self.add_condition,
            "condition": self.condition,
            "conditionType": self.condition_type,
            "dnsServers": self.dns_servers,
            "dnsSearchDomains": self.dns_search_domains,
            "hostname": self.hostname,
            "resolvedIpsForHostname": self.resolved_ips_for_hostname,
            "trustedSubnets": self.trusted_subnets,
            "trustedGateways": self.trusted_gateways,
            "trustedDhcpServers": self.trusted_dhcp_servers,
            "trustedEgressIps": self.trusted_egress_ips,
            "enableUnifiedTunnel": self.enable_unified_tunnel,
            "enableLWFDriver": self.enable_lwf_driver,
            "enableSplitVpnTN": self.enable_split_vpn_tn,
            "enableAllDefaultAdaptersTN": self.enable_all_default_adapters_tn,
            "skipTrustedCriteriaMatch": self.skip_trusted_criteria_match,
            "evaluateTrustedNetwork": self.evaluate_trusted_network,
            "predefinedTrustedNetworks": self.predefined_trusted_networks,
            "predefinedTnAll": self.predefined_tn_all,
            "predefinedTrustedNetworkOption": self.predefined_trusted_network_option,
            "trustedNetworkIds": self.trusted_network_ids,
            "trustedNetworks": self.trusted_networks,
            "forwardingProfileActions": self.forwarding_profile_actions,
            "forwardingProfileZpaActions": self.forwarding_profile_zpa_actions,
            "unifiedTunnel": self.unified_tunnel,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
