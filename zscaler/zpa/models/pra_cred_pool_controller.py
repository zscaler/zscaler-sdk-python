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
from zscaler.zpa.models import common as common


class PRACredentialPoolController(ZscalerObject):
    """
    A class representing the Privileged Remote Access Credential Pool.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.credential_mapping_count = config["credentialMappingCount"] if "credentialMappingCount" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.credential_type = config["credentialType"] if "credentialType" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None

            self.credentials = ZscalerCollection.form_list(
                config["credentials"] if "credentials" in config else [], common.CommonIDName
            )
        else:
            self.id = None
            self.name = None
            self.description = None
            self.credential_mapping_count = None
            self.credential_type = None
            self.credentials = None
            self.creation_time = None
            self.modified_by = None
            self.modified_time = None
            self.microtenant_id = None
            self.microtenant_name = None

    def request_format(self):
        """
        Formats the credential data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "credentialMappingCount": self.credential_mapping_count,
            "credentials": self.credentials,
            "credentialType": self.credential_type,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
