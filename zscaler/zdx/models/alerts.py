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
from zscaler.zdx.models import common as common_reference


class Alerts(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the Alerts model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        print(f"DEBUG: Raw config received in Alerts: {config}")  # Debugging input

        if config:
            self.id = config.get("id")
            self.rule_name = config.get("ruleName")
            self.severity = config.get("severity")
            self.alert_type = config.get("alertType")
            self.alert_status = config.get("alertStatus")
            self.application = config.get("application")
            self.num_geolocations = config.get("numGeolocations")
            self.num_devices = config.get("numDevices")
            self.started_on = config.get("startedOn")
            self.ended_on = config.get("endedOn")

        # print(f"DEBUG: Parsed Alerts object - id: {self.id}, rule_name: {self.rule_name}, alert_type: {self.alert_type}")

    def as_dict(self):
        """
        Ensure this method correctly returns the alert data.
        """
        alert_dict = {
            "id": self.id,
            "rule_name": self.rule_name,
            "severity": self.severity,
            "alert_type": self.alert_type,
            "alert_status": self.alert_status,
            "application": self.application,
            "num_geolocations": self.num_geolocations,
            "num_devices": self.num_devices,
            "started_on": self.started_on,
            "ended_on": self.ended_on,
        }
        # print(f"DEBUG: as_dict() output: {alert_dict}")  # ✅ Debugging as_dict()
        return alert_dict


class AlertDetails(ZscalerObject):
    """
    A class for AlertDetails objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AlertDetails model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.rule_name = config["rule_name"] if "rule_name" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.alert_type = config["alert_type"] if "alert_type" in config else None
            self.alert_status = config["alert_status"] if "alert_status" in config else None
            self.application = config["application"] if "application" in config else None
            self.geolocations = ZscalerCollection.form_list(
                config["geolocations"] if "geolocations" in config else [], common_reference.GeoLocations
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], common_reference.Departments
            )
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], common_reference.Locations
            )
            self.started_on = config["started_on"] if "started_on" in config else None
            self.ended_on = config["ended_on"] if "ended_on" in config else None
        else:
            self.id = None
            self.rule_name = None
            self.severity = None
            self.alert_type = None
            self.alert_status = None
            self.application = None
            self.geolocations = []
            self.departments = []
            self.locations = []
            self.started_on = None
            self.ended_on = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "rule_name": self.rule_name,
            "severity": self.severity,
            "alert_type": self.alert_type,
            "alert_status": self.alert_status,
            "application": self.application,
            "geolocations": self.geolocations,
            "departments": self.departments,
            "locations": self.locations,
            "started_on": self.started_on,
            "ended_on": self.ended_on,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
