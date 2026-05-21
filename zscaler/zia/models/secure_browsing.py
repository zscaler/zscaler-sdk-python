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

from typing import Any, Dict, List, Optional
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import cloud_browser_isolation as isolation

class BrowserControlSettings(ZscalerObject):
    """
    A class for Secure Browsing objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Secure Browsing model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.enable_smart_browser_isolation: Optional[Any] = config["enableSmartBrowserIsolation"] \
                if "enableSmartBrowserIsolation" in config else None
            self.enable_warnings: Optional[Any] = config["enableWarnings"] \
                if "enableWarnings" in config else None
            self.plugin_check_frequency: Optional[Any] = config["pluginCheckFrequency"] \
                if "pluginCheckFrequency" in config else None
            self.bypass_plugins: List[Any] = ZscalerCollection.form_list(
                config["bypassPlugins"] if "bypassPlugins" in config else [], str
            )
            self.bypass_applications: List[Any] = ZscalerCollection.form_list(
                config["bypassApplications"] if "bypassApplications" in config else [], str
            )
            self.allow_all_browsers: Optional[Any] = config["allowAllBrowsers"] \
                if "allowAllBrowsers" in config else None
            self.bypass_all_browsers: Optional[Any] = config["bypassAllBrowsers"] \
                if "bypassAllBrowsers" in config else None
            self.blocked_chrome_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedChromeVersions"] if "blockedChromeVersions" in config else [], str
            )
            self.blocked_firefox_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedFirefoxVersions"] if "blockedFirefoxVersions" in config else [], str
            )
            self.blocked_internet_explorer_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedInternetExplorerVersions"] if "blockedInternetExplorerVersions" in config else [], str
            )
            self.blocked_opera_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedOperaVersions"] if "blockedOperaVersions" in config else [], str
            )
            self.blocked_safari_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedSafariVersions"] if "blockedSafariVersions" in config else [], str
            )
            if "smartIsolationProfile" in config:
                if isinstance(config["smartIsolationProfile"], isolation.CBIProfile):
                    self.smart_isolation_profile: Optional[isolation.CBIProfile] = config["smartIsolationProfile"]
                elif config["smartIsolationProfile"] is not None:
                    self.smart_isolation_profile = isolation.CBIProfile(config["smartIsolationProfile"])
                else:
                    self.smart_isolation_profile = None
            else:
                self.smart_isolation_profile: Optional[isolation.CBIProfile] = None
            self.smart_isolation_profile_id: Optional[Any] = config["smartIsolationProfileId"] \
                if "smartIsolationProfileId" in config else None
        else:
            self.enable_smart_browser_isolation: Optional[Any] = None
            self.enable_warnings: Optional[Any] = None
            self.plugin_check_frequency: Optional[Any] = None
            self.bypass_plugins: List[Any] = []
            self.bypass_applications: List[Any] = []
            self.allow_all_browsers: Optional[Any] = None
            self.bypass_all_browsers: Optional[Any] = None
            self.blocked_chrome_versions: List[Any] = []
            self.blocked_firefox_versions: List[Any] = []
            self.blocked_internet_explorer_versions: List[Any] = []
            self.blocked_opera_versions: List[Any] = []
            self.blocked_safari_versions: List[Any] = []
            self.smart_isolation_profile: Optional[SmartIsolationProfile] = None
            self.smart_isolation_profile_id: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "enableSmartBrowserIsolation": self.enable_smart_browser_isolation,
            "enableWarnings": self.enable_warnings,
            "pluginCheckFrequency": self.plugin_check_frequency,
            "bypassPlugins": self.bypass_plugins,
            "bypassApplications": self.bypass_applications,
            "allowAllBrowsers": self.allow_all_browsers,
            "bypassAllBrowsers": self.bypass_all_browsers,
            "blockedChromeVersions": self.blocked_chrome_versions,
            "blockedFirefoxVersions": self.blocked_firefox_versions,
            "blockedInternetExplorerVersions": self.blocked_internet_explorer_versions,
            "blockedOperaVersions": self.blocked_opera_versions,
            "blockedSafariVersions": self.blocked_safari_versions,
            "smartIsolationProfile": self.smart_isolation_profile,
            "smartIsolationProfileId": self.smart_isolation_profile_id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SmartIsolation(ZscalerObject):
    """
    A class for SmartIsolation objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the SmartIsolation model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.plugin_check_frequency: Optional[Any] = config["pluginCheckFrequency"] \
                if "pluginCheckFrequency" in config else None
            self.bypass_plugins: List[Any] = ZscalerCollection.form_list(
                config["bypassPlugins"] if "bypassPlugins" in config else [], str
            )
            self.bypass_applications: List[Any] = ZscalerCollection.form_list(
                config["bypassApplications"] if "bypassApplications" in config else [], str
            )
            self.bypass_all_browsers: Optional[Any] = config["bypassAllBrowsers"] \
                if "bypassAllBrowsers" in config else None
            self.blocked_internet_explorer_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedInternetExplorerVersions"] if "blockedInternetExplorerVersions" in config else [], str
            )
            self.blocked_chrome_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedChromeVersions"] if "blockedChromeVersions" in config else [], str
            )
            self.blocked_firefox_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedFirefoxVersions"] if "blockedFirefoxVersions" in config else [], str
            )
            self.blocked_safari_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedSafariVersions"] if "blockedSafariVersions" in config else [], str
            )
            self.blocked_opera_versions: List[Any] = ZscalerCollection.form_list(
                config["blockedOperaVersions"] if "blockedOperaVersions" in config else [], str
            )
            self.allow_all_browsers: Optional[Any] = config["allowAllBrowsers"] \
                if "allowAllBrowsers" in config else None
            self.enable_warnings: Optional[Any] = config["enableWarnings"] \
                if "enableWarnings" in config else None
            self.enable_smart_browser_isolation: Optional[Any] = config["enableSmartBrowserIsolation"] \
                if "enableSmartBrowserIsolation" in config else None

            self.smart_isolation_groups = ZscalerCollection.form_list(config["smartIsolationGroups"] if "smartIsolationGroups" in config else [], user_management.Groups)

            self.smart_isolation_users = ZscalerCollection.form_list(
                config["smartIsolationUsers"] if "smartIsolationUsers" in config else [], user_management.UserManagement
            )

            if "smartIsolationProfile" in config:
                if isinstance(config["smartIsolationProfile"], cloud_browser_isolation.CBIProfile):
                    self.smart_isolation_profile: Optional[cloud_browser_isolation.CBIProfile] = config["smartIsolationProfile"]
                elif config["smartIsolationProfile"] is not None:
                    self.smart_isolation_profile = cloud_browser_isolation.CBIProfile(config["smartIsolationProfile"])
                else:
                    self.smart_isolation_profile = None
            else:
                self.smart_isolation_profile: Optional[SmartIsolationProfile] = None
            self.smart_isolation_profile_id: Optional[Any] = config["smartIsolationProfileId"] \
                if "smartIsolationProfileId" in config else None
        else:
            self.plugin_check_frequency: Optional[Any] = None
            self.bypass_plugins: List[Any] = []
            self.bypass_applications: List[Any] = []
            self.bypass_all_browsers: Optional[Any] = None
            self.blocked_internet_explorer_versions: List[Any] = []
            self.blocked_chrome_versions: List[Any] = []
            self.blocked_firefox_versions: List[Any] = []
            self.blocked_safari_versions: List[Any] = []
            self.blocked_opera_versions: List[Any] = []
            self.allow_all_browsers: Optional[Any] = None
            self.enable_warnings: Optional[Any] = None
            self.enable_smart_browser_isolation: Optional[Any] = None
            self.smart_isolation_users: List[SmartIsolationUser] = []
            self.smart_isolation_groups: List[SmartIsolationGroup] = []
            self.smart_isolation_profile: Optional[SmartIsolationProfile] = None
            self.smart_isolation_profile_id: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "pluginCheckFrequency": self.plugin_check_frequency,
            "bypassPlugins": self.bypass_plugins,
            "bypassApplications": self.bypass_applications,
            "bypassAllBrowsers": self.bypass_all_browsers,
            "blockedInternetExplorerVersions": self.blocked_internet_explorer_versions,
            "blockedChromeVersions": self.blocked_chrome_versions,
            "blockedFirefoxVersions": self.blocked_firefox_versions,
            "blockedSafariVersions": self.blocked_safari_versions,
            "blockedOperaVersions": self.blocked_opera_versions,
            "allowAllBrowsers": self.allow_all_browsers,
            "enableWarnings": self.enable_warnings,
            "enableSmartBrowserIsolation": self.enable_smart_browser_isolation,
            "smartIsolationUsers": self.smart_isolation_users,
            "smartIsolationGroups": self.smart_isolation_groups,
            "smartIsolationProfile": self.smart_isolation_profile,
            "smartIsolationProfileId": self.smart_isolation_profile_id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SupportedBrowserVersions(ZscalerObject):
    """
    A class for SupportedBrowserVersions objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the SupportedBrowserVersions model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.browser_type: Optional[Any] = config["browserType"] \
                if "browserType" in config else None
            self.versions: List[Any] = ZscalerCollection.form_list(
                config["versions"] if "versions" in config else [], str
            )
            self.older_versions: List[Any] = ZscalerCollection.form_list(
                config["olderVersions"] if "olderVersions" in config else [], str
            )
        else:
            self.browser_type: Optional[Any] = None
            self.versions: List[Any] = []
            self.older_versions: List[Any] = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "browserType": self.browser_type,
            "versions": self.versions,
            "olderVersions": self.older_versions
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
