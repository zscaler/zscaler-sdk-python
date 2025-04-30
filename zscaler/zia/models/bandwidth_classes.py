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


class BandwidthClasses(ZscalerObject):
    """
    A class for BandwidthClasses objects.
    """

    def __init__(self, config=None):
        """
        Initialize the BandwidthClasses model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.is_name_l10n_tag = config["isNameL10nTag"] if "isNameL10nTag" in config else None
            self.type = config["type"] if "type" in config else None
            self.name = config["name"] if "name" in config else None
            self.applications = ZscalerCollection.form_list(config["applications"] if "applications" in config else [], str)
            self.web_applications = ZscalerCollection.form_list(
                config["webApplications"] if "webApplications" in config else [], str
            )
            self.urls = ZscalerCollection.form_list(config["urls"] if "urls" in config else [], str)
            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], str
            )
        else:
            self.id = None
            self.is_name_l10n_tag = None
            self.type = None
            self.name = None
            self.applications = []
            self.web_applications = []
            self.urls = []
            self.url_categories = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "isNameL10nTag": self.is_name_l10n_tag,
            "type": self.type,
            "name": self.name,
            "applications": self.applications,
            "webApplications": self.web_applications,
            "urls": self.urls,
            "urlCategories": self.url_categories,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
