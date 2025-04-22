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


class ProxyGatways(ZscalerObject):
    """
    A class for ProxyGatways objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ProxyGatways model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.type = config["type"] if "type" in config else None
            self.primary_proxy = config["primaryProxy"] if "primaryProxy" in config else None
            self.secondary_proxy = config["secondaryProxy"] if "secondaryProxy" in config else None
            self.description = config["description"] if "description" in config else None
            self.last_modified_by = config["lastModifiedBy"] if "lastModifiedBy" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.fail_closed = config["failClosed"] if "failClosed" in config else None
        else:
            self.id = None
            self.name = None
            self.type = None
            self.primary_proxy = None
            self.secondary_proxy = None
            self.description = None
            self.last_modified_by = None
            self.last_modified_time = None
            self.fail_closed = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "primaryProxy": self.primary_proxy,
            "secondaryProxy": self.secondary_proxy,
            "description": self.description,
            "lastModifiedBy": self.last_modified_by,
            "lastModifiedTime": self.last_modified_time,
            "failClosed": self.fail_closed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
