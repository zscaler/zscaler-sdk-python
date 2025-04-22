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
from zscaler.zia.models import location_management as location_management
from zscaler.zia.models import common as common


class TrafficVPNCredentials(ZscalerObject):
    """
    A class representing a VPN Credentials object.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.type = config["type"] if "type" in config else None
            self.fqdn = config["fqdn"] if "fqdn" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.pre_shared_key = config["preSharedKey"] if "preSharedKey" in config else None
            self.comments = config["comments"] if "comments" in config else None
            self.disabled = config["disabled"] if "disabled" in config else False

            if "location" in config:
                if isinstance(config["location"], common.CommonBlocks):
                    self.location = config["location"]
                elif config["location"] is not None:
                    self.location = common.CommonBlocks(config["location"])
                else:
                    self.location = None
            else:
                self.location = None

            if "managedBy" in config:
                if isinstance(config["managedBy"], common.CommonBlocks):
                    self.managed_by = config["managedBy"]
                elif config["managedBy"] is not None:
                    self.managed_by = common.CommonBlocks(config["managedBy"])
                else:
                    self.managed_by = None
            else:
                self.managed_by = None

        else:
            self.id = None
            self.type = None
            self.fqdn = None
            self.ip_address = None
            self.pre_shared_key = None
            self.comments = None
            self.disabled = False
            self.location = None
            self.managed_by = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "type": self.type,
            "fqdn": self.fqdn,
            "ipAddress": self.ip_address,
            "preSharedKey": self.pre_shared_key,
            "comments": self.comments,
            "disabled": self.disabled,
            "location": self.location,
            "managedBy": self.managed_by,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
