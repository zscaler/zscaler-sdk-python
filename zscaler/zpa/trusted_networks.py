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
from zscaler.zpa.models.trusted_network import TrustedNetwork
from zscaler.utils import format_url


class TrustedNetworksAPI(APIClient):
    """
    A client object for the Trusted Networks resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_trusted_networks(self, query_params=None) -> tuple:
        """
        Returns a list of all configured trusted networks.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.
                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            list: A list of `TrustedNetwork` instances.

        Example:
            >>> trusted_networks = zpa.trusted_networks.list_trusted_networks(search="example")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /network
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Prepare request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TrustedNetwork(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_network(self, network_id: str) -> tuple:
        """
        Returns information on the specified trusted network.

        Args:
            network_id (str): The unique identifier for the trusted network.

        Returns:
            TrustedNetwork: The corresponding trusted network object.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /network/{network_id}
        """
        )

        # Prepare request body, headers, and form (if needed)
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, TrustedNetwork)

        if error:
            return (None, response, error)

        try:
            result = TrustedNetwork(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_network_by_name(self, name: str, query_params=None):
        """
        Returns information on the trusted network with the specified name.

        Args:
            name (str): The name of the trusted network.

        Returns:
            TrustedNetwork or None: The resource record for the trusted network if found, otherwise None.
        """
        networks, response, error = self.list_trusted_networks(query_params=query_params)
        if error:
            return (None, response, error)

        for network in networks:
            if network.name == name:
                return network, response, None

        return None, response, None

    def get_network_by_udid(self, search_id: str, query_params={}) -> tuple:
        """
        Returns a trusted network based on its 'network_id'.

        Args:
            search_id (str): The unique identifier for the network_udid of the trusted network.

        Returns:
            TrustedNetwork: The resource record for the trusted network, or None if not found.
        """
        networks, response, error = self.list_trusted_networks(query_params=query_params)
        if error:
            return (None, response, error)

        for network in networks:
            if network.network_id == search_id:  # Assuming `network_id` is the UDID field
                return network, response, None  # Return the full TrustedNetwork object

        return None, response, None
