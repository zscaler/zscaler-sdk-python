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


class ProvisioningKey(ZscalerObject):
    """
    A class for ProvisioningKey objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.name = config["name"] if "name" in config else None
            self.usage_count = config["usageCount"] if "usageCount" in config else None
            self.max_usage = config["maxUsage"] if "maxUsage" in config else None
            self.zcomponent_id = config["zcomponentId"] if "zcomponentId" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.zcomponent_name = config["zcomponentName"] if "zcomponentName" in config else None
            self.provisioning_key = config["provisioningKey"] if "provisioningKey" in config else None
            self.enrollment_cert_id = config["enrollmentCertId"] if "enrollmentCertId" in config else None
            self.enrollment_cert_name = config["enrollmentCertName"] if "enrollmentCertName" in config else None
        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.usage_count = None
            self.max_usage = None
            self.zcomponent_id = None
            self.enabled = None
            self.zcomponent_name = None
            self.provisioning_key = None
            self.enrollment_cert_id = None
            self.enrollment_cert_name = None

    def request_format(self):
        """
        Formats the current object for making requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "usageCount": self.usage_count,
            "maxUsage": self.max_usage,
            "zcomponentId": self.zcomponent_id,
            "enabled": self.enabled,
            "zcomponentName": self.zcomponent_name,
            "provisioningKey": self.provisioning_key,
            "enrollmentCertId": self.enrollment_cert_id,
            "enrollmentCertName": self.enrollment_cert_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
