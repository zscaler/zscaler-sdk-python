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


class EunTemplateProduct(ZscalerObject):
    """
    A class for EunTemplateProduct objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EunTemplateProduct model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.channel = config["channel"] if "channel" in config else None
            self.product = config["product"] if "product" in config else None
            self.type = config["type"] if "type" in config else None
            self.caution_interval = config["cautionInterval"] if "cautionInterval" in config else None
            self.default = config["default"] if "default" in config else None
            self.language_templates = ZscalerCollection.form_list(
                config["languageTemplates"] if "languageTemplates" in config else [], LanguageTemplate
            )
            self.notification_details = ZscalerCollection.form_list(
                config["notificationDetails"] if "notificationDetails" in config else [], str
            )

            if "recommendedCloudApp" in config:
                if isinstance(config["recommendedCloudApp"], RecommendedCloudApp):
                    self.recommended_cloud_app = config["recommendedCloudApp"]
                elif config["recommendedCloudApp"] is not None:
                    self.recommended_cloud_app = RecommendedCloudApp(config["recommendedCloudApp"])
                else:
                    self.recommended_cloud_app = None
            else:
                self.recommended_cloud_app = None
        else:
            self.id = None
            self.name = None
            self.channel = None
            self.product = None
            self.type = None
            self.caution_interval = None
            self.default = None
            self.language_templates = []
            self.notification_details = []
            self.recommended_cloud_app = None

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
            "type": self.type,
            "cautionInterval": self.caution_interval,
            "default": self.default,
            "languageTemplates": [item.request_format() for item in (self.language_templates or [])],
            "notificationDetails": self.notification_details,
            "recommendedCloudApp": self.recommended_cloud_app,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class RecommendedCloudApp(ZscalerObject):
    """
    A class for RecommendedCloudApp objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the RecommendedCloudApp model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.val = config["val"] if "val" in config else None
            self.web_application_class = config["webApplicationClass"] if "webApplicationClass" in config else None
            self.backend_name = config["backendName"] if "backendName" in config else None
            self.original_name = config["originalName"] if "originalName" in config else None
            self.name = config["name"] if "name" in config else None
            self.deprecated = config["deprecated"] if "deprecated" in config else None
            self.misc = config["misc"] if "misc" in config else None
            self.app_not_ready = config["appNotReady"] if "appNotReady" in config else None
            self.under_migration = config["underMigration"] if "underMigration" in config else None
            self.app_cat_modified = config["appCatModified"] if "appCatModified" in config else None
        else:
            self.val = None
            self.web_application_class = None
            self.backend_name = None
            self.original_name = None
            self.name = None
            self.deprecated = None
            self.misc = None
            self.app_not_ready = None
            self.under_migration = None
            self.app_cat_modified = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "val": self.val,
            "webApplicationClass": self.web_application_class,
            "backendName": self.backend_name,
            "originalName": self.original_name,
            "name": self.name,
            "deprecated": self.deprecated,
            "misc": self.misc,
            "appNotReady": self.app_not_ready,
            "underMigration": self.under_migration,
            "appCatModified": self.app_cat_modified,
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
            self.allow_message = config["allowMessage"] if "allowMessage" in config else None
            self.block_message = config["blockMessage"] if "blockMessage" in config else None
            self.encrypt_message = config["encryptMessage"] if "encryptMessage" in config else None
            self.readonly_message = config["readonlyMessage"] if "readonlyMessage" in config else None
            self.caution_message = config["cautionMessage"] if "cautionMessage" in config else None
            self.redirect_response_message = config["redirectResponseMessage"] if "redirectResponseMessage" in config else None
            self.default = config["default"] if "default" in config else None
        else:
            self.language = None
            self.allow_message = None
            self.block_message = None
            self.encrypt_message = None
            self.readonly_message = None
            self.caution_message = None
            self.redirect_response_message = None
            self.default = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "language": self.language,
            "allowMessage": self.allow_message,
            "blockMessage": self.block_message,
            "encryptMessage": self.encrypt_message,
            "readonlyMessage": self.readonly_message,
            "cautionMessage": self.caution_message,
            "redirectResponseMessage": self.redirect_response_message,
            "default": self.default,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
