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
from zscaler.zia.models import common
from zscaler.zia.models import dlp_engine as dlp_engine
from zscaler.zia.models import rule_labels as labels
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import saas_security_api as saas_security_api


class CasbdDlpRules(ZscalerObject):
    """
    A class for CasbdDlpRules objects.
    """

    def __init__(self, config=None):
        """
        Initialize the CasbdDlpRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.type = config["type"] \
                if "type" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.order = config["order"] \
                if "order" in config else None
            self.rank = config["rank"] \
                if "rank" in config else None
            self.action = config["action"] \
                if "action" in config else None
            self.severity = config["severity"] \
                if "severity" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.state = config["state"] \
                if "state" in config else None
            self.include_criteria_domain_profile = config["includeCriteriaDomainProfile"] \
                if "includeCriteriaDomainProfile" in config else None
            self.include_email_recipient_profile = config["includeEmailRecipientProfile"] \
                if "includeEmailRecipientProfile" in config else None
            self.bucket_owner = config["bucketOwner"] \
                if "bucketOwner" in config else None
            self.content_location = config["contentLocation"] \
                if "contentLocation" in config else None
            self.watermark_delete_old_version = config["watermarkDeleteOldVersion"] \
                if "watermarkDeleteOldVersion" in config else None
            self.number_of_internal_collaborators = config["numberOfInternalCollaborators"] \
                if "numberOfInternalCollaborators" in config else None
            self.number_of_external_collaborators = config["numberOfExternalCollaborators"] \
                if "numberOfExternalCollaborators" in config else None
            self.external_auditor_email = config["externalAuditorEmail"] \
                if "externalAuditorEmail" in config else None
            self.recipient = config["recipient"] \
                if "recipient" in config else None
            self.last_modified_time = config["lastModifiedTime"] \
                if "lastModifiedTime" in config else None
            self.without_content_inspection = config["withoutContentInspection"] \
                if "withoutContentInspection" in config else None
            self.quarantine_location = config["quarantineLocation"] \
                if "quarantineLocation" in config else None
            self.include_entity_groups = config["includeEntityGroups"] \
                if "includeEntityGroups" in config else None
            self.access_control = config["accessControl"] \
                if "accessControl" in config else None

            self.file_types = ZscalerCollection.form_list(
                config["fileTypes"] if "fileTypes" in config else [], str
            )
            self.collaboration_scope = ZscalerCollection.form_list(
                config["collaborationScope"] if "collaborationScope" in config else [], str
            )
            self.domains = ZscalerCollection.form_list(
                config["domains"] if "domains" in config else [], str
            )
            self.components = ZscalerCollection.form_list(
                config["components"] if "components" in config else [], str
            )

            self.cloud_app_tenants = ZscalerCollection.form_list(
                config["cloudAppTenants"] if "cloudAppTenants" in config else [], saas_security_api.CasbTenant
            )

            self.entity_groups = ZscalerCollection.form_list(
                config["entityGroups"] if "entityGroups" in config else [], common.ResourceReference
            )
            self.included_domain_profiles = ZscalerCollection.form_list(
                config["includedDomainProfiles"] if "includedDomainProfiles" in config else [], common.ResourceReference
            )
            self.excluded_domain_profiles = ZscalerCollection.form_list(
                config["excludedDomainProfiles"] if "excludedDomainProfiles" in config else [], common.ResourceReference
            )
            self.criteria_domain_profiles = ZscalerCollection.form_list(
                config["criteriaDomainProfiles"] if "criteriaDomainProfiles" in config else [], common.ResourceReference
            )
            self.email_recipient_profiles = ZscalerCollection.form_list(
                config["emailRecipientProfiles"] if "emailRecipientProfiles" in config else [], common.ResourceReference
            )
            self.buckets = ZscalerCollection.form_list(
                config["buckets"] if "buckets" in config else [], common.ResourceReference
            )
            self.object_types = ZscalerCollection.form_list(
                config["objectTypes"] if "objectTypes" in config else [], common.ResourceReference
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.groups = ZscalerCollection.form_list(
                config["groups"] if "groups" in config else [], user_management.Groups)

            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], dlp_engine.DLPEngine
            )
            self.labels = ZscalerCollection.form_list(
                config["labels"] if "labels" in config else [], labels.RuleLabels
            )

            if "zscalerIncidentReceiver" in config:
                if isinstance(config["zscalerIncidentReceiver"], common.CommonIDName):
                    self.zscaler_incident_receiver = config["zscalerIncidentReceiver"]
                elif config["zscalerIncidentReceiver"] is not None:
                    self.zscaler_incident_receiver = common.CommonIDName(config["zscalerIncidentReceiver"])
                else:
                    self.zscaler_incident_receiver = None
            else:
                self.zscaler_incident_receiver = None

            if "auditor" in config:
                if isinstance(config["auditor"], common.CommonIDName):
                    self.auditor = config["auditor"]
                elif config["auditor"] is not None:
                    self.auditor = common.CommonIDName(config["auditor"])
                else:
                    self.auditor = None
            else:
                self.auditor = None
            if "auditorNotification" in config:
                if isinstance(config["auditorNotification"], common.CommonIDName):
                    self.auditor_notification = config["auditorNotification"]
                elif config["auditorNotification"] is not None:
                    self.auditor_notification = common.CommonIDName(config["auditorNotification"])
                else:
                    self.auditor_notification = None
            else:
                self.auditor_notification = None

            if "tag" in config:
                if isinstance(config["tag"], common.CommonIDName):
                    self.tag = config["tag"]
                elif config["tag"] is not None:
                    self.tag = common.CommonIDName(config["tag"])
                else:
                    self.tag = None
            else:
                self.tag = None

            if "watermarkProfile" in config:
                if isinstance(config["watermarkProfile"], common.CommonIDName):
                    self.watermark_profile = config["watermarkProfile"]
                elif config["watermarkProfile"] is not None:
                    self.watermark_profile = common.CommonIDName(config["watermarkProfile"])
                else:
                    self.watermark_profile = None
            else:
                self.watermark_profile = None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            if "redactionProfile" in config:
                if isinstance(config["redactionProfile"], common.CommonBlocks):
                    self.redaction_profile = config["redactionProfile"]
                elif config["redactionProfile"] is not None:
                    self.redaction_profile = common.CommonBlocks(config["redactionProfile"])
                else:
                    self.redaction_profile = None
            else:
                self.redaction_profile = None

            if "casbEmailLabel" in config:
                if isinstance(config["casbEmailLabel"], saas_security_api.CasbEmailLabel):
                    self.casb_email_label = config["casbEmailLabel"]
                elif config["casbEmailLabel"] is not None:
                    self.casb_email_label = saas_security_api.CasbEmailLabel(config["casbEmailLabel"])
                else:
                    self.casb_email_label = None
            else:
                self.casb_email_label = None

            if "casbTombstoneTemplate" in config:
                if isinstance(config["casbTombstoneTemplate"], saas_security_api.QuarantineTombstoneTemplate):
                    self.casb_tombstone_template = config["casbTombstoneTemplate"]
                elif config["casbTombstoneTemplate"] is not None:
                    self.casb_tombstone_template = saas_security_api.QuarantineTombstoneTemplate
                    (config["casbTombstoneTemplate"])
                else:
                    self.casb_tombstone_template = None
            else:
                self.casb_tombstone_template = None

        else:
            self.type = None
            self.id = None
            self.order = None
            self.rank = None
            self.name = None
            self.state = None
            self.cloud_app_tenants = []
            self.users = []
            self.groups = []
            self.departments = []
            self.dlp_engines = []
            self.action = None
            self.severity = None
            self.description = None
            self.file_types = []
            self.collaboration_scope = []
            self.content_location = None
            self.domains = []
            self.object_types = []
            self.components = []
            self.buckets = []
            self.bucket_owner = None
            self.zscaler_incident_receiver = None
            self.external_auditor_email = None
            self.auditor = None
            self.auditor_notification = None
            self.tag = None
            self.watermark_profile = None
            self.watermark_delete_old_version = None
            self.number_of_internal_collaborators = None
            self.number_of_external_collaborators = None
            self.recipient = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.quarantine_location = None
            self.access_control = None
            self.redaction_profile = None
            self.labels = []
            self.casb_email_label = None
            self.casb_tombstone_template = None
            self.included_domain_profiles = []
            self.excluded_domain_profiles = []
            self.criteria_domain_profiles = []
            self.email_recipient_profiles = []
            self.include_criteria_domain_profile = None
            self.include_email_recipient_profile = None
            self.without_content_inspection = None
            self.entity_groups = []
            self.include_entity_groups = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "type": self.type,
            "id": self.id,
            "order": self.order,
            "rank": self.rank,
            "name": self.name,
            "state": self.state,
            "cloudAppTenants": self.cloud_app_tenants,
            "users": self.users,
            "groups": self.groups,
            "departments": self.departments,
            "dlpEngines": self.dlp_engines,
            "action": self.action,
            "severity": self.severity,
            "description": self.description,
            "fileTypes": self.file_types,
            "collaborationScope": self.collaboration_scope,
            "contentLocation": self.content_location,
            "domains": self.domains,
            "objectTypes": self.object_types,
            "components": self.components,
            "buckets": self.buckets,
            "bucketOwner": self.bucket_owner,
            "zscalerIncidentReceiver": self.zscaler_incident_receiver,
            "externalAuditorEmail": self.external_auditor_email,
            "auditor": self.auditor,
            "auditorNotification": self.auditor_notification,
            "tag": self.tag,
            "watermarkProfile": self.watermark_profile,
            "watermarkDeleteOldVersion": self.watermark_delete_old_version,
            "numberOfInternalCollaborators": self.number_of_internal_collaborators,
            "numberOfExternalCollaborators": self.number_of_external_collaborators,
            "recipient": self.recipient,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "quarantineLocation": self.quarantine_location,
            "accessControl": self.access_control,
            "redactionProfile": self.redaction_profile,
            "labels": self.labels,
            "casbEmailLabel": self.casb_email_label,
            "casbTombstoneTemplate": self.casb_tombstone_template,
            "includedDomainProfiles": self.included_domain_profiles,
            "excludedDomainProfiles": self.excluded_domain_profiles,
            "criteriaDomainProfiles": self.criteria_domain_profiles,
            "emailRecipientProfiles": self.email_recipient_profiles,
            "includeCriteriaDomainProfile": self.include_criteria_domain_profile,
            "includeEmailRecipientProfile": self.include_email_recipient_profile,
            "withoutContentInspection": self.without_content_inspection,
            "entityGroups": self.entity_groups,
            "includeEntityGroups": self.include_entity_groups
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
