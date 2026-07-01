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
from zscaler.zia.models.azure_integration import AzureVirtualHub


class AzureIntegrationAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_azures_refresh_connection_status(self, query_params=None) -> APIResult[List[AzureVirtualHub]]:
        """
        List azures (refreshConnectionStatus).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AzureVirtualHub instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /azure/refreshConnectionStatus
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
                result.append(AzureVirtualHub(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_azures_tunnel_configuration(self, query_params=None) -> APIResult[List[AzureVirtualHub]]:
        """
        List azures (tunnelConfiguration).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AzureVirtualHub instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /azure/tunnelConfiguration
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
                result.append(AzureVirtualHub(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_azures_un_configure_tunnel_status(self, query_params=None) -> APIResult[List[AzureVirtualHub]]:
        """
        List azures (unConfigureTunnelStatus).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AzureVirtualHub instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /azure/unConfigureTunnelStatus
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
                result.append(AzureVirtualHub(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_azures_virtual_hub_sync(self, query_params=None) -> APIResult[List[AzureVirtualHub]]:
        """
        List azures (virtualHubSync).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AzureVirtualHub instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /azure/virtualHubSync
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
                result.append(AzureVirtualHub(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_azures_virtual_hubs(self, query_params=None) -> APIResult[List[AzureVirtualHub]]:
        """
        List azures (virtualHubs).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AzureVirtualHub instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /azure/virtualHubs
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
                result.append(AzureVirtualHub(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_azure(self, **kwargs) -> APIResult[AzureVirtualHub]:
        """
        Adds a new azure.

        Returns:
            tuple: The newly created azure resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /azure
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AzureVirtualHub)
        if error:
            return (None, response, error)
        try:
            result = AzureVirtualHub(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_azure(self, azure_id: int) -> APIResult[None]:
        """
        Deletes the specified azure.

        Args:
            azure_id (int): The unique identifier for the azure.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /azure/{azure_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
