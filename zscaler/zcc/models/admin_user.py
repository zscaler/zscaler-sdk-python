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


class AdminUser(ZscalerObject):
    """
    A class for Adminuser objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdminUser model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.account_enabled = config["accountEnabled"] if "accountEnabled" in config else None
            self.company_id = config["companyId"] if "companyId" in config else None
            self.company_role = config["companyRole"] if "companyRole" in config else None
            self.edit_enabled = config["editEnabled"] if "editEnabled" in config else None
            self.id = config["id"] if "id" in config else None
            self.is_default_admin = config["isDefaultAdmin"] if "isDefaultAdmin" in config else None
            self.service_type = config["serviceType"] if "serviceType" in config else None
            self.user_name = config["userName"] if "userName" in config else None
        else:
            self.account_enabled = None
            self.company_id = None
            self.company_role = None
            self.edit_enabled = None
            self.id = None
            self.is_default_admin = None
            self.service_type = None
            self.user_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "accountEnabled": self.account_enabled,
            "companyId": self.company_id,
            "companyRole": self.company_role,
            "editEnabled": self.edit_enabled,
            "id": self.id,
            "isDefaultAdmin": self.is_default_admin,
            "serviceType": self.service_type,
            "userName": self.user_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
