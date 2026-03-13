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

import logging
from typing import Dict, Any, Optional, List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.alarms import Alarms
from zscaler.ztb.models.app_connector_config import AppConnectorConfigResult


class AppConnectorConfigAPI(APIClient):
    """
    Client for the ZTB App Connector Config resource.

    Provides CRUD operations for app connector config in the
    Zero Trust Branch API.
    """

    # ASSUMPTION: ZTB alarm endpoints live under /api/v2 based on Swagger docs.
    # When used via the OneAPI gateway the ``/ztb`` prefix is prepended by
    # the service routing layer.
    _ztb_base_endpoint = "/ztb/api/v3"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_app_connector_config(self, cluster_id: str) -> APIResult:
        """
        Get a single app connector config by cluster ID.

        Args:
            cluster_id: The cluster identifier.

        Returns:
            Tuple of (AppConnectorConfigResult instance, response, error).

        Examples:
            >>> app_connector_config, response, error = client.ztb.app_connector_config.get_app_connector_config("abc-123")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /appconnector/config
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppConnectorConfigResult)
        if error:
            return (None, response, error)

        try:
            result = AppConnectorConfigResult(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_app_connector_config(self, **kwargs) -> APIResult:
        """
        Create a new app connector config.

        Args:
            **kwargs: App connector config creation fields.

        Returns:
            Tuple of (AppConnectorConfigResult instance, response, error).

        Examples:
            >>> app_connector_config, response, error = client.ztb.app_connector_config.create_app_connector_config(name="test")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /appconnector/config
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppConnectorConfigResult)
        if error:
            return (None, response, error)

        try:
            result = AppConnectorConfigResult(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_app_connector(self, cluster_id: int) -> APIResult[dict]:
        """
        Delete AppConnector config.

        Args:
            cluster_id (str): The unique identifier of the Cluster.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a app connector config:

            >>> _, _, error = client.ztb.app_connector_config.delete_app_connector('73459')
            >>> if error:
            ...     print(f"Error deleting AppConnector config: {error}")
            ...     return
            ... print(f"AppConnector config with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /appconnector/config
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
