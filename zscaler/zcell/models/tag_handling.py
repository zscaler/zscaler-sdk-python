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


class TagHandling(ZscalerObject):
    """
    A class representing a TagHandling object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by_user_id = config["modifiedByUserId"] if "modifiedByUserId" in config else None
            self.tenant_id = config["tenantId"] if "tenantId" in config else None
            self.mvno_customer_id = config["mvnoCustomerId"] if "mvnoCustomerId" in config else None
        else:
            self.id = None
            self.name = None
            self.creation_time = None
            self.modified_by_user_id = None
            self.tenant_id = None
            self.mvno_customer_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "creationTime": self.creation_time,
            "modifiedByUserId": self.modified_by_user_id,
            "tenantId": self.tenant_id,
            "mvnoCustomerId": self.mvno_customer_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CreateTag(ZscalerObject):
    """
    A class representing a CreateTag object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.name = config["name"] if "name" in config else None
        else:
            self.name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
