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
from zscaler.zcc.models.manage_pass import ManagePassResponseContract
from zscaler.utils import format_url


class ManagePassAPI(APIClient):

    def __init__(self, request_executor):
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def update_manage_pass(self, manage_pass):
        """
        Updates the manage pass settings.

        Args:
            manage_pass (dict): A dictionary containing manage pass settings.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /managePass
        """
        )

        # Ensure app_segment is a dictionary
        if isinstance(manage_pass, dict):
            body = manage_pass
        else:
            body = manage_pass.as_dict()

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return None, None, error

        response, error = self._request_executor.execute(request)
        if error:
            return None, response, error

        try:
            result = ManagePassResponseContract(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
