# flake8: noqa
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


class WebAppService(ZscalerObject):
    """
    A class for WebAppService objects.
    """

    def __init__(self, config=None):
        """
        Initialize the WebAppService model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.app_data_blob = ZscalerCollection.form_list(config["appDataBlob"] if "appDataBlob" in config else [], str)
            self.app_data_blob_v6 = ZscalerCollection.form_list(
                config["appDataBlobV6"] if "appDataBlobV6" in config else [], str
            )
            self.app_name = config["appName"] if "appName" in config else None
            self.app_svc_id = config["appSvcId"] if "appSvcId" in config else None
            self.app_version = config["appVersion"] if "appVersion" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.edited_by = config["editedBy"] if "editedBy" in config else None
            self.edited_timestamp = config["editedTimestamp"] if "editedTimestamp" in config else None
            self.id = config["id"] if "id" in config else None
            self.uid = config["uid"] if "uid" in config else None
            self.version = config["version"] if "version" in config else None
        else:
            self.active = None
            self.app_data_blob = ZscalerCollection.form_list([], str)
            self.app_data_blob_v6 = ZscalerCollection.form_list([], str)
            self.app_name = None
            self.app_svc_id = None
            self.app_version = None
            self.created_by = None
            self.edited_by = None
            self.edited_timestamp = None
            self.id = None
            self.uid = None
            self.version = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "appDataBlob": self.app_data_blob,
            "appDataBlobV6": self.app_data_blob_v6,
            "appName": self.app_name,
            "appSvcId": self.app_svc_id,
            "appVersion": self.app_version,
            "createdBy": self.created_by,
            "editedBy": self.edited_by,
            "editedTimestamp": self.edited_timestamp,
            "id": self.id,
            "uid": self.uid,
            "version": self.version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
