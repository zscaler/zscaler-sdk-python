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
from zscaler.zia.models.traffic_static_ip import TrafficStaticIP
from zscaler.utils import format_url


class TrafficStaticIPAPI(APIClient):
    """
    A Client object for the Traffic Forwarding Static IP resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_static_ips(self, query_params=None) -> tuple:
        """
        Returns the list of all configured static IPs.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Page size for pagination.

                ``[query_params.available_for_gre_tunnel]`` {bool}: The type of VPN credential.
                    Must be one of 'CN', 'IP', 'UFQDN', 'XAUTH'.

                ``[query_params.ip_address]`` {str}: Include VPN credential only if not associated with any location.

        Returns:
            tuple: A tuple containing (list of the configured static IPs instances, Response, error)

        Examples:
            List static IPs using default settings:

            >>> for ip_address in zia.traffic.list_static_ips():
            ...    print(ip_address)

            List static IPs, limiting to a maximum of 10 items:

            >>> for ip_address in zia.traffic.list_static_ips(max_items=10):
            ...    print(ip_address)

            List static IPs, returning 200 items per page for a maximum of 2 pages:

            >>> for ip_address in zia.traffic.list_static_ips(page_size=200, max_pages=2):
            ...    print(ip_address)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /staticIP
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
                result.append(TrafficStaticIP(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_static_ip(self, static_ip_id: int) -> tuple:
        """
        Returns information for the specified static IP.

        Args:
            static_ip_id (str):
                The unique identifier for the static IP.

        Returns:
            :obj:`dict`: The resource record for the static IP

        Examples:
            >>> static_ip = zia.traffic.get_static_ip('967134')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /staticIP/{static_ip_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TrafficStaticIP)

        if error:
            return (None, response, error)

        try:
            result = TrafficStaticIP(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_static_ip(self, **kwargs) -> tuple:
        """
        Adds a new static IP.

        Args:
            ip_address (str):
                The static IP address

        Keyword Args:
            **comment (str):
                Additional information about this static IP address.
            **geo_override (bool):
                If not set, geographic coordinates and city are automatically determined from the IP address.
                Otherwise, the latitude and longitude coordinates must be provided.
            **routable_ip (bool):
                Indicates whether a non-RFC 1918 IP address is publicly routable. This attribute is ignored if there
                is no ZIA Private Service Edge associated to the organization.
            **latitude (float):
                Required only if the geoOverride attribute is set. Latitude with 7 digit precision after
                decimal point, ranges between -90 and 90 degrees.
            **longitude (float):
                Required only if the geoOverride attribute is set. Longitude with 7 digit precision after decimal
                point, ranges between -180 and 180 degrees.

        Returns:
            :obj:`tuple`: The resource record for the newly created static IP.

        Examples:
            Add a new static IP address:

            >>> added_static_ip, response, error = client.zia.traffic_static_ip.add_static_ip(
            ...     comment=f"NewStaticIP {random.randint(1000, 10000)}",
            ...     ip_address="200.201.203.204",
            ... )
            ... if err:
            ...     print(f"Error adding static_ip: {err}")
            ...     return
            ... print(f"static_ip added successfully: {added_static_ip.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /staticIP
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

        response, error = self._request_executor.execute(request, TrafficStaticIP)
        if error:
            return (None, response, error)

        try:
            result = TrafficStaticIP(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_static_ip(self, static_ip_id: int, **kwargs) -> tuple:
        """
        Updates information relating to the specified static IP.

        Args:
            static_ip_id (str): The unique identifier for the static IP
            static_ip (dict): The updated static IP data

        Returns:
            :obj:`tuple`: The updated static IP resource record.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /staticIP/{static_ip_id}
        """
        )

        # Fetch the current static IP data
        current_ip, _, err = self.get_static_ip(static_ip_id)
        if err:
            return (None, None, err)

        body = {}

        body.update(kwargs)

        # Ensure the current IP address is included in the update payload
        body["ip_address"] = current_ip.ip_address

        # Validation: Ensure the IP address is not being updated
        if body["ip_address"] != current_ip.ip_address:
            return (None, None, ValueError("The IP address cannot be updated once it is set."))

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, TrafficStaticIP)
        if error:
            return (None, response, error)

        try:
            result = TrafficStaticIP(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_static_ip(self, static_ip_id: int) -> tuple:
        """
        Delete the specified static IP.

        Args:
            static_ip_id (int):
                The unique identifier for the static IP.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zia.traffic.delete_static_ip('972494')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""{
            self._zia_base_endpoint}
            /staticIP/{static_ip_id}
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

    def check_static_ip(self, ip_address: str) -> tuple:
        """
        Validates if a static IP object is correct.

        Args:
            ip_address (str): The static IP address.

        Returns:
            tuple: (True, None, None) if the static IP provided is valid and response is "SUCCESS".
                   (False, response, error) if the IP is invalid or if there's an error.

        Examples:
            >>> success, _, _ = zia.traffic.check_static_ip(ip_address='203.0.113.11')
            >>> if success:
            >>>     print("IP is valid.")
            >>> else:
            >>>     print("IP is invalid or already exists.")
        """
        # Define the HTTP method and API endpoint
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /staticIP/validate
        """
        )

        # Create the payload with the IP address
        payload = {"ipAddress": ip_address}

        # Create the request
        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, body=payload)

        if error:
            return (False, None, error)

        # ✅ Tell the executor to return the raw response so we can manually parse text
        raw_response, error = self._request_executor.execute(request, return_raw_response=True)

        if error:
            return (False, raw_response, error)

        try:
            body = raw_response.text.strip()
            if raw_response.status_code == 200 and body.upper() == "SUCCESS":
                return (True, None, None)
            else:
                return (False, raw_response, None)
        except Exception as ex:
            return (False, raw_response, ex)
