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


class MobileAdvancedThreatSettings(ZscalerObject):
    """
    A class for MobileAdvancedThreatSettings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the MobileAdvancedThreatSettings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.block_apps_with_malicious_activity = (
                config["blockAppsWithMaliciousActivity"] if "blockAppsWithMaliciousActivity" in config else None
            )
            self.block_apps_with_known_vulnerabilities = (
                config["blockAppsWithKnownVulnerabilities"] if "blockAppsWithKnownVulnerabilities" in config else None
            )
            self.block_apps_sending_unencrypted_user_credentials = (
                config["blockAppsSendingUnencryptedUserCredentials"]
                if "blockAppsSendingUnencryptedUserCredentials" in config
                else None
            )
            self.block_apps_sending_location_info = (
                config["blockAppsSendingLocationInfo"] if "blockAppsSendingLocationInfo" in config else None
            )
            self.block_apps_sending_personally_identifiable_info = (
                config["blockAppsSendingPersonallyIdentifiableInfo"]
                if "blockAppsSendingPersonallyIdentifiableInfo" in config
                else None
            )
            self.block_apps_sending_device_identifier = (
                config["blockAppsSendingDeviceIdentifier"] if "blockAppsSendingDeviceIdentifier" in config else None
            )
            self.block_apps_communicating_with_ad_websites = (
                config["blockAppsCommunicatingWithAdWebsites"] if "blockAppsCommunicatingWithAdWebsites" in config else None
            )
            self.block_apps_communicating_with_remote_unknown_servers = (
                config["blockAppsCommunicatingWithRemoteUnknownServers"]
                if "blockAppsCommunicatingWithRemoteUnknownServers" in config
                else None
            )
        else:
            self.block_apps_with_malicious_activity = None
            self.block_apps_with_known_vulnerabilities = None
            self.block_apps_sending_unencrypted_user_credentials = None
            self.block_apps_sending_location_info = None
            self.block_apps_sending_personally_identifiable_info = None
            self.block_apps_sending_device_identifier = None
            self.block_apps_communicating_with_ad_websites = None
            self.block_apps_communicating_with_remote_unknown_servers = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "blockAppsWithMaliciousActivity": self.block_apps_with_malicious_activity,
            "blockAppsWithKnownVulnerabilities": self.block_apps_with_known_vulnerabilities,
            "blockAppsSendingUnencryptedUserCredentials": self.block_apps_sending_unencrypted_user_credentials,
            "blockAppsSendingLocationInfo": self.block_apps_sending_location_info,
            "blockAppsSendingPersonallyIdentifiableInfo": self.block_apps_sending_personally_identifiable_info,
            "blockAppsSendingDeviceIdentifier": self.block_apps_sending_device_identifier,
            "blockAppsCommunicatingWithAdWebsites": self.block_apps_communicating_with_ad_websites,
            "blockAppsCommunicatingWithRemoteUnknownServers": self.block_apps_communicating_with_remote_unknown_servers,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
