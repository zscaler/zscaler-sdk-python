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
from zscaler.zia.models.dns_gatways import DNSGateways
from zscaler.utils import format_url
import logging

logger = logging.getLogger(__name__)


class DNSGatewayAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_dns_gateways(self, query_params=None) -> tuple:
        """
        Returns a list of dns gateways.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.page]`` (int): Specifies the page offset.

                ``[query_params.page_size]`` (int): Specifies the page size. The default size is 255.

        Returns:
            tuple:
                List of configured dns gateways as (DNSGatways, Response, error).

        Examples:
            List all dns gateways

            >>> gw_list, _, error = zia.dns_gateways.list_dns_gateways()
            ... if error:
            ...     print(f"Error listing gateways: {error}")
            ...     return
            ... print(f"Total gateways found: {len(gw_list)}")
            ... for gw in gw_list:
            ...     print(gw.as_dict())

            List dns gateway that match the name 'DNS_GW01'

            >>> gw_list, _, error = zia.dns_gateways.list_dns_gateways(
                query_params={"search": 'DNS_GW01'})
            ... if error:
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
            /dnsGateways
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                if isinstance(item, dict):
                    results.append(DNSGateways(self.form_response_body(item)))
                else:
                    logger.warning(f"Skipping non-dict item in DNS Gateways list: {item}")
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_dns_gateways(
        self,
        gateway_id: int,
    ) -> tuple:
        """
        Retrieves a list of Proxy Gateways.

        Returns:
            tuple: A tuple containing:
                N/A

        Examples:
            >>> proxy, response, err = client.zia.forwarding_control.get_proxy_gateways()

        """

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnsGateways/{gateway_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DNSGateways)

        if error:
            return (None, response, error)

        try:
            result = DNSGateways(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_dns_gateway(self, **kwargs) -> tuple:
        """
        Creates a new ZIA DNS Gateway.

        Args:
            name (str): Name of the rule, max 31 chars.
            action (str): Action for the rule.
            device_trust_levels (list): Device trust levels for the rule application.
                Values: `ANY`, `UNKNOWN_DEVICETRUSTLEVEL`, `LOW_TRUST`, `MEDIUM_TRUST`,
                `HIGH_TRUST`.

        Keyword Args:
            order (str): Rule order, defaults to the bottom.
            rank (str): Admin rank of the rule.
            state (str): Rule state ('ENABLED' or 'DISABLED').

        Returns:
            tuple: A tuple containing the newly added DNS Gateway, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnsGateways
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DNSGateways)

        if error:
            return (None, response, error)

        try:
            result = DNSGateways(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_dns_gateway(self, gateway_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA DNS Gateway.

        Args:
            gateway_id (int): The unique ID for the DNS Gateway.

        Returns:
            tuple: A tuple containing the updated DNS Gateway, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnsGateways/{gateway_id}
        """
        )
        body = kwargs.copy()
        body["id"] = gateway_id

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DNSGateways)
        if error:
            return (None, response, error)

        try:
            result = DNSGateways(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_dns_gateway(self, gateway_id: int) -> tuple:
        """
        Deletes the specified DNS Gateway.

        Args:
            gateway_id (str): The unique identifier of the DNS Gateway.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnsGateways/{gateway_id}
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
