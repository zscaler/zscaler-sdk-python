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


class RoleController(ZscalerObject):
    """
    A class for RoleController objects.
    """

    def __init__(self, config=None):
        """
        Initialize the RoleController model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] \
                if "microtenantName" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.bypass_remote_assistance_check = config["bypassRemoteAssistanceCheck"] \
                if "bypassRemoteAssistanceCheck" in config else None

            self.custom_role = config["customRole"] \
                if "customRole" in config else None
            self.system_role = config["systemRole"] \
                if "systemRole" in config else None
            self.restricted_role = config["restrictedRole"] \
                if "restrictedRole" in config else None
            self.users = config["users"] \
                if "users" in config else None
            self.api_keys = config["apiKeys"] \
                if "apiKeys" in config else None
            self.new_audit_message = config["newAuditMessage"] \
                if "newAuditMessage" in config else None
            self.old_audit_message = config["oldAuditMessage"] \
                if "oldAuditMessage" in config else None

            self.permissions = ZscalerCollection.form_list(
                config["permissions"] if "permissions" in config else [], Permissions
            )

            self.class_permission_groups = ZscalerCollection.form_list(
                config["classPermissionGroups"] if "classPermissionGroups" in config else [], ClassPermissionGroups
            )

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.description = None
            self.bypass_remote_assistance_check = None
            self.permissions = []
            self.system_role = None
            self.restricted_role = None
            self.class_permission_groups = []
            self.users = None
            self.api_keys = None
            self.new_audit_message = None
            self.old_audit_message = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "description": self.description,
            "bypassRemoteAssistanceCheck": self.bypass_remote_assistance_check,
            "permissions": self.permissions,
            "customRole": self.custom_role,
            "systemRole": self.system_role,
            "restrictedRole": self.restricted_role,
            "classPermissionGroups": self.class_permission_groups,
            "users": self.users,
            "apiKeys": self.api_keys,
            "newAuditMessage": self.new_audit_message,
            "oldAuditMessage": self.old_audit_message
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Permissions(ZscalerObject):
    """
    A class for Permissions objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Permissions model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.permission_mask = config["permissionMask"] \
                if "permissionMask" in config else None
            self.role = config["role"] \
                if "role" in config else None
            self.customer_id = config["customerId"] \
                if "customerId" in config else None

            if "classType" in config:
                if isinstance(config["classType"], ClassType):
                    self.class_type = config["classType"]
                elif config["classType"] is not None:
                    self.class_type = ClassType(config["classType"])
                else:
                    self.class_type = None
            else:
                self.class_type = None
        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.permission_mask = None
            self.class_type = None
            self.role = None
            self.customer_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "permissionMask": self.permission_mask,
            "classType": self.class_type,
            "role": self.role,
            "customerId": self.customer_id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ClassType(ZscalerObject):
    """
    A class for ClassType objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ClassType model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.acl_class = config["aclClass"] \
                if "aclClass" in config else None
            self.friendly_name = config["friendlyName"] \
                if "friendlyName" in config else None
            self.local_scope_mask = config["localScopeMask"] \
                if "localScopeMask" in config else None
            self.customer_id = config["customerId"] \
                if "customerId" in config else None
        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.acl_class = None
            self.friendly_name = None
            self.local_scope_mask = None
            self.customer_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "aclClass": self.acl_class,
            "friendlyName": self.friendly_name,
            "localScopeMask": self.local_scope_mask,
            "customerId": self.customer_id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ClassPermissionGroups(ZscalerObject):
    """
    A class for ClassPermissionGroups objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ClassPermissionGroups model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.hidden = config["hidden"] \
                if "hidden" in config else None
            self.internal = config["internal"] \
                if "internal" in config else None
            self.local_scope_permission_group = config["localScopePermissionGroup"] \
                if "localScopePermissionGroup" in config else None

            self.class_permissions = ZscalerCollection.form_list(
                config["classPermissions"] if "classPermissions" in config else [], ClassPermissions
            )

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.hidden = None
            self.internal = None
            self.local_scope_permission_group = None
            self.class_permissions = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "hidden": self.hidden,
            "internal": self.internal,
            "localScopePermissionGroup": self.local_scope_permission_group,
            "classPermissions": self.class_permissions
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ClassPermissions(ZscalerObject):
    """
    A class for ClassPermissions objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ClassPermissions model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None

            if "permission" in config:
                if isinstance(config["permission"], Permission):
                    self.permission = config["permission"]
                elif config["permission"] is not None:
                    self.permission = Permission(config["permission"])
                else:
                    self.permission = None
            else:
                self.permission = None

            if "classType" in config:
                if isinstance(config["classType"], ClassType):
                    self.class_type = config["classType"]
                elif config["classType"] is not None:
                    self.class_type = ClassType(config["classType"])
                else:
                    self.class_type = None
            else:
                self.class_type = None

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.permission = None
            self.class_type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "permission": self.permission,
            "classType": self.class_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Permission(ZscalerObject):
    """
    A class for Permission objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Permission model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.mask = config["mask"] \
                if "mask" in config else None
            self.type = config["type"] \
                if "type" in config else None
            self.max_mask = config["maxMask"] \
                if "maxMask" in config else None

        else:
            self.mask = None
            self.type = None
            self.max_mask = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "mask": self.mask,
            "type": self.type,
            "max_mask": self.max_mask,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
