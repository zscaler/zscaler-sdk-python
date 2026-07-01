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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject
from zscaler.zia.models import common as common
from zscaler.zia.models import location_management as location_management
from zscaler.zia.models import user_management as user_management


class AlertDefinition(ZscalerObject):
    """
    A class representing a AlertDefinition object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.status = config["status"] if "status" in config else None
            self.alert_name = config["alertName"] if "alertName" in config else None
            self.occurrence = config["occurrence"] if "occurrence" in config else None
            self.traffic_change_percent = config["trafficChangePercent"] if "trafficChangePercent" in config else None
            self.interval = config["interval"] if "interval" in config else None
            self.scope = config["scope"] if "scope" in config else None
            if "entity" in config:
                if isinstance(config["entity"], common.CommonBlocks):
                    self.entity = config["entity"]
                elif config["entity"] is not None:
                    self.entity = common.CommonBlocks(config["entity"])
                else:
                    self.entity = None
            else:
                self.entity = None
            self.severity = config["severity"] if "severity" in config else None
            self.comments = config["comments"] if "comments" in config else None
        else:
            self.id = None
            self.status = None
            self.alert_name = None
            self.occurrence = None
            self.traffic_change_percent = None
            self.interval = None
            self.scope = None
            self.entity = None
            self.severity = None
            self.comments = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "status": self.status,
            "alertName": self.alert_name,
            "occurrence": self.occurrence,
            "trafficChangePercent": self.traffic_change_percent,
            "interval": self.interval,
            "scope": self.scope,
            "entity": self.entity,
            "severity": self.severity,
            "comments": self.comments,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlertRuleConfiguration(ZscalerObject):
    """
    A class representing a AlertRuleConfiguration object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.alert_name = config["alertName"] if "alertName" in config else None
            self.alert_class = config["alertClass"] if "alertClass" in config else None
            self.status = config["status"] if "status" in config else None
            self.event_types = ZscalerCollection.form_list(config["eventTypes"] if "eventTypes" in config else [], str)
            self.within_time = config["withinTime"] if "withinTime" in config else None
            self.min_times = config["minTimes"] if "minTimes" in config else None
            self.window_size = config["windowSize"] if "windowSize" in config else None
            self.enable_update = config["enableUpdate"] if "enableUpdate" in config else False
            self.update_window_size = config["updateWindowSize"] if "updateWindowSize" in config else None
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.num_system_impacted = config["numSystemImpacted"] if "numSystemImpacted" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None
            self.webhooks = ZscalerCollection.form_list(config["webhooks"] if "webhooks" in config else [], str)
            self.email_ids = ZscalerCollection.form_list(config["emailIds"] if "emailIds" in config else [], str)
            self.channel = config["channel"] if "channel" in config else None
            self.alert_type = config["alertType"] if "alertType" in config else None
            self.action = config["action"] if "action" in config else None
            self.action_threshold = config["actionThreshold"] if "actionThreshold" in config else None
            self.countries = ZscalerCollection.form_list(config["countries"] if "countries" in config else [], str)
            self.casb_applications = ZscalerCollection.form_list(
                config["casbApplications"] if "casbApplications" in config else [], common.CommonBlocks
            )
            self.object_types = ZscalerCollection.form_list(config["objectTypes"] if "objectTypes" in config else [], str)
            self.doc_types = ZscalerCollection.form_list(config["docTypes"] if "docTypes" in config else [], str)
            if "userGroupId" in config:
                if isinstance(config["userGroupId"], AlertRuleConfigurationUserGroupId):
                    self.user_group_id = config["userGroupId"]
                elif config["userGroupId"] is not None:
                    self.user_group_id = AlertRuleConfigurationUserGroupId(config["userGroupId"])
                else:
                    self.user_group_id = None
            else:
                self.user_group_id = None
            self.action_time_interval = config["actionTimeInterval"] if "actionTimeInterval" in config else None
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], AlertRuleConfigurationDlpEngines
            )
            self.activities = ZscalerCollection.form_list(config["activities"] if "activities" in config else [], str)
            self.id = config["id"] if "id" in config else None
        else:
            self.alert_name = None
            self.alert_class = None
            self.status = None
            self.event_types = []
            self.within_time = None
            self.min_times = None
            self.window_size = None
            self.enable_update = False
            self.update_window_size = None
            self.locations = []
            self.users = []
            self.departments = []
            self.num_system_impacted = None
            self.deleted = False
            self.last_modified_time = None
            self.last_modified_by = None
            self.webhooks = []
            self.email_ids = []
            self.channel = None
            self.alert_type = None
            self.action = None
            self.action_threshold = None
            self.countries = []
            self.casb_applications = []
            self.object_types = []
            self.doc_types = []
            self.user_group_id = None
            self.action_time_interval = None
            self.dlp_engines = []
            self.activities = []
            self.id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "alertName": self.alert_name,
            "alertClass": self.alert_class,
            "status": self.status,
            "eventTypes": self.event_types,
            "withinTime": self.within_time,
            "minTimes": self.min_times,
            "windowSize": self.window_size,
            "enableUpdate": self.enable_update,
            "updateWindowSize": self.update_window_size,
            "locations": [item.request_format() for item in (self.locations or [])],
            "users": [item.request_format() for item in (self.users or [])],
            "departments": [item.request_format() for item in (self.departments or [])],
            "numSystemImpacted": self.num_system_impacted,
            "deleted": self.deleted,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "webhooks": self.webhooks,
            "emailIds": self.email_ids,
            "channel": self.channel,
            "alertType": self.alert_type,
            "action": self.action,
            "actionThreshold": self.action_threshold,
            "countries": self.countries,
            "casbApplications": [item.request_format() for item in (self.casb_applications or [])],
            "objectTypes": self.object_types,
            "docTypes": self.doc_types,
            "userGroupId": self.user_group_id,
            "actionTimeInterval": self.action_time_interval,
            "dlpEngines": [item.request_format() for item in (self.dlp_engines or [])],
            "activities": self.activities,
            "id": self.id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlertRuleConfigurationUebaRule(ZscalerObject):
    """
    A class representing a AlertRuleConfigurationUebaRule object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.alert_name = config["alertName"] if "alertName" in config else None
            self.alert_class = config["alertClass"] if "alertClass" in config else None
            self.status = config["status"] if "status" in config else None
            self.event_types = ZscalerCollection.form_list(config["eventTypes"] if "eventTypes" in config else [], str)
            self.within_time = config["withinTime"] if "withinTime" in config else None
            self.min_times = config["minTimes"] if "minTimes" in config else None
            self.window_size = config["windowSize"] if "windowSize" in config else None
            self.enable_update = config["enableUpdate"] if "enableUpdate" in config else False
            self.update_window_size = config["updateWindowSize"] if "updateWindowSize" in config else None
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.num_system_impacted = config["numSystemImpacted"] if "numSystemImpacted" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None
            self.webhooks = ZscalerCollection.form_list(config["webhooks"] if "webhooks" in config else [], str)
            self.email_ids = ZscalerCollection.form_list(config["emailIds"] if "emailIds" in config else [], str)
            self.channel = config["channel"] if "channel" in config else None
            self.alert_type = config["alertType"] if "alertType" in config else None
            self.action = config["action"] if "action" in config else None
            self.action_threshold = config["actionThreshold"] if "actionThreshold" in config else None
            self.countries = ZscalerCollection.form_list(config["countries"] if "countries" in config else [], str)
            self.casb_applications = ZscalerCollection.form_list(
                config["casbApplications"] if "casbApplications" in config else [], common.CommonBlocks
            )
            self.object_types = ZscalerCollection.form_list(config["objectTypes"] if "objectTypes" in config else [], str)
            self.doc_types = ZscalerCollection.form_list(config["docTypes"] if "docTypes" in config else [], str)
            if "userGroupId" in config:
                if isinstance(config["userGroupId"], AlertRuleConfigurationUebaRuleUserGroupId):
                    self.user_group_id = config["userGroupId"]
                elif config["userGroupId"] is not None:
                    self.user_group_id = AlertRuleConfigurationUebaRuleUserGroupId(config["userGroupId"])
                else:
                    self.user_group_id = None
            else:
                self.user_group_id = None
            self.action_time_interval = config["actionTimeInterval"] if "actionTimeInterval" in config else None
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], AlertRuleConfigurationUebaRuleDlpEngines
            )
            self.activities = ZscalerCollection.form_list(config["activities"] if "activities" in config else [], str)
            self.id = config["id"] if "id" in config else None
        else:
            self.alert_name = None
            self.alert_class = None
            self.status = None
            self.event_types = []
            self.within_time = None
            self.min_times = None
            self.window_size = None
            self.enable_update = False
            self.update_window_size = None
            self.locations = []
            self.users = []
            self.departments = []
            self.num_system_impacted = None
            self.deleted = False
            self.last_modified_time = None
            self.last_modified_by = None
            self.webhooks = []
            self.email_ids = []
            self.channel = None
            self.alert_type = None
            self.action = None
            self.action_threshold = None
            self.countries = []
            self.casb_applications = []
            self.object_types = []
            self.doc_types = []
            self.user_group_id = None
            self.action_time_interval = None
            self.dlp_engines = []
            self.activities = []
            self.id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "alertName": self.alert_name,
            "alertClass": self.alert_class,
            "status": self.status,
            "eventTypes": self.event_types,
            "withinTime": self.within_time,
            "minTimes": self.min_times,
            "windowSize": self.window_size,
            "enableUpdate": self.enable_update,
            "updateWindowSize": self.update_window_size,
            "locations": [item.request_format() for item in (self.locations or [])],
            "users": [item.request_format() for item in (self.users or [])],
            "departments": [item.request_format() for item in (self.departments or [])],
            "numSystemImpacted": self.num_system_impacted,
            "deleted": self.deleted,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "webhooks": self.webhooks,
            "emailIds": self.email_ids,
            "channel": self.channel,
            "alertType": self.alert_type,
            "action": self.action,
            "actionThreshold": self.action_threshold,
            "countries": self.countries,
            "casbApplications": [item.request_format() for item in (self.casb_applications or [])],
            "objectTypes": self.object_types,
            "docTypes": self.doc_types,
            "userGroupId": self.user_group_id,
            "actionTimeInterval": self.action_time_interval,
            "dlpEngines": [item.request_format() for item in (self.dlp_engines or [])],
            "activities": self.activities,
            "id": self.id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlertRuleConfigurationWebhook(ZscalerObject):
    """
    A class representing a AlertRuleConfigurationWebhook object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.user_name = config["userName"] if "userName" in config else None
            self.password = config["password"] if "password" in config else None
            self.auth_token = config["authToken"] if "authToken" in config else None
            self.url_text = config["urlText"] if "urlText" in config else None
            self.status = config["status"] if "status" in config else False
            self.last_triggered = config["lastTriggered"] if "lastTriggered" in config else None
            self.authentication_type = config["authenticationType"] if "authenticationType" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None
        else:
            self.id = None
            self.name = None
            self.user_name = None
            self.password = None
            self.auth_token = None
            self.url_text = None
            self.status = False
            self.last_triggered = None
            self.authentication_type = None
            self.deleted = False
            self.last_modified_time = None
            self.last_modified_by = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "userName": self.user_name,
            "password": self.password,
            "authToken": self.auth_token,
            "urlText": self.url_text,
            "status": self.status,
            "lastTriggered": self.last_triggered,
            "authenticationType": self.authentication_type,
            "deleted": self.deleted,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlertRuleConfigurationUserGroupId(ZscalerObject):
    """
    A class representing a AlertRuleConfigurationUserGroupId object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.pid = config["pid"] if "pid" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.getl_id = config["getlId"] if "getlId" in config else None
        else:
            self.id = None
            self.pid = None
            self.name = None
            self.description = None
            self.deleted = False
            self.getl_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "pid": self.pid,
            "name": self.name,
            "description": self.description,
            "deleted": self.deleted,
            "getlId": self.getl_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlertRuleConfigurationDlpEngines(ZscalerObject):
    """
    A class representing a AlertRuleConfigurationDlpEngines object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.pid = config["pid"] if "pid" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.getl_id = config["getlId"] if "getlId" in config else None
        else:
            self.id = None
            self.pid = None
            self.name = None
            self.description = None
            self.deleted = False
            self.getl_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "pid": self.pid,
            "name": self.name,
            "description": self.description,
            "deleted": self.deleted,
            "getlId": self.getl_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlertRuleConfigurationUebaRuleUserGroupId(ZscalerObject):
    """
    A class representing a AlertRuleConfigurationUebaRuleUserGroupId object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.pid = config["pid"] if "pid" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.getl_id = config["getlId"] if "getlId" in config else None
        else:
            self.id = None
            self.pid = None
            self.name = None
            self.description = None
            self.deleted = False
            self.getl_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "pid": self.pid,
            "name": self.name,
            "description": self.description,
            "deleted": self.deleted,
            "getlId": self.getl_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlertRuleConfigurationUebaRuleDlpEngines(ZscalerObject):
    """
    A class representing a AlertRuleConfigurationUebaRuleDlpEngines object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.pid = config["pid"] if "pid" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.getl_id = config["getlId"] if "getlId" in config else None
        else:
            self.id = None
            self.pid = None
            self.name = None
            self.description = None
            self.deleted = False
            self.getl_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "pid": self.pid,
            "name": self.name,
            "description": self.description,
            "deleted": self.deleted,
            "getlId": self.getl_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
