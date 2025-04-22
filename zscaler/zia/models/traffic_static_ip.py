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
from zscaler.zia.models import common as common


class TrafficStaticIP(ZscalerObject):
    """
    A class representing a VPN Credentials object.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.comment = config["comment"] if "comment" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.geo_override = config["geoOverride"] if "geoOverride" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.routable_ip = config["routableIP"] if "routableIP" in config else None
            self.last_modification_time = config["lastModificationTime"] if "lastModificationTime" in config else None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None

            if "city" in config:
                if isinstance(config["city"], common.CommonIDName):
                    self.city = config["city"]
                elif config["city"] is not None:
                    self.city = common.CommonIDName(config["city"])
                else:
                    self.city = None
            else:
                self.city = None

        else:
            self.id = None
            self.comment = None
            self.ip_address = None
            self.geo_override = False
            self.comments = None
            self.latitude = None
            self.longitude = None
            self.routable_ip = False
            self.last_modification_time = None
            self.last_modified_by = None
            self.city = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "comment": self.comment,
            "ipAddress": self.ip_address,
            "geoOverride": self.geo_override,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "routableIP": self.routable_ip,
            "lastModificationTime": self.last_modification_time,
            "lastModifiedBy": self.last_modified_by,
            "city": self.city,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
