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

from typing import Any, Dict, Optional

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject
from zscaler.zpa.models import app_connector_groups as app_connector_groups
from zscaler.zpa.models import common as common
from zscaler.zpa.models import policyset_controller_v2 as policyset_controller_v2
from zscaler.zpa.models import server_group as server_group
from zscaler.zpa.models import service_edge_groups as service_edge_groups


class PolicyGroup(ZscalerObject):
    """
    A class for PolicyGroup objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the PolicyGroup model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
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
                if isinstance(config["groupCriteriaRule"], GroupCriteriaRule):
                    self.group_criteria_rule = config["groupCriteriaRule"]
                elif config["groupCriteriaRule"] is not None:
                    self.group_criteria_rule = GroupCriteriaRule(config["groupCriteriaRule"])
                else:
                    self.group_criteria_rule = None
            else:
                self.group_criteria_rule = None
        else:
            self.creation_time = None
            self.description = None
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
            self.group_criteria_rule = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "description": self.description,
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
            "groupCriteriaRule": self.group_criteria_rule,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GroupCriteriaRule(ZscalerObject):
    """
    A class for GroupCriteriaRule objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the GroupCriteriaRule model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
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
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.custom_msg = config["customMsg"] if "customMsg" in config else None
            self.default_rule = config["defaultRule"] if "defaultRule" in config else None
            self.default_rule_name = config["defaultRuleName"] if "defaultRuleName" in config else None
            self.description = config["description"] if "description" in config else None
            self.device_posture_failure_notification_enabled = (
                config["devicePostureFailureNotificationEnabled"]
                if "devicePostureFailureNotificationEnabled" in config
                else None
            )
            self.disabled = config["disabled"] if "disabled" in config else None
            self.extranet_enabled = config["extranetEnabled"] if "extranetEnabled" in config else None
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
            self.post_actions = config["postActions"] if "postActions" in config else None
            self.priority = config["priority"] if "priority" in config else None
            self.read_only = config["readOnly"] if "readOnly" in config else None
            self.reauth_idle_timeout = config["reauthIdleTimeout"] if "reauthIdleTimeout" in config else None
            self.reauth_timeout = config["reauthTimeout"] if "reauthTimeout" in config else None
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.rule_order = config["ruleOrder"] if "ruleOrder" in config else None
            self.rule_type = config["ruleType"] if "ruleType" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.url = config["url"] if "url" in config else None
            self.zpn_isolation_profile_id = config["zpnIsolationProfileId"] if "zpnIsolationProfileId" in config else None
            self.zpn_inspection_profile_id = config["zpnInspectionProfileId"] if "zpnInspectionProfileId" in config else None
            self.zpn_inspection_profile_name = (
                config["zpnInspectionProfileName"] if "zpnInspectionProfileName" in config else None
            )
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else None
            self.app_server_groups = ZscalerCollection.form_list(
                config["appServerGroups"] if "appServerGroups" in config else [], server_group.ServerGroup
            )
            self.app_connector_groups = ZscalerCollection.form_list(
                config["appConnectorGroups"] if "appConnectorGroups" in config else [], app_connector_groups.AppConnectorGroup
            )
            self.conditions = ZscalerCollection.form_list(config["conditions"] if "conditions" in config else [], Condition)
            self.desktop_policy_mappings = ZscalerCollection.form_list(
                config["desktopPolicyMappings"] if "desktopPolicyMappings" in config else [], common.DesktopPolicyMappingsDTO
            )
            self.post_action_types = ZscalerCollection.form_list(
                config["postActionTypes"] if "postActionTypes" in config else [], str
            )
            self.service_edge_groups = ZscalerCollection.form_list(
                config["serviceEdgeGroups"] if "serviceEdgeGroups" in config else [], service_edge_groups.ServiceEdgeGroup
            )

            if "credential" in config:
                if isinstance(config["credential"], policyset_controller_v2.Credential):
                    self.credential = config["credential"]
                elif config["credential"] is not None:
                    self.credential = policyset_controller_v2.Credential(config["credential"])
                else:
                    self.credential = None
            else:
                self.credential = None

            if "credentialPool" in config:
                if isinstance(config["credentialPool"], policyset_controller_v2.Credential):
                    self.credential_pool = config["credentialPool"]
                elif config["credentialPool"] is not None:
                    self.credential_pool = policyset_controller_v2.Credential(config["credentialPool"])
                else:
                    self.credential_pool = None
            else:
                self.credential_pool = None

            if "extranetDTO" in config:
                if isinstance(config["extranetDTO"], common.ExtranetDTO):
                    self.extranet_dto = config["extranetDTO"]
                elif config["extranetDTO"] is not None:
                    self.extranet_dto = common.ExtranetDTO(config["extranetDTO"])
                else:
                    self.extranet_dto = None
            else:
                self.extranet_dto = None

            if "inconsistentConfigDetails" in config:
                if isinstance(config["inconsistentConfigDetails"], InconsistentConfigDetails):
                    self.inconsistent_config_details = config["inconsistentConfigDetails"]
                elif config["inconsistentConfigDetails"] is not None:
                    self.inconsistent_config_details = InconsistentConfigDetails(config["inconsistentConfigDetails"])
                else:
                    self.inconsistent_config_details = None
            else:
                self.inconsistent_config_details = None

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
        else:
            self.action = None
            self.action_id = None
            self.browser_posture_profile_id = None
            self.browser_posture_profile_name = None
            self.button_text = None
            self.creation_time = None
            self.custom_msg = None
            self.default_rule = None
            self.default_rule_name = None
            self.description = None
            self.device_posture_failure_notification_enabled = None
            self.disabled = None
            self.extranet_enabled = None
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
            self.post_actions = None
            self.priority = None
            self.read_only = None
            self.reauth_idle_timeout = None
            self.reauth_timeout = None
            self.restriction_type = None
            self.rule_order = None
            self.rule_type = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.url = None
            self.zpn_isolation_profile_id = None
            self.zpn_inspection_profile_id = None
            self.zpn_inspection_profile_name = None
            self.zscaler_managed = None
            self.app_server_groups = []
            self.app_connector_groups = []
            self.conditions = []
            self.desktop_policy_mappings = []
            self.post_action_types = []
            self.service_edge_groups = []
            self.credential = None
            self.credential_pool = None
            self.extranet_dto = None
            self.inconsistent_config_details = None
            self.privileged_capabilities = None
            self.privileged_portal_capabilities = None

    def request_format(self) -> Dict[str, Any]:
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
            "creationTime": self.creation_time,
            "customMsg": self.custom_msg,
            "defaultRule": self.default_rule,
            "defaultRuleName": self.default_rule_name,
            "description": self.description,
            "devicePostureFailureNotificationEnabled": self.device_posture_failure_notification_enabled,
            "disabled": self.disabled,
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
            "postActions": self.post_actions,
            "priority": self.priority,
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
            "appServerGroups": [item.request_format() for item in (self.app_server_groups or [])],
            "appConnectorGroups": [item.request_format() for item in (self.app_connector_groups or [])],
            "conditions": [item.request_format() for item in (self.conditions or [])],
            "desktopPolicyMappings": [item.request_format() for item in (self.desktop_policy_mappings or [])],
            "postActionTypes": self.post_action_types,
            "serviceEdgeGroups": [item.request_format() for item in (self.service_edge_groups or [])],
            "credential": self.credential,
            "credentialPool": self.credential_pool,
            "extranetDTO": self.extranet_dto,
            "inconsistentConfigDetails": self.inconsistent_config_details,
            "privilegedCapabilities": self.privileged_capabilities,
            "privilegedPortalCapabilities": self.privileged_portal_capabilities,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Condition(ZscalerObject):
    """
    A class for Condition objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Condition model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.negated = config["negated"] if "negated" in config else None
            self.operator = config["operator"] if "operator" in config else None
            self.policy_set_type = config["policySetType"] if "policySetType" in config else None
            self.rule_gid = config["ruleGid"] if "ruleGid" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.operands = ZscalerCollection.form_list(config["operands"] if "operands" in config else [], dict)
        else:
            self.creation_time = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.negated = None
            self.operator = None
            self.policy_set_type = None
            self.rule_gid = None
            self.microtenant_id = None
            self.operands = []

    def request_format(self) -> Dict[str, Any]:
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
            "operator": self.operator,
            "policySetType": self.policy_set_type,
            "ruleGid": self.rule_gid,
            "microtenantId": self.microtenant_id,
            "operands": self.operands,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class InconsistentConfigDetails(ZscalerObject):
    """
    A class for InconsistentConfigDetails objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the InconsistentConfigDetails model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.application = ZscalerCollection.form_list(config["application"] if "application" in config else [], dict)
            self.segment_group = ZscalerCollection.form_list(config["segmentGroup"] if "segmentGroup" in config else [], dict)
            self.app_connector_group = ZscalerCollection.form_list(
                config["appConnectorGroup"] if "appConnectorGroup" in config else [], dict
            )
            self.ba_certificate = ZscalerCollection.form_list(
                config["baCertificate"] if "baCertificate" in config else [], dict
            )
            self.branch_connector_group = ZscalerCollection.form_list(
                config["branchConnectorGroup"] if "branchConnectorGroup" in config else [], dict
            )
            self.cloud_connector_group = ZscalerCollection.form_list(
                config["cloudConnectorGroup"] if "cloudConnectorGroup" in config else [], dict
            )
            self.idp = ZscalerCollection.form_list(config["idp"] if "idp" in config else [], dict)
            self.location = ZscalerCollection.form_list(config["location"] if "location" in config else [], dict)
            self.machine_group = ZscalerCollection.form_list(config["machineGroup"] if "machineGroup" in config else [], dict)
            self.posture_profile = ZscalerCollection.form_list(
                config["postureProfile"] if "postureProfile" in config else [], dict
            )
            self.saml_attributes = ZscalerCollection.form_list(
                config["samlAttributes"] if "samlAttributes" in config else [], dict
            )
            self.scim_attributes = ZscalerCollection.form_list(
                config["scimAttributes"] if "scimAttributes" in config else [], dict
            )
            self.server_group = ZscalerCollection.form_list(config["serverGroup"] if "serverGroup" in config else [], dict)
            self.sra_application = ZscalerCollection.form_list(
                config["sraApplication"] if "sraApplication" in config else [], dict
            )
            self.trusted_network = ZscalerCollection.form_list(
                config["trustedNetwork"] if "trustedNetwork" in config else [], dict
            )
            self.user_portal = ZscalerCollection.form_list(config["userPortal"] if "userPortal" in config else [], dict)
            self.workload_tag_group = ZscalerCollection.form_list(
                config["workloadTagGroup"] if "workloadTagGroup" in config else [], dict
            )
        else:
            self.application = []
            self.segment_group = []
            self.app_connector_group = []
            self.ba_certificate = []
            self.branch_connector_group = []
            self.cloud_connector_group = []
            self.idp = []
            self.location = []
            self.machine_group = []
            self.posture_profile = []
            self.saml_attributes = []
            self.scim_attributes = []
            self.server_group = []
            self.sra_application = []
            self.trusted_network = []
            self.user_portal = []
            self.workload_tag_group = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "application": self.application,
            "segmentGroup": self.segment_group,
            "appConnectorGroup": self.app_connector_group,
            "baCertificate": self.ba_certificate,
            "branchConnectorGroup": self.branch_connector_group,
            "cloudConnectorGroup": self.cloud_connector_group,
            "idp": self.idp,
            "location": self.location,
            "machineGroup": self.machine_group,
            "postureProfile": self.posture_profile,
            "samlAttributes": self.saml_attributes,
            "scimAttributes": self.scim_attributes,
            "serverGroup": self.server_group,
            "sraApplication": self.sra_application,
            "trustedNetwork": self.trusted_network,
            "userPortal": self.user_portal,
            "workloadTagGroup": self.workload_tag_group,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
