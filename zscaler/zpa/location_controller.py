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
from zscaler.zpa.models.common import CommonIDName, LocationGroupDTO
from zscaler.utils import format_url
from zscaler.types import APIResult


class LocationControllerAPI(APIClient):
    """
    A Client object for the Location Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def get_location_summary(self, query_params: Optional[dict] = None) -> APIResult[List[CommonIDName]]:
        """
           Get all Location ID and names configured for a given customer.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            :obj:`Tuple`: A tuple containing (list of ExtranetResource instances, Response, error)

        Examples:
            >>> location_list, _, err = client.zpa.location_controller.get_location_summary(
            ... query_params={'search': 'Location01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing locations: {err}")
            ...     return
            ... print(f"Total locations found: {len(location_list)}")
            ... for location in location_list:
            ...     print(location.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /location/summary
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CommonIDName)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CommonIDName(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_location_extranet_resource(self, zpn_er_id: str, query_params: Optional[dict] = None) -> APIResult[dict]:
        """
        Gets information on the specified location extranet resource.

        Args:
            zpn_er_id (str): The unique identifier of the ZPN extranet resource.

            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.fetch_sub_locations]`` {bool}: Fetch sub-locations for the specified location.

        Returns:
            :obj:`Tuple`: ExtranetResource: The corresponding location extranet resource object.

        Example:
            Retrieve details of a specific extranet resource

            >>> fetched_extranet_resource, _, err = client.zpa.location_controller.get_location_extranet_resource('999999')
            ... if err:
            ...     print(f"Error fetching location extranet resource by ID: {err}")
            ...     return
            ... print(f"Fetched location extranet resource by ID: {fetched_extranet_resource.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /location/extranetResource/{zpn_er_id}
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CommonIDName)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CommonIDName(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_location_group_extranet_resource(
        self, zpn_er_id: str, query_params: Optional[dict] = None
    ) -> APIResult[List[LocationGroupDTO]]:
        """
        Get information about location groups associated with a specific extranet resource.

        This endpoint retrieves a paginated list of location groups that are associated
        with the specified extranet resource. Each location group includes its associated
        ZIA locations (ziaLocations).

        Args:
            zpn_er_id (str): The unique identifier of the ZPN extranet resource.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.

                ``[query_params.is_special_location_group_included]`` {bool}: Include special location groups in the response.

        Returns:
            :obj:`Tuple`: A tuple containing (list of LocationGroupDTO instances, Response, error).
                Each LocationGroupDTO includes:
                - id: The unique identifier of the location group
                - name: The name of the location group
                - zia_locations: List of ZIA locations associated with the location group

        Examples:
            Get location groups for an extranet resource:

            >>> location_groups, _, err = (
            ...     client.zpa.location_controller.get_location_group_extranet_resource(
            ...         '72058304855108633'
            ...     )
            ... )
            ... if err:
            ...     print(f"Error fetching location groups: {err}")
            ...     return
            ... print(f"Total location groups found: {len(location_groups)}")
            ... for group in location_groups:
            ...     print(f"Group: {group.name} (ID: {group.id})")
            ...     print(f"  ZIA Locations: {len(group.zia_locations)}")
            ...     for location in group.zia_locations:
            ...         print(f"    - {location.name} (ID: {location.id})")

            Get location groups with pagination and search:

            >>> location_groups, _, err = client.zpa.location_controller.get_location_group_extranet_resource(
            ...     '72058304855108633',
            ...     query_params={
            ...         'page': '1',
            ...         'page_size': '100',
            ...         'search': 'Extranet',
            ...         'is_special_location_group_included': True
            ...     }
            ... )
            ... if err:
            ...     print(f"Error fetching location groups: {err}")
            ...     return
            ... for group in location_groups:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /locationGroup/extranetResource/{zpn_er_id}
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LocationGroupDTO)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(LocationGroupDTO(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
