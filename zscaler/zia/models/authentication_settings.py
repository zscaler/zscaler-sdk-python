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


class AuthenticationSettings(ZscalerObject):
    """
    A class for AuthenticationSettings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AuthenticationSettings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.org_auth_type = config["orgAuthType"] if "orgAuthType" in config else None
            self.one_time_auth = config["oneTimeAuth"] if "oneTimeAuth" in config else None
            self.saml_enabled = config["samlEnabled"] if "samlEnabled" in config else False
            self.kerberos_enabled = config["kerberosEnabled"] if "kerberosEnabled" in config else False
            self.kerberos_pwd = config["kerberosPwd"] if "kerberosPwd" in config else None
            self.auth_frequency = config["authFrequency"] if "authFrequency" in config else None
            self.auth_custom_frequency = config["authCustomFrequency"] if "authCustomFrequency" in config else None
            self.password_strength = config["passwordStrength"] if "passwordStrength" in config else None
            self.password_expiry = config["passwordExpiry"] if "passwordExpiry" in config else None
            self.last_sync_start_time = config["lastSyncStartTime"] if "lastSyncStartTime" in config else None
            self.last_sync_end_time = config["lastSyncEndTime"] if "lastSyncEndTime" in config else None
            self.mobile_admin_saml_idp_enabled = (
                config["mobileAdminSamlIdpEnabled"] if "mobileAdminSamlIdpEnabled" in config else False
            )
            self.auto_provision = config["autoProvision"] if "autoProvision" in config else False
            self.directory_sync_migrate_to_scim_enabled = (
                config["directorySyncMigrateToScimEnabled"] if "directorySyncMigrateToScimEnabled" in config else False
            )
        else:
            self.org_auth_type = None
            self.one_time_auth = None
            self.saml_enabled = False
            self.kerberos_enabled = False
            self.kerberos_pwd = None
            self.auth_frequency = None
            self.auth_custom_frequency = None
            self.password_strength = None
            self.password_expiry = None
            self.last_sync_start_time = None
            self.last_sync_end_time = None
            self.mobile_admin_saml_idp_enabled = False
            self.auto_provision = False
            self.directory_sync_migrate_to_scim_enabled = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "orgAuthType": self.org_auth_type,
            "oneTimeAuth": self.one_time_auth,
            "samlEnabled": self.saml_enabled,
            "kerberosEnabled": self.kerberos_enabled,
            "kerberosPwd": self.kerberos_pwd,
            "authFrequency": self.auth_frequency,
            "authCustomFrequency": self.auth_custom_frequency,
            "passwordStrength": self.password_strength,
            "passwordExpiry": self.password_expiry,
            "lastSyncStartTime": self.last_sync_start_time,
            "lastSyncEndTime": self.last_sync_end_time,
            "mobileAdminSamlIdpEnabled": self.mobile_admin_saml_idp_enabled,
            "autoProvision": self.auto_provision,
            "directorySyncMigrateToScimEnabled": self.directory_sync_migrate_to_scim_enabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
