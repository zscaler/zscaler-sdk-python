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
from zscaler.utils import format_url
from zscaler.zpa.models.application_segment import AppSegmentByType


class ApplicationSegmentByTypeAPI(APIClient):
    """
    A client object for the Application Segment By Type resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def get_segments_by_type(
        self,
        application_type: str,
        expand_all: bool = False,
        query_params: Optional[dict] = None,
        **kwargs
    ) -> List[AppSegmentByType]:
        """
        Retrieve all configured application segments of a specified type.

        Args:
            application_type (str): Type of application segment to retrieve.
                Must be one of "BROWSER_ACCESS", "INSPECT", "SECURE_REMOTE_ACCESS".
            expand_all (bool, optional): Whether to expand all related data.
            query_params (dict, optional): Map of query parameters.

        Returns:
            List[AppSegmentByType]: List of application segments.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If application_type is not provided.

        Examples:
            >>> try:
            ...     segments = client.zpa.app_segment_by_type.get_segments_by_type(
            ...         'BROWSER_ACCESS',
            ...         expand_all=True
            ...     )
            ...     for segment in segments:
            ...         print(segment.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        if not application_type:
            raise ValueError("The 'application_type' parameter must be provided.")

        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/getAppsByType")

        query_params = query_params or {}
        query_params.update(kwargs)
        query_params["application_type"] = application_type
        query_params["expand_all"] = str(expand_all).lower()

        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params=query_params)
        response = self._request_executor.execute(request, AppSegmentByType)

        return [AppSegmentByType(self.form_response_body(item)) for item in response.get_results()]

    def delete_segments_by_type(
        self,
        segment_id: str,
        application_type: str,
        microtenant_id: Optional[str] = None
    ) -> None:
        """
        Deletes the specified Application Segment from ZPA by type.

        Args:
            segment_id (str): The unique identifier for the Application Segment.
            application_type (str): Type of application segment to delete.
                Must be one of "BROWSER_ACCESS", "INSPECT", "SECURE_REMOTE_ACCESS".
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.app_segment_by_type.delete_segments_by_type(
            ...         segment_id='999999',
            ...         application_type='BROWSER_ACCESS'
            ...     )
            ...     print("Segment deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{segment_id}/deleteAppByType")

        params = {"applicationType": application_type}
        if microtenant_id:
            params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
