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


class ClientSettings(ZscalerObject):
    """
    A class for ClientSettings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ClientSettings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.enrollment_cert_id = config["enrollmentCertId"] \
                if "enrollmentCertId" in config else None
            self.client_certificate_type = config["clientCertificateType"] \
                if "clientCertificateType" in config else None
            self.enrollment_cert_name = config["enrollmentCertName"] \
                if "enrollmentCertName" in config else None
            self.singning_cert_expiry_in_epoch_sec = config["singningCertExpiryInEpochSec"] \
                if "singningCertExpiryInEpochSec" in config else None
            self.name = config["name"] \
                if "name" in config else None
        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.microtenant_id = None
            self.enrollment_cert_id = None
            self.client_certificate_type = None
            self.enrollment_cert_name = None
            self.singning_cert_expiry_in_epoch_sec = None
            self.name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "microtenantId": self.microtenant_id,
            "enrollmentCertId": self.enrollment_cert_id,
            "clientCertificateType": self.client_certificate_type,
            "enrollmentCertName": self.enrollment_cert_name,
            "singningCertExpiryInEpochSec": self.singning_cert_expiry_in_epoch_sec,
            "name": self.name
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
