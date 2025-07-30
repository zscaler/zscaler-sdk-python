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


class ApiKeys(ZscalerObject):
    """
    A class for ApiKeys objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ApiKeys model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.client_id = config["clientId"] \
                if "clientId" in config else None
            self.client_secret = config["clientSecret"] \
                if "clientSecret" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.iam_client_id = config["iamClientId"] \
                if "iamClientId" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.is_locked = config["isLocked"] \
                if "isLocked" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.pin_session_enabled = config["pinSessionEnabled"] \
                if "pinSessionEnabled" in config else None
            self.read_only = config["readOnly"] \
                if "readOnly" in config else None
            self.restriction_type = config["restrictionType"] \
                if "restrictionType" in config else None
            self.role_id = config["roleId"] \
                if "roleId" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] \
                if "microtenantName" in config else None
            self.sync_version = config["syncVersion"] \
                if "syncVersion" in config else None
            self.token_expiry_time_in_sec = config["tokenExpiryTimeInSec"] \
                if "tokenExpiryTimeInSec" in config else None
            self.zscaler_managed = config["zscalerManaged"] \
                if "zscalerManaged" in config else None
        else:
            self.client_id = None
            self.client_secret = None
            self.creation_time = None
            self.enabled = None
            self.iam_client_id = None
            self.id = None
            self.is_locked = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.pin_session_enabled = None
            self.read_only = None
            self.restriction_type = None
            self.role_id = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.sync_version = None
            self.token_expiry_time_in_sec = None
            self.zscaler_managed = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "creationTime": self.creation_time,
            "enabled": self.enabled,
            "iamClientId": self.iam_client_id,
            "id": self.id,
            "isLocked": self.is_locked,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "pinSessionEnabled": self.pin_session_enabled,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "roleId": self.role_id,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "syncVersion": self.sync_version,
            "tokenExpiryTimeInSec": self.token_expiry_time_in_sec,
            "zscalerManaged": self.zscaler_managed
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
