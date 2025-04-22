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


class IPDestinationGroups(ZscalerObject):
    """
    A class representing a Cloud Firewall IP Destination Group object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.type = config["type"] if "type" in config else None
            self.is_non_editable = config["isNonEditable"] if "isNonEditable" in config else None

            self.addresses = ZscalerCollection.form_list(config["addresses"] if "addresses" in config else [], str)
            self.ip_categories = ZscalerCollection.form_list(config["ipCategories"] if "ipCategories" in config else [], str)
            self.countries = ZscalerCollection.form_list(config["countries"] if "countries" in config else [], str)
        else:
            self.id = None
            self.name = None
            self.description = None
            self.type = None
            self.is_non_editable = None
            self.addresses = []
            self.ip_categories = []
            self.countries = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "isNonEditable": self.is_non_editable,
            "addresses": self.addresses,
            "countries": self.countries,
            "ipCategories": self.ip_categories,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
