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


class AlertSubscriptions(ZscalerObject):
    """
    A class for AlertSubscriptions objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AlertSubscriptions model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.description = config["description"] if "description" in config else None
            self.email = config["email"] if "email" in config else None

            self.pt0_severities = ZscalerCollection.form_list(
                config["pt0Severities"] if "pt0Severities" in config else [], str
            )
            self.secure_severities = ZscalerCollection.form_list(
                config["secureSeverities"] if "secureSeverities" in config else [], str
            )
            self.manage_severities = ZscalerCollection.form_list(
                config["manageSeverities"] if "manageSeverities" in config else [], str
            )
            self.comply_severities = ZscalerCollection.form_list(
                config["complySeverities"] if "complySeverities" in config else [], str
            )
            self.system_severities = ZscalerCollection.form_list(
                config["systemSeverities"] if "systemSeverities" in config else [], str
            )
            self.deleted = config["deleted"] if "deleted" in config else False
        else:
            self.id = None
            self.description = None
            self.email = None
            self.pt0_severities = []
            self.secure_severities = []
            self.manage_severities = []
            self.comply_severities = []
            self.system_severities = []
            self.deleted = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "description": self.description,
            "email": self.email,
            "pt0Severities": self.pt0_severities,
            "secureSeverities": self.secure_severities,
            "manageSeverities": self.manage_severities,
            "complySeverities": self.comply_severities,
            "systemSeverities": self.system_severities,
            "deleted": self.deleted,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
