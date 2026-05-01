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
from zscaler.oneapi_collection import ZscalerCollection


class PredefinedIPBasedApps(ZscalerObject):
    """
    A class for PredefinedIPBasedApps objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the PredefinedIPBasedApps model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.app_version = config["appVersion"] if "appVersion" in config else None
            self.app_svc_id = config["appSvcId"] if "appSvcId" in config else None
            self.app_name = config["appName"] if "appName" in config else None
            self.active = config["active"] if "active" in config else None
            self.uid = config["uid"] if "uid" in config else None

            self.app_data_blob = ZscalerCollection.form_list(
                config["appDataBlob"] if "appDataBlob" in config else [], AppDataBlob
            )
            self.app_data_blob_v6 = ZscalerCollection.form_list(
                config["appDataBlobV6"] if "appDataBlobV6" in config else [], AppDataBlob
            )

            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.edited_by = config["editedBy"] if "editedBy" in config else None
            self.edited_timestamp = config["editedTimestamp"] if "editedTimestamp" in config else None
            self.zapp_data_blob = config["zappDataBlob"] if "zappDataBlob" in config else None
            self.zapp_data_blob_v6 = config["zappDataBlobV6"] if "zappDataBlobV6" in config else None
        else:
            self.id = None
            self.app_version = None
            self.app_svc_id = None
            self.app_name = None
            self.active = None
            self.uid = None
            self.app_data_blob = ZscalerCollection.form_list([], AppDataBlob)
            self.app_data_blob_v6 = ZscalerCollection.form_list([], AppDataBlob)
            self.created_by = None
            self.edited_by = None
            self.edited_timestamp = None
            self.zapp_data_blob = None
            self.zapp_data_blob_v6 = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "appVersion": self.app_version,
            "appSvcId": self.app_svc_id,
            "appName": self.app_name,
            "active": self.active,
            "uid": self.uid,
            "appDataBlob": self.app_data_blob,
            "appDataBlobV6": self.app_data_blob_v6,
            "createdBy": self.created_by,
            "editedBy": self.edited_by,
            "editedTimestamp": self.edited_timestamp,
            "zappDataBlob": self.zapp_data_blob,
            "zappDataBlobV6": self.zapp_data_blob_v6,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppDataBlob(ZscalerObject):
    """
    A class for AppDataBlob objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the AppDataBlob model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.proto = config["proto"] if "proto" in config else None
            self.port = config["port"] if "port" in config else None
            self.ipaddr = config["ipaddr"] if "ipaddr" in config else None
            self.fqdn = config["fqdn"] if "fqdn" in config else None
        else:
            self.proto = None
            self.port = None
            self.ipaddr = None
            self.fqdn = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "proto": self.proto,
            "port": self.port,
            "ipaddr": self.ipaddr,
            "fqdn": self.fqdn,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
