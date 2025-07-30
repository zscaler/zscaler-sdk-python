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


class CustomerDomainController(ZscalerObject):
    """
    A class for CustomerDomainController objects.
    """

    def __init__(self, config=None):
        """
        Initialize the CustomerDomainController model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.association_type = config["associationType"] \
                if "associationType" in config else None
            self.capture = config["capture"] \
                if "capture" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.domain = config["domain"] \
                if "domain" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
        else:
            self.association_type = None
            self.capture = None
            self.creation_time = None
            self.domain = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.microtenant_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "associationType": self.association_type,
            "capture": self.capture,
            "creationTime": self.creation_time,
            "domain": self.domain,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "microtenantId": self.microtenant_id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
