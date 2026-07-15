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

from typing import Any, Dict, Optional

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject
from zscaler.zpa.models import app_connectors as app_connectors
from zscaler.zpa.models import server_group as server_group


class AppConnectorGroup(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the AppConnectorGroup model based on API response.

        Args:
            config (dict): A dictionary representing the App Connector Group configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.name = config["name"] if "name" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.description = config["description"] if "description" in config else None
            self.version_profile_id = config["versionProfileId"] if "versionProfileId" in config else None
            self.override_version_profile = config["overrideVersionProfile"] if "overrideVersionProfile" in config else None
            self.version_profile_name = config["versionProfileName"] if "versionProfileName" in config else None
            self.upgrade_priority = config["upgradePriority"] if "upgradePriority" in config else None
            self.version_profile_visibility_scope = (
                config["versionProfileVisibilityScope"] if "versionProfileVisibilityScope" in config else None
            )
            self.upgrade_time_in_secs = config["upgradeTimeInSecs"] if "upgradeTimeInSecs" in config else None
            self.upgrade_day = config["upgradeDay"] if "upgradeDay" in config else None
            self.location = config["location"] if "location" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.dns_query_type = config["dnsQueryType"] if "dnsQueryType" in config else None
            self.city = config["city"] if "city" in config else None
            self.city_country = config["cityCountry"] if "cityCountry" in config else None
            self.connector_group_type = config["connectorGroupType"] if "connectorGroupType" in config else None
            self.country_code = config["countryCode"] if "countryCode" in config else None
            self.geo_location_id = config["geoLocationId"] if "geoLocationId" in config else None
            self.name_without_trim = config["nameWithoutTrim"] if "nameWithoutTrim" in config else None
            self.enrollment_cert_id = config["enrollmentCertId"] if "enrollmentCertId" in config else None
            self.tcp_quick_ack_app = config["tcpQuickAckApp"] if "tcpQuickAckApp" in config else False
            self.tcp_quick_ack_assistant = config["tcpQuickAckAssistant"] if "tcpQuickAckAssistant" in config else False
            self.tcp_quick_ack_read_assistant = (
                config["tcpQuickAckReadAssistant"] if "tcpQuickAckReadAssistant" in config else False
            )
            self.pra_enabled = config["praEnabled"] if "praEnabled" in config else False
            self.use_in_dr_mode = config["useInDrMode"] if "useInDrMode" in config else False
            self.waf_disabled = config["wafDisabled"] if "wafDisabled" in config else False
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.site_id = config["siteId"] if "siteId" in config else None
            self.site_name = config["siteName"] if "siteName" in config else None
            self.private_cloud_id = config["privateCloudId"] if "privateCloudId" in config else None
            self.lss_app_connector_group = config["lssAppConnectorGroup"] if "lssAppConnectorGroup" in config else False
            self.read_only = config["readOnly"] if "readOnly" in config else None
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else None
            self.dc_hosting_info = config["dcHostingInfo"] if "dcHostingInfo" in config else None

            self.ip_acl = ZscalerCollection.form_list(config["ipAcl"] if "ipAcl" in config else [], str)

            self.server_groups = ZscalerCollection.form_list(
                config["serverGroups"] if "serverGroups" in config else [], server_group.ServerGroup
            )
            self.connectors = ZscalerCollection.form_list(
                config["connectors"] if "connectors" in config else [], app_connectors.AppConnectorController
            )
            if "npAssistantGroup" in config:
                if isinstance(config["npAssistantGroup"], NPAssistantGroup):
                    self.np_assistant_group = config["npAssistantGroup"]
                elif config["npAssistantGroup"] is not None:
                    self.np_assistant_group = NPAssistantGroup(config["npAssistantGroup"])
                else:
                    self.np_assistant_group = None
            else:
                self.np_assistant_group = None

            if "version" in config:
                if isinstance(config["version"], app_connectors.ComponentLevelVersion):
                    self.version = config["version"]
                elif config["version"] is not None:
                    self.version = app_connectors.ComponentLevelVersion(config["version"])
                else:
                    self.version = None
            else:
                self.version = None
        else:
            self.id = None
            self.ip_acl = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.enabled = None
            self.description = None
            self.version_profile_id = None
            self.override_version_profile = None
            self.version_profile_name = None
            self.upgrade_priority = None
            self.version_profile_visibility_scope = None
            self.upgrade_time_in_secs = None
            self.upgrade_day = None
            self.location = None
            self.latitude = None
            self.longitude = None
            self.dns_query_type = None
            self.connector_group_type = None
            self.city = None
            self.city_country = None
            self.country_code = None
            self.geo_location_id = None
            self.name_without_trim = None
            self.enrollment_cert_id = None
            self.tcp_quick_ack_app = False
            self.tcp_quick_ack_assistant = False
            self.tcp_quick_ack_read_assistant = False
            self.pra_enabled = False
            self.use_in_dr_mode = False
            self.waf_disabled = False
            self.microtenant_id = None
            self.microtenant_name = None
            self.site_id = None
            self.site_name = None
            self.lss_app_connector_group = None
            self.read_only = None
            self.restriction_type = None
            self.zscaler_managed = None
            self.dc_hosting_info = None
            self.private_cloud_id = None
            self.server_groups = []
            self.connectors = []
            self.np_assistant_group = None
            self.version = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "ipAcl": self.ip_acl,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
            "versionProfileId": self.version_profile_id,
            "overrideVersionProfile": self.override_version_profile,
            "versionProfileName": self.version_profile_name,
            "upgradePriority": self.upgrade_priority,
            "versionProfileVisibilityScope": self.version_profile_visibility_scope,
            "upgradeTimeInSecs": self.upgrade_time_in_secs,
            "upgradeDay": self.upgrade_day,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "dnsQueryType": self.dns_query_type,
            "connectorGroupType": self.connector_group_type,
            "city": self.city,
            "cityCountry": self.city_country,
            "countryCode": self.country_code,
            "geoLocationId": self.geo_location_id,
            "nameWithoutTrim": self.name_without_trim,
            "enrollmentCertId": self.enrollment_cert_id,
            "tcpQuickAckApp": self.tcp_quick_ack_app,
            "tcpQuickAckAssistant": self.tcp_quick_ack_assistant,
            "tcpQuickAckReadAssistant": self.tcp_quick_ack_read_assistant,
            "praEnabled": self.pra_enabled,
            "useInDrMode": self.use_in_dr_mode,
            "wafDisabled": self.waf_disabled,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "siteId": self.site_id,
            "siteName": self.site_name,
            "lssAppConnectorGroup": self.lss_app_connector_group,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "zscalerManaged": self.zscaler_managed,
            "dcHostingInfo": self.dc_hosting_info,
            "privateCloudId": self.private_cloud_id,
            "connectors": self.connectors,
            "serverGroups": [server_group.request_format() for server_group in self.server_groups],
            "npAssistantGroup": self.np_assistant_group,
            "version": self.version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NPAssistantGroup(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the NPAssistantGroup model based on API response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.app_connector_group_id = config["appConnectorGroupId"] if "appConnectorGroupId" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.mtu = config["mtu"] if "mtu" in config else None
            self.np_assistant_count = config["npAssistantCount"] if "npAssistantCount" in config else None
            self.redundant_mode_enabled = config["redundantModeEnabled"] if "redundantModeEnabled" in config else None
            self.is_advertise_lan_segment_locally_disabled = (
                config["isAdvertiseLanSegmentLocallyDisabled"] if "isAdvertiseLanSegmentLocallyDisabled" in config else None
            )
            self.external_routers = ZscalerCollection.form_list(
                config["externalRouters"] if "externalRouters" in config else [], NPExternalRouters
            )
            self.lan_subnets = ZscalerCollection.form_list(config["lanSubnets"] if "lanSubnets" in config else [], LanSubnet)
        else:
            self.id = None
            self.app_connector_group_id = None
            self.creation_time = None
            self.modified_time = None
            self.modified_by = None
            self.mtu = None
            self.np_assistant_count = None
            self.redundant_mode_enabled = None
            self.is_advertise_lan_segment_locally_disabled = None
            self.lan_subnets = []
            self.external_routers = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "appConnectorGroupId": self.app_connector_group_id,
            "creationTime": self.creation_time,
            "modifiedTime": self.modified_time,
            "modifiedBy": self.modified_by,
            "mtu": self.mtu,
            "npAssistantCount": self.np_assistant_count,
            "redundantModeEnabled": self.redundant_mode_enabled,
            "isAdvertiseLanSegmentLocallyDisabled": self.is_advertise_lan_segment_locally_disabled,
            "lanSubnets": [subnet.request_format() for subnet in self.lan_subnets],
            "externalRouters": [router.request_format() for router in (self.external_routers or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LanSubnet(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LanSubnet model based on API response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.name = config["name"] if "name" in config else None
            self.name_without_trim = config["nameWithoutTrim"] if "nameWithoutTrim" in config else None
            self.app_connector_group_id = config["appConnectorGroupId"] if "appConnectorGroupId" in config else None
            self.assistant_group_ids = ZscalerCollection.form_list(
                config["assistantGroupIds"] if "assistantGroupIds" in config else [], str
            )
            self.description = config["description"] if "description" in config else None
            self.subnet = config["subnet"] if "subnet" in config else None
            self.lan_subnets = ZscalerCollection.form_list(config["lanSubnets"] if "lanSubnets" in config else [], str)
            self.old_audit_string = config["oldAuditString"] if "oldAuditString" in config else None
            self.npserver_ips = ZscalerCollection.form_list(config["npserverips"] if "npserverips" in config else [], str)
            self.fqdns = ZscalerCollection.form_list(config["fqdns"] if "fqdns" in config else [], str)
            self.np_dns_ns_record = NPDnsNsRecord(config["npDnsNsRecord"] if "npDnsNsRecord" in config else None)
        else:
            self.id = None
            self.creation_time = None
            self.modified_time = None
            self.modified_by = None
            self.name = None
            self.name_without_trim = None
            self.app_connector_group_id = None
            self.description = None
            self.subnet = None
            self.lan_subnets = []
            self.old_audit_string = None
            self.npserver_ips = []
            self.fqdns = []
            self.assistant_group_ids = []
            self.np_dns_ns_record = NPDnsNsRecord()

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "creationTime": self.creation_time,
            "modifiedTime": self.modified_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "nameWithoutTrim": self.name_without_trim,
            "appConnectorGroupId": self.app_connector_group_id,
            "assistantGroupIds": self.assistant_group_ids,
            "description": self.description,
            "oldAuditString": self.old_audit_string,
            "subnet": self.subnet,
            "lanSubnets": self.lan_subnets,
            "npserverips": self.npserver_ips,
            "fqdns": self.fqdns,
            "npDnsNsRecord": self.np_dns_ns_record.request_format(),
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NPDnsNsRecord(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the NPDnsNsRecord model based on API response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.name = config["name"] if "name" in config else None
            self.name_without_trim = config["nameWithoutTrim"] if "nameWithoutTrim" in config else None
            self.fqdn = ZscalerCollection.form_list(config["fqdn"] if "fqdn" in config else [], str)
            self.nameserver_ips = ZscalerCollection.form_list(
                config["nameserverIps"] if "nameserverIps" in config else [], str
            )

        else:
            self.id = None
            self.creation_time = None
            self.modified_time = None
            self.modified_by = None
            self.name = None
            self.name_without_trim = None
            self.fqdn = []
            self.nameserver_ips = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "creationTime": self.creation_time,
            "modifiedTime": self.modified_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "nameWithoutTrim": self.name_without_trim,
            "fqdn": self.fqdn,
            "nameserverIps": self.nameserver_ips,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NPExternalRouters(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the NP External Routers model based on API response.
        """
        super().__init__(config)
        if config:
            self.bgp_hold_time_interval = config["bgpHoldTimeInterval"] if "bgpHoldTimeInterval" in config else None
            self.bgp_keep_alive_interval = config["bgpKeepAliveInterval"] if "bgpKeepAliveInterval" in config else None
            self.enable_multi_hop = config["enableMultiHop"] if "enableMultiHop" in config else None
            self.external_router_id = config["externalRouterId"] if "externalRouterId" in config else None
            self.external_router_name = config["externalRouterName"] if "externalRouterName" in config else None
            self.source_interface = config["sourceInterface"] if "sourceInterface" in config else None
        else:
            self.bgp_hold_time_interval = None
            self.bgp_keep_alive_interval = None
            self.enable_multi_hop = None
            self.external_router_id = None
            self.external_router_name = None
            self.source_interface = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "bgpHoldTimeInterval": self.bgp_hold_time_interval,
            "bgpKeepAliveInterval": self.bgp_keep_alive_interval,
            "enableMultiHop": self.enable_multi_hop,
            "externalRouterId": self.external_router_id,
            "externalRouterName": self.external_router_name,
            "sourceInterface": self.source_interface,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
