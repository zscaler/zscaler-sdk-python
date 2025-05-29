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


class WeightedLBConfig(ZscalerObject):
    """
    A class for WeightedLBConfig objects.
    """

    def __init__(self, config=None):
        """
        Initialize the WeightedLBConfig model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.application_id = config["applicationId"] \
                if "applicationId" in config else None

            self.weighted_load_balancing = config["weightedLoadBalancing"] \
                if "weightedLoadBalancing" in config else None

            self.application_to_server_group_mappings = ZscalerCollection.form_list(
                config["applicationToServerGroupMappings"] if
                "applicationToServerGroupMappings" in config else [], ApplicationToServerGroupMappings
            )
        else:
            self.application_id = None
            self.application_to_server_group_mappings = []
            self.weighted_load_balancing = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "applicationId": self.application_id,
            "applicationToServerGroupMappings": self.application_to_server_group_mappings,
            "weightedLoadBalancing": self.weighted_load_balancing
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationToServerGroupMappings(ZscalerObject):
    """
    A class for ApplicationToServerGroupMappings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ApplicationToServerGroupMappings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.passive = config["passive"] \
                if "passive" in config else None
            self.weight = config["weight"] \
                if "weight" in config else None
        else:
            self.id = None
            self.name = None
            self.passive = None
            self.weight = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "passive": self.passive,
            "weight": self.weight
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
