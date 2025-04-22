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


class CloudConnectorGroup(ZscalerObject):
    """
    A class representing a Cloud Connector Group object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if config and "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if config and "modifiedBy" in config else None
            self.id = config["id"] if config and "id" in config else None
            self.name = config["name"] if config and "name" in config else None
            self.enabled = config["enabled"] if config and "enabled" in config else True
            self.description = config["description"] if config and "description" in config else None
            self.zia_cloud = config["ziaCloud"] if config and "ziaCloud" in config else None
            self.zia_org_id = config["ziaOrgId"] if config and "ziaOrgId" in config else None
        else:
            self.creation_time = None
            self.modified_by = None
            self.id = None
            self.name = None
            self.enabled = True
            self.description = None
            self.zia_cloud = None
            self.zia_org_id = None

    def request_format(self):
        """
        Formats the Cloud Connector Group data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
            "ziaCloud": self.zia_cloud,
            "ziaOrgId": self.zia_org_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
