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
from zscaler.zcon.models.location_management import LocationManagement
from zscaler.utils import format_url

class LocationManagementAPI(APIClient):
    """
    A Client object for the Admin and Role resource.
    """

    _zcon_base_endpoint = "/zcon/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_locations(self, query_params=None) -> tuple:
        """
        Returns a list of locations.

        Keyword Args:
            query_params {dict}: Optional query parameters.
            
                ``[query_params.page]`` {int}: Specifies the page offset.
                
                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 100, but the maximum size is 1000.
                
                ``[query_params.state]`` {str}: Filter based on geographical state for a location.
                
                ``[query_params.xff_enabled]`` {bool}: Filter based on whether Enforce XFF Forwarding is enabled for a location.
                
                ``[query_params.auth_required]`` {bool}: Filter based on whether Enforce Authentication is enabled for a location.
                
                ``[query_params.bw_enforced]`` {bool}: Filter based on whether Bandwith Control is enforced for a location.
                
                ``[query_params.partner_id]`` {bool}: Not applicable to Cloud & Branch Connector.
                
                ``[query_params.enforce_aup]`` {bool}: Filter based on whether Acceptable Use Policy (AUP) is enforced for a location.
                
                ``[query_params.enable_firewall]`` {bool}: Filter based on whether firewall is enabled for a location.
                
                ``[query_params.location_type]`` {bool}: Filter based on type of location.
                    Supported values: `NONE`, `CORPORATE`, `SERVER`, `GUESTWIFI`, `IOT`, `WORKLOAD`

        Returns:
            :obj:`Tuple`: List of configured locations.

        Examples:
            List locations using default settings:

            >>> for location in zcon.locations.list_locations():
            ...    print(location)

            List locations, limiting to a maximum of 10 items:

            >>> for location in zcon.locations.list_locations(max_items=10):
            ...    print(location)

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zcon.locations.list_locations(page_size=200, max_pages=2):
            ...    print(location)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcon_base_endpoint}
            /location
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
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
                result.append(LocationManagement(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_location(self, location_id: int) -> tuple:
        """
        Returns information for the specified location based on the location id or location name.

        Args:
            location_id (int): The unique identifier for the location.

        Returns:
           tuple: A tuple containing (Location instance, Response, error).

        Examples:
            >>> location = zia.locations.get_location('97456691')

            >>> location = zia.locations.get_location_name(name='stockholm_office')
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcon_base_endpoint}
            /location/{location_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LocationManagement)

        if error:
            return (None, response, error)

        try:
            result = LocationManagement(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_locations_lite(self, query_params=None) -> tuple:
        """
        Returns only the name and ID of all configured locations.

        Keyword Args:
            query_params {dict}: Optional query parameters.
            
                ``[query_params.page]`` {int}: Specifies the page offset.
                
                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 100, but the maximum size is 1000.

                ``[query_params.search]`` {str}: The search string used to partially match against the location name and port attributes.

                ``[query_params.group_id]`` {int}: Filter based on location group ID for a location.

                ``[query_params.partner_id]`` {int}: Not applicable to Cloud & Branch Connector.

                ``[query_params.version]`` {int}: Not applicable to Cloud & Branch Connector.

                ``[query_params.include_sub_locations]`` {bool}: If set to true, sub-locations are included in the response.

                ``[query_params.include_parent_locations]`` {bool}: If set to true, parent locations (i.e., locations with sub-locations) are included in the response.

                ``[query_params.include_default_location]`` {bool}: If set to true, default location is included in response.

        Returns:
            :obj:`Tuple`: A list of configured locations.

        Examples:
            List locations with default settings:

            >>> for location in zia.locations.list_locations_lite():
            ...    print(location)

            List locations, limiting to a maximum of 10 items:

            >>> for location in zia.locations.list_locations_lite(max_items=10):
            ...    print(location)

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zia.locations.list_locations_lite(page_size=200, max_pages=2):
            ...    print(location)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcon_base_endpoint}
            /location/lite
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(
                    LocationManagement(
                        self.form_response_body(item))
                    )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

