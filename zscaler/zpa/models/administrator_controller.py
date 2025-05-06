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
from zscaler.zia.models import common


class AdministratorController(ZscalerObject):
    """
    A class for AdministratorController objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdministratorController model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] \
                if "microtenantName" in config else None
            self.username = config["username"] \
                if "username" in config else None
            self.display_name = config["displayName"] \
                if "displayName" in config else None
            self.email = config["email"] \
                if "email" in config else None
            self.customer_id = config["customerId"] \
                if "customerId" in config else None
            self.timezone = config["timezone"] \
                if "timezone" in config else None
            self.is_deleted = config["isDeleted"] \
                if "isDeleted" in config else None
            self.password = config["password"] \
                if "password" in config else None
            self.tmp_password = config["tmpPassword"] \
                if "tmpPassword" in config else None
            self.tmp_email = config["tmpEmail"] \
                if "tmpEmail" in config else None
            self.role = config["role"] \
                if "role" in config else None
            self.comments = config["comments"] \
                if "comments" in config else None
            self.language_code = config["languageCode"] \
                if "languageCode" in config else None
            self.eula = config["eula"] \
                if "eula" in config else None
            self.department = config["department"] \
                if "department" in config else None
            self.is_enabled = config["isEnabled"] \
                if "isEnabled" in config else None
            self.two_factor_auth_enabled = config["twoFactorAuthEnabled"] \
                if "twoFactorAuthEnabled" in config else None
            self.phone_number = config["phoneNumber"] \
                if "phoneNumber" in config else None
            self.force_pwd_change = config["forcePwdChange"] \
                if "forcePwdChange" in config else None
            self.two_factor_auth_type = config["twoFactorAuthType"] \
                if "twoFactorAuthType" in config else None
            self.pin_session = config["pinSession"] \
                if "pinSession" in config else None
            self.local_login_disabled = config["localLoginDisabled"] \
                if "localLoginDisabled" in config else None
            self.is_locked = config["isLocked"] \
                if "isLocked" in config else None
            self.delivery_tag = config["deliveryTag"] \
                if "deliveryTag" in config else None
            self.operation_type = config["operationType"] \
                if "operationType" in config else None
            self.sync_version = config["syncVersion"] \
                if "syncVersion" in config else None
            self.token_id = config["tokenId"] \
                if "tokenId" in config else None
            self.group_id = ZscalerCollection.form_list(
                config["groupIds"] if "groupIds" in config else [], str
            )
        else:
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.id = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.username = None
            self.display_name = None
            self.email = None
            self.customer_id = None
            self.timezone = None
            self.is_deleted = None
            self.password = None
            self.tmp_password = None
            self.tmp_email = None
            self.role = None
            self.comments = None
            self.language_code = None
            self.eula = None
            self.department = None
            self.is_enabled = None
            self.two_factor_auth_enabled = None
            self.phone_number = None
            self.force_pwd_change = None
            self.two_factor_auth_type = None
            self.pin_session = None
            self.local_login_disabled = None
            self.is_locked = None
            self.delivery_tag = None
            self.operation_type = None
            self.sync_version = None
            self.token_id = None
            self.group_id = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "id": self.id,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "username": self.username,
            "displayName": self.display_name,
            "email": self.email,
            "customerId": self.customer_id,
            "timezone": self.timezone,
            "isDeleted": self.is_deleted,
            "password": self.password,
            "tmpPassword": self.tmp_password,
            "tmpEmail": self.tmp_email,
            "role": self.role,
            "comments": self.comments,
            "languageCode": self.language_code,
            "eula": self.eula,
            "department": self.department,
            "isEnabled": self.is_enabled,
            "twoFactorAuthEnabled": self.two_factor_auth_enabled,
            "phoneNumber": self.phone_number,
            "forcePwdChange": self.force_pwd_change,
            "twoFactorAuthType": self.two_factor_auth_type,
            "pinSession": self.pin_session,
            "localLoginDisabled": self.local_login_disabled,
            "isLocked": self.is_locked,
            "groupId": self.group_id,
            "deliveryTag": self.delivery_tag,
            "operationType": self.operation_type,
            "syncVersion": self.sync_version,
            "tokenId": self.token_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
