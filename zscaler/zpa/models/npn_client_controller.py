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
from zscaler.zia.models import common


class NPNClientController(ZscalerObject):
    """
    A class for NPNClientController objects.
    """

    def __init__(self, config=None):
        """
        Initialize the NPNClientController model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.client_ip_address = config["clientIpAddress"] \
                if "clientIpAddress" in config else None
            self.common_name = config["commonName"] \
                if "commonName" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.device_state = config["deviceState"] \
                if "deviceState" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.vpn_service_edge_name = config["vpnServiceEdgeName"] \
                if "vpnServiceEdgeName" in config else None
            self.vpn_service_edge_id = config["vpnServiceEdgeId"] \
                if "vpnServiceEdgeId" in config else None
            self.user_name = config["UserName"] \
                if "UserName" in config else None
        else:
            self.client_ip_address = None
            self.common_name = None
            self.creation_time = None
            self.device_state = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.vpn_service_edge_name = None
            self.vpn_service_edge_id = None
            self.user_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "clientIpAddress": self.client_ip_address,
            "commonName": self.common_name,
            "creationTime": self.creation_time,
            "deviceState": self.device_state,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "vpnServiceEdgeName": self.vpn_service_edge_name,
            "vpnServiceEdgeId": self.vpn_service_edge_id,
            "UserName": self.user_name
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
