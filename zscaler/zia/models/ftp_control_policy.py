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


class FTPControlPolicy(ZscalerObject):
    """
    A class for FTPControlPolicy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the FTPControlPolicy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.ftp_over_http_enabled = config["ftpOverHttpEnabled"] if "ftpOverHttpEnabled" in config else None
            self.ftp_enabled = config["ftpEnabled"] if "ftpEnabled" in config else None

            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], str
            )
            self.urls = ZscalerCollection.form_list(config["urls"] if "urls" in config else [], str)
        else:
            self.ftp_over_http_enabled = None
            self.ftp_enabled = None
            self.url_categories = []
            self.urls = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ftpOverHttpEnabled": self.ftp_over_http_enabled,
            "ftpEnabled": self.ftp_enabled,
            "urlCategories": self.url_categories,
            "urls": self.urls,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
