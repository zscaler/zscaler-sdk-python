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
from zscaler.ztw.models import common as common


class ApiKeys(ZscalerObject):
    """
    A class for ApiKeys objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ApiKeys model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.key_value = config["keyValue"] if "keyValue" in config else None
            self.permissions = ZscalerCollection.form_list(config["permissions"] if "permissions" in config else [], str)
            self.enabled = config["enabled"] if "enabled" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.partner = config["partner"] if "partner" in config else None
            self.partner_url = config["partnerUrl"] if "partnerUrl" in config else None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonIDNameExternalID):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonIDNameExternalID(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            if "partner" in config:
                if isinstance(config["partner"], common.CommonIDNameExternalID):
                    self.partner = config["partner"]
                elif config["partner"] is not None:
                    self.partner = common.CommonIDNameExternalID(config["partner"])
                else:
                    self.partner = None
            else:
                self.partner = None

        else:
            self.id = None
            self.key_value = None
            self.permissions = ZscalerCollection.form_list([], str)
            self.enabled = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.partner = None
            self.partner_url = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "keyValue": self.key_value,
            "permissions": self.permissions,
            "enabled": self.enabled,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "partner": self.partner,
            "partnerUrl": self.partner_url,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
