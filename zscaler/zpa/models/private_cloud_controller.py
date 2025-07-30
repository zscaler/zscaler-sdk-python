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


class PrivateCloudController(ZscalerObject):
    """
    A class for PrivateCloudController objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PrivateCloudController model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.application_start_time = config["applicationStartTime"] \
                if "applicationStartTime" in config else None
            self.control_channel_status = config["controlChannelStatus"] \
                if "controlChannelStatus" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.ctrl_broker_name = config["ctrlBrokerName"] \
                if "ctrlBrokerName" in config else None
            self.current_version = config["currentVersion"] \
                if "currentVersion" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.expected_sarge_version = config["expectedSargeVersion"] \
                if "expectedSargeVersion" in config else None
            self.expected_upgrade_time = config["expectedUpgradeTime"] \
                if "expectedUpgradeTime" in config else None
            self.expected_version = config["expectedVersion"] \
                if "expectedVersion" in config else None
            self.fingerprint = config["fingerprint"] \
                if "fingerprint" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.issued_cert_id = config["issuedCertId"] \
                if "issuedCertId" in config else None
            self.last_broker_connect_time = config["lastBrokerConnectTime"] \
                if "lastBrokerConnectTime" in config else None
            self.last_broker_connect_time_duration = config["lastBrokerConnectTimeDuration"] \
                if "lastBrokerConnectTimeDuration" in config else None
            self.last_broker_disconnect_time = config["lastBrokerDisconnectTime"] \
                if "lastBrokerDisconnectTime" in config else None
            self.last_broker_disconnect_time_duration = config["lastBrokerDisconnectTimeDuration"] \
                if "lastBrokerDisconnectTimeDuration" in config else None
            self.last_o_s_upgrade_time = config["lastOSUpgradeTime"] \
                if "lastOSUpgradeTime" in config else None
            self.last_sarge_upgrade_time = config["lastSargeUpgradeTime"] \
                if "lastSargeUpgradeTime" in config else None
            self.last_upgrade_time = config["lastUpgradeTime"] \
                if "lastUpgradeTime" in config else None
            self.latitude = config["latitude"] \
                if "latitude" in config else None
            self.location = config["location"] \
                if "location" in config else None
            self.longitude = config["longitude"] \
                if "longitude" in config else None
            self.master_last_sync_time = config["masterLastSyncTime"] \
                if "masterLastSyncTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.provisioning_key_id = config["provisioningKeyId"] \
                if "provisioningKeyId" in config else None
            self.provisioning_key_name = config["provisioningKeyName"] \
                if "provisioningKeyName" in config else None
            self.os_upgrade_enabled = config["osUpgradeEnabled"] \
                if "osUpgradeEnabled" in config else None
            self.os_upgrade_status = config["osUpgradeStatus"] \
                if "osUpgradeStatus" in config else None
            self.platform = config["platform"] \
                if "platform" in config else None
            self.platform_detail = config["platformDetail"] \
                if "platformDetail" in config else None
            self.platform_version = config["platformVersion"] \
                if "platformVersion" in config else None
            self.previous_version = config["previousVersion"] \
                if "previousVersion" in config else None
            self.private_ip = config["privateIp"] \
                if "privateIp" in config else None
            self.public_ip = config["publicIp"] \
                if "publicIp" in config else None
            self.read_only = config["readOnly"] \
                if "readOnly" in config else None
            self.restriction_type = config["restrictionType"] \
                if "restrictionType" in config else None

            self.runtime_os = (
                config.get("runtime_os")  # ← used by the converted keys
                or config.get("runtimeOs")  # ← if not snake_cased
                or config.get("runtimeOS")  # ← raw from the API
                or False  # ← fallback
            )
            self.sarge_upgrade_attempt = config["sargeUpgradeAttempt"] \
                if "sargeUpgradeAttempt" in config else None
            self.sarge_upgrade_status = config["sargeUpgradeStatus"] \
                if "sargeUpgradeStatus" in config else None
            self.sarge_version = config["sargeVersion"] \
                if "sargeVersion" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] \
                if "microtenantName" in config else None
            self.shard_last_sync_time = config["shardLastSyncTime"] \
                if "shardLastSyncTime" in config else None
            self.enrollment_cert = config["enrollmentCert"] \
                if "enrollmentCert" in config else None
            self.private_cloud_controller_group_id = config["privateCloudControllerGroupId"] \
                if "privateCloudControllerGroupId" in config else None
            self.private_cloud_controller_group_name = config["privateCloudControllerGroupName"] \
                if "privateCloudControllerGroupName" in config else None
            self.site_sp_dns_name = config["siteSpDnsName"] \
                if "siteSpDnsName" in config else None
            self.upgrade_attempt = config["upgradeAttempt"] \
                if "upgradeAttempt" in config else None
            self.upgrade_status = config["upgradeStatus"] \
                if "upgradeStatus" in config else None
            self.userdb_last_sync_time = config["userdbLastSyncTime"] \
                if "userdbLastSyncTime" in config else None
            self.zscaler_managed = config["zscalerManaged"] \
                if "zscalerManaged" in config else None

            self.ip_acl = ZscalerCollection.form_list(
                config["ipAcl"] if "ipAcl" in config else [], str
            )
            self.listen_ips = ZscalerCollection.form_list(
                config["listenIps"] if "listenIps" in config else [], str
            )
            self.publish_ips = ZscalerCollection.form_list(
                config["publishIps"] if "publishIps" in config else [], str
            )

            if "privateCloudControllerVersion" in config:
                if isinstance(config["privateCloudControllerVersion"], PrivateCloudcontrollerVersion):
                    self.private_cloud_controller_version = config["privateCloudControllerVersion"]
                elif config["privateCloudControllerVersion"] is not None:
                    self.private_cloud_controller_version = PrivateCloudcontrollerVersion(
                        config["privateCloudControllerVersion"])
                else:
                    self.private_cloud_controller_version = None
            else:
                self.private_cloud_controller_version = None

            self.zpn_sub_module_upgrade_list = ZscalerCollection.form_list(
                config["zpnSubModuleUpgrade"] if "zpnSubModuleUpgrade" in config else [], ZPNSubmoduleUpgradeList
            )

        else:
            self.application_start_time = None
            self.control_channel_status = None
            self.creation_time = None
            self.ctrl_broker_name = None
            self.current_version = None
            self.description = None
            self.enabled = None
            self.expected_sarge_version = None
            self.expected_upgrade_time = None
            self.expected_version = None
            self.fingerprint = None
            self.id = None
            self.ip_acl = []
            self.issued_cert_id = None
            self.last_broker_connect_time = None
            self.last_broker_connect_time_duration = None
            self.last_broker_disconnect_time = None
            self.last_broker_disconnect_time_duration = None
            self.last_o_s_upgrade_time = None
            self.last_sarge_upgrade_time = None
            self.last_upgrade_time = None
            self.latitude = None
            self.listen_ips = []
            self.location = None
            self.longitude = None
            self.master_last_sync_time = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.provisioning_key_id = None
            self.provisioning_key_name = None
            self.os_upgrade_enabled = None
            self.os_upgrade_status = None
            self.platform = None
            self.platform_detail = None
            self.platform_version = None
            self.previous_version = None
            self.private_ip = None
            self.public_ip = None
            self.publish_ips = []
            self.read_only = None
            self.restriction_type = None
            self.runtime_os = None
            self.sarge_upgrade_attempt = None
            self.sarge_upgrade_status = None
            self.sarge_version = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.shard_last_sync_time = None
            self.enrollment_cert = None
            self.private_cloud_controller_group_id = None
            self.private_cloud_controller_group_name = None
            self.private_cloud_controller_version = None
            self.site_sp_dns_name = None
            self.upgrade_attempt = None
            self.upgrade_status = None
            self.userdb_last_sync_time = None
            self.zpn_sub_module_upgrade_list = []
            self.zscaler_managed = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "applicationStartTime": self.application_start_time,
            "controlChannelStatus": self.control_channel_status,
            "creationTime": self.creation_time,
            "ctrlBrokerName": self.ctrl_broker_name,
            "currentVersion": self.current_version,
            "description": self.description,
            "enabled": self.enabled,
            "expectedSargeVersion": self.expected_sarge_version,
            "expectedUpgradeTime": self.expected_upgrade_time,
            "expectedVersion": self.expected_version,
            "fingerprint": self.fingerprint,
            "id": self.id,
            "ipAcl": self.ip_acl,
            "issuedCertId": self.issued_cert_id,
            "lastBrokerConnectTime": self.last_broker_connect_time,
            "lastBrokerConnectTimeDuration": self.last_broker_connect_time_duration,
            "lastBrokerDisconnectTime": self.last_broker_disconnect_time,
            "lastBrokerDisconnectTimeDuration": self.last_broker_disconnect_time_duration,
            "lastOSUpgradeTime": self.last_o_s_upgrade_time,
            "lastSargeUpgradeTime": self.last_sarge_upgrade_time,
            "lastUpgradeTime": self.last_upgrade_time,
            "latitude": self.latitude,
            "listenIps": self.listen_ips,
            "location": self.location,
            "longitude": self.longitude,
            "masterLastSyncTime": self.master_last_sync_time,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "provisioningKeyId": self.provisioning_key_id,
            "provisioningKeyName": self.provisioning_key_name,
            "osUpgradeEnabled": self.os_upgrade_enabled,
            "osUpgradeStatus": self.os_upgrade_status,
            "platform": self.platform,
            "platformDetail": self.platform_detail,
            "platformVersion": self.platform_version,
            "previousVersion": self.previous_version,
            "privateIp": self.private_ip,
            "publicIp": self.public_ip,
            "publishIps": self.publish_ips,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "runtimeOS": self.runtime_os,
            "sargeUpgradeAttempt": self.sarge_upgrade_attempt,
            "sargeUpgradeStatus": self.sarge_upgrade_status,
            "sargeVersion": self.sarge_version,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "shardLastSyncTime": self.shard_last_sync_time,
            "enrollmentCert": self.enrollment_cert,
            "privateCloudControllerGroupId": self.private_cloud_controller_group_id,
            "privateCloudControllerGroupName": self.private_cloud_controller_group_name,
            "privateCloudControllerVersion": self.private_cloud_controller_version,
            "siteSpDnsName": self.site_sp_dns_name,
            "upgradeAttempt": self.upgrade_attempt,
            "upgradeStatus": self.upgrade_status,
            "userdbLastSyncTime": self.userdb_last_sync_time,
            "zpnSubModuleUpgradeList": self.zpn_sub_module_upgrade_list,
            "zscalerManaged": self.zscaler_managed
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ZPNSubmoduleUpgradeList(ZscalerObject):
    """
    A class for ZPNSubmoduleUpgradeList objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ZPNSubmoduleUpgradeList model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.current_version = config["currentVersion"] \
                if "currentVersion" in config else None
            self.entity_gid = config["entityGid"] \
                if "entityGid" in config else None
            self.entity_type = config["entityType"] \
                if "entityType" in config else None
            self.expected_version = config["expectedVersion"] \
                if "expectedVersion" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.previous_version = config["previousVersion"] \
                if "previousVersion" in config else None
            self.role = config["role"] \
                if "role" in config else None
            self.upgrade_status = config["upgradeStatus"] \
                if "upgradeStatus" in config else None
            self.upgrade_time = config["upgradeTime"] \
                if "upgradeTime" in config else None
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
            "upgradeTime": self.upgrade_time
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PrivateCloudcontrollerVersion(ZscalerObject):
    """
    A class for PrivateCloudcontrollerVersion objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PrivateCloudcontrollerVersion model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.application_start_time = config["applicationStartTime"] \
                if "applicationStartTime" in config else None
            self.broker_id = config["brokerId"] \
                if "brokerId" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.ctrl_channel_status = config["ctrlChannelStatus"] \
                if "ctrlChannelStatus" in config else None
            self.current_version = config["currentVersion"] \
                if "currentVersion" in config else None
            self.disable_auto_update = config["disableAutoUpdate"] \
                if "disableAutoUpdate" in config else None
            self.expected_sarge_version = config["expectedSargeVersion"] \
                if "expectedSargeVersion" in config else None
            self.expected_version = config["expectedVersion"] \
                if "expectedVersion" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.last_connect_time = config["lastConnectTime"] \
                if "lastConnectTime" in config else None
            self.last_disconnect_time = config["lastDisconnectTime"] \
                if "lastDisconnectTime" in config else None
            self.last_o_s_upgrade_time = config["lastOSUpgradeTime"] \
                if "lastOSUpgradeTime" in config else None
            self.last_sarge_upgrade_time = config["lastSargeUpgradeTime"] \
                if "lastSargeUpgradeTime" in config else None
            self.last_upgraded_time = config["lastUpgradedTime"] \
                if "lastUpgradedTime" in config else None
            self.lone_warrior = config["loneWarrior"] \
                if "loneWarrior" in config else None
            self.master_last_sync_time = config["masterLastSyncTime"] \
                if "masterLastSyncTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.os_upgrade_enabled = config["osUpgradeEnabled"] \
                if "osUpgradeEnabled" in config else None
            self.os_upgrade_status = config["osUpgradeStatus"] \
                if "osUpgradeStatus" in config else None
            self.platform = config["platform"] \
                if "platform" in config else None
            self.platform_detail = config["platformDetail"] \
                if "platformDetail" in config else None
            self.platform_version = config["platformVersion"] \
                if "platformVersion" in config else None
            self.previous_version = config["previousVersion"] \
                if "previousVersion" in config else None
            self.private_ip = config["privateIp"] \
                if "privateIp" in config else None
            self.public_ip = config["publicIp"] \
                if "publicIp" in config else None
            self.restart_instructions = config["restartInstructions"] \
                if "restartInstructions" in config else None
            self.restart_time_in_sec = config["restartTimeInSec"] \
                if "restartTimeInSec" in config else None
            self.runtime_os = (
                config.get("runtime_os")  # ← used by the converted keys
                or config.get("runtimeOs")  # ← if not snake_cased
                or config.get("runtimeOS")  # ← raw from the API
                or False  # ← fallback
            )
            self.sarge_upgrade_attempt = config["sargeUpgradeAttempt"] \
                if "sargeUpgradeAttempt" in config else None
            self.sarge_upgrade_status = config["sargeUpgradeStatus"] \
                if "sargeUpgradeStatus" in config else None
            self.sarge_version = config["sargeVersion"] \
                if "sargeVersion" in config else None
            self.shard_last_sync_time = config["shardLastSyncTime"] \
                if "shardLastSyncTime" in config else None
            self.private_cloud_controller_group_id = config["privateCloudControllerGroupId"] \
                if "privateCloudControllerGroupId" in config else None
            self.system_start_time = config["systemStartTime"] \
                if "systemStartTime" in config else None
            self.tunnel_id = config["tunnelId"] \
                if "tunnelId" in config else None
            self.upgrade_attempt = config["upgradeAttempt"] \
                if "upgradeAttempt" in config else None
            self.upgrade_now_once = config["upgradeNowOnce"] \
                if "upgradeNowOnce" in config else None
            self.upgrade_status = config["upgradeStatus"] \
                if "upgradeStatus" in config else None
            self.userdb_last_sync_time = config["userdbLastSyncTime"] \
                if "userdbLastSyncTime" in config else None
        else:
            self.application_start_time = None
            self.broker_id = None
            self.creation_time = None
            self.ctrl_channel_status = None
            self.current_version = None
            self.disable_auto_update = None
            self.expected_sarge_version = None
            self.expected_version = None
            self.id = None
            self.last_connect_time = None
            self.last_disconnect_time = None
            self.last_o_s_upgrade_time = None
            self.last_sarge_upgrade_time = None
            self.last_upgraded_time = None
            self.lone_warrior = None
            self.master_last_sync_time = None
            self.modified_by = None
            self.modified_time = None
            self.os_upgrade_enabled = None
            self.os_upgrade_status = None
            self.platform = None
            self.platform_detail = None
            self.platform_version = None
            self.previous_version = None
            self.private_ip = None
            self.public_ip = None
            self.restart_instructions = None
            self.restart_time_in_sec = None
            self.runtime_os = None
            self.sarge_upgrade_attempt = None
            self.sarge_upgrade_status = None
            self.sarge_version = None
            self.shard_last_sync_time = None
            self.private_cloud_controller_group_id = None
            self.system_start_time = None
            self.tunnel_id = None
            self.upgrade_attempt = None
            self.upgrade_now_once = None
            self.upgrade_status = None
            self.userdb_last_sync_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "applicationStartTime": self.application_start_time,
            "brokerId": self.broker_id,
            "creationTime": self.creation_time,
            "ctrlChannelStatus": self.ctrl_channel_status,
            "currentVersion": self.current_version,
            "disableAutoUpdate": self.disable_auto_update,
            "expectedSargeVersion": self.expected_sarge_version,
            "expectedVersion": self.expected_version,
            "id": self.id,
            "lastConnectTime": self.last_connect_time,
            "lastDisconnectTime": self.last_disconnect_time,
            "lastOSUpgradeTime": self.last_o_s_upgrade_time,
            "lastSargeUpgradeTime": self.last_sarge_upgrade_time,
            "lastUpgradedTime": self.last_upgraded_time,
            "loneWarrior": self.lone_warrior,
            "masterLastSyncTime": self.master_last_sync_time,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "osUpgradeEnabled": self.os_upgrade_enabled,
            "osUpgradeStatus": self.os_upgrade_status,
            "platform": self.platform,
            "platformDetail": self.platform_detail,
            "platformVersion": self.platform_version,
            "previousVersion": self.previous_version,
            "privateIp": self.private_ip,
            "publicIp": self.public_ip,
            "restartInstructions": self.restart_instructions,
            "restartTimeInSec": self.restart_time_in_sec,
            "runtimeOS": self.runtime_os,
            "sargeUpgradeAttempt": self.sarge_upgrade_attempt,
            "sargeUpgradeStatus": self.sarge_upgrade_status,
            "sargeVersion": self.sarge_version,
            "shardLastSyncTime": self.shard_last_sync_time,
            "privateCloudControllerGroupId": self.private_cloud_controller_group_id,
            "systemStartTime": self.system_start_time,
            "tunnelId": self.tunnel_id,
            "upgradeAttempt": self.upgrade_attempt,
            "upgradeNowOnce": self.upgrade_now_once,
            "upgradeStatus": self.upgrade_status,
            "userdbLastSyncTime": self.userdb_last_sync_time
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
