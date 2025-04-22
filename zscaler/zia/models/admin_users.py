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
from zscaler.zia.models import admin_roles as admin_roles


class AdminUser(ZscalerObject):
    """
    A class for AdminUser objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None

            self.login_name = config["loginName"] if "loginName" in config else None

            self.user_name = config["userName"] if "userName" in config else None

            self.email = config["email"] if "email" in config else None

            self.comments = config["comments"] if "comments" in config else None

            self.is_non_editable = config["isNonEditable"] if "isNonEditable" in config else False

            self.disabled = config["disabled"] if "disabled" in config else False

            self.is_auditor = config["isAuditor"] if "isAuditor" in config else False

            self.password = config["password"] if "password" in config else None

            self.is_password_login_allowed = config["isPasswordLoginAllowed"] if "isPasswordLoginAllowed" in config else False

            self.is_security_report_comm_enabled = (
                config["isSecurityReportCommEnabled"] if "isSecurityReportCommEnabled" in config else False
            )

            self.is_service_update_comm_enabled = (
                config["isServiceUpdateCommEnabled"] if "isServiceUpdateCommEnabled" in config else False
            )

            self.is_product_update_comm_enabled = (
                config["isProductUpdateCommEnabled"] if "isProductUpdateCommEnabled" in config else False
            )

            self.is_password_expired = config["isPasswordExpired"] if "isPasswordExpired" in config else False

            self.is_exec_mobile_app_enabled = config["isExecMobileAppEnabled"] if "isExecMobileAppEnabled" in config else False

            self.new_location_create_allowed = (
                config["newLocationCreateAllowed"] if "newLocationCreateAllowed" in config else False
            )

            self.exec_mobile_app_tokens = ZscalerCollection.form_list(
                config["execMobileAppTokens"] if "execMobileAppTokens" in config else [], ExecMobileAppTokens
            )

            if "role" in config:
                if isinstance(config["role"], admin_roles.AdminRoles):
                    self.role = config["role"]
                elif config["role"] is not None:
                    self.role = admin_roles.AdminRoles(config["role"])
                else:
                    self.role = None
            else:
                self.role = None

            if "adminScope" in config:
                if isinstance(config["adminScope"], AdminScope):
                    self.admin_scope = config["adminScope"]
                elif config["adminScope"] is not None:
                    self.admin_scope = AdminScope(config["adminScope"])
                else:
                    self.admin_scope = None
            else:
                self.admin_scope = None

            self.admin_scope_group_member_entities = (
                config["adminScopescopeGroupMemberEntities"] if "adminScopescopeGroupMemberEntities" in config else []
            )
            self.admin_scope_type = config["adminScopeType"] if "adminScopeType" in config else None
            self.admin_scope_scope_entities = config["adminScopeScopeEntities"] if "adminScopeScopeEntities" in config else []
        else:
            self.id = None
            self.login_name = None
            self.user_name = None
            self.email = None
            self.comments = None
            self.is_non_editable = None
            self.disabled = None
            self.is_auditor = None
            self.password = None
            self.is_password_login_allowed = None
            self.is_security_report_comm_enabled = None
            self.is_service_update_comm_enabled = None
            self.is_product_update_comm_enabled = None
            self.is_password_expired = None
            self.is_exec_mobile_app_enabled = None
            self.new_location_create_allowed = None
            self.role = None
            self.admin_scope_group_member_entities = []
            self.admin_scope_type = None
            self.admin_scope_scope_entities = []

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
            "comments": self.comments,
            "isNonEditable": self.is_non_editable,
            "disabled": self.disabled,
            "isAuditor": self.is_auditor,
            "password": self.password,
            "isPasswordLoginAllowed": self.is_password_login_allowed,
            "isSecurityReportCommEnabled": self.is_security_report_comm_enabled,
            "isServiceUpdateCommEnabled": self.is_service_update_comm_enabled,
            "isProductUpdateCommEnabled": self.is_product_update_comm_enabled,
            "isPasswordExpired": self.is_password_expired,
            "isExecMobileAppEnabled": self.is_exec_mobile_app_enabled,
            "newLocationCreateAllowed": self.new_location_create_allowed,
            "role": self.role,
            "adminScopescopeGroupMemberEntities": self.admin_scope_group_member_entities,
            "adminScopeType": self.admin_scope_type,
            "adminScopeScopeEntities": self.admin_scope_scope_entities,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AdminScope(ZscalerObject):
    """
    A class for AdminScope objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdminScope model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.type = config["Type"] if "Type" in config else None

            self.scope_group_member_entities = ZscalerCollection.form_list(
                config["scopeGroupMemberEntities"] if "scopeGroupMemberEntities" in config else [], ScopeGroupMemberEntities
            )
            self.scope_entities = ZscalerCollection.form_list(
                config["ScopeEntities"] if "ScopeEntities" in config else [], ScopeEntities
            )

        else:
            self.scope_group_member_entities = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "scopeGroupMemberEntities": self.scope_group_member_entities,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ScopeGroupMemberEntities(ZscalerObject):
    """
    A class for ScopeGroupMemberEntities objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdminScope model based on API response.

        Args:
            config (dict): A dictionary representing the ScopeGroupMemberEntities configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.external_id = config["externalId"] if "externalId" in config else None
            self.extensions = config if isinstance(config, dict) else {}

        else:
            self.id = None
            self.name = None
            self.extensions = None
            self.external_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "extensions": self.extensions,
            "externalId": self.external_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ScopeEntities(ZscalerObject):
    """
    A class for ScopeEntities objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdminScope model based on API response.

        Args:
            config (dict): A dictionary representing the ScopeEntities configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.external_id = config["externalId"] if "externalId" in config else None

            self.extensions = config if isinstance(config, dict) else {}

        else:
            self.id = None
            self.name = None
            self.external_id = None
            self.extensions = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "externalId": self.external_id,
            "extensions": self.extensions,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ExecMobileAppTokens(ZscalerObject):
    """
    A class for ExecMobileAppTokens objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdminScope model based on API response.

        Args:
            config (dict): A dictionary representing the ExecMobileAppTokens configuration.
        """
        super().__init__(config)

        if config:
            self.cloud = config["cloud"] if "cloud" in config else None
            self.org_id = config["orgId"] if "orgId" in config else None
            self.name = config["name"] if "name" in config else None
            self.token_id = config["tokenId"] if "tokenId" in config else None
            self.token = config["token"] if "token" in config else None
            self.token_expiry = config["tokenExpiry"] if "tokenExpiry" in config else None
            self.create_time = config["createTime"] if "createTime" in config else None
            self.device_id = config["deviceId"] if "deviceId" in config else None
            self.device_name = config["deviceName"] if "deviceName" in config else None

        else:
            self.cloud = None
            self.org_id = None
            self.name = None
            self.token_id = None
            self.token = None
            self.token_expiry = None
            self.create_time = None
            self.device_id = None
            self.device_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "cloud": self.cloud,
            "orgId": self.org_id,
            "name": self.name,
            "tokenId": self.token_id,
            "token": self.token,
            "tokenExpiry": self.token_expiry,
            "createTime": self.create_time,
            "deviceId": self.device_id,
            "deviceName": self.device_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
