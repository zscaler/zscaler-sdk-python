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

from typing import Dict, List, Optional, Any, Union
from zscaler.oneapi_object import ZscalerObject


class BranchConnectorController(ZscalerObject):
    """
    A class representing the Branch Connector Controller.
    """

    def __init__(self, config=None):
        """
        Initialize the Branchconnectorcontroller model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.branch_connector_group_id = config["branchConnectorGroupId"] \
                if "branchConnectorGroupId" in config else None
            self.branch_connector_group_name = config["branchConnectorGroupName"] \
                if "branchConnectorGroupName" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.edge_connector_group_id = config["edgeConnectorGroupId"] \
                if "edgeConnectorGroupId" in config else None
            self.edge_connector_group_name = config["edgeConnectorGroupName"] \
                if "edgeConnectorGroupName" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.fingerprint = config["fingerprint"] \
                if "fingerprint" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.ip_acl = config["ipAcl"] if "ipAcl" in config else []
            self.issued_cert_id = config["issuedCertId"] \
                if "issuedCertId" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.enrollment_cert = config["enrollmentCert"] \
                if "enrollmentCert" in config else None
        else:
            self.branch_connector_group_id = None
            self.branch_connector_group_name = None
            self.creation_time = None
            self.description = None
            self.edge_connector_group_id = None
            self.edge_connector_group_name = None
            self.enabled = None
            self.fingerprint = None
            self.id = None
            self.ip_acl = []
            self.issued_cert_id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.enrollment_cert = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "branchConnectorGroupId": self.branch_connector_group_id,
            "branchConnectorGroupName": self.branch_connector_group_name,
            "creationTime": self.creation_time,
            "description": self.description,
            "edgeConnectorGroupId": self.edge_connector_group_id,
            "edgeConnectorGroupName": self.edge_connector_group_name,
            "enabled": self.enabled,
            "fingerprint": self.fingerprint,
            "id": self.id,
            "ipAcl": self.ip_acl,
            "issuedCertId": self.issued_cert_id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "enrollmentCert": self.enrollment_cert
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
