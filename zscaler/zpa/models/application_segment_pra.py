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
from zscaler.zpa.models import server_group as server_group


class ApplicationSegmentPRA(ZscalerObject):
    """
    A class representing the Application Segment in ZPA for PRA (Privileged Remote Access).
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.domain_names = config["domainNames"] if "domainNames" in config else []
            self.segment_group_id = config["segmentGroupId"] if "segmentGroupId" in config else None
            self.segment_group_name = config["segmentGroupName"] if "segmentGroupName" in config else None
            self.tcp_port_ranges = ZscalerCollection.form_list(
                config["tcpPortRanges"] if "tcpPortRanges" in config else [], str
            )
            self.udp_port_ranges = ZscalerCollection.form_list(
                config["udpPortRanges"] if "udpPortRanges" in config else [], str
            )
            self.enabled = config["enabled"] if "enabled" in config else True
            self.double_encrypt = config["doubleEncrypt"] if "doubleEncrypt" in config else False
            self.config_space = config["configSpace"] if "configSpace" in config else "DEFAULT"
            self.bypass_type = config["bypassType"] if "bypassType" in config else "NEVER"
            self.health_check_type = config["healthCheckType"] if "healthCheckType" in config else "NONE"
            self.icmp_access_type = config["icmpAccessType"] if "icmpAccessType" in config else "NONE"
            self.is_cname_enabled = config["isCnameEnabled"] if "isCnameEnabled" in config else False
            self.ip_anchored = config["ipAnchored"] if "ipAnchored" in config else False
            self.bypass_on_reauth = config["bypassOnReauth"] if "bypassOnReauth" in config else False
            self.inspect_traffic_with_zia = config["inspectTrafficWithZia"] if "inspectTrafficWithZia" in config else False
            self.health_reporting = config["healthReporting"] if "healthReporting" in config else "NONE"
            self.use_in_dr_mode = config["useInDrMode"] if "useInDrMode" in config else False
            self.tcp_keep_alive = config["tcpKeepAlive"] if "tcpKeepAlive" in config else "0"
            self.select_connector_close_to_app = (
                config["selectConnectorCloseToApp"] if "selectConnectorCloseToApp" in config else False
            )
            self.match_style = config["matchStyle"] if "matchStyle" in config else "EXCLUSIVE"
            self.is_incomplete_dr_config = config["isIncompleteDRConfig"] if "isIncompleteDRConfig" in config else False
            self.adp_enabled = config["adpEnabled"] if "adpEnabled" in config else False
            self.auto_app_protect_enabled = config["autoAppProtectEnabled"] if "autoAppProtectEnabled" in config else False
            self.api_protection_enabled = config["apiProtectionEnabled"] if "apiProtectionEnabled" in config else False
            self.fqdn_dns_check = config["fqdnDnsCheck"] if "fqdnDnsCheck" in config else False
            self.weighted_load_balancing = config["weightedLoadBalancing"] if "weightedLoadBalancing" in config else False
            self.extranet_enabled = config["extranetEnabled"] if "extranetEnabled" in config else False
            # self.microtenant_name = config["microtenantName"]\
            #     if "microtenantName" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None

            # Handle serverGroups using defensive programming
            self.server_groups = []
            if "serverGroups" in config:
                for group in config["serverGroups"]:
                    if isinstance(group, server_group.ServerGroup):
                        self.server_groups.append(group)
                    else:
                        self.server_groups.append(server_group.ServerGroup(group))

            # Handle PRA applications (commonAppsDto)
            self.common_apps_dto = config.get("commonAppsDto", {})
            if "appsConfig" in self.common_apps_dto:
                self.common_apps_dto["appsConfig"] = ZscalerCollection.form_list(self.common_apps_dto["appsConfig"], AppConfig)
            self.pra_apps = config["praApps"] if "praApps" in config else []

            # Handle tcpPortRange using conditionals for defensive programming
            self.tcp_port_range = []
            if "tcpPortRange" in config:
                for port_range in config["tcpPortRange"]:
                    if isinstance(port_range, dict):
                        self.tcp_port_range.append({"from": port_range.get("from"), "to": port_range.get("to")})

            self.udp_port_range = []
            if "udpPortRange" in config:
                for port_range in config["udpPortRange"]:
                    if isinstance(port_range, dict):
                        self.tcp_port_range.append({"from": port_range.get("from"), "to": port_range.get("to")})
        else:
            self.id = None
            self.name = None
            self.domain_names = []
            self.server_groups = []
            self.pra_apps = []
            self.common_apps_dto = {}
            self.tcp_port_ranges = []
            self.udp_port_ranges = []
            self.tcp_port_range = []
            self.udp_port_range = []
            self.enabled = True
            self.double_encrypt = False
            self.config_space = "DEFAULT"
            self.bypass_type = "NEVER"
            self.health_check_type = "NONE"
            self.icmp_access_type = "NONE"
            self.is_cname_enabled = False
            self.ip_anchored = False
            self.bypass_on_reauth = False
            self.inspect_traffic_with_zia = False
            self.health_reporting = "NONE"
            self.use_in_dr_mode = False
            self.tcp_keep_alive = "0"
            self.select_connector_close_to_app = False
            self.match_style = "EXCLUSIVE"
            self.is_incomplete_dr_config = False
            self.adp_enabled = False
            self.auto_app_protect_enabled = False
            self.api_protection_enabled = False
            self.fqdn_dns_check = False
            self.weighted_load_balancing = False
            self.extranet_enabled = False
            # self.microtenant_name = None
            self.microtenant_id = None

    def request_format(self):
        """
        Formats the Application Segment data into a dictionary suitable for API requests.
        """
        return {
            "id": self.id,
            "name": self.name,
            "domainNames": self.domain_names,
            "serverGroups": [group.request_format() for group in self.server_groups],
            "enabled": self.enabled,
            "tcpPortRanges": self.tcp_port_ranges,
            "udpPortRanges": self.udp_port_ranges,
            "tcpPortRange": [{"from": pr["from"], "to": pr["to"]} for pr in self.tcp_port_range],
            "udpPortRange": [{"from": pr["from"], "to": pr["to"]} for pr in self.udp_port_range],
            "doubleEncrypt": self.double_encrypt,
            "configSpace": self.config_space,
            "bypassType": self.bypass_type,
            "healthCheckType": self.health_check_type,
            "icmpAccessType": self.icmp_access_type,
            "isCnameEnabled": self.is_cname_enabled,
            "ipAnchored": self.ip_anchored,
            "bypassOnReauth": self.bypass_on_reauth,
            "inspectTrafficWithZia": self.inspect_traffic_with_zia,
            "healthReporting": self.health_reporting,
            "useInDrMode": self.use_in_dr_mode,
            "tcpKeepAlive": self.tcp_keep_alive,
            "selectConnectorCloseToApp": self.select_connector_close_to_app,
            "matchStyle": self.match_style,
            "isIncompleteDRConfig": self.is_incomplete_dr_config,
            "adpEnabled": self.adp_enabled,
            "autoAppProtectEnabled": self.auto_app_protect_enabled,
            "apiProtectionEnabled": self.api_protection_enabled,
            "fqdnDnsCheck": self.fqdn_dns_check,
            "weightedLoadBalancing": self.weighted_load_balancing,
            "extranetEnabled": self.extranet_enabled,
            # "microtenantName": self.microtenant_name,
            "microtenantId": self.microtenant_id,
            "segmentGroupId": self.segment_group_id,
            "segmentGroupName": self.segment_group_name,
            "commonAppsDto": self.common_apps_dto,
            "praApps": self.pra_apps,
        }


class AppConfig(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.app_types = config["appTypes"] if "appTypes" in config else []
            self.application_port = config["applicationPort"] if "applicationPort" in config else None
            self.application_protocol = config["applicationProtocol"] if "applicationProtocol" in config else None
            self.connection_security = config["connectionSecurity"] if "connectionSecurity" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.domain = config["domain"] if "domain" in config else None
            self.name = config["name"] if "name" in config else None
        else:
            self.app_types = []
            self.application_port = None
            self.application_protocol = None
            self.connection_security = None
            self.enabled = True
            self.domain = None
            self.name = None

    def request_format(self):
        """
        Formats the AppConfig data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "appTypes": self.app_types,
            "applicationPort": self.application_port,
            "applicationProtocol": self.application_protocol,
            "connectionSecurity": self.connection_security,
            "enabled": self.enabled,
            "domain": self.domain,
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
