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


class AdminRoles(ZscalerObject):
    """
    A class for AdminRole objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.name = config["name"] if "name" in config else None
            self.role_type = config["roleType"] if "roleType" in config else None
            self.policy_access = config["policyAccess"] if "policyAccess" in config else None
            self.alerting_access = config["alertingAccess"] if "alertingAccess" in config else None
            self.dashboard_access = config["dashboardAccess"] if "dashboardAccess" in config else None
            self.report_access = config["reportAccess"] if "reportAccess" in config else None
            self.analysis_access = config["analysisAccess"] if "analysisAccess" in config else None
            self.username_access = config["usernameAccess"] if "usernameAccess" in config else None
            self.device_info_access = config["deviceInfoAccess"] if "deviceInfoAccess" in config else None
            self.admin_acct_access = config["adminAcctAccess"] if "adminAcctAccess" in config else None
            self.is_auditor = config["isAuditor"] if "isAuditor" in config else None
            self.is_non_editable = config["isNonEditable"] if "isNonEditable" in config else None
            self.logs_limit = config["logsLimit"] if "logsLimit" in config else None
            self.role_type = config["roleType"] if "roleType" in config else None
            self.report_time_duration = config["reportTimeDuration"] if "reportTimeDuration" in config else None

            self.permissions = ZscalerCollection.form_list(config["permissions"] if "permissions" in config else [], str)

            self.feature_permissions = config if isinstance(config, dict) else {}
            self.ext_feature_permissions = config if isinstance(config, dict) else {}

        else:
            self.id = None
            self.rank = None
            self.name = None
            self.policy_access = None
            self.alerting_access = None
            self.dashboard_access = None
            self.report_access = None
            self.analysis_access = None
            self.username_access = None
            self.device_info_access = None
            self.admin_acct_access = None
            self.is_auditor = None
            self.permissions = None
            self.feature_permissions = {}
            self.ext_feature_permissions = {}
            self.role_type = None
            self.report_time_duration = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "rank": self.rank,
            "name": self.name,
            "policyAccess": self.policy_access,
            "alertingAccess": self.alerting_access,
            "dashboardAccess": self.dashboard_access,
            "reportAccess": self.report_access,
            "analysisAccess": self.analysis_access,
            "usernameAccess": self.username_access,
            "deviceInfoAccess": self.device_info_access,
            "adminAcctAccess": self.admin_acct_access,
            "isAuditor": self.is_auditor,
            "roleType": self.role_type,
            "reportTimeDuration": self.report_time_duration,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PasswordExpiry(ZscalerObject):
    """
    A class for PasswordExpiry objects.
    Handles Password Expiry attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the PasswordExpiry model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.password_expiration_enabled = (
                config["passwordExpirationEnabled"] if "passwordExpirationEnabled" in config else None
            )

            self.password_expiry_days = config["passwordExpiryDays"] if "passwordExpiryDays" in config else None

        else:
            self.password_expiration_enabled = None
            self.password_expiry_days = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "passwordExpirationEnabled": self.password_expiration_enabled,
            "passwordExpiryDays": self.password_expiry_days,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
