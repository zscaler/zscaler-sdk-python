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
from zscaler.zia.models.time_intervals import TimeIntervals
from zscaler.utils import format_url


class TimeIntervalsAPI(APIClient):
    """
    A Client object for the Time Intervals resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_time_intervals(self, query_params=None) -> tuple:
        """
        Retrieves a list of all configured time intervals.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Page size for pagination.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of Time Intervals instances, Response, error)

        Examples:
            List Time Intervals using default settings:

            >>> interval_list, _, error = client.zia.time_intervals.list_time_intervals(
                query_params={'search': Off-Work})
            >>> if error:
            ...     print(f"Error listing intervals: {error}")
            ...     return
            ... print(f"Total intervals found: {len(interval_list)}")
            ... for interval in interval_list:
            ...     print(interval.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeIntervals
        """
        )

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
                result.append(TimeIntervals(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_time_intervals(self, interval_id: int) -> tuple:
        """
        Fetches a specific Time Intervals by ID.

        Args:
            interval_id (int): The unique identifier for the Time Interval.

        Returns:
            tuple: A tuple containing (Time Interval instance, Response, error).

        Examples:
            Retrieve a specific time interval:

            >>> fetched_interval, _, error = client.zia.time_intervals.get_time_intervals('125245')
            >>> if error:
            ...     print(f"Error fetching time interval by ID: {error}")
            ...     return
            ... print(f"Fetched time interval by ID: {fetched_interval.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeIntervals/{interval_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TimeIntervals)
        if error:
            return (None, response, error)

        try:
            result = TimeIntervals(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_time_intervals(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Time Interval.

        Args:
            name (str): Name to identify the time interval
            **kwargs: Optional keyword args.

        Keyword Args:
            start_time (int): The time interval start time.
            end_time (str): The time interval end time.
            days_of_week (list): Specifies which days of the week apply to the time interval.
                If set to EVERYDAY, all the days of the week are chosen.
                Values supported: `EVERYDAY`, `SUN`, `MON`, `TUE`, `WED`, `THU`, `FRI`, `SAT`

        Returns:
            tuple: A tuple containing the newly added Time Interval, response, and error.

        Examples:
            Add a new Time Interval

            >>> added_interval, _, error = client.zia.time_intervals.add_time_intervals(
            ...     name=f"NewTimeInterval01_{random.randint(1000, 10000)}",
            ...     start_time='0',
            ...     end_time='1439',
            ...     days_of_week=["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
            ... )
            >>> if error:
            ...     print(f"Error adding Time Interval: {error}")
            ...     return
            ... print(f"Time Interval added successfully: {added_interval.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeIntervals
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TimeIntervals)
        if error:
            return (None, response, error)

        try:
            result = TimeIntervals(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_time_intervals(self, interval_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Time Interval.

        Args:
            interval_id (int): The unique ID for the Time Interval.

        Returns:
            tuple: A tuple containing the updated Time Interval, response, and error.

        Examples:
            Update a Time Interval

            >>> added_interval, _, error = client.zia.time_intervals.update_time_intervals(
                    interval_id='15455'
            ...     name=f"UpdateTimeInterval01_{random.randint(1000, 10000)}",
            ...     start_time='0',
            ...     end_time='1439',
            ...     days_of_week=["SUN", "MON", "TUE", "WED", "THU"],
            ... )
            >>> if error:
            ...     print(f"Error updating Time Interval: {error}")
            ...     return
            ... print(f"Time Interval updated successfully: {added_interval.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeIntervals/{interval_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TimeIntervals)
        if error:
            return (None, response, error)

        try:
            result = TimeIntervals(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_time_intervals(self, interval_id: int) -> tuple:
        """
        Deletes the specified Time Interval.

        Args:
            interval_id (str): The unique identifier of the Time Interval.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete Time Interval:

            >>> _, _, error = client.zia.time_intervals.delete_time_intervals('73459')
            >>> if error:
            ...     print(f"Error deleting Time Interval: {error}")
            ...     return
            ... print(f"Time Interval with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeIntervals/{interval_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
