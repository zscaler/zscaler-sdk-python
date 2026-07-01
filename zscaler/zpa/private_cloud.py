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
from zscaler.zpa.models.private_cloud import PrivateCloud


class PrivateCloudAPI(APIClient):

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_private_clouds(self, query_params=None) -> APIResult[List[PrivateCloud]]:
        """
        List private_clouds.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of PrivateCloud instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /privateCloud
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
                result.append(PrivateCloud(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_private_cloud(self, private_cloud_id: str) -> APIResult[PrivateCloud]:
        """
        Returns information for the specified private_cloud.

        Args:
            private_cloud_id (str): The unique identifier for the private_cloud.

        Returns:
            tuple: The resource record for the private_cloud.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /privateCloud/{private_cloud_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloud)
        if error:
            return (None, response, error)
        try:
            result = PrivateCloud(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_private_cloud(self, **kwargs) -> APIResult[PrivateCloud]:
        """
        Adds a new private_cloud.

        Returns:
            tuple: The newly created private_cloud resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /privateCloud
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloud)
        if error:
            return (None, response, error)
        try:
            result = PrivateCloud(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_private_cloud(self, private_cloud_id: str, **kwargs) -> APIResult[PrivateCloud]:
        """
        Updates an existing private_cloud.

        Args:
            private_cloud_id (str): The unique ID for the private_cloud being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated private_cloud resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /privateCloud/{private_cloud_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloud)
        if error:
            return (None, response, error)
        try:
            result = PrivateCloud(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_private_cloud(self, private_cloud_id: str) -> APIResult[None]:
        """
        Deletes the specified private_cloud.

        Args:
            private_cloud_id (str): The unique identifier for the private_cloud.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /privateCloud/{private_cloud_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
