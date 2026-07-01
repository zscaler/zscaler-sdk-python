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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zcell.models.network_events import NetworkEvents


class NetworkEventsAPI(APIClient):

    _zcell_base_endpoint = "/zcell/config/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_network_events_search_start_time_end_time(
        self, id: str, start_time: str, end_time: str, query_params=None, **kwargs
    ) -> APIResult[List[NetworkEvents]]:
        """
        Searches for network events for a given customer with filtering and pagination.

        Args:
            id (str): Path parameter.
            start_time (str): Path parameter.
            end_time (str): Path parameter.
            **kwargs: Request body fields.
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.network_events.list_network_events_search_start_time_end_time(
            ...     id='...',
            ...     start_time='...',
            ...     end_time='...',
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(
            f"{self._zcell_base_endpoint}/network-events/{id}/search/startTime/{start_time}/endTime/{end_time}"
        )

        query_params = query_params or {}

        body = kwargs
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
                result.append(NetworkEvents(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
