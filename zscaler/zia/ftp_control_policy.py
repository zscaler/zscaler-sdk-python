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
            - ftp_over_http_enabled (bool): Indicates whether to enable FTP over HTTP.
            - ftp_enabled (bool): Indicates whether to enable native FTP.
                When enabled, users can connect to native FTP sites and download files.
            - url_categories (list[str]): List of URL categories that allow FTP traffic
            - urls (list[str]): Domains or URLs included for the FTP Control settings

        Returns:
            tuple:
                - **FTPControlPolicy**: The updated ftp control policy object.
                - **Response**: The raw HTTP response returned by the API.
                - **error**: An error message if the update failed; otherwise, `None`.

        Examples:
            Update mobile setting options:

            >>> ftp_settings, _, err = client.zia.ftp_control_policy.update_ftp_settings(
            ...     ftp_over_http_enabled = True,
            ...     ftp_enabled = True,
            ...     url_categories = ["ADULT_THEMES", "ADULT_SEX_EDUCATION"],
            ...     urls = ["zscaler.com", "zscaler.net"],
            ... )
            >>> if err:
            ...     print(f"Error fetching ftp settings: {err}")
            ...     return
            ... print("Current ftp settings fetched successfully.")
            ... print(ftp_settings)
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
