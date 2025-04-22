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
from zscaler.utils import format_url


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
            Get a list of all ZPA Gateways Items

            >>> gw_list, _, error = client.zia.zpa_gateway.list_gateways()
                if error:
                    print(f"Error listing zpa gateway: {error}")
                    return
                print(f"Total gateways found: {len(rulgw_listes_list)}")
                for rule in gw_list:
                    print(rule.as_dict())

            Search a ZPA Gateways By Name

            >>> gw_list, _, error = client.zia.zpa_gateway.list_gateways(query_params={'search': 'ZPA_GW01'})
            ... if error:
            ...     print(f"Error listing zpa gateway: {error}")
            ...     return
            ... for rule in gw_list:
            ...     print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/zpaGateways
        """
        )

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
                result.append(ZPAGateway(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_gateway(self, gateway_id: int) -> tuple:
        """
        Returns the zpa gateway details for a given ZPA Gateway.

        Args:
            gateway_id (str): The unique identifier for the ZPA Gateway.

        Returns:
            tuple: A tuple containing (ZPA Gateway instance, Response, error).

        Examples:
            >>> etched_gateway, _, error = client.zia.zpa_gateway.get_gateway(gateway_id=18423896)
            ... if error:
            ...     print(f"Error fetching gateway by ID: {error}")
            ...     return
            ... print(f"Fetched gateway by ID: {fetched_gateway.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/zpaGateways/{gateway_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ZPAGateway)

        if error:
            return (None, response, error)

        try:
            result = ZPAGateway(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_gateway(
        self,
        name: str,
        zpa_server_group: dict = None,
        zpa_app_segments: dict = None,
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

        Examples:
            Adding a new ZPA Gateway

            >>> added_gateway, _, error = client.zia.zpa_gateway.add_gateway(
            ... name=f"NewGateway_{random.randint(1000, 10000)}",
            ... description=f"NewGateway_{random.randint(1000, 10000)}",
            ... zpa_server_group={
            ...     "name": "App_Segment_IP_Source_Anchoring2",
            ...     "external_id": "72058304855090128"
            ... },
            ... zpa_app_segments=[
            ... {
            ...      "name": "App_Segment_IP_Source_Anchoring1",
            ...      "external_id": "72058304855090129"
            ...  }
            ... ])
            ... if error:
            ...     print(f"Error adding gateway: {error}")
            ...     return
            ... print(f"Gateway added successfully: {added_gateway.as_dict()}")
        """

        if not zpa_server_group:
            return (None, None, ValueError("zpa_server_group is required"))
        if not zpa_app_segments:
            return (None, None, ValueError("zpa_app_segments is required"))

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /zpaGateways
        """
        )

        body = {
            "name": name,
            "type": "ZPA",
            "zpaServerGroup": zpa_server_group,
            "zpaAppSegments": zpa_app_segments,
        }
        body.update(kwargs)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ZPAGateway)
        if error:
            return (None, response, error)

        try:
            result = ZPAGateway(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_gateway(self, gateway_id: str, zpa_server_group: dict = None, zpa_app_segments: dict = None, **kwargs) -> tuple:
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

        Examples:
            Updating a new ZPA Gateway

            >>> update_gateway, _, error = client.zia.zpa_gateway.update_gateway(
            ... gateway_id=18423896
            ... name=f"NewGateway_{random.randint(1000, 10000)}",
            ... description=f"NewGateway_{random.randint(1000, 10000)}",
            ... zpa_server_group={
            ...     "name": "App_Segment_IP_Source_Anchoring2",
            ...     "external_id": "72058304855090128"
            ... },
            ... zpa_app_segments=[
            ... {
            ...      "name": "App_Segment_IP_Source_Anchoring1",
            ...      "external_id": "72058304855090129"
            ...  }
            ... ])
            ... if error:
            ...     print(f"Error updating gateway: {error}")
            ...     return
            ... print(f"Gateway updated successfully: {update_gateway.as_dict()}")
        """

        if not zpa_server_group:
            return (None, None, ValueError("zpa_server_group is required"))
        if not zpa_app_segments:
            return (None, None, ValueError("zpa_app_segments is required"))

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /zpaGateways/{gateway_id}
        """
        )

        body = {
            "id": gateway_id,  # ← this is the key fix
            "type": "ZPA",
            "zpaServerGroup": zpa_server_group,
            "zpaAppSegments": zpa_app_segments,
        }
        body.update(kwargs)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ZPAGateway)
        if error:
            return (None, response, error)

        try:
            result = ZPAGateway(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_gateway(self, gateway_id) -> tuple:
        """
        Deletes the specified ZPA Gateway.

        Args:
            gateway_id (str): The unique identifier of the ZPA Gateway that will be deleted.

        Returns:
            :obj:`int`: The response code for the request.

        Examples
            >>> _, _, error = client.zia.zpa_gateway.delete_gateway(gateway_id=18423896)
            ... if error:
            ...     print(f"Error deleting zpa gateway: {error}")
            ...     return
            ... print(f"Rule with ID {updated_gateway.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /zpaGateways/{gateway_id}
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
