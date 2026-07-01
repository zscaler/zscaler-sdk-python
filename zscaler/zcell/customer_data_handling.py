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
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zcell.models.customer_data_handling import CustomerDataHandling
from zscaler.zcell.models.sim_location_groups import ResponseMessage


class CustomerDataHandlingAPI(APIClient):

    _zcell_base_endpoint_customer = "/zcell/config/api/v1/customers"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_customer_data_handling(self, id: str) -> APIResult[CustomerDataHandling]:
        """
        Gets the customer data from the DB for the logged-in customer.

        Args:
            id (str): Path parameter.
        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.customer_data_handling.get_customer_data_handling(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}")
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CustomerDataHandling)
        if error:
            return (None, response, error)
        try:
            result = CustomerDataHandling(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_customer_data_handling(self, id: str, **kwargs) -> APIResult[ResponseMessage]:
        """
        Activate end customer.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.customer_data_handling.update_customer_data_handling(
            ...     id='...',
            ...     name='example',
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "put".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ResponseMessage)
        if error:
            return (None, response, error)
        try:
            result = ResponseMessage(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
