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


class EndpointDlpRules(ZscalerObject):
    """
    A class for EndpointDlpRules objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EndpointDlpRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.state = config["state"] if "state" in config else None
            self.order = config["order"] if "order" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.file_types = config["fileTypes"] if "fileTypes" in config else None
            self.data_transfer_method = config["dataTransferMethod"] if "dataTransferMethod" in config else None
            self.description = config["description"] if "description" in config else None
            self.min_size = config["minSize"] if "minSize" in config else None
            self.action = config["action"] if "action" in config else None
            self.external_auditor_email = config["externalAuditorEmail"] if "externalAuditorEmail" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.parent_rule = config["parentRule"] if "parentRule" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.eun_enabled = config["eunEnabled"] if "eunEnabled" in config else None
            self.eun_template_id = config["eunTemplateId"] if "eunTemplateId" in config else None
            self.uc_template_id = config["ucTemplateId"] if "ucTemplateId" in config else None
            self.network_type = config["networkType"] if "networkType" in config else None
            self.without_content_inspection = (
                config["withoutContentInspection"] if "withoutContentInspection" in config else None
            )
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], common.ResourceReference
            )
            self.users = ZscalerCollection.form_list(config["users"] if "users" in config else [], common.ResourceReference)
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], common.ResourceReference)
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], common.ResourceReference
            )
            self.devices = ZscalerCollection.form_list(
                config["devices"] if "devices" in config else [], common.ResourceReference
            )
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], common.ResourceReference
            )
            self.device_trust_levels = ZscalerCollection.form_list(
                config["deviceTrustLevels"] if "deviceTrustLevels" in config else [], str
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], common.ResourceReference
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], common.ResourceReference)
            self.end_point_applications = ZscalerCollection.form_list(
                config["endPointApplications"] if "endPointApplications" in config else [], EndPointApplication
            )
            self.end_point_application_groups = ZscalerCollection.form_list(
                config["endPointApplicationGroups"] if "endPointApplicationGroups" in config else [], EndPointApplicationGroup
            )
            self.resources = ZscalerCollection.form_list(
                config["resources"] if "resources" in config else [], common.ResourceReference
            )
            self.resource_groups = ZscalerCollection.form_list(
                config["resourceGroups"] if "resourceGroups" in config else [], common.ResourceReference
            )
            self.user_risk_score_levels = ZscalerCollection.form_list(
                config["userRiskScoreLevels"] if "userRiskScoreLevels" in config else [], str
            )
            self.sub_rules = ZscalerCollection.form_list(config["subRules"] if "subRules" in config else [], SubRule)

            if "notificationTemplate" in config:
                if isinstance(config["notificationTemplate"], common.CommonBlocks):
                    self.notification_template = config["notificationTemplate"]
                elif config["notificationTemplate"] is not None:
                    self.notification_template = common.CommonBlocks(config["notificationTemplate"])
                else:
                    self.notification_template = None
            else:
                self.notification_template = None

            if "auditor" in config:
                if isinstance(config["auditor"], common.CommonBlocks):
                    self.auditor = config["auditor"]
                elif config["auditor"] is not None:
                    self.auditor = common.CommonBlocks(config["auditor"])
                else:
                    self.auditor = None
            else:
                self.auditor = None

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
                if isinstance(config["receiver"], Receiver):
                    self.receiver = config["receiver"]
                elif config["receiver"] is not None:
                    self.receiver = Receiver(config["receiver"])
                else:
                    self.receiver = None
            else:
                self.receiver = None
        else:
            self.id = None
            self.name = None
            self.state = None
            self.order = None
            self.rank = None
            self.file_types = None
            self.data_transfer_method = None
            self.description = None
            self.min_size = None
            self.action = None
            self.external_auditor_email = None
            self.last_modified_time = None
            self.parent_rule = None
            self.severity = None
            self.eun_enabled = None
            self.eun_template_id = None
            self.uc_template_id = None
            self.network_type = None
            self.without_content_inspection = None
            self.dlp_engines = []
            self.users = []
            self.groups = []
            self.departments = []
            self.devices = []
            self.device_groups = []
            self.device_trust_levels = []
            self.time_windows = []
            self.labels = []
            self.end_point_applications = []
            self.end_point_application_groups = []
            self.resources = []
            self.resource_groups = []
            self.user_risk_score_levels = []
            self.sub_rules = []
            self.notification_template = None
            self.auditor = None
            self.last_modified_by = None
            self.receiver = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "order": self.order,
            "rank": self.rank,
            "fileTypes": self.file_types,
            "dataTransferMethod": self.data_transfer_method,
            "description": self.description,
            "minSize": self.min_size,
            "action": self.action,
            "externalAuditorEmail": self.external_auditor_email,
            "lastModifiedTime": self.last_modified_time,
            "parentRule": self.parent_rule,
            "severity": self.severity,
            "eunEnabled": self.eun_enabled,
            "eunTemplateId": self.eun_template_id,
            "ucTemplateId": self.uc_template_id,
            "networkType": self.network_type,
            "withoutContentInspection": self.without_content_inspection,
            "dlpEngines": [item.request_format() for item in (self.dlp_engines or [])],
            "users": [item.request_format() for item in (self.users or [])],
            "groups": [item.request_format() for item in (self.groups or [])],
            "departments": [item.request_format() for item in (self.departments or [])],
            "devices": [item.request_format() for item in (self.devices or [])],
            "deviceGroups": [item.request_format() for item in (self.device_groups or [])],
            "deviceTrustLevels": self.device_trust_levels,
            "timeWindows": [item.request_format() for item in (self.time_windows or [])],
            "labels": [item.request_format() for item in (self.labels or [])],
            "endPointApplications": [item.request_format() for item in (self.end_point_applications or [])],
            "endPointApplicationGroups": [item.request_format() for item in (self.end_point_application_groups or [])],
            "resources": [item.request_format() for item in (self.resources or [])],
            "resourceGroups": [item.request_format() for item in (self.resource_groups or [])],
            "userRiskScoreLevels": self.user_risk_score_levels,
            "subRules": [item.request_format() for item in (self.sub_rules or [])],
            "notificationTemplate": self.notification_template,
            "auditor": self.auditor,
            "lastModifiedBy": self.last_modified_by,
            "receiver": self.receiver,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class EndPointApplication(ZscalerObject):
    """
    A class for EndPointApplication objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EndPointApplication model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.resource_id = config["resourceId"] if "resourceId" in config else None
            self.description = config["description"] if "description" in config else None
            self.os_type = config["osType"] if "osType" in config else None
            self.application_name = config["applicationName"] if "applicationName" in config else None
            self.bundle_id = config["bundleID"] if "bundleID" in config else None
            self.filename = config["filename"] if "filename" in config else None
            self.original_file_name = config["originalFileName"] if "originalFileName" in config else None
            self.digitally_signed = config["digitallySigned"] if "digitallySigned" in config else None
            self.mod_uid = config["modUId"] if "modUId" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.application_type = config["applicationType"] if "applicationType" in config else None
            self.zapp_id = config["zappId"] if "zappId" in config else None
            self.deleted = config["deleted"] if "deleted" in config else None
            self.versions = ZscalerCollection.form_list(config["versions"] if "versions" in config else [], Version)

            if "version" in config:
                if isinstance(config["version"], Version):
                    self.version = config["version"]
                elif config["version"] is not None:
                    self.version = Version(config["version"])
                else:
                    self.version = None
            else:
                self.version = None
        else:
            self.resource_id = None
            self.description = None
            self.os_type = None
            self.application_name = None
            self.bundle_id = None
            self.filename = None
            self.original_file_name = None
            self.digitally_signed = None
            self.mod_uid = None
            self.last_modified_time = None
            self.application_type = None
            self.zapp_id = None
            self.deleted = None
            self.versions = []
            self.version = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "resourceId": self.resource_id,
            "description": self.description,
            "osType": self.os_type,
            "applicationName": self.application_name,
            "bundleID": self.bundle_id,
            "filename": self.filename,
            "originalFileName": self.original_file_name,
            "digitallySigned": self.digitally_signed,
            "modUId": self.mod_uid,
            "lastModifiedTime": self.last_modified_time,
            "applicationType": self.application_type,
            "zappId": self.zapp_id,
            "deleted": self.deleted,
            "versions": [item.request_format() for item in (self.versions or [])],
            "version": self.version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Version(ZscalerObject):
    """
    A class for Version objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Version model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.version = config["version"] if "version" in config else None
            self.z_ver_id_md32 = config["z_ver_id_md32"] if "z_ver_id_md32" in config else None
            self.threat_type = config["threat_type"] if "threat_type" in config else None
            self.threat_level = config["threat_level"] if "threat_level" in config else None
            self.bundle_id = config["bundle_id"] if "bundle_id" in config else None
            self.code_signing_certificate_status = (
                config["code_signing_certificate_status"] if "code_signing_certificate_status" in config else None
            )
            self.threat_level_updated = config["threatLevelUpdated"] if "threatLevelUpdated" in config else None
        else:
            self.version = None
            self.z_ver_id_md32 = None
            self.threat_type = None
            self.threat_level = None
            self.bundle_id = None
            self.code_signing_certificate_status = None
            self.threat_level_updated = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "version": self.version,
            "z_ver_id_md32": self.z_ver_id_md32,
            "threat_type": self.threat_type,
            "threat_level": self.threat_level,
            "bundle_id": self.bundle_id,
            "code_signing_certificate_status": self.code_signing_certificate_status,
            "threatLevelUpdated": self.threat_level_updated,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class EndPointApplicationGroup(ZscalerObject):
    """
    A class for EndPointApplicationGroup objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EndPointApplicationGroup model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.group_id = config["groupId"] if "groupId" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.mod_uid = config["modUId"] if "modUId" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.end_point_applications = ZscalerCollection.form_list(
                config["endPointApplications"] if "endPointApplications" in config else [], EndPointApplication
            )
        else:
            self.group_id = None
            self.name = None
            self.description = None
            self.mod_uid = None
            self.last_modified_time = None
            self.end_point_applications = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "groupId": self.group_id,
            "name": self.name,
            "description": self.description,
            "modUId": self.mod_uid,
            "lastModifiedTime": self.last_modified_time,
            "endPointApplications": [item.request_format() for item in (self.end_point_applications or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Receiver(ZscalerObject):
    """
    A class for Receiver objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Receiver model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.type = config["type"] if "type" in config else None

            if "tenant" in config:
                if isinstance(config["tenant"], common.CommonBlocks):
                    self.tenant = config["tenant"]
                elif config["tenant"] is not None:
                    self.tenant = common.CommonBlocks(config["tenant"])
                else:
                    self.tenant = None
            else:
                self.tenant = None
        else:
            self.id = None
            self.name = None
            self.type = None
            self.tenant = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "tenant": self.tenant,
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
            self.name = config["name"] if "name" in config else None
            self.state = config["state"] if "state" in config else None
            self.order = config["order"] if "order" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.file_types = config["fileTypes"] if "fileTypes" in config else None
            self.data_transfer_method = config["dataTransferMethod"] if "dataTransferMethod" in config else None
            self.description = config["description"] if "description" in config else None
            self.min_size = config["minSize"] if "minSize" in config else None
            self.action = config["action"] if "action" in config else None
            self.external_auditor_email = config["externalAuditorEmail"] if "externalAuditorEmail" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.parent_rule = config["parentRule"] if "parentRule" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.eun_enabled = config["eunEnabled"] if "eunEnabled" in config else None
            self.eun_template_id = config["eunTemplateId"] if "eunTemplateId" in config else None
            self.uc_template_id = config["ucTemplateId"] if "ucTemplateId" in config else None
            self.network_type = config["networkType"] if "networkType" in config else None
            self.without_content_inspection = (
                config["withoutContentInspection"] if "withoutContentInspection" in config else None
            )
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], common.ResourceReference
            )
            self.users = ZscalerCollection.form_list(config["users"] if "users" in config else [], common.ResourceReference)
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], common.ResourceReference)
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], common.ResourceReference
            )
            self.devices = ZscalerCollection.form_list(
                config["devices"] if "devices" in config else [], common.ResourceReference
            )
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], common.ResourceReference
            )
            self.device_trust_levels = ZscalerCollection.form_list(
                config["deviceTrustLevels"] if "deviceTrustLevels" in config else [], str
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], common.ResourceReference
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], common.ResourceReference)
            self.end_point_applications = ZscalerCollection.form_list(
                config["endPointApplications"] if "endPointApplications" in config else [], EndPointApplication
            )
            self.end_point_application_groups = ZscalerCollection.form_list(
                config["endPointApplicationGroups"] if "endPointApplicationGroups" in config else [], EndPointApplicationGroup
            )
            self.resources = ZscalerCollection.form_list(
                config["resources"] if "resources" in config else [], common.ResourceReference
            )
            self.resource_groups = ZscalerCollection.form_list(
                config["resourceGroups"] if "resourceGroups" in config else [], common.ResourceReference
            )
            self.user_risk_score_levels = ZscalerCollection.form_list(
                config["userRiskScoreLevels"] if "userRiskScoreLevels" in config else [], str
            )

            if "notificationTemplate" in config:
                if isinstance(config["notificationTemplate"], common.CommonBlocks):
                    self.notification_template = config["notificationTemplate"]
                elif config["notificationTemplate"] is not None:
                    self.notification_template = common.CommonBlocks(config["notificationTemplate"])
                else:
                    self.notification_template = None
            else:
                self.notification_template = None

            if "auditor" in config:
                if isinstance(config["auditor"], common.CommonBlocks):
                    self.auditor = config["auditor"]
                elif config["auditor"] is not None:
                    self.auditor = common.CommonBlocks(config["auditor"])
                else:
                    self.auditor = None
            else:
                self.auditor = None

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
                if isinstance(config["receiver"], Receiver):
                    self.receiver = config["receiver"]
                elif config["receiver"] is not None:
                    self.receiver = Receiver(config["receiver"])
                else:
                    self.receiver = None
            else:
                self.receiver = None
        else:
            self.id = None
            self.name = None
            self.state = None
            self.order = None
            self.rank = None
            self.file_types = None
            self.data_transfer_method = None
            self.description = None
            self.min_size = None
            self.action = None
            self.external_auditor_email = None
            self.last_modified_time = None
            self.parent_rule = None
            self.severity = None
            self.eun_enabled = None
            self.eun_template_id = None
            self.uc_template_id = None
            self.network_type = None
            self.without_content_inspection = None
            self.dlp_engines = []
            self.users = []
            self.groups = []
            self.departments = []
            self.devices = []
            self.device_groups = []
            self.device_trust_levels = []
            self.time_windows = []
            self.labels = []
            self.end_point_applications = []
            self.end_point_application_groups = []
            self.resources = []
            self.resource_groups = []
            self.user_risk_score_levels = []
            self.notification_template = None
            self.auditor = None
            self.last_modified_by = None
            self.receiver = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "order": self.order,
            "rank": self.rank,
            "fileTypes": self.file_types,
            "dataTransferMethod": self.data_transfer_method,
            "description": self.description,
            "minSize": self.min_size,
            "action": self.action,
            "externalAuditorEmail": self.external_auditor_email,
            "lastModifiedTime": self.last_modified_time,
            "parentRule": self.parent_rule,
            "severity": self.severity,
            "eunEnabled": self.eun_enabled,
            "eunTemplateId": self.eun_template_id,
            "ucTemplateId": self.uc_template_id,
            "networkType": self.network_type,
            "withoutContentInspection": self.without_content_inspection,
            "dlpEngines": [item.request_format() for item in (self.dlp_engines or [])],
            "users": [item.request_format() for item in (self.users or [])],
            "groups": [item.request_format() for item in (self.groups or [])],
            "departments": [item.request_format() for item in (self.departments or [])],
            "devices": [item.request_format() for item in (self.devices or [])],
            "deviceGroups": [item.request_format() for item in (self.device_groups or [])],
            "deviceTrustLevels": self.device_trust_levels,
            "timeWindows": [item.request_format() for item in (self.time_windows or [])],
            "labels": [item.request_format() for item in (self.labels or [])],
            "endPointApplications": [item.request_format() for item in (self.end_point_applications or [])],
            "endPointApplicationGroups": [item.request_format() for item in (self.end_point_application_groups or [])],
            "resources": [item.request_format() for item in (self.resources or [])],
            "resourceGroups": [item.request_format() for item in (self.resource_groups or [])],
            "userRiskScoreLevels": self.user_risk_score_levels,
            "notificationTemplate": self.notification_template,
            "auditor": self.auditor,
            "lastModifiedBy": self.last_modified_by,
            "receiver": self.receiver,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
