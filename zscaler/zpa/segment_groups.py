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
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zpa.models.segment_group import SegmentGroup


class SegmentGroupsAPI(APIClient):
    """
    A Client object for the Segment Groups resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_groups(self, query_params: Optional[dict] = None) -> APIResult[List[SegmentGroup]]:
        """
        Lists the segment groups configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            tuple: A tuple containing (list of SegmentGroup instances, Response, error)

        Examples:
            List segment groups:

            >>> group_list, _, error = client.zpa.segment_groups.list_groups()
            >>> if error:
            ...     print(f"Error listing segment groups: {error}")
            ...     return
            ... print(f"Total segment groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            List segment groups using filters:

            >>> group_list, _, error = client.zpa.segment_groups.list_groups(
            ...     query_params={'page': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing segment groups: {error}")
            ...     return
            ... print(f"Total segment groups found: {len(group_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /segmentGroup
        """)

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

    def get_group(self, group_id: str, query_params: Optional[dict] = None) -> APIResult[SegmentGroup]:
        """
        Fetches a specific segment group by ID.

        Args:
            group_id (str): The unique identifier for the segment group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (SegmentGroup instance, Response, error).

        Examples:
            Print a specific segment group:

            >>> fetched_group, _, error = client.zpa.segment_groups.get_group('216196257331370181')
            >>> if error:
            ...     print(f"Error fetching segment group by ID: {error}")
            ...     return
            ... print(f"Fetched segment group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /segmentGroup/{group_id}
        """)

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

    def add_group(self, **kwargs) -> APIResult[SegmentGroup]:
        """
        Creates a new segment group.

        Args:
            name (str): The name of the segment group.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the segment group.
            enabled (bool): Indicates whether the segment group is enabled.
            policy_migrated (str): The policy migrated for this segment group.
            config_space (str): The config space for this segment group.
            tcp_keep_alive_enabled (str): The tcp keep alive enabled for this segment group.
            microtenant_name (str): The microtenant name for this segment group.
            skip_detailed_app_info (str): The skip detailed app info for this segment group.
            applications (str): The applications for this segment group.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            tuple: A tuple containing the newly added SegmentGroup instance, response, and error.

        Examples:
            Add a new segment group:

            >>> added_group, _, error = client.zpa.segment_groups.add_group(
            ...     name=f"NewGroup_{random.randint(1000, 10000)}",
            ...     description=f"NewGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding segment group: {error}")
            ...     return
            ... print(f"Segment group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /segmentGroup
        """)

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

    def update_group(self, group_id: str, **kwargs) -> APIResult[SegmentGroup]:
        """
        Updates information for the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group.

        Keyword Args:
            name (str): The name of the segment group.
            description (str): Additional information about the segment group.
            enabled (bool): Indicates whether the segment group is enabled.
            policy_migrated (str): The policy migrated for this segment group.
            config_space (str): The config space for this segment group.
            tcp_keep_alive_enabled (str): The tcp keep alive enabled for this segment group.
            microtenant_name (str): The microtenant name for this segment group.
            skip_detailed_app_info (str): The skip detailed app info for this segment group.
            applications (str): The applications for this segment group.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            tuple: A tuple containing the updated SegmentGroup instance, response, and error.

        Examples:
            Update an existing segment group:

            >>> updated_group, _, error = client.zpa.segment_groups.update_group(
            ...     group_id='216196257331370181',
            ...     name=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating segment group: {error}")
            ...     return
            ... print(f"Segment group updated successfully: {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /segmentGroup/{group_id}
        """)

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

        # Handle 204 No Content - response exists but body is empty
        if response is None or not response.get_body():
            return (SegmentGroup({"id": group_id}), response, None)

        try:
            result = SegmentGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group_v2(self, group_id: str, **kwargs) -> APIResult[SegmentGroup]:
        """
        Updates the specified segment group (v2 endpoint).

        Args:
            group_id (str): The unique identifier for the segment group.

        Keyword Args:
            name (str): The name of the segment group.
            description (str): Additional information about the segment group.
            enabled (bool): Indicates whether the segment group is enabled.
            policy_migrated (str): The policy migrated for this segment group.
            config_space (str): The config space for this segment group.
            tcp_keep_alive_enabled (str): The tcp keep alive enabled for this segment group.
            microtenant_name (str): The microtenant name for this segment group.
            skip_detailed_app_info (str): The skip detailed app info for this segment group.
            applications (str): The applications for this segment group.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            tuple: A tuple containing the updated SegmentGroup instance, response, and error.

        Examples:
            Update an existing segment group:

            >>> updated_group, _, error = client.zpa.segment_groups.update_group_v2(
            ...     group_id='216196257331370181',
            ...     name=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating segment group: {error}")
            ...     return
            ... print(f"Segment group updated successfully: {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint_v2}
            /segmentGroup/{group_id}
        """)

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

        # Handle 204 No Content - response exists but body is empty
        if response is None or not response.get_body():
            return (SegmentGroup({"id": group_id}), response, None)

        try:
            result = SegmentGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: str, microtenant_id: str = None) -> APIResult[None]:
        """
        Deletes the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group.
            microtenant_id (str, optional): The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a segment group:

            >>> _, _, error = client.zpa.segment_groups.delete_group('216196257331370181')
            >>> if error:
            ...     print(f"Error deleting segment group: {error}")
            ...     return
            ... print(f"Segment group deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /segmentGroup/{group_id}
        """)

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
