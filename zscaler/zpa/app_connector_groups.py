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
from zscaler.zpa.models.app_connector_groups import AppConnectorGroup


class AppConnectorGroupAPI(APIClient):

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_app_connector_groups(self, query_params=None) -> APIResult[List[AppConnectorGroup]]:
        """
        List app_connector_groups.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AppConnectorGroup instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /appConnectorGroup
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
                result.append(AppConnectorGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_app_connector_groups_sg(self, query_params=None) -> APIResult[List[AppConnectorGroup]]:
        """
        List app_connector_groups (sg).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AppConnectorGroup instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /appConnectorGroup/sg
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
                result.append(AppConnectorGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_app_connector_groups_summary(self, query_params=None) -> APIResult[List[AppConnectorGroup]]:
        """
        List app_connector_groups (summary).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AppConnectorGroup instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /appConnectorGroup/summary
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
                result.append(AppConnectorGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_app_connector_group(self, app_connector_group_id: str) -> APIResult[AppConnectorGroup]:
        """
        Returns information for the specified app_connector_group.

        Args:
            app_connector_group_id (str): The unique identifier for the app_connector_group.

        Returns:
            tuple: The resource record for the app_connector_group.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /appConnectorGroup/{app_connector_group_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppConnectorGroup)
        if error:
            return (None, response, error)
        try:
            result = AppConnectorGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_app_connector_group(self, **kwargs) -> APIResult[AppConnectorGroup]:
        """
        Adds a new app_connector_group.

        Returns:
            tuple: The newly created app_connector_group resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /appConnectorGroup
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppConnectorGroup)
        if error:
            return (None, response, error)
        try:
            result = AppConnectorGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_app_connector_group(self, app_connector_group_id: str, **kwargs) -> APIResult[AppConnectorGroup]:
        """
        Updates an existing app_connector_group.

        Args:
            app_connector_group_id (str): The unique ID for the app_connector_group being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated app_connector_group resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /appConnectorGroup/{app_connector_group_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppConnectorGroup)
        if error:
            return (None, response, error)
        try:
            result = AppConnectorGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_app_connector_group(self, app_connector_group_id: str) -> APIResult[None]:
        """
        Deletes the specified app_connector_group.

        Args:
            app_connector_group_id (str): The unique identifier for the app_connector_group.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /appConnectorGroup/{app_connector_group_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
