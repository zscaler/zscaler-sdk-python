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
from zscaler.zia.models import common as common_reference


class SandboxRules(ZscalerObject):
    """
    A class for SandboxRules objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SandboxRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.protocols = ZscalerCollection.form_list(config["protocols"] if "protocols" in config else [], str)
            self.order = config["order"] if "order" in config else None
            self.ba_policy_categories = ZscalerCollection.form_list(
                config["baPolicyCategories"] if "baPolicyCategories" in config else [], str
            )
            self.description = config["description"] if "description" in config else None
            # self.cbi_profile = config["cbiProfile"] \
            #     if "cbiProfile" in config else None
            # self.cbi_profile_id = config["cbiProfileId"] \
            #     if "cbiProfileId" in config else None
            self.state = config["state"] if "state" in config else None

            self.rank = config["rank"] if "rank" in config else None
            # self.last_modified_time = config["lastModifiedTime"] \
            #     if "lastModifiedTime" in config else None
            # self.last_modified_by = config["lastModifiedBy"] \
            #     if "lastModifiedBy" in config else None
            # self.access_control = config["accessControl"] \
            #     if "accessControl" in config else None
            self.ba_rule_action = config["baRuleAction"] if "baRuleAction" in config else None
            self.first_time_enable = config["firstTimeEnable"] if "firstTimeEnable" in config else False
            self.first_time_operation = config["firstTimeOperation"] if "firstTimeOperation" in config else None
            self.ml_action_enabled = config["mlActionEnabled"] if "mlActionEnabled" in config else False

            self.by_threat_score = config["byThreatScore"] if "byThreatScore" in config else None
            # self.default_rule = config["defaultRule"] \
            #     if "defaultRule" in config else False

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
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], rule_labels.RuleLabels)
            self.zpa_app_segments = ZscalerCollection.form_list(
                config["zpaAppSegments"] if "zpaAppSegments" in config else [], common_reference.ResourceReference
            )
            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], str
            )
            self.file_types = ZscalerCollection.form_list(config["fileTypes"] if "fileTypes" in config else [], str)

        else:
            self.id = None
            self.name = None
            self.protocols = []
            self.order = None
            self.ba_policy_categories = []
            self.description = None
            self.locations = []
            self.location_groups = []
            self.groups = []
            self.departments = []
            self.users = []
            self.url_categories = []
            self.file_types = []
            # self.cbi_profile = None
            # self.cbi_profile_id = None
            self.state = None
            self.rank = None
            # self.last_modified_time = None
            # self.last_modified_by = None
            # self.access_control = None
            self.ba_rule_action = None
            self.first_time_enable = None
            self.first_time_operation = None
            self.ml_action_enabled = None
            self.labels = []
            self.zpa_app_segments = []
            self.by_threat_score = None
            # self.default_rule = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "protocols": self.protocols,
            "order": self.order,
            "baPolicyCategories": self.ba_policy_categories,
            "description": self.description,
            "urlCategories": self.url_categories,
            "fileTypes": self.file_types,
            # "cbiProfile": self.cbi_profile,
            # "cbiProfileId": self.cbi_profile_id,
            "state": self.state,
            "rank": self.rank,
            # "lastModifiedTime": self.last_modified_time,
            # "lastModifiedBy": self.last_modified_by,
            # "accessControl": self.access_control,
            "baRuleAction": self.ba_rule_action,
            "firstTimeEnable": self.first_time_enable,
            "firstTimeOperation": self.first_time_operation,
            "mlActionEnabled": self.ml_action_enabled,
            "byThreatScore": self.by_threat_score,
            # "defaultRule": self.default_rule,
            "locations": [loc.request_format() for loc in (self.locations or [])],
            "locationGroups": [loc_group.request_format() for loc_group in (self.location_groups or [])],
            "departments": [dept.request_format() for dept in (self.departments or [])],
            "groups": [group.request_format() for group in (self.groups or [])],
            "users": [user.request_format() for user in (self.users or [])],
            "labels": [label.request_format() for label in (self.labels or [])],
            "zpaAppSegments": [zpa.request_format() for zpa in (self.zpa_app_segments or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
