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
from zscaler.zia.models.remoteassistance import RemoteAssistance
from zscaler.utils import format_url


class RemoteAssistanceAPI(APIClient):
    """
    A Client object for the Remote Assistance resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_remote_assistance(self) -> tuple:
        """
        Retrieves information about the Remote Assistance option configured in the ZIA Admin Portal.
        Using this option, you can allow Zscaler Support to access your organization's ZIA Admin Portal
        for a specified time period to troubleshoot issues.

        Returns:
            tuple: A tuple containing:
                - RemoteAssistance: The current remote assistance settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current remote assistance settings:

            >>> settings, response, err = client.zia.remote_assistance.get_remote_assistance()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /remoteAssistance
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            remote_assistance = RemoteAssistance(response.get_body())
            return (remote_assistance, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_remote_assistance(self, **kwargs) -> tuple:
        """
        Retrieves information about the Remote Assistance option configured in the ZIA Admin Portal.

        Using this option, you can allow Zscaler Support to access your organization's ZIA Admin Portal
        for a specified time period to troubleshoot issues.

        Args:
            settings (:obj:`RemoteAssistance`):
                An instance of `RemoteAssistance` containing the updated configuration.

                Supported attributes:
                    - view_only_until (int): Unix timestamp until which view-only access is allowed
                    - full_access_until (int): Unix timestamp until which full access is allowed
                    - username_obfuscated (bool): Whether usernames for SSO users are obfuscated
                    - device_info_obfuscate (bool): Whether device info (hostname, name, owner) is hidden in UI

        Returns:
            tuple: A tuple containing:
                - RemoteAssistance: The updated remote assistance object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the update failed; otherwise, `None`.

        Examples:
            Update Remote Assistance by enabling Office365 and adjusting the session timeout:

            >>> settings, response, err = client.zia.remote_assistance.get_remote_assistance()
            >>> if not err:
            ...     settings.view_only_until = 78415241
            ...     settings.full_access_until = 78415242
            ...     settings.username_obfuscated = True
            ...     settings.device_info_obfuscate = True
            ...     updated_settings, response, err = client.zia.remote_assistance.update_remote_assistance(settings)
            ...     if not err:
            ...         print(f"Updated View Only Until: {updated_settings.view_only_until}")
            ...     else:
            ...         print(f"Failed to update remote assistance settings: {err}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /remoteAssistance
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RemoteAssistance)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = RemoteAssistance(self.form_response_body(response.get_body()))
            else:
                result = RemoteAssistance()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
