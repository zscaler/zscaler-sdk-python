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
from zscaler.zia.models.gre_tunnels import TrafficGRETunnel
from zscaler.zia.models.gre_recommended_list import TrafficGRERecommendedVIP
from zscaler.zia.models.gre_vips import TrafficVips
from zscaler.zia.models.gre_tunnel_info import GreTunnelInfo
from zscaler.zia.models.gre_vips import GroupByDatacenter

from zscaler.utils import format_url


class TrafficForwardingGRETunnelAPI(APIClient):
    """
    A Client object for the Traffic Forwarding  GRE Tunnel resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_gre_tunnels(self, query_params=None) -> tuple:
        """
        Returns the list of all configured GRE tunnels.

        Keyword Args:
                ``[query_params.page]`` {int, optional}: Specifies the page size. The default size is 100, but the maximum size is 1000.
                ``[query_params.page_size]`` {int, optional}: Specifies the page size. The default size is 100, but the maximum size is 1000.
                
        Returns:
            :obj:`Tuple`: A list of GRE tunnels configured in ZIA.

        Examples:
            List configured GRE tunnels with default settings:

        >>> tunnels_list, _, err = client.zia.gre_tunnel.list_gre_tunnels(
            query_params={'page': 1, 'page_size': 100}
        )
        ... if err:
        ...     print(f"Error listing tunnels: {err}")
        ...     return
        ... for tunnel in tunnels_list:
        ...     print(tunnel.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /greTunnels
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TrafficGRETunnel(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_gre_tunnel(self, tunnel_id: int) -> tuple:
        """
        Returns information for the specified GRE tunnel.

        Args:
            tunnel_id (str):
                The unique identifier for the GRE tunnel.

        Returns:
            :obj:`tuple`: The GRE tunnel resource record.

        Examples:
        >>> tunnel, _, err = client.zia.gre_tunnel.get_gre_tunnel('4190936')
        ... if err:
        ...     print(f"Error fetching tunnel by ID: {err}")
        ...     return
        ... print(f"Fetched tunnel by ID: {tunnel.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /greTunnels/{tunnel_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, TrafficGRETunnel)

        if error:
            return (None, response, error)

        try:
            result = TrafficGRETunnel(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_gre_tunnel(
        self,
        **kwargs,
    ) -> tuple:
        """
        Add a new GRE tunnel.

        Note: If the `primary_dest_vip_id` and `secondary_dest_vip_id` aren't specified then the closest recommended
        VIPs will be automatically chosen.

        Args:
            source_ip (str):
                The source IP address of the GRE tunnel. This is typically a static IP address in the organisation
                or SD-WAN.
            primary_dest_vip_id (str):
                The unique identifier for the primary destination virtual IP address (VIP) of the GRE tunnel.
                Defaults to the closest recommended VIP.
            secondary_dest_vip_id (str):
                The unique identifier for the secondary destination virtual IP address (VIP) of the GRE tunnel.
                Defaults to the closest recommended VIP that isn't in the same city as the primary VIP.

        Keyword Args:
             **comment (str):
                Additional information about this GRE tunnel
             **ip_unnumbered (bool):
                This is required to support the automated SD-WAN provisioning of GRE tunnels, when set to true
                gre_tun_ip and gre_tun_id are set to null
             **internal_ip_range (str):
                The start of the internal IP address in /29 CIDR range.
             **within_country (bool):
                Restrict the data center virtual IP addresses (VIPs) only to those within the same country as the
                source IP address.

        Returns:
            :obj:`tuple`: The resource record for the newly created GRE tunnel.

        Examples:
            Add a GRE tunnel with closest recommended VIPs:

            >>> zia.traffic.add_gre_tunnel('203.0.113.10')

            Add a GRE tunnel with explicit VIPs:

            >>> zia.traffic.add_gre_tunnel('203.0.113.11',
            ...    primary_dest_vip_id='88088',
            ...    secondary_dest_vip_id='54590',
            ...    comment='GRE Tunnel for Manufacturing Plant')

        """
        # Define the HTTP method and API endpoint
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /greTunnels
        """
        )

        body = kwargs

        if "source_ip" in body and "sourceIp" not in body:
            body["sourceIp"] = body.pop("source_ip")

        # Auto-select closest VIPs if not provided in the payload
        if "primaryDestVip" not in body or "secondaryDestVip" not in body:
            recommended_vips = self.get_closest_diverse_vip_ids(body["sourceIp"])
            body["primaryDestVip"] = {"id": recommended_vips[0]}
            body["secondaryDestVip"] = {"id": recommended_vips[1]}

        # Create the request
        request, error = self._request_executor\
            .create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.\
            execute(request, TrafficGRETunnel)
        if error:
            return (None, response, error)

        try:
            result = TrafficGRETunnel(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_gre_tunnel(
        self, 
        tunnel_id: str,
        **kwargs
    ) -> tuple:
        """
        Update an existing GRE tunnel.

        Args:
            tunnel_id (str): The unique identifier for the GRE tunnel.
            source_ip (str):
                The source IP address of the GRE tunnel. This is typically a static IP address in the organisation
                or SD-WAN.
            primary_dest_vip_id (str):
                The unique identifier for the primary destination virtual IP address (VIP) of the GRE tunnel.
                Defaults to the closest recommended VIP.
            secondary_dest_vip_id (str):
                The unique identifier for the secondary destination virtual IP address (VIP) of the GRE tunnel.
                Defaults to the closest recommended VIP that isn't in the same city as the primary VIP.

        Keyword Args:
             **comment (str):
                Additional information about this GRE tunnel
             **ip_unnumbered (bool):
                This is required to support the automated SD-WAN provisioning of GRE tunnels, when set to true
                gre_tun_ip and gre_tun_id are set to null
             **internal_ip_range (str):
                The start of the internal IP address in /29 CIDR range.
             **within_country (bool):
                Restrict the data center virtual IP addresses (VIPs) only to those within the same country as the
                source IP address.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /greTunnels/{tunnel_id}
        """
        )

        if tunnel_id is None:
            raise ValueError("tunnel_id is a required parameter for updating a GRE tunnel.")

        body = kwargs

        if "source_ip" in body and "sourceIp" not in body:
            body["sourceIp"] = body.pop("source_ip")

        # Auto-select closest VIPs if not provided in the payload
        if "primaryDestVip" not in body or "secondaryDestVip" not in body:
            recommended_vips = self.get_closest_diverse_vip_ids(body["sourceIp"])
            body["primaryDestVip"] = {"id": recommended_vips[0]}
            body["secondaryDestVip"] = {"id": recommended_vips[1]}

        request, error = self._request_executor\
            .create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, TrafficGRETunnel)
        if error:
            return (None, response, error)

        try:
            result = TrafficGRETunnel(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_gre_tunnel(self, tunnel_id: int) -> tuple:
        """
        Delete the specified GRE Tunnel.

        Args:
            tunnel_id (int):
                The unique identifier for the GRE Tunnel.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            >>> zia.traffic.delete_gre_tunnel('972494')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /greTunnels/{tunnel_id}
        """
        )

        params = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)

    def list_gre_ranges(self, query_params=None) -> tuple:
        """
        Returns a list of available GRE tunnel ranges.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.internal_ip_range]`` {int}: Internal IP range information.
                ``[query_params.static_ip]`` {str}: Search string for filtering Static IP information.
                ``[query_params.limit]`` {int}: The maximum number of GRE tunnel IP ranges that can be added.

        Returns:
            tuple: List of configured gre .

        Examples:
            >>> gre_tunnel_ranges = zia.traffic.list_gre_ranges()
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /greTunnels/availableInternalIpRanges
            """
        )

        query_params = query_params or {}

        body = {}
        headers = {}
        
        request, error = self._request_executor\
             .create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = response.get_results()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_vips_recommended(
        self,
        query_params=None
    ) -> tuple:
        """
        Returns a list of recommended virtual IP addresses (VIPs) based on parameters.

        Args:
            query_params (dict, optional): A dictionary of query parameters to filter results.

        Keyword Args:
            - **[query_params.routable_ip]** (bool, optional): The routable IP address. Default: `True`.
            - **[query_params.within_country_only]** (bool, optional): Search within country only. Default: `False`.
            - **[query_params.include_private_service_edge]** (bool, optional): The maximum number of GRE tunnel IP ranges that can be added.
            - **[query_params.include_current_vips]** (bool, optional): Include currently assigned VIPs. Default: `True`.
            - **[query_params.source_ip]** (str, optional): The source IP address.
            - **[query_params.latitude]** (str, optional): Latitude coordinate of GRE tunnel source.
            - **[query_params.longitude]** (str, optional): Longitude coordinate of GRE tunnel source.
            - **[query_params.geo_override]** (bool, optional): Override the geographic coordinates. Default: `False`.
            - **[query_params.sub_cloud]** (str, optional): The subcloud for the VIP.

        Returns:
            tuple: A tuple containing:

                - **list[TrafficGRERecommendedVIP]**: A list of recommended VIPs.
                - **Response**: The raw API response object.
                - **Error**: An error message, if applicable.

        Examples:
            Return recommended VIPs for a given source IP:

            >>> vips, response, err = zia.traffic.list_vips_recommended(source_ip='203.0.113.30')
            >>> for vip in vips:
            ...     pprint(vip)
        """

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /vips/recommendedList
        """
        )

        query_params = query_params or {}

        headers = {}
        body = {}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=body, headers=headers, params=query_params
        )

        if error:
            return (False, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (False, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TrafficGRERecommendedVIP(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_closest_diverse_vip_ids(self, ip_address: str) -> tuple:
        """
        Returns the closest diverse Zscaler destination VIPs for a given IP address.

        Args:
            ip_address (str):
                The IP address used for locating the closest diverse VIPs.

        Returns:
            :obj:`tuple`: Tuple containing the preferred and secondary VIP IDs.

        Examples:
            >>> closest_vips = zia.traffic.get_closest_diverse_vip_ids('203.0.113.20')

        """
        # Fetch the recommended VIPs
        vips_list, _, err = self.list_vips_recommended(query_params={'source_ip':ip_address})

        if err:
            raise ValueError(f"Error fetching recommended VIPs: {err}")

        if not vips_list:
            raise ValueError("No VIPs found for the given source IP.")

        # Find the preferred VIP (first entry)
        preferred_vip = vips_list[0]  # First entry is closest VIP

        # Find the next closest VIP that is in a different city
        secondary_vip = next((vip for vip in vips_list if vip.city != preferred_vip.city), None)

        if not secondary_vip:
            raise ValueError("No diverse VIPs found in different cities.")

        # Return both VIP IDs
        recommended_vips = (preferred_vip.id, secondary_vip.id)

        return recommended_vips

    def list_vip_group_by_dc(
        self,
        # source_ip: str,
        query_params=None
    ) -> tuple:
        """
        Returns a list of recommended GRE tunnel (VIPs) grouped by data center.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.source_ip]`` {str}: The source IP address (required).
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.routable_ip]`` {bool}: The routable IP address. Default: True.
                ``[query_params.within_country_only]`` {bool}: Search within country only. Default: False.
                ``[query_params.include_private_service_edge]`` {bool}: Include ZIA Private Service Edge VIPs. Default: True.
                ``[query_params.include_current_vips]`` {bool}: Include currently assigned VIPs. Default: True.
                ``[query_params.latitude]`` {str}: Latitude coordinate of GRE tunnel source.
                ``[query_params.longitude]`` {str}: Longitude coordinate of GRE tunnel source.
                ``[query_params.geo_override]`` {bool}: Override the geographic coordinates. Default: False.

        Returns:
            tuple: A tuple containing (list of VIP groups by data center, Response, error)

        Examples:
            List VIP groups for a given source IP:

            >>> vip_groups, resp, err = zia.vips.list_vip_group_by_dc(query_params={"sourceIp": "203.0.113.30"})
            >>> for vip_group in vip_groups:
            ...    print(vip_group)

        """
        query_params = query_params or {}

        # Ensure sourceIp is provided in the query parameters
        # if "sourceIp" not in query_params:
        #     return (None, None, ValueError("sourceIp is a required query parameter."))

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /vips/groupByDatacenter
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(GroupByDatacenter(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_vips(self, query_params=None) -> tuple:
        """
        Returns a list of virtual IP addresses (VIPs) available in the Zscaler cloud.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.dc]`` {str}: Filter based on data center.
                ``[query_params.region]`` {str}: Filter based on region.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 100, but the maximum size is 1000.
                ``[query_params.include]`` {str}: Include all, private, or public VIPs in the list. Supported values: `all`, `private`, `public`
                ``[query_params.sub_cloud]`` {str}: Filter based on the subcloud for the VIP. 

        Returns:
            tuple: A tuple containing (list of VIPs, Response, error)

        Examples:
            List VIPs using default settings:

            >>> vips, response, err = zia.vips.list_vips()

            List VIPs, limiting to a maximum of 10 items:

            >>> vips, response, err = zia.vips.list_vips(query_params={"max_items": 10})

            List VIPs, returning 200 items per page for a maximum of 2 pages:

            >>> vips, response, err = zia.vips.list_vips(query_params={"page_size": 200, "max_pages": 2})
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /vips
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TrafficVips(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
    
    def get_ip_gre_tunnel_info(
        self,
        query_params=None
    ) -> tuple:
        """
        Returns information for the list of IP addresses with GRE tunnel details.

        Args:
            query_params (dict, optional): Optional query parameters.
                ``[query_params.ip_addresses]`` {list[int]}: Filter based on an IP address range.

        Returns:
            tuple: A tuple containing a list of GreTunnelInfo instances, Response, error.

        Example:
        >>> tunnels_list, _, err = client.zia.gre_tunnel.get_ip_gre_tunnel_info()
        ... if err:
        ...     print(f"Error listing tunnels: {err}")
        ...     return
        ... for tunnel in tunnels_list:
        ...     print(tunnel.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /orgProvisioning/ipGreTunnelInfo
        """
        )

        query_params = query_params or {}
        
        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)

        if error:
            return (None, response, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = [
                GreTunnelInfo(item) for item in response.get_body()
            ]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
