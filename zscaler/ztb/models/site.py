# flake8: noqa
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

from pydash.strings import camel_case

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


def _get(config: dict, snake_key: str, default=None):
    """Get from config with camelCase or snake_case fallback."""
    if not config:
        return default
    v = config.get(snake_key)
    if v is not None:
        return v
    return config.get(camel_case(snake_key), default)


# ---------------------------------------------------------------------------
# Shared nested types
# ---------------------------------------------------------------------------


class SiteCluster(ZscalerObject):
    """Cluster info nested in Site objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.cluster_id = _get(config, "cluster_id")
            self.nat_enabled = _get(config, "nat_enabled")
            self.user_reachable_ip = _get(config, "user_reachable_ip")
        else:
            self.cluster_id = None
            self.nat_enabled = None
            self.user_reachable_ip = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "nat_enabled": self.nat_enabled,
            "user_reachable_ip": self.user_reachable_ip,
        }


# ---------------------------------------------------------------------------
# GET /api/v2/Site/ - list sites (result.rows)
# GET /api/v2/Site/siteByID/{id}, siteByName/{name} - single site (result)
# ---------------------------------------------------------------------------


class Site(ZscalerObject):
    """Site object from list and get endpoints."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.airgapped_lans = _get(config, "airgapped_lans")
            self.clusters = ZscalerCollection.form_list(config.get("clusters") or [], SiteCluster)
            self.created_at = _get(config, "created_at")
            self.display_name = _get(config, "display_name")
            self.dns = config.get("dns") or []
            self.gateway_type = _get(config, "gateway_type")
            self.id = _get(config, "id")
            self.location_id = _get(config, "location_id")
            self.name = _get(config, "name")
            self.proxy_rt_vlan = _get(config, "proxy_rt_vlan")
            self.public_ip = _get(config, "public_ip")
            self.secret_key = _get(config, "secret_key")
            self.site_status = _get(config, "site_status")
            self.template_id = _get(config, "template_id")
            self.updated_at = _get(config, "updated_at")
            self.use_appseg_static_ip_mapping = _get(config, "use_appseg_static_ip_mapping")
        else:
            self.airgapped_lans = None
            self.clusters = []
            self.created_at = None
            self.display_name = None
            self.dns = []
            self.gateway_type = None
            self.id = None
            self.location_id = None
            self.name = None
            self.proxy_rt_vlan = None
            self.public_ip = None
            self.secret_key = None
            self.site_status = None
            self.template_id = None
            self.updated_at = None
            self.use_appseg_static_ip_mapping = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "airgapped_lans": self.airgapped_lans,
            "clusters": [c.request_format() for c in (self.clusters or [])],
            "created_at": self.created_at,
            "display_name": self.display_name,
            "dns": self.dns,
            "gateway_type": self.gateway_type,
            "id": self.id,
            "location_id": self.location_id,
            "name": self.name,
            "proxy_rt_vlan": self.proxy_rt_vlan,
            "public_ip": self.public_ip,
            "secret_key": self.secret_key,
            "site_status": self.site_status,
            "template_id": self.template_id,
            "updated_at": self.updated_at,
            "use_appseg_static_ip_mapping": self.use_appseg_static_ip_mapping,
        }


# ---------------------------------------------------------------------------
# PUT /api/v2/Site/{siteId} - update body
# ---------------------------------------------------------------------------


class SiteUpdateBody(ZscalerObject):
    """Request body for PUT site update."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.connect_to_hub = _get(config, "connect_to_hub")
            self.display_name = _get(config, "display_name")
            self.dns = _get(config, "dns")
            self.name = _get(config, "name")
            self.nat_enabled = _get(config, "nat_enabled")
            self.proxy_rt_vlan = _get(config, "proxy_rt_vlan")
            self.public_ip = _get(config, "public_ip")
            self.secret_key = _get(config, "secret_key")
        else:
            self.connect_to_hub = None
            self.display_name = None
            self.dns = None
            self.name = None
            self.nat_enabled = None
            self.proxy_rt_vlan = None
            self.public_ip = None
            self.secret_key = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "connect_to_hub": self.connect_to_hub,
            "display_name": self.display_name,
            "dns": self.dns,
            "name": self.name,
            "nat_enabled": self.nat_enabled,
            "proxy_rt_vlan": self.proxy_rt_vlan,
            "public_ip": self.public_ip,
            "secret_key": self.secret_key,
        }


# ---------------------------------------------------------------------------
# GET /api/v2/Site/app_segments
# ---------------------------------------------------------------------------


class AppSegment(ZscalerObject):
    """App segment item from list."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id = _get(config, "id")
            self.name = _get(config, "name")
            self.sites = config.get("sites")
        else:
            self.id = None
            self.name = None
            self.sites = None

    def request_format(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "sites": self.sites}


# ---------------------------------------------------------------------------
# POST /api/v2/Site/cloudSite/ - create cloud gateway body
# ---------------------------------------------------------------------------


class CloudSiteCreateBody(ZscalerObject):
    """Request body for creating cloud gateway site."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.activation_code = _get(config, "activation_code")
            self.customer_name = _get(config, "customer_name")
            self.deployment_type = _get(config, "deployment_type")
            self.enable_backup = _get(config, "enable_backup")
            self.gateway_name = _get(config, "gateway_name")
            self.location = _get(config, "location")
            self.name = _get(config, "name")
            self.plan = _get(config, "plan")
            self.provider = _get(config, "provider")
            self.region = _get(config, "region")
            self.vmsize = _get(config, "vmsize")
        else:
            self.activation_code = None
            self.customer_name = None
            self.deployment_type = None
            self.enable_backup = None
            self.gateway_name = None
            self.location = None
            self.name = None
            self.plan = None
            self.provider = None
            self.region = None
            self.vmsize = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "activation_code": self.activation_code,
            "customer_name": self.customer_name,
            "deployment_type": self.deployment_type,
            "enable_backup": self.enable_backup,
            "gateway_name": self.gateway_name,
            "location": self.location,
            "name": self.name,
            "plan": self.plan,
            "provider": self.provider,
            "region": self.region,
            "vmsize": self.vmsize,
        }


# ---------------------------------------------------------------------------
# GET /api/v2/Site/hostnameconfig
# ---------------------------------------------------------------------------


class HostnameConfig(ZscalerObject):
    """Hostname config result."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            cfg = config.get("result") or config
            if isinstance(cfg, dict):
                self.cluster_id = _get(cfg, "cluster_id")
                self.gateway_display_name = _get(cfg, "gateway_display_name")
                self.site_display_name = _get(cfg, "site_display_name")
            else:
                self.cluster_id = None
                self.gateway_display_name = None
                self.site_display_name = None
        else:
            self.cluster_id = None
            self.gateway_display_name = None
            self.site_display_name = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "gateway_display_name": self.gateway_display_name,
            "site_display_name": self.site_display_name,
        }


# ---------------------------------------------------------------------------
# GET /api/v2/Site/names - result item
# ---------------------------------------------------------------------------


class SiteNameItem(ZscalerObject):
    """Site name item from list names."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.cluster_info = ZscalerCollection.form_list(
                config.get("cluster_info") or config.get("clusterInfo") or [],
                SiteCluster,
            )
            self.display_name = _get(config, "display_name")
            self.gateway_type = _get(config, "gateway_type")
            self.id = _get(config, "id")
            self.name = _get(config, "name")
            self.permissions = _get(config, "permissions")
            self.rks_level = _get(config, "rks_level")
            self.site_status = _get(config, "site_status")
            self.template_id = _get(config, "template_id")
        else:
            self.cluster_info = []
            self.display_name = None
            self.gateway_type = None
            self.id = None
            self.name = None
            self.permissions = None
            self.rks_level = None
            self.site_status = None
            self.template_id = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "cluster_info": [c.request_format() for c in (self.cluster_info or [])],
            "display_name": self.display_name,
            "gateway_type": self.gateway_type,
            "id": self.id,
            "name": self.name,
            "permissions": self.permissions,
            "rks_level": self.rks_level,
            "site_status": self.site_status,
            "template_id": self.template_id,
        }


# ---------------------------------------------------------------------------
# GET /api/v2/Site/siteByID/{id}/overview - nested cluster/connector/gateway types
# ---------------------------------------------------------------------------


class OverviewConnector(ZscalerObject):
    """Connector in overview cluster."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.allowed_ips = _get(config, "allowed_ips")
            self.connector_id = _get(config, "connector_id")
            self.connector_ip = _get(config, "connector_ip")
            self.created_at = _get(config, "created_at")
            self.endpoint = _get(config, "endpoint")
            self.ip_address = _get(config, "ip_address")
            self.latest_handshake = _get(config, "latest_handshake")
            self.name = _get(config, "name")
            self.peer_pubkey = _get(config, "peer_pubkey")
            self.rx = _get(config, "rx")
            self.status_color = _get(config, "status_color")
            self.tx = _get(config, "tx")
            self.updated_at = _get(config, "updated_at")
        else:
            self.allowed_ips = None
            self.connector_id = None
            self.connector_ip = None
            self.created_at = None
            self.endpoint = None
            self.ip_address = None
            self.latest_handshake = None
            self.name = None
            self.peer_pubkey = None
            self.rx = None
            self.status_color = None
            self.tx = None
            self.updated_at = None


class OverviewGateway(ZscalerObject):
    """Gateway in overview cluster."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.activation_link = _get(config, "activation_link")
            self.control_plane = _get(config, "control_plane")
            self.created_at = _get(config, "created_at")
            self.deployment_type = _get(config, "deployment_type")
            self.display_name = _get(config, "display_name")
            self.gateway_id = _get(config, "gateway_id")
            self.gateway_ip_address = _get(config, "gateway_ip_address")
            self.gateway_name = _get(config, "gateway_name")
            self.health_color = _get(config, "health_color")
            self.mgmt_ip = _get(config, "mgmt_ip")
            self.nat_enabled = _get(config, "nat_enabled")
            self.operational_state = _get(config, "operational_state")
            self.public_ip = _get(config, "public_ip")
            self.region = _get(config, "region")
            self.running_version = _get(config, "running_version")
            self.sgw_wireguard_ip = _get(config, "sgw_wireguard_ip")
            self.sgw_wireguard_public_key = _get(config, "sgw_wireguard_public_key")
            self.system_serial_tag = _get(config, "system_serial_tag")
            self.trigger_techsupport = _get(config, "trigger_techsupport")
            self.updated_at = _get(config, "updated_at")
            self.vm_ip_address = _get(config, "vm_ip_address")
            self.vrrp_state = _get(config, "vrrp_state")
            self.wireguard_enabled = _get(config, "wireguard_enabled")
        else:
            self.activation_link = None
            self.control_plane = None
            self.created_at = None
            self.deployment_type = None
            self.display_name = None
            self.gateway_id = None
            self.gateway_ip_address = None
            self.gateway_name = None
            self.health_color = None
            self.mgmt_ip = None
            self.nat_enabled = None
            self.operational_state = None
            self.public_ip = None
            self.region = None
            self.running_version = None
            self.sgw_wireguard_ip = None
            self.sgw_wireguard_public_key = None
            self.system_serial_tag = None
            self.trigger_techsupport = None
            self.updated_at = None
            self.vm_ip_address = None
            self.vrrp_state = None
            self.wireguard_enabled = None


class OverviewCluster(ZscalerObject):
    """Cluster in site overview."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.allowed_commands = _get(config, "allowed_commands")
            self.bgp = config.get("bgp")
            self.cluster_id = _get(config, "cluster_id")
            self.cluster_name = _get(config, "cluster_name")
            self.connect_to_hub = _get(config, "connect_to_hub")
            self.connectors = ZscalerCollection.form_list(config.get("connectors") or [], OverviewConnector)
            self.created_at = _get(config, "created_at")
            self.debug_switch = _get(config, "debug_switch")
            self.dhcp_options = config.get("dhcp_options") or config.get("dhcpOptions")
            self.dhcp_server_ip = _get(config, "dhcp_server_ip")
            self.dhcp_service = _get(config, "dhcp_service")
            self.gateway_type = _get(config, "gateway_type")
            self.gateways = ZscalerCollection.form_list(config.get("gateways") or [], OverviewGateway)
            self.nat_enabled = _get(config, "nat_enabled")
            self.snmp_enabled = _get(config, "snmp_enabled")
            self.syn_ack_target = _get(config, "syn_ack_target")
            self.updated_at = _get(config, "updated_at")
            self.user_reachable_ip = _get(config, "user_reachable_ip")
            self.vlans = config.get("vlans")
            self.vrrp = config.get("vrrp") or config.get("vrrp")
        else:
            self.allowed_commands = None
            self.bgp = None
            self.cluster_id = None
            self.cluster_name = None
            self.connect_to_hub = None
            self.connectors = []
            self.created_at = None
            self.debug_switch = None
            self.dhcp_options = None
            self.dhcp_server_ip = None
            self.dhcp_service = None
            self.gateway_type = None
            self.gateways = []
            self.nat_enabled = None
            self.snmp_enabled = None
            self.syn_ack_target = None
            self.updated_at = None
            self.user_reachable_ip = None
            self.vlans = None
            self.vrrp = None


class SiteOverview(ZscalerObject):
    """Site overview from GET siteByID/{id}/overview."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            res = config.get("result") or config
            if isinstance(res, dict):
                self.clusters = ZscalerCollection.form_list(res.get("clusters") or [], OverviewCluster)
                self.created_at = _get(res, "created_at")
                self.display_name = _get(res, "display_name")
                self.dns = res.get("dns") or []
                self.id = _get(res, "id")
                self.killswitch = _get(res, "killswitch")
                self.name = _get(res, "name")
                self.site_status = _get(res, "site_status")
                self.template_id = _get(res, "template_id")
                self.template_name = _get(res, "template_name")
                self.updated_at = _get(res, "updated_at")
            else:
                self.clusters = []
                self.created_at = None
                self.display_name = None
                self.dns = []
                self.id = None
                self.killswitch = None
                self.name = None
                self.site_status = None
                self.template_id = None
                self.template_name = None
                self.updated_at = None
        else:
            self.clusters = []
            self.created_at = None
            self.display_name = None
            self.dns = []
            self.id = None
            self.killswitch = None
            self.name = None
            self.site_status = None
            self.template_id = None
            self.template_name = None
            self.updated_at = None


# ---------------------------------------------------------------------------
# PUT /api/v2/Site/{id}/static_ips_mapping
# ---------------------------------------------------------------------------


class StaticIpMappingBody(ZscalerObject):
    """Request body for static IP mapping update."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.enabled = _get(config, "enabled")
        else:
            self.enabled = None

    def request_format(self) -> Dict[str, Any]:
        return {"enabled": self.enabled}
