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
from zscaler.ztb.models.api_key import APIKeyAuthRouter, APIKeyCreateResponse


class APIKeyAuthRouterAPI(APIClient):
    """
    Client for the ZTB API Key Auth resource.

    Provides operations for managing API keys in the
    Zero Trust Branch API.

    Endpoints live under ``/api/v3/api-key-auth``.
    """

    _ztb_base_endpoint = "/ztb/api/v3"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_api_keys(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get all API keys.

        Returns:
            Tuple of (list of APIKeyAuthRouter instances, response, error).

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.search]`` (str): Search string for filtering results.

                ``[query_params.page]`` (int): Page number for pagination.

                ``[query_params.limit]`` (int): Number of results per page.

                ``[query_params.sort]`` (str): Field to sort by.

                ``[query_params.sortdir]`` (str): Sort direction.

        Examples:
            List all API keys:

            >>> api_keys, _, error = client.ztb.api_keys.list_api_keys()
            >>> if error:
            ...     print(f"Error listing API keys: {error}")
            ...     return
            ... for key in api_keys:
            ...     print(key.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /api-key-auth/list
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
                result.append(APIKeyAuthRouter(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_api_key(self, **kwargs) -> APIResult:
        """
        Create a new API key.

        Args:
            name (str): The name for the new API key.
            **kwargs: Optional keyword args.

        Returns:
            Tuple of (APIKeyCreateResponse instance, response, error).

        Examples:
            Create a new API key:

            >>> created_key, _, error = client.ztb.api_keys.create_api_key(
            ...     name="Python_New_API_Key",
            ... )
            >>> if error:
            ...     print(f"Error creating API key: {error}")
            ...     return
            ... print(f"API key created successfully: {created_key.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /api-key-auth/create
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, APIKeyCreateResponse)
        if error:
            return (None, response, error)

        try:
            result = APIKeyCreateResponse(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def revoke_api_key(self, api_key_id: str) -> APIResult[dict]:
        """
        Revoke an API key by ID.

        Args:
            api_key_id (str): The unique identifier of the API key to revoke.

        Returns:
            Tuple of (None, response, error).

        Examples:
            Revoke an API key:

            >>> _, _, error = client.ztb.api_keys.revoke_api_key("abc-123")
            >>> if error:
            ...     print(f"Error revoking API key: {error}")
            ...     return
            ... print(f"API key 'abc-123' revoked successfully.")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /api-key-auth/revoke/{api_key_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
