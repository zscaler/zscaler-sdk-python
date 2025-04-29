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
from zscaler.zia.models.ftp_control_policy import FTPControlPolicy
from zscaler.utils import format_url


class FTPControlPolicyAPI(APIClient):
    """
    A Client object for the FTP Control Settings resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_ftp_settings(self) -> tuple:
        """
        Retrieves the FTP Control status and the list of URL categories for which FTP is allowed.

        Returns:
            tuple: A tuple containing:
                - FTPControlPolicy: The current ftp control settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current mobile settings:

            >>> settings, _, err = client.zia.ftp_control_policy.get_ftp_settings()
            >>> if err:
            ...     print(f"Error fetching ftp control settings: {err}")
            ...     return
            ... print("Current ftp control settings fetched successfully.")
            ... print(settings)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ftpSettings
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = FTPControlPolicy(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_ftp_settings(self, **kwargs) -> tuple:
        """
        Updates the FTP Control settings.

        Args:
            settings (:obj:`FTPControlPolicy`):
                An instance of `FTPControlPolicy` containing the updated configuration.

        Supported attributes:
            - block_apps_with_malicious_activity (bool): Blocks malicious or hidden applications
            - block_apps_with_known_vulnerabilities (bool): Block apps with known vulnerabilities or insecure modules
            - block_apps_sending_unencrypted_user_credentials (bool): Block apps leaking user credentials unencrypted
            - block_apps_sending_location_info (bool): Block apps leaking device location unencrypted or for unknown purposes
            - block_apps_sending_personally_identifiable_info (bool): Block app leaking PII unencrypted or for unknown purposes
            - block_apps_sending_device_identifier (bool): Block apps leaking device IDs unencrypted or for unknown purposes
            - block_apps_communicating_with_ad_websites (bool): Block apps communicating with known ad websites
            - block_apps_communicating_with_remote_unknown_servers (bool): Block apps talking to unknown remote servers

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
            /ftpSettings
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, FTPControlPolicy)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = FTPControlPolicy(self.form_response_body(response.get_body()))
            else:
                result = FTPControlPolicy()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
