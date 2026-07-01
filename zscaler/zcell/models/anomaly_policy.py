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


class AnomalyPolicy(ZscalerObject):
    """
    A class for Anomaly Policy objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Anomaly Policy model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.policy_type = config["policyType"] if "policyType" in config else None
            self.policy_name = config["policyName"] if "policyName" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None

            if "jsonData" in config:
                if isinstance(config["jsonData"], JsonData):
                    self.json_data = config["jsonData"]
                elif config["jsonData"] is not None:
                    self.json_data = JsonData(config["jsonData"])
                else:
                    self.json_data = None
            else:
                self.json_data = None

            self.running_status = config["runningStatus"] if "runningStatus" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None
            self.enabled_at = config["enabledAt"] if "enabledAt" in config else None
            self.sim_location_group_ids = ZscalerCollection.form_list(
                config["simLocationGroupIds"] if "simLocationGroupIds" in config else [], int
            )
            self.violations = config["violations"] if "violations" in config else None
        else:
            self.id = None
            self.policy_type = None
            self.policy_name = None
            self.enabled = None
            self.json_data = None
            self.running_status = None
            self.created_at = None
            self.enabled_at = None
            self.sim_location_group_ids = []
            self.violations = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "policyType": self.policy_type,
            "policyName": self.policy_name,
            "enabled": self.enabled,
            "jsonData": self.json_data,
            "runningStatus": self.running_status,
            "createdAt": self.created_at,
            "enabledAt": self.enabled_at,
            "simLocationGroupIds": self.sim_location_group_ids,
            "violations": self.violations,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class JsonData(ZscalerObject):
    """
    A class for Json Data objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Json Data model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.alerts = ZscalerCollection.form_list(config["alerts"] if "alerts" in config else [], Alerts)
            self.mvno_type = config["mvnoType"] if "mvnoType" in config else None
            self.policy_id = config["policyId"] if "policyId" in config else None
            self.tenant_id = config["tenantId"] if "tenantId" in config else None
            self.policy_name = config["policyName"] if "policyName" in config else None
            self.policy_type = config["policyType"] if "policyType" in config else None
            self.tenant_name = config["tenantName"] if "tenantName" in config else None

            if "configurations" in config:
                if isinstance(config["configurations"], JsonDataConfigurations):
                    self.configurations = config["configurations"]
                elif config["configurations"] is not None:
                    self.configurations = JsonDataConfigurations(config["configurations"])
                else:
                    self.configurations = None
            else:
                self.configurations = None
        else:
            self.alerts = []
            self.mvno_type = None
            self.policy_id = None
            self.tenant_id = None
            self.policy_name = None
            self.policy_type = None
            self.tenant_name = None
            self.configurations = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "alerts": self.alerts,
            "mvnoType": self.mvno_type,
            "policyId": self.policy_id,
            "tenantId": self.tenant_id,
            "policyName": self.policy_name,
            "policyType": self.policy_type,
            "tenantName": self.tenant_name,
            "configurations": self.configurations,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Alerts(ZscalerObject):
    """
    A class for Alerts objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Alerts model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.alert_type = config["alertType"] if "alertType" in config else None
            self.recipients = ZscalerCollection.form_list(config["recipients"] if "recipients" in config else [], str)
            self.alert_window = config["alertWindow"] if "alertWindow" in config else None
        else:
            self.alert_type = None
            self.recipients = []
            self.alert_window = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "alertType": self.alert_type,
            "recipients": self.recipients,
            "alertWindow": self.alert_window,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class JsonDataConfigurations(ZscalerObject):
    """
    A class for Json Data Configurations objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Json Data Configurations model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.geo_fence_zones = ZscalerCollection.form_list(
                config["geoFenceZones"] if "geoFenceZones" in config else [], GeoFenceZones
            )
        else:
            self.geo_fence_zones = []

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "geoFenceZones": self.geo_fence_zones,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GeoFenceZones(ZscalerObject):
    """
    A class for Geo Fence Zones objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Geo Fence Zones model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            if "center" in config:
                if isinstance(config["center"], Center):
                    self.center = config["center"]
                elif config["center"] is not None:
                    self.center = Center(config["center"])
                else:
                    self.center = None
            else:
                self.center = None

            self.radius = config["radius"] if "radius" in config else None
            self.zone_id = config["zoneId"] if "zoneId" in config else None
            self.tracked_devices = ZscalerCollection.form_list(
                config["trackedDevices"] if "trackedDevices" in config else [], TrackedDevices
            )
        else:
            self.center = None
            self.radius = None
            self.zone_id = None
            self.tracked_devices = []

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "center": self.center,
            "radius": self.radius,
            "zoneId": self.zone_id,
            "trackedDevices": self.tracked_devices,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Center(ZscalerObject):
    """
    A class for Center objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Center model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.lat = config["lat"] if "lat" in config else None
            self.lng = config["lng"] if "lng" in config else None
        else:
            self.lat = None
            self.lng = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "lat": self.lat,
            "lng": self.lng,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TrackedDevices(ZscalerObject):
    """
    A class for Tracked Devices objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Tracked Devices model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.lat = config["lat"] if "lat" in config else None
            self.lng = config["lng"] if "lng" in config else None

            if "locationInfo" in config:
                if isinstance(config["locationInfo"], LocationInfo):
                    self.location_info = config["locationInfo"]
                elif config["locationInfo"] is not None:
                    self.location_info = LocationInfo(config["locationInfo"])
                else:
                    self.location_info = None
            else:
                self.location_info = None
        else:
            self.id = None
            self.lat = None
            self.lng = None
            self.location_info = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "lat": self.lat,
            "lng": self.lng,
            "locationInfo": self.location_info,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LocationInfo(ZscalerObject):
    """
    A class for Location Info objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Location Info model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.eci = config["ECI"] if "ECI" in config else None
            self.mcc = config["MCC"] if "MCC" in config else None
            self.mnc = config["MNC"] if "MNC" in config else None
            self.tac = config["TAC"] if "TAC" in config else None
            self.type = config["type"] if "type" in config else None
        else:
            self.eci = None
            self.mcc = None
            self.mnc = None
            self.tac = None
            self.type = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ECI": self.eci,
            "MCC": self.mcc,
            "MNC": self.mnc,
            "TAC": self.tac,
            "type": self.type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GetViolationDetails(ZscalerObject):
    """
    A class for Get Violation Details objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Get Violation Details model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.policy_id = config["policyId"] if "policyId" in config else None
            self.tenant_id = config["tenantId"] if "tenantId" in config else None
            self.iccid = config["iccid"] if "iccid" in config else None
            self.imsi = config["imsi"] if "imsi" in config else None
            self.event_type = config["eventType"] if "eventType" in config else None
            self.policy_type = config["policyType"] if "policyType" in config else None
            self.zone_id = config["zoneId"] if "zoneId" in config else None
            self.timestamp = config["timestamp"] if "timestamp" in config else None

            if "eventDeviceLocation" in config:
                if isinstance(config["eventDeviceLocation"], Center):
                    self.event_device_location = config["eventDeviceLocation"]
                elif config["eventDeviceLocation"] is not None:
                    self.event_device_location = Center(config["eventDeviceLocation"])
                else:
                    self.event_device_location = None
            else:
                self.event_device_location = None

            if "policyDeviceLocation" in config:
                if isinstance(config["policyDeviceLocation"], Center):
                    self.policy_device_location = config["policyDeviceLocation"]
                elif config["policyDeviceLocation"] is not None:
                    self.policy_device_location = Center(config["policyDeviceLocation"])
                else:
                    self.policy_device_location = None
            else:
                self.policy_device_location = None
        else:
            self.policy_id = None
            self.tenant_id = None
            self.iccid = None
            self.imsi = None
            self.event_type = None
            self.policy_type = None
            self.zone_id = None
            self.timestamp = None
            self.event_device_location = None
            self.policy_device_location = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "policyId": self.policy_id,
            "tenantId": self.tenant_id,
            "iccid": self.iccid,
            "imsi": self.imsi,
            "eventType": self.event_type,
            "policyType": self.policy_type,
            "zoneId": self.zone_id,
            "timestamp": self.timestamp,
            "eventDeviceLocation": self.event_device_location,
            "policyDeviceLocation": self.policy_device_location,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AnomalyPolicyLog(ZscalerObject):
    """
    A class for Anomaly Policy objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Anomaly Policy model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.content = ZscalerCollection.form_list(
                config["content"] if "content" in config else [], AnomalyPolicyLogContent
            )
        else:
            self.content = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "content": self.content,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AnomalyPolicyLogContent(ZscalerObject):
    """
    A class for Anomaly Policy Log Content objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Anomaly Policy Log Content model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.policy_id = config["policyId"] if "policyId" in config else None
            self.message = config["message"] if "message" in config else None
            self.status = config["status"] if "status" in config else None
            self.recorded_at = config["recordedAt"] if "recordedAt" in config else None
        else:
            self.policy_id = None
            self.message = None
            self.status = None
            self.recorded_at = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "policyId": self.policy_id,
            "message": self.message,
            "status": self.status,
            "recordedAt": self.recorded_at,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
