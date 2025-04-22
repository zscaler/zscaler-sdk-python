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
from zscaler.zpa.models import server_group as server_group
from zscaler.zpa.models import service_edge_groups as service_edge_groups
from zscaler.zpa.models import policyset_controller_v2 as credentials
from zscaler.zpa.models import common as common


class PolicySetControllerV1(ZscalerObject):
    """
    A class representing a Policy Set Controller.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            # Handle fields
            self.id = config["id"] if "id" in config else None
            self.policy_set_id = config["policySetId"] if "policySetId" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.rule_order = config["ruleOrder"] if "ruleOrder" in config else None
            self.priority = config["priority"] if "priority" in config else None
            self.policy_type = config["policyType"] if "policyType" in config else None
            self.operator = config["operator"] if "operator" in config else None
            self.action = config["action"] if "action" in config else None
            self.reauth_idle_timeout = config["reauthIdleTimeout"] if "reauthIdleTimeout" in config else None
            self.reauth_timeout = config["reauthTimeout"] if "reauthTimeout" in config else None
            self.custom_msg = config["customMsg"] if "customMsg" in config else None
            self.disabled = config["disabled"] if "disabled" in config else None
            self.extranet_enabled = config["extranetEnabled"] if "extranetEnabled" in config else False
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.zpn_isolation_profile_id = config["zpnIsolationProfileId"] if "zpnIsolationProfileId" in config else None
            self.zpn_inspection_profile_id = config["zpnInspectionProfileId"] if "zpnInspectionProfileId" in config else None
            self.zpn_inspection_profile_name = (
                config["zpnInspectionProfileName"] if "zpnInspectionProfileName" in config else None
            )
            self.version = config["version"] if "version" in config else None
            self.default_rule = config["defaultRule"] if "defaultRule" in config else False

            # Handle conditions using ZscalerCollection
            self.conditions = ZscalerCollection.form_list(config.get("conditions", []), Condition)

            self.app_connector_groups = ZscalerCollection.form_list(
                config["appConnectorGroups"] if "appConnectorGroups" in config else [], app_connector_groups.AppConnectorGroup
            )

            self.app_server_groups = ZscalerCollection.form_list(
                config["appServerGroups"] if "appServerGroups" in config else [], server_group.ServerGroup
            )

            self.service_edge_groups = ZscalerCollection.form_list(
                config["serviceEdgeGroups"] if "serviceEdgeGroups" in config else [], service_edge_groups.ServiceEdgeGroup
            )

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

            if "extranetDTO" in config:
                if isinstance(config["extranetDTO"], common.ExtranetDTO):
                    self.extranet_dto = config["extranetDTO"]
                elif config["extranetDTO"] is not None:
                    self.extranet_dto = common.ExtranetDTO(config["extranetDTO"])
                else:
                    self.extranet_dto = None
            else:
                self.extranet_dto = None

            if "credential" in config:
                if isinstance(config["credential"], credentials.Credential):
                    self.credential = config["credential"]
                elif config["credential"] is not None:
                    self.credential = credentials.Credential(config["credential"])
                else:
                    self.credential = None
            else:
                self.credential = None

            if "credentialPool" in config:
                if isinstance(config["credentialPool"], credentials.Credential):
                    self.credential_pool = config["credentialPool"]
                elif config["credentialPool"] is not None:
                    self.credential_pool = credentials.Credential(config["credentialPool"])
                else:
                    self.credential_pool = None
            else:
                self.credential_pool = None
        else:
            # Defaults when config is None
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.description = None
            self.rule_order = None
            self.priority = None
            self.policy_type = None
            self.operator = None
            self.action = None
            self.custom_msg = None
            self.disabled = None
            self.extranet_dto = None
            self.extranet_enabled = False
            self.default_rule = False
            self.microtenant_id = None
            self.microtenant_name = None
            self.version = None
            self.credential = None
            self.credential_pool = None
            self.zpn_isolation_profile_id = None
            self.zpn_inspection_profile_id = None
            self.zpn_inspection_profile_name = None
            self.conditions = []
            self.app_connector_groups = []
            self.app_server_groups = []
            self.service_edge_groups = []
            self.privileged_capabilities = None
            self.privileged_portal_capabilities = None
            self.reauth_idle_timeout = None
            self.reauth_timeout = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "description": self.description,
            "ruleOrder": self.rule_order,
            "priority": self.priority,
            "policyType": self.policy_type,
            "operator": self.operator,
            "action": self.action,
            "customMsg": self.custom_msg,
            "disabled": self.disabled,
            "extranetEnabled": self.extranet_enabled,
            "defaultRule": self.default_rule,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "zpnIsolationProfileId": self.zpn_isolation_profile_id,
            "zpnInspectionProfileId": self.zpn_inspection_profile_id,
            "zpnInspectionProfileName": self.zpn_inspection_profile_name,
            "reauthIdleTimeout": self.reauth_idle_timeout,
            "reauthTimeout": self.reauth_timeout,
            "version": self.version,
            "credential": self.credential,
            "extranetDTO": self.extranet_dto,
            "credentialPool": self.credential_pool,
            "privilegedCapabilities": self.privileged_capabilities,
            "privilegedPortalCapabilities": self.privileged_portal_capabilities,
            "conditions": [condition.request_format() for condition in self.conditions],
            "appConnectorGroups": [group.request_format() for group in self.app_connector_groups],
            "appServerGroups": [group.request_format() for group in self.app_server_groups],
            "serviceEdgeGroups": [group.request_format() for group in self.service_edge_groups],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


# The Condition class used within PolicySetController (kept inline with how operands are structured)
class Condition(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.operator = config["operator"] if "operator" in config else None
            self.negated = config.get("negated", False)

            # Handle operands using ZscalerCollection
            self.operands = ZscalerCollection.form_list(config.get("operands", []), Operand)

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.operator = None
            self.negated = False
            self.operands = []

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "operator": self.operator,
            "negated": self.negated,
            "operands": [operand.request_format() for operand in self.operands],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Operand(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.object_type = config["objectType"] if "objectType" in config else None
            self.lhs = config["lhs"] if "lhs" in config else None
            self.rhs = config["rhs"] if "rhs" in config else None
            self.name = config["name"] if "name" in config else None
            self.idp_id = config["idpId"] if "idpId" in config else None
            self.idp_name = config["idpName"] if "idpName" in config else None

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.object_type = None
            self.lhs = None
            self.rhs = None
            self.name = None
            self.idp_id = None
            self.idp_name = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "objectType": self.object_type,
            "lhs": self.lhs,
            "rhs": self.rhs,
            "name": self.name,
            "idpId": self.idp_id,
            "idpName": self.idp_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
