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
from zscaler.zpa.models import app_connector_groups as app_connector_groups
from zscaler.zpa.models import application_segment as application_segment
from zscaler.zpa.models import common as common
from zscaler.zpa.models import policyset_controller_v2 as policyset_controller_v2
from zscaler.zpa.models import private_cloud as private_cloud
from zscaler.zpa.models import service_edge_groups as service_edge_groups


class PolicyGroup(ZscalerObject):
    """
    A class representing a PolicyGroup object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.description = config["description"] if "description" in config else None
            self.group_criteria_rule_gid = config["groupCriteriaRuleGid"] if "groupCriteriaRuleGid" in config else None
            self.group_order = config["groupOrder"] if "groupOrder" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.policy_group_set_gid = config["policyGroupSetGid"] if "policyGroupSetGid" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.type = config["type"] if "type" in config else None

            if "groupCriteriaRule" in config:
                if isinstance(config["groupCriteriaRule"], PolicyRule):
                    self.group_criteria_rule = config["groupCriteriaRule"]
                elif config["groupCriteriaRule"] is not None:
                    self.group_criteria_rule = PolicyRule(config["groupCriteriaRule"])
                else:
                    self.group_criteria_rule = None
            else:
                self.group_criteria_rule = None
        else:
            self.creation_time = None
            self.description = None
            self.group_criteria_rule = None
            self.group_criteria_rule_gid = None
            self.group_order = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.policy_group_set_gid = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "description": self.description,
            "groupCriteriaRule": self.group_criteria_rule,
            "groupCriteriaRuleGid": self.group_criteria_rule_gid,
            "groupOrder": self.group_order,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "policyGroupSetGid": self.policy_group_set_gid,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "type": self.type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PolicyRule(ZscalerObject):
    """
    A class representing a PolicyRule object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.action = config["action"] if "action" in config else None
            self.action_id = config["actionId"] if "actionId" in config else None
            self.browser_posture_profile_id = (
                config["browserPostureProfileId"] if "browserPostureProfileId" in config else None
            )
            self.browser_posture_profile_name = (
                config["browserPostureProfileName"] if "browserPostureProfileName" in config else None
            )
            self.button_text = config["buttonText"] if "buttonText" in config else None

            self.conditions = ZscalerCollection.form_list(config["conditions"] if "conditions" in config else [], ConditionSet)
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            if "credential" in config:
                if isinstance(config["credential"], common.CommonIDName):
                    self.credential = config["credential"]
                elif config["credential"] is not None:
                    self.credential = common.CommonIDName(config["credential"])
                else:
                    self.credential = None
            else:
                self.credential = None
            if "credentialPool" in config:
                if isinstance(config["credentialPool"], common.CommonIDName):
                    self.credential_pool = config["credentialPool"]
                elif config["credentialPool"] is not None:
                    self.credential_pool = common.CommonIDName(config["credentialPool"])
                else:
                    self.credential_pool = None
            else:
                self.credential_pool = None
            self.custom_msg = config["customMsg"] if "customMsg" in config else None
            self.default_rule = config["defaultRule"] if "defaultRule" in config else False
            self.default_rule_name = config["defaultRuleName"] if "defaultRuleName" in config else None
            self.description = config["description"] if "description" in config else None
            self.desktop_policy_mappings = ZscalerCollection.form_list(
                config["desktopPolicyMappings"] if "desktopPolicyMappings" in config else [], common.DesktopPolicyMappingsDTO
            )
            self.device_posture_failure_notification_enabled = (
                config["devicePostureFailureNotificationEnabled"]
                if "devicePostureFailureNotificationEnabled" in config
                else False
            )
            self.disabled = config["disabled"] if "disabled" in config else None
            if "extranetDTO" in config:
                if isinstance(config["extranetDTO"], common.ExtranetDTO):
                    self.extranet_dto = config["extranetDTO"]
                elif config["extranetDTO"] is not None:
                    self.extranet_dto = common.ExtranetDTO(config["extranetDTO"])
                else:
                    self.extranet_dto = None
            else:
                self.extranet_dto = None
            self.extranet_enabled = config["extranetEnabled"] if "extranetEnabled" in config else False
            self.group_id = config["groupId"] if "groupId" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.name_without_trim = config["nameWithoutTrim"] if "nameWithoutTrim" in config else None
            self.operator = config["operator"] if "operator" in config else None
            self.policy_group_name = config["policyGroupName"] if "policyGroupName" in config else None
            self.policy_set_id = config["policySetId"] if "policySetId" in config else None
            self.policy_type = config["policyType"] if "policyType" in config else None
            self.post_action_types = ZscalerCollection.form_list(
                config["postActionTypes"] if "postActionTypes" in config else [], str
            )
            self.post_actions = config["postActions"] if "postActions" in config else None
            self.priority = config["priority"] if "priority" in config else None

            if "privilegedCapabilities" in config:
                if isinstance(config["privilegedCapabilities"], common.PrivilegedCapabilitiesResource):
                    self.privileged_capabilities = config["privilegedCapabilities"]
                elif config["privilegedCapabilities"] is not None:
                    self.privileged_capabilities = common.PrivilegedCapabilitiesResource(config["privilegedCapabilities"])
                else:
                    self.privileged_capabilities = None
            else:
                self.privileged_capabilities = None

            if "privilegedPortalCapabilities" in config:
                if isinstance(config["privilegedPortalCapabilities"], common.PrivilegedCapabilitiesResource):
                    self.privileged_portal_capabilities = config["privilegedPortalCapabilities"]
                elif config["privilegedPortalCapabilities"] is not None:
                    self.privileged_portal_capabilities = common.PrivilegedCapabilitiesResource(
                        config["privilegedPortalCapabilities"]
                    )
                else:
                    self.privileged_portal_capabilities = None
            else:
                self.privileged_portal_capabilities = None
            self.read_only = config["readOnly"] if "readOnly" in config else False
            self.reauth_idle_timeout = config["reauthIdleTimeout"] if "reauthIdleTimeout" in config else None
            self.reauth_timeout = config["reauthTimeout"] if "reauthTimeout" in config else None
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.rule_order = config["ruleOrder"] if "ruleOrder" in config else None
            self.rule_type = config["ruleType"] if "ruleType" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.service_edge_groups = ZscalerCollection.form_list(
                config["serviceEdgeGroups"] if "serviceEdgeGroups" in config else [], service_edge_groups.ServiceEdgeGroup
            )
            self.url = config["url"] if "url" in config else None
            self.zpn_isolation_profile_id = config["zpnIsolationProfileId"] if "zpnIsolationProfileId" in config else None
            self.zpn_inspection_profile_id = config["zpnInspectionProfileId"] if "zpnInspectionProfileId" in config else None
            self.zpn_inspection_profile_name = (
                config["zpnInspectionProfileName"] if "zpnInspectionProfileName" in config else None
            )
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else False
        else:
            self.action = None
            self.action_id = None
            self.app_server_groups = []
            self.app_connector_groups = []
            self.browser_posture_profile_id = None
            self.browser_posture_profile_name = None
            self.button_text = None
            self.conditions = []
            self.creation_time = None
            self.credential = None
            self.credential_pool = None
            self.custom_msg = None
            self.default_rule = False
            self.default_rule_name = None
            self.description = None
            self.desktop_policy_mappings = []
            self.device_posture_failure_notification_enabled = False
            self.disabled = None
            self.extranet_dto = None
            self.extranet_enabled = False
            self.group_id = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.name_without_trim = None
            self.operator = None
            self.policy_group_name = None
            self.policy_set_id = None
            self.policy_type = None
            self.post_action_types = []
            self.post_actions = None
            self.priority = None
            self.privileged_capabilities = None
            self.privileged_portal_capabilities = None
            self.read_only = False
            self.reauth_idle_timeout = None
            self.reauth_timeout = None
            self.restriction_type = None
            self.rule_order = None
            self.rule_type = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.service_edge_groups = []
            self.url = None
            self.zpn_isolation_profile_id = None
            self.zpn_inspection_profile_id = None
            self.zpn_inspection_profile_name = None
            self.zscaler_managed = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "actionId": self.action_id,
            "browserPostureProfileId": self.browser_posture_profile_id,
            "browserPostureProfileName": self.browser_posture_profile_name,
            "buttonText": self.button_text,
            "conditions": [item.request_format() for item in (self.conditions or [])],
            "creationTime": self.creation_time,
            "credential": self.credential,
            "credentialPool": self.credential_pool,
            "customMsg": self.custom_msg,
            "defaultRule": self.default_rule,
            "defaultRuleName": self.default_rule_name,
            "description": self.description,
            "desktopPolicyMappings": [mapping.request_format() for mapping in self.desktop_policy_mappings],
            "devicePostureFailureNotificationEnabled": self.device_posture_failure_notification_enabled,
            "disabled": self.disabled,
            "extranetDTO": self.extranet_dto,
            "extranetEnabled": self.extranet_enabled,
            "groupId": self.group_id,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "nameWithoutTrim": self.name_without_trim,
            "operator": self.operator,
            "policyGroupName": self.policy_group_name,
            "policySetId": self.policy_set_id,
            "policyType": self.policy_type,
            "postActionTypes": self.post_action_types,
            "postActions": self.post_actions,
            "priority": self.priority,
            "privilegedCapabilities": self.privileged_capabilities,
            "privilegedPortalCapabilities": self.privileged_portal_capabilities,
            "readOnly": self.read_only,
            "reauthIdleTimeout": self.reauth_idle_timeout,
            "reauthTimeout": self.reauth_timeout,
            "restrictionType": self.restriction_type,
            "ruleOrder": self.rule_order,
            "ruleType": self.rule_type,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "url": self.url,
            "zpnIsolationProfileId": self.zpn_isolation_profile_id,
            "zpnInspectionProfileId": self.zpn_inspection_profile_id,
            "zpnInspectionProfileName": self.zpn_inspection_profile_name,
            "zscalerManaged": self.zscaler_managed,
            "appConnectorGroups": [group.request_format() for group in self.app_connector_groups],
            "appServerGroups": [group.request_format() for group in self.app_server_groups],
            "serviceEdgeGroups": [group.request_format() for group in self.service_edge_groups],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ConditionSet(ZscalerObject):
    """
    A class representing a ConditionSet object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.negated = config["negated"] if "negated" in config else False
            self.operands = ZscalerCollection.form_list(
                config["operands"] if "operands" in config else [], policyset_controller_v2.OperandResource
            )
            self.operator = config["operator"] if "operator" in config else None
            self.policy_set_type = config["policySetType"] if "policySetType" in config else None
            self.rule_gid = config["ruleGid"] if "ruleGid" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
        else:
            self.creation_time = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.negated = False
            self.operands = []
            self.operator = None
            self.policy_set_type = None
            self.rule_gid = None
            self.microtenant_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "negated": self.negated,
            "operands": [item.request_format() for item in (self.operands or [])],
            "operator": self.operator,
            "policySetType": self.policy_set_type,
            "ruleGid": self.rule_gid,
            "microtenantId": self.microtenant_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
