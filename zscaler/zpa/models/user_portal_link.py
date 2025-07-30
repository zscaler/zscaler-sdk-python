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
from zscaler.zpa.models import user_portal_controller as user_portal_controller


class UserPortalLinks(ZscalerObject):
    """
    A class for User Portal Links objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the User Portal Links model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.user_portals = ZscalerCollection.form_list(
                config["userPortals"] if "userPortals" in config else [], user_portal_controller.UserPortalController
            )
            self.user_portal_links = ZscalerCollection.form_list(
                config["userPortalLinks"] if "userPortalLinks" in config else [], UserPortalLink
            )
        else:
            self.user_portals = []
            self.user_portal_links = []

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "userPortals": self.user_portals,
            "userPortalLinks": self.user_portal_links,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class UserPortalLink(ZscalerObject):
    """
    A class for User Portal Link objects.
    """

    def __init__(self, config=None):
        """
        Initialize the User Portal Link model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.application_id = config["applicationId"] \
                if "applicationId" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.icon_text = config["iconText"] \
                if "iconText" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.link = config["link"] \
                if "link" in config else None
            self.link_path = config["linkPath"] \
                if "linkPath" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.protocol = config["protocol"] \
                if "protocol" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] \
                if "microtenantName" in config else None
            self.user_portal_id = config["userPortalId"] \
                if "userPortalId" in config else None

            self.user_portals = ZscalerCollection.form_list(
                config["userPortals"] if "userPortals" in config else [], user_portal_controller.UserPortalController
            )
        else:
            self.application_id = None
            self.creation_time = None
            self.description = None
            self.enabled = None
            self.icon_text = None
            self.id = None
            self.link = None
            self.link_path = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.protocol = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.user_portal_id = None
            self.user_portals = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "applicationId": self.application_id,
            "creationTime": self.creation_time,
            "description": self.description,
            "enabled": self.enabled,
            "iconText": self.icon_text,
            "id": self.id,
            "link": self.link,
            "linkPath": self.link_path,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "protocol": self.protocol,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "userPortalId": self.user_portal_id,
            "userPortals": self.user_portals
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
