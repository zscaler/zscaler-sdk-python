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
from zscaler.ztw.models import admin_roles as admin_roles


class AdminUsers(ZscalerObject):
    """
    A class for AdminUsers objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdminUsers model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.login_name = config["loginName"] if "loginName" in config else None
            self.user_name = config["userName"] if "userName" in config else None
            self.email = config["email"] if "email" in config else None
            self.comments = config["comments"] if "comments" in config else None
            self.admin_scopescope_group_member_entities = ZscalerCollection.form_list(
                config["adminScopescopeGroupMemberEntities"] if "adminScopescopeGroupMemberEntities" in config else [], str
            )
            self.admin_scope_type = config["adminScopeType"] if "adminScopeType" in config else None
            self.admin_scope_scope_entities = ZscalerCollection.form_list(
                config["adminScopeScopeEntities"] if "adminScopeScopeEntities" in config else [], str
            )
            self.is_default_admin = config["isDefaultAdmin"] if "isDefaultAdmin" in config else None
            self.disabled = config["disabled"] if "disabled" in config else None
            self.is_deprecated_default_admin = (
                config["isDeprecatedDefaultAdmin"] if "isDeprecatedDefaultAdmin" in config else None
            )
            self.is_auditor = config["isAuditor"] if "isAuditor" in config else None
            self.password = config["password"] if "password" in config else None
            self.is_password_login_allowed = config["isPasswordLoginAllowed"] if "isPasswordLoginAllowed" in config else None
            self.is_security_report_comm_enabled = (
                config["isSecurityReportCommEnabled"] if "isSecurityReportCommEnabled" in config else None
            )
            self.is_service_update_comm_enabled = (
                config["isServiceUpdateCommEnabled"] if "isServiceUpdateCommEnabled" in config else None
            )
            self.is_product_update_comm_enabled = (
                config["isProductUpdateCommEnabled"] if "isProductUpdateCommEnabled" in config else None
            )
            self.pwd_last_modified_time = config["pwdLastModifiedTime"] if "pwdLastModifiedTime" in config else None
            self.is_password_expired = config["isPasswordExpired"] if "isPasswordExpired" in config else None
            self.is_exec_mobile_app_enabled = config["isExecMobileAppEnabled"] if "isExecMobileAppEnabled" in config else None
            self.send_mobile_app_invite = config["sendMobileAppInvite"] if "sendMobileAppInvite" in config else None
            self.exec_mobile_app_tokens = ZscalerCollection.form_list(
                config["execMobileAppTokens"] if "execMobileAppTokens" in config else [], str
            )
            self.new_location_create_allowed = (
                config["newLocationCreateAllowed"] if "newLocationCreateAllowed" in config else None
            )
            self.send_zdx_onboard_invite = config["sendZdxOnboardInvite"] if "sendZdxOnboardInvite" in config else None
            self.name = config["name"] if "name" in config else None

            if "role" in config:
                if isinstance(config["role"], admin_roles.AdminRoles):
                    self.role = config["role"]
                elif config["role"] is not None:
                    self.role = admin_roles.AdminRoles(config["role"])
                else:
                    self.role = None
            else:
                self.role = None
        else:
            self.id = None
            self.login_name = None
            self.user_name = None
            self.email = None
            self.role = None
            self.comments = None
            self.admin_scopescope_group_member_entities = ZscalerCollection.form_list([], str)
            self.admin_scope_type = None
            self.admin_scope_scope_entities = ZscalerCollection.form_list([], str)
            self.is_default_admin = None
            self.disabled = None
            self.is_deprecated_default_admin = None
            self.is_auditor = None
            self.password = None
            self.is_password_login_allowed = None
            self.is_security_report_comm_enabled = None
            self.is_service_update_comm_enabled = None
            self.is_product_update_comm_enabled = None
            self.pwd_last_modified_time = None
            self.is_password_expired = None
            self.is_exec_mobile_app_enabled = None
            self.send_mobile_app_invite = None
            self.exec_mobile_app_tokens = ZscalerCollection.form_list([], str)
            self.new_location_create_allowed = None
            self.send_zdx_onboard_invite = None
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
            "role": self.role,
            "comments": self.comments,
            "adminScopescopeGroupMemberEntities": self.admin_scopescope_group_member_entities,
            "adminScopeType": self.admin_scope_type,
            "adminScopeScopeEntities": self.admin_scope_scope_entities,
            "isDefaultAdmin": self.is_default_admin,
            "disabled": self.disabled,
            "isDeprecatedDefaultAdmin": self.is_deprecated_default_admin,
            "isAuditor": self.is_auditor,
            "password": self.password,
            "isPasswordLoginAllowed": self.is_password_login_allowed,
            "isSecurityReportCommEnabled": self.is_security_report_comm_enabled,
            "isServiceUpdateCommEnabled": self.is_service_update_comm_enabled,
            "isProductUpdateCommEnabled": self.is_product_update_comm_enabled,
            "pwdLastModifiedTime": self.pwd_last_modified_time,
            "isPasswordExpired": self.is_password_expired,
            "isExecMobileAppEnabled": self.is_exec_mobile_app_enabled,
            "sendMobileAppInvite": self.send_mobile_app_invite,
            "execMobileAppTokens": self.exec_mobile_app_tokens,
            "newLocationCreateAllowed": self.new_location_create_allowed,
            "sendZdxOnboardInvite": self.send_zdx_onboard_invite,
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
