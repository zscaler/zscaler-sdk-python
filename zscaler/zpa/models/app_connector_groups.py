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
from zscaler.zpa.models import app_connector_groups as app_connector_groups
from zscaler.zpa.models import common as common


class AppConnectorGroup(ZscalerObject):
    """
    A class representing a AppConnectorGroup object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.connectors = ZscalerCollection.form_list(config["connectors"] if "connectors" in config else [], Connector)
            self.city = config["city"] if "city" in config else None
            self.city_country = config["cityCountry"] if "cityCountry" in config else None
            self.connector_group_type = config["connectorGroupType"] if "connectorGroupType" in config else None
            self.country_code = config["countryCode"] if "countryCode" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.dc_hosting_info = config["dcHostingInfo"] if "dcHostingInfo" in config else None
            self.description = config["description"] if "description" in config else None
            self.dns_query_type = config["dnsQueryType"] if "dnsQueryType" in config else None
            self.enabled = config["enabled"] if "enabled" in config else False
            self.geo_location_id = config["geoLocationId"] if "geoLocationId" in config else None
            self.id = config["id"] if "id" in config else None
            self.ip_acl = ZscalerCollection.form_list(config["ipAcl"] if "ipAcl" in config else [], str)
            self.latitude = config["latitude"] if "latitude" in config else None
            self.location = config["location"] if "location" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.name_without_trim = config["nameWithoutTrim"] if "nameWithoutTrim" in config else None
            if "npAssistantGroup" in config:
                if isinstance(config["npAssistantGroup"], app_connector_groups.NPAssistantGroup):
                    self.np_assistant_group = config["npAssistantGroup"]
                elif config["npAssistantGroup"] is not None:
                    self.np_assistant_group = app_connector_groups.NPAssistantGroup(config["npAssistantGroup"])
                else:
                    self.np_assistant_group = None
            else:
                self.np_assistant_group = None
            self.override_version_profile = config["overrideVersionProfile"] if "overrideVersionProfile" in config else False
            self.pra_enabled = config["praEnabled"] if "praEnabled" in config else False
            self.read_only = config["readOnly"] if "readOnly" in config else False
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.selected_upgrade_priority = config["selectedUpgradePriority"] if "selectedUpgradePriority" in config else None
            self.server_groups = ZscalerCollection.form_list(
                config["serverGroups"] if "serverGroups" in config else [], AppServerGroup
            )
            self.lss_app_connector_group = config["lssAppConnectorGroup"] if "lssAppConnectorGroup" in config else False
            self.enrollment_cert_id = config["enrollmentCertId"] if "enrollmentCertId" in config else None
            self.private_cloud_id = config["privateCloudId"] if "privateCloudId" in config else None
            self.site_name = config["siteName"] if "siteName" in config else None
            self.tcp_quick_ack_app = config["tcpQuickAckApp"] if "tcpQuickAckApp" in config else False
            self.tcp_quick_ack_assistant = config["tcpQuickAckAssistant"] if "tcpQuickAckAssistant" in config else False
            self.tcp_quick_ack_read_assistant = (
                config["tcpQuickAckReadAssistant"] if "tcpQuickAckReadAssistant" in config else False
            )
            self.upgrade_day = config["upgradeDay"] if "upgradeDay" in config else None
            self.upgrade_priorities = ZscalerCollection.form_list(
                config["upgradePriorities"] if "upgradePriorities" in config else [], str
            )
            self.upgrade_priority = config["upgradePriority"] if "upgradePriority" in config else None
            self.upgrade_time_in_secs = config["upgradeTimeInSecs"] if "upgradeTimeInSecs" in config else None
            self.use_in_dr_mode = config["useInDrMode"] if "useInDrMode" in config else False
            if "version" in config:
                if isinstance(config["version"], common.ComponentLevelVersion):
                    self.version = config["version"]
                elif config["version"] is not None:
                    self.version = common.ComponentLevelVersion(config["version"])
                else:
                    self.version = None
            else:
                self.version = None
            self.version_profile_id = config["versionProfileId"] if "versionProfileId" in config else None
            self.version_profile_name = config["versionProfileName"] if "versionProfileName" in config else None
            self.version_profile_visibility_scope = (
                config["versionProfileVisibilityScope"] if "versionProfileVisibilityScope" in config else None
            )
            self.waf_disabled = config["wafDisabled"] if "wafDisabled" in config else False
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else False
        else:
            self.connectors = []
            self.city = None
            self.city_country = None
            self.connector_group_type = None
            self.country_code = None
            self.creation_time = None
            self.dc_hosting_info = None
            self.description = None
            self.dns_query_type = None
            self.enabled = False
            self.geo_location_id = None
            self.id = None
            self.ip_acl = []
            self.latitude = None
            self.location = None
            self.longitude = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.name_without_trim = None
            self.np_assistant_group = None
            self.override_version_profile = False
            self.pra_enabled = False
            self.read_only = False
            self.restriction_type = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.selected_upgrade_priority = None
            self.server_groups = []
            self.lss_app_connector_group = False
            self.enrollment_cert_id = None
            self.private_cloud_id = None
            self.site_name = None
            self.tcp_quick_ack_app = False
            self.tcp_quick_ack_assistant = False
            self.tcp_quick_ack_read_assistant = False
            self.upgrade_day = None
            self.upgrade_priorities = []
            self.upgrade_priority = None
            self.upgrade_time_in_secs = None
            self.use_in_dr_mode = False
            self.version = None
            self.version_profile_id = None
            self.version_profile_name = None
            self.version_profile_visibility_scope = None
            self.waf_disabled = False
            self.zscaler_managed = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "connectors": [item.request_format() for item in (self.connectors or [])],
            "city": self.city,
            "cityCountry": self.city_country,
            "connectorGroupType": self.connector_group_type,
            "countryCode": self.country_code,
            "creationTime": self.creation_time,
            "dcHostingInfo": self.dc_hosting_info,
            "description": self.description,
            "dnsQueryType": self.dns_query_type,
            "enabled": self.enabled,
            "geoLocationId": self.geo_location_id,
            "id": self.id,
            "ipAcl": self.ip_acl,
            "latitude": self.latitude,
            "location": self.location,
            "longitude": self.longitude,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "nameWithoutTrim": self.name_without_trim,
            "npAssistantGroup": self.np_assistant_group,
            "overrideVersionProfile": self.override_version_profile,
            "praEnabled": self.pra_enabled,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "selectedUpgradePriority": self.selected_upgrade_priority,
            "serverGroups": [item.request_format() for item in (self.server_groups or [])],
            "lssAppConnectorGroup": self.lss_app_connector_group,
            "enrollmentCertId": self.enrollment_cert_id,
            "privateCloudId": self.private_cloud_id,
            "siteName": self.site_name,
            "tcpQuickAckApp": self.tcp_quick_ack_app,
            "tcpQuickAckAssistant": self.tcp_quick_ack_assistant,
            "tcpQuickAckReadAssistant": self.tcp_quick_ack_read_assistant,
            "upgradeDay": self.upgrade_day,
            "upgradePriorities": self.upgrade_priorities,
            "upgradePriority": self.upgrade_priority,
            "upgradeTimeInSecs": self.upgrade_time_in_secs,
            "useInDrMode": self.use_in_dr_mode,
            "version": self.version,
            "versionProfileId": self.version_profile_id,
            "versionProfileName": self.version_profile_name,
            "versionProfileVisibilityScope": self.version_profile_visibility_scope,
            "wafDisabled": self.waf_disabled,
            "zscalerManaged": self.zscaler_managed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Connector(ZscalerObject):
    """
    A class representing a Connector object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.application_start_time = config["applicationStartTime"] if "applicationStartTime" in config else None
            self.app_connector_group_id = config["appConnectorGroupId"] if "appConnectorGroupId" in config else None
            self.app_connector_group_name = config["appConnectorGroupName"] if "appConnectorGroupName" in config else None
            if "assistantVersion" in config:
                if isinstance(config["assistantVersion"], AssistantVersion):
                    self.assistant_version = config["assistantVersion"]
                elif config["assistantVersion"] is not None:
                    self.assistant_version = AssistantVersion(config["assistantVersion"])
                else:
                    self.assistant_version = None
            else:
                self.assistant_version = None
            self.connector_type = config["connectorType"] if "connectorType" in config else None
            self.control_channel_status = config["controlChannelStatus"] if "controlChannelStatus" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.ctrl_broker_name = config["ctrlBrokerName"] if "ctrlBrokerName" in config else None
            self.current_version = config["currentVersion"] if "currentVersion" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else False
            self.enrollment_time = config["enrollmentTime"] if "enrollmentTime" in config else None
            self.expected_sarge_version = config["expectedSargeVersion"] if "expectedSargeVersion" in config else None
            self.expected_upgrade_time = config["expectedUpgradeTime"] if "expectedUpgradeTime" in config else None
            self.expected_version = config["expectedVersion"] if "expectedVersion" in config else None
            self.fingerprint = config["fingerprint"] if "fingerprint" in config else None
            self.id = config["id"] if "id" in config else None
            self.ip_acl = ZscalerCollection.form_list(config["ipAcl"] if "ipAcl" in config else [], str)
            self.ip_addr_setting = ZscalerCollection.form_list(
                config["ip_addr_setting"] if "ip_addr_setting" in config else [], IpAddrSetting
            )
            self.issued_cert_id = config["issuedCertId"] if "issuedCertId" in config else None
            self.last_broker_connect_time = config["lastBrokerConnectTime"] if "lastBrokerConnectTime" in config else None
            self.last_broker_connect_time_duration = (
                config["lastBrokerConnectTimeDuration"] if "lastBrokerConnectTimeDuration" in config else None
            )
            self.last_broker_disconnect_time = (
                config["lastBrokerDisconnectTime"] if "lastBrokerDisconnectTime" in config else None
            )
            self.last_broker_disconnect_time_duration = (
                config["lastBrokerDisconnectTimeDuration"] if "lastBrokerDisconnectTimeDuration" in config else None
            )
            self.last_o_s_upgrade_time = config["lastOSUpgradeTime"] if "lastOSUpgradeTime" in config else None
            self.last_sarge_upgrade_time = config["lastSargeUpgradeTime"] if "lastSargeUpgradeTime" in config else None
            self.last_upgrade_time = config["lastUpgradeTime"] if "lastUpgradeTime" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.location = config["location"] if "location" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.name_without_trim = config["nameWithoutTrim"] if "nameWithoutTrim" in config else None
            self.provisioning_key_id = config["provisioningKeyId"] if "provisioningKeyId" in config else None
            self.provisioning_key_name = config["provisioningKeyName"] if "provisioningKeyName" in config else None
            if "npAssistant" in config:
                if isinstance(config["npAssistant"], NPAssistant):
                    self.np_assistant = config["npAssistant"]
                elif config["npAssistant"] is not None:
                    self.np_assistant = NPAssistant(config["npAssistant"])
                else:
                    self.np_assistant = None
            else:
                self.np_assistant = None
            self.os_upgrade_enabled = config["osUpgradeEnabled"] if "osUpgradeEnabled" in config else False
            self.os_upgrade_fail_reason_code = (
                config["osUpgradeFailReasonCode"] if "osUpgradeFailReasonCode" in config else None
            )
            self.os_upgrade_status = config["osUpgradeStatus"] if "osUpgradeStatus" in config else None
            self.platform = config["platform"] if "platform" in config else None
            self.platform_detail = config["platformDetail"] if "platformDetail" in config else None
            self.platform_version = config["platformVersion"] if "platformVersion" in config else None
            self.previous_version = config["previousVersion"] if "previousVersion" in config else None
            self.private_ip = config["privateIp"] if "privateIp" in config else None
            self.public_ip = config["publicIp"] if "publicIp" in config else None
            self.read_only = config["readOnly"] if "readOnly" in config else False
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.runtime_os = config["runtimeOS"] if "runtimeOS" in config else None
            self.sarge_upgrade_attempt = config["sargeUpgradeAttempt"] if "sargeUpgradeAttempt" in config else None
            self.sarge_upgrade_status = config["sargeUpgradeStatus"] if "sargeUpgradeStatus" in config else None
            self.sarge_version = config["sargeVersion"] if "sargeVersion" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.enrollment_cert = config["enrollmentCert"] if "enrollmentCert" in config else None
            if "ssh_setting" in config:
                if isinstance(config["ssh_setting"], SshSetting):
                    self.ssh_setting = config["ssh_setting"]
                elif config["ssh_setting"] is not None:
                    self.ssh_setting = SshSetting(config["ssh_setting"])
                else:
                    self.ssh_setting = None
            else:
                self.ssh_setting = None
            self.upgrade_attempt = config["upgradeAttempt"] if "upgradeAttempt" in config else None
            self.upgrade_status = config["upgradeStatus"] if "upgradeStatus" in config else None
            if "version" in config:
                if isinstance(config["version"], common.ComponentLevelVersion):
                    self.version = config["version"]
                elif config["version"] is not None:
                    self.version = common.ComponentLevelVersion(config["version"])
                else:
                    self.version = None
            else:
                self.version = None
            self.zpn_sub_module_upgrade_list = ZscalerCollection.form_list(
                config["zpnSubModuleUpgradeList"] if "zpnSubModuleUpgradeList" in config else [], ZpnSubModuleUpgrade
            )
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else False
        else:
            self.application_start_time = None
            self.app_connector_group_id = None
            self.app_connector_group_name = None
            self.assistant_version = None
            self.connector_type = None
            self.control_channel_status = None
            self.creation_time = None
            self.ctrl_broker_name = None
            self.current_version = None
            self.description = None
            self.enabled = False
            self.enrollment_time = None
            self.expected_sarge_version = None
            self.expected_upgrade_time = None
            self.expected_version = None
            self.fingerprint = None
            self.id = None
            self.ip_acl = []
            self.ip_addr_setting = []
            self.issued_cert_id = None
            self.last_broker_connect_time = None
            self.last_broker_connect_time_duration = None
            self.last_broker_disconnect_time = None
            self.last_broker_disconnect_time_duration = None
            self.last_o_s_upgrade_time = None
            self.last_sarge_upgrade_time = None
            self.last_upgrade_time = None
            self.latitude = None
            self.location = None
            self.longitude = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.name_without_trim = None
            self.provisioning_key_id = None
            self.provisioning_key_name = None
            self.np_assistant = None
            self.os_upgrade_enabled = False
            self.os_upgrade_fail_reason_code = None
            self.os_upgrade_status = None
            self.platform = None
            self.platform_detail = None
            self.platform_version = None
            self.previous_version = None
            self.private_ip = None
            self.public_ip = None
            self.read_only = False
            self.restriction_type = None
            self.runtime_os = None
            self.sarge_upgrade_attempt = None
            self.sarge_upgrade_status = None
            self.sarge_version = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.enrollment_cert = None
            self.ssh_setting = None
            self.upgrade_attempt = None
            self.upgrade_status = None
            self.version = None
            self.zpn_sub_module_upgrade_list = []
            self.zscaler_managed = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "applicationStartTime": self.application_start_time,
            "appConnectorGroupId": self.app_connector_group_id,
            "appConnectorGroupName": self.app_connector_group_name,
            "assistantVersion": self.assistant_version,
            "connectorType": self.connector_type,
            "controlChannelStatus": self.control_channel_status,
            "creationTime": self.creation_time,
            "ctrlBrokerName": self.ctrl_broker_name,
            "currentVersion": self.current_version,
            "description": self.description,
            "enabled": self.enabled,
            "enrollmentTime": self.enrollment_time,
            "expectedSargeVersion": self.expected_sarge_version,
            "expectedUpgradeTime": self.expected_upgrade_time,
            "expectedVersion": self.expected_version,
            "fingerprint": self.fingerprint,
            "id": self.id,
            "ipAcl": self.ip_acl,
            "ip_addr_setting": [item.request_format() for item in (self.ip_addr_setting or [])],
            "issuedCertId": self.issued_cert_id,
            "lastBrokerConnectTime": self.last_broker_connect_time,
            "lastBrokerConnectTimeDuration": self.last_broker_connect_time_duration,
            "lastBrokerDisconnectTime": self.last_broker_disconnect_time,
            "lastBrokerDisconnectTimeDuration": self.last_broker_disconnect_time_duration,
            "lastOSUpgradeTime": self.last_o_s_upgrade_time,
            "lastSargeUpgradeTime": self.last_sarge_upgrade_time,
            "lastUpgradeTime": self.last_upgrade_time,
            "latitude": self.latitude,
            "location": self.location,
            "longitude": self.longitude,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "nameWithoutTrim": self.name_without_trim,
            "provisioningKeyId": self.provisioning_key_id,
            "provisioningKeyName": self.provisioning_key_name,
            "npAssistant": self.np_assistant,
            "osUpgradeEnabled": self.os_upgrade_enabled,
            "osUpgradeFailReasonCode": self.os_upgrade_fail_reason_code,
            "osUpgradeStatus": self.os_upgrade_status,
            "platform": self.platform,
            "platformDetail": self.platform_detail,
            "platformVersion": self.platform_version,
            "previousVersion": self.previous_version,
            "privateIp": self.private_ip,
            "publicIp": self.public_ip,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "runtimeOS": self.runtime_os,
            "sargeUpgradeAttempt": self.sarge_upgrade_attempt,
            "sargeUpgradeStatus": self.sarge_upgrade_status,
            "sargeVersion": self.sarge_version,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "enrollmentCert": self.enrollment_cert,
            "ssh_setting": self.ssh_setting,
            "upgradeAttempt": self.upgrade_attempt,
            "upgradeStatus": self.upgrade_status,
            "version": self.version,
            "zpnSubModuleUpgradeList": [item.request_format() for item in (self.zpn_sub_module_upgrade_list or [])],
            "zscalerManaged": self.zscaler_managed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppServerGroup(ZscalerObject):
    """
    A class representing a AppServerGroup object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.config_space = config["configSpace"] if "configSpace" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else False
            self.extranet_enabled = config["extranetEnabled"] if "extranetEnabled" in config else False
            self.id = config["id"] if "id" in config else None
            self.dynamic_discovery = config["dynamicDiscovery"] if "dynamicDiscovery" in config else False
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.name_without_trim = config["nameWithoutTrim"] if "nameWithoutTrim" in config else None
            self.passive = config["passive"] if "passive" in config else False
            self.read_only = config["readOnly"] if "readOnly" in config else False
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.weight = config["weight"] if "weight" in config else None
            if "zpnErId" in config:
                if isinstance(config["zpnErId"], ZpnExtranet):
                    self.zpn_er_id = config["zpnErId"]
                elif config["zpnErId"] is not None:
                    self.zpn_er_id = ZpnExtranet(config["zpnErId"])
                else:
                    self.zpn_er_id = None
            else:
                self.zpn_er_id = None
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else False
        else:
            self.config_space = None
            self.creation_time = None
            self.description = None
            self.enabled = False
            self.extranet_enabled = False
            self.id = None
            self.dynamic_discovery = False
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.name_without_trim = None
            self.passive = False
            self.read_only = False
            self.restriction_type = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.weight = None
            self.zpn_er_id = None
            self.zscaler_managed = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "configSpace": self.config_space,
            "creationTime": self.creation_time,
            "description": self.description,
            "enabled": self.enabled,
            "extranetEnabled": self.extranet_enabled,
            "id": self.id,
            "dynamicDiscovery": self.dynamic_discovery,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "nameWithoutTrim": self.name_without_trim,
            "passive": self.passive,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "weight": self.weight,
            "zpnErId": self.zpn_er_id,
            "zscalerManaged": self.zscaler_managed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AssistantVersion(ZscalerObject):
    """
    A class representing a AssistantVersion object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.application_start_time = config["applicationStartTime"] if "applicationStartTime" in config else None
            self.app_connector_group_id = config["appConnectorGroupId"] if "appConnectorGroupId" in config else None
            self.broker_id = config["brokerId"] if "brokerId" in config else None
            self.connector_type = config["connectorType"] if "connectorType" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.ctrl_channel_status = config["ctrlChannelStatus"] if "ctrlChannelStatus" in config else None
            self.current_version = config["currentVersion"] if "currentVersion" in config else None
            self.disable_auto_update = config["disableAutoUpdate"] if "disableAutoUpdate" in config else False
            self.expected_sarge_version = config["expectedSargeVersion"] if "expectedSargeVersion" in config else None
            self.expected_version = config["expectedVersion"] if "expectedVersion" in config else None
            self.id = config["id"] if "id" in config else None
            self.last_broker_connect_time = config["lastBrokerConnectTime"] if "lastBrokerConnectTime" in config else None
            self.last_broker_disconnect_time = (
                config["lastBrokerDisconnectTime"] if "lastBrokerDisconnectTime" in config else None
            )
            self.last_o_s_upgrade_time = config["lastOSUpgradeTime"] if "lastOSUpgradeTime" in config else None
            self.last_sarge_upgrade_time = config["lastSargeUpgradeTime"] if "lastSargeUpgradeTime" in config else None
            self.last_upgraded_time = config["lastUpgradedTime"] if "lastUpgradedTime" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.lone_warrior = config["loneWarrior"] if "loneWarrior" in config else False
            self.longitude = config["longitude"] if "longitude" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.mtunnel_id = config["mtunnelId"] if "mtunnelId" in config else None
            self.os_upgrade_enabled = config["osUpgradeEnabled"] if "osUpgradeEnabled" in config else False
            self.os_upgrade_fail_reason_code = (
                config["osUpgradeFailReasonCode"] if "osUpgradeFailReasonCode" in config else None
            )
            self.os_upgrade_status = config["osUpgradeStatus"] if "osUpgradeStatus" in config else None
            self.platform = config["platform"] if "platform" in config else None
            self.platform_detail = config["platformDetail"] if "platformDetail" in config else None
            self.platform_version = config["platformVersion"] if "platformVersion" in config else None
            self.previous_sarge_version = config["previousSargeVersion"] if "previousSargeVersion" in config else None
            self.previous_version = config["previousVersion"] if "previousVersion" in config else None
            self.private_ip = config["privateIp"] if "privateIp" in config else None
            self.public_ip = config["publicIp"] if "publicIp" in config else None
            self.restart_time_in_sec = config["restartTimeInSec"] if "restartTimeInSec" in config else None
            self.runtime_os = config["runtimeOS"] if "runtimeOS" in config else None
            self.sarge_upgrade_attempt = config["sargeUpgradeAttempt"] if "sargeUpgradeAttempt" in config else None
            self.sarge_upgrade_status = config["sargeUpgradeStatus"] if "sargeUpgradeStatus" in config else None
            self.sarge_version = config["sargeVersion"] if "sargeVersion" in config else None
            self.system_start_time = config["systemStartTime"] if "systemStartTime" in config else None
            self.upgrade_attempt = config["upgradeAttempt"] if "upgradeAttempt" in config else None
            self.upgrade_now_once = config["upgradeNowOnce"] if "upgradeNowOnce" in config else False
            self.upgrade_status = config["upgradeStatus"] if "upgradeStatus" in config else None
            self.zpn_sub_module_upgrade = ZscalerCollection.form_list(
                config["zpnSubModuleUpgrade"] if "zpnSubModuleUpgrade" in config else [], ZpnSubModuleUpgrade
            )
        else:
            self.application_start_time = None
            self.app_connector_group_id = None
            self.broker_id = None
            self.connector_type = None
            self.creation_time = None
            self.ctrl_channel_status = None
            self.current_version = None
            self.disable_auto_update = False
            self.expected_sarge_version = None
            self.expected_version = None
            self.id = None
            self.last_broker_connect_time = None
            self.last_broker_disconnect_time = None
            self.last_o_s_upgrade_time = None
            self.last_sarge_upgrade_time = None
            self.last_upgraded_time = None
            self.latitude = None
            self.lone_warrior = False
            self.longitude = None
            self.modified_by = None
            self.modified_time = None
            self.mtunnel_id = None
            self.os_upgrade_enabled = False
            self.os_upgrade_fail_reason_code = None
            self.os_upgrade_status = None
            self.platform = None
            self.platform_detail = None
            self.platform_version = None
            self.previous_sarge_version = None
            self.previous_version = None
            self.private_ip = None
            self.public_ip = None
            self.restart_time_in_sec = None
            self.runtime_os = None
            self.sarge_upgrade_attempt = None
            self.sarge_upgrade_status = None
            self.sarge_version = None
            self.system_start_time = None
            self.upgrade_attempt = None
            self.upgrade_now_once = False
            self.upgrade_status = None
            self.zpn_sub_module_upgrade = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "applicationStartTime": self.application_start_time,
            "appConnectorGroupId": self.app_connector_group_id,
            "brokerId": self.broker_id,
            "connectorType": self.connector_type,
            "creationTime": self.creation_time,
            "ctrlChannelStatus": self.ctrl_channel_status,
            "currentVersion": self.current_version,
            "disableAutoUpdate": self.disable_auto_update,
            "expectedSargeVersion": self.expected_sarge_version,
            "expectedVersion": self.expected_version,
            "id": self.id,
            "lastBrokerConnectTime": self.last_broker_connect_time,
            "lastBrokerDisconnectTime": self.last_broker_disconnect_time,
            "lastOSUpgradeTime": self.last_o_s_upgrade_time,
            "lastSargeUpgradeTime": self.last_sarge_upgrade_time,
            "lastUpgradedTime": self.last_upgraded_time,
            "latitude": self.latitude,
            "loneWarrior": self.lone_warrior,
            "longitude": self.longitude,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "mtunnelId": self.mtunnel_id,
            "osUpgradeEnabled": self.os_upgrade_enabled,
            "osUpgradeFailReasonCode": self.os_upgrade_fail_reason_code,
            "osUpgradeStatus": self.os_upgrade_status,
            "platform": self.platform,
            "platformDetail": self.platform_detail,
            "platformVersion": self.platform_version,
            "previousSargeVersion": self.previous_sarge_version,
            "previousVersion": self.previous_version,
            "privateIp": self.private_ip,
            "publicIp": self.public_ip,
            "restartTimeInSec": self.restart_time_in_sec,
            "runtimeOS": self.runtime_os,
            "sargeUpgradeAttempt": self.sarge_upgrade_attempt,
            "sargeUpgradeStatus": self.sarge_upgrade_status,
            "sargeVersion": self.sarge_version,
            "systemStartTime": self.system_start_time,
            "upgradeAttempt": self.upgrade_attempt,
            "upgradeNowOnce": self.upgrade_now_once,
            "upgradeStatus": self.upgrade_status,
            "zpnSubModuleUpgrade": [item.request_format() for item in (self.zpn_sub_module_upgrade or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class IpAddrSetting(ZscalerObject):
    """
    A class representing a IpAddrSetting object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.interface = config["interface"] if "interface" in config else None
            self.ip_addr_cidr = config["ip_addr_cidr"] if "ip_addr_cidr" in config else None
        else:
            self.interface = None
            self.ip_addr_cidr = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "interface": self.interface,
            "ip_addr_cidr": self.ip_addr_cidr,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NPAssistant(ZscalerObject):
    """
    A class representing a NPAssistant object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.connector_id = config["connectorId"] if "connectorId" in config else None
            self.config_override = config["configOverride"] if "configOverride" in config else None
            self.connector_state = config["connectorState"] if "connectorState" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.force_reload_config = config["forceReloadConfig"] if "forceReloadConfig" in config else False
            self.gateway_listener_port = config["gatewayListenerPort"] if "gatewayListenerPort" in config else None
            self.id = config["id"] if "id" in config else None
            self.local_router_id = config["localRouterId"] if "localRouterId" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.override_mode = config["overrideMode"] if "overrideMode" in config else False
            self.public_key = config["publicKey"] if "publicKey" in config else None
            self.public_key_expiry = config["publicKeyExpiry"] if "publicKeyExpiry" in config else None
            self.redundant_mode_enabled = config["redundantModeEnabled"] if "redundantModeEnabled" in config else False
        else:
            self.connector_id = None
            self.config_override = None
            self.connector_state = None
            self.creation_time = None
            self.force_reload_config = False
            self.gateway_listener_port = None
            self.id = None
            self.local_router_id = None
            self.modified_by = None
            self.modified_time = None
            self.override_mode = False
            self.public_key = None
            self.public_key_expiry = None
            self.redundant_mode_enabled = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "connectorId": self.connector_id,
            "configOverride": self.config_override,
            "connectorState": self.connector_state,
            "creationTime": self.creation_time,
            "forceReloadConfig": self.force_reload_config,
            "gatewayListenerPort": self.gateway_listener_port,
            "id": self.id,
            "localRouterId": self.local_router_id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "overrideMode": self.override_mode,
            "publicKey": self.public_key,
            "publicKeyExpiry": self.public_key_expiry,
            "redundantModeEnabled": self.redundant_mode_enabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SshSetting(ZscalerObject):
    """
    A class representing a SshSetting object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.status = config["status"] if "status" in config else None
        else:
            self.status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ZpnSubModuleUpgrade(ZscalerObject):
    """
    A class representing a ZpnSubModuleUpgrade object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.current_version = config["currentVersion"] if "currentVersion" in config else None
            self.entity_gid = config["entityGid"] if "entityGid" in config else None
            self.entity_type = config["entityType"] if "entityType" in config else None
            self.expected_version = config["expectedVersion"] if "expectedVersion" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.previous_version = config["previousVersion"] if "previousVersion" in config else None
            self.role = config["role"] if "role" in config else None
            self.upgrade_status = config["upgradeStatus"] if "upgradeStatus" in config else None
            self.upgrade_time = config["upgradeTime"] if "upgradeTime" in config else None
        else:
            self.creation_time = None
            self.current_version = None
            self.entity_gid = None
            self.entity_type = None
            self.expected_version = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.previous_version = None
            self.role = None
            self.upgrade_status = None
            self.upgrade_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "currentVersion": self.current_version,
            "entityGid": self.entity_gid,
            "entityType": self.entity_type,
            "expectedVersion": self.expected_version,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "previousVersion": self.previous_version,
            "role": self.role,
            "upgradeStatus": self.upgrade_status,
            "upgradeTime": self.upgrade_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ZpnExtranet(ZscalerObject):
    """
    A class representing a ZpnExtranet object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.zia_cloud = config["ziaCloud"] if "ziaCloud" in config else None
            self.zia_er_id = config["ziaErId"] if "ziaErId" in config else None
            self.zia_er_name = config["ziaErName"] if "ziaErName" in config else None
            self.zia_modified_time = config["ziaModifiedTime"] if "ziaModifiedTime" in config else None
            self.zia_org_id = config["ziaOrgId"] if "ziaOrgId" in config else None
        else:
            self.creation_time = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.zia_cloud = None
            self.zia_er_id = None
            self.zia_er_name = None
            self.zia_modified_time = None
            self.zia_org_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "ziaCloud": self.zia_cloud,
            "ziaErId": self.zia_er_id,
            "ziaErName": self.zia_er_name,
            "ziaModifiedTime": self.zia_modified_time,
            "ziaOrgId": self.zia_org_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
