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

from zscaler.zia.models import admin_users as admin_users
from zscaler.zia.models import device_groups as device_groups
from zscaler.zia.models import devices as devices
from zscaler.zia.models import cloud_browser_isolation as isolation
from zscaler.zia.models import cloud_firewall_source_groups as cloud_firewall_source_groups
from zscaler.zia.models import cloud_firewall_time_windows as time_windows
from zscaler.zia.models import location_group as location_group
from zscaler.zia.models import location_management as location
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import urlcategory as urlcategory
from zscaler.zia.models import rule_labels as labels
from zscaler.zia.models import workload_groups as workload_groups
from zscaler.zia.models import common as common


class URLFilteringRule(ZscalerObject):
    """
    A class representing a URL Filtering Rule object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.order = config["order"] if "order" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.state = config["state"] if "state" in config else None
            self.end_user_notification_url = config["endUserNotificationUrl"] if "endUserNotificationUrl" in config else None
            self.block_override = config["blockOverride"] if "blockOverride" in config else False
            self.time_quota = config["timeQuota"] if "timeQuota" in config else 0
            self.size_quota = config["sizeQuota"] if "sizeQuota" in config else 0
            self.description = config["description"] if "description" in config else None
            self.validity_start_time = config["validityStartTime"] if "validityStartTime" in config else None
            self.validity_end_time = config["validityEndTime"] if "validityEndTime" in config else None
            self.validity_time_zone_id = config["validityTimeZoneId"] if "validityTimeZoneId" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.enforce_time_validity = config["enforceTimeValidity"] if "enforceTimeValidity" in config else False
            self.action = config["action"] if "action" in config else None
            self.ciparule = config["ciparule"] if "ciparule" in config else False

            # Handling lists of simple values
            self.protocols = ZscalerCollection.form_list(config["protocols"] if "protocols" in config else [], str)
            self.user_agent_types = ZscalerCollection.form_list(
                config["userAgentTypes"] if "userAgentTypes" in config else [], str
            )
            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], str
            )
            self.url_categories2 = ZscalerCollection.form_list(
                config["urlCategories2"] if "urlCategories2" in config else [], str
            )
            self.request_methods = ZscalerCollection.form_list(
                config["requestMethods"] if "requestMethods" in config else [], str
            )
            self.device_trust_levels = ZscalerCollection.form_list(
                config["deviceTrustLevels"] if "deviceTrustLevels" in config else [], str
            )
            self.user_risk_score_levels = ZscalerCollection.form_list(
                config["userRiskScoreLevels"] if "userRiskScoreLevels" in config else [], str
            )
            # Handling nested objects and lists of objects
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location.LocationManagement
            )
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], user_management.Groups)
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            self.workload_groups = ZscalerCollection.form_list(
                config["workloadGroups"] if "workloadGroups" in config else [], workload_groups.WorkloadGroups
            )
            self.override_users = ZscalerCollection.form_list(
                config["overrideUsers"] if "overrideUsers" in config else [], user_management.UserManagement
            )
            self.override_groups = ZscalerCollection.form_list(
                config["overrideGroups"] if "overrideGroups" in config else [], user_management.Groups
            )
            self.location_groups = ZscalerCollection.form_list(
                config["locationGroups"] if "locationGroups" in config else [], location_group.LocationGroup
            )
            self.source_ip_groups = ZscalerCollection.form_list(
                config["sourceIpGroups"] if "sourceIpGroups" in config else [], cloud_firewall_source_groups.IPSourceGroup
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], labels.RuleLabels)
            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )

            # Handling nested single object for CBIProfile
            self.cbi_profile = isolation.CBIProfile(config["cbiProfile"]) if "cbiProfile" in config else None

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
            # Defaults if config is None
            self.id = None
            self.name = None
            self.order = None
            self.rank = None
            self.state = None
            self.end_user_notification_url = None
            self.block_override = False
            self.time_quota = 0
            self.size_quota = 0
            self.description = None
            self.validity_start_time = None
            self.validity_end_time = None
            self.validity_time_zone_id = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.enforce_time_validity = False
            self.action = None
            self.ciparule = False
            self.protocols = []
            self.user_agent_types = []
            self.url_categories = []
            self.url_categories2 = []
            self.request_methods = []
            self.device_trust_levels = []
            self.locations = []
            self.groups = []
            self.departments = []
            self.users = []
            self.time_windows = []
            self.workload_groups = []
            self.override_users = []
            self.override_groups = []
            self.location_groups = []
            self.labels = []
            self.devices = []
            self.device_groups = []
            self.user_risk_score_levels = []
            self.source_ip_groups = []
            self.cbi_profile = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "rank": self.rank,
            "state": self.state,
            "endUserNotificationUrl": self.end_user_notification_url,
            "blockOverride": self.block_override,
            "timeQuota": self.time_quota,
            "sizeQuota": self.size_quota,
            "description": self.description,
            "validityStartTime": self.validity_start_time,
            "validityEndTime": self.validity_end_time,
            "validityTimeZoneId": self.validity_time_zone_id,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "enforceTimeValidity": self.enforce_time_validity,
            "action": self.action,
            "ciparule": self.ciparule,
            "protocols": self.protocols,
            "userAgentTypes": self.user_agent_types,
            "urlCategories": self.url_categories,
            "urlCategories2": self.url_categories2,
            "requestMethods": self.request_methods,
            "deviceTrustLevels": self.device_trust_levels,
            "userRiskScoreLevels": self.user_risk_score_levels,
            "sourceIpGroups": [group.request_format() for group in (self.source_ip_groups or [])],
            "locations": [location.request_format() for location in (self.locations or [])],
            "groups": [group.request_format() for group in self.groups],
            "departments": [department.request_format() for department in (self.departments or [])],
            "users": [user.request_format() for user in self.users],
            "timeWindows": [window.request_format() for window in (self.time_windows or [])],
            "workloadGroups": [group.request_format() for group in (self.workload_groups or [])],
            "overrideUsers": [user.request_format() for user in (self.override_users or [])],
            "overrideGroups": [group.request_format() for group in (self.override_groups or [])],
            "locationGroups": [group.request_format() for group in (self.location_groups or [])],
            "labels": [label.request_format() for label in (self.labels or [])],
            "devices": [device.request_format() for device in (self.devices or [])],
            "deviceGroups": [group.request_format() for group in (self.device_groups or [])],
            "cbiProfile": self.cbi_profile.request_format() if self.cbi_profile else None,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
