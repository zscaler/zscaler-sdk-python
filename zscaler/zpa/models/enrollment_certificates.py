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


class EnrollmentCertificate(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the EnrollmentCertificate model based on the API response.

        Args:
            config (dict): A dictionary representing the enrollment certificate configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if config and "id" in config else None
            self.modified_time = config["modifiedTime"] if config and "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if config and "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if config and "modifiedBy" in config else None
            self.get_cname = config["getcName"] if config and "getcName" in config else None
            self.valid_from_in_epoch_sec = config["validFromInEpochSec"] \
                if config and "validFromInEpochSec" in config else None
            self.valid_to_in_epoch_sec = config["validToInEpochSec"] \
                if config and "validToInEpochSec" in config else None
            self.certificate = config["certificate"] if config and "certificate" in config else None
            self.issued_to = config["issuedTo"] if config and "issuedTo" in config else None
            self.issued_by = config["issuedBy"] if config and "issuedBy" in config else None
            self.serial_no = config["serialNo"] if config and "serialNo" in config else None
            self.name = config["name"] if config and "name" in config else None
            self.allow_signing = config["allowSigning"] if config and "allowSigning" in config else None
            self.private_key_present = config["privateKeyPresent"] if config and "privateKeyPresent" in config else None
            self.client_cert_type = config["clientCertType"] if config and "clientCertType" in config else None
            self.csr = config["csr"] if config and "csr" in config else None
            self.parent_cert_id = config["parentCertId"] if config and "parentCertId" in config else None
            self.parent_cert_name = config["parentCertName"] if config and "parentCertName" in config else None
            self.zrsaencryptedprivatekey = (
                config["zrsaencryptedprivatekey"] if config and "zrsaencryptedprivatekey" in config else None
            )
            self.zrsaencryptedsessionkey = (
                config["zrsaencryptedsessionkey"] if config and "zrsaencryptedsessionkey" in config else None
            )
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None

            self.root_certificate_id = (
                config["rootCertificateId"] if config and "rootCertificateId" in config else None
            )
        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.description = None
            self.get_cname = None
            self.valid_from_in_epoch_sec = None
            self.valid_to_in_epoch_sec = None
            self.certificate = None
            self.issued_to = None
            self.issued_by = None
            self.serial_no = None
            self.name = None
            self.allow_signing = None
            self.private_key_present = None
            self.client_cert_type = None
            self.csr = None
            self.parent_cert_id = None
            self.parent_cert_name = None
            self.zrsaencryptedprivate_key = None
            self.zrsaencryptedsessionkey = None
            self.microtenant_id = None
            self.root_certificate_id = None

    def request_format(self):
        """
        Formats the model data for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "getcName": self.get_cname,
            "validFromInEpochSec": self.valid_from_in_epoch_sec,
            "validToInEpochSec": self.valid_to_in_epoch_sec,
            "certificate": self.certificate,
            "issuedTo": self.issued_to,
            "issuedBy": self.issued_by,
            "serialNo": self.serial_no,
            "name": self.name,
            "allowSigning": self.allow_signing,
            "privateKeyPresent": self.private_key_present,
            "clientCertType": self.client_cert_type,
            "csr": self.csr,
            "parentCertId": self.parent_cert_id,
            "parentCertName": self.parent_cert_name,
            "zrsaencryptedprivatekey": self.zrsaencryptedprivatekey,
            "zrsaencryptedsessionkey": self.zrsaencryptedsessionkey,
            "rootCertificateId": self.root_certificate_id,
            "microtenantId": self.microtenant_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
