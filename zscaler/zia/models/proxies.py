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
from zscaler.zia.models import common


class Proxies(ZscalerObject):
    """
    A class for Proxies objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Proxies model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.type = config["type"] if "type" in config else None
            self.address = config["address"] if "address" in config else None
            self.port = config["port"] if "port" in config else None

            self.description = config["description"] if "description" in config else None
            self.insert_xau_header = config["insertXauHeader"] if "insertXauHeader" in config else None
            self.base64_encode_xau_header = config["base64EncodeXauHeader"] if "base64EncodeXauHeader" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            if "cert" in config:
                if isinstance(config["cert"], common.CommonBlocks):
                    self.cert = config["cert"]
                elif config["cert"] is not None:
                    self.cert = common.CommonBlocks(config["cert"])
                else:
                    self.cert = None
            else:
                self.cert = None

        else:
            self.id = None
            self.name = None
            self.type = None
            self.address = None
            self.port = None
            self.cert = None
            self.description = None
            self.insert_xau_header = None
            self.base64_encode_xau_header = None
            self.last_modified_by = None
            self.last_modified_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "address": self.address,
            "port": self.port,
            "cert": self.cert,
            "description": self.description,
            "insertXauHeader": self.insert_xau_header,
            "base64EncodeXauHeader": self.base64_encode_xau_header,
            "lastModifiedBy": self.last_modified_by,
            "lastModifiedTime": self.last_modified_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
