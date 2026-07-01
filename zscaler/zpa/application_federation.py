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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zpa.models.application_federation import ApplicationFederation


class ApplicationFederationAPI(APIClient):

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/customers/{customer_id}"

    def list_applications_host(self, query_params=None) -> APIResult[List[ApplicationFederation]]:
        """
        List applications (host).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of ApplicationFederation instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /application/host
        """)

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            result = []
            for item in response.get_results():
                result.append(ApplicationFederation(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_application(self, application_id: str, **kwargs) -> APIResult[ApplicationFederation]:
        """
        Updates an existing application.

        Args:
            application_id (str): The unique ID for the application being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated application resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /application/{application_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationFederation)
        if error:
            return (None, response, error)
        try:
            result = ApplicationFederation(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
