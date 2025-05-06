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
from zscaler.zia.models import location_management as location_management
from zscaler.zia.models import location_group as location_group
from zscaler.zia.models import rule_labels as rule_labels
from zscaler.zia.models import cloud_firewall_time_windows as time_windows
from zscaler.zia.models import bandwidth_classes as bandwidth_classes
from zscaler.zia.models import common


class BandwidthControlRules(ZscalerObject):
    """
    A class for BandwidthControlRules objects.
    """

    def __init__(self, config=None):
        """
        Initialize the BandwidthControlRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None

            self.name = config["name"] if "name" in config else None

            self.order = config["order"] if "order" in config else None

            self.state = config["state"] if "state" in config else None

            self.description = config["description"] if "description" in config else None

            self.max_bandwidth = config["maxBandwidth"] if "maxBandwidth" in config else None

            self.min_bandwidth = config["minBandwidth"] if "minBandwidth" in config else None

            self.rank = config["rank"] if "rank" in config else None

            self.access_control = config["accessControl"] if "accessControl" in config else None

            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None

            self.protocols = ZscalerCollection.form_list(config["protocols"] if "protocols" in config else [], str)

            self.bandwidth_classes = ZscalerCollection.form_list(
                config["bandwidthClasses"] if "bandwidthClasses" in config else [], bandwidth_classes.BandwidthClasses
            )

            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.location_groups = ZscalerCollection.form_list(
                config["locationGroups"] if "locationGroups" in config else [], location_group.LocationGroup
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], rule_labels.RuleLabels)

            self.default_rule = config["defaultRule"] if "defaultRule" in config else None
        else:
            self.id = None
            self.name = None
            self.order = None
            self.state = None
            self.locations = []
            self.time_windows = []
            self.description = None
            self.protocols = []
            self.location_groups = []
            self.max_bandwidth = None
            self.min_bandwidth = None
            self.bandwidth_classes = []
            self.rank = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.access_control = None
            self.labels = []
            self.default_rule = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "state": self.state,
            "rank": self.rank,
            "locations": self.locations,
            "timeWindows": self.time_windows,
            "description": self.description,
            "protocols": self.protocols,
            "locationGroups": self.location_groups,
            "maxBandwidth": self.max_bandwidth,
            "minBandwidth": self.min_bandwidth,
            "bandwidthClasses": self.bandwidth_classes,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "accessControl": self.access_control,
            "labels": self.labels,
            "defaultRule": self.default_rule,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
