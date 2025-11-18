import json
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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.traffic_static_ip import TrafficStaticIP
from zscaler.utils import format_url
from zscaler.types import APIResult


class TrafficStaticIPAPI(APIClient):
    """
    A Client object for the Traffic Forwarding Static IP resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_static_ips(self, query_params: Optional[dict] = None) -> APIResult[List[TrafficStaticIP]]:
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

    def get_static_ip(self, static_ip_id: int) -> APIResult[dict]:
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

    def add_static_ip(self, **kwargs) -> APIResult[dict]:
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

    def update_static_ip(self, static_ip_id: int, **kwargs) -> APIResult[dict]:
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

    def delete_static_ip(self, static_ip_id: int) -> APIResult[dict]:
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

    def check_static_ip(self, ip_address: str) -> APIResult[dict]:
        """
        Validates if a static IP address can be added to the organization.

        This method checks if the provided IP address is available for use.
        The API returns plain text "SUCCESS" (HTTP 200) if the IP is available,
        or a JSON error (HTTP 409) if the IP already exists.

        Args:
            ip_address (str): The static IP address to validate.

        Returns:
            tuple: A tuple of (is_valid, response, error) where:
                - **is_valid=True, response=None, error=None**: IP is available (not in system)
                - **is_valid=False, response=raw_response, error=error_obj**: IP already exists (HTTP 409)
                - **is_valid=False, response=None, error=error_obj**: Network or request error

        Examples:
            Check if an IP address is available:

            >>> is_valid, _, err = client.zia.traffic_static_ip.check_static_ip('203.0.113.11')
            >>> if err:
            ...     print(f"Error: {err}")
            >>> elif is_valid:
            ...     print("IP is available - can be added")
            >>> else:
            ...     print("IP already exists in the organization")
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

        # Get raw response - this endpoint returns plain text "SUCCESS" for valid IPs
        raw_response, error = self._request_executor.execute(request, return_raw_response=True)

        # Check the actual HTTP status code, not the error object
        # The executor may return an "error" for non-JSON responses even on HTTP 200
        # When return_raw_response=True, we need to check the actual response status
        if raw_response is None:
            # True network/request error
            return (False, None, error)

        try:
            # Ensure we have a valid response object with status_code attribute
            if not hasattr(raw_response, 'status_code'):
                return (False, raw_response, error if error else "Invalid response object")

            status_code = raw_response.status_code
            body_text = raw_response.text.strip() if hasattr(raw_response, 'text') else ""

            # HTTP 200 with "SUCCESS" = IP is valid (not in system)
            # Important: Ignore any error that might have been set for non-JSON responses
            if status_code == 200 and body_text.upper() == "SUCCESS":
                return (True, None, None)

            # HTTP 409 = IP already exists (duplicate)
            # For 409, parse the JSON error from the response body
            elif status_code == 409:
                # Try to parse the error from the response body
                try:
                    if body_text:
                        error_data = json.loads(body_text)
                        # Create a structured error object if available
                        # Ensure status code is included in the error dict
                        if isinstance(error_data, dict):
                            structured_error = error_data.copy()
                            structured_error["status"] = 409
                        else:
                            structured_error = error
                    else:
                        structured_error = error
                except (json.JSONDecodeError, ValueError):
                    # If parsing fails, use the provided error or create a generic one
                    structured_error = error if error else {"status": 409, "message": "IP already exists"}

                return (False, raw_response, structured_error)

            # Any other response = invalid
            else:
                return (False, raw_response, error if error else f"Unexpected response: {status_code}")

        except Exception as ex:
            return (False, raw_response, ex)
