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


class TrustedNetwork(ZscalerObject):
    """
    A class for Trusted Network objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.name = config["name"] if "name" in config else None
            self.domain = config["domain"] if "domain" in config else None
            self.network_id = config["networkId"] if "networkId" in config else None
            self.zscaler_cloud = config["zscalerCloud"] if "zscalerCloud" in config else None
            self.master_customer_id = config["masterCustomerId"] if config and "masterCustomerId" in config else None

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.domain = None
            self.network_id = None
            self.zscaler_cloud = None
            self.master_customer_id = None

    def request_format(self):
        """
        Formats the Trusted Network data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "domain": self.domain,
            "networkId": self.network_id,
            "zscalerCloud": self.zscaler_cloud,
            "masterCustomerId": self.master_customer_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
