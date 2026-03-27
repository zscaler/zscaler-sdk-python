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

from typing import Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.logs import VisibilityChartData


class LogsAPI(APIClient):
    """
    Client for the ZTB Logs resource.

    Provides operations for retrieving log data and visibility chart data
    in the Zero Trust Branch API. Endpoint: ``/api/logs``.
    """

    _ztb_base_endpoint = "/ztb/api"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_visibility_chart(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get data for visibility chart.

        Args:
            query_params (dict, optional): Map of query parameters.
                ``[query_params.query_type]`` (str): Required. Type of query (e.g. sites).
                ``[query_params.search_criteria]`` (str): Search criteria.
                ``[query_params.search_text]`` (str): Text to search for.
                ``[query_params.site]`` (str): Site filter.
                ``[query_params.network]`` (str): Network filter.
                ``[query_params.subnet]`` (str): Subnet filter.
                ``[query_params.osgroup]`` (str): OS group filter.

        Returns:
            tuple: (VisibilityChartData instance, Response, error).

        Examples:
            >>> chart_data, _, err = client.ztb.logs.get_visibility_chart(
            ...     query_params={"query_type": "sites"}
            ... )
            >>> if err:
            ...     print(f"Error: {err}")
            ...     return
            >>> for item in chart_data.data:
            ...     print(item.type, item.id)
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /logs
        """)
        query_params = query_params or {}
        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = VisibilityChartData(self.form_response_body(payload))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)
