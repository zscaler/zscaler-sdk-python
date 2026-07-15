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

    def __init__(self, request_executor: "RequestExecutor", config: dict = None) -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcell_customer_id = (config or {}).get("client", {}).get("zcellCustomerId")

    def get_customer_data_handling(self, id: str = None) -> APIResult[CustomerDataHandling]:
        """
        Gets the customer data from the DB for the logged-in customer.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
        Returns:
            tuple: (result, Response, error)

        Examples:
            Fetch the logged-in customer's data::

                >>> customer_data, _, err = client.zcell.customer_data_handling.get_customer_data_handling(
                ...     id='gi754cvqb07r0',
                ... )
                >>> if err:
                ...     print(f"Error fetching customer data: {err}")
                ...     return
                >>> print(f"Customer data fetched successfully: {customer_data.as_dict()}")
        """
        http_method = "get".upper()
        id = id or self._zcell_customer_id
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

    def update_customer_data_handling(self, id: str = None, **kwargs) -> APIResult[ResponseMessage]:
        """
        Activate end customer.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            **kwargs: Request body fields (all required).

                ``username`` (str): The activation username.

                ``password`` (str): The activation password.

                ``api_key`` (str): The activation API key.

        Returns:
            tuple: (result, Response, error)

        Examples:
            Activate an end customer::

                >>> result, _, error = client.zcell.customer_data_handling.update_customer_data_handling(
                ...     id='gi754cvqb07r0',
                ...     username='deploy@cellular-beta-two.zsloginbeta.net',
                ...     password='********',
                ...     api_key='********',
                ... )
                >>> if error:
                ...     print(f"Error activating customer: {error}")
                ...     return
                >>> print(f"Customer activated successfully: {result.as_dict()}")
        """
        http_method = "put".upper()
        id = id or self._zcell_customer_id
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

        # The API may return 204 No Content on success — there is no body to parse.
        if not response or not response.get_body():
            return (None, response, None)

        try:
            result = ResponseMessage(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
