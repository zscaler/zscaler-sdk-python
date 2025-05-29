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
from zscaler.zpa.models import segment_group as segment_group


class ApplicationSegments(ZscalerObject):
    """
    A class representing the Application Segment.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.segment_group_id = config["segmentGroupId"] if "segmentGroupId" in config else None
            self.segment_group_name = config["segmentGroupName"] if "segmentGroupName" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.double_encrypt = config["doubleEncrypt"] if "doubleEncrypt" in config else None
            self.config_space = config["configSpace"] if "configSpace" in config else None
            self.bypass_type = config["bypassType"] if "bypassType" in config else None
            self.health_check_type = config["healthCheckType"] if "healthCheckType" in config else None
            self.icmp_access_type = config["icmpAccessType"] if "icmpAccessType" in config else None
            self.is_cname_enabled = config["isCnameEnabled"] if "isCnameEnabled" in config else None
            self.ip_anchored = config["ipAnchored"] if "ipAnchored" in config else None
            self.bypass_on_reauth = config["bypassOnReauth"] if "bypassOnReauth" in config else None
            self.inspect_traffic_with_zia = config["inspectTrafficWithZia"] if "inspectTrafficWithZia" in config else None
            self.health_reporting = config["healthReporting"] if "healthReporting" in config else None
            self.use_in_dr_mode = config["useInDrMode"] if "useInDrMode" in config else None
            self.tcp_keep_alive = config["tcpKeepAlive"] if "tcpKeepAlive" in config else None
            self.passive_health_enabled = config["passiveHealthEnabled"] \
                if "passiveHealthEnabled" in config else None
            self.select_connector_close_to_app = (
                config["selectConnectorCloseToApp"] if "selectConnectorCloseToApp" in config else None
            )
            self.match_style = config["matchStyle"] if "matchStyle" in config else None
            self.is_incomplete_dr_config = config["isIncompleteDRConfig"] if "isIncompleteDRConfig" in config else None
            self.adp_enabled = config["adpEnabled"] if "adpEnabled" in config else None
            self.auto_app_protect_enabled = config["autoAppProtectEnabled"] if "autoAppProtectEnabled" in config else None
            self.api_protection_enabled = config["apiProtectionEnabled"] if "apiProtectionEnabled" in config else None
            self.fqdn_dns_check = config["fqdnDnsCheck"] if "fqdnDnsCheck" in config else None
            self.weighted_load_balancing = config["weightedLoadBalancing"] if "weightedLoadBalancing" in config else None
            self.extranet_enabled = config["extranetEnabled"] if "extranetEnabled" in config else None
            self.microtenant_name = config["microtenantName"]\
                if "microtenantName" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.read_only = config["readOnly"] if "readOnly" in config else None
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else None

            self.domain_names = ZscalerCollection.form_list(
                config["domainNames"] if "domainNames" in config else [], str
            )

            self.server_groups = []
            if "serverGroups" in config:
                for group in config["serverGroups"]:
                    if isinstance(group, server_group.ServerGroup):
                        self.server_groups.append(group)
                    else:
                        self.server_groups.append(server_group.ServerGroup(group))

            self.pra_apps = ZscalerCollection.form_list(
                config["praApps"] if "praApps" in config else [], PRAApps
            )

            self.inspection_apps = ZscalerCollection.form_list(
                config["inspectionApps"] if "inspectionApps" in config else [], InspectionApps
            )

            self.tcp_port_ranges = ZscalerCollection.form_list(
                config["tcpPortRanges"] if "tcpPortRanges" in config else [], str
            )
            self.udp_port_ranges = ZscalerCollection.form_list(
                config["udpPortRanges"] if "udpPortRanges" in config else [], str
            )

            self.tcp_port_range = []
            if "tcpPortRange" in config:
                for port_range in config["tcpPortRange"]:
                    if isinstance(port_range, dict):
                        self.tcp_port_range.append({"from": port_range.get("from"), "to": port_range.get("to")})

            self.udp_port_range = []
            if "udpPortRange" in config:
                for port_range in config["udpPortRange"]:
                    if isinstance(port_range, dict):
                        self.udp_port_range.append({"from": port_range.get("from"), "to": port_range.get("to")})

            self.inspection_apps = ZscalerCollection.form_list(
                config["clientlessApps"] if "clientlessApps" in config else [], BAAppDto
            )

            if "commonAppsDto" in config:
                if isinstance(config["commonAppsDto"], CommonAppsDto):
                    self.common_apps_dto = config["commonAppsDto"]
                elif config["commonAppsDto"] is not None:
                    self.common_apps_dto = CommonAppsDto(config["commonAppsDto"])
                else:
                    self.common_apps_dto = None
            else:
                self.common_apps_dto = None

            if "sharedMicrotenantDetails" in config:
                if isinstance(config["sharedMicrotenantDetails"], SharedMicrotenantDetails):
                    self.shared_microtenant_details = config["sharedMicrotenantDetails"]
                elif config["sharedMicrotenantDetails"] is not None:
                    self.shared_microtenant_details = SharedMicrotenantDetails(config["sharedMicrotenantDetails"])
                else:
                    self.shared_microtenant_details = None
            else:
                self.shared_microtenant_details = None

            if "zpnErId" in config:
                if isinstance(config["zpnErId"], ZPNExtranetResource):
                    self.zpn_er_id = config["zpnErId"]
                elif config["zpnErId"] is not None:
                    self.zpn_er_id = ZPNExtranetResource(config["zpnErId"])
                else:
                    self.zpn_er_id = None
            else:
                self.zpn_er_id = None

            if "applicationGroup" in config:
                if isinstance(config["applicationGroup"], segment_group.SegmentGroup):
                    self.application_group = config["applicationGroup"]
                elif config["applicationGroup"] is not None:
                    self.application_group = segment_group.SegmentGroup(config["applicationGroup"])
                else:
                    self.application_group = None
            else:
                self.application_group = None
        else:
            self.id = None
            self.name = None
            self.description = None
            self.domain_names = []
            self.server_groups = []
            self.pra_apps = []
            self.common_apps_dto = None
            self.tcp_port_ranges = []
            self.udp_port_ranges = []
            self.tcp_port_range = []
            self.udp_port_range = []
            self.enabled = None
            self.double_encrypt = None
            self.passive_health_enabled = None
            self.config_space = None
            self.bypass_type = None
            self.health_check_type = None
            self.icmp_access_type = None
            self.is_cname_enabled = None
            self.ip_anchored = None
            self.bypass_on_reauth = None
            self.inspect_traffic_with_zia = None
            self.health_reporting = None
            self.use_in_dr_mode = None
            self.tcp_keep_alive = None
            self.select_connector_close_to_app = None
            self.match_style = None
            self.is_incomplete_dr_config = None
            self.adp_enabled = None
            self.auto_app_protect_enabled = None
            self.api_protection_enabled = None
            self.fqdn_dns_check = None
            self.weighted_load_balancing = None
            self.extranet_enabled = None
            self.microtenant_name = None
            self.microtenant_id = None
            self.read_only = None
            self.restriction_type = None
            self.zscaler_managed = None
            self.shared_microtenant_details = None
            self.application_group = None
            self.zpn_er_id = None

    def request_format(self):
        """
        Formats the Application Segment data into a dictionary suitable for API requests.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "domainNames": self.domain_names,
            "serverGroups": self.server_groups,
            "enabled": self.enabled,
            "tcpPortRanges": self.tcp_port_ranges,
            "udpPortRanges": self.udp_port_ranges,
            "tcpPortRange": [{"from": pr["from"], "to": pr["to"]} for pr in self.tcp_port_range],
            "udpPortRange": [{"from": pr["from"], "to": pr["to"]} for pr in self.udp_port_range],
            "doubleEncrypt": self.double_encrypt,
            "configSpace": self.config_space,
            "bypassType": self.bypass_type,
            "healthCheckType": self.health_check_type,
            "passiveHealthEnabled": self.passive_health_enabled,
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
            "microtenantName": self.microtenant_name,
            "microtenantId": self.microtenant_id,
            "segmentGroupId": self.segment_group_id,
            "segmentGroupName": self.segment_group_name,
            "commonAppsDto": self.common_apps_dto,
            "praApps": self.pra_apps,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "zscalerManaged": self.zscaler_managed,
            "sharedMicrotenantDetails": self.shared_microtenant_details,
            "applicationGroup": self.application_group,
            "zpnErId": self.zpn_er_id
        }


class CommonAppsDto(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.deleted_ba_apps = ZscalerCollection.form_list(
                config["deletedBaApps"] if "deletedBaApps" in config else [], str
            )
            self.deleted_pra_apps = ZscalerCollection.form_list(
                config["deletedPraApps"] if "deletedPraApps" in config else [], str
            )
            self.deleted_inspect_apps = ZscalerCollection.form_list(
                config["deletedInspectApps"] if "deletedInspectApps" in config else [], str
            )
            self.apps_config = ZscalerCollection.form_list(
                config["appsConfig"] if "appsConfig" in config else [], AppsConfig
            )
        else:
            self.apps_config = []
            self.deleted_ba_apps = []
            self.deleted_inspect_apps = []
            self.deleted_pra_apps = []

    def request_format(self):
        """
        Formats the AppConfig data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "appsConfig": self.apps_config,
            "deletedBaApps": self.deleted_ba_apps,
            "deletedInspectApps": self.deleted_inspect_apps,
            "deletedPraApps": self.deleted_pra_apps,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppsConfig(ZscalerObject):
    """
    A class for Appsconfig objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Appsconfig model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.adp_enabled = config["adpEnabled"] \
                if "adpEnabled" in config else None
            self.allow_options = config["allowOptions"] \
                if "allowOptions" in config else None
            self.app_id = config["appId"] \
                if "appId" in config else None
            self.app_types = ZscalerCollection.form_list(
                config["appTypes"] if "appTypes" in config else [], str
            )
            self.application_port = config["applicationPort"] \
                if "applicationPort" in config else None
            self.application_protocol = config["applicationProtocol"] \
                if "applicationProtocol" in config else None
            self.ba_app_id = config["baAppId"] \
                if "baAppId" in config else None
            self.certificate_id = config["certificateId"] \
                if "certificateId" in config else None
            self.certificate_name = config["certificateName"] \
                if "certificateName" in config else None
            self.cname = config["cname"] \
                if "cname" in config else None
            self.connection_security = config["connectionSecurity"] \
                if "connectionSecurity" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.domain = config["domain"] \
                if "domain" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.ext_domain = config["extDomain"] \
                if "extDomain" in config else None
            self.ext_id = config["extId"] \
                if "extId" in config else None
            self.ext_label = config["extLabel"] \
                if "extLabel" in config else None
            self.hidden = config["hidden"] \
                if "hidden" in config else None
            self.inspect_app_id = config["inspectAppId"] \
                if "inspectAppId" in config else None
            self.local_domain = config["localDomain"] \
                if "localDomain" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.path = config["path"] \
                if "path" in config else None
            self.portal = config["portal"] \
                if "portal" in config else None
            self.pra_app_id = config["praAppId"] \
                if "praAppId" in config else None
            self.protocols = ZscalerCollection.form_list(
                config["protocols"] if "protocols" in config else [], str
            )
            self.trust_untrusted_cert = config["trustUntrustedCert"] \
                if "trustUntrustedCert" in config else None
        else:
            self.adp_enabled = None
            self.allow_options = None
            self.app_id = None
            self.app_types = ZscalerCollection.form_list([], str)
            self.application_port = None
            self.application_protocol = None
            self.ba_app_id = None
            self.certificate_id = None
            self.certificate_name = None
            self.cname = None
            self.connection_security = None
            self.description = None
            self.domain = None
            self.enabled = None
            self.ext_domain = None
            self.ext_id = None
            self.ext_label = None
            self.hidden = None
            self.inspect_app_id = None
            self.local_domain = None
            self.name = None
            self.path = None
            self.portal = None
            self.pra_app_id = None
            self.protocols = ZscalerCollection.form_list([], str)
            self.trust_untrusted_cert = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "adpEnabled": self.adp_enabled,
            "allowOptions": self.allow_options,
            "appId": self.app_id,
            "appTypes": self.app_types,
            "applicationPort": self.application_port,
            "applicationProtocol": self.application_protocol,
            "baAppId": self.ba_app_id,
            "certificateId": self.certificate_id,
            "certificateName": self.certificate_name,
            "cname": self.cname,
            "connectionSecurity": self.connection_security,
            "description": self.description,
            "domain": self.domain,
            "enabled": self.enabled,
            "extDomain": self.ext_domain,
            "extId": self.ext_id,
            "extLabel": self.ext_label,
            "hidden": self.hidden,
            "inspectAppId": self.inspect_app_id,
            "localDomain": self.local_domain,
            "name": self.name,
            "path": self.path,
            "portal": self.portal,
            "praAppId": self.pra_app_id,
            "protocols": self.protocols,
            "trustUntrustedCert": self.trust_untrusted_cert
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class InspectionApps(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.app_id = config["appId"] if "appId" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.domain = config["domain"] if "domain" in config else None
            self.application_protocol = config["applicationProtocol"] if "applicationProtocol" in config else None
            self.application_port = config["applicationPort"] if "applicationPort" in config else None
            self.protocols = config["protocols"] if "protocols" in config else None
            self.certificate_id = config["certificateId"] if "certificateId" in config else None
            self.certificate_name = config["certificateName"] if "certificateName" in config else None
            self.trust_untrusted_cert = config["trustUntrustedCert	"] if "trustUntrustedCert	" in config else None
            self.microtenant_name = config["microtenantName"]\
                if "microtenantName" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None

        else:
            self.id = None
            self.app_id = None
            self.name = None
            self.description = None
            self.enabled = None
            self.domain = None
            self.application_protocol = None
            self.application_port = None
            self.protocols = None
            self.certificate_id = None
            self.certificate_name = None
            self.trust_untrusted_cert = None
            self.microtenant_name = None
            self.microtenant_id = None

    def request_format(self):
        """
        Formats the AppConfig data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "appId": self.app_id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "domain": self.domain,
            "applicationProtocol": self.application_protocol,
            "applicationPort": self.application_port,
            "protocols": self.protocols,
            "certificateId": self.certificate_id,
            "certificateName": self.certificate_name,
            "microtenantName": self.microtenant_name,
            "microtenantId": self.microtenant_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PRAApps(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.app_id = config["appId"] if "appId" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.domain = config["domain"] if "domain" in config else None
            self.application_protocol = config["applicationProtocol"] if "applicationProtocol" in config else None
            self.application_port = config["applicationPort"] if "applicationPort" in config else None
            self.connection_security = config["connectionSecurity"] if "connectionSecurity" in config else None
            self.certificate_id = config["certificateId"] if "certificateId" in config else None
            self.certificate_name = config["certificateName"] if "certificateName" in config else None
            self.hidden = config["hidden"] if "hidden" in config else None
            self.microtenant_name = config["microtenantName"]\
                if "microtenantName" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None

        else:
            self.id = None
            self.app_id = None
            self.name = None
            self.description = None
            self.enabled = None
            self.domain = None
            self.application_protocol = None
            self.application_port = None
            self.connection_security = None
            self.certificate_id = None
            self.certificate_name = None
            self.hidden = None
            self.microtenant_name = None
            self.microtenant_id = None

    def request_format(self):
        """
        Formats the AppConfig data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "appId": self.app_id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "domain": self.domain,
            "applicationProtocol": self.application_protocol,
            "applicationPort": self.application_port,
            "connectionSecurity": self.connection_security,
            "certificateId": self.certificate_id,
            "certificateName": self.certificate_name,
            "hidden": self.hidden,
            "microtenantName": self.microtenant_name,
            "microtenantId": self.microtenant_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SharedMicrotenantDetails(ZscalerObject):
    """
    A class for SharedMicrotenantDetails objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SharedMicrotenantDetails model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            if "sharedFromMicrotenant" in config:
                if isinstance(config["sharedFromMicrotenant"], SharedFromMicrotenant):
                    self.shared_from_microtenant = config["sharedFromMicrotenant"]
                elif config["sharedFromMicrotenant"] is not None:
                    self.shared_from_microtenant = SharedFromMicrotenant(config["sharedFromMicrotenant"])
                else:
                    self.shared_from_microtenant = None
            else:
                self.shared_from_microtenant = None

            if "sharedToMicrotenants" in config:
                if isinstance(config["sharedToMicrotenants"], SharedToMicrotenants):
                    self.shared_to_microtenant = config["sharedToMicrotenants"]
                elif config["sharedToMicrotenants"] is not None:
                    self.shared_to_microtenant = SharedToMicrotenants(config["sharedToMicrotenants"])
                else:
                    self.shared_to_microtenant = None
            else:
                self.shared_to_microtenant = None

        else:
            self.shared_from_microtenant = None
            self.shared_to_microtenant = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "sharedFromMicrotenant": self.shared_from_microtenant,
            "sharedToMicrotenants": self.shared_to_microtenant,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SharedFromMicrotenant(ZscalerObject):
    """
    A class for SharedFromMicrotenant objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SharedFromMicrotenant model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None

        else:
            self.id = None
            self.name = None

    def request_format(self):
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


class SharedToMicrotenants(ZscalerObject):
    """
    A class for SharedToMicrotenants objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SharedToMicrotenants model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None

        else:
            self.id = None
            self.name = None

    def request_format(self):
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


class ZPNExtranetResource(ZscalerObject):
    """
    A class for ZPNExtranetResource objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the ZPNExtranetResource model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.zia_cloud = config["ziaCloud"] if "ziaCloud" in config else None
            self.zia_er_id = config["ziaErId"] if "ziaErId" in config else None
            self.zia_er_name = config["ziaErName"] if "ziaErName" in config else None
            self.zia_modified_time = config["ziaModifiedTime"] if "ziaModifiedTime" in config else None
            self.zia_org_id = config["ziaOrgId"] if "ziaOrgId" in config else None

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.zia_cloud = None
            self.zia_er_id = None
            self.zia_er_name = None
            self.zia_modified_time = None
            self.zia_org_id = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "ziaCloud": self.zia_cloud,
            "ziaErId": self.zia_er_id,
            "ziaErName": self.zia_er_name,
            "ziaModifiedTime": self.zia_modified_time,
            "ziaOrgId": self.zia_org_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class BAAppDto(ZscalerObject):
    """
    A class for Clientless Application Segment Entity objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.app_id = config["appId"] if "appId" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.certificate_id = config["certificateId"] if "certificateId" in config else None
            self.certificate_name = config["certificateName"] if "certificateName" in config else None
            self.application_port = config["applicationPort"] if "applicationPort" in config else None
            self.application_protocol = config["applicationProtocol"] if "applicationProtocol" in config else None
            self.domain = config["domain"] if "domain" in config else None
            self.hidden = config["hidden"] if "hidden" in config else None
            self.local_domain = config["localDomain"] if "localDomain" in config else None
            self.portal = config["portal"] if "portal" in config else None
            self.trust_untrusted_cert = config["trustUntrustedCert"] if "trustUntrustedCert" in config else None
            self.allow_options = config["allowOptions"] if "allowOptions" in config else None
            self.cname = config["cname"] if "cname" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.ext_domain = config["extDomain"] if "extDomain" in config else None
            self.ext_domain_name = config["extDomainName"] if "extDomainName" in config else None
            self.ext_label = config["extLabel"] if "extLabel" in config else None

            if "appResource" in config:
                if isinstance(config["appResource"], AppResource):
                    self.app_resource = config["appResource"]
                elif config["appResource"] is not None:
                    self.app_resource = AppResource(config["appResource"])
                else:
                    self.app_resource = None
            else:
                self.app_resource = None
        else:
            self.id = None
            self.app_id = None
            self.app_resource = None
            self.name = None
            self.description = None
            self.enabled = None
            self.certificate_id = None
            self.certificate_name = None
            self.application_port = None
            self.application_protocol = None
            self.domain = None
            self.hidden = None
            self.local_domain = None
            self.portal = None
            self.trust_untrusted_cert = None
            self.allow_options = None
            self.cname = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.ext_domain = None
            self.ext_domain_name = None
            self.ext_label = None

    def request_format(self):
        """
        Return a dictionary representing this object for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "appId": self.app_id,
            "appResource": self.app_resource,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "certificateId": self.certificate_id,
            "certificateName": self.certificate_name,
            "applicationPort": self.application_port,
            "applicationProtocol": self.application_protocol,
            "domain": self.domain,
            "hidden": self.hidden,
            "localDomain": self.local_domain,
            "portal": self.portal,
            "trustUntrustedCert": self.trust_untrusted_cert,
            "allowOptions": self.allow_options,
            "cname": self.cname,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "extDomain": self.ext_domain,
            "extDomainName	": self.ext_domain_name,
            "extLabel	": self.ext_label,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppResource(ZscalerObject):
    """
    A class for AppResource objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AppResource model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.app_recommendation_id = config["appRecommendationId"] \
                if "appRecommendationId" in config else None
            self.segment_group_id = config["segmentGroupId"] \
                if "segmentGroupId" in config else None
            self.segment_group_name = config["segmentGroupName"] \
                if "segmentGroupName" in config else None
            self.bypass_type = config["bypassType"] \
                if "bypassType" in config else None
            self.config_space = config["configSpace"] \
                if "configSpace" in config else None
            self.default_idle_timeout = config["defaultIdleTimeout"] \
                if "defaultIdleTimeout" in config else None
            self.default_max_age = config["defaultMaxAge"] \
                if "defaultMaxAge" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.domain_names = ZscalerCollection.form_list(
                config["domainNames"] if "domainNames" in config else [], str
            )
            self.double_encrypt = config["doubleEncrypt"] \
                if "doubleEncrypt" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.fqdn_dns_check = config["fqdnDnsCheck"] \
                if "fqdnDnsCheck" in config else None
            self.health_check_type = config["healthCheckType"] \
                if "healthCheckType" in config else None
            self.health_reporting = config["healthReporting"] \
                if "healthReporting" in config else None
            self.icmp_access_type = config["icmpAccessType"] \
                if "icmpAccessType" in config else None
            self.ip_anchored = config["ipAnchored"] \
                if "ipAnchored" in config else None
            self.is_cname_enabled = config["isCnameEnabled"] \
                if "isCnameEnabled" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.passive_health_enabled = config["passiveHealthEnabled"] \
                if "passiveHealthEnabled" in config else None
            self.read_only = config["readOnly"] \
                if "readOnly" in config else None
            self.restriction_type = config["restrictionType"] \
                if "restrictionType" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] \
                if "microtenantName" in config else None
            self.select_connector_close_to_app = config["selectConnectorCloseToApp"] \
                if "selectConnectorCloseToApp" in config else None
            self.zscaler_managed = config["zscalerManaged"] \
                if "zscalerManaged" in config else None

            self.server_groups = []
            if "serverGroups" in config:
                for group in config["serverGroups"]:
                    if isinstance(group, server_group.ServerGroup):
                        self.server_groups.append(group)
                    else:
                        self.server_groups.append(server_group.ServerGroup(group))

            self.tcp_keep_alive = config["tcpKeepAlive"] \
                if "tcpKeepAlive" in config else None

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

            self.tcp_port_ranges = ZscalerCollection.form_list(
                config["tcpPortRanges"] if "tcpPortRanges" in config else [], str
            )
            self.udp_port_ranges = ZscalerCollection.form_list(
                config["udpPortRanges"] if "udpPortRanges" in config else [], str
            )

            if "sharedMicrotenantDetails" in config:
                if isinstance(config["sharedMicrotenantDetails"], SharedMicrotenantDetails):
                    self.shared_microtenant_details = config["sharedMicrotenantDetails"]
                elif config["sharedMicrotenantDetails"] is not None:
                    self.shared_microtenant_details = SharedMicrotenantDetails(config["sharedMicrotenantDetails"])
                else:
                    self.shared_microtenant_details = None
            else:
                self.shared_microtenant_details = None
        else:
            self.app_recommendation_id = None
            self.segment_group_id = None
            self.segment_group_name = None
            self.bypass_type = None
            self.config_space = None
            self.default_idle_timeout = None
            self.default_max_age = None
            self.description = None
            self.domain_names = []
            self.double_encrypt = None
            self.enabled = None
            self.fqdn_dns_check = None
            self.health_check_type = None
            self.health_reporting = None
            self.icmp_access_type = None
            self.inconsistent_config_details = None
            self.ip_anchored = None
            self.is_cname_enabled = None
            self.name = None
            self.passive_health_enabled = None
            self.read_only = None
            self.restriction_type = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.select_connector_close_to_app = None
            self.server_groups = []
            self.shared_microtenant_details = None
            self.tcp_keep_alive = None
            self.tcp_port_ranges = []
            self.udp_port_ranges = []
            self.tcp_port_range = []
            self.udp_port_range = []
            self.zscaler_managed = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "appRecommendationId": self.app_recommendation_id,
            "segmentGroupId": self.segment_group_id,
            "segmentGroupName": self.segment_group_name,
            "bypassType": self.bypass_type,
            "configSpace": self.config_space,
            "defaultIdleTimeout": self.default_idle_timeout,
            "defaultMaxAge": self.default_max_age,
            "description": self.description,
            "domainNames": self.domain_names,
            "doubleEncrypt": self.double_encrypt,
            "enabled": self.enabled,
            "fqdnDnsCheck": self.fqdn_dns_check,
            "healthCheckType": self.health_check_type,
            "healthReporting": self.health_reporting,
            "icmpAccessType": self.icmp_access_type,
            "inconsistentConfigDetails": self.inconsistent_config_details,
            "ipAnchored": self.ip_anchored,
            "isCnameEnabled": self.is_cname_enabled,
            "name": self.name,
            "passiveHealthEnabled": self.passive_health_enabled,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "selectConnectorCloseToApp": self.select_connector_close_to_app,
            "serverGroups": self.server_groups,
            "sharedMicrotenantDetails": self.shared_microtenant_details,
            "tcpKeepAlive": self.tcp_keep_alive,
            "tcpPortRanges": self.tcp_port_ranges,
            "udpPortRanges": self.udp_port_ranges,
            "tcpPortRange": [{"from": pr["from"], "to": pr["to"]} for pr in self.tcp_port_range],
            "udpPortRange": [{"from": pr["from"], "to": pr["to"]} for pr in self.udp_port_range],
            "zscalerManaged": self.zscaler_managed
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppSegmentByType(ZscalerObject):
    """
    A class for AppSegmentByType objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AppSegmentByType model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.application_port = config["applicationPort"] if "applicationPort" in config else None
            self.application_protocol = config["applicationProtocol"] if "applicationProtocol" in config else None
            self.domain = config["domain"] if "domain" in config else None
            self.app_id = config["appId"] if "appId" in config else None
            self.hidden = config["hidden"] if "hidden" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None

            if "appResource" in config:
                if isinstance(config["appResource"], AppResource):
                    self.app_resource = config["appResource"]
                elif config["appResource"] is not None:
                    self.app_resource = AppResource(config["appResource"])
                else:
                    self.app_resource = None
            else:
                self.app_resource = None

        else:
            self.id = None
            self.name = None
            self.enabled = None
            self.application_port = None
            self.application_protocol = None
            self.domain = None
            self.app_id = None
            self.hidden = None
            self.microtenant_name = None
            self.app_resource = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
            "applicationPort": self.application_port,
            "applicationProtocol": self.application_protocol,
            "domain": self.domain,
            "appId": self.app_id,
            "hidden": self.hidden,
            "microtenantName": self.microtenant_name,
            "appResource": self.app_resource,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
