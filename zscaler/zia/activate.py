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
from zscaler.zia.models.activation import Activation
from zscaler.utils import format_url


class ActivationAPI(APIClient):
    """
    A Client object for the Activation resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def status(self) -> tuple:
        """
        Returns the activation status for a configuration change.

        Returns:
            :obj:`Activation`, response object, and error if any.

        Examples:
            >>> config_status, response, error = zia.config.status()
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /status
        """
        )

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params={})

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, Activation)

        if error:
            return (None, response, error)

        try:
            result = Activation(response.get_body())
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def activate(self) -> tuple:
        """
        Activates configuration changes.

        Returns:
            :obj:`Activation`, response object, and error if any.

        Examples:
            >>> config_activate, response, error = zia.activate.activate()
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /status/activate
        """
        )

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params={})

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, Activation)

        if error:
            return (None, response, error)

        try:
            result = Activation(response.get_body())
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
