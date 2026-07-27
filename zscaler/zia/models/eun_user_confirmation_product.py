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


class EunUserConfirmationProduct(ZscalerObject):
    """
    A class for EunUserConfirmationProduct objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EunUserConfirmationProduct model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.channel = config["channel"] if "channel" in config else None
            self.product = config["product"] if "product" in config else None
            self.default = config["default"] if "default" in config else None
            self.language_templates = ZscalerCollection.form_list(
                config["languageTemplates"] if "languageTemplates" in config else [], LanguageTemplate
            )
        else:
            self.id = None
            self.name = None
            self.channel = None
            self.product = None
            self.default = None
            self.language_templates = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "channel": self.channel,
            "product": self.product,
            "default": self.default,
            "languageTemplates": [item.request_format() for item in (self.language_templates or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LanguageTemplate(ZscalerObject):
    """
    A class for LanguageTemplate objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LanguageTemplate model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.language = config["language"] if "language" in config else None
            self.message = config["message"] if "message" in config else None
            self.default = config["default"] if "default" in config else None
        else:
            self.language = None
            self.message = None
            self.default = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "language": self.language,
            "message": self.message,
            "default": self.default,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
