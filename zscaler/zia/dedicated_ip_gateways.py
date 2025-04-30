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
from zscaler.zia.models.proxies import Proxies
from zscaler.zia.models.dedicated_ip_gateways import DedicatedIPGateways
from zscaler.utils import format_url


class DedicatedIPGatewaysAPI(APIClient):
    """
    A Client object for the Dedicated IP Gateways resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_dedicated_ip_gw_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Retrieves a list of dedicated IP gateways

        Args:

        Returns:
            tuple: A tuple containing (Proxies instance, Response, error).

        Examples:
            >>> gw_list, _, error = client.zia.dedicated_ip_gateways.list_dedicated_ip_gw_lite()
            >>> if error:
            ...     print(f"Error listing gateways: {error}")
            ...     return
            ... print(f"Total gateways found: {len(gw_list)}")
            ... for gw in gw_list:
            ...     print(gw.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dedicatedIPGateways/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DedicatedIPGateways)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(DedicatedIPGateways(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
