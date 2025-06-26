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
from zscaler.zia.models.proxy_gateways import ProxyGatways
from zscaler.utils import format_url


class ProxiesAPI(APIClient):
    """
    A Client object for the Proxies resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_proxy_gateways(self) -> tuple:
        """
        Retrieves a list of Proxy Gateways.

        Returns:
            tuple: A tuple containing:
                N/A

        Examples:
            >>> gw_list, _, error = client.zia.proxies.list_proxy_gateways()
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
            /proxyGateways
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return None

        response, error = self._request_executor.execute(request)
        if error:
            return None

        try:
            result = []
            for item in response.get_results():
                result.append(ProxyGatways(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_proxy_gateway_lite(self) -> tuple:
        """
        Retrieves the name and ID of the proxy.

        Args:

        Returns:
            tuple: A tuple containing (Proxies instance, Response, error).

        Examples:
            >>> gw_list, _, error = client.zia.proxies.list_proxy_gateway_lite()
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
            /proxyGateways/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ProxyGatways)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ProxyGatways(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_proxies(self, query_params=None) -> tuple:
        """
        Lists Proxiess in your organization with pagination.
        A subset of Proxiess  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Page size for pagination.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of Proxiess instances, Response, error)

        Examples:
            List Proxiess using default settings:

            >>> label_list, _, error = client.zia.rule_labels.list_labels(
                query_params={'search': updated_label.name})
            >>> if error:
            ...     print(f"Error listing labels: {error}")
            ...     return
            ... print(f"Total labels found: {len(label_list)}")
            ... for label in label_list:
            ...     print(label.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /proxies
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
                result.append(Proxies(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_proxies_lite(self) -> tuple:
        """
        Fetches a specific Proxies lite.

        Args:

        Returns:
            tuple: A tuple containing (Proxies instance, Response, error).

        Example:
            List all proxies:

            >>> rules_list, response, error = client.zia.proxies.list_proxies_lite()
            ... if error:
            ...    print(f"Error listing bandwidth control rules: {error}")
            ...    return
            ... print(f"Total rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /proxies/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Proxies)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(Proxies(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_proxy(self, proxy_id: int) -> tuple:
        """
        Fetches a specific Proxiess by ID.

        Args:
            proxy_id (int): The unique identifier for the Proxies.

        Returns:
            tuple: A tuple containing (Proxies instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /proxies/{proxy_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Proxies)
        if error:
            return (None, response, error)

        try:
            result = Proxies(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_proxy(self, **kwargs) -> tuple:
        """
        Adds a new proxy for a third-party proxy service.

        Args:
            name (str): The name of the Proxy.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional notes or information
            type (str): Gateway type. Supported Values: `PROXYCHAIN`, `ZIA`, `ECSELF`
            address (list): The IP address or the FQDN of the third-party proxy service
            port (str): The port number on which the third-party proxy service listens to the requests forwarded from Zscaler
            cert (list): The root certificate used by the third-party proxy to perform SSL inspection.
            insert_xau_header (bool): Flag indicating whether X-Authenticated-User header is added by the proxy.
            base64_encode_xau_header (bool): Flag indicating whether the added X-Authenticated-User header is Base64 encoded.

        Returns:
            :obj:`Tuple`: The newly created IP Destination Group resource record.

        Examples:
            Add a Proxy of Type `PROXYCHAIN`:

            >>> zia.proxies.add_proxy(
            ...     name='Proxy01',
            ...     description='Proxy01',
            ...     type='PROXYCHAIN',
            ...     address='192.168.1.1',
            ...     port='5000',
            ...     cert={'id': 5465},
            ...     insert_xau_header=True,
            ...     base64_encode_xau_header=True,
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /proxies
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

        response, error = self._request_executor.execute(request, Proxies)
        if error:
            return (None, response, error)

        try:
            result = Proxies(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_proxy(self, proxy_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Proxies.

        Args:
            proxy_id (int): The unique ID for the Proxies.

        Returns:
            tuple: A tuple containing the updated Proxies, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /proxies/{proxy_id}
        """
        )

        body = kwargs
        body["id"] = proxy_id

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Proxies)
        if error:
            return (None, response, error)

        try:
            result = Proxies(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_proxy(self, proxy_id: int) -> tuple:
        """
        Deletes the specified Proxies.

        Args:
            proxy_id (str): The unique identifier of the Proxies.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /proxies/{proxy_id}
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
