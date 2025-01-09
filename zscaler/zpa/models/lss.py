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
from zscaler.zpa.models import app_connector_groups\
    as app_connector_groups
from zscaler.zpa.models import policyset_controller_v2\
    as policyset_controller_v2

class LSSConfig(ZscalerObject):
    """
    A class representing the LSS Receiver configuration.
    """

    def __init__(self, config=None):
        """
        Initialize the LSSConfig object with given config data.
        Uses defensive programming with conditionals for handling configuration attributes.

        Args:
            config (dict): The configuration dictionary from API response.
        """
        super().__init__(config)

        if config:
            self.id = config["id"]\
                if "id" in config else None
            self.modified_time = config["modifiedTime"]\
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"]\
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"]\
                if "modifiedBy" in config else None
            self.name = config["name"]\
                if "name" in config else None
            self.description = config["description"]\
                if "description" in config else None
            self.enabled = config["enabled"]\
                if "enabled" in config else True
            self.source_log_type = config["sourceLogType"]\
                if "sourceLogType" in config else None
            self.use_tls = config["useTls"]\
                if "useTls" in config else False
            self.format = config["format"]\
                if "format" in config else None
            self.filter = config["filter"]\
                if "filter" in config else []
            self.audit_message = config["auditMessage"]\
                if "auditMessage" in config else None
            self.lss_host = config["lssHost"]\
                if "lssHost" in config else None
            self.lss_port = config["lssPort"]\
                if "lssPort" in config else None

            self.connector_groups = ZscalerCollection.form_list(
                config["connectorGroups"] if "connectorGroups" in config else [], app_connector_groups.AppConnectorGroup
            )
            
            if "policyRule" in config:
                self.policy_rule = policyset_controller_v2.PolicySetControllerV2(config["policyRule"])
            else:
                self.policy_rule = None
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
            self.connector_groups = []
            self.policy_rule = None

    def request_format(self):
        """
        Formats the LSS Config data into a dictionary suitable for API requests.
        """
        return {
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
            "connectorGroups": self.connector_groups,
            "policyRule": self.policy_rule.request_format() if self.policy_rule else None,
        }
