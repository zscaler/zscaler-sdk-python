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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject


class UserManagement(ZscalerObject):
    """
    A class for UserManagement objects.
    """

    def __init__(self, config=None):
        """
        Initialize the UserManagement model based on API response.

        Args:
            config (dict): A dictionary representing the UserManagement configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None

            self.name = config["name"] if "name" in config else None

            self.email = config["email"] if "email" in config else None

            self.comments = config["comments"] if "comments" in config else None

            self.temp_auth_email = config["tempAuthEmail"] if "tempAuthEmail" in config else None

            self.password = config["password"] if "password" in config else None

            self.admin_user = config["adminUser"] if "adminUser" in config else False

            self.type = config["type"] if "type" in config else None

            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], Groups)

            if "department" in config:
                if isinstance(config["department"], Department):
                    self.department = config["department"]
                elif config["department"] is not None:
                    self.department = Department(config["department"])
                else:
                    self.department = None
            else:
                self.department = None

        else:
            self.id = None
            self.name = None
            self.email = None
            self.comments = None
            self.temp_auth_email = None
            self.password = None
            self.admin_user = False
            self.type = None
            self.groups = []
            self.department = {}

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "comments": self.comments,
            "tempAuthEmail": self.temp_auth_email,
            "password": self.password,
            "adminUser": self.admin_user,
            "type": self.type,
            "groups": [group.request_format() for group in self.groups] if self.groups else [],
            "department": self.department.request_format() if self.department else None,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Department(ZscalerObject):
    """
    A class for Department objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Department model based on API response.

        Args:
            config (dict): A dictionary representing the Department configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.comments = config["comments"] if "comments" in config else None
            self.idp_id = config["idpId"] if "idpId" in config else None
            self.deleted = config["deleted"] if "deleted" in config else None
        else:
            self.id = None
            self.name = None
            self.comments = None
            self.idp_id = None
            self.deleted = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "comments": self.comments,
            "idpId": self.idp_id,
            "deleted": self.deleted,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Groups(ZscalerObject):
    """
    A class for Groups objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Groups model based on API response.

        Args:
            config (dict): A dictionary representing the Groups configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None

            self.name = config["name"] if "name" in config else None

            self.comments = config["comments"] if "comments" in config else None

            self.idp_id = config["idpId"] if "idpId" in config else None

            self.is_system_defined = config["isSystemDefined"] if "isSystemDefined" in config else None
        else:
            self.id = None
            self.name = None
            self.comments = None
            self.idp_id = None
            self.is_system_defined = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "comments": self.comments,
            "idpId": self.idp_id,
            "isSystemDefined": self.is_system_defined,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
