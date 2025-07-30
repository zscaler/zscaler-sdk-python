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
from zscaler.zpa.models.c2c_ip_ranges import IpRanges
from zscaler.zpa.models.common import CommonFilterSearch
from zscaler.utils import format_url


class IPRangesAPI(APIClient):
    """
    A client object for the C2C IP Range Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}/v2"

    def list_ip_ranges(self) -> tuple:
        """
        Enumerates ip ranges in your organization with pagination.
        A subset of ip ranges can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (list of SegmentGroup instances, Response, error)

        Example:
            Fetch all ip ranges without filtering

            >>> group_list, _, err = client.zpa.segment_groups.list_groups()
            ... if err:
            ...     print(f"Error listing ip ranges: {err}")
            ...     return
            ... print(f"Total ip ranges found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Fetch ip ranges with query_params filters
            >>> group_list, _, err = client.zpa.segment_groups.list_groups(
            ... query_params={'search': 'Group01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing ip ranges: {err}")
            ...     return
            ... print(f"Total ip ranges found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /ipRanges
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IpRanges)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(IpRanges(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ip_range(self, range_id: str) -> tuple:
        """
        Gets information on the specified ip range.

        Args:
            range_id (str): The unique identifier of the ip range.

        Returns:
            :obj:`Tuple`: IpRanges: The corresponding ip range object.

        Example:
            Retrieve details of a specific ip range

            >>> fetched_range, _, err = client.zpa.c2c_ip_ranges.get_ip_range('999999')
            ... if err:
            ...     print(f"Error fetching ip range by ID: {err}")
            ...     return
            ... print(f"Fetched ip range by ID: {fetched_range.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /ipRanges/{range_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IpRanges)
        if error:
            return (None, response, error)

        try:
            result = IpRanges(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_ip_range(self, **kwargs) -> tuple:
        """
        Adds a new ip range.

        Args:
            name (str): The name of the ip range.
            description (str): The description of the ip range.
            enabled (bool): Enable the ip range. Defaults to True.
            ip_range_begin (str): The starting IP address of the range.
            ip_range_end (str): The ending IP address of the range.
            subnet_cidr (str): The subnet CIDR notation for the IP range.
            location (str): The location description for the IP range.
            location_hint (str): A hint about the location of the IP range.
            country_code (str): The country code for the IP range location.
            latitude_in_db (float): The latitude coordinate stored in the database.
            longitude_in_db (float): The longitude coordinate stored in the database.
            sccm_flag (bool): Whether the IP range is flagged for SCCM.
            available_ips (int): The number of available IP addresses in the range.
            total_ips (int): The total number of IP addresses in the range.
            used_ips (int): The number of used IP addresses in the range.

        Returns:
            :obj:`Tuple`: IpRanges: The created ip range object.

        Example:
            # Basic example: Add a new ip range
            >>> added_range, _, err = client.zpa.c2c_ip_ranges.add_ip_range(
            ...     name=f"NewIPRange_{random.randint(1000, 10000)}",
            ...     description=f"NewIPRange_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     location_hint= "Created via Python SDK",
            ...     ip_range_begin= "192.168.1.1",
            ...     ip_range_end= "192.168.1.254",
            ...     location=       "San Jose, CA, USA",
            ...     country_code=   "US",
            ...     latitude_in_db=  "37.33874",
            ...     longitude_in_db= "-121.8852525",
            ... )
            >>> if err:
            ...     print(f"Error adding ip range: {err}")
            ...     return
            ... print(f"ip range added successfully: {added_range.as_dict()}")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /ipRanges
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IpRanges)
        if error:
            return (None, response, error)

        try:
            result = IpRanges(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_ip_range(self, range_id: str, **kwargs) -> tuple:
        """
        Updates the specified ip range.

        Args:
            range_id (str): The unique identifier for the ip range being updated.
            name (str): The name of the ip range.
            description (str): The description of the ip range.
            enabled (bool): Enable the ip range. Defaults to True.
            ip_range_begin (str): The starting IP address of the range.
            ip_range_end (str): The ending IP address of the range.
            subnet_cidr (str): The subnet CIDR notation for the IP range.
            location (str): The location description for the IP range.
            location_hint (str): A hint about the location of the IP range.
            country_code (str): The country code for the IP range location.
            latitude_in_db (float): The latitude coordinate stored in the database.
            longitude_in_db (float): The longitude coordinate stored in the database.
            sccm_flag (bool): Whether the IP range is flagged for SCCM.
            available_ips (int): The number of available IP addresses in the range.
            total_ips (int): The total number of IP addresses in the range.
            used_ips (int): The number of used IP addresses in the range.

        Returns:
            :obj:`Tuple`: SegmentGroup: The updated ip range object.

        Example:
            Update an existing ip range

            >>> range_id = "216196257331370181"
            >>> updated_range, _, err = client.zpa.c2c_ip_ranges.update_ip_range(
            ...     range_id,
            ...     name=f"UpdatedIPRange_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedIPRange_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     location_hint= "Updated via Python SDK",
            ...     ip_range_begin= "192.168.2.1",
            ...     ip_range_end= "192.168.2.254",
            ...     location=       "San Francisco, CA, USA",
            ...     country_code=   "US",
            ...     latitude_in_db=  "37.7749",
            ...     longitude_in_db= "-122.4194",
            ... )
            >>> if err:
            ...     print(f"Error updating ip range: {err}")
            ...     return
            ... print(f"ip range updated successfully: {updated_range.as_dict()}")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /ipRanges/{range_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IpRanges)
        if error:
            return (None, response, error)

        if response is None:
            return (IpRanges({"id": range_id}), None, None)

        try:
            result = IpRanges(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_ip_range(self, range_id: str) -> tuple:
        """
        Deletes the specified ip range.

        Args:
            range_id (str): The unique identifier for the ip range to be deleted.

        Returns:
            int: Status code of the delete operation.

        Example:
            Delete a ip range by ID

            >>> _, _, err = client.zpa.c2c_ip_ranges.delete_ip_range(72058304855141483)
            ... if err:
            ...     print(f"Error deleting ip range: {err}")
            ...     return
            ... print(f"IP Range with ID {72058304855141483} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /ipRanges/{range_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        return (None, response, error)

    def get_ip_range_search(self, **kwargs) -> tuple:
        """
        Gets the IP range by page and pageSize for the specified customer based on given filters.

        Args:
            **kwargs: Keyword arguments that define search filters, pagination, and sorting criteria.

        Keyword Args:
            filter_and_sort_dto (dict): A dictionary containing filtering, pagination, and sorting information.

                - **filter_by** (list): A list of filter condition dictionaries.

                    - **filter_name** (str): The name of the field to filter on (e.g., `name`, `criteria_attribute_values`).
                    - **operator** (str): The logical operator (e.g., `EQUALS`, `LIKE`).
                    - **values** (list): A list of values to match.
                    - **comma_sep_values** (str, optional): Optional comma-separated string version of values.

                - **page_by** (dict, optional): Dictionary containing pagination configuration.

                    - **page** (int): The current page number.
                    - **page_size** (int): The number of records per page.
                    - **valid_page** (int, optional): Optional page validation flag.
                    - **valid_page_size** (int, optional): Optional page size validation flag.

                - **sort_by** (dict, optional): Dictionary defining sorting options.

                    - **sort_name** (str): The name of the field to sort by (e.g., `name`).
                    - **sort_order** (str): Sorting direction (e.g., `ASC` or `DESC`).

        Returns:
            tuple: A tuple containing:

                - **CommonFilterSearch**: The parsed response object containing filter results, paging, and sorting.
                - **Response**: The raw response object returned by the request executor.
                - **Error**: An exception if one occurred, otherwise `None`.

        Example:
            >>> search_payload = {
            ...     "filter_and_sort_dto": {
            ...         "filter_by": [
            ...             {
            ...                 "filter_name": "criteria_attribute_values",
            ...                 "operator": "LIKE",
            ...                 "values": ["Test"]
            ...             }
            ...         ],
            ...         "page_by": {
            ...             "page": 1,
            ...             "page_size": 20
            ...         },
            ...         "sort_by": {
            ...             "sort_name": "name",
            ...             "sort_order": "ASC"
            ...         }
            ...     }
            ... }
            >>> result, _, err = client.zpa.c2c_ip_ranges.get_ip_range_search(**search_payload)
            >>> if err:
            ...     print(f"Error searching ip range: {err}")
            ... else:
            ...     for item in result.filter_by:
            ...         print(item.request_format())
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /ipRanges/search
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CommonFilterSearch)
        if error:
            return (None, response, error)

        try:
            result = CommonFilterSearch(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
