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

    def get_segments_by_type(self, application_type: str, expand_all: bool = False, query_params=None, **kwargs) -> tuple:
        """
        Retrieve all configured application segments of a specified type, optionally expanding all related data.

        Args:
            application_type (str): Type of application segment to retrieve.
            Must be one of "BROWSER_ACCESS", "INSPECT", "SECURE_REMOTE_ACCESS".
            expand_all (bool, optional): Whether to expand all related data. Defaults to False.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.expand_all]`` {bool}: Additional information related to the applications
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            tuple: List of application segments.

        Examples:
            >>> app_type = 'BROWSER_ACCESS'
            >>> expand_all = True
            >>> search = "ba_server01"
            >>> app_segments = zpa.app_segments.get_segments_by_type(app_type, expand_all, search=search)
        """
        if not application_type:
            raise ValueError("The 'application_type' parameter must be provided.")

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/getAppsByType
        """
        )

        query_params = query_params or {}
        query_params.update(kwargs)
        query_params["application_type"] = application_type
        query_params["expand_all"] = str(expand_all).lower()

        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppSegmentByType)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(AppSegmentByType(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
