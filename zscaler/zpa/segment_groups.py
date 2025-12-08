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

from typing import List, Optional
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.segment_group import SegmentGroup
from zscaler.utils import format_url


class SegmentGroupsAPI(APIClient):
    """
    A client object for the Segment Groups resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_groups(self, query_params: Optional[dict] = None) -> List[SegmentGroup]:
        """
        Enumerates segment groups in your organization with pagination.
        A subset of segment groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            List[SegmentGroup]: A list of SegmentGroup instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Example:
            Fetch all segment groups without filtering:

            >>> try:
            ...     group_list = client.zpa.segment_groups.list_groups()
            ...     print(f"Total segment groups found: {len(group_list)}")
            ...     for group in group_list:
            ...         print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error listing segment groups: {e}")

            Fetch segment groups with query_params filters:

            >>> try:
            ...     group_list = client.zpa.segment_groups.list_groups(
            ...         query_params={'search': 'Group01', 'page': '1', 'page_size': '100'}
            ...     )
            ...     print(f"Total segment groups found: {len(group_list)}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/segmentGroup")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, SegmentGroup)

        return [SegmentGroup(self.form_response_body(item)) for item in response.get_results()]

    def get_group(self, group_id: str, query_params: Optional[dict] = None) -> SegmentGroup:
        """
        Gets information on the specified segment group.

        Args:
            group_id (str): The unique identifier of the segment group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            SegmentGroup: The corresponding segment group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Example:
            Retrieve details of a specific segment group:

            >>> try:
            ...     group = client.zpa.segment_groups.get_group('999999')
            ...     print(f"Fetched segment group: {group.as_dict()}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error fetching segment group: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/segmentGroup/{group_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, SegmentGroup)

        return SegmentGroup(self.form_response_body(response.get_body()))

    def add_group(self, **kwargs) -> SegmentGroup:
        """
        Adds a new segment group.

        Args:
            name (str): The name of the segment group.
            description (str): The description of the segment group.
            enabled (bool): Enable the segment group. Defaults to True.

        Returns:
            SegmentGroup: The created segment group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Example:
            Add a new segment group:

            >>> try:
            ...     group = client.zpa.segment_groups.add_group(
            ...         name="Example Group",
            ...         description="This is an example segment group.",
            ...         enabled=True
            ...     )
            ...     print(f"Created group: {group.as_dict()}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error creating group: {e}")

            Adding a new segment group for a specific microtenant:

            >>> try:
            ...     group = client.zpa.segment_groups.add_group(
            ...         name="Example Group",
            ...         description="Segment group for microtenant",
            ...         enabled=True,
            ...         microtenant_id="216196257331380392"
            ...     )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/segmentGroup")

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, SegmentGroup)

        return SegmentGroup(self.form_response_body(response.get_body()))

    def update_group(self, group_id: str, **kwargs) -> SegmentGroup:
        """
        Updates the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group being updated.

        Returns:
            SegmentGroup: The updated segment group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Example:
            Update an existing segment group:

            >>> try:
            ...     group = client.zpa.segment_groups.update_group(
            ...         "216196257331370181",
            ...         name="Updated Group Name",
            ...         description="Updated description",
            ...         enabled=False
            ...     )
            ...     print(f"Updated group: {group.as_dict()}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error updating group: {e}")

            Updating a segment group for a specific microtenant:

            >>> try:
            ...     group = client.zpa.segment_groups.update_group(
            ...         "216196257331370181",
            ...         name="Tenant-Specific Group Update",
            ...         enabled=True,
            ...         microtenant_id="216196257331380392"
            ...     )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/segmentGroup/{group_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, SegmentGroup)

        if response is None:
            return SegmentGroup({"id": group_id})

        return SegmentGroup(self.form_response_body(response.get_body()))

    def update_group_v2(self, group_id: str, **kwargs) -> SegmentGroup:
        """
        Updates the specified segment group using v2 API.

        Args:
            group_id (str): The unique identifier for the segment group being updated.

        Returns:
            SegmentGroup: The updated segment group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Example:
            Update an existing segment group:

            >>> try:
            ...     group = client.zpa.segment_groups.update_group_v2(
            ...         "216196257331370181",
            ...         name="Updated Group Name",
            ...         description="Updated description",
            ...         enabled=False
            ...     )
            ...     print(f"Updated group: {group.as_dict()}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error updating group: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint_v2}/segmentGroup/{group_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, SegmentGroup)

        if response is None:
            return SegmentGroup({"id": group_id})

        return SegmentGroup(self.form_response_body(response.get_body()))

    def delete_group(self, group_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group to be deleted.
            microtenant_id (str, optional): The microtenant ID, if applicable.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Example:
            Delete a segment group by ID:

            >>> try:
            ...     client.zpa.segment_groups.delete_group("216196257331370181")
            ...     print("Group deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error deleting group: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/segmentGroup/{group_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
