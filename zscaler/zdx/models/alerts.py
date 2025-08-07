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
from zscaler.zdx.models import common as common


class Alerts(ZscalerObject):
    """
    A class for ongoing alert rules across an organization objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ongoing alert rules across an organization model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.next_offset = config["next_offset"] if "next_offset" in config else None

            self.alerts = ZscalerCollection.form_list(
                config["alerts"] if "alerts" in config else [], AlertDetails
            )
        else:
            self.next_offset = None
            self.alerts = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "next_offset": self.next_offset,
            "alerts": self.alerts,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


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
            self.started_on = config["started_on"] if "started_on" in config else None
            self.ended_on = config["ended_on"] if "ended_on" in config else None

            if "application" in config:
                if isinstance(config["application"], common.CommonIDName):
                    self.application = config["application"]
                elif config["application"] is not None:
                    self.application = common.CommonIDName(config["application"])
                else:
                    self.application = None
            else:
                self.application = None

            self.geolocations = ZscalerCollection.form_list(

                config["geolocations"] if "geolocations" in config else [], common.GeoLocations
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], common.Departments
            )
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], common.Locations
            )

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


class AffectedDevices(ZscalerObject):
    """
    A class for affected devices associated with an alert rule objects.
    """

    def __init__(self, config=None):
        """
        Initialize the affected devices associated with an alert rule model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.next_offset = config["next_offset"] if "next_offset" in config else None

            self.devices = ZscalerCollection.form_list(
                config["devices"] if "devices" in config else [], DeviceDetails
            )
        else:
            self.next_offset = None
            self.devices = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "next_offset": self.next_offset,
            "devices": self.devices,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceDetails(ZscalerObject):
    """
    A class for affected devices associated with an alert rule objects.
    """

    def __init__(self, config=None):
        """
        Initialize the affected devices associated with an alert rule model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.userid = config["userid"] if "userid" in config else None
            self.user_name = config["userName"] if "userName" in config else None
            self.user_email = config["userEmail"] if "userEmail" in config else None
        else:
            self.id = None
            self.name = None
            self.userid = None
            self.user_name = None
            self.user_email = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "userid": self.userid,
            "userName": self.user_name,
            "userEmail": self.user_email,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
