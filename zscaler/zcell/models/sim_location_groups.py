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


class ApiCreateSimLocationGroupRequestBody(ZscalerObject):
    """
    A class representing a ApiCreateSimLocationGroupRequestBody object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            pass
        else:
            pass

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {}
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
