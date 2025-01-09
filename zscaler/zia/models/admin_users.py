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
from zscaler.zia.models import admin_roles\
    as admin_roles

class AdminUser(ZscalerObject):
    """
    A class for AdminUser objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"]\
                if "id" in config else None
            self.login_name = config["loginName"]\
                if "loginName" in config else None
            self.user_name = config["userName"]\
                if "userName" in config else None
            self.email = config["email"]\
                if "email" in config else None

            # Role object
            if "role" in config:
                if isinstance(config["role"], admin_roles.AdminRoles):
                    self.role = config["role"]
                elif config["role"] is not None:
                    self.role = admin_roles.AdminRoles(config["role"])
                else:
                    self.role = None
            else:
                self.role = None

            self.admin_scope_group_member_entities = config["adminScopescopeGroupMemberEntities"] if "adminScopescopeGroupMemberEntities" in config else []
            self.admin_scope_type = config["adminScopeType"] if "adminScopeType" in config else None
            self.admin_scope_scope_entities = config["adminScopeScopeEntities"] if "adminScopeScopeEntities" in config else []
            self.disabled = config["disabled"] if "disabled" in config else False
            self.pwd_last_modified_time = config["pwdLastModifiedTime"] if "pwdLastModifiedTime" in config else 0
            self.name = config["name"] if "name" in config else None
        else:
            self.id = None
            self.login_name = None
            self.user_name = None
            self.email = None
            self.role = None
            self.admin_scope_group_member_entities = []
            self.admin_scope_type = None
            self.admin_scope_scope_entities = []
            self.disabled = False
            self.pwd_last_modified_time = 0
            self.name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "loginName": self.login_name,
            "userName": self.user_name,
            "email": self.email,
            "role": self.role.request_format() if self.role else None,
            "adminScopescopeGroupMemberEntities": self.admin_scope_group_member_entities,
            "adminScopeType": self.admin_scope_type,
            "adminScopeScopeEntities": self.admin_scope_scope_entities,
            "disabled": self.disabled,
            "pwdLastModifiedTime": self.pwd_last_modified_time,
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
