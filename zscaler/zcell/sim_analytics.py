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
from zscaler.zcell.models.sim_analytics import (
    SimAnalytics,
    SimCountryUsage,
    SimDayUsage,
    SimSummary, 
    SimUsage
)


class SimAnalyticsAPI(APIClient):

    _zcell_base_endpoint_customer = "/zcell/config/api/v1/customers"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_sim_analytics_map(self, id: str, query_params=None, **kwargs) -> APIResult[List[SimAnalytics]]:
        """
        Returns dashboard lat/lng details summary.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.sim_analytics.list_sim_analytics_map(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim/analytics/map")

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
                result.append(SimAnalytics(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_sim_analytics_summary(self, id: str, query_params=None) -> APIResult[List[SimSummary]]:
        """
        Returns sim status summary.

        Args:
            id (str): Path parameter.
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.sim_analytics.list_sim_analytics_summary(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim/analytics/summary")

        query_params = query_params or {}

        body = {}
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
                result.append(SimSummary(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @zcell_params(start_key="startDate", end_key="endDate")
    def list_sim_analytics_usage_countries(
        self, id: str, start_date: int = None, end_date: int = None, query_params=None
    ) -> APIResult[List[SimCountryUsage]]:
        """
        Returns top countries by usage.

        This endpoint uses ``startDate`` / ``endDate`` (epoch seconds) for the
        time window — not the ``startDateTime`` / ``endDateTime`` used by most
        other ZCell endpoints. The ``days`` shorthand fills both accordingly.

        Args:
            id (str): Path parameter.
            start_date (int): Window start as epoch seconds. Required unless ``days`` is supplied.
            end_date (int): Window end as epoch seconds. Required unless ``days`` is supplied.
            days (int): Convenience shorthand — sets a [now - days, now] start_date/end_date epoch-seconds window.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.start_date]`` {int}: Required
                ``[query_params.end_date]`` {int}: Required
                ``[query_params.limit]`` {int}: Page size (<= 20). Default: 10

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.sim_analytics.list_sim_analytics_usage_countries(
            ...     id='gi754cvqb07r0',
            ...     days=14
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim/analytics/usage/countries")

        query_params = query_params or {}
        if start_date is not None:
            query_params["start_date"] = start_date
        if end_date is not None:
            query_params["end_date"] = end_date

        body = {}
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
                result.append(SimCountryUsage(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @zcell_params(start_key="startDate", end_key="endDate")
    def list_sim_analytics_usage_day(
        self, id: str, start_date: int = None, end_date: int = None, query_params=None
    ) -> APIResult[List[SimDayUsage]]:
        """
        Returns data usage in given date range.

        This endpoint uses ``startDate`` / ``endDate`` (epoch seconds) for the
        time window — not the ``startDateTime`` / ``endDateTime`` used by most
        other ZCell endpoints. The ``days`` shorthand fills both accordingly.

        Args:
            id (str): Path parameter.
            start_date (int): Window start as epoch seconds. Required unless ``days`` is supplied.
            end_date (int): Window end as epoch seconds. Required unless ``days`` is supplied.
            days (int): Convenience shorthand — sets a [now - days, now] start_date/end_date epoch-seconds window.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.start_date]`` {int}: Required
                ``[query_params.end_date]`` {int}: Required
                ``[query_params.icc_id]`` {str}

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.sim_analytics.list_sim_analytics_usage_day(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim/analytics/usage/day")

        query_params = query_params or {}
        if start_date is not None:
            query_params["start_date"] = start_date
        if end_date is not None:
            query_params["end_date"] = end_date

        body = {}
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
                result.append(SimDayUsage(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @zcell_params(start_key="startDate", end_key="endDate")
    def list_sim_analytics_usage_sims(
        self, id: str, start_date: int = None, end_date: int = None, query_params=None
    ) -> APIResult[List[SimUsage]]:
        """
        Returns top sim by usage.

        Args:
            id (str): Path parameter.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.start_date]`` {int}: Required
                ``[query_params.end_date]`` {int}: Required
                ``[query_params.limit]`` {int}

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.sim_analytics.list_sim_analytics_usage_sims(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim/analytics/usage/sims")

        query_params = query_params or {}
        if start_date is not None:
            query_params["start_date"] = start_date
        if end_date is not None:
            query_params["end_date"] = end_date

        body = {}
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
                result.append(SimUsage(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
