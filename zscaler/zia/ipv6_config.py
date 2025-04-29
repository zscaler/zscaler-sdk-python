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
from zscaler.zia.models.ipv6_config import IPV6PrefixMask
from zscaler.zia.models.ipv6_config import IPV6Configuration

from zscaler.utils import format_url


class TrafficIPV6ConfigAPI(APIClient):
    """
    A Client object for the Traffic IPV6 Configuration resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_ipv6_config(self) -> tuple:
        """
        Gets the IPv6 configuration details for the organization.

        Returns:
            tuple: A tuple containing (IPV6 Configuration instance, Response, error)

        Examples:
            List IPV6 Configuration:

        >>> ipv6_config, _, err = client.zia.ipv6_config.get_ipv6_config()
        ... if err:
        ...     print(f"Error fetching ipv6 config: {err}")
        ...  return ipv6_config
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPV6Configuration)
        if error:
            return (None, response, error)

        try:
            result = IPV6Configuration(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_dns64_prefix(self, query_params=None) -> tuple:
        """
        Fetches the list of NAT64 prefixes configured as the DNS64 prefix for the organization

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: String used to match against a DNS64 prefix's name,
                    description, or prefixMask attributes.

        Returns:
            tuple: A tuple containing (IPV6Config instance, Response, error).

        Examples:
            List IPV6 Configuration:

        >>> ipv6_list, _, err = client.zia.gre_tunnel.get_ipv6_config()
        ... if err:
        ...     print(f"Error listing ipv6 config: {err}")
        ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPV6PrefixMask)

        if error:
            return (None, response, error)

        try:
            response_data = self.form_response_body(response.get_body())
            results = []
            for item in response_data:
                results.append(IPV6PrefixMask(item))

            return (results, response, None)

        except Exception as error:
            return (None, response, error)

    def list_nat64_prefix(self, query_params=None) -> tuple:
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
            tuple: A tuple containing (IPV6Config instance, Response, error).

        Examples:
            List IPV6 Configuration:

        >>> ipv6_list, _, err = client.zia.gre_tunnel.get_nat64_prefix()
        ... if err:
        ...     print(f"Error listing ipv6 config: {err}")
        ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(IPV6PrefixMask(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
