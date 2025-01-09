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
from zscaler.zpa.models import app_connector_groups\
    as app_connector_groups
from zscaler.zpa.models import server_group\
    as server_group
from zscaler.zpa.models import service_edge_groups\
    as service_edge_groups
from zscaler.oneapi_collection import ZscalerCollection

class PolicySetControllerV2(ZscalerObject):
    """
    A class representing a Policy Set Controller V2.
    """

    def __init__(self, config=None):
        super().__init__(config)
        
        if config:
            self.id = config["id"]\
                if "id" in config else None
            self.policy_set_id = config["policySetId"]\
                if "policySetId" in config else None
            self.name = config["name"]\
                if "name" in config else None
            self.description = config["description"]\
                if "description" in config else None
            self.action = config["action"]\
                if "action" in config else None
            self.custom_msg = config["customMsg"]\
                if "customMsg" in config else None
            self.disabled = config["disabled"]\
                if "disabled" in config else None
            self.reauth_idle_timeout = config["reauthIdleTimeout"]\
                if "reauthIdleTimeout" in config else None
            self.reauth_timeout = config["reauthTimeout"]\
                if "reauthTimeout" in config else None
            self.rule_order = config["ruleOrder"]\
                if "ruleOrder" in config else None
            self.microtenant_id = config["microtenantId"]\
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"]\
                if "microtenantName" in config else None
            self.zpn_isolation_profile_id = config["zpnIsolationProfileId"]\
                if "zpnIsolationProfileId" in config else None
            self.zpn_inspection_profile_id = config["zpnInspectionProfileId"]\
                if "zpnInspectionProfileId" in config else None
            self.zpn_inspection_profile_name = config["zpnInspectionProfileName"]\
                if "zpnInspectionProfileName" in config else None
            self.extranet_enabled = config["extranetEnabled"]\
                if "extranetEnabled" in config else False
            self.version = config["version"]\
                if "version" in config else None
            self.default_rule = config["defaultRule"]\
                if "defaultRule" in config else False

            # Handle conditions using ZscalerCollection and isinstance check for reusability
            self.conditions = ZscalerCollection.form_list(config.get("conditions", []), Condition)

            # Handle appConnectorGroups using isinstance check
            self.app_connector_groups = []
            if "appConnectorGroups" in config:
                for group in config["appConnectorGroups"]:
                    if isinstance(group, app_connector_groups.AppConnectorGroup):
                        self.app_connector_groups.append(group)
                    else:
                        self.app_connector_groups.append(app_connector_groups.AppConnectorGroup(group))

            # Handle appServerGroups using isinstance check
            self.app_server_groups = []
            if "appServerGroups" in config:
                for group in config["appServerGroups"]:
                    if isinstance(group, server_group.ServerGroup):
                        self.app_server_groups.append(group)
                    else:
                        self.app_server_groups.append(server_group.ServerGroup(group))

            # Handle serviceEdgeGroups using isinstance check
            self.service_edge_groups = []
            if "serviceEdgeGroups" in config:
                for group in config["serviceEdgeGroups"]:
                    if isinstance(group, service_edge_groups.ServiceEdgeGroup):
                        self.service_edge_groups.append(group)
                    else:
                        self.service_edge_groups.append(service_edge_groups.ServiceEdgeGroup(group))

            # Handle extranetDTO using isinstance check
            self.extranet_dto = ExtranetDTO(config["extranetDTO"]) if isinstance(config.get("extranetDTO"), ExtranetDTO) else ExtranetDTO(config.get("extranetDTO")) if "extranetDTO" in config else None

            # Handle privileged capabilities
            self.privileged_capabilities = config.get("privilegedCapabilities", {}).get("capabilities", [])
            self.privileged_portal_capabilities = config.get("privilegedPortalCapabilities", {}).get("capabilities", [])

            # Handle credential using isinstance check
            self.credential = Credential(config["credential"]) if isinstance(config.get("credential"), Credential) else Credential(config.get("credential")) if "credential" in config else None

        else:
            # Defaults when config is None
            self.policy_set_id = None
            self.name = None
            self.description = None
            self.action = None
            self.custom_msg = None
            self.reauth_idle_timeout = None
            self.reauth_timeout = None
            self.rule_order = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.zpn_isolation_profile_id = None
            self.zpn_inspection_profile_id = None
            self.zpn_inspection_profile_name = None
            self.extranet_enabled = False
            self.conditions = []
            self.app_connector_groups = []
            self.app_server_groups = []
            self.service_edge_groups = []
            self.extranet_dto = None
            self.privileged_capabilities = []
            self.privileged_portal_capabilities = []
            self.credential = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "policySetId": self.policy_set_id,
            "conditions": [condition.request_format() for condition in self.conditions],
            "name": self.name,
            "description": self.description,
            "action": self.action,
            "appConnectorGroups": [group.request_format() for group in self.app_connector_groups],
            "appServerGroups": [group.request_format() for group in self.app_server_groups],
            "extranetEnabled": self.extranet_enabled,
            "extranetDTO": self.extranet_dto.request_format() if self.extranet_dto else None,
            "privilegedCapabilities": {"capabilities": self.privileged_capabilities},
            "privilegedPortalCapabilities": {"capabilities": self.privileged_portal_capabilities},
            "credential": self.credential.request_format() if self.credential else None,
            "serviceEdgeGroups": [group.request_format() for group in self.service_edge_groups],
            "customMsg": self.custom_msg,
            "disabled": self.disabled,
            "reauthIdleTimeout": self.reauth_idle_timeout,
            "reauthTimeout": self.reauth_timeout,
            "ruleOrder": self.rule_order,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "zpnIsolationProfileId": self.zpn_isolation_profile_id,
            "zpnInspectionProfileId": self.zpn_inspection_profile_id,
            "zpnInspectionProfileName": self.zpn_inspection_profile_name
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format

# The Condition class used within PolicySetControllerV2
class Condition(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.operator = config.get("operator")
            self.operands = []
            if "operands" in config:
                for operand in config["operands"]:
                    if isinstance(operand, Operand):
                        self.operands.append(operand)
                    else:
                        self.operands.append(Operand(operand))

        else:
            self.operator = None
            self.operands = []

    def request_format(self):
        return {
            "operator": self.operator,
            "operands": [operand.request_format() for operand in self.operands]
        }

# The Operand class used within Condition
class Operand(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.object_type = config.get("objectType")
            self.values = config.get("values", [])
            self.entry_values = [{"lhs": entry["lhs"], "rhs": entry["rhs"]} for entry in config.get("entryValues", [])] if "entryValues" in config else []

        else:
            self.object_type = None
            self.values = []
            self.entry_values = []

    def request_format(self):
        return {
            "objectType": self.object_type,
            "values": self.values,
            "entryValues": self.entry_values
        }

# The ExtranetDTO class used within PolicySetControllerV2
class ExtranetDTO(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.location_dto = [{"id": loc["id"], "name": loc["name"]} for loc in config.get("locationDTO", [])]
            self.location_group_dto = [{
                "id": group["id"],
                "name": group["name"],
                "ziaLocations": [{"id": loc["id"], "name": loc["name"]} for loc in group.get("ziaLocations", [])]
            } for group in config.get("locationGroupDTO", [])]
            self.zia_er_name = config.get("ziaErName")
            self.zpn_er_id = config.get("zpnErId")

        else:
            self.location_dto = []
            self.location_group_dto = []
            self.zia_er_name = None
            self.zpn_er_id = None

    def request_format(self):
        return {
            "locationDTO": self.location_dto,
            "locationGroupDTO": self.location_group_dto,
            "ziaErName": self.zia_er_name,
            "zpnErId": self.zpn_er_id
        }

# The Credential class used within PolicySetControllerV2
class Credential(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.id = config.get("id")
            self.name = config.get("name")

        else:
            self.id = None
            self.name = None

    def request_format(self):
        return {
            "id": self.id,
            "name": self.name
        }
