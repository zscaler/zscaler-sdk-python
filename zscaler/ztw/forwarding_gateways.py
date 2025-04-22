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

from zscaler.request_executor import RequestExecutor
from zscaler.api_client import APIClient
from zscaler.ztw.models.forwarding_gateways import ForwardingGateways
from zscaler.utils import format_url


class ForwardingGatewaysAPI(APIClient):

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_gateways(self, query_params=None) -> tuple:
        """
        Retrieves a list of ZIA gateways and Log and Control gateways.

        Returns:
            tuple: A tuple containing:
                N/A

        Examples:
            >>> proxy, response, err = client.ztw.forwarding_gateways.list_gateways()

        """

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /gateways
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
                results.append(ForwardingGateways(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def list_gateway_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists IP Source Groups name and ID  all IP Source Groups.
        This endpoint retrieves only IPv4 source address groups.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: The search string used to match against a group's name or description attributes.

        Returns:
            tuple: List of forward gateways resource records.

        Examples:
            Gets a list of all forward gateways.

            >>> gw_list, response, error = ztw.forwarding_gateways.list_gateway_lite():
            ... if error:
            ...     print(f"Error listing forward gateways: {error}")
            ...     return
            ... print(f"Total gateways found: {len(gw_list)}")
            ... for gw in gw_list:
            ...     print(gw.as_dict())

            Gets a list of all forward gateways name and ID.

            >>> gw_list, response, error = ztw.forwarding_gateways.list_gateway_lite(query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing forward gateways: {error}")
            ...     return
            ... print(f"Total gateways found: {len(gw_list)}")
            ... for gw in gw_list:
            ...     print(gw.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /gateways/lite
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
                results.append(ForwardingGateways(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def add_gateway(self, **kwargs) -> tuple:
        """
        Creates a new ZTW Forwarding Gateway.

        Args:
            name (str): Name of the gateway.
            **kwargs: Optional keyword args.

        Keyword Args:
            type (str): Type of the gateway. Supported types are ZIA and ECSELF (Log and Control gateway).
                Supported Values: "PROXYCHAIN", "ZIA", "ECSELF"
            description (str): Description of the gateway.
            fail_closed (bool): Indicates that traffic must be dropped when both primary and secondary proxies defined in the gateway are unreachable.
            manual_primary (str): Specifies the primary proxy through which traffic must be forwarded.
            manual_secondary (str): Specifies the secondary proxy through which traffic must be forwarded.
            subcloud_primary (list): If a manual (DC) primary proxy is used and if the organization has subclouds associated, you can specify a subcloud using this field for the specified DC
            subcloud_secondary (list): If a manual (DC) secondary proxy is used and if the organization has subclouds associated, you can specify a subcloud using this field for the specified DC
            primary_type (str): Type of the primary proxy, such as automatic proxy (AUTO), manual proxy (DC)
                Supported values: "NONE", "AUTO", "MANUAL_OVERRIDE", "SUBCLOUD", "VZEN", "PZEN", "DC"
            secondary_type (str): Type of the secondary proxy, such as automatic proxy (AUTO), manual proxy (DC)
                Supported values: "NONE", "AUTO", "MANUAL_OVERRIDE", "SUBCLOUD", "VZEN", "PZEN", "DC"

        Returns:
            tuple: A tuple containing the newly added Forwarding Gateway, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /gateways
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

        response, error = self._request_executor.execute(request, ForwardingGateways)
        if error:
            return (None, response, error)

        try:
            result = ForwardingGateways(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_gateway(self, gateway_id: int) -> tuple:
        """
        Deletes a ZIA gateway or Log and Control gateway based on the specified ID.

        Args:
            gateway_id (str): The unique identifier of the ZIA gateway or Log and Control gateway.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /gateways/{gateway_id}
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
