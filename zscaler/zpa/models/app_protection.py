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
from zscaler.zpa.models import app_protection_predefined_controls as app_protection_predefined_controls
from zscaler.zpa.models import common as common


class InspectionProfile(ZscalerObject):
    """
    A class for InspectionProfile objects.
    """

    def __init__(self, config=None):
        """
        Initialize the InspectionProfile model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.api_profile = config["apiProfile"] if "apiProfile" in config else None
            self.check_control_deployment_status = (
                config["checkControlDeploymentStatus"] if "checkControlDeploymentStatus" in config else None
            )
            self.controls_info = ZscalerCollection.form_list(config["controlsInfo"] if "controlsInfo" in config else [], str)
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.custom_controls = ZscalerCollection.form_list(
                config["customControls"] if "customControls" in config else [], str
            )
            self.description = config["description"] if "description" in config else None
            self.exceptions_version = config["exceptionsVersion"] if "exceptionsVersion" in config else None
            self.global_control_actions = ZscalerCollection.form_list(
                config["globalControlActions"] if "globalControlActions" in config else [], str
            )
            self.id = config["id"] if "id" in config else None
            self.incarnation_number = config["incarnationNumber"] if "incarnationNumber" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.paranoia_level = config["paranoiaLevel"] if "paranoiaLevel" in config else None
            self.predefined_adp_controls = ZscalerCollection.form_list(
                config["predefinedADPControls"] if "predefinedADPControls" in config else [], str
            )
            self.predefined_api_controls = ZscalerCollection.form_list(
                config["predefinedApiControls"] if "predefinedApiControls" in config else [], str
            )

            self.predefined_controls = ZscalerCollection.form_list(
                config["predefinedControls"] if "predefinedControls" in config else [],
                app_protection_predefined_controls.PredefinedInspectionControlResource,
            )

            self.predefined_controls_version = (
                config["predefinedControlsVersion"] if "predefinedControlsVersion" in config else None
            )
            self.threatlabz_controls = ZscalerCollection.form_list(
                config["threatlabzControls"] if "threatlabzControls" in config else [], str
            )
            self.websocket_controls = ZscalerCollection.form_list(
                config["websocketControls"] if "websocketControls" in config else [], str
            )
            self.zs_defined_control_choice = config["zsDefinedControlChoice"] if "zsDefinedControlChoice" in config else None
        else:
            self.api_profile = None
            self.check_control_deployment_status = None
            self.controls_info = ZscalerCollection.form_list([], str)
            self.creation_time = None
            self.custom_controls = ZscalerCollection.form_list([], str)
            self.description = None
            self.exceptions_version = None
            self.global_control_actions = ZscalerCollection.form_list([], str)
            self.id = None
            self.incarnation_number = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.paranoia_level = None
            self.predefined_adp_controls = ZscalerCollection.form_list([], str)
            self.predefined_api_controls = ZscalerCollection.form_list([], str)
            self.predefined_controls = ZscalerCollection.form_list([], str)
            self.predefined_controls_version = None
            self.threatlabz_controls = ZscalerCollection.form_list([], str)
            self.websocket_controls = ZscalerCollection.form_list([], str)
            self.zs_defined_control_choice = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "apiProfile": self.api_profile,
            "checkControlDeploymentStatus": self.check_control_deployment_status,
            "controlsInfo": self.controls_info,
            "creationTime": self.creation_time,
            "customControls": self.custom_controls,
            "description": self.description,
            "exceptionsVersion": self.exceptions_version,
            "globalControlActions": self.global_control_actions,
            "id": self.id,
            "incarnationNumber": self.incarnation_number,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "paranoiaLevel": self.paranoia_level,
            "predefinedADPControls": self.predefined_adp_controls,
            "predefinedApiControls": self.predefined_api_controls,
            "predefinedControls": self.predefined_controls,
            "predefinedControlsVersion": self.predefined_controls_version,
            "threatlabzControls": self.threatlabz_controls,
            "websocketControls": self.websocket_controls,
            "zsDefinedControlChoice": self.zs_defined_control_choice,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppProtectionCustomControl(ZscalerObject):
    """
       A class for class AppProtectionCustomControl(ZscalerObject):
    objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AppProtectionCustomControl model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.action = config["action"] if "action" in config else None
            self.action_value = config["actionValue"] if "actionValue" in config else None
            self.control_number = config["controlNumber"] if "controlNumber" in config else None
            self.control_rule_json = config["controlRuleJson"] if "controlRuleJson" in config else None
            self.control_type = config["controlType"] if "controlType" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.default_action = config["defaultAction"] if "defaultAction" in config else None
            self.default_action_value = config["defaultActionValue"] if "defaultActionValue" in config else None
            self.description = config["description"] if "description" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.paranoia_level = config["paranoiaLevel"] if "paranoiaLevel" in config else None
            self.protocol_type = config["protocolType"] if "protocolType" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.type = config["type"] if "type" in config else None
            self.version = config["version"] if "version" in config else None

            self.associated_inspection_profile_names = ZscalerCollection.form_list(
                config["associatedInspectionProfileNames"] if "associatedInspectionProfileNames" in config else [],
                common.CommonIDName,
            )

            self.rules = ZscalerCollection.form_list(config["rules"] if "rules" in config else [], InspectionRule)

            if "controlException" in config:
                if isinstance(config["controlException"], common.InspectionControlException):
                    self.control_exception = config["controlException"]
                elif config["controlException"] is not None:
                    self.control_exception = common.InspectionControlException(config["controlException"])
                else:
                    self.control_exception = None
            else:
                self.control_exception = None

        else:
            self.action = None
            self.action_value = None
            self.associated_inspection_profile_names = []
            self.control_exception = None
            self.control_number = None
            self.control_rule_json = None
            self.control_type = None
            self.creation_time = None
            self.default_action = None
            self.default_action_value = None
            self.description = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.paranoia_level = None
            self.protocol_type = None
            self.rules = []
            self.severity = None
            self.type = None
            self.version = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "actionValue": self.action_value,
            "associatedInspectionProfileNames": self.associated_inspection_profile_names,
            "controlException": self.control_exception,
            "controlNumber": self.control_number,
            "controlRuleJson": self.control_rule_json,
            "controlType": self.control_type,
            "creationTime": self.creation_time,
            "defaultAction": self.default_action,
            "defaultActionValue": self.default_action_value,
            "description": self.description,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "paranoiaLevel": self.paranoia_level,
            "protocolType": self.protocol_type,
            "rules": self.rules,
            "severity": self.severity,
            "type": self.type,
            "version": self.version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class InspectionRule(ZscalerObject):
    """
    A class for Rules objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the Rules model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.names = config["names"] if "names" in config else None
            self.type = config["type"] if "type" in config else None
            self.conditions = ZscalerCollection.form_list(
                config["conditions"] if "conditions" in config else [], InspectionRuleCondition
            )

        else:
            self.names = None
            self.type = None
            self.conditions = []

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "names": self.names,
            "type": self.type,
            "conditions": self.conditions,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class InspectionRuleCondition(ZscalerObject):
    """
    A class for InspectionRuleCondition objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the Rules model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.lhs = config["lhs"] if "lhs" in config else None
            self.op = config["op"] if "op" in config else None
            self.rhs = config["rhs"] if "rhs" in config else None

        else:
            self.lhs = None
            self.op = None
            self.rhs = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "lhs": self.lhs,
            "op": self.op,
            "rhs": self.rhs,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
