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


class AdminSSOControllerAPI(APIClient):
    """
    A Client object for the admin sso configuration controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}/v2"

    def get_sso_controller(self) -> tuple:
        """
        Fetches Admin SSO Login Details

        Args:
            N/A:

        Returns:
            :obj:`Tuple[dict, Response, Exception]`:
                A tuple containing:
                - A dictionary with the SSO setting (e.g., `{"ssologinonly": True}`) if the request succeeds,
                - The raw `Response` object,
                - Or an `Exception` if an error occurred.

        Examples:
            >>> fetched, _, err = client.zpa.admin_sso_controller.get_sso_controller()
            >>> if err:
            ...     print(f"Error fetching updated SSO setting: {err}")
            ...     return
            ... print(f"Current SSO login-only setting: {fetched['ssologinonly']}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /ssoLoginOptions
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_sso_controller(self, **kwargs) -> tuple:
        """
        Update SSO Options

        Args:
            ssologinonly (bool): Enable SSO Login Option

        Returns:
            :obj:`Tuple[dict, Response, Exception]`:
                A tuple containing:
                - An empty dictionary `{}` on success (due to 204 No Content),
                - The raw `Response` object,
                - Or an `Exception` if an error occurred.

                The dictionary is always empty since the API returns no response body.

        Example:

            Enable SSO Login Option

            >>> _, _, err = client.zpa.admin_sso_controller.update_sso_controller(
            ...     ssologinonly=True
            ... )
            >>> if err:
            ...     print(f"Error updating SSO login option: {err}")
            ...     return
            ... print("SSO login-only setting updated successfully.")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /ssoLoginOptions
        """
        )

        body = kwargs
        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error or response is None:
            return (None, response, error)

        if getattr(response, "status_code", None) == 204:
            return ({}, response, None)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
