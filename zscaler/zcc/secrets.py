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

from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url, zcc_param_map
from zscaler.api_client import APIClient
from zscaler.zcc.models.secrets_otp import OtpResponse
from zscaler.zcc.models.secrets_passwords import Passwords


class SecretsAPI(APIClient):

    def __init__(self, request_executor):
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def get_otp(self, device_id: str):
        """
        Returns the OTP code for the specified device id.

        Args:
            device_id (str): The unique id for the enrolled device that the OTP will be obtained for.

        Returns:
            OtpResponse: An instance of OtpResponse containing the requested OTP code for the specified device id.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getOtp
        """
        )

        payload = {"udid": device_id}

        request, error = self._request_executor.create_request(http_method, api_url, params=payload)
        if error:
            return None, None, error

        response, error = self._request_executor.execute(request)
        if error:
            return None, response, error

        try:
            result = OtpResponse(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_passwords(self, username: str, os_type: str = "windows") -> tuple:
        """
        Return passwords for the specified username and device OS type.

        Args:
            username (str): The username that the device belongs to.
            os_type (str): The OS Type for the device, defaults to `windows`. Valid options are:

                - ios
                - android
                - windows
                - macos
                - linux

        Returns:
            Passwords: An instance of Passwords containing passwords for the specified username's device.
        """
        # Simplify the os_type argument, raise an error if the user supplies the wrong one.
        os_type = zcc_param_map["os"].get(os_type, None)
        if not os_type:
            raise ValueError("Invalid os_type specified. Check the pyZscaler documentation for valid os_type options.")

        params = {
            "username": username,
            "osType": os_type,
        }

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getPasswords
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return None, None, error

        response, error = self._request_executor.execute(request)
        if error:
            return None, response, error

        try:
            result = Passwords(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
