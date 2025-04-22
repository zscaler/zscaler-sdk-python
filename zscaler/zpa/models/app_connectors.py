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


class AppConnectorController(ZscalerObject):
    """
    A class representing the App Connector Controller.
    """

    def __init__(self, config=None):
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
            self.upgrade_attempt = config["upgradeAttempt"] if "upgradeAttempt" in config else 0
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
            self.creation_time = config["creationTime"] if "creationTime" in config else 0
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else 0
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else 0
            self.last_broker_connect_time = config["lastBrokerConnectTime"] if "lastBrokerConnectTime" in config else 0
            self.last_broker_connect_time_duration = (
                config["lastBrokerConnectTimeDuration"] if "lastBrokerConnectTimeDuration" in config else None
            )
            self.last_broker_disconnect_time = (
                config["lastBrokerDisconnectTime"] if "lastBrokerDisconnectTime" in config else 0
            )
            self.last_broker_disconnect_time_duration = (
                config["lastBrokerDisconnectTimeDuration"] if "lastBrokerDisconnectTimeDuration" in config else None
            )
            self.last_upgrade_time = config["lastUpgradeTime"] if "lastUpgradeTime" in config else 0
            self.expected_upgrade_time = config["expectedUpgradeTime"] if "expectedUpgradeTime" in config else 0
            self.ctrl_broker_name = config["ctrlBrokerName"] if "ctrlBrokerName" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.enrollment_cert = config["enrollmentCert"] if "enrollmentCert" in config else None
            self.application_start_time = config["applicationStartTime"] if "applicationStartTime" in config else 0
            self.ip_acl = config["ipAcl"] if "ipAcl" in config else []
            self.zpn_sub_module_upgrade_list = config["zpnSubModuleUpgradeList"] if "zpnSubModuleUpgradeList" in config else []
            self.assistant_version = config["assistantVersion"] if "assistantVersion" in config else {}
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
            self.upgrade_attempt = 0
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
            self.creation_time = 0
            self.modified_time = 0
            self.modified_by = 0
            self.last_broker_connect_time = 0
            self.last_broker_connect_time_duration = None
            self.last_broker_disconnect_time = 0
            self.last_broker_disconnect_time_duration = None
            self.last_upgrade_time = 0
            self.expected_upgrade_time = 0
            self.ctrl_broker_name = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.enrollment_cert = None
            self.application_start_time = 0
            self.ip_acl = []
            self.zpn_sub_module_upgrade_list = []
            self.assistant_version = {}

    def request_format(self):
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
            "zpnSubModuleUpgradeList": self.zpn_sub_module_upgrade_list,
            "assistantVersion": self.assistant_version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
