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
from zscaler.zpa.models import policyset_controller_v1 as policyset_controller_v1


class LSSResourceModel(ZscalerObject):
    """
    A class for LSSResourceModel objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the LSSResourceModel model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None

            self.connector_groups = ZscalerCollection.form_list(
                config["connectorGroups"] if "connectorGroups" in config else [], app_connector_groups.AppConnectorGroup
            )

            if "config" in config:
                if isinstance(config["config"], LSSConfig):
                    self.config = config["config"]
                elif config["config"] is not None:
                    self.config = LSSConfig(config["config"])
                else:
                    self.config = None
            else:
                self.config = None

            if "policyRule" in config:
                if isinstance(config["policyRule"], policyset_controller_v1.PolicySetControllerV1):
                    self.policy_rule = config["policyRule"]
                elif config["policyRule"] is not None:
                    self.policy_rule = policyset_controller_v1.PolicySetControllerV1(config["policyRule"])
                else:
                    self.policy_rule = None
            else:
                self.policy_rule = None

            if "policyRuleResource" in config:
                if isinstance(config["policyRuleResource"], policyset_controller_v1.PolicySetControllerV1):
                    self.policy_rule_resource = config["policyRuleResource"]
                elif config["policyRuleResource"] is not None:
                    self.policy_rule_resource = policyset_controller_v1.PolicySetControllerV1(config["policyRuleResource"])
                else:
                    self.policy_rule_resource = None
            else:
                self.policy_rule_resource = None

        else:
            self.id = None
            self.connector_groups = []
            self.policy_rule = None
            self.policy_rule_resource = None
            self.lss_config = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "config": self.config.request_format() if self.config else None,
            "connectorGroups": [g.request_format() for g in self.connector_groups],
            "policyRule": self.policy_rule.request_format() if self.policy_rule else None,
            "policyRuleResource": self.policy_rule_resource.request_format() if self.policy_rule_resource else None,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LSSConfig(ZscalerObject):
    """
    A class for LSSConfig objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the LSSConfig model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.source_log_type = config["sourceLogType"] if "sourceLogType" in config else None
            self.use_tls = config["useTls"] if "useTls" in config else False
            self.format = config["format"] if "format" in config else None
            self.filter = config["filter"] if "filter" in config else []
            self.audit_message = config["auditMessage"] if "auditMessage" in config else None
            self.lss_host = config["lssHost"] if "lssHost" in config else None
            self.lss_port = config["lssPort"] if "lssPort" in config else None

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.description = None
            self.enabled = True
            self.source_log_type = None
            self.use_tls = False
            self.format = None
            self.filter = []
            self.audit_message = None
            self.lss_host = None
            self.lss_port = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "sourceLogType": self.source_log_type,
            "useTls": self.use_tls,
            "format": self.format,
            "filter": self.filter,
            "auditMessage": self.audit_message,
            "lssHost": self.lss_host,
            "lssPort": self.lss_port,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
