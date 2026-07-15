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
# GET /api/v3/CloudGateway/hubs - Cloud gateway hub list
# ---------------------------------------------------------------------------


class ClusterGatewayInfo(ZscalerObject):
    """Gateway info within cluster_info."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.cloud_gateway_id = _get(config, "cloud_gateway_id")
            self.created_at = _get(config, "created_at")
            self.desired_state = _get(config, "desired_state")
            self.desired_version = _get(config, "desired_version")
            self.display_name = _get(config, "display_name")
            self.gateway_id = _get(config, "gateway_id")
            self.gateway_ip_address = _get(config, "gateway_ip_address")
            self.gateway_name = _get(config, "gateway_name")
            self.health_color = _get(config, "health_color")
            self.operational_state = _get(config, "operational_state")
            self.public_ip_address = _get(config, "public_ip_address")
            self.region = _get(config, "region")
            self.running_version = _get(config, "running_version")
            self.sgw_wireguard_ip = _get(config, "sgw_wireguard_ip")
            self.sgw_wireguard_public_key = _get(config, "sgw_wireguard_public_key")
            self.updated_at = _get(config, "updated_at")
        else:
            self.cloud_gateway_id = None
            self.created_at = None
            self.desired_state = None
            self.desired_version = None
            self.display_name = None
            self.gateway_id = None
            self.gateway_ip_address = None
            self.gateway_name = None
            self.health_color = None
            self.operational_state = None
            self.public_ip_address = None
            self.region = None
            self.running_version = None
            self.sgw_wireguard_ip = None
            self.sgw_wireguard_public_key = None
            self.updated_at = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "cloud_gateway_id": self.cloud_gateway_id,
            "created_at": self.created_at,
            "desired_state": self.desired_state,
            "desired_version": self.desired_version,
            "display_name": self.display_name,
            "gateway_id": self.gateway_id,
            "gateway_ip_address": self.gateway_ip_address,
            "gateway_name": self.gateway_name,
            "health_color": self.health_color,
            "operational_state": self.operational_state,
            "public_ip_address": self.public_ip_address,
            "region": self.region,
            "running_version": self.running_version,
            "sgw_wireguard_ip": self.sgw_wireguard_ip,
            "sgw_wireguard_public_key": self.sgw_wireguard_public_key,
            "updated_at": self.updated_at,
        }


class ClusterInfo(ZscalerObject):
    """Cluster info nested in CloudGatewayHub."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.allowed_commands = _get(config, "allowed_commands")
            self.certificate_profile_id = _get(config, "certificate_profile_id")
            self.cluster_id = _get(config, "cluster_id")
            self.cluster_name = _get(config, "cluster_name")
            self.connect_to_hub = _get(config, "connect_to_hub")
            self.created_at = _get(config, "created_at")
            self.debug_switch = _get(config, "debug_switch")
            self.desired_version = _get(config, "desired_version")
            self.dhcp_options = config.get("dhcpOptions") or config.get("dhcp_options")
            self.dhcp_server_ip = _get(config, "dhcp_server_ip")
            self.dhcp_service = _get(config, "dhcp_service")
            self.gateway_type = _get(config, "gateway_type")
            self.gateways = ZscalerCollection.form_list(config.get("gateways") or [], ClusterGatewayInfo)
            self.nat_enabled = _get(config, "nat_enabled")
            self.per_site_dns = _get(config, "per_site_dns")
            self.syn_ack_target = _get(config, "syn_ack_target")
            self.updated_at = _get(config, "updated_at")
            self.user_reachable_ip = _get(config, "user_reachable_ip")
        else:
            self.allowed_commands = None
            self.certificate_profile_id = None
            self.cluster_id = None
            self.cluster_name = None
            self.connect_to_hub = None
            self.created_at = None
            self.debug_switch = None
            self.desired_version = None
            self.dhcp_options = None
            self.dhcp_server_ip = None
            self.dhcp_service = None
            self.gateway_type = None
            self.gateways = []
            self.nat_enabled = None
            self.per_site_dns = None
            self.syn_ack_target = None
            self.updated_at = None
            self.user_reachable_ip = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "allowed_commands": self.allowed_commands,
            "certificate_profile_id": self.certificate_profile_id,
            "cluster_id": self.cluster_id,
            "cluster_name": self.cluster_name,
            "connect_to_hub": self.connect_to_hub,
            "created_at": self.created_at,
            "debug_switch": self.debug_switch,
            "desired_version": self.desired_version,
            "dhcp_options": self.dhcp_options,
            "dhcp_server_ip": self.dhcp_server_ip,
            "dhcp_service": self.dhcp_service,
            "gateway_type": self.gateway_type,
            "gateways": [g.request_format() for g in (self.gateways or [])],
            "nat_enabled": self.nat_enabled,
            "per_site_dns": self.per_site_dns,
            "syn_ack_target": self.syn_ack_target,
            "updated_at": self.updated_at,
            "user_reachable_ip": self.user_reachable_ip,
        }


class CloudGatewayHub(ZscalerObject):
    """Single hub item from GET /CloudGateway/hubs."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            ci = config.get("clusterInfo") or config.get("cluster_info")
            self.cluster_info = ClusterInfo(ci) if ci else None
            self.created_at = _get(config, "created_at")
            self.location = _get(config, "location")
            self.location_display_name = _get(config, "location_display_name")
            self.public_ip = _get(config, "public_ip")
            self.region = _get(config, "region")
            self.sites = _get(config, "sites")
            self.updated_at = _get(config, "updated_at")
        else:
            self.cluster_info = None
            self.created_at = None
            self.location = None
            self.location_display_name = None
            self.public_ip = None
            self.region = None
            self.sites = None
            self.updated_at = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "cluster_info": self.cluster_info.request_format() if self.cluster_info else None,
            "created_at": self.created_at,
            "location": self.location,
            "location_display_name": self.location_display_name,
            "public_ip": self.public_ip,
            "region": self.region,
            "sites": self.sites,
            "updated_at": self.updated_at,
        }


# ---------------------------------------------------------------------------
# GET/POST/PUT /api/v3/CloudGateway/s2s/{cluster_id} - S2S connection
# ---------------------------------------------------------------------------


class S2SGateway(ZscalerObject):
    """Gateway in S2S connection."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.gateway_id = _get(config, "gateway_id")
            self.gateway_name = _get(config, "gateway_name")
            self.hub_id = _get(config, "hub_id")
            self.id = _get(config, "id")
            self.idx = _get(config, "idx")
            self.interface_id = _get(config, "interface_id")
            self.interface_name = _get(config, "interface_name")
        else:
            self.gateway_id = None
            self.gateway_name = None
            self.hub_id = None
            self.id = None
            self.idx = None
            self.interface_id = None
            self.interface_name = None

    def request_format(self) -> Dict[str, Any]:
        out = {
            "gateway_id": self.gateway_id,
            "gateway_name": self.gateway_name,
            "hub_id": self.hub_id,
            "idx": self.idx,
            "interface_id": self.interface_id,
        }
        if self.id is not None:
            out["id"] = self.id
        if self.interface_name is not None:
            out["interface_name"] = self.interface_name
        return out


class S2SHubs(ZscalerObject):
    """Hubs primary/secondary in S2S connection."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.primary_id = _get(config, "primary_id")
            self.secondary_id = _get(config, "secondary_id")
        else:
            self.primary_id = None
            self.secondary_id = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "primary_id": self.primary_id,
            "secondary_id": self.secondary_id,
        }


class S2SConnection(ZscalerObject):
    """S2S VPN connection for a cluster."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.connect_to_hub = _get(config, "connect_to_hub")
            self.gateways = ZscalerCollection.form_list(config.get("gateways") or [], S2SGateway)
            hubs = config.get("hubs")
            self.hubs = S2SHubs(hubs) if hubs else None
        else:
            self.connect_to_hub = None
            self.gateways = []
            self.hubs = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "connect_to_hub": self.connect_to_hub,
            "gateways": [g.request_format() for g in (self.gateways or [])],
            "hubs": self.hubs.request_format() if self.hubs else None,
        }


# ---------------------------------------------------------------------------
# DELETE /api/v3/CloudGateway/s2s/{cluster_id} - body
# ---------------------------------------------------------------------------


class S2SDeleteRequest(ZscalerObject):
    """Request body for DELETE S2S connections."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.gateway_ids = config.get("gatewayIds") or config.get("gateway_ids") or []
        else:
            self.gateway_ids = []

    def request_format(self) -> Dict[str, Any]:
        return {"gateway_ids": self.gateway_ids}


# ---------------------------------------------------------------------------
# GET /api/v3/CloudGateway/s2s/{cluster_id}/gateways
# ---------------------------------------------------------------------------


class GatewayInterface(ZscalerObject):
    """Interface in gateway with interfaces list."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.interface_name = _get(config, "interface_name") or config.get("interface_Name")
            self.interface_id = _get(config, "interface_id")
            self.interface_type = _get(config, "interface_type")
            self.operational_state = _get(config, "operational_state")
        else:
            self.interface_name = None
            self.interface_id = None
            self.interface_type = None
            self.operational_state = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "interface_name": self.interface_name,
            "interface_id": self.interface_id,
            "interface_type": self.interface_type,
            "operational_state": self.operational_state,
        }


class ClusterGatewayWithInterfaces(ZscalerObject):
    """Gateway with interfaces from GET .../gateways."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.gateway_id = _get(config, "gateway_id")
            self.gateway_name = _get(config, "gateway_name")
            self.gateway_type = _get(config, "gateway_type")
            self.interfaces = ZscalerCollection.form_list(config.get("interfaces") or [], GatewayInterface)
            self.operational_state = _get(config, "operational_state")
        else:
            self.gateway_id = None
            self.gateway_name = None
            self.gateway_type = None
            self.interfaces = []
            self.operational_state = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "gateway_id": self.gateway_id,
            "gateway_name": self.gateway_name,
            "gateway_type": self.gateway_type,
            "interfaces": [i.request_format() for i in (self.interfaces or [])],
            "operational_state": self.operational_state,
        }


# ---------------------------------------------------------------------------
# GET /api/v3/CloudGateway/s2s_hubs
# ---------------------------------------------------------------------------


class S2SHubItem(ZscalerObject):
    """Hub item from GET s2s_hubs."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.hub_cluster_id = _get(config, "hub_cluster_id")
            self.hub_name = _get(config, "hub_name")
            self.public_ip_address = _get(config, "public_ip_address")
            self.region = _get(config, "region")
        else:
            self.hub_cluster_id = None
            self.hub_name = None
            self.public_ip_address = None
            self.region = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "hub_cluster_id": self.hub_cluster_id,
            "hub_name": self.hub_name,
            "public_ip_address": self.public_ip_address,
            "region": self.region,
        }
