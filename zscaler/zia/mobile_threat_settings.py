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
from zscaler.zia.models.mobile_threat_settings import MobileAdvancedThreatSettings
from zscaler.utils import format_url


class MobileAdvancedSettingsAPI(APIClient):
    """
    A Client object for the Mobile Advanced Settings resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_mobile_advanced_settings(self) -> tuple:
        """
        Retrieves all the rules in the Mobile Malware Protection policy

        This method makes a GET request to the ZIA Admin API and returns detailed mobile settings,
        including various bypass rules, DNS optimization configurations, and traffic control settings.

        Returns:
            tuple: A tuple containing:
                - MobileAdvancedThreatSettings: The current mobile settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current mobile settings:

            >>> settings, _, err = client.zia.mobile_threat_settings.get_mobile_advanced_settings()
            >>> if err:
            ...     print(f"Error fetching mobile settings: {err}")
            ...     return
            ... print("Current mobile settings fetched successfully.")
            ... print(settings)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /mobileAdvanceThreatSettings
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = MobileAdvancedThreatSettings(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_mobile_advanced_settings(self, **kwargs) -> tuple:
        """
        Updates mobile settings in the ZIA Admin Portal with the provided configuration.

        Args:
            settings (:obj:`MobileAdvancedThreatSettings`):
                An instance of `MobileAdvancedThreatSettings` containing the updated configuration.

            Supported attributes:
                - block_apps_with_malicious_activity (bool): Blocks malicious or hidden applications
                - block_apps_with_known_vulnerabilities (bool): Block app with known vulnerabilities or insecure modules
                - block_apps_sending_unencrypted_user_credentials (bool): Block app leaking user credentials unencrypted
                - block_apps_sending_location_info (bool): Block app leaking device location unencrypted for unknown purpose
                - block_apps_sending_personally_identifiable_info (bool): Block app leaking PII unencrypted for unknown purpose
                - block_apps_sending_device_identifier (bool): Block app leaking device IDs unencrypted or for unknown purposes
                - block_apps_communicating_with_ad_websites (bool): Block app communicating with known ad websites
                - block_apps_communicating_with_remote_unknown_servers (bool): Block app talking to unknown remote servers

        Returns:
            tuple:
                - **MobileAdvancedThreatSettings**: The updated advanced settings object.
                - **Response**: The raw HTTP response returned by the API.
                - **error**: An error message if the update failed; otherwise, `None`.

        Examples:
            Update mobile setting options:

            >>> malware_settings, _, err = client.zia.mobile_threat_settings.update_mobile_advanced_settings(
            ...     block_apps_with_malicious_activity = True,
            ...     block_apps_with_known_vulnerabilities = True,
            ...     block_apps_sending_unencrypted_user_credentials = True,
            ...     block_apps_sending_location_info = True,
            ...     block_apps_sending_personally_identifiable_info = True,
            ...     block_apps_sending_device_identifier = True,
            ...     block_apps_communicating_with_ad_websites = True,
            ...     block_apps_communicating_with_remote_unknown_servers = True
            ... )
            >>> if err:
            ...     print(f"Error fetching malware settings: {err}")
            ...     return
            ... print("Current malware settings fetched successfully.")
            ... print(malware_settings)
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /mobileAdvanceThreatSettings
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, MobileAdvancedThreatSettings)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = MobileAdvancedThreatSettings(self.form_response_body(response.get_body()))
            else:
                result = MobileAdvancedThreatSettings()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
