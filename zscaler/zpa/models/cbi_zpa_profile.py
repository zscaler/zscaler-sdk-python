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


class ZPACBIProfile(ZscalerObject):
    """
    A class representing a ZPA Profile object.
    """

    def __init__(self, config=None):
        """
        Initialize the ZPAProfile model based on API response.

        Args:
            config (dict): A dictionary containing ZPA profile data.
        """
        super().__init__(config)

        self.id = config["id"] if config and "id" in config else None
        self.modified_time = config["modifiedTime"] if config and "modifiedTime" in config else None
        self.creation_time = config["creationTime"] if config and "creationTime" in config else None
        self.modified_by = config["modifiedBy"] if config and "modifiedBy" in config else None
        self.name = config["name"] if config and "name" in config else None
        self.cbi_tenant_id = config["cbiTenantId"] if config and "cbiTenantId" in config else None
        self.cbi_profile_id = config["cbiProfileId"] if config and "cbiProfileId" in config else None
        self.description = config["description"] if config and "description" in config else None
        self.cbi_url = config["cbiUrl"] if config and "cbiUrl" in config else None
        self.enabled = config["enabled"] if config and "enabled" in config else True

    def request_format(self):
        """
        Prepare the object in a format suitable for sending as a request payload.

        Returns:
            dict: A dictionary representing the ZPA profile for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "cbiTenantId": self.cbi_tenant_id,
            "cbiProfileId": self.cbi_profile_id,
            "description": self.description,
            "cbiUrl": self.cbi_url,
            "enabled": self.enabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CBIProfile(ZscalerObject):
    """
    A class representing a ZPA Profile object.
    """

    def __init__(self, config=None):
        """
        Initialize the ZPAProfile model based on API response.

        Args:
            config (dict): A dictionary containing ZPA profile data.
        """
        super().__init__(config)

        self.id = config["id"] if config and "id" in config else None
        self.name = config["name"] if config and "name" in config else None
        self.description = config["description"] if config and "description" in config else None
        self.enabled = config["enabled"] if config and "enabled" in config else None
        self.modified_time = config["modifiedTime"] if config and "modifiedTime" in config else None
        self.creation_time = config["creationTime"] if config and "creationTime" in config else None
        self.modified_by = config["modifiedBy"] if config and "modifiedBy" in config else None
        self.isolation_profile_id = config["isolationProfileId"] if config and "isolationProfileId" in config else None
        self.isolation_tenant_id = config["isolationTenantId"] if config and "isolationTenantId" in config else None
        self.isolation_url = config["isolationUrl"] if config and "isolationUrl" in config else None
        self.microtenant_id = config["microtenantId"] if config and "microtenantId" in config else None
        self.microtenant_name = config["microtenantName"] if config and "microtenantName" in config else True

    def request_format(self):
        """
        Prepare the object in a format suitable for sending as a request payload.

        Returns:
            dict: A dictionary representing the ZPA profile for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "isolationProfileId": self.isolation_profile_id,
            "isolationTenantId": self.isolation_tenant_id,
            "isolationUrl": self.isolation_url,
            "microtenant_id": self.microtenant_id,
            "microtenant_name": self.microtenant_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
