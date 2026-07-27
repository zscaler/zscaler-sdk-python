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

from typing import Any, Dict, Optional

from zscaler.oneapi_object import ZscalerObject


class EndpointApplicationsCustomAppsLite(ZscalerObject):
    """
    A class for EndpointApplicationsCustomAppsLite objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EndpointApplicationsCustomAppsLite model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.resource_id = config["resourceId"] if "resourceId" in config else None
            self.os_type = config["osType"] if "osType" in config else None
            self.z_ver_id_md32 = config["z_ver_id_md32"] if "z_ver_id_md32" in config else None
            self.threat_level = config["threatLevel"] if "threatLevel" in config else None
            self.application_name = config["applicationName"] if "applicationName" in config else None
            self.bundle_id = config["bundleID"] if "bundleID" in config else None
            self.filename = config["filename"] if "filename" in config else None
            self.original_file_name = config["originalFileName"] if "originalFileName" in config else None
            self.digitally_signed = config["digitallySigned"] if "digitallySigned" in config else None
            self.application_type = config["applicationType"] if "applicationType" in config else None
            self.deleted = config["deleted"] if "deleted" in config else None
            self.zapp_id = config["zappId"] if "zappId" in config else None
        else:
            self.resource_id = None
            self.os_type = None
            self.z_ver_id_md32 = None
            self.threat_level = None
            self.application_name = None
            self.bundle_id = None
            self.filename = None
            self.original_file_name = None
            self.digitally_signed = None
            self.application_type = None
            self.deleted = None
            self.zapp_id = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "resourceId": self.resource_id,
            "osType": self.os_type,
            "z_ver_id_md32": self.z_ver_id_md32,
            "threatLevel": self.threat_level,
            "applicationName": self.application_name,
            "bundleID": self.bundle_id,
            "filename": self.filename,
            "originalFileName": self.original_file_name,
            "digitallySigned": self.digitally_signed,
            "applicationType": self.application_type,
            "deleted": self.deleted,
            "zappId": self.zapp_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
