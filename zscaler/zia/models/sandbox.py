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
from zscaler.zia.models import common


class BehavioralAnalysisAdvancedSettings(ZscalerObject):
    """
    A class for Behavioral Analysis Advanced Settings objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Behavioral Analysis Advanced Settings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.md5_hash_value_list = ZscalerCollection.form_list(
                config["md5HashValueList"] if "md5HashValueList" in config else [], MD5HashValueList
            )
        else:
            self.md5_hash_value_list = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "md5HashValueList": self.md5_hash_value_list,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MD5HashValueList(ZscalerObject):
    """
    A class for MD5 Hash Value List objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the MD5 Hash Value List model based on API response.
        """
        super().__init__(config)
        if config:
            self.url = config["url"] if "url" in config else None
            self.url_comment = config["urlComment"] if "urlComment" in config else None
            self.type = config["type"] if "type" in config else None
        else:
            self.url = None
            self.url_comment = None
            self.type = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "url": self.url,
            "urlComment": self.url_comment,
            "type": self.type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
