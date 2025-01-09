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
from zscaler.zia.models import traffic_gre_recommended_list as gre_recommended_list

class TrafficGRETunnel(ZscalerObject):
    """
    A class representing a Traffic Forwarding GRE Tunnel object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.comment = config["comment"] if "comment" in config else None
            self.source_ip = config["sourceIp"] if "sourceIp" in config else None
            self.internal_ip_range = config["internalIpRange"] if "internalIpRange" in config else None
            self.within_country = config["withinCountry"] if "withinCountry" in config else None
            self.ip_unnumbered = config["ipUnnumbered"] if "ipUnnumbered" in config else None
            self.sub_cloud = config["subcloud"] if "subcloud" in config else None
            self.last_modification_time = config["lastModificationTime"] if "lastModificationTime" in config else None
            self.last_modified_by = config["lastModifiedBy"] if "lastModifiedBy" in config else None
            self.managed_by = config["managedBy"] if "managedBy" in config else None

            # Directly handle primaryDestVip and secondaryDestVip as dictionaries
            self.primary_dest_vip = config.get("primaryDestVip", {})
            self.secondary_dest_vip = config.get("secondaryDestVip", {})
            
        else:
            # Initialize with default None values
            self.id = None
            self.comment = None
            self.source_ip = None
            self.internal_ip_range = None
            self.within_country = False
            self.ip_unnumbered = None
            self.sub_cloud = None
            self.last_modification_time = None
            self.last_modified_by = None
            self.managed_by = None
            self.primary_dest_vip = {}
            self.secondary_dest_vip = {}

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "comment": self.comment,
            "sourceIp": self.source_ip,
            "internalIpRange": self.internal_ip_range,
            "withinCountry": self.within_country,
            "ipUnnumbered": self.ip_unnumbered,
            "subcloud": self.sub_cloud,
            "lastModificationTime": self.last_modification_time,
            "lastModifiedBy": self.last_modified_by,
            "managedBy": self.managed_by,
            "primaryDestVip": self.primary_dest_vip,  # Pass as a simple dictionary
            "secondaryDestVip": self.secondary_dest_vip,  # Pass as a simple dictionary
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
