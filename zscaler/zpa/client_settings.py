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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.client_settings import ClientSettings
from zscaler.utils import format_url


class ClientSettingsAPI(APIClient):
    """
    A Client object for the Client Setting resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def get_client_settings(self, query_params: Optional[dict] = None) -> ClientSettings:
        """
        Returns a list of client setting details.
        ClientCertType defaults to `CLIENT_CONNECTOR`

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.type]`` {str}: Available values: `ZAPP_CLIENT`, `ISOLATION_CLIENT`, `APP_PROTECTION`

        Returns:
            :obj:`Tuple`: A tuple containing a list of `ClientSettings` instances, response object, and error if any.

        Examples:
            Return all client setting types

            >>> try:
            ...     client_settings = client.zpa.client_settings.get_client_settings()
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... for setting in client_settings:
            ...     print(setting.as_dict())

            Return a specific client setting type

            >>> try:
            ...     client_settings = client.zpa.client_settings.get_client_settings(
            ... query_params={'type': 'ZAPP_CLIENT'}
            )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... for setting in client_settings:
            ...     print(setting.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /clientSetting
        """
        )

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ClientSettings)
        result = []
        for item in response.get_results():
            result.append(ClientSettings(self.form_response_body(item)))
        return result

    def get_all_client_settings(self) -> Any:
        """
        Returns all client setting details.
        ClientCertType defaults to `CLIENT_CONNECTOR`

        Returns:
            :obj:`Tuple`: A tuple containing a list of `ClientSettings` instances, response object, and error if any.

        Examples:
            >>> try:
            ...     fetched_settings = client.zpa.client_settings.get_all_client_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ...     return
            ... for setting in fetched_settings:
            ...     print(setting.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /clientSetting/all
        """
        )

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request)
        result = []
        for item in response.get_results():
            result.append(ClientSettings(self.form_response_body(item)))
        return result

    def add_client_setting(self, **kwargs) -> ClientSettings:
        """
        Ccreate Client Setting for a customer. `ClientCertType` defaults to `CLIENT_CONNECTOR`

        Args:
            name (str):
            enrollment_cert_id (str):
            client_certificate_type (str):

        Returns:
            :obj:`Tuple`: ClientSettings: The created client setting object.

        Example:
            # Basic example: Add a new client setting
            >>> try:
            ...     added_client_setting = client.zpa.client_settings.add_client_setting(
            ...     name="NewClientSetting",
            ...     enrollment_cert_id='245675',
            ...     client_certificate_type='ZAPP_CLIENT'
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /clientSetting
        """
        )

        body = kwargs

        request = self._request_executor.create_request(http_method, api_url, body=body)
        response = self._request_executor.execute(request, ClientSettings)
        result = ClientSettings(self.form_response_body(response.get_body()))
        return result

    def delete_client_setting(self) -> None:
        """
        Deletes the specified client setting.

        Args:

        Returns:
            int: Status code of the delete operation.

        Example:
            # Delete a client setting
            >>> try:
            ...     _ = client.zpa.client settings.delete_client_setting()
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Client setting with ID deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /clientSetting
        """
        )

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request)

        return None
