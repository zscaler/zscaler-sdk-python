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

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.browser_control_settings import BrowserControlSettings
from zscaler.utils import format_url, transform_common_id_fields, reformat_params


class BrowserControlSettingsPI(APIClient):
    """
    A Client object for the Browser Control Settings resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_browser_control_settings(self) -> tuple:
        """
        Retrieves the Browser Control status and the list of configured browsers in the Browser Control policy

        Returns:
            tuple: A tuple containing:
                - BrowserControlSettings: The current browser control settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current browser control settings:

            >>> settings, _, err = client.zia.browser_control_settings.get_browser_control_settings()
            >>> if err:
            ...     print(f"Error fetching browser control settings: {err}")
            ...     return
            ... print("Current browser control settings fetched successfully.")
            ... print(settings)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /browserControlSettings
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = BrowserControlSettings(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_browser_control_settings(self, **kwargs) -> tuple:
        """
        Updates the Browser Control Settings.

        Args:
            settings (:obj:`BrowserControlSettings`):
                An instance of `BrowserControlSettings` containing the updated configuration.

        Supported attributes:
            - plugin_check_frequency (str):
                Specifies how frequently the service checks browsers and relevant applications to warn
                users regarding outdated or vulnerable browsers, plugins, and applications. If not set,
                the warnings are disabled

                Supported Values: `DAILY`, `WEEKLY`, `MONTHLY`, `EVERY_2_HOURS`, `EVERY_4_HOURS`,
                `EVERY_6_HOURS`, `EVERY_8_HOURS`, `EVERY_12_HOURS`

            - bypass_plugins (list[str]): List of plugins that need to be bypassed for warnings.

                Supported Values: `ANY`, `NONE`, `ACROBAT`, `FLASH`, `SHOCKWAVE`, `QUICKTIME`,
                `DIVX`, `GOOGLEGEARS`, `DOTNET`, `SILVERLIGHT`, `REALPLAYER`, `JAVA`, `TOTEM`, `WMP`

            - bypass_applications (list[str]): List of applications that need to be bypassed for warnings.
                Supported Values: `ANY`, `NONE`, `OUTLOOKEXP`, `MSOFFICE`

            - bypass_all_browsers (bool): If set to true, all the browsers are bypassed for warnings.

            - blocked_internet_explorer_versions (list[str]): Versions of Microsoft browser that need to be
                blocked. If not set, all Microsoft browser versions are allowed.

                See the `Browser Control API reference:
                <https://help.zscaler.com/zia/browser-control-policy#/browserControlSettings-get>`_
                for the supported values.

            - blocked_chrome_versions (list[str]): Versions of Google Chrome browser that need to be blocked.
                If not set, all Google Chrome versions are allowed.
                See the `Browser Control API reference:
                <https://help.zscaler.com/zia/browser-control-policy#/browserControlSettings-get>`_
                for the supported values.

            - blocked_firefox_versions (list[str]): Versions of Mozilla Firefox browser that need to be blocked.
                If not set, all Mozilla Firefox versions are allowed.
                See the `Browser Control API reference:
                <https://help.zscaler.com/zia/browser-control-policy#/browserControlSettings-get>`_
                for the supported values.

            - blocked_safari_versions (list[str]): Versions of Apple Safari browser that need to be blocked.
                If not set, all Apple Safari versions are allowed.
                See the `Browser Control API reference:
                <https://help.zscaler.com/zia/browser-control-policy#/browserControlSettings-get>`_
                for the supported values.

            - blocked_opera_versions (list[str]): Versions of Opera browser that need to be blocked. If not set,
                all Opera versions are allowed.
                See the `Browser Control API reference:
                <https://help.zscaler.com/zia/browser-control-policy#/browserControlSettings-get>`_
                for the supported values.

            - allow_all_browsers (bool): Specifies whether or not to allow all the browsers and their respective
                versions access to the internet
            - enable_warnings (bool): A Boolean value that specifies if the warnings are enabled
            - enable_smart_browser_isolation (bool): A Boolean value that specifies if Smart Browser Isolation is enabled
            - smart_isolation_users (list[int]): List of users for which the rule is applied
            - smart_isolation_groups (list[int]): List of groups for which the rule is applied
            - smart_isolation_profile_id (int): The isolation profile ID

        Returns:
            tuple:
                - **BrowserControlSettings**: The updated browser control setting object.
                - **Response**: The raw HTTP response returned by the API.
                - **error**: An error message if the update failed; otherwise, `None`.

        Examples:
            Update browser control setting options:

            >>> browser_settings, _, err = client.zia.browser_control_settings.update_browser_control_settings(
            ...     plugin_check_frequency = 'DAILY',
            ...     bypass_plugins = ['ACROBAT', 'FLASH', 'SHOCKWAVE'],
            ...     bypass_applications = ['OUTLOOKEXP', 'MSOFFICE'],
            ...     blocked_internet_explorer_versions = ['IE10', 'MSE81', 'MSE92'],
            ...     blocked_chrome_versions = ['CH143', 'CH142'],
            ...     blocked_firefox_versions = ['MF145', 'MF144'],
            ...     blocked_safari_versions = ['AS19', 'AS18'],
            ...     blocked_opera_versions = ['O129X', 'O130X'],
            ...     bypass_all_browsers = True,
            ...     allow_all_browsers = True,
            ...     enable_warnings = True,
            ... )
            >>> if err:
            ...     print(f"Error fetching browser settings: {err}")
            ...     return
            ... print("Current browser settings fetched successfully.")
            ... print(browser_settings)

            Enable Smart Browser Isolation:

            >>> browser_settings, _, err = client.zia.browser_control_settings.update_browser_control_settings(
            ...     plugin_check_frequency = 'DAILY',
            ...     bypass_plugins = ['ACROBAT', 'FLASH', 'SHOCKWAVE'],
            ...     bypass_applications = ['OUTLOOKEXP', 'MSOFFICE'],
            ...     blocked_internet_explorer_versions = ['IE10', 'MSE81', 'MSE92'],
            ...     blocked_chrome_versions = ['CH143', 'CH142'],
            ...     blocked_firefox_versions = ['MF145', 'MF144'],
            ...     blocked_safari_versions = ['AS19', 'AS18'],
            ...     blocked_opera_versions = ['O129X', 'O130X'],
            ...     bypass_all_browsers = True,
            ...     allow_all_browsers = True,
            ...     enable_warnings = True,
            ...     enable_smart_browser_isolation = True,
            ...     smart_isolation_users = [5452145],
            ...     smart_isolation_groups = [21568541],
            ...     smart_isolation_profile = {
            ...         "id": "161d0907-0a57-4aab-98c2-eccbd651c448"
            ...     },
            ... )
            >>> if err:
            ...     print(f"Error fetching browser settings: {err}")
            ...     return
            ... print("Current browser settings fetched successfully.")
            ... print(browser_settings)
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /browserControlSettings
            """
        )

        body = kwargs

        transform_common_id_fields(reformat_params, body, body)

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
