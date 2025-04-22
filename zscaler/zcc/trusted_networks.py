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
from zscaler.utils import format_url
from zscaler.zcc.models.trustednetworks import TrustedNetworks


class TrustedNetworksAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def list_by_company(self, query_params=None) -> tuple:
        """
        Returns the list of Trusted Networks By Company ID in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size.
                ``[query_params.search]`` {str}: The search string used to partially match.

        Returns:
            :obj:`list`: A list containing Trusted Networks By Company ID in the Client Connector Portal.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webTrustedNetwork/listByCompany
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            # Extract the list of trusted networks from the response
            response_body = response.get_body()
            trusted_networks = response_body.get("trustedNetworkContracts", [])

            # Convert each network into a TrustedNetwork object
            result = [TrustedNetworks(network) for network in trusted_networks]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_trusted_network(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Rule Label.

        Args:
            id (str):
            active (bool):
            company_id (str):
            condition_type (str):
            created_by (str):
            dns_search_domains (str):
            dns_servers (str):
            edited_by (str):
            guid (str):
            hostnames (str):
            network_name (str):
            resolved_ips_for_hostname (str):
            ssids (str):
            trusted_dhcp_servers (str):
            trusted_egress_ips (str):
            trusted_gateways (str):
            trusted_subnets (str):

        Returns:
            tuple: A tuple containing the newly added Trusted Network, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webTrustedNetwork/create
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

        # Execute the request
        response, error = self._request_executor.execute(request, TrustedNetworks)
        if error:
            return (None, response, error)

        try:
            result = TrustedNetworks(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_trusted_network(self, **kwargs) -> tuple:
        """
        Update Trusted Network

        Args:
            N/A

        Returns:
            tuple: A tuple containing the Update Trusted Network, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webTrustedNetwork/edit
        """
        )
        body = {}

        body.update(kwargs)

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, TrustedNetworks)
        if error:
            return (None, response, error)

        try:
            result = TrustedNetworks(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_trusted_network(self, network_id: int) -> tuple:
        """
        Deletes the specified Trusted Network.

        Args:
            network_id (str): The unique identifier of the Trusted Network.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webTrustedNetwork/{network_id}/delete
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
