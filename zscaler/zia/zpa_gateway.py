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
from zscaler.zia.models.zpa_gateway import ZPAGateway
from zscaler.utils import format_url, convert_keys, snake_to_camel, transform_common_id_fields


class ZPAGatewayAPI(APIClient):
    """
    A Client object for the ZPA Gateway API resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_gateways(self, query_params=None) -> tuple:
        """
        Lists ZPA Gateways in your organization with pagination.
        A subset of ZPA Gateways can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.app_segment]`` {list}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of ZPA Gateways instances, Response, error)


        Examples:
            Get a list of all  ZPA Gateways Items

            >>> results = zia.zpa_gateway.list_gateways()
            ... for item in results:
            ...    print(item)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/zpaGateways
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ZPAGateway(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_gateway(self, gateway_id: int) -> tuple:
        """
        Returns the zpa gateway details for a given ZPA Gateway.

        Args:
            gatewayId (str): The unique identifier for the ZPA Gateway.

        Returns:
            tuple: A tuple containing (ZPA Gateway instance, Response, error).

        Examples:
            >>> gw = zia.zpa_gateway.get_gateway('99999')
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/zpaGateways/{gateway_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, ZPAGateway)

        if error:
            return (None, response, error)

        try:
            result = ZPAGateway(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_gateway(
        self,
        name: str,
        zpa_server_group: dict = None,
        **kwargs,
    ) -> tuple:
        """
        Creates a new ZPA Gateway.

        Args:
            name (str): The name of the ZPA Gateway.
            zpa_server_group (dict, required): The ZPA Server Group that is
                configured for Source IP Anchoring.
            zpa_app_segments (list, optional): All the Application Segments that are
                associated with the selected ZPA Server Group for which Source IP
                Anchoring is enabled.

        Keyword Args:
            description (str): Additional details about the ZPA gateway.
            type (str): Indicates whether the ZPA gateway is configured for Zscaler
                Internet Access (using option ZPA) or Zscaler Cloud Connector (using
                option ECZPA). Accepted values are 'ZPA' or 'ECZPA'.
            zpa_tenant_id (int): The ID of the ZPA tenant where Source IP Anchoring
                is configured

        Returns:
            :obj:`Tuple`: The newly added ZPA Gateway resource record.
        """
        payload = {"name": name, "type": "ZPA"}

        # Add zpa_server_group to kwargs
        if zpa_server_group:
            kwargs["zpa_server_group"] = zpa_server_group

        # Define the id groups specific to this function
        zpa_gateway_id_groups = [
            ("zpa_server_group", "zpaServerGroup"),
        ]
        transform_common_id_fields(zpa_gateway_id_groups, kwargs, payload)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        http_method = "post".upper()
        api_url = f"{self._zia_base_endpoint}/zpaGateways"

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = ZPAGateway(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_gateway(self, gateway_id: str, **kwargs) -> tuple:
        """
        Updates information for the specified ZPA Gateway.

        Args:
            gateway_id (str): The unique id for the ZPA Gateway to be updated.

        Keyword Args:
            name (str): The name of the ZPA gateway.
            description (str): Additional details about the ZPA gateway.
            type (str): Indicates whether the ZPA gateway is configured for
                Zscaler Internet Access (using option ZPA) or Zscaler Cloud
                Connector (using option ECZPA). Accepted values are 'ZPA' or 'ECZPA'.
            zpa_server_group (dict, optional): The ZPA Server Group configured for
                Source IP Anchoring.
            zpa_app_segments (list, optional): All the Application Segments associated
                with the selected ZPA Server Group for which Source IP Anchoring is
                enabled.
            zpa_tenant_id (int): The ID of the ZPA tenant where Source IP Anchoring
                is configured

        Returns:
            :obj:`Tuple`: The updated ZPA Gateway resource record.
        """
        payload = convert_keys(self.get_gateway(gateway_id))

        # Define the id groups specific to this function
        zpa_gateway_id_groups = [
            ("zpa_server_group", "zpaServerGroup"),
        ]

        transform_common_id_fields(zpa_gateway_id_groups, kwargs, payload)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        http_method = "put".upper()
        api_url = f"{self._zia_base_endpoint}/zpaGateways/{gateway_id}"

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return self.get_gateway(gateway_id)

    def delete_gateway(self, gateway_id) -> tuple:
        """
        Deletes the specified ZPA Gateway.

        Args:
            gateway_id (str): The unique identifier of the ZPA Gateway that will be deleted.

        Returns:
            :obj:`int`: The response code for the request.

        Examples
            >>> gateway = zia.zpa_gateway.delete_gateway('99999')

        """
        http_method = "delete".upper()
        api_url = f"{self._zia_base_endpoint}/zpaGateways/{gateway_id}"

        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.get_status(), response, None)
