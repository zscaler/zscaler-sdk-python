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

from zscaler.zia.models import admin_users as admin_users
from zscaler.zia.models import dlp_engine as dlp_engine
from zscaler.zia.models import dlp_templates as dlp_templates
from zscaler.zia.models import dlp_resources as dlp_resources
from zscaler.zia.models import cloud_firewall_source_groups as cloud_firewall_source_groups
from zscaler.zia.models import location_group as location_group
from zscaler.zia.models import location_management as location_management
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import urlcategory as urlcategory
from zscaler.zia.models import rule_labels as labels
from zscaler.zia.models import workload_groups as workload_groups
from zscaler.zia.models import common as common_reference


class DLPWebRules(ZscalerObject):
    """
    A class representing a DLP Web Rule object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.access_control = config["accessControl"] if "accessControl" in config else None
            self.min_size = config["minSize"] if "minSize" in config else None
            self.action = config["action"] if "action" in config else None
            self.state = config["state"] if "state" in config else None
            self.match_only = config["matchOnly"] if "matchOnly" in config else False
            self.without_content_inspection = (
                config["withoutContentInspection"] if "withoutContentInspection" in config else False
            )
            self.inspect_http_get_enabled = config["inspectHttpGetEnabled"] if "inspectHttpGetEnabled" in config else False
            self.dlp_download_scan_enabled = config["dlpDownloadScanEnabled"] if "dlpDownloadScanEnabled" in config else False
            self.zcc_notifications_enabled = (
                config["zccNotificationsEnabled"] if "zccNotificationsEnabled" in config else False
            )
            self.severity = config["severity"] if "severity" in config else None
            self.parent_rule = config["parentRule"] if "parentRule" in config else None
            self.sub_rules = config["subRules"] if "subRules" in config else None
            self.order = config["order"] if "order" in config else None
            self.eun_template_id = config["eunTemplateId"] if "eunTemplateId" in config else None
            self.inspect_http_get_enabled = config["inspectHttpGetEnabled"] if "inspectHttpGetEnabled" in config else None
            self.zscaler_incident_receiver = config["zscalerIncidentReceiver"] if "zscalerIncidentReceiver" in config else None
            self.external_auditor_email = config["externalAuditorEmail"] if "externalAuditorEmail" in config else None

            self.protocols = ZscalerCollection.form_list(config["protocols"] if "protocols" in config else [], str)

            self.file_types = ZscalerCollection.form_list(config["fileTypes"] if "fileTypes" in config else [], str)

            self.cloud_applications = ZscalerCollection.form_list(
                config["cloudApplications"] if "cloudApplications" in config else [], str
            )
            self.user_risk_score_levels = ZscalerCollection.form_list(
                config["userRiskScoreLevels"] if "userRiskScoreLevels" in config else [], str
            )
            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], common_reference.ResourceReference
            )

            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.location_groups = ZscalerCollection.form_list(
                config["locationGroups"] if "locationGroups" in config else [], location_group.LocationGroup
            )
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], user_management.Groups)
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.workload_groups = ZscalerCollection.form_list(
                config["workloadGroups"] if "workloadGroups" in config else [], workload_groups.WorkloadGroups
            )
            self.included_domain_profiles = ZscalerCollection.form_list(
                config["includedDomainProfiles"] if "includedDomainProfiles" in config else [],
                common_reference.ResourceReference,
            )
            self.excluded_domain_profiles = ZscalerCollection.form_list(
                config["excludedDomainProfiles"] if "excludedDomainProfiles" in config else [],
                common_reference.ResourceReference,
            )
            self.source_ip_groups = ZscalerCollection.form_list(
                config["sourceIpGroups"] if "sourceIpGroups" in config else [], cloud_firewall_source_groups.IPSourceGroup
            )

            self.zpa_app_segments = ZscalerCollection.form_list(
                config["zpaAppSegments"] if "zpaAppSegments" in config else [], common_reference.ResourceReference
            )
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], dlp_engine.DLPEngine
            )
            self.labels = ZscalerCollection.form_list(
                config["labels"] if "labels" in config else [], labels.RuleLabels
            )
            self.excluded_groups = ZscalerCollection.form_list(
                config["excludedGroups"] if "excludedGroups" in config else [], user_management.Groups
            )
            self.excluded_departments = ZscalerCollection.form_list(
                config["excludedDepartments"] if "excludedDepartments" in config else [], user_management.Department
            )
            self.excluded_users = ZscalerCollection.form_list(
                config["excludedUsers"] if "excludedUsers" in config else [], user_management.UserManagement
            )

            self.auditor = admin_users.AdminUser(config["auditor"]) if "auditor" in config else None

            self.notification_template = (
                dlp_templates.DLPTemplates(config["notificationTemplate"]) if "notificationTemplate" in config else None
            )

            self.icap_server = dlp_resources.DLPICAPServer(config["icapServer"]) if "icapServer" in config else None

        else:
            self.id = None
            self.name = None
            self.description = None
            self.rank = None
            self.access_control = None
            self.min_size = None
            self.action = None
            self.state = None
            self.match_only = False
            self.without_content_inspection = False
            self.inspect_http_get_enabled = False
            self.dlp_download_scan_enabled = False
            self.zcc_notifications_enabled = False
            self.severity = None
            self.parent_rule = None
            self.sub_rules = []
            self.order = None
            self.eun_template_id = None
            self.zscaler_incident_receiver = None
            self.protocols = []
            self.file_types = []
            self.cloud_applications = []
            self.locations = []
            self.location_groups = []
            self.groups = []
            self.departments = []
            self.users = []
            self.url_categories = []
            self.zpa_app_segments = []
            self.workload_groups = []
            self.included_domain_profiles = []
            self.excluded_domain_profiles = []
            self.source_ip_groups = []
            self.labels = []
            self.excluded_groups = []
            self.excluded_departments = []
            self.excluded_users = []
            self.user_risk_score_levels = []
            self.auditor = None
            self.notification_template = None
            self.icap_server = None
            self.external_auditor_email = None  # New attribute

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rank": self.rank,
            "accessControl": self.access_control,
            "minSize": self.min_size,
            "action": self.action,
            "state": self.state,
            "matchOnly": self.match_only,
            "withoutContentInspection": self.without_content_inspection,
            "inspectHttpGetEnabled": self.inspect_http_get_enabled,
            "dlpDownloadScanEnabled": self.dlp_download_scan_enabled,
            "zccNotificationsEnabled": self.zcc_notifications_enabled,
            "severity": self.severity,
            "parentRule": self.parent_rule,
            "subRules": self.sub_rules,
            "order": self.order,
            "eunTemplateId": self.eun_template_id,
            "zscalerIncidentReceiver": self.zscaler_incident_receiver,
            "protocols": self.protocols,
            "fileTypes": self.file_types,
            "cloudApplications": self.cloud_applications,
            "userRiskScoreLevels": self.user_risk_score_levels,
            "locations": [location.request_format() for location in (self.locations or [])],
            "locationGroups": [group.request_format() for group in (self.location_groups or [])],
            "groups": [group.request_format() for group in (self.groups or [])],
            "departments": [department.request_format() for department in (self.departments or [])],
            "users": [user.request_format() for user in (self.users or [])],
            "urlCategories": [url_category.request_format() for url_category in (self.url_categories or [])],
            "zpaAppSegments": [segment.request_format() for segment in (self.zpa_app_segments or [])],
            "workloadGroups": [group.request_format() for group in (self.workload_groups or [])],
            "includedDomainProfiles": [profile.request_format() for profile in (self.included_domain_profiles or [])],
            "excludedDomainProfiles": [
                exclude_profile.request_format() for exclude_profile in (self.excluded_domain_profiles or [])
            ],
            "sourceIpGroups": [group.request_format() for group in (self.source_ip_groups or [])],
            "labels": [label.request_format() for label in (self.labels or [])],
            "excludedGroups": [group.request_format() for group in (self.excluded_groups or [])],  # New Attribute
            "excludedDepartments": [
                department.request_format() for department in (self.excluded_departments or [])
            ],  # New Attribute
            "excludedUsers": [user.request_format() for user in (self.excluded_users or [])],  # New Attribute
            "auditor": self.auditor.request_format() if self.auditor else None,
            "notificationTemplate": self.notification_template.request_format() if self.notification_template else None,
            "icapServer": self.icap_server.request_format() if self.icap_server else None,
            "externalAuditorEmail": self.external_auditor_email,  # New Attribute
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
