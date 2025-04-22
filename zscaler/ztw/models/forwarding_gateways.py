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
from zscaler.ztw.models import common as common


class ForwardingGateways(ZscalerObject):
    """
    A class representing a VPN Credentials object.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            # Top-level attributes
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.fail_closed = config["failClosed"] if "failClosed" in config else None

            self.manual_primary = config["manualPrimary"] if "manualPrimary" in config else None

            self.manual_secondary = config["manualSecondary"] if "manualSecondary" in config else None

            self.primary_type = config["primaryType"] if "primaryType" in config else None

            self.secondary_type = config["secondaryType"] if "secondaryType" in config else None

            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonIDNameExternalID):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonIDNameExternalID(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            if "subcloudPrimary" in config:
                if isinstance(config["subcloudPrimary"], common.CommonIDNameExternalID):
                    self.subcloud_primary = config["subcloudPrimary"]
                elif config["subcloudPrimary"] is not None:
                    self.subcloud_primary = common.CommonIDNameExternalID(config["subcloudPrimary"])
                else:
                    self.subcloud_primary = None
            else:
                self.subcloud_primary = None

            if "subcloudSecondary" in config:
                if isinstance(config["subcloudSecondary"], common.CommonIDNameExternalID):
                    self.subcloud_secondary = config["subcloudSecondary"]
                elif config["subcloudSecondary"] is not None:
                    self.subcloud_secondary = common.CommonIDNameExternalID(config["subcloudSecondary"])
                else:
                    self.subcloud_secondary = None
            else:
                self.subcloud_secondary = None

        else:
            # Initialize with default None values
            self.id = None
            self.name = None
            self.description = None
            self.fail_closed = None
            self.manual_primary = None
            self.manual_secondary = None
            self.subcloud_primary = None
            self.subcloud_secondary = None
            self.primary_type = None
            self.secondary_type = None
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
            "description": self.description,
            "failClosed": self.fail_closed,
            "manualPrimary": self.manual_primary,
            "manualSecondary": self.manual_secondary,
            "subcloudPrimary": self.subcloud_primary,
            "subcloudSecondary": self.subcloud_secondary,
            "primaryType": self.primary_type,
            "secondaryType": self.secondary_type,
            "lastModifiedBy": self.last_modified_by,
            "lastModifiedTime": self.last_modified_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
