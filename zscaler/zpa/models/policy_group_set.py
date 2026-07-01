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


class PolicyGroupSet(ZscalerObject):
    """
    A class representing a PolicyGroupSet object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.custom_policy_group_gids = ZscalerCollection.form_list(
                config["customPolicyGroupGids"] if "customPolicyGroupGids" in config else [], str
            )
            self.default_policy_group_gid = config["defaultPolicyGroupGid"] if "defaultPolicyGroupGid" in config else None
            self.global_policy_group_gid = config["globalPolicyGroupGid"] if "globalPolicyGroupGid" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.policy_type = config["policyType"] if "policyType" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
        else:
            self.creation_time = None
            self.custom_policy_group_gids = []
            self.default_policy_group_gid = None
            self.global_policy_group_gid = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.policy_type = None
            self.microtenant_id = None
            self.microtenant_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "customPolicyGroupGids": self.custom_policy_group_gids,
            "defaultPolicyGroupGid": self.default_policy_group_gid,
            "globalPolicyGroupGid": self.global_policy_group_gid,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "policyType": self.policy_type,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PolicyGroupSetSummary(ZscalerObject):
    """
    A class representing a PolicyGroupSetSummary object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.group_count_excluding_global = (
                config["groupCountExcludingGlobal"] if "groupCountExcludingGlobal" in config else None
            )
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.policy_group_summary_list = ZscalerCollection.form_list(
                config["policyGroupSummaryList"] if "policyGroupSummaryList" in config else [], PolicyGroupSummary
            )
            self.policy_type = config["policyType"] if "policyType" in config else None
        else:
            self.group_count_excluding_global = None
            self.id = None
            self.name = None
            self.policy_group_summary_list = []
            self.policy_type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "groupCountExcludingGlobal": self.group_count_excluding_global,
            "id": self.id,
            "name": self.name,
            "policyGroupSummaryList": [item.request_format() for item in (self.policy_group_summary_list or [])],
            "policyType": self.policy_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PolicyGroupSetSummaryStat(ZscalerObject):
    """
    A class representing a PolicyGroupSetSummaryStat object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.disabled_rules = config["disabledRules"] if "disabledRules" in config else None
            self.enabled_rules = config["enabledRules"] if "enabledRules" in config else None
            self.total_policy_groups = config["totalPolicyGroups"] if "totalPolicyGroups" in config else None
            self.total_rules = config["totalRules"] if "totalRules" in config else None
        else:
            self.disabled_rules = None
            self.enabled_rules = None
            self.total_policy_groups = None
            self.total_rules = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "disabledRules": self.disabled_rules,
            "enabledRules": self.enabled_rules,
            "totalPolicyGroups": self.total_policy_groups,
            "totalRules": self.total_rules,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PolicyGroupSummary(ZscalerObject):
    """
    A class representing a PolicyGroupSummary object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.group_criteria_count = config["groupCriteriaCount"] if "groupCriteriaCount" in config else None
            self.group_order = config["groupOrder"] if "groupOrder" in config else None
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.rule_count = config["ruleCount"] if "ruleCount" in config else None
            self.type = config["type"] if "type" in config else None
        else:
            self.group_criteria_count = None
            self.group_order = None
            self.id = None
            self.name = None
            self.rule_count = None
            self.type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "groupCriteriaCount": self.group_criteria_count,
            "groupOrder": self.group_order,
            "id": self.id,
            "name": self.name,
            "ruleCount": self.rule_count,
            "type": self.type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
