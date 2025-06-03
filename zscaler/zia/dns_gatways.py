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
            ... query_params={"search": 'DNS_GW01'})
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
            >>> fetched_gw, _, error = client.zia.dns_gatways.get_dns_gateways('87787')
            >>> if error:
            ...     print(f"Error fetching dns gateway by ID: {error}")
            ...     return
            ... print(f"Fetched dns gateway  by ID: {fetched_gw.as_dict()}")
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
            name (str): Name of the DNS Gateway

        Keyword Args:
            primary_ip_or_fqdn (str): IP address or FQDN of the primary DNS service provided by your DNS service provider
            secondary_ip_or_fqdn (str): IP address or FQDN of the secondary DNS service provided by your DNS service provider
            primary_ports (list[int]): Lists the ports for the primary DNS server based on the protocols selected.
            secondary_ports (list[int]): Lists the ports for the secondary DNS server based on the protocols selected.
            failure_behavior (str): Action that must be performed if the configured DNS service is unavailable or unhealthy.
            protocols (list[str]): Protocols that must be used to connect to the DNS service
                Supported Values: `ANY`, `TCP`, `UDP`, `DOH`

        Returns:
            tuple: A tuple containing the newly added DNS Gateway, response, and error.

        Examples:
            Add a new DNS Gateway:

            >>> added_gw, _, error = client.zia.dns_gatways.add_dns_gateway(
            ...     name=f"DNS_GW01_{random.randint(1000, 10000)}",
            ...     primary_ip_or_fqdn='8.8.8.8',
            ...     secondary_ip_or_fqdn='4.4.4.4',
            ...     failure_behavior='FAIL_RET_ERR',
            ...     protocols=['TCP', 'UDP', 'DOH'],
            ...     primary_ports=['53', '53', '443'],
            ...     secondary_ports=['53', '53', '443']
            ... )
            >>> if error:
            ...     print(f"Error adding dns gateway: {error}")
            ...     return
            ... print(f"DNS Gateway added successfully: {added_gw.as_dict()}")
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

        Keyword Args:
            name (str): Name of the rule, max 31 chars.
            primary_ip_or_fqdn (str): IP address or FQDN of the primary DNS service provided by your DNS service provider
            secondary_ip_or_fqdn (str): IP address or FQDN of the secondary DNS service provided by your DNS service provider
            primary_ports (list[int]): Lists the ports for the primary DNS server based on the protocols selected.
            secondary_ports (list[int]): Lists the ports for the secondary DNS server based on the protocols selected.
            failure_behavior (str): Action that must be performed if the configured DNS service is unavailable or unhealthy.
            protocols (list[str]): Protocols that must be used to connect to the DNS service
                Supported Values: `ANY`, `TCP`, `UDP`, `DOH`

        Returns:
            tuple: A tuple containing the updated DNS Gateway, response, and error.

        Examples:
            Updating an existing DNS Gateway:

            >>> updated_gw, _, error = client.zia.dns_gatways.add_dns_gateway(
            ...     gateway_id='671763',
            ...     name=f"UpdateDNS_GW01_{random.randint(1000, 10000)}",
            ...     primary_ip_or_fqdn='8.8.8.8',
            ...     secondary_ip_or_fqdn='4.4.4.4',
            ...     failure_behavior='FAIL_RET_ERR',
            ...     protocols=['TCP', 'UDP', 'DOH'],
            ...     primary_ports=['53', '53', '443'],
            ...     secondary_ports=['53', '53', '443']
            ... )
            >>> if error:
            ...     print(f"Error updating dns gateway: {error}")
            ...     return
            ... print(f"DNS Gateway updated successfully: {updated_gw.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnsGateways/{gateway_id}
        """
        )
        body = kwargs
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

        Examples:
            Updating an existing DNS Gateway:

            >>> _, _, error = client.zia.dns_gatways.delete_dns_gateway('778766')
            >>> if error:
            ...     print(f"Error deleting dns gateway: {error}")
            ...     return
            ... print(f"DNS Gateway with ID '778766' deleted successfully.")
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
