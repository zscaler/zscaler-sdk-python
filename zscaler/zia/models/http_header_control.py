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


class HttpHeaderProfile(ZscalerObject):
    """
    A class representing a HttpHeaderProfile object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.slot_id = config["slotId"] if "slotId" in config else None
            self.http_header_profile_criteria = ZscalerCollection.form_list(
                config["httpHeaderProfileCriteria"] if "httpHeaderProfileCriteria" in config else [],
                HttpHeaderProfileHttpHeaderProfileCriteria,
            )
            self.deleted = config["deleted"] if "deleted" in config else False
            self.profile_ready_for_use = config["profileReadyForUse"] if "profileReadyForUse" in config else False
        else:
            self.id = None
            self.name = None
            self.description = None
            self.slot_id = None
            self.http_header_profile_criteria = []
            self.deleted = False
            self.profile_ready_for_use = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "slotId": self.slot_id,
            "httpHeaderProfileCriteria": [item.request_format() for item in (self.http_header_profile_criteria or [])],
            "deleted": self.deleted,
            "profileReadyForUse": self.profile_ready_for_use,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class HttpHeaderActionProfile(ZscalerObject):
    """
    A class representing a HttpHeaderActionProfile object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.slot_id = config["slotId"] if "slotId" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.profile_ready_for_use = config["profileReadyForUse"] if "profileReadyForUse" in config else False
            self.description = config["description"] if "description" in config else None
            self.http_header_action_profile_keys = ZscalerCollection.form_list(
                config["httpHeaderActionProfileKeys"] if "httpHeaderActionProfileKeys" in config else [],
                HttpHeaderActionProfileHttpHeaderActionProfileKeys,
            )
        else:
            self.id = None
            self.name = None
            self.slot_id = None
            self.deleted = False
            self.profile_ready_for_use = False
            self.description = None
            self.http_header_action_profile_keys = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "slotId": self.slot_id,
            "deleted": self.deleted,
            "profileReadyForUse": self.profile_ready_for_use,
            "description": self.description,
            "httpHeaderActionProfileKeys": [item.request_format() for item in (self.http_header_action_profile_keys or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class HttpHeaderProfileHttpHeaderProfileCriteria(ZscalerObject):
    """
    A class representing a HttpHeaderProfileHttpHeaderProfileCriteria object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.header = config["header"] if "header" in config else None
            self.operator = config["operator"] if "operator" in config else None
            self.category_bitmap = ZscalerCollection.form_list(
                config["categoryBitmap"] if "categoryBitmap" in config else [],
                HttpHeaderProfileHttpHeaderProfileCriteriaCategoryBitmap,
            )
            self.cloud_app_bitmap = ZscalerCollection.form_list(
                config["cloudAppBitmap"] if "cloudAppBitmap" in config else [],
                HttpHeaderProfileHttpHeaderProfileCriteriaCloudAppBitmap,
            )
            self.user_agent = config["userAgent"] if "userAgent" in config else None
            self.user_agent_bitmap = config["userAgentBitmap"] if "userAgentBitmap" in config else None
            self.user_agent_version = config["userAgentVersion"] if "userAgentVersion" in config else None
        else:
            self.id = None
            self.header = None
            self.operator = None
            self.category_bitmap = []
            self.cloud_app_bitmap = []
            self.user_agent = None
            self.user_agent_bitmap = None
            self.user_agent_version = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "header": self.header,
            "operator": self.operator,
            "categoryBitmap": [item.request_format() for item in (self.category_bitmap or [])],
            "cloudAppBitmap": [item.request_format() for item in (self.cloud_app_bitmap or [])],
            "userAgent": self.user_agent,
            "userAgentBitmap": self.user_agent_bitmap,
            "userAgentVersion": self.user_agent_version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class HttpHeaderActionProfileHttpHeaderActionProfileKeys(ZscalerObject):
    """
    A class representing a HttpHeaderActionProfileHttpHeaderActionProfileKeys object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.key = config["key"] if "key" in config else None
            self.value = config["value"] if "value" in config else None
        else:
            self.id = None
            self.key = None
            self.value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "key": self.key,
            "value": self.value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class HttpHeaderProfileHttpHeaderProfileCriteriaCategoryBitmap(ZscalerObject):
    """
    A class representing a HttpHeaderProfileHttpHeaderProfileCriteriaCategoryBitmap object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.url_supercategory = config["urlSupercategory"] if "urlSupercategory" in config else None
            self.deprecated = config["deprecated"] if "deprecated" in config else False
            self.backend_name = config["backendName"] if "backendName" in config else None
            self.name = config["name"] if "name" in config else None
            self.user_configured_name = config["userConfiguredName"] if "userConfiguredName" in config else None
            self.comments = config["comments"] if "comments" in config else None
        else:
            self.url_supercategory = None
            self.deprecated = False
            self.backend_name = None
            self.name = None
            self.user_configured_name = None
            self.comments = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "urlSupercategory": self.url_supercategory,
            "deprecated": self.deprecated,
            "backendName": self.backend_name,
            "name": self.name,
            "userConfiguredName": self.user_configured_name,
            "comments": self.comments,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class HttpHeaderProfileHttpHeaderProfileCriteriaCloudAppBitmap(ZscalerObject):
    """
    A class representing a HttpHeaderProfileHttpHeaderProfileCriteriaCloudAppBitmap object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.val = config["val"] if "val" in config else None
            self.web_application_class = config["webApplicationClass"] if "webApplicationClass" in config else None
            self.backend_name = config["backendName"] if "backendName" in config else None
            self.original_name = config["originalName"] if "originalName" in config else None
            self.name = config["name"] if "name" in config else None
            self.deprecated = config["deprecated"] if "deprecated" in config else False
            self.misc = config["misc"] if "misc" in config else False
            self.app_not_ready = config["appNotReady"] if "appNotReady" in config else False
            self.under_migration = config["underMigration"] if "underMigration" in config else False
            self.app_cat_modified = config["appCatModified"] if "appCatModified" in config else False
        else:
            self.val = None
            self.web_application_class = None
            self.backend_name = None
            self.original_name = None
            self.name = None
            self.deprecated = False
            self.misc = False
            self.app_not_ready = False
            self.under_migration = False
            self.app_cat_modified = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "val": self.val,
            "webApplicationClass": self.web_application_class,
            "backendName": self.backend_name,
            "originalName": self.original_name,
            "name": self.name,
            "deprecated": self.deprecated,
            "misc": self.misc,
            "appNotReady": self.app_not_ready,
            "underMigration": self.under_migration,
            "appCatModified": self.app_cat_modified,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
