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
from zscaler.utils import format_url, zcc_param_mapper
from zscaler.api_client import APIClient
from zscaler.zcc.models.secrets_otp import OtpResponse
from zscaler.zcc.models.secrets_passwords import Passwords


class SecretsAPI(APIClient):

    def __init__(self, request_executor):
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def get_otp(self, query_params=None) -> tuple:
        """
        Returns the OTP code for the specified device id.

        Args:
            query_params (dict): Query parameters for the request.
                - device_id (str): Optional alias for `udid`. If provided, it will be mapped automatically.
                - udid (str): The actual UDID expected by the API.

        Returns:
            tuple: (list of OtpResponse, response, error)

        Examples:
            >>> otps, _, err = client.zcc.secrets.get_otp(query_params={'device_id': 'd-29-9b-7c-c5-3f-d2-90-3c-d5-'})
            >>> if err:
            ...     print(f"Error retrieving one-time password (OTP): {err}")
            ...     return
            ... print("OTP:", otps.otp)
            ... print("Full response:", otps.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getOtp
        """
        )

        query_params = query_params or {}

        if "device_id" in query_params and "udid" not in query_params:
            query_params["udid"] = query_params.pop("device_id")

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(
            http_method, api_url, body, headers, params=query_params
        )

        if error:
            return None, None, error

        response, error = self._request_executor.execute(request, OtpResponse)
        if error:
            return None, response, error

        try:
            result = OtpResponse(self.form_response_body(response.get_body()))
            return result, response, None
        except Exception as error:
            return None, response, error

    @zcc_param_mapper
    def get_passwords(self, query_params=None) -> tuple:
        """
        Return passwords for the specified username and device OS type.

        Args:
            query_params (dict, optional): A dictionary containing supported filters.

                ``[query_params.os_type]`` {str}: Filter by device operating system type. Valid options are:
                    ios, android, windows, macos, linux.

                ``[query_params.username]`` {str}:  Filter by enrolled username for the device.

        Returns:
            tuple: (Passwords object, response, error)

        Example:
            >>> passwords, _, err = client.zcc.secrets.get_passwords(query_params={
            ...     "username": "jdoe@example.com",
            ...     "os_type": "windows"
            ... })
            >>> if err:
            ...     print("Error:", err)
            >>> else:
            ...     print(passwords.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getPasswords
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(
            http_method, api_url, params=query_params
        )

        if error:
            return None, None, error

        response, error = self._request_executor.execute(request)
        if error:
            return None, response, error

        try:
            result = Passwords(self.form_response_body(response.get_body()))
        except Exception as error:
            return None, response, error

        return result, response, None
