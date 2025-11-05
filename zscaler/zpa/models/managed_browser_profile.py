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


class ManagedBrowserProfile(ZscalerObject):
    """
    A class for ManagedBrowserProfile objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ManagedBrowserProfile model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.browser_type = config["browserType"] \
                if "browserType" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.customer_id = config["customerId"] \
                if "customerId" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] \
                if "microtenantName" in config else None

            if "chromePostureProfile" in config:
                if isinstance(config["chromePostureProfile"], ChromePostureProfile):
                    self.chrome_posture_profile = config["chromePostureProfile"]
                elif config["chromePostureProfile"] is not None:
                    self.chrome_posture_profile = ChromePostureProfile(config["chromePostureProfile"])
                else:
                    self.chrome_posture_profile = None
            else:
                self.chrome_posture_profile = None

        else:
            self.browser_type = None
            self.chrome_posture_profile = None
            self.creation_time = None
            self.customer_id = None
            self.description = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.microtenant_id = None
            self.microtenant_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "browserType": self.browser_type,
            "chromePostureProfile": self.chrome_posture_profile,
            "creationTime": self.creation_time,
            "customerId": self.customer_id,
            "description": self.description,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ChromePostureProfile(ZscalerObject):
    """
    A class for ChromePostureProfile objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the ChromePostureProfile model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.browser_type = config["browserType"] \
                if "browserType" in config else None
            self.crowd_strike_agent = config["crowdStrikeAgent"] \
                if "crowdStrikeAgent" in config else None
        else:
            self.id = None
            self.creation_time = None
            self.modified_by = None
            self.modified_time = None
            self.browser_type = None
            self.crowd_strike_agent = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "browserType": self.browser_type,
            "crowdStrikeAgent": self.crowd_strike_agent,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
