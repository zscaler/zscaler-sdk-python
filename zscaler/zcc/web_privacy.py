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
from zscaler.utils import format_url
from zscaler.zcc.models.webprivacy import WebPrivacy


class WebPrivacyAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def get_web_privacy(self) -> tuple:
        """
        Returns Web Privacy Information from the Client Connector Portal.

        Args:
            N/A

        Returns:
            :obj:`list`: Returns Web Privacy Information in the Client Connector Portal.

        Examples:
            Prints Web Privacy Information in the Client Connector Portal to the console:

            >>> web_privacy_info = client.zcc.web_privacy.get_web_privacy()
            ...    print(web_privacy_info)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getWebPrivacyInfo
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return None

        response, error = self._request_executor.execute(request)
        if error:
            return None

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return None

        return result

    def set_web_privacy_info(self, **kwargs) -> tuple:
        """
        Adds or updates the configuration information for end user and device-related PII.

        Args:
            id (str):
            active (str):
            collect_machine_hostname (str):
            collect_user_info (str):
            collect_zdx_location (str):
            disable_crashlytics (str):
            enable_packet_capture (str):
            export_logs_for_non_admin (str):
            grant_access_to_zscaler_log_folder (str):
            override_t2_protocol_setting (str):
            restrict_remote_packet_capture (str):

        Returns:
            tuple: A tuple containing the updated Web Privacy Information, response, and error.

        Examples:
            updates the configuration information for end user and device-related PII:

            >>> private_info, _, error = client.zcc.web_privacy.set_web_privacy_info(
            ...     active='1',
            ...     collect_user_info='1',
            ...     collect_machine_hostname='1',
            ...     collect_zdx_location='1',
            ...     enable_packet_capture='1',
            ...     disable_crashlytics='1',
            ...     override_t2_protocol_setting='1',
            ...     restrict_remote_packet_capture='0',
            ...     grant_access_to_zscaler_log_folder='0',
            ...     export_logs_for_non_admin='1',
            ...     enable_auto_log_snippet='0'
            ... )
            >>> if error:
            ...     print(f"Error updating web privacy info: {error}")
            ...     return
            ... print(f"web Privacy Info updated successfully: {private_info.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /setWebPrivacyInfo
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WebPrivacy)
        if error:
            return (None, response, error)

        try:
            result = WebPrivacy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
