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


class Device(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the Device model based on API response.

        Args:
            config (dict): A dictionary representing the Device configuration.
        """
        super().__init__(config)

        if config:
            self.agent_version = config["agentVersion"] if "agentVersion" in config else None
            self.company_name = config["companyName"] if "companyName" in config else None
            self.config_download_time = config["config_download_time"] if "config_download_time" in config else None
            self.deregistration_timestamp = config["deregistrationTimestamp"] if "deregistrationTimestamp" in config else None
            self.detail = config["detail"] if "detail" in config else None
            self.download_count = config["download_count"] if "download_count" in config else None
            self.hardware_fingerprint = config["hardwareFingerprint"] if "hardwareFingerprint" in config else None
            self.keep_alive_time = config["keepAliveTime"] if "keepAliveTime" in config else None
            self.last_seen_time = config["last_seen_time"] if "last_seen_time" in config else None
            self.mac_address = config["macAddress"] if "macAddress" in config else None
            self.machine_hostname = config["machineHostname"] if "machineHostname" in config else None
            self.manufacturer = config["manufacturer"] if "manufacturer" in config else None
            self.os_version = config["osVersion"] if "osVersion" in config else None
            self.owner = config["owner"] if "owner" in config else None
            self.policy_name = config["policyName"] if "policyName" in config else None
            self.registration_state = config["registrationState"] if "registrationState" in config else None
            self.registration_time = config["registration_time"] if "registration_time" in config else None
            self.state = config["state"] if "state" in config else None
            self.tunnel_version = config["tunnelVersion"] if "tunnelVersion" in config else None
            self.type = config["type"] if "type" in config else None
            self.udid = config["udid"] if "udid" in config else None
            self.upm_version = config["upmVersion"] if "upmVersion" in config else None
            self.user = config["user"] if "user" in config else None
            self.vpn_state = config["vpnState"] if "vpnState" in config else None
            self.zapp_arch = config["zappArch"] if "zappArch" in config else None

        else:
            self.agent_version = None
            self.company_name = None
            self.config_download_time = None
            self.deregistration_timestamp = None
            self.detail = None
            self.download_count = None
            self.hardware_fingerprint = None
            self.keep_alive_time = None
            self.last_seen_time = None
            self.mac_address = None
            self.machine_hostname = None
            self.manufacturer = None
            self.os_version = None
            self.owner = None
            self.policy_name = None
            self.registration_state = None
            self.registration_time = None
            self.state = None
            self.tunnel_version = None
            self.type = None
            self.udid = None
            self.upm_version = None
            self.user = None
            self.vpn_state = None
            self.zapp_arch = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "agentVersion": self.agent_version,
            "companyName": self.company_name,
            "config_download_time": self.config_download_time,
            "deregistrationTimestamp": self.deregistration_timestamp,
            "detail": self.detail,
            "download_count": self.download_count,
            "hardwareFingerprint": self.hardware_fingerprint,
            "keepAliveTime": self.keep_alive_time,
            "last_seen_time": self.last_seen_time,
            "macAddress": self.mac_address,
            "machineHostname": self.machine_hostname,
            "manufacturer": self.manufacturer,
            "osVersion": self.os_version,
            "owner": self.owner,
            "policyName": self.policy_name,
            "registrationState": self.registration_state,
            "registration_time": self.registration_time,
            "state": self.state,
            "tunnelVersion": self.tunnel_version,
            "type": self.type,
            "udid": self.udid,
            "upmVersion": self.upm_version,
            "user": self.user,
            "vpnState": self.vpn_state,
            "zappArch": self.zapp_arch,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ForceRemoveDevices(ZscalerObject):
    """
    A class for ForceRemoveDevices objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ForceRemoveDevices model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.client_connector_version = ZscalerCollection.form_list(
                config["clientConnectorVersion"] if "clientConnectorVersion" in config else [], str
            )
            self.os_type = config["osType"] if "osType" in config else None
            self.udids = ZscalerCollection.form_list(config["udids"] if "udids" in config else [], str)
            self.username = config["username"] if "username" in config else None
            self.devices_removed = config["devicesRemoved"] if "devicesRemoved" in config else None
            self.error_msg = config["errorMsg"] if "errorMsg" in config else None
        else:
            self.client_connector_version = ZscalerCollection.form_list([], str)
            self.os_type = None
            self.udids = ZscalerCollection.form_list([], str)
            self.username = None
            self.devices_removed = None
            self.error_msg = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "clientConnectorVersion": self.client_connector_version,
            "osType": self.os_type,
            "udids": self.udids,
            "username": self.username,
            "devicesRemoved": self.devices_removed,
            "errorMsg": self.error_msg,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SetDeviceCleanupInfo(ZscalerObject):
    """
    A class for SetDeviceCleanupInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SetDeviceCleanupInfo model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.auto_purge_days = config["autoPurgeDays"] if "autoPurgeDays" in config else None
            self.auto_removal_days = config["autoRemovalDays"] if "autoRemovalDays" in config else None
            self.company_id = config["companyId"] if "companyId" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.device_exceed_limit = config["deviceExceedLimit"] if "deviceExceedLimit" in config else None
            self.edited_by = config["editedBy"] if "editedBy" in config else None
            self.force_remove_type = config["forceRemoveType"] if "forceRemoveType" in config else None
            self.force_remove_type_string = config["forceRemoveTypeString"] if "forceRemoveTypeString" in config else None
            self.id = config["id"] if "id" in config else None
        else:
            self.active = None
            self.auto_purge_days = None
            self.auto_removal_days = None
            self.company_id = None
            self.created_by = None
            self.device_exceed_limit = None
            self.edited_by = None
            self.force_remove_type = None
            self.force_remove_type_string = None
            self.id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "autoPurgeDays": self.auto_purge_days,
            "autoRemovalDays": self.auto_removal_days,
            "companyId": self.company_id,
            "createdBy": self.created_by,
            "deviceExceedLimit": self.device_exceed_limit,
            "editedBy": self.edited_by,
            "forceRemoveType": self.force_remove_type,
            "forceRemoveTypeString": self.force_remove_type_string,
            "id": self.id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceCleanup(ZscalerObject):
    """
    A class for DeviceCleanup objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceCleanup model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] \
                if "active" in config else None
            self.auto_purge_days = config["autoPurgeDays"] \
                if "autoPurgeDays" in config else None
            self.auto_removal_days = config["autoRemovalDays"] \
                if "autoRemovalDays" in config else None
            self.company_id = config["companyId"] \
                if "companyId" in config else None
            self.created_by = config["createdBy"] \
                if "createdBy" in config else None
            self.device_exceed_limit = config["deviceExceedLimit"] \
                if "deviceExceedLimit" in config else None
            self.edited_by = config["editedBy"] \
                if "editedBy" in config else None
            self.force_remove_type = config["forceRemoveType"] \
                if "forceRemoveType" in config else None
            self.force_remove_type_string = config["forceRemoveTypeString"] \
                if "forceRemoveTypeString" in config else None
            self.id = config["id"] \
                if "id" in config else None
        else:
            self.active = None
            self.auto_purge_days = None
            self.auto_removal_days = None
            self.company_id = None
            self.created_by = None
            self.device_exceed_limit = None
            self.edited_by = None
            self.force_remove_type = None
            self.force_remove_type_string = None
            self.id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "autoPurgeDays": self.auto_purge_days,
            "autoRemovalDays": self.auto_removal_days,
            "companyId": self.company_id,
            "createdBy": self.created_by,
            "deviceExceedLimit": self.device_exceed_limit,
            "editedBy": self.edited_by,
            "forceRemoveType": self.force_remove_type,
            "forceRemoveTypeString": self.force_remove_type_string,
            "id": self.id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceDetails(ZscalerObject):
    """
    A class for DevicedDeviceDetailsetails objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceDetails model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.agent_version = config["agent_version"] \
                if "agent_version" in config else None
            self.carrier = config["carrier"] \
                if "carrier" in config else None
            self.config_download_time = config["config_download_time"] \
                if "config_download_time" in config else None
            self.deregistration_time = config["deregistration_time"] \
                if "deregistration_time" in config else None
            self.device_policy_name = config["devicePolicyName"] \
                if "devicePolicyName" in config else None
            self.device_locale = config["device_locale"] \
                if "device_locale" in config else None
            self.download_count = config["download_count"] \
                if "download_count" in config else None
            self.external_model = config["external_model"] \
                if "external_model" in config else None
            self.hardware_fingerprint = config["hardwareFingerprint"] \
                if "hardwareFingerprint" in config else None
            self.keep_alive_time = config["keep_alive_time"] \
                if "keep_alive_time" in config else None
            self.last_seen_time = config["last_seen_time"] \
                if "last_seen_time" in config else None
            self.mac_address = config["mac_address"] \
                if "mac_address" in config else None
            self.machine_hostname = config["machineHostname"] \
                if "machineHostname" in config else None
            self.manufacturer = config["manufacturer"] \
                if "manufacturer" in config else None
            self.os_version = config["os_version"] \
                if "os_version" in config else None
            self.owner = config["owner"] \
                if "owner" in config else None
            self.registration_time = config["registration_time"] \
                if "registration_time" in config else None
            self.rooted = config["rooted"] \
                if "rooted" in config else None
            self.state = config["state"] \
                if "state" in config else None
            self.tunnel_version = config["tunnelVersion"] \
                if "tunnelVersion" in config else None
            self.type = config["type"] \
                if "type" in config else None
            self.unique_id = config["unique_id"] \
                if "unique_id" in config else None
            self.upm_version = config["upmVersion"] \
                if "upmVersion" in config else None
            self.user_name = config["user_name"] \
                if "user_name" in config else None
            self.zad_version = config["zadVersion"] \
                if "zadVersion" in config else None
            self.zapp_arch = config["zappArch"] \
                if "zappArch" in config else None
        else:
            self.agent_version = None
            self.carrier = None
            self.config_download_time = None
            self.deregistration_time = None
            self.device_policy_name = None
            self.device_locale = None
            self.download_count = None
            self.external_model = None
            self.hardware_fingerprint = None
            self.keep_alive_time = None
            self.last_seen_time = None
            self.mac_address = None
            self.machine_hostname = None
            self.manufacturer = None
            self.os_version = None
            self.owner = None
            self.registration_time = None
            self.rooted = None
            self.state = None
            self.tunnel_version = None
            self.type = None
            self.unique_id = None
            self.upm_version = None
            self.user_name = None
            self.zad_version = None
            self.zapp_arch = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "agent_version": self.agent_version,
            "carrier": self.carrier,
            "config_download_time": self.config_download_time,
            "deregistration_time": self.deregistration_time,
            "devicePolicyName": self.device_policy_name,
            "device_locale": self.device_locale,
            "download_count": self.download_count,
            "external_model": self.external_model,
            "hardwareFingerprint": self.hardware_fingerprint,
            "keep_alive_time": self.keep_alive_time,
            "last_seen_time": self.last_seen_time,
            "mac_address": self.mac_address,
            "machineHostname": self.machine_hostname,
            "manufacturer": self.manufacturer,
            "os_version": self.os_version,
            "owner": self.owner,
            "registration_time": self.registration_time,
            "rooted": self.rooted,
            "state": self.state,
            "tunnelVersion": self.tunnel_version,
            "type": self.type,
            "unique_id": self.unique_id,
            "upmVersion": self.upm_version,
            "user_name": self.user_name,
            "zadVersion": self.zad_version,
            "zappArch": self.zapp_arch
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
