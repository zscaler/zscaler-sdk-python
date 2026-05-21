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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url, reformat_params, transform_common_id_fields
from zscaler.zia.models.secure_browsing import BrowserControlSettings, SmartIsolation, SupportedBrowserVersions


class SecureBrowsingAPI(APIClient):
    """
    A Client object for the Secure Browsing resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_browser_control_settings(self) -> APIResult[dict]:
        """
        Retrieves the Browser Control status and the list of configured browsers in the Browser Control policy.

        Returns:
            tuple: A tuple containing:
                - BrowserControlSettings: The current Browser Control settings object. Exposes
                  ``plugin_check_frequency``, ``bypass_plugins``, ``bypass_applications``,
                  ``bypass_all_browsers``, ``blocked_internet_explorer_versions``,
                  ``blocked_chrome_versions``, ``blocked_firefox_versions``, ``blocked_safari_versions``,
                  ``blocked_opera_versions``, ``allow_all_browsers``, ``enable_warnings``,
                  ``enable_smart_browser_isolation``, ``smart_isolation_profile`` and
                  ``smart_isolation_profile_id``.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, ``None``.

        Examples:
            Retrieve and inspect the current Browser Control settings:

            >>> settings, response, err = client.zia.secure_browsing.get_browser_control_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Plugin check frequency: {settings.plugin_check_frequency}")
            ...     print(f"Warnings enabled: {settings.enable_warnings}")
            ...     print(f"Smart Browser Isolation: {settings.enable_smart_browser_isolation}")
            ...     print(f"Blocked Chrome versions: {settings.blocked_chrome_versions}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /browserControlSettings
        """)

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            browser_control_settings = BrowserControlSettings(response.get_body())
            return (browser_control_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_browser_control_settings(self, **kwargs) -> APIResult[dict]:
        """
        Updates the Browser Control settings. To learn more, see `Configuring the Browser Control Policy
        <https://help.zscaler.com/zia/configuring-browser-control-policy>`_.

        Keyword Args:
            plugin_check_frequency (str): How frequently the service checks browsers and relevant applications
                to warn users about outdated or vulnerable browsers, plugins, and applications. If not set,
                the warnings are disabled. Supported values: ``DAILY``, ``WEEKLY``, ``MONTHLY``,
                ``EVERY_2_HOURS``, ``EVERY_4_HOURS``, ``EVERY_6_HOURS``, ``EVERY_8_HOURS``, ``EVERY_12_HOURS``.
            bypass_plugins (list[str]): Plugins to bypass for warnings. Only has effect when
                ``enable_warnings=True``. If not set, all vulnerable plugins are warned. Supported values:
                ``ANY``, ``NONE``, ``ACROBAT``, ``FLASH``, ``SHOCKWAVE``, ``QUICKTIME``, ``DIVX``,
                ``GOOGLEGEARS``, ``DOTNET``, ``SILVERLIGHT``, ``REALPLAYER``, ``JAVA``, ``TOTEM``, ``WMP``.
            bypass_applications (list[str]): Applications to bypass for warnings. Only has effect when
                ``enable_warnings=True``. If not set, all vulnerable applications are warned. Supported values:
                ``ANY``, ``NONE``, ``OUTLOOKEXP``, ``MSOFFICE``.
            bypass_all_browsers (bool): If ``True``, all browsers are bypassed for warnings. Only has effect
                when ``enable_warnings=True``. If not set, all vulnerable browsers are warned.
            blocked_internet_explorer_versions (list[str]): Versions of Microsoft browsers to block. If not
                set, all Microsoft browser versions are allowed. Supported values include ``ANY``, ``NONE``,
                ``IE5``..``IE11``, and ``MSE12``..``MSE145``.
            blocked_chrome_versions (list[str]): Versions of Google Chrome to block. If not set, all Chrome
                versions are allowed. Supported values include ``ANY``, ``NONE``, ``CH0``..``CH143``.
            blocked_firefox_versions (list[str]): Versions of Mozilla Firefox to block. If not set, all
                Firefox versions are allowed. Supported values include ``ANY``, ``NONE``, ``MF1``..``MF145``.
            blocked_safari_versions (list[str]): Versions of Apple Safari to block. If not set, all Safari
                versions are allowed. Supported values include ``ANY``, ``NONE``, ``AS1``..``AS19``.
            blocked_opera_versions (list[str]): Versions of Opera to block. If not set, all Opera versions
                are allowed. Supported values include ``ANY``, ``NONE``, ``O85``, ``O9``,
                ``O39X``..``O130X``.
            allow_all_browsers (bool): Whether to allow all browsers and their respective versions access
                to the internet.
            enable_warnings (bool): Whether the browser-control warnings are enabled.
            enable_smart_browser_isolation (bool): Whether Smart Browser Isolation is enabled.
            smart_isolation_profile (dict): The isolation profile. Contains ``id`` (UUID), ``name``, ``url``
                and ``default_profile``. See `Creating Isolation Profiles for ZIA
                <https://help.zscaler.com/zia/creating-isolation-profiles-zia>`_.
            smart_isolation_profile_id (int): The isolation profile ID.

        Returns:
            tuple: A tuple containing:
                - BrowserControlSettings: The updated Browser Control settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the update failed; otherwise, ``None``.

        Examples:
            Enable warnings, set a daily check frequency, and block specific Chrome / Firefox versions:

            >>> updated, response, err = client.zia.secure_browsing.update_browser_control_settings(
            ...     enable_warnings=True,
            ...     plugin_check_frequency="DAILY",
            ...     bypass_plugins=["FLASH", "JAVA"],
            ...     bypass_applications=["MSOFFICE"],
            ...     blocked_chrome_versions=["CH100", "CH101"],
            ...     blocked_firefox_versions=["MF100"],
            ...     allow_all_browsers=False,
            ... )
            >>> if err:
            ...     print(f"Failed to update Browser Control settings: {err}")
            ... else:
            ...     print(f"Warnings enabled: {updated.enable_warnings}")
            ...     print(f"Plugin check frequency: {updated.plugin_check_frequency}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /browserControlSettings
            """)

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BrowserControlSettings)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = BrowserControlSettings(self.form_response_body(response.get_body()))
            else:
                result = BrowserControlSettings()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_supported_browser_versions(self) -> APIResult[List[SupportedBrowserVersions]]:
        """
        Retrieves a list of all supported browsers and their versions. To learn more, see `Configuring the
        Browser Control Policy <https://help.zscaler.com/zia/configuring-browser-control-policy>`_.

        The API returns one entry per browser type (``OPERA``, ``FIREFOX``, ``CHROME``, ``SAFARI``,
        ``MSCHREDGE``, etc.), each wrapped as a :class:`SupportedBrowserVersions` instance.

        Returns:
            tuple: A tuple containing:
                - list[SupportedBrowserVersions]: One entry per browser type. Each entry exposes:

                    - ``browser_type`` (str): The browser type. One of ``OPERA``, ``FIREFOX``, ``MSIE``,
                      ``MSEDGE``, ``CHROME``, ``SAFARI``, ``OTHER``, ``MSCHREDGE``. Read-only.
                    - ``versions`` (list[str]): The current versions of the browser.
                    - ``older_versions`` (list[str]): Earlier versions of the browser.

                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, ``None``.

        Examples:
            Retrieve and print every supported browser with its current and older versions:

            >>> browsers, _, error = client.zia.secure_browsing.get_supported_browser_versions()
            >>> if error:
            ...     print(f"Error fetching supported browser versions: {error}")
            ...     return
            >>> for browser in browsers:
            ...     print(f"Browser: {browser.browser_type}")
            ...     print(f"  Current versions: {browser.versions}")
            ...     print(f"  Older versions:   {browser.older_versions}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /browserControlSettings/supportedBrowserVersions
        """)

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(SupportedBrowserVersions(self.form_response_body(item)))
        except Exception as ex:
            return (None, response, ex)

        return (result, response, None)

    def update_smart_isolation(self, **kwargs) -> APIResult[dict]:
        """
        Updates the Smart Browser Isolation policy settings. To learn more, see `Configuring Smart Browser
        Isolation Policy <https://help.zscaler.com/zia/configuring-smart-browser-isolation-policy>`_.

        The PUT body uses the same Browser Control settings model as ``update_browser_control_settings``,
        with the addition of ``smart_isolation_users`` and ``smart_isolation_groups`` (user / group scoping
        for the Smart Browser Isolation rule).

        Keyword Args:
            plugin_check_frequency (str): How frequently the service checks browsers and relevant applications
                to warn users about outdated or vulnerable browsers, plugins, and applications. If not set,
                the warnings are disabled. Supported values: ``DAILY``, ``WEEKLY``, ``MONTHLY``,
                ``EVERY_2_HOURS``, ``EVERY_4_HOURS``, ``EVERY_6_HOURS``, ``EVERY_8_HOURS``, ``EVERY_12_HOURS``.
            bypass_plugins (list[str]): Plugins to bypass for warnings. Only has effect when
                ``enable_warnings=True``. If not set, all vulnerable plugins are warned. Supported values:
                ``ANY``, ``NONE``, ``ACROBAT``, ``FLASH``, ``SHOCKWAVE``, ``QUICKTIME``, ``DIVX``,
                ``GOOGLEGEARS``, ``DOTNET``, ``SILVERLIGHT``, ``REALPLAYER``, ``JAVA``, ``TOTEM``, ``WMP``.
            bypass_applications (list[str]): Applications to bypass for warnings. Only has effect when
                ``enable_warnings=True``. If not set, all vulnerable applications are warned. Supported values:
                ``ANY``, ``NONE``, ``OUTLOOKEXP``, ``MSOFFICE``.
            bypass_all_browsers (bool): If ``True``, all browsers are bypassed for warnings. Only has effect
                when ``enable_warnings=True``. If not set, all vulnerable browsers are warned.
            blocked_internet_explorer_versions (list[str]): Versions of Microsoft browsers to block. If not
                set, all Microsoft browser versions are allowed. Supported values include ``ANY``, ``NONE``,
                ``IE5``..``IE11``, and ``MSE12``..``MSE145``.
            blocked_chrome_versions (list[str]): Versions of Google Chrome to block. If not set, all Chrome
                versions are allowed. Supported values include ``ANY``, ``NONE``, ``CH0``..``CH143``.
            blocked_firefox_versions (list[str]): Versions of Mozilla Firefox to block. If not set, all
                Firefox versions are allowed. Supported values include ``ANY``, ``NONE``, ``MF1``..``MF145``.
            blocked_safari_versions (list[str]): Versions of Apple Safari to block. If not set, all Safari
                versions are allowed. Supported values include ``ANY``, ``NONE``, ``AS1``..``AS19``.
            blocked_opera_versions (list[str]): Versions of Opera to block. If not set, all Opera versions
                are allowed. Supported values include ``ANY``, ``NONE``, ``O85``, ``O9``,
                ``O39X``..``O130X``.
            allow_all_browsers (bool): Whether to allow all browsers and their respective versions access
                to the internet.
            enable_warnings (bool): Whether the browser-control warnings are enabled.
            enable_smart_browser_isolation (bool): Whether Smart Browser Isolation is enabled.
            smart_isolation_users_ids (list[str]): IDs of users for which the rule is applied.
            smart_isolation_groups_ids (list[str]): IDs of groups for which the rule is applied.
            smart_isolation_profile (dict): The isolation profile. Contains ``id`` (UUID), ``name``, ``url``
                and ``default_profile``. See `Creating Isolation Profiles for ZIA
                <https://help.zscaler.com/zia/creating-isolation-profiles-zia>`_.
            smart_isolation_profile_id (int): The isolation profile ID.

        Returns:
            tuple: A tuple containing:
                - SmartIsolation: The updated Smart Browser Isolation policy settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the update failed; otherwise, ``None``.

        Examples:
            Enable Smart Browser Isolation for a set of users and groups using a specific isolation profile:

            >>> updated, response, err = client.zia.secure_browsing.update_smart_isolation(
            ...     enable_smart_browser_isolation=True,
            ...     smart_isolation_users_ids=[12345, 67890],
            ...     smart_isolation_groups_ids=[24680, 24681],
            ...     smart_isolation_profile={
            ...         "id": "161d0907-0a57-4aab-98c2-eccbd651c448",
            ...         "name": "Profile1_ZIA",
            ...         "url": "https://redirect.isolation-beta.zscaler.com/tenant/support/profile/161d0907-0a57-4aab-98c2-eccbd651c448"
            ...     }
            ... )
            >>> if err:
            ...     print(f"Error updating smart isolation: {err}")
            ...     return
            ... print("Current smart isolation updated successfully.")
            ... print(updated)
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /browserControlSettings/smartIsolation
            """)

        body = {}
        body.update(kwargs)

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SmartIsolation)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = SmartIsolation(self.form_response_body(response.get_body()))
            else:
                result = SmartIsolation()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
