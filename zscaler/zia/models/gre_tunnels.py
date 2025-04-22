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
            self.within_country = config["withinCountry"] if "withinCountry" in config else False
            self.ip_unnumbered = config["ipUnnumbered"] if "ipUnnumbered" in config else False
            self.sub_cloud = config["subcloud"] if "subcloud" in config else None
            self.last_modification_time = config["lastModificationTime"] if "lastModificationTime" in config else None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None

            if "primaryDestVip" in config:
                if isinstance(config["primaryDestVip"], GreVirtualIP):
                    self.primary_dest_vip = config["primaryDestVip"]
                elif config["primaryDestVip"] is not None:
                    self.primary_dest_vip = GreVirtualIP(config["primaryDestVip"])
                else:
                    self.primary_dest_vip = None

            if "secondaryDestVip" in config:
                if isinstance(config["secondaryDestVip"], GreVirtualIP):
                    self.secondary_dest_vip = config["secondaryDestVip"]
                elif config["secondaryDestVip"] is not None:
                    self.secondary_dest_vip = GreVirtualIP(config["secondaryDestVip"])
                else:
                    self.secondary_dest_vip = None

        else:
            self.id = None
            self.comment = None
            self.source_ip = None
            self.internal_ip_range = None
            self.within_country = False
            self.ip_unnumbered = False
            self.sub_cloud = None
            self.last_modification_time = None
            self.last_modified_by = None
            self.primary_dest_vip = None
            self.secondary_dest_vip = None

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
            "primaryDestVip": self.primary_dest_vip,
            "secondaryDestVip": self.secondary_dest_vip,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GreVirtualIP(ZscalerObject):
    """
    A class for GreVirtualIP objects.
    Handles arbitrary keys dynamically.
    """

    def __init__(self, config=None):
        """
        Initialize the GreVirtualIP model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.virtual_ip = config["virtualIp"] if "virtualIp" in config else None
            self.private_service_edge = config["privateServiceEdge"] if "privateServiceEdge" in config else False
            self.datacenter = config["datacenter"] if "datacenter" in config else False

        else:
            self.id = None
            self.virtual_ip = None
            self.private_service_edge = None
            self.datacenter = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "virtualIp": self.virtual_ip,
            "privateServiceEdge": self.private_service_edge,
            "datacenter": self.datacenter,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
