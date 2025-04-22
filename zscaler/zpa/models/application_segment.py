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
from zscaler.zpa.models import common as common


class ApplicationSegment(ZscalerObject):
    """
    A class representing the Application Segment in Zscaler.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.domain_names = config["domainNames"] if "domainNames" in config else []
            self.enabled = config["enabled"] if "enabled" in config else True
            self.passive_health_enabled = config["passiveHealthEnabled"] if "passiveHealthEnabled" in config else False
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
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else "Default"
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.segment_group_id = config["segmentGroupId"] if "segmentGroupId" in config else None
            self.segment_group_name = config["segmentGroupName"] if "segmentGroupName" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None

            self.tcp_protocols = ZscalerCollection.form_list(config["tcpProtocols"] if "tcpProtocols" in config else [], str)

            self.udp_protocols = ZscalerCollection.form_list(config["udpProtocols"] if "udpProtocols" in config else [], str)

            self.server_groups = ZscalerCollection.form_list(config.get("serverGroups", []), server_group.ServerGroup)

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
                        self.tcp_port_range.append({"from": port_range.get("from"), "to": port_range.get("to")})

            self.clientless_apps = (
                ZscalerCollection.form_list(config["clientlessApps"], AppSegmentClientlessApps)
                if "clientlessApps" in config
                else []
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

            if "zpnErId	" in config:
                if isinstance(config["zpnErId	"], ZPNExtranetResource):
                    self.zpn_er_id = config["zpnErId	"]
                elif config["zpnErId	"] is not None:
                    self.zpn_er_id = ZPNExtranetResource(config["zpnErId	"])
                else:
                    self.zpn_er_id = None
            else:
                self.zpn_er_id = None

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.description = None
            self.domain_names = []
            self.server_groups = []
            self.clientless_apps = []
            self.enabled = True
            self.tcp_port_ranges = []
            self.udp_port_ranges = []
            self.tcp_port_range = []
            self.udp_port_range = []
            self.tcp_protocols = []
            self.udp_protocols = []
            self.double_encrypt = False
            self.config_space = None
            self.bypass_type = None
            self.health_check_type = None
            self.icmp_access_type = None
            self.is_cname_enabled = False
            self.ip_anchored = False
            self.bypass_on_reauth = False
            self.inspect_traffic_with_zia = False
            self.health_reporting = None
            self.use_in_dr_mode = False
            self.passive_health_enabled = False
            self.tcp_keep_alive = None
            self.select_connector_close_to_app = False
            self.match_style = None
            self.is_incomplete_dr_config = False
            self.adp_enabled = False
            self.auto_app_protect_enabled = False
            self.api_protection_enabled = False
            self.fqdn_dns_check = False
            self.weighted_load_balancing = False
            self.extranet_enabled = False
            self.microtenant_name = None
            self.microtenant_id = None
            self.segment_group_id = None
            self.segment_group_name = None
            self.zpn_er_id = None

    def request_format(self):
        """
        Formats the Application Segment data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "description": self.description,
            "domainNames": self.domain_names,
            "serverGroups": [group.request_format() for group in self.server_groups],
            "clientlessApps": [clientless.request_format() for clientless in self.clientless_apps],
            "enabled": self.enabled,
            "tcpPortRanges": self.tcp_port_ranges,
            "udpPortRanges": self.udp_port_ranges,
            "tcpPortRange": [{"from": pr["from"], "to": pr["to"]} for pr in self.tcp_port_range],
            "udpPortRange": [{"from": pr["from"], "to": pr["to"]} for pr in self.udp_port_range],
            "tcpProtocols": self.tcp_protocols,
            "udpProtocols": self.udp_protocols,
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
            "passiveHealthEnabled": self.passive_health_enabled,
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
            "zpnErId	": self.zpn_er_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppSegmentClientlessApps(ZscalerObject):
    """
    A class for Clientless Application Segment Entity objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.certificate_id = config["certificateId"] if "certificateId" in config else None
            self.certificate_name = config["certificateName"] if "certificateName" in config else None
            self.application_port = config["applicationPort"] if "applicationPort" in config else None
            self.application_protocol = config["applicationProtocol"] if "applicationProtocol" in config else None
            self.domain = config["domain"] if "domain" in config else None
            self.app_id = config["appId"] if "appId" in config else None
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

        else:
            self.id = None
            self.name = None
            self.description = None
            self.enabled = None
            self.certificate_id = None
            self.certificate_name = None
            self.application_port = None
            self.application_protocol = None
            self.domain = None
            self.app_id = None
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
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "certificateId": self.certificate_id,
            "certificateName": self.certificate_name,
            "applicationPort": self.application_port,
            "applicationProtocol": self.application_protocol,
            "domain": self.domain,
            "appId": self.app_id,
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


class AppResource(ZscalerObject):
    """
    A class for AppResource objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the AppResource model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            if "appResource" in config:
                if isinstance(config["appResource"], ApplicationSegment):
                    self.app_resource = config["appResource"]
                elif config["appResource"] is not None:
                    self.app_resource = ApplicationSegment(config["appResource"])
                else:
                    self.app_resource = None
            else:
                self.app_resource = None

        else:
            self.app_resource = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "appResource": self.app_resource,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
