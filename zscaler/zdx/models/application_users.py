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
from zscaler.zdx.models import common


class ApplicationActiveUsers(ZscalerObject):
    """
    A class for active users, their devices, active geolocations objects.
    """

    def __init__(self, config=None):
        """
        Initialize the active users, their devices, active geolocations model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.next_offset = config["next_offset"] if "next_offset" in config else None

            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], common.CommonIDName
            )
        else:
            self.next_offset = None
            self.users = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "next_offset": self.next_offset,
            "users": self.users,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationUserDetails(ZscalerObject):
    """
    A class for ApplicationUserDetails objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ApplicationUserDetails model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.email = config["email"] if "email" in config else None
            self.score = config["score"] if "score" in config else None
            self.devices = ZscalerCollection.form_list(
                config["devices"] if "devices" in config else [], common.Devices
            )
        else:
            self.id = None
            self.name = None
            self.email = None
            self.score = None
            self.devices = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "score": self.score,
            "devices": self.devices,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
