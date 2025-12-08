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
from zscaler.zia.models.ipv6_config import IPV6PrefixMask
from zscaler.zia.models.ipv6_config import IPV6Configuration

from zscaler.utils import format_url


class TrafficIPV6ConfigAPI(APIClient):
    """
    A Client object for the Traffic IPV6 Configuration resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_ipv6_config(self) -> IPV6Configuration:
        """
        Gets the IPv6 configuration details for the organization.

        Returns:

        Examples:
            List IPV6 Configuration:

        >>> try:
            ...     ipv6_config = client.zia.ipv6_config.get_ipv6_config()
        ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}") ipv6_config
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipv6config
        """
        )

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request, IPV6Configuration)
        result = IPV6Configuration(self.form_response_body(response.get_body()))
        return result

    def list_dns64_prefix(self, query_params: Optional[dict] = None) -> List[IPV6PrefixMask]:
        """
        Fetches the list of NAT64 prefixes configured as the DNS64 prefix for the organization

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: String used to match against a DNS64 prefix's name,
                    description, or prefixMask attributes.

        Returns:

        Examples:
            List IPV6 Configuration:

        >>> try:
            ...     ipv6_list = client.zia.gre_tunnel.get_ipv6_config()
        ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        ... for ipv6 in ipv6_list:
        ...     print(ipv6.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipv6config/dns64prefix
        """
        )

        body = {}
        headers = {}

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        response = self._request_executor.execute(request, IPV6PrefixMask)

        try:
            response_data = self.form_response_body(response.get_body())
            results = []
            for item in response_data:
                results.append(IPV6PrefixMask(item))

            return results

        except Exception as error:
            return List[IPV6PrefixMask]

    def list_nat64_prefix(self, query_params: Optional[dict] = None) -> List[IPV6PrefixMask]:
        """
        Fetches the list of NAT64 prefixes configured for the organization

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 100 and the maximum size is 1000.

                ``[query_params.search]`` {str}: String used to match against a DNS64 prefix's name,
                    description, or prefixMask attributes.

        Returns:

        Examples:
            List IPV6 Configuration:

        >>> try:
            ...     ipv6_list = client.zia.gre_tunnel.get_nat64_prefix()
        ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        ... for ipv6 in ipv6_list:
        ...     print(ipv6.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipv6config/nat64prefix
        """
        )

        body = {}
        headers = {}

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        response = self._request_executor.execute(request)

        result = []
        for item in response.get_results():
            result.append(IPV6PrefixMask(self.form_response_body(item)))
        return result
