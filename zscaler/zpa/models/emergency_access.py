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


class EmergencyAccessUser(ZscalerObject):
    """
    Initialize the EmergencyAccessUser model based on API response.

    Args:
        config (dict): A dictionary representing the emergency access user configuration.
    """
    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.user_id = config["userId"] if config and "userId" in config else None
            self.first_name = config["firstName"] if config and "firstName" in config else None
            self.last_name = config["lastName"] if config and "lastName" in config else None
            self.email_id = config["emailId"] if config and "emailId" in config else None
            self.user_status = config["userStatus"] if config and "userStatus" in config else None
            self.activated_on = config["activatedOn"] if config and "activatedOn" in config else None
            self.last_login_time = config["lastLoginTime"] if config and "lastLoginTime" in config else None
            self.allowed_activate = config["allowedActivate"] if config and "allowedActivate" in config else None
            self.allowed_deactivate = config["allowedDeactivate"] if config and "allowedDeactivate" in config else None
            self.update_enabled = config["updateEnabled"] if config and "updateEnabled" in config else None

        else:
            self.user_id = None
            self.first_name = None
            self.last_name = None
            self.email_id = None
            self.user_status = None
            self.activated_on = None
            self.last_login_time = None
            self.allowed_activate = None
            self.allowed_deactivate = None
            self.update_enabled = None

    def request_format(self):
        """
        Formats the model data for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "userId": self.user_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "emailId": self.email_id,
            "userStatus": self.user_status,
            "activatedOn": self.activated_on,
            "lastLoginTime": self.last_login_time,
            "allowedActivate": self.allowed_activate,
            "allowedDeactivate": self.allowed_deactivate,
            "updateEnabled": self.update_enabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
