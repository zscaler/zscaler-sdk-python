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


class CloudApplicationPolicy(ZscalerObject):
    """
    A class for CloudApplicationPolicy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the CloudApplicationPolicy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.app = config["app"] if "app" in config else None
            self.app_name = config["appName"] if "appName" in config else None
            self.parent = config["parent"] if "parent" in config else None
            self.parent_name = config["parentName"] if "parentName" in config else None
        else:
            self.app = None
            self.app_name = None
            self.parent = None
            self.parent_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"app": self.app, "appName": self.app_name, "parent": self.parent, "parentName": self.parent_name}
        parent_req_format.update(current_obj_format)
        return parent_req_format
