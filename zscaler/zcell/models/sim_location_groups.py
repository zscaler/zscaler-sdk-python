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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject
from zscaler.zcell.models import sim_location_groups as sim_location_groups


class SimLocationGroups(ZscalerObject):
    """
    A class representing a SimLocationGroups object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.tracked_devices = ZscalerCollection.form_list(
                config["trackedDevices"] if "trackedDevices" in config else [], str
            )
        else:
            self.id = None
            self.name = None
            self.tracked_devices = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "trackedDevices": self.tracked_devices,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ResponseMessage(ZscalerObject):
    """
    A class representing a ResponseMessage object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.message = config["message"] if "message" in config else None
        else:
            self.id = None
            self.message = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "message": self.message,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GeoFence(ZscalerObject):
    """
    A class representing the geo fence of a SIM location group.

    The API spells this ``geoFenceData`` on read/update and ``geoFenceDetails`` on
    create; both carry the same shape. ``lat``/``lng``/``radius`` are fractional --
    e.g. ``{"lat": -17.687827, "lng": 52.8125, "radius": 1637864.965089}``.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.lat = config["lat"] if "lat" in config else None
            self.lng = config["lng"] if "lng" in config else None
            self.radius = config["radius"] if "radius" in config else None
        else:
            self.lat = None
            self.lng = None
            self.radius = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "lat": self.lat,
            "lng": self.lng,
            "radius": self.radius,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LinkedPolicyDetails(ZscalerObject):
    """
    A class representing a policy linked to a SIM location group.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.policy_id = config["policyId"] if "policyId" in config else None
            self.policy_name = config["policyName"] if "policyName" in config else None
            self.policy_type = config["policyType"] if "policyType" in config else None
            self.status = config["status"] if "status" in config else None
        else:
            self.policy_id = None
            self.policy_name = None
            self.policy_type = None
            self.status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "policyId": self.policy_id,
            "policyName": self.policy_name,
            "policyType": self.policy_type,
            "status": self.status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApiCreateSimLocationGroupRequestBody(ZscalerObject):
    """
    A class representing a ApiCreateSimLocationGroupRequestBody object.

    Note the create payload uses ``geoFenceDetails``, where read and update use
    ``geoFenceData``. The endpoint takes a *list* of these bodies per call.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.name = config["name"] if "name" in config else None
            self.tracked_devices = ZscalerCollection.form_list(
                config["trackedDevices"] if "trackedDevices" in config else [], str
            )
            if "geoFenceDetails" in config:
                if isinstance(config["geoFenceDetails"], sim_location_groups.GeoFence):
                    self.geo_fence_details = config["geoFenceDetails"]
                elif config["geoFenceDetails"] is not None:
                    self.geo_fence_details = sim_location_groups.GeoFence(config["geoFenceDetails"])
                else:
                    self.geo_fence_details = None
            else:
                self.geo_fence_details = None
        else:
            self.name = None
            self.tracked_devices = []
            self.geo_fence_details = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "trackedDevices": self.tracked_devices,
            "geoFenceDetails": self.geo_fence_details,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GetSimLocationGroup(ZscalerObject):
    """
    A class representing a GetSimLocationGroup object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            if "geoFenceData" in config:
                if isinstance(config["geoFenceData"], sim_location_groups.GeoFence):
                    self.geo_fence_data = config["geoFenceData"]
                elif config["geoFenceData"] is not None:
                    self.geo_fence_data = sim_location_groups.GeoFence(config["geoFenceData"])
                else:
                    self.geo_fence_data = None
            else:
                self.geo_fence_data = None
            self.linked_policies = ZscalerCollection.form_list(
                config["linkedPolicies"] if "linkedPolicies" in config else [], sim_location_groups.LinkedPolicyDetails
            )
            self.inside_and_tracked_iccids = ZscalerCollection.form_list(
                config["insideAndTrackedIccids"] if "insideAndTrackedIccids" in config else [], str
            )
            self.inside_and_untracked_iccids = ZscalerCollection.form_list(
                config["insideAndUntrackedIccids"] if "insideAndUntrackedIccids" in config else [], str
            )
            self.outside_and_tracked_iccids = ZscalerCollection.form_list(
                config["outsideAndTrackedIccids"] if "outsideAndTrackedIccids" in config else [], str
            )
        else:
            self.id = None
            self.name = None
            self.geo_fence_data = None
            self.linked_policies = []
            self.inside_and_tracked_iccids = []
            self.inside_and_untracked_iccids = []
            self.outside_and_tracked_iccids = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "geoFenceData": self.geo_fence_data,
            "linkedPolicies": [item.request_format() for item in (self.linked_policies or [])],
            "insideAndTrackedIccids": self.inside_and_tracked_iccids,
            "insideAndUntrackedIccids": self.inside_and_untracked_iccids,
            "outsideAndTrackedIccids": self.outside_and_tracked_iccids,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class UpdateSimLocationGroup(ZscalerObject):
    """
    A class representing a UpdateSimLocationGroup object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.tracked_devices = ZscalerCollection.form_list(
                config["trackedDevices"] if "trackedDevices" in config else [], str
            )
            if "geoFenceData" in config:
                if isinstance(config["geoFenceData"], sim_location_groups.GeoFence):
                    self.geo_fence_data = config["geoFenceData"]
                elif config["geoFenceData"] is not None:
                    self.geo_fence_data = sim_location_groups.GeoFence(config["geoFenceData"])
                else:
                    self.geo_fence_data = None
            else:
                self.geo_fence_data = None
        else:
            self.tracked_devices = []
            self.geo_fence_data = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "trackedDevices": self.tracked_devices,
            "geoFenceData": self.geo_fence_data,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
