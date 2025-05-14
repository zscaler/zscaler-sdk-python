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

    def list_groups(self, query_params=None) -> tuple:
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
            :obj:`Tuple`: A tuple containing (list of SegmentGroup instances, Response, error)

        Example:
            Fetch all segment groups without filtering

            >>> group_list, _, err = client.zpa.segment_groups.list_groups()
            ... if err:
            ...     print(f"Error listing segment groups: {err}")
            ...     return
            ... print(f"Total segment groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Fetch segment groups with query_params filters
            >>> group_list, _, err = client.zpa.segment_groups.list_groups(
            ... query_params={'search': 'Group01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing segment groups: {err}")
            ...     return
            ... print(f"Total segment groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /segmentGroup
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SegmentGroup)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(SegmentGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_group(self, group_id: str, query_params=None) -> tuple:
        """
        Gets information on the specified segment group.

        Args:
            group_id (str): The unique identifier of the segment group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: SegmentGroup: The corresponding segment group object.

        Example:
            Retrieve details of a specific segment group

            >>> fetched_group, _, err = client.zpa.segment_groups.get_group('999999')
            ... if err:
            ...     print(f"Error fetching segment group by ID: {err}")
            ...     return
            ... print(f"Fetched segment group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /segmentGroup/{group_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SegmentGroup)
        if error:
            return (None, response, error)

        try:
            result = SegmentGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_group(self, **kwargs) -> tuple:
        """
        Adds a new segment group.

        Args:
            name (str): The name of the segment group.
            description (str): The description of the segment group.
            enabled (bool): Enable the segment group. Defaults to True.

        Returns:
            :obj:`Tuple`: SegmentGroup: The created segment group object.

        Example:
            # Basic example: Add a new segment group
            >>> added_group, _, err = client.zpa.segment_groups.add_group(
            ...     name="Example Group",
            ...     description="This is an example segment group.",
            ...     enabled=True
            ... )

            # Adding a new segment group for a specific microtenant
            >>> added_group, _, err = zpa.segment_groups.add_group(
            ...     name="Example Group",
            ...     description="Segment group for microtenant",
            ...     enabled=True,
            ...     microtenant_id="216196257331380392"
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /segmentGroup
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SegmentGroup)
        if error:
            return (None, response, error)

        try:
            result = SegmentGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_id: str, **kwargs) -> tuple:
        """
        Updates the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group being updated.

        Returns:
            :obj:`Tuple`: SegmentGroup: The updated segment group object.

        Example:
            # Basic example: Update an existing segment group
            >>> group_id = "216196257331370181"
            >>> updated_group, _, err = zpa.segment_groups.update_group(
            ...     group_id,
            ...     name="Updated Group Name",
            ...     description="Updated description for the segment group",
            ...     enabled=False
            ... )

            # Updating a segment group for a specific microtenant
            >>> group_id = "216196257331370181"
            >>> updated_group, _, err = zpa.segment_groups.update_group(
            ...     group_id,
            ...     name="Tenant-Specific Group Update",
            ...     description="Updated segment group for microtenant",
            ...     enabled=True,
            ...     microtenant_id="216196257331380392"
            ... )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /segmentGroup/{group_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SegmentGroup)
        if error:
            return (None, response, error)

        if response is None:
            return (SegmentGroup({"id": group_id}), None, None)

        try:
            result = SegmentGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group_v2(self, group_id: str, **kwargs) -> tuple:
        """
        Updates the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group being updated.

        Returns:
            :obj:`Tuple`: SegmentGroup: The updated segment group object.

        Example:
            # Basic example: Update an existing segment group
            >>> group_id = "216196257331370181"
            >>> updated_group, response, err = zpa.segment_groups.update_group_v2(
            ...     group_id,
            ...     name="Updated Group Name",
            ...     description="Updated description for the segment group",
            ...     enabled=False
            ... )

            # Updating a segment group for a specific microtenant
            >>> group_id = "216196257331370181"
            >>> updated_group, response, err = zpa.segment_groups.update_group_v2(
            ...     group_id,
            ...     name="Tenant-Specific Group Update",
            ...     description="Updated segment group for microtenant",
            ...     enabled=True,
            ...     microtenant_id="216196257331380392"
            ... )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /segmentGroup/{group_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SegmentGroup)
        if error:
            return (None, response, error)

        if response is None:
            return (SegmentGroup({"id": group_id}), None, None)

        try:
            result = SegmentGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group to be deleted.

        Returns:
            int: Status code of the delete operation.

        Example:
            # Delete a segment group by ID
            >>> _, _, err = client.zpa.segment_groups.delete_group(updated_group_v2.id)
            ... if err:
            ...     print(f"Error deleting group: {err}")
            ...     return
            ... print(f"Group with ID {updated_group_v2.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /segmentGroup/{group_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        return (None, response, error)
