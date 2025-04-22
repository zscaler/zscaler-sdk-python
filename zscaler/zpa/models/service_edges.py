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


class ServiceEdge(ZscalerObject):
    """
    A class representing the Service Edge.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.fingerprint = config["fingerprint"] if "fingerprint" in config else None
            self.issued_cert_id = config["issuedCertId"] if "issuedCertId" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.location = config["location"] if "location" in config else None
            self.expected_version = config["expectedVersion"] if "expectedVersion" in config else None
            self.current_version = config["currentVersion"] if "currentVersion" in config else None
            self.expected_upgrade_time = config["expectedUpgradeTime"] if "expectedUpgradeTime" in config else None
            self.upgrade_status = config["upgradeStatus"] if "upgradeStatus" in config else None
            self.upgrade_attempt = config["upgradeAttempt"] if "upgradeAttempt" in config else 0
            self.control_channel_status = config["controlChannelStatus"] if "controlChannelStatus" in config else None
            self.ctrl_broker_name = config["ctrlBrokerName"] if "ctrlBrokerName" in config else None
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
            self.private_ip = config["privateIp"] if "privateIp" in config else None
            self.public_ip = config["publicIp"] if "publicIp" in config else None
            self.platform = config["platform"] if "platform" in config else None
            self.runtime_os = config["runtimeOS"] if "runtimeOS" in config else None
            self.application_start_time = config["applicationStartTime"] if "applicationStartTime" in config else None
            self.sarge_version = config["sargeVersion"] if "sargeVersion" in config else None
            self.platform_detail = config["platformDetail"] if "platformDetail" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.provisioning_key_id = config["provisioningKeyId"] if "provisioningKeyId" in config else None
            self.provisioning_key_name = config["provisioningKeyName"] if "provisioningKeyName" in config else None
            self.service_edge_group_id = config["serviceEdgeGroupId"] if "serviceEdgeGroupId" in config else None
            self.service_edge_group_name = config["serviceEdgeGroupName"] if "serviceEdgeGroupName" in config else None
            self.enrollment_cert = (
                config["enrollmentCert"]["name"] if "enrollmentCert" in config and "name" in config["enrollmentCert"] else None
            )

            # Handling the nested zpnSubModuleUpgradeList using ZscalerCollection
            self.zpn_sub_module_upgrade_list = ZscalerCollection.form_list(config.get("zpnSubModuleUpgradeList", []), dict)
        else:
            self.id = None
            self.name = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.fingerprint = None
            self.issued_cert_id = None
            self.enabled = True
            self.latitude = None
            self.longitude = None
            self.location = None
            self.expected_version = None
            self.current_version = None
            self.expected_upgrade_time = None
            self.upgrade_status = None
            self.upgrade_attempt = 0
            self.control_channel_status = None
            self.ctrl_broker_name = None
            self.last_broker_connect_time = None
            self.last_broker_connect_time_duration = None
            self.last_broker_disconnect_time = None
            self.last_broker_disconnect_time_duration = None
            self.private_ip = None
            self.public_ip = None
            self.platform = None
            self.runtime_os = None
            self.application_start_time = None
            self.sarge_version = None
            self.platform_detail = None
            self.microtenant_name = None
            self.microtenant_id = None
            self.provisioning_key_id = None
            self.provisioning_key_name = None
            self.service_edge_group_id = None
            self.service_edge_group_name = None
            self.enrollment_cert = None
            self.zpn_sub_module_upgrade_list = []

    def request_format(self):
        """
        Formats the Service Edge data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "fingerprint": self.fingerprint,
            "issuedCertId": self.issued_cert_id,
            "enabled": self.enabled,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location": self.location,
            "expectedVersion": self.expected_version,
            "currentVersion": self.current_version,
            "expectedUpgradeTime": self.expected_upgrade_time,
            "upgradeStatus": self.upgrade_status,
            "upgradeAttempt": self.upgrade_attempt,
            "controlChannelStatus": self.control_channel_status,
            "ctrlBrokerName": self.ctrl_broker_name,
            "lastBrokerConnectTime": self.last_broker_connect_time,
            "lastBrokerConnectTimeDuration": self.last_broker_connect_time_duration,
            "lastBrokerDisconnectTime": self.last_broker_disconnect_time,
            "lastBrokerDisconnectTimeDuration": self.last_broker_disconnect_time_duration,
            "privateIp": self.private_ip,
            "publicIp": self.public_ip,
            "platform": self.platform,
            "runtimeOS": self.runtime_os,
            "applicationStartTime": self.application_start_time,
            "sargeVersion": self.sarge_version,
            "platformDetail": self.platform_detail,
            "microtenantName": self.microtenant_name,
            "microtenantId": self.microtenant_id,
            "provisioningKeyId": self.provisioning_key_id,
            "provisioningKeyName": self.provisioning_key_name,
            "serviceEdgeGroupId": self.service_edge_group_id,
            "serviceEdgeGroupName": self.service_edge_group_name,
            "enrollmentCert": {"name": self.enrollment_cert} if self.enrollment_cert else None,
            "zpnSubModuleUpgradeList": self.zpn_sub_module_upgrade_list,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
