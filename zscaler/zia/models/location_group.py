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


class LocationGroup(ZscalerObject):
    """
    A class representing a Location Group object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.group_type = config["groupType"] if "groupType" in config else None
            self.comments = config["comments"] if "comments" in config else None
            self.last_mod_time = config["lastModTime"] if "lastModTime" in config else None
            self.predefined = config["predefined"] if "predefined" in config else False

            # Explicit handling of dynamicLocationGroupCriteria with profiles list
            if "dynamicLocationGroupCriteria" in config:
                if "profiles" in config["dynamicLocationGroupCriteria"]:
                    self.dynamic_location_group_criteria = {
                        "profiles": ZscalerCollection.form_list(config["dynamicLocationGroupCriteria"]["profiles"], str)
                    }
                else:
                    self.dynamic_location_group_criteria = {"profiles": []}
            else:
                self.dynamic_location_group_criteria = None

            # Explicit handling of nested list of locations
            self.locations = []
            if "locations" in config:
                for location in config["locations"]:
                    if isinstance(location, dict):
                        self.locations.append(location)
        else:
            self.id = None
            self.name = None
            self.group_type = None
            self.comments = None
            self.last_mod_time = None
            self.predefined = False
            self.dynamic_location_group_criteria = None
            self.locations = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "groupType": self.group_type,
            "comments": self.comments,
            "lastModTime": self.last_mod_time,
            "predefined": self.predefined,
            "dynamicLocationGroupCriteria": (
                self.dynamic_location_group_criteria if self.dynamic_location_group_criteria else None
            ),
            "locations": [{"id": location["id"], "name": location["name"]} for location in self.locations],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
