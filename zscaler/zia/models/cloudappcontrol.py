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
from zscaler.zia.models import common as common_reference
from zscaler.zia.models import device_groups as device_groups
from zscaler.zia.models import devices as devices
from zscaler.zia.models import cloud_browser_isolation as isolation
from zscaler.zia.models import cloud_firewall_source_groups as cloud_firewall_source_groups
from zscaler.zia.models import cloud_firewall_time_windows as time_windows
from zscaler.zia.models import location_group as location_group
from zscaler.zia.models import location_management as location
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import rule_labels as labels
from zscaler.zia.models import workload_groups as workload_groups


class CloudApplicationControl(ZscalerObject):
    """
    A class representing a Cloud Application Control Policy object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.type = config["type"] if "type" in config else None
            self.order = config["order"] if "order" in config else None
            self.access_control = config["accessControl"] if "accessControl" in config else None
            self.time_quota = config["timeQuota"] if "timeQuota" in config else 0
            self.size_quota = config["sizeQuota"] if "sizeQuota" in config else 0
            self.description = config["description"] if "description" in config else None
            self.state = config["state"] if "state" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.validity_start_time = config["validityStartTime"] if "validityStartTime" in config else None
            self.validity_end_time = config["validityEndTime"] if "validityEndTime" in config else None
            self.validity_time_zone_id = config["validityTimeZoneId"] if "validityTimeZoneId" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.last_modified_by = config["lastModifiedBy"] if "lastModifiedBy" in config else None
            self.enforce_time_validity = config["enforceTimeValidity"] if "enforceTimeValidity" in config else False
            self.eun_enabled = config["eunEnabled"] if "eunEnabled" in config else False
            self.eun_template_id = config["eunTemplateId"] if "eunTemplateId" in config else None
            self.browser_eun_template_id = config["browserEunTemplateId"] if "browserEunTemplateId" in config else None
            self.cascading_enabled = config["cascadingEnabled"] if "cascadingEnabled" in config else False
            self.predefined = config["predefined"] if "predefined" in config else False

            # Handling lists of simple values
            self.actions = ZscalerCollection.form_list(config["actions"] if "actions" in config else [], str)
            self.user_agent_types = ZscalerCollection.form_list(
                config["userAgentTypes"] if "userAgentTypes" in config else [], str
            )
            self.device_trust_levels = ZscalerCollection.form_list(
                config["deviceTrustLevels"] if "deviceTrustLevels" in config else [], str
            )
            self.user_risk_score_levels = ZscalerCollection.form_list(
                config["userRiskScoreLevels"] if "userRiskScoreLevels" in config else [], str
            )

            self.applications = ZscalerCollection.form_list(config["applications"] if "applications" in config else [], str)

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

            self.location_groups = ZscalerCollection.form_list(
                config["locationGroups"] if "locationGroups" in config else [], location_group.LocationGroup
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], labels.RuleLabels)
            self.cloud_app_instances = ZscalerCollection.form_list(
                config["cloudAppInstances"] if "cloudAppInstances" in config else [], CloudAppInstance
            )
            self.tenancy_profile_ids = ZscalerCollection.form_list(
                config["tenancyProfileIds"] if "tenancyProfileIds" in config else [], common_reference.ResourceReference
            )
            self.sharing_domain_profiles = ZscalerCollection.form_list(
                config["sharingDomainProfiles"] if "sharingDomainProfiles" in config else [],
                common_reference.ResourceReference,
            )
            self.form_sharing_domain_profiles = ZscalerCollection.form_list(
                config["formSharingDomainProfiles"] if "formSharingDomainProfiles" in config else [],
                common_reference.ResourceReference,
            )
            self.cloud_app_risk_profile = ZscalerCollection.form_list(
                config["cloudAppRiskProfile"] if "cloudAppRiskProfile" in config else [], common_reference.ResourceReference
            )

            # Assign the cbi_profile as-is; conversions are handled by ZscalerObject
            self.cbi_profile = config.get("cbiProfile", {})

        else:
            # Defaults if config is None
            self.id = None
            self.name = None
            self.type = None
            self.order = None
            self.access_control = None
            self.time_quota = 0
            self.size_quota = 0
            self.description = None
            self.state = None
            self.rank = None
            self.validity_start_time = None
            self.validity_end_time = None
            self.validity_time_zone_id = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.enforce_time_validity = False
            self.eun_enabled = False
            self.eun_template_id = None
            self.browser_eun_template_id = None
            self.cascading_enabled = False
            self.predefined = False
            self.actions = []
            self.user_agent_types = []
            self.device_trust_levels = []
            self.user_risk_score_levels = []
            self.locations = []
            self.groups = []
            self.departments = []
            self.users = []
            self.applications = []
            self.location_groups = []
            self.time_windows = []
            self.devices = []
            self.device_groups = []
            self.tenancy_profile_ids = []
            self.labels = []
            self.cloud_app_instances = []
            self.sharing_domain_profiles = []
            self.form_sharing_domain_profiles = []
            self.cloud_app_risk_profile = None
            self.cbi_profile = {}

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "order": self.order,
            "accessControl": self.access_control,
            "timeQuota": self.time_quota,
            "sizeQuota": self.size_quota,
            "description": self.description,
            "state": self.state,
            "rank": self.rank,
            "validityStartTime": self.validity_start_time,
            "validityEndTime": self.validity_end_time,
            "validityTimeZoneId": self.validity_time_zone_id,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "enforceTimeValidity": self.enforce_time_validity,
            "eunEnabled": self.eun_enabled,
            "eunTemplateId": self.eun_template_id,
            "browserEunTemplateId": self.browser_eun_template_id,
            "cascadingEnabled": self.cascading_enabled,
            "predefined": self.predefined,
            "actions": self.actions,
            "userAgentTypes": self.user_agent_types,
            "deviceTrustLevels": self.device_trust_levels,
            "userRiskScoreLevels": self.user_risk_score_levels,
            "applications": self.applications,
            "locations": [loc.request_format() for loc in (self.locations or [])],
            "groups": [grp.request_format() for grp in (self.groups or [])],
            "departments": [dept.request_format() for dept in (self.departments or [])],
            "users": [usr.request_format() for usr in (self.users or [])],
            "locationGroups": [lg.request_format() for lg in (self.location_groups or [])],
            "timeWindows": [tw.request_format() for tw in (self.time_windows or [])],
            "devices": [dev.request_format() for dev in (self.devices or [])],
            "deviceGroups": [dg.request_format() for dg in (self.device_groups or [])],
            "tenancyProfileIds": [tp.request_format() for tp in (self.tenancy_profile_ids or [])],
            "labels": [label.request_format() for label in (self.labels or [])],
            "cloudAppInstances": [inst.request_format() for inst in (self.cloud_app_instances or [])],
            "sharingDomainProfiles": [sdp.request_format() for sdp in (self.sharing_domain_profiles or [])],
            "formSharingDomainProfiles": [fsdp.request_format() for fsdp in (self.form_sharing_domain_profiles or [])],
            "cloudAppRiskProfile": self.cloud_app_risk_profile.request_format() if self.cloud_app_risk_profile else None,
            "cbiProfile": self.cbi_profile.request_format() if self.cbi_profile else None,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


# USED IN /webApplicationRules/{rule_type}/availableActions
class Application(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)
        self.val = config["val"] if "val" in config else None
        self.web_application_class = config["webApplicationClass"] if "webApplicationClass" in config else None
        self.backend_name = config["backendName"] if "backendName" in config else None
        self.original_name = config["originalName"] if "originalName" in config else None
        self.name = config["name"] if "name" in config else None
        self.deprecated = config["deprecated"] if "deprecated" in config else False
        self.misc = config["misc"] if "misc" in config else False
        self.app_not_ready = config["appNotReady"] if "appNotReady" in config else False
        self.under_migration = config["underMigration"] if "underMigration" in config else False
        self.app_cat_modified = config["appCatModified"] if "appCatModified" in config else False

    def request_format(self):
        return {
            "val": self.val,
            "webApplicationClass": self.web_application_class,
            "backendName": self.backend_name,
            "originalName": self.original_name,
            "name": self.name,
            "deprecated": self.deprecated,
            "misc": self.misc,
            "appNotReady": self.app_not_ready,
            "underMigration": self.under_migration,
            "appCatModified": self.app_cat_modified,
        }


class CloudAppInstance(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)
        self.id = config["id"] if "id" in config else None
        self.name = config["name"] if "name" in config else None
        self.type = config["type"] if "type" in config else None

    def request_format(self):
        return {"id": self.id, "name": self.name, "type": self.type}
