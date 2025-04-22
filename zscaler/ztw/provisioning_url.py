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
from zscaler.ztw.models.provisioning_url import ProvisioningURL
from zscaler.utils import format_url


class ProvisioningURLAPI(APIClient):
    """
    A Client object for the ProvisioningURLAPI resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_provisioning_url(self, query_params=None) -> tuple:
        """
        List all provisioning URLs.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            :obj:`Tuple`: The list of provisioning URLs.

        Examples:
            Print all provisioning URLs::

                roles = ztw.provisioning.list_provisioning_url()
                for role in roles:
                    print(role)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /provUrl
        """
        )

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
                result.append(ProvisioningURL(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_provisioning_url(self, provision_id: str) -> tuple:
        """
        Get details for a provisioning template by ID.

        Args:
            provision_id (str): ID of Cloud & Branch Connector provisioning template.

        Returns:
            :obj:`Tuple`: The provisiong template url details.

        Examples:
            Print the details of a provisioning template url:

                print(ztw.provisioning.get_provisioning_url("123456789")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /provUrl/{provision_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ProvisioningURL)
        if error:
            return (None, response, error)

        try:
            result = ProvisioningURL(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
