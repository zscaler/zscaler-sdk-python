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


class CBIBanner(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the CBIBanner model based on API response.

        Args:
            config (dict): A dictionary representing the cloud browser isolation banner.
        """
        super().__init__(config)

        # Using defensive programming to check each key's presence
        self.id = config["id"] if config and "id" in config else None
        self.name = config["name"] if config and "name" in config else None
        self.primary_color = config["primaryColor"] if config and "primaryColor" in config else None
        self.text_color = config["textColor"] if config and "textColor" in config else None
        self.notification_title = config["notificationTitle"] if config and "notificationTitle" in config else None
        self.notification_text = config["notificationText"] if config and "notificationText" in config else None
        self.logo = config["logo"] if config and "logo" in config else None
        self.banner = config["banner"] if config and "banner" in config else None
        self.persist = config["persist"] if config and "persist" in config else None
        self.is_default = config["isDefault"] if config and "isDefault" in config else None

    def request_format(self):
        """
        Formats the model data for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "primaryColor": self.primary_color,
            "textColor": self.text_color,
            "notificationTitle": self.notification_title,
            "notificationText": self.notification_text,
            "logo": self.logo,
            "banner": self.banner,
            "persist": self.persist,
            "isDefault": self.is_default,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
