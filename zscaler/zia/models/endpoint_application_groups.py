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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject


class EndpointApplicationGroups(ZscalerObject):
    """
    A class for EndpointApplicationGroups objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EndpointApplicationGroups model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.group_id = config["groupId"] if "groupId" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.mod_uid = config["modUId"] if "modUId" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.end_point_applications = ZscalerCollection.form_list(
                config["endPointApplications"] if "endPointApplications" in config else [], EndPointApplication
            )
        else:
            self.group_id = None
            self.name = None
            self.description = None
            self.mod_uid = None
            self.last_modified_time = None
            self.end_point_applications = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "groupId": self.group_id,
            "name": self.name,
            "description": self.description,
            "modUId": self.mod_uid,
            "lastModifiedTime": self.last_modified_time,
            "endPointApplications": [item.request_format() for item in (self.end_point_applications or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class EndPointApplication(ZscalerObject):
    """
    A class for EndPointApplication objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EndPointApplication model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.resource_id = config["resourceId"] if "resourceId" in config else None
            self.description = config["description"] if "description" in config else None
            self.os_type = config["osType"] if "osType" in config else None
            self.application_name = config["applicationName"] if "applicationName" in config else None
            self.bundle_id = config["bundleID"] if "bundleID" in config else None
            self.filename = config["filename"] if "filename" in config else None
            self.original_file_name = config["originalFileName"] if "originalFileName" in config else None
            self.digitally_signed = config["digitallySigned"] if "digitallySigned" in config else None
            self.mod_uid = config["modUId"] if "modUId" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.application_type = config["applicationType"] if "applicationType" in config else None
            self.zapp_id = config["zappId"] if "zappId" in config else None
            self.deleted = config["deleted"] if "deleted" in config else None
            self.versions = ZscalerCollection.form_list(config["versions"] if "versions" in config else [], Version)

            if "version" in config:
                if isinstance(config["version"], Version):
                    self.version = config["version"]
                elif config["version"] is not None:
                    self.version = Version(config["version"])
                else:
                    self.version = None
            else:
                self.version = None
        else:
            self.resource_id = None
            self.description = None
            self.os_type = None
            self.application_name = None
            self.bundle_id = None
            self.filename = None
            self.original_file_name = None
            self.digitally_signed = None
            self.mod_uid = None
            self.last_modified_time = None
            self.application_type = None
            self.zapp_id = None
            self.deleted = None
            self.versions = []
            self.version = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "resourceId": self.resource_id,
            "description": self.description,
            "osType": self.os_type,
            "applicationName": self.application_name,
            "bundleID": self.bundle_id,
            "filename": self.filename,
            "originalFileName": self.original_file_name,
            "digitallySigned": self.digitally_signed,
            "modUId": self.mod_uid,
            "lastModifiedTime": self.last_modified_time,
            "applicationType": self.application_type,
            "zappId": self.zapp_id,
            "deleted": self.deleted,
            "versions": [item.request_format() for item in (self.versions or [])],
            "version": self.version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Version(ZscalerObject):
    """
    A class for Version objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Version model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.version = config["version"] if "version" in config else None
            self.z_ver_id_md32 = config["z_ver_id_md32"] if "z_ver_id_md32" in config else None
            self.threat_type = config["threat_type"] if "threat_type" in config else None
            self.threat_level = config["threat_level"] if "threat_level" in config else None
            self.bundle_id = config["bundle_id"] if "bundle_id" in config else None
            self.code_signing_certificate_status = (
                config["code_signing_certificate_status"] if "code_signing_certificate_status" in config else None
            )
            self.threat_level_updated = config["threatLevelUpdated"] if "threatLevelUpdated" in config else None
        else:
            self.version = None
            self.z_ver_id_md32 = None
            self.threat_type = None
            self.threat_level = None
            self.bundle_id = None
            self.code_signing_certificate_status = None
            self.threat_level_updated = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "version": self.version,
            "z_ver_id_md32": self.z_ver_id_md32,
            "threat_type": self.threat_type,
            "threat_level": self.threat_level,
            "bundle_id": self.bundle_id,
            "code_signing_certificate_status": self.code_signing_certificate_status,
            "threatLevelUpdated": self.threat_level_updated,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
