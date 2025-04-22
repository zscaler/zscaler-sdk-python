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


class Users(ZscalerObject):
    """
    A class for Users objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Users model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)
        print(f"DEBUG: Raw config received in Users: {config}")  # Debugging input

        if config:
            self.users = ZscalerCollection.form_list(config.get("users", []), UserDetails)
            self.next_offset = config.get("next_offset")

        else:
            self.users = []
            self.next_offset = None

        print(f"DEBUG: Parsed Users object - {len(self.users)} users found")

    def as_list(self):
        """
        Return the list of user objects.
        """
        return self.users  # ✅ This ensures `list_users` returns a list, not an object.

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"users": [user.as_dict() for user in self.users], "next_offset": self.next_offset}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class UserDetails(ZscalerObject):
    """
    A class for Users objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Users model based on API response.

        Args:
            config (dict): A dictionary representing the Department configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.email = config["email"] if "email" in config else None
            self.score = config["score"] if "score" in config else None
        else:
            self.id = None
            self.name = None
            self.email = None
            self.score = None

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
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
