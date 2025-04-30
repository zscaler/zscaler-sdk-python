# flake8: noqa
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
from zscaler.zia.models import device_groups as device_groups
from zscaler.zia.models import devices as devices
from zscaler.zia.models import location_management as location_management
from zscaler.zia.models import location_group as location_group
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import rule_labels as rule_labels
from zscaler.zia.models import cloud_firewall_time_windows as time_windows
from zscaler.zia.models import workload_groups as workload_groups
from zscaler.zia.models import common as common_reference
from zscaler.zia.models import common


class FileTypeControlRules(ZscalerObject):
    """
    A class for FileTypeControlRules objects.
    """

    def __init__(self, config=None):
        """
        Initialize the FileTypeControlRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.protocols = ZscalerCollection.form_list(config["protocols"] if "protocols" in config else [], str)
            self.order = config["order"] if "order" in config else None
            self.time_quota = config["timeQuota"] if "timeQuota" in config else None
            self.size_quota = config["sizeQuota"] if "sizeQuota" in config else None
            self.description = config["description"] if "description" in config else None
            self.min_size = config["minSize"] if "minSize" in config else 0
            self.max_size = config["maxSize"] if "maxSize" in config else 0
            self.filtering_action = config["filteringAction"] if "filteringAction" in config else None
            self.capture_pcap = config["capturePCAP"] if "capturePCAP" in config else False
            self.operation = config["operation"] if "operation" in config else None
            self.active_content = config["activeContent"] if "activeContent" in config else False
            self.unscannable = config["unscannable"] if "unscannable" in config else False
            self.state = config["state"] if "state" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.access_control = config["accessControl"] if "accessControl" in config else None
            self.name = config["name"] if "name" in config else None

            self.device_trust_levels = ZscalerCollection.form_list(
                config["deviceTrustLevels"] if "deviceTrustLevels" in config else [], str
            )
            self.cloud_applications = ZscalerCollection.form_list(
                config["cloudApplications"] if "cloudApplications" in config else [], str
            )
            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], str
            )
            self.file_types = ZscalerCollection.form_list(config["fileTypes"] if "fileTypes" in config else [], str)
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.location_groups = ZscalerCollection.form_list(
                config["locationGroups"] if "locationGroups" in config else [], location_group.LocationGroup
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], user_management.Groups)
            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], rule_labels.RuleLabels)

            self.zpa_app_segments = ZscalerCollection.form_list(
                config["zpaAppSegments"] if "zpaAppSegments" in config else [], common_reference.ResourceReference
            )

            # Handle nested CommonBlocks for last_modified_by
            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

        else:
            self.id = None
            self.protocols = []
            self.order = None
            self.time_quota = None
            self.size_quota = None
            self.description = None
            self.locations = []
            self.location_groups = []
            self.groups = []
            self.departments = []
            self.users = []
            self.url_categories = []
            self.file_types = []
            self.devices = []
            self.device_groups = []
            self.device_trust_levels = []
            self.min_size = 0
            self.max_size = 0
            self.filtering_action = None
            self.capture_pcap = None
            self.operation = None
            self.active_content = None
            self.unscannable = None
            self.state = None
            self.time_windows = []
            self.rank = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.access_control = None
            self.name = None
            self.labels = []
            self.zpa_app_segments = []
            self.cloud_applications = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "protocols": self.protocols,
            "order": self.order,
            "timeQuota": self.time_quota,
            "sizeQuota": self.size_quota,
            "description": self.description,
            "locations": [loc.request_format() for loc in (self.locations or [])],
            "locationGroups": [loc_group.request_format() for loc_group in (self.location_groups or [])],
            "departments": [dept.request_format() for dept in (self.departments or [])],
            "groups": [group.request_format() for group in (self.groups or [])],
            "users": [user.request_format() for user in (self.users or [])],
            "devices": [device.request_format() for device in (self.devices or [])],
            "deviceGroups": [dg.request_format() for dg in (self.device_groups or [])],
            "timeWindows": [window.request_format() for window in (self.time_windows or [])],
            "labels": [label.request_format() for label in (self.labels or [])],
            "zpaAppSegments": [zpa.request_format() for zpa in (self.zpa_app_segments or [])],
            "urlCategories": self.url_categories,
            "fileTypes": self.file_types,
            "deviceTrustLevels": self.device_trust_levels,
            "minSize": self.min_size,
            "maxSize": self.max_size,
            "filteringAction": self.filtering_action,
            "capturePCAP": self.capture_pcap,
            "operation": self.operation,
            "activeContent": self.active_content,
            "unscannable": self.unscannable,
            "state": self.state,
            "rank": self.rank,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "accessControl": self.access_control,
            "name": self.name,
            "cloudApplications": self.cloud_applications,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
