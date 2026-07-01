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
from zscaler.zpa.models.business_continuity import BusinessContinuity


class BusinessContinuityAPI(APIClient):

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_business_continuity_settings(self, query_params=None) -> APIResult[List[BusinessContinuity]]:
        """
        List business_continuity_settings.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of BusinessContinuity instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings
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
                result.append(BusinessContinuity(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_business_continuity_setting_certificate(self, query_params=None) -> APIResult:
        """
        Returns the certificate for business_continuity_setting (raw response, no model).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/certificate
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
        return (response, response, None)

    def get_business_continuity_setting_metadata(self, query_params=None) -> APIResult:
        """
        Returns the metadata for business_continuity_setting (raw response, no model).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/metadata
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
        return (response, response, None)

    def get_business_continuity_setting(self, business_continuity_setting_id: str) -> APIResult[BusinessContinuity]:
        """
        Returns information for the specified business_continuity_setting.

        Args:
            business_continuity_setting_id (str): The unique identifier for the business_continuity_setting.

        Returns:
            tuple: The resource record for the business_continuity_setting.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/{business_continuity_setting_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BusinessContinuity)
        if error:
            return (None, response, error)
        try:
            result = BusinessContinuity(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_business_continuity_setting(self, **kwargs) -> APIResult[BusinessContinuity]:
        """
        Adds a new business_continuity_setting.

        Returns:
            tuple: The newly created business_continuity_setting resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BusinessContinuity)
        if error:
            return (None, response, error)
        try:
            result = BusinessContinuity(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_business_continuity_setting(
        self, business_continuity_setting_id: str, **kwargs
    ) -> APIResult[BusinessContinuity]:
        """
        Updates an existing business_continuity_setting.

        Args:
            business_continuity_setting_id (str): The unique ID for the business_continuity_setting being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated business_continuity_setting resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/{business_continuity_setting_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BusinessContinuity)
        if error:
            return (None, response, error)
        try:
            result = BusinessContinuity(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_business_continuity_setting(self, business_continuity_setting_id: str) -> APIResult[None]:
        """
        Deletes the specified business_continuity_setting.

        Args:
            business_continuity_setting_id (str): The unique identifier for the business_continuity_setting.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/{business_continuity_setting_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
