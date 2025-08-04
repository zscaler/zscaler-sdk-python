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
from zscaler.zidentity.models import common


class Groups(ZscalerObject):
    """
    A class for Groups objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Groups model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.results_total = config["results_total"] \
                if "results_total" in config else None
            self.page_offset = config["pageOffset"] \
                if "pageOffset" in config else None
            self.page_size = config["pageSize"] \
                if "pageSize" in config else None
            self.next_link = config["next_link"] \
                if "next_link" in config else None
            self.prev_link = config["prev_link"] \
                if "prev_link" in config else None
            self.records = ZscalerCollection.form_list(
                config["records"] if "records" in config else [], GroupRecord
            )
        else:
            self.results_total = None
            self.page_offset = None
            self.page_size = None
            self.next_link = None
            self.prev_link = None
            self.records = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "results_total": self.results_total,
            "pageOffset": self.page_offset,
            "pageSize": self.page_size,
            "next_link": self.next_link,
            "prev_link": self.prev_link,
            "records": self.records
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GroupRecord(ZscalerObject):
    """
    A class for Group Record objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Group Record model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.name = config["name"] \
                if "name" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.source = config["source"] \
                if "source" in config else None
            self.is_dynamic_group = config["isDynamicGroup"] \
                if "isDynamicGroup" in config else None
            self.dynamic_group = config["dynamicGroup"] \
                if "dynamicGroup" in config else None
            self.admin_entitlement_enabled = config["adminEntitlementEnabled"] \
                if "adminEntitlementEnabled" in config else None
            self.service_entitlement_enabled = config["serviceEntitlementEnabled"] \
                if "serviceEntitlementEnabled" in config else None
            self.custom_attrs_info = config if isinstance(config, dict) else {}

            self.login_name = config["loginName"] \
                if "loginName" in config else None
            self.display_name = config["displayName"] \
                if "displayName" in config else None
            self.first_name = config["firstName"] \
                if "firstName" in config else None
            self.last_name = config["lastName"] \
                if "lastName" in config else None
            self.primary_email = config["primaryEmail"] \
                if "primaryEmail" in config else None
            self.secondary_email = config["secondaryEmail"] \
                if "secondaryEmail" in config else None
            self.status = config["status"] \
                if "status" in config else None

            if "idp" in config:
                if isinstance(config["idp"], common.CommonIDNameDisplayName):
                    self.idp = config["idp"]
                elif config["idp"] is not None:
                    self.idp = common.CommonIDNameDisplayName(config["idp"])
                else:
                    self.idp = None

            else:
                self.idp = None

            if "department" in config:
                if isinstance(config["department"], common.CommonIDNameDisplayName):
                    self.department = config["department"]
                elif config["department"] is not None:
                    self.department = common.CommonIDNameDisplayName(config["department"])
                else:
                    self.department = None

            else:
                self.department = None

        else:
            self.name = None
            self.description = None
            self.id = None
            self.source = None
            self.idp = None
            self.department = None
            self.is_dynamic_group = None
            self.dynamic_group = None
            self.admin_entitlement_enabled = None
            self.service_entitlement_enabled = None
            self.custom_attrs_info = None
            self.login_name = None
            self.display_name = None
            self.first_name = None
            self.last_name = None
            self.primary_email = None
            self.secondary_email = None
            self.status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "source": self.source,
            "idp": self.idp,
            "department": self.department,
            "isDynamicGroup": self.is_dynamic_group,
            "dynamicGroup": self.dynamic_group,
            "adminEntitlementEnabled": self.admin_entitlement_enabled,
            "serviceEntitlementEnabled": self.service_entitlement_enabled,
            "customAttrsInfo": self.custom_attrs_info,
            "loginName": self.login_name,
            "displayName": self.display_name,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "primaryEmail": self.primary_email,
            "secondaryEmail": self.secondary_email,
            "status": self.status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
