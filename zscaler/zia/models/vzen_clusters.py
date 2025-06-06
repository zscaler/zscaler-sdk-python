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
from zscaler.zia.models import common as common_reference


class VZENClusters(ZscalerObject):
    """
    A class for VZENClusters objects.
    """

    def __init__(self, config=None):
        """
        Initialize the VZENClusters model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.status = config["status"] \
                if "status" in config else None
            self.ip_address = config["ipAddress"] \
                if "ipAddress" in config else None
            self.subnet_mask = config["subnetMask"] \
                if "subnetMask" in config else None
            self.default_gateway = config["defaultGateway"] \
                if "defaultGateway" in config else None
            self.type = config["type"] \
                if "type" in config else None
            self.ip_sec_enabled = config["ipSecEnabled"] \
                if "ipSecEnabled" in config else None

            self.virtual_zen_nodes = ZscalerCollection.form_list(
                config["virtualZenNodes"] if "virtualZenNodes" in config else [], common_reference.ResourceReference
            )

        else:
            self.id = None
            self.name = None
            self.status = None
            self.ip_address = None
            self.subnet_mask = None
            self.default_gateway = None
            self.type = None
            self.ip_sec_enabled = None
            self.virtual_zen_nodes = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "ipAddress": self.ip_address,
            "subnetMask": self.subnet_mask,
            "defaultGateway": self.default_gateway,
            "type": self.type,
            "ipSecEnabled": self.ip_sec_enabled,
            "virtualZenNodes": self.virtual_zen_nodes
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
