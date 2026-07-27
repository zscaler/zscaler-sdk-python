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
from zscaler.zia.models import common as common


class OutboundEmailDlpRules(ZscalerObject):
    """
    A class for OutboundEmailDlpRules objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the OutboundEmailDlpRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.order = config["order"] if "order" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.state = config["state"] if "state" in config else None
            self.action = config["action"] if "action" in config else None
            self.min_size = config["minSize"] if "minSize" in config else None
            self.without_content_inspection = (
                config["withoutContentInspection"] if "withoutContentInspection" in config else None
            )
            self.external_auditor_email = config["externalAuditorEmail"] if "externalAuditorEmail" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.parent_rule = config["parentRule"] if "parentRule" in config else None
            self.custom_header = config["customHeader"] if "customHeader" in config else None
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], common.ResourceReference)
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], common.ResourceReference
            )
            self.users = ZscalerCollection.form_list(config["users"] if "users" in config else [], common.ResourceReference)
            self.excluded_groups = ZscalerCollection.form_list(
                config["excludedGroups"] if "excludedGroups" in config else [], common.ResourceReference
            )
            self.excluded_departments = ZscalerCollection.form_list(
                config["excludedDepartments"] if "excludedDepartments" in config else [], common.ResourceReference
            )
            self.excluded_users = ZscalerCollection.form_list(
                config["excludedUsers"] if "excludedUsers" in config else [], common.ResourceReference
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], common.ResourceReference
            )
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], common.ResourceReference
            )
            self.file_types = ZscalerCollection.form_list(config["fileTypes"] if "fileTypes" in config else [], str)
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], common.ResourceReference)
            self.included_domain_profiles = ZscalerCollection.form_list(
                config["includedDomainProfiles"] if "includedDomainProfiles" in config else [], common.ResourceReference
            )
            self.user_risk_score_levels = ZscalerCollection.form_list(
                config["userRiskScoreLevels"] if "userRiskScoreLevels" in config else [], str
            )
            self.email_tenants = ZscalerCollection.form_list(
                config["emailTenants"] if "emailTenants" in config else [], common.ResourceReference
            )
            self.content_locations = ZscalerCollection.form_list(
                config["contentLocations"] if "contentLocations" in config else [], str
            )
            self.sub_rules = ZscalerCollection.form_list(config["subRules"] if "subRules" in config else [], SubRule)
            self.email_recipient_profiles = ZscalerCollection.form_list(
                config["emailRecipientProfiles"] if "emailRecipientProfiles" in config else [], common.ResourceReference
            )

            if "auditor" in config:
                if isinstance(config["auditor"], common.CommonBlocks):
                    self.auditor = config["auditor"]
                elif config["auditor"] is not None:
                    self.auditor = common.CommonBlocks(config["auditor"])
                else:
                    self.auditor = None
            else:
                self.auditor = None

            if "notificationTemplate" in config:
                if isinstance(config["notificationTemplate"], common.CommonBlocks):
                    self.notification_template = config["notificationTemplate"]
                elif config["notificationTemplate"] is not None:
                    self.notification_template = common.CommonBlocks(config["notificationTemplate"])
                else:
                    self.notification_template = None
            else:
                self.notification_template = None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            if "receiver" in config:
                if isinstance(config["receiver"], common.CommonIDName):
                    self.receiver = config["receiver"]
                elif config["receiver"] is not None:
                    self.receiver = common.CommonIDName(config["receiver"])
                else:
                    self.receiver = None
            else:
                self.receiver = None
        else:
            self.id = None
            self.order = None
            self.name = None
            self.description = None
            self.state = None
            self.action = None
            self.min_size = None
            self.without_content_inspection = None
            self.external_auditor_email = None
            self.last_modified_time = None
            self.severity = None
            self.parent_rule = None
            self.custom_header = None
            self.groups = []
            self.departments = []
            self.users = []
            self.excluded_groups = []
            self.excluded_departments = []
            self.excluded_users = []
            self.time_windows = []
            self.dlp_engines = []
            self.file_types = []
            self.labels = []
            self.included_domain_profiles = []
            self.user_risk_score_levels = []
            self.email_tenants = []
            self.content_locations = []
            self.sub_rules = []
            self.email_recipient_profiles = []
            self.auditor = None
            self.notification_template = None
            self.last_modified_by = None
            self.receiver = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "order": self.order,
            "name": self.name,
            "description": self.description,
            "state": self.state,
            "action": self.action,
            "minSize": self.min_size,
            "withoutContentInspection": self.without_content_inspection,
            "externalAuditorEmail": self.external_auditor_email,
            "lastModifiedTime": self.last_modified_time,
            "severity": self.severity,
            "parentRule": self.parent_rule,
            "customHeader": self.custom_header,
            "groups": [item.request_format() for item in (self.groups or [])],
            "departments": [item.request_format() for item in (self.departments or [])],
            "users": [item.request_format() for item in (self.users or [])],
            "excludedGroups": [item.request_format() for item in (self.excluded_groups or [])],
            "excludedDepartments": [item.request_format() for item in (self.excluded_departments or [])],
            "excludedUsers": [item.request_format() for item in (self.excluded_users or [])],
            "timeWindows": [item.request_format() for item in (self.time_windows or [])],
            "dlpEngines": [item.request_format() for item in (self.dlp_engines or [])],
            "fileTypes": self.file_types,
            "labels": [item.request_format() for item in (self.labels or [])],
            "includedDomainProfiles": [item.request_format() for item in (self.included_domain_profiles or [])],
            "userRiskScoreLevels": self.user_risk_score_levels,
            "emailTenants": [item.request_format() for item in (self.email_tenants or [])],
            "contentLocations": self.content_locations,
            "subRules": [item.request_format() for item in (self.sub_rules or [])],
            "emailRecipientProfiles": [item.request_format() for item in (self.email_recipient_profiles or [])],
            "auditor": self.auditor,
            "notificationTemplate": self.notification_template,
            "lastModifiedBy": self.last_modified_by,
            "receiver": self.receiver,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SubRule(ZscalerObject):
    """
    A class for SubRule objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the SubRule model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.order = config["order"] if "order" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.state = config["state"] if "state" in config else None
            self.action = config["action"] if "action" in config else None
            self.min_size = config["minSize"] if "minSize" in config else None
            self.without_content_inspection = (
                config["withoutContentInspection"] if "withoutContentInspection" in config else None
            )
            self.external_auditor_email = config["externalAuditorEmail"] if "externalAuditorEmail" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.parent_rule = config["parentRule"] if "parentRule" in config else None
            self.custom_header = config["customHeader"] if "customHeader" in config else None
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], common.ResourceReference)
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], common.ResourceReference
            )
            self.users = ZscalerCollection.form_list(config["users"] if "users" in config else [], common.ResourceReference)
            self.excluded_groups = ZscalerCollection.form_list(
                config["excludedGroups"] if "excludedGroups" in config else [], common.ResourceReference
            )
            self.excluded_departments = ZscalerCollection.form_list(
                config["excludedDepartments"] if "excludedDepartments" in config else [], common.ResourceReference
            )
            self.excluded_users = ZscalerCollection.form_list(
                config["excludedUsers"] if "excludedUsers" in config else [], common.ResourceReference
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], common.ResourceReference
            )
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], common.ResourceReference
            )
            self.file_types = ZscalerCollection.form_list(config["fileTypes"] if "fileTypes" in config else [], str)
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], common.ResourceReference)
            self.included_domain_profiles = ZscalerCollection.form_list(
                config["includedDomainProfiles"] if "includedDomainProfiles" in config else [], common.ResourceReference
            )
            self.user_risk_score_levels = ZscalerCollection.form_list(
                config["userRiskScoreLevels"] if "userRiskScoreLevels" in config else [], str
            )
            self.email_tenants = ZscalerCollection.form_list(
                config["emailTenants"] if "emailTenants" in config else [], common.ResourceReference
            )
            self.content_locations = ZscalerCollection.form_list(
                config["contentLocations"] if "contentLocations" in config else [], str
            )
            self.email_recipient_profiles = ZscalerCollection.form_list(
                config["emailRecipientProfiles"] if "emailRecipientProfiles" in config else [], common.ResourceReference
            )

            if "auditor" in config:
                if isinstance(config["auditor"], common.CommonBlocks):
                    self.auditor = config["auditor"]
                elif config["auditor"] is not None:
                    self.auditor = common.CommonBlocks(config["auditor"])
                else:
                    self.auditor = None
            else:
                self.auditor = None

            if "notificationTemplate" in config:
                if isinstance(config["notificationTemplate"], common.CommonBlocks):
                    self.notification_template = config["notificationTemplate"]
                elif config["notificationTemplate"] is not None:
                    self.notification_template = common.CommonBlocks(config["notificationTemplate"])
                else:
                    self.notification_template = None
            else:
                self.notification_template = None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            if "receiver" in config:
                if isinstance(config["receiver"], common.CommonIDName):
                    self.receiver = config["receiver"]
                elif config["receiver"] is not None:
                    self.receiver = common.CommonIDName(config["receiver"])
                else:
                    self.receiver = None
            else:
                self.receiver = None
        else:
            self.id = None
            self.order = None
            self.name = None
            self.description = None
            self.state = None
            self.action = None
            self.min_size = None
            self.without_content_inspection = None
            self.external_auditor_email = None
            self.last_modified_time = None
            self.severity = None
            self.parent_rule = None
            self.custom_header = None
            self.groups = []
            self.departments = []
            self.users = []
            self.excluded_groups = []
            self.excluded_departments = []
            self.excluded_users = []
            self.time_windows = []
            self.dlp_engines = []
            self.file_types = []
            self.labels = []
            self.included_domain_profiles = []
            self.user_risk_score_levels = []
            self.email_tenants = []
            self.content_locations = []
            self.email_recipient_profiles = []
            self.auditor = None
            self.notification_template = None
            self.last_modified_by = None
            self.receiver = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "order": self.order,
            "name": self.name,
            "description": self.description,
            "state": self.state,
            "action": self.action,
            "minSize": self.min_size,
            "withoutContentInspection": self.without_content_inspection,
            "externalAuditorEmail": self.external_auditor_email,
            "lastModifiedTime": self.last_modified_time,
            "severity": self.severity,
            "parentRule": self.parent_rule,
            "customHeader": self.custom_header,
            "groups": [item.request_format() for item in (self.groups or [])],
            "departments": [item.request_format() for item in (self.departments or [])],
            "users": [item.request_format() for item in (self.users or [])],
            "excludedGroups": [item.request_format() for item in (self.excluded_groups or [])],
            "excludedDepartments": [item.request_format() for item in (self.excluded_departments or [])],
            "excludedUsers": [item.request_format() for item in (self.excluded_users or [])],
            "timeWindows": [item.request_format() for item in (self.time_windows or [])],
            "dlpEngines": [item.request_format() for item in (self.dlp_engines or [])],
            "fileTypes": self.file_types,
            "labels": [item.request_format() for item in (self.labels or [])],
            "includedDomainProfiles": [item.request_format() for item in (self.included_domain_profiles or [])],
            "userRiskScoreLevels": self.user_risk_score_levels,
            "emailTenants": [item.request_format() for item in (self.email_tenants or [])],
            "contentLocations": self.content_locations,
            "emailRecipientProfiles": [item.request_format() for item in (self.email_recipient_profiles or [])],
            "auditor": self.auditor,
            "notificationTemplate": self.notification_template,
            "lastModifiedBy": self.last_modified_by,
            "receiver": self.receiver,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
