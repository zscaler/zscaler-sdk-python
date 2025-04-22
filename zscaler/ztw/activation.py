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
from zscaler.ztw.models.activation import Activation
from zscaler.utils import format_url


class ActivationAPI(APIClient):
    """
    A Client object for the Activation resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def activate(self, force: bool = False) -> tuple:
        """
        Activate the configuration.

        Args:
            force (bool): If set to True, forces the activation. Default is False.

        Returns:
            :obj:`Tuple`: The status code of the operation.

        Examples:
            Activate the configuration without forcing::

                ztw.config.activate()

            Forcefully activate the configuration::

                ztw.config.activate(force=True)

        """
        http_method = "put".upper()
        # Choose the endpoint based on the force parameter
        if force:
            endpoint_path = "/ecAdminActivateStatus/forcedActivate"
        else:
            endpoint_path = "/ecAdminActivateStatus/activate"

        api_url = format_url(f"{self._ztw_base_endpoint}{endpoint_path}")

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params={})
        if error:
            return (None, None, error)

        # Execute the request and parse the response using the Activation model
        response, error = self._request_executor.execute(request, Activation)
        if error:
            return (None, response, error)

        try:
            result = Activation(response.get_body())
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_status(self):
        """
        Get the status of the configuration.

        Returns:
            :obj:`Tuple`: The status of the configuration.

        Examples:
            Get the status of the configuration::

                print(ztw.config.get_status())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecAdminActivateStatus
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            activation = Activation(response.get_body())
            return (activation, response, None)
        except Exception as ex:
            return (None, response, ex)
