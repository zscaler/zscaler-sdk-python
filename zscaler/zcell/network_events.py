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
from zscaler.utils import format_url, zcell_params
from zscaler.zcell.models.network_events import NetworkEvents


class NetworkEventsAPI(APIClient):

    _zcell_base_endpoint = "/zcell/config/api/v1"

    def __init__(self, request_executor: "RequestExecutor", config: dict = None) -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcell_customer_id = (config or {}).get("client", {}).get("zcellCustomerId")

    @zcell_params(start_key="start_time", end_key="end_time", target="path")
    def list_network_events_search(
        self, id: str = None, start_time: int = None, end_time: int = None, **kwargs
    ) -> APIResult[List[NetworkEvents]]:
        """
        Searches for network events for a given customer with filtering and pagination.

        The time window (``startTime`` / ``endTime``, epoch seconds) is supplied as
        **path** parameters, while the filter and pagination options are sent as a
        flat JSON request **body**. The ``days`` shorthand fills ``start_time`` /
        ``end_time`` with a ``[now - days, now]`` window.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            start_time (int): Path parameter. Window start as epoch seconds. Required unless ``days`` is supplied.
            end_time (int): Path parameter. Window end as epoch seconds. Required unless ``days`` is supplied.
            days (int): Convenience shorthand — sets a [now - days, now] start_time/end_time epoch-seconds path window.
            **kwargs: Request body fields (flat):
                ``[sort_by]`` {dict}: Sort object, e.g. ``{"name": "DESC"}`` (SortDirectionEnum: ASC, DESC).
                ``[filter_by]`` {list[dict]}: List of filters, each with ``filterName`` (str),
                ``operator`` (str: EQ, NE, LIKE, NOT_LIKE), and ``values`` (list[str]).
                ``[exclude_apn_config]`` {bool}: Whether to exclude APN config.
                ``[page]`` {int}: Page number (>= 0).
                ``[size]`` {int}: Page size (1-100).

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            Search network events over the last 7 days with a filter::

                >>> results, _, error = client.zcell.network_events.list_network_events_search(
                ...     id='gi754cvqb07r0',
                ...     days=7,
                ...     filter_by=[{'filterName': 'country', 'operator': 'EQ', 'values': ['US']}],
                ...     page=0,
                ...     size=10,
                ... )
                >>> if error:
                ...     print(f"Error: {error}")
                ...     return
                >>> for item in results:
                ...     print(item.as_dict())

            Provide an explicit path window instead of the ``days`` shorthand::

                >>> results, _, error = client.zcell.network_events.list_network_events_search(
                ...     id='gi754cvqb07r0',
                ...     start_time=1781296768,
                ...     end_time=1782506368,
                ...     sort_by={'name': 'DESC'},
                ... )
        """
        http_method = "post".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(
            f"{self._zcell_base_endpoint}/network-events/{id}/search/startTime/{start_time}/endTime/{end_time}"
        )

        body = kwargs
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
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
