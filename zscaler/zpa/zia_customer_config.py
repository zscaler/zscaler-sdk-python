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
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.zia_customer_config import ZIACustomerConfig
from zscaler.zpa.models.zia_customer_config import SessionTerminationOnReauth
from zscaler.api_client import APIClient
from zscaler.utils import format_url
from zscaler.types import APIResult


class ZIACustomerConfigAPI(APIClient):
    """
    A Client object for the ZIA Customer Config resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def check_zia_cloud_config(self) -> APIResult[bool]:
        """
        Check if ZIA cloud config for a given customer is available.

        This endpoint returns a boolean value indicating whether the ZIA (Zscaler Internet Access)
        cloud service configuration is available for the customer.

        Returns:
            :obj:`Tuple`: A tuple containing a boolean value (True if available, False otherwise),
            the response object, and error if any.

        Examples:
            >>> is_available, _, err = client.zpa.zia_customer_config.check_zia_cloud_config()
            ... if err:
            ...     print(f"Error checking ZIA cloud config availability: {err}")
            ...     return
            ... if is_available:
            ...     print("ZIA cloud config is available")
            ... else:
            ...     print("ZIA cloud config is not available")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /config/isZiaCloudConfigAvailable
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_zia_cloud_service_config(self) -> APIResult[List[ZIACustomerConfig]]:
        """
        Get ZIA cloud service configuration for a given customer.

        This endpoint returns the ZIA (Zscaler Internet Access) cloud service configuration
        including domain, API keys, username, password, and sandbox API token settings.

        Returns:
            :obj:`Tuple`: A tuple containing (list of ZIACustomerConfig instances, Response, error)

        Examples:
            >>> config_list, _, err = client.zpa.zia_customer_config.get_zia_cloud_service_config()
            ... if err:
            ...     print(f"Error getting ZIA cloud service config: {err}")
            ...     return
            ... print(f"Total ZIA customer configs found: {len(config_list)}")
            ... for config in config_list:
            ...     print(config.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /config/ziaCloudConfig
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ZIACustomerConfig)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ZIACustomerConfig(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_zia_cloud_service_config(self, **kwargs) -> APIResult[ZIACustomerConfig]:
        """
        Add or update ZIA cloud service configuration for a given customer.

        This endpoint allows you to configure the ZIA (Zscaler Internet Access) cloud service
        integration settings including domain, API keys, authentication credentials, and sandbox token.

        Keyword Args:
            zia_cloud_domain (str): The ZIA cloud domain name for the customer.
            zia_cloud_service_api_key (str): The API key for accessing ZIA cloud services.
            zia_username (str): The username for ZIA authentication.
            zia_password (str): The password for ZIA authentication.
            zia_sandbox_api_token (str): The API token for ZIA Sandbox service integration.

        Returns:
            :obj:`Tuple`: A tuple containing the ZIACustomerConfig instance, response object, and error if any.

        Examples:
            >>> config, _, err = client.zpa.zia_customer_config.add_zia_cloud_service_config(
            ...     zia_cloud_domain="example.zscaler.net",
            ...     zia_cloud_service_api_key="your_api_key_here",
            ...     zia_username="admin@example.com",
            ...     zia_password="your_password",
            ...     zia_sandbox_api_token="your_sandbox_token"
            ... )
            ... if err:
            ...     print(f"Error adding ZIA cloud service config: {err}")
            ...     return
            ... print(f"ZIA cloud service config added successfully: {config.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /config/ziaCloudConfig
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ZIACustomerConfig)
        if error:
            return (None, response, error)

        try:
            result = ZIACustomerConfig(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_session_termination_on_reauth(self) -> APIResult[dict]:
        """
        Get session termination on reauth configuration for a given customer.

        This endpoint returns the session termination on reauth settings including whether
        session termination is enabled and whether it can be disabled.

        Returns:
            :obj:`Tuple`: A tuple containing a dictionary with the following keys:
            - `allow_disable_session_termination_on_reauth` (bool): Whether disabling session termination on reauth is allowed
            - `session_termination_on_reauth` (bool): Whether session termination on reauth is enabled
            The response object, and error if any.

        Examples:
            >>> config, _, err = client.zpa.zia_customer_config.get_session_termination_on_reauth()
            ... if err:
            ...     print(f"Error getting session termination on reauth config: {err}")
            ...     return
            ... print(f"Session termination on reauth: {config.get('session_termination_on_reauth')}")
            ... print(f"Allow disable: {config.get('allow_disable_session_termination_on_reauth')}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /config/sessionTerminationOnReauth
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SessionTerminationOnReauth)
        if error:
            return (None, response, error)

        try:
            result = SessionTerminationOnReauth(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_session_termination_on_reauth(self, **kwargs) -> APIResult[SessionTerminationOnReauth]:
        """
        Update the session termination on reauth configuration for a given customer.

        This endpoint allows you to update whether session termination on reauth is enabled.
        The API requires the `session_termination_on_reauth` attribute to be passed in the body.

        Keyword Args:
            session_termination_on_reauth (bool): Whether session termination on reauth is enabled.

        Returns:
            :obj:`Tuple`: A tuple containing the SessionTerminationOnReauth instance (None if 204 No Content),
            response object, and error if any.

            Note: This API returns 204 No Content on success, so the result will be None. To get the
            updated configuration, call `get_session_termination_on_reauth()` after this operation.

        Examples:
            >>> updated_config, _, err = client.zpa.zia_customer_config.update_session_termination_on_reauth(
            ...     session_termination_on_reauth=True
            ... )
            ... if err:
            ...     print(f"Error updating session termination on reauth: {err}")
            ...     return
            ... print(f"Session termination on reauth updated: {updated_config.session_termination_on_reauth}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /config/sessionTerminationOnReauth
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SessionTerminationOnReauth)
        if error:
            return (None, response, error)

        if response is None:
            return (None, None, None)

        try:
            result = SessionTerminationOnReauth(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
