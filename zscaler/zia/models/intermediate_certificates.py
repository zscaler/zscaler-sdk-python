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


class IntermediateCACertificate(ZscalerObject):
    """
    A class for Intermediate Certificate objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Intermediate Certificates model based on API response.

        Args:
            config (dict): A dictionary representing the Intermediate Certificates configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.type = config["type"] if "type" in config else None
            self.region = config["region"] if "region" in config else None
            self.status = config["status"] if "status" in config else None
            self.default_certificate = config["defaultCertificate"] if "defaultCertificate" in config else None
            self.cert_start_date = config["certStartDate"] if "certStartDate" in config else None
            self.cert_exp_date = config["certExpDate"] if "certExpDate" in config else None
            self.current_state = config["currentState"] if "currentState" in config else None
            self.public_key = config["publicKey"] if "publicKey" in config else None
            self.key_generation_time = config["keyGenerationTime"] if "keyGenerationTime" in config else None
            self.hsm_attestation_verified_time = (
                config["hsmAttestationVerifiedTime"] if "hsmAttestationVerifiedTime" in config else None
            )
            self.csr_file_name = config["csrFileName"] if "csrFileName" in config else None
            self.csr_generation_time = config["csrGenerationTime"] if "csrGenerationTime" in config else None
        else:
            # Initialize with default None or 0 values
            self.id = None
            self.name = None
            self.description = None
            self.type = None
            self.region = None
            self.status = None
            self.default_certificate = None
            self.cert_start_date = None
            self.cert_exp_date = None
            self.current_state = None
            self.public_key = None
            self.key_generation_time = None
            self.hsm_attestation_verified_time = None
            self.csr_file_name = None
            self.csr_generation_time = None

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
            "region": self.region,
            "status": self.status,
            "defaultCertificate": self.default_certificate,
            "certStartDate": self.cert_start_date,
            "certExpDate": self.cert_exp_date,
            "currentState": self.current_state,
            "publicKey": self.public_key,
            "keyGenerationTime": self.key_generation_time,
            "hsmAttestationVerifiedTime": self.hsm_attestation_verified_time,
            "csrFileName": self.csr_file_name,
            "csrGenerationTime": self.csr_generation_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CertSigningRequest(ZscalerObject):
    """
    A class for Generate CSR objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Generate CSR model based on API response.

        Args:
            config (dict): A dictionary representing the Generate CSR configuration.
        """
        super().__init__(config)

        if config:
            self.cert_id = config["certId"] if "certId" in config else None
            self.csr_file_name = config["csrFileName"] if "csrFileName" in config else None
            self.comm_name = config["commName"] if "commName" in config else None
            self.org_name = config["orgName"] if "orgName" in config else None
            self.dept_name = config["deptName"] if "deptName" in config else None
            self.city = config["city"] if "city" in config else None
            self.state = config["state"] if "state" in config else None
            self.country = config["country"] if "country" in config else None
            self.key_size = config["keySize"] if "keySize" in config else None
            self.signature_algorithm = config["signatureAlgorithm"] if "signatureAlgorithm" in config else None
            self.path_length_constraint = config["pathLengthConstraint"] if "pathLengthConstraint" in config else None
        else:
            # Initialize with default None or 0 values
            self.cert_id = None
            self.csr_generation_time = None
            self.csr_file_name = None
            self.comm_name = None
            self.org_name = None
            self.dept_name = None
            self.city = None
            self.state = None
            self.country = None
            self.key_size = None
            self.signature_algorithm = None
            self.path_length_constraint = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "certId": self.cert_id,
            "csrGenerationTime": self.csr_generation_time,
            "csrFileName": self.csr_file_name,
            "commName": self.comm_name,
            "orgName": self.org_name,
            "deptName": self.dept_name,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "keySize": self.key_size,
            "signatureAlgorithm": self.signature_algorithm,
            "pathLengthConstraint": self.path_length_constraint,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
