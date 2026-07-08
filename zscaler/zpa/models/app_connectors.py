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


class AppConnectorController(ZscalerObject):
    """
    A class representing the App Connector Controller.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the AppConnector model based on API response.

        Args:
            config (dict): A dictionary representing the App Connector configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.fingerprint = config["fingerprint"] if "fingerprint" in config else None
            self.current_version = config["currentVersion"] if "currentVersion" in config else None
            self.previous_version = config["previousVersion"] if "previousVersion" in config else None
            self.expected_version = config["expectedVersion"] if "expectedVersion" in config else None
            self.upgrade_status = config["upgradeStatus"] if "upgradeStatus" in config else None
            self.upgrade_attempt = config["upgradeAttempt"] if "upgradeAttempt" in config else None
            self.control_channel_status = config["controlChannelStatus"] if "controlChannelStatus" in config else None
            self.private_ip = config["privateIp"] if "privateIp" in config else None
            self.public_ip = config["publicIp"] if "publicIp" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.location = config["location"] if "location" in config else None
            self.provisioning_key_id = config["provisioningKeyId"] if "provisioningKeyId" in config else None
            self.provisioning_key_name = config["provisioningKeyName"] if "provisioningKeyName" in config else None
            self.app_connector_group_id = config["appConnectorGroupId"] if "appConnectorGroupId" in config else None
            self.app_connector_group_name = config["appConnectorGroupName"] if "appConnectorGroupName" in config else None
            self.platform = config["platform"] if "platform" in config else None
            self.platform_detail = config["platformDetail"] if "platformDetail" in config else None
            self.runtime_os = config["runtimeOS"] if "runtimeOS" in config else None
            self.sarge_version = config["sargeVersion"] if "sargeVersion" in config else None
            self.issued_cert_id = config["issuedCertId"] if "issuedCertId" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
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
            self.last_upgrade_time = config["lastUpgradeTime"] if "lastUpgradeTime" in config else None
            self.expected_upgrade_time = config["expectedUpgradeTime"] if "expectedUpgradeTime" in config else None
            self.ctrl_broker_name = config["ctrlBrokerName"] if "ctrlBrokerName" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.enrollment_cert = config["enrollmentCert"] if "enrollmentCert" in config else None
            self.application_start_time = config["applicationStartTime"] if "applicationStartTime" in config else None
            self.ip_acl = config["ipAcl"] if "ipAcl" in config else []
            self.zpn_sub_module_upgrade_list = ZscalerCollection.form_list(
                config["zpnSubModuleUpgradeList"] if "zpnSubModuleUpgradeList" in config else [], ZPNSubModuleUpgradeList
            )
            self.connector_type = config["connectorType"] if "connectorType" in config else None
            self.enrollment_time = config["enrollmentTime"] if "enrollmentTime" in config else None
            self.expected_sarge_version = config["expectedSargeVersion"] if "expectedSargeVersion" in config else None
            self.last_os_upgrade_time = config["lastOSUpgradeTime"] if "lastOSUpgradeTime" in config else None
            self.last_sarge_upgrade_time = config["lastSargeUpgradeTime"] if "lastSargeUpgradeTime" in config else None
            self.name_without_trim = config["nameWithoutTrim"] if "nameWithoutTrim" in config else None
            self.os_upgrade_enabled = config["osUpgradeEnabled"] if "osUpgradeEnabled" in config else None
            self.os_upgrade_fail_reason_code = (
                config["osUpgradeFailReasonCode"] if "osUpgradeFailReasonCode" in config else None
            )
            self.os_upgrade_status = config["osUpgradeStatus"] if "osUpgradeStatus" in config else None
            self.platform_version = config["platformVersion"] if "platformVersion" in config else None
            self.read_only = config["readOnly"] if "readOnly" in config else None
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.sarge_upgrade_attempt = config["sargeUpgradeAttempt"] if "sargeUpgradeAttempt" in config else None
            self.sarge_upgrade_status = config["sargeUpgradeStatus"] if "sargeUpgradeStatus" in config else None
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else None
            self.ip_addr_setting = ZscalerCollection.form_list(
                config["ip_addr_setting"] if "ip_addr_setting" in config else [], IpAddrSetting
            )

            if "assistantVersion" in config:
                if isinstance(config["assistantVersion"], AssistantVersion):
                    self.assistant_version = config["assistantVersion"]
                elif config["assistantVersion"] is not None:
                    self.assistant_version = AssistantVersion(config["assistantVersion"])
                else:
                    self.assistant_version = None
            else:
                self.assistant_version = None

            if "npAssistant" in config:
                if isinstance(config["npAssistant"], NPAssistant):
                    self.np_assistant = config["npAssistant"]
                elif config["npAssistant"] is not None:
                    self.np_assistant = NPAssistant(config["npAssistant"])
                else:
                    self.np_assistant = None
            else:
                self.np_assistant = None

            if "version" in config:
                if isinstance(config["version"], ComponentLevelVersion):
                    self.version = config["version"]
                elif config["version"] is not None:
                    self.version = ComponentLevelVersion(config["version"])
                else:
                    self.version = None
            else:
                self.version = None

            if "ssh_setting" in config:
                if isinstance(config["ssh_setting"], SshSetting):
                    self.ssh_setting = config["ssh_setting"]
                elif config["ssh_setting"] is not None:
                    self.ssh_setting = SshSetting(config["ssh_setting"])
                else:
                    self.ssh_setting = None
            else:
                self.ssh_setting = None

        else:
            self.id = None
            self.name = None
            self.description = None
            self.enabled = True
            self.fingerprint = None
            self.current_version = None
            self.previous_version = None
            self.expected_version = None
            self.upgrade_status = None
            self.upgrade_attempt = None
            self.control_channel_status = None
            self.private_ip = None
            self.public_ip = None
            self.latitude = None
            self.longitude = None
            self.location = None
            self.provisioning_key_id = None
            self.provisioning_key_name = None
            self.app_connector_group_id = None
            self.app_connector_group_name = None
            self.platform = None
            self.platform_detail = None
            self.runtime_os = None
            self.sarge_version = None
            self.issued_cert_id = None
            self.creation_time = None
            self.modified_time = None
            self.modified_by = None
            self.last_broker_connect_time = None
            self.last_broker_connect_time_duration = None
            self.last_broker_disconnect_time = None
            self.last_broker_disconnect_time_duration = None
            self.last_upgrade_time = None
            self.expected_upgrade_time = None
            self.ctrl_broker_name = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.enrollment_cert = None
            self.application_start_time = None
            self.assistant_version = None
            self.ssh_setting = None
            self.ip_acl = []
            self.zpn_sub_module_upgrade_list = []
            self.connector_type = None
            self.enrollment_time = None
            self.expected_sarge_version = None
            self.last_os_upgrade_time = None
            self.last_sarge_upgrade_time = None
            self.name_without_trim = None
            self.os_upgrade_enabled = None
            self.os_upgrade_fail_reason_code = None
            self.os_upgrade_status = None
            self.platform_version = None
            self.read_only = None
            self.restriction_type = None
            self.sarge_upgrade_attempt = None
            self.sarge_upgrade_status = None
            self.zscaler_managed = None
            self.ip_addr_setting = []
            self.np_assistant = None
            self.version = None

    def request_format(self) -> Dict[str, Any]:
        """
        Formats the App Connector data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "fingerprint": self.fingerprint,
            "currentVersion": self.current_version,
            "previousVersion": self.previous_version,
            "expectedVersion": self.expected_version,
            "upgradeStatus": self.upgrade_status,
            "upgradeAttempt": self.upgrade_attempt,
            "controlChannelStatus": self.control_channel_status,
            "privateIp": self.private_ip,
            "publicIp": self.public_ip,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location": self.location,
            "provisioningKeyId": self.provisioning_key_id,
            "provisioningKeyName": self.provisioning_key_name,
            "appConnectorGroupId": self.app_connector_group_id,
            "appConnectorGroupName": self.app_connector_group_name,
            "platform": self.platform,
            "platformDetail": self.platform_detail,
            "runtimeOS": self.runtime_os,
            "sargeVersion": self.sarge_version,
            "issuedCertId": self.issued_cert_id,
            "creationTime": self.creation_time,
            "modifiedTime": self.modified_time,
            "modifiedBy": self.modified_by,
            "lastBrokerConnectTime": self.last_broker_connect_time,
            "lastBrokerConnectTimeDuration": self.last_broker_connect_time_duration,
            "lastBrokerDisconnectTime": self.last_broker_disconnect_time,
            "lastBrokerDisconnectTimeDuration": self.last_broker_disconnect_time_duration,
            "lastUpgradeTime": self.last_upgrade_time,
            "expectedUpgradeTime": self.expected_upgrade_time,
            "ctrlBrokerName": self.ctrl_broker_name,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "enrollmentCert": self.enrollment_cert,
            "applicationStartTime": self.application_start_time,
            "ipAcl": self.ip_acl,
            "ssh_setting": self.ssh_setting,
            "zpnSubModuleUpgradeList": self.zpn_sub_module_upgrade_list,
            "assistantVersion": self.assistant_version,
            "connectorType": self.connector_type,
            "enrollmentTime": self.enrollment_time,
            "expectedSargeVersion": self.expected_sarge_version,
            "lastOSUpgradeTime": self.last_os_upgrade_time,
            "lastSargeUpgradeTime": self.last_sarge_upgrade_time,
            "nameWithoutTrim": self.name_without_trim,
            "osUpgradeEnabled": self.os_upgrade_enabled,
            "osUpgradeFailReasonCode": self.os_upgrade_fail_reason_code,
            "osUpgradeStatus": self.os_upgrade_status,
            "platformVersion": self.platform_version,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "sargeUpgradeAttempt": self.sarge_upgrade_attempt,
            "sargeUpgradeStatus": self.sarge_upgrade_status,
            "zscalerManaged": self.zscaler_managed,
            "ip_addr_setting": self.ip_addr_setting,
            "npAssistant": self.np_assistant,
            "version": self.version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AssistantVersion(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Assistant Version model based on API response.
        """
        super().__init__(config)
        if config:
            self.application_start_time = config["applicationStartTime"] if "applicationStartTime" in config else None
            self.app_connector_group_id = config["appConnectorGroupId"] if "appConnectorGroupId" in config else None
            self.broker_id = config["brokerId"] if "brokerId" in config else None
            self.connector_type = config["connectorType"] if "connectorType" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.ctrl_channel_status = config["ctrlChannelStatus"] if "ctrlChannelStatus" in config else None
            self.current_version = config["currentVersion"] if "currentVersion" in config else None
            self.disable_auto_update = config["disableAutoUpdate"] if "disableAutoUpdate" in config else None
            self.expected_sarge_version = config["expectedSargeVersion"] if "expectedSargeVersion" in config else None
            self.expected_version = config["expectedVersion"] if "expectedVersion" in config else None
            self.id = config["id"] if "id" in config else None
            self.last_broker_connect_time = config["lastBrokerConnectTime"] if "lastBrokerConnectTime" in config else None
            self.last_broker_disconnect_time = (
                config["lastBrokerDisconnectTime"] if "lastBrokerDisconnectTime" in config else None
            )
            self.last_os_upgrade_time = config["lastOSUpgradeTime"] if "lastOSUpgradeTime" in config else None
            self.last_sarge_upgrade_time = config["lastSargeUpgradeTime"] if "lastSargeUpgradeTime" in config else None
            self.last_upgraded_time = config["lastUpgradedTime"] if "lastUpgradedTime" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.lone_warrior = config["loneWarrior"] if "loneWarrior" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.mtunnel_id = config["mtunnelId"] if "mtunnelId" in config else None
            self.os_upgrade_enabled = config["osUpgradeEnabled"] if "osUpgradeEnabled" in config else None
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
            self.upgrade_now_once = config["upgradeNowOnce"] if "upgradeNowOnce" in config else None
            self.upgrade_status = config["upgradeStatus"] if "upgradeStatus" in config else None
            self.zpn_sub_module_upgrade = ZscalerCollection.form_list(
                config["zpnSubModuleUpgrade"] if "zpnSubModuleUpgrade" in config else [], ZPNSubModuleUpgradeList
            )
        else:
            self.application_start_time = None
            self.app_connector_group_id = None
            self.broker_id = None
            self.connector_type = None
            self.creation_time = None
            self.ctrl_channel_status = None
            self.current_version = None
            self.disable_auto_update = None
            self.expected_sarge_version = None
            self.expected_version = None
            self.id = None
            self.last_broker_connect_time = None
            self.last_broker_disconnect_time = None
            self.last_os_upgrade_time = None
            self.last_sarge_upgrade_time = None
            self.last_upgraded_time = None
            self.latitude = None
            self.lone_warrior = None
            self.longitude = None
            self.modified_by = None
            self.modified_time = None
            self.mtunnel_id = None
            self.os_upgrade_enabled = None
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
            self.upgrade_now_once = None
            self.upgrade_status = None
            self.zpn_sub_module_upgrade = []

    def request_format(self) -> Dict[str, Any]:
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
            "lastOSUpgradeTime": self.last_os_upgrade_time,
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
            "zpnSubModuleUpgrade": self.zpn_sub_module_upgrade,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NPAssistant(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the NP Assistant model based on API response.
        """
        super().__init__(config)
        if config:
            self.connector_id = config["connectorId"] if "connectorId" in config else None
            self.config_override = config["configOverride"] if "configOverride" in config else None
            self.connector_state = config["connectorState"] if "connectorState" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.force_reload_config = config["forceReloadConfig"] if "forceReloadConfig" in config else None
            self.gateway_listener_port = config["gatewayListenerPort"] if "gatewayListenerPort" in config else None
            self.id = config["id"] if "id" in config else None
            self.local_router_id = config["localRouterId"] if "localRouterId" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.override_mode = config["overrideMode"] if "overrideMode" in config else None
            self.public_key = config["publicKey"] if "publicKey" in config else None
            self.public_key_expiry = config["publicKeyExpiry"] if "publicKeyExpiry" in config else None
            self.redundant_mode_enabled = config["redundantModeEnabled"] if "redundantModeEnabled" in config else None
        else:
            self.connector_id = None
            self.config_override = None
            self.connector_state = None
            self.creation_time = None
            self.force_reload_config = None
            self.gateway_listener_port = None
            self.id = None
            self.local_router_id = None
            self.modified_by = None
            self.modified_time = None
            self.override_mode = None
            self.public_key = None
            self.public_key_expiry = None
            self.redundant_mode_enabled = None

    def request_format(self) -> Dict[str, Any]:
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


class ComponentLevelVersion(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Assistant Version model based on API response.
        """
        super().__init__(config)
        if config:
            self.child_version = config["childVersion"] if "childVersion" in config else None
            self.latest_platform = config["latestPlatform"] if "latestPlatform" in config else None
            self.platform = config["platform"] if "platform" in config else None
            self.sarge_version = config["sargeVersion"] if "sargeVersion" in config else None
            self.version_profile_name = config["versionProfileName"] if "versionProfileName" in config else None
            self.version_profile_gid = config["version_profile_gid"] if "version_profile_gid" in config else None
        else:
            self.child_version = None
            self.latest_platform = None
            self.platform = None
            self.sarge_version = None
            self.version_profile_name = None
            self.version_profile_gid = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "childVersion": self.child_version,
            "latestPlatform": self.latest_platform,
            "platform": self.platform,
            "sargeVersion": self.sarge_version,
            "versionProfileName": self.version_profile_name,
            "version_profile_gid": self.version_profile_gid,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ZPNSubModuleUpgradeList(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ZPN Sub Module Upgrade List model based on API response.
        """
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

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "creationTime": self.creation_time,
            "currentVersion": self.current_version,
            "entityGid": self.entity_gid,
            "entityType": self.entity_type,
            "expectedVersion": self.expected_version,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "previousVersion": self.previous_version,
            "role": self.role,
            "upgradeStatus": self.upgrade_status,
            "upgradeTime": self.upgrade_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class IpAddrSetting(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the IpAddrSetting model based on API response.
        """
        super().__init__(config)
        if config:
            self.interface = config["interface"] if "interface" in config else None
            self.ip_addr_cidr = config["ip_addr_cidr"] if "ip_addr_cidr" in config else None
        else:
            self.interface = None
            self.ip_addr_cidr = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "interface": self.interface,
            "ip_addr_cidr": self.ip_addr_cidr,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SshSetting(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the SshSetting model based on API response.
        """
        super().__init__(config)
        if config:
            self.status = config["status"] if "status" in config else None
        else:
            self.status = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
