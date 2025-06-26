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
from zscaler.zia.models import common as common
from zscaler.zia.models import common as common_reference


class BrowserControlSettings(ZscalerObject):
    """
    A class for BrowserControlSettings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the BrowserControlSettings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.plugin_check_frequency = config["pluginCheckFrequency"] \
                if "pluginCheckFrequency" in config else None

            self.bypass_all_browsers = config["bypassAllBrowsers"] \
                if "bypassAllBrowsers" in config else None

            self.allow_all_browsers = config["allowAllBrowsers"] \
                if "allowAllBrowsers" in config else None

            self.enable_warnings = config["enableWarnings"] \
                if "enableWarnings" in config else None

            self.enable_smart_browser_isolation = config["enableSmartBrowserIsolation"] \
                if "enableSmartBrowserIsolation" in config else None

            self.smart_isolation_profile_id = config["smartIsolationProfileId"] \
                if "smartIsolationProfileId" in config else None

            self.bypass_plugins = ZscalerCollection.form_list(
                config["bypassPlugins"] if "bypassPlugins" in config else [], str
            )

            self.bypass_applications = ZscalerCollection.form_list(
                config["bypassApplications"] if "bypassApplications" in config else [], str
            )

            self.blocked_internet_explorer_versions = ZscalerCollection.form_list(
                config["blockedInternetExplorerVersions"] if "blockedInternetExplorerVersions" in config else [], str
            )
            self.blocked_chrome_versions = ZscalerCollection.form_list(
                config["blockedChromeVersions"] if "blockedChromeVersions" in config else [], str
            )
            self.blocked_firefox_versions = ZscalerCollection.form_list(
                config["blockedFirefoxVersions"] if "blockedFirefoxVersions" in config else [], str
            )
            self.blocked_safari_versions = ZscalerCollection.form_list(
                config["blockedSafariVersions"] if "blockedSafariVersions" in config else [], str
            )
            self.blocked_opera_versions = ZscalerCollection.form_list(
                config["blockedOperaVersions"] if "blockedOperaVersions" in config else [], str
            )

            self.smart_isolation_users = ZscalerCollection.form_list(
                config["smartIsolationUsers"] if "smartIsolationUsers" in config else [], common_reference.ResourceReference
            )

            self.smart_isolation_groups = ZscalerCollection.form_list(
                config["smartIsolationGroups"] if "smartIsolationGroups" in config else [], common_reference.ResourceReference
            )
            if "smartIsolationProfile" in config:
                if isinstance(config["smartIsolationProfile"], common.CommonBlocks):
                    self.smart_isolation_profile = config["smartIsolationProfile"]
                elif config["smartIsolationProfile"] is not None:
                    self.smart_isolation_profile = common.CommonBlocks(config["smartIsolationProfile"])
                else:
                    self.smart_isolation_profile = None
            else:
                self.smart_isolation_profile = None
        else:
            self.bypass_plugins = ZscalerCollection.form_list([], str)
            self.bypass_applications = ZscalerCollection.form_list([], str)
            self.blocked_internet_explorer_versions = ZscalerCollection.form_list([], str)
            self.blocked_chrome_versions = ZscalerCollection.form_list([], str)
            self.blocked_firefox_versions = ZscalerCollection.form_list([], str)
            self.blocked_safari_versions = ZscalerCollection.form_list([], str)
            self.blocked_opera_versions = ZscalerCollection.form_list([], str)
            self.smart_isolation_users = []
            self.smart_isolation_groups = []
            self.plugin_check_frequency = None
            self.bypass_all_browsers = None
            self.allow_all_browsers = None
            self.enable_warnings = None
            self.enable_smart_browser_isolation = None
            self.smart_isolation_profile = None
            self.smart_isolation_profile_id = None

    def request_format(self):
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
