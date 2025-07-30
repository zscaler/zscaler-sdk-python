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

    def list_api_keys(self, query_params=None) -> tuple:
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
            :obj:`Tuple`: A tuple containing (list of ApiKeys instances, Response, error)

        Examples:
            >>> key_list, _, err = client.zpa.api_keys.list_api_keys(
            ... query_params={'search': 'ZPA_Dev01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing api key: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApiKeys)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ApiKeys(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_api_key(self, key_id: str, query_params=None) -> tuple:
        """
        Fetches a specific api key by ID.

        Args:
            key_id (str): The unique identifier for the API Key.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (ApiKeys instance, Response, error).

        Examples:
            >>> fetched_key, _, err = client.zpa.api_keys.get_api_key('999999')
            ... if err:
            ...     print(f"Error fetching key by ID: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApiKeys)
        if error:
            return (None, response, error)

        try:
            result = ApiKeys(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_api_key(self, **kwargs) -> tuple:
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
            >>> added_key, _, err = client.zpa.api_keys.add_api_key(
            ...     name=f"NewAPIKey_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     token_expiry_time_in_sec= '3600',
            ...     role_id='28',
            ... )
            ... if err:
            ...     print(f"Error creating api key: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApiKeys)
        if error:
            return (None, response, error)

        try:
            result = ApiKeys(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_api_key(self, key_id: str, **kwargs) -> tuple:
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
            >>> added_key, _, err = client.zpa.api_keys.add_api_key(
            ...     name=f"NewAPIKey_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     token_expiry_time_in_sec= '3600',
            ...     role_id='28',
            ... )
            ... if err:
            ...     print(f"Error creating api key: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApiKeys)
        if error:
            return (None, response, error)

        if response is None:
            return (ApiKeys({"id": key_id}), None, None)

        try:
            result = ApiKeys(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_api_key(self, key_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified API Key from ZPA.

        Args:
            key_id (str): The unique identifier for the API Key.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:
            tuple: A tuple containing the response and error (if any).

        Examples:
            >>> _, _, err = client.zpa.api_keys.delete_key_id(
            ...     key_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting api key: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
