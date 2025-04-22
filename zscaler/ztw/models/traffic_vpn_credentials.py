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
from zscaler.ztw.models import location_management as location_management


class TrafficVPNCredentials(ZscalerObject):
    """
    A class representing a VPN Credentials object.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            # Top-level attributes
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.type = config["type"] if "type" in config else None
            self.fqdn = config["fqdn"] if "fqdn" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.pre_shared_key = config["preSharedKey"] if "preSharedKey" in config else None
            self.comments = config["comments"] if "comments" in config else None
            self.common_name = config["commonName"] if "commonName" in config else None

            self.xauth_password = config["xauthPassword"] if "xauthPassword" in config else None

            self.location = ZscalerCollection.form_list(
                config["location"] if "location" in config else [], location_management.LocationManagement
            )

            self.managed_by = config["managedBy"] if "managedBy" in config else None

            self.disabled = config["disabled"] if "disabled" in config else None

            self.psk = config["psk"] if "psk" in config else None

        else:
            # Initialize with default None values
            self.id = None
            self.name = None
            self.comments = None
            self.common_name = None
            self.type = None
            self.fqdn = None
            self.ip_address = None
            self.pre_shared_key = None
            self.psk = None
            self.xauth_password = None
            self.location = []
            self.managed_by = None
            self.disabled = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "commonName": self.common_name,
            "type": self.type,
            "fqdn": self.fqdn,
            "ipAddress": self.ip_address,
            "preSharedKey": self.pre_shared_key,
            "psk": self.psk,
            "xauthPassword": self.xauth_password,
            "comments": self.comments,
            "managedBy": self.managed_by,
            "disabled": self.disabled,
            "location": [loc.request_format() for loc in (self.locations or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
