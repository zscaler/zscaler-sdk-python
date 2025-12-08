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
from zscaler.zpa.models.api_keys import ApiKeys
from zscaler.utils import format_url


class ApiKeysAPI(APIClient):
    """
    A Client object for the Api Keys resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_api_keys(self, query_params: Optional[dict] = None) -> List[ApiKeys]:
        """
        List all API keys details.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing List[ApiKeys]

        Examples:
            >>> try:
            ...     key_list = client.zpa.api_keys.list_api_keys(
            ... query_params={'search': 'ZPA_Dev01', 'page': '1', 'page_size': '100'})
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Total api key found: {len(key_list)}")
            ... for key in keys:
            ...     print(key.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /apiKeys
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ApiKeys)
        result = []
        for item in response.get_results():
            result.append(ApiKeys(self.form_response_body(item)))
        return result

    def get_api_key(self, key_id: str, query_params: Optional[dict] = None) -> ApiKeys:
        """
        Fetches a specific api key by ID.

        Args:
            key_id (str): The unique identifier for the API Key.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing ApiKeys.

        Examples:
            >>> try:
            ...     fetched_key = client.zpa.api_keys.get_api_key('999999')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Fetched key by ID: {fetched_key.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /apiKeys/{key_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ApiKeys)
        result = ApiKeys(self.form_response_body(response.get_body()))
        return result

    def add_api_key(self, **kwargs) -> ApiKeys:
        """
        Adds a new ZPA API Key.

        Args:
            name (str): The name of the API Key.

        Keyword Args:
            enabled (bool): Whether the API Key is enabled. Defaults to True.
            token_expiry_time_in_sec (str): The API Key Client ID.
            role_id (str): The unique identifier for the role associated with the API Key.

        Returns:
            :obj:`Tuple[dict, Response, Exception]`:
                A tuple containing:
                - An empty dictionary `{}` on success (due to 204 No Content),
                - The raw `Response` object,
                - Or an `Exception` if an error occurred.
                - This returns the client_secret attribute

        Examples:
            >>> try:
            ...     added_key = client.zpa.api_keys.add_api_key(
            ...     name=f"NewAPIKey_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     token_expiry_time_in_sec= '3600',
            ...     role_id='28',
            ... )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"API key created successfully: {added_key.as_dict()}")
            ... key_dict = added_key.as_dict()
            ... client_secret = key_dict.get('client_secret')
            ... print(f"Client Secret: {client_secret}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /apiKeys
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, ApiKeys)
        result = ApiKeys(self.form_response_body(response.get_body()))
        return result

    def update_api_key(self, key_id: str, **kwargs) -> ApiKeys:
        """
        Update a new ZPA API Key.

        Args:
            key_id (str): The unique identifier for the API Key.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Args:
            name (str): The name of the API Key.

        Keyword Args:
            enabled (bool): Whether the API Key is enabled. Defaults to True.
            token_expiry_time_in_sec (str): The API Key Client ID.
            role_id (str): The unique identifier for the role associated with the API Key.

        Returns:
            :obj:`Tuple[dict, Response, Exception]`:
                A tuple containing:
                - An empty dictionary `{}` on success (due to 204 No Content),
                - The raw `Response` object,
                - Or an `Exception` if an error occurred.
                - This method does not return the client_secret attribute

                The dictionary is always empty since the API returns no response body.

        Examples:
            >>> try:
            ...     added_key = client.zpa.api_keys.add_api_key(
            ...     name=f"NewAPIKey_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     token_expiry_time_in_sec= '3600',
            ...     role_id='28',
            ... )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"API key created successfully: {added_key.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /apiKeys/{key_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, ApiKeys)
        if response is None:
            return ApiKeys({"id": key_id})

        result = ApiKeys(self.form_response_body(response.get_body()))
        return result

    def delete_api_key(self, key_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified API Key from ZPA.

        Args:
            key_id (str): The unique identifier for the API Key.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:

        Examples:
            >>> try:
            ...     _ = client.zpa.api_keys.delete_key_id(
            ...     key_id='999999'
            ... )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"API Key with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /apiKeys/{key_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None
