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
from zscaler.zia.models.activation import EusaStatus
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

    def get_eusa_status(self) -> tuple:
        """
        Retrieves the End User Subscription Agreement (EUSA) acceptance status.
        If the status does not exist, it returns a status object with no ID.

        Args:
            N/A

        Returns:
            tuple: A tuple containing (Eusa status instance, Response, error).

        Examples:
            Print latest Eusa status

            >>> fetched_eusa, _, error = client.zia.activate.get_eusa_status()
            >>> if error:
            ...     print(f"Error fetching Eusa status: {error}")
            ...     return
            ... print(f"Fetched Eusa status by ID: {fetched_eusa.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /eusaStatus/latest
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EusaStatus)
        if error:
            return (None, response, error)

        try:
            result = EusaStatus(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_eusa_status(self, status_id: int, **kwargs) -> tuple:
        """
        Updates the EUSA status based on the specified status ID

        Args:
            status_id (int): The unique ID for the EUSA status.

            version (dict): Specifies the EUSA info ID version.
                This field is for Zscaler internal use only.

            acceptedStatus (bool): A Boolean value that specifies the EUSA status.
                If set to true, the EUSA is accepted.
                If set to false, the EUSA is in an 'agreement pending' state.

        Returns:
            tuple: A tuple containing the updated EUSA status, response, and error.

        Examples:
            Update an existing EUSA status :

            >>> updated_eusa_status, _, error = client.zia.activate.update_eusa_status(
            ... status_id='1524566'
            ... )
            >>> if error:
            ...     print(f"Error updating EUSA status: {error}")
            ...     return
            ... print(f"EUSA status updated successfully: {updated_eusa_status.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /eusaStatus/{status_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EusaStatus)
        if error:
            return (None, response, error)

        try:
            result = EusaStatus(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
