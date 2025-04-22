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


class IPV6PrefixMask(ZscalerObject):
    """
    A class for IPV6PrefixMask objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the IPV6PrefixMask model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.prefix_mask = config["prefixMask"] if "prefixMask" in config else None
            self.dns_prefix = config["dnsPrefix"] if "dnsPrefix" in config else None
            self.non_editable = config["nonEditable"] if "nonEditable" in config else None

        else:
            self.id = None
            self.name = None
            self.description = None
            self.prefix_mask = None
            self.dns_prefix = None
            self.non_editable = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "prefixMask": self.prefix_mask,
            "dnsPrefix": self.dns_prefix,
            "nonEditable": self.non_editable,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class IPV6Configuration(ZscalerObject):
    """
    A class for IPV6Configuration objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the IPV6Configuration model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.ipv6_enabled = config["ipV6Enabled"] if "ipV6Enabled" in config else None
            self.dns_prefix = config["dnsPrefix"] if "dnsPrefix" in config else None

            self.nat_prefixes = ZscalerCollection.form_list(
                config["natPrefixes"] if "natPrefixes" in config else [], IPV6PrefixMask
            )

        else:
            self.ipv6_enabled = None
            self.nat_prefixes = []
            self.dns_prefix = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ipV6Enabled": self.ipv6_enabled,
            "natPrefixes": self.nat_prefixes,
            "dnsPrefix": self.dns_prefix,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
