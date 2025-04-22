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
from zscaler.ztw.models.api_keys import ApiKeys
from zscaler.utils import format_url


class ProvisioningAPIKeyAPI(APIClient):
    """
    A Client object for the ProvisioningAPIKeyAPI resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_api_keys(self, query_params=None) -> tuple:
        """
        List all existing API keys.

        Keyword Args:
            query_params (dict): Map of query parameters for the request.

                ``[query_params.include_partner_keys]`` (bool): Include or exclude partner keys from the list.

        Returns:
            :obj:`Tuple`: The list of API keys.

        Examples:
            List all API keys::

                for api_key in ztw.admin.list_api_keys():
                    print(api_key)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /apiKeys
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ApiKeys(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def regenerate_api_key(self, key_id: str, **kwargs) -> tuple:
        """
        Regenerate the specified API key.

        Args:
            key_id (str): The ID of the API key to regenerate.

        Returns:
            :obj:`Tuple`: The regenerated API key.

        Examples:
            Regenerate an API key::

                print(ztw.admin.regenerate_api_key("123456789"))

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /apiKeys/{key_id}/regenerate
        """
        )

        body = kwargs

        # Create the request with no empty param handling logic
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ApiKeys)
        if error:
            return (None, response, error)

        try:
            result = ApiKeys(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
