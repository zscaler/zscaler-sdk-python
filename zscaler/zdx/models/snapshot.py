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


class Snapshot(ZscalerObject):
    """
    A class for Snapshot objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Snapshot model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.name = config["name"] \
                if "name" in config else None
            self.alert_id = config["alert_id"] \
                if "alert_id" in config else None
            self.expiry = config["expiry"] \
                if "expiry" in config else None
            self.obfuscation = ZscalerCollection.form_list(
                config["obfuscation"] if "obfuscation" in config else [], str
            )
            self.id = config["id"] \
                if "id" in config else None
            self.url = config["url"] \
                if "url" in config else None
            self.status = config["status"] \
                if "status" in config else None
        else:
            self.name = None
            self.alert_id = None
            self.expiry = None
            self.obfuscation = ZscalerCollection.form_list([], str)
            self.id = None
            self.url = None
            self.status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "alert_id": self.alert_id,
            "expiry": self.expiry,
            "obfuscation": self.obfuscation,
            "id": self.id,
            "url": self.url,
            "status": self.status
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
