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


class ProcessBasedApps(ZscalerObject):
    """
    A class for ProcessBasedApps objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ProcessBasedApps model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.app_name = config["appName"] if "appName" in config else None
            self.file_names = ZscalerCollection.form_list(config["fileNames"] if "fileNames" in config else [], str)
            self.file_paths = ZscalerCollection.form_list(config["filePaths"] if "filePaths" in config else [], str)
            self.matching_criteria = config["matchingCriteria"] if "matchingCriteria" in config else None
            self.signature_payload = config["signaturePayload"] if "signaturePayload" in config else None
            self.certificate_payload = config["certificatePayload"] if "certificatePayload" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.edited_by = config["editedBy"] if "editedBy" in config else None
            self.edited_timestamp = config["editedTimestamp"] if "editedTimestamp" in config else None
        else:
            self.id = None
            self.app_name = None
            self.file_names = ZscalerCollection.form_list([], str)
            self.file_paths = ZscalerCollection.form_list([], str)
            self.matching_criteria = None
            self.signature_payload = None
            self.certificate_payload = None
            self.created_by = None
            self.edited_by = None
            self.edited_timestamp = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "appName": self.app_name,
            "fileNames": self.file_names,
            "filePaths": self.file_paths,
            "matchingCriteria": self.matching_criteria,
            "signaturePayload": self.signature_payload,
            "certificatePayload": self.certificate_payload,
            "createdBy": self.created_by,
            "editedBy": self.edited_by,
            "editedTimestamp": self.edited_timestamp,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
