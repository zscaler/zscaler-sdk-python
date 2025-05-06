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
from zscaler.zia.models.traffic_datacenters import TrafficDatacenters
from zscaler.zia.models.traffic_dc_exclusions import TrafficDcExclusions
from zscaler.utils import format_url, validate_and_convert_times


class TrafficDatacentersAPI(APIClient):
    """
    A Client object for the Traffic Datacenters resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_dc_exclusions(
        self,
        query_params=None,
    ) -> tuple:
        """
        Retrieves the list of Zscaler data centers (DCs) that are
        currently excluded from service to your organization based
        on configured exclusions in the ZIA Admin Portal

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of DC Exclusions instances, Response, error)

        Examples:
            List DC Exclusions:

            >>> fetched_dc, _, error = client.zia.traffic_datacenters.list_dc_exclusions()
            >>>     if error:
            ...         print(f"Error fetching dc by ID: {error}")
            ...         return
            ...     print(f"Fetched dc by ID: {fetched_dc[0].as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dcExclusions
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(TrafficDcExclusions(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def add_dc_exclusion(self, **kwargs) -> tuple:
        """
        Adds a data center (DC) exclusion to disable the tunnels terminating at a virtual IP address of a Zscaler DC
        triggering a failover from primary to secondary tunnels in the event of service disruptions
        Zscaler Trust Portal incidents, disasters, etc. You can configure to exclude a specific DC based
        on the traffic forwarding method for a designated time period.

        Note: Currently, only the IPSec VPN tunnel forwarding method is supported for DC exclusion.

        Args:
            dc_id (str): The unique identifier for the DC exclusion configuration
            **kwargs: Optional keyword args.

        Keyword Args:
            dc_name (list): The name of the data center.
            description (str): Additional information about the DC exclusion
            expired (bool): A Boolean value indicating whether the DC exclusion has expired
            start_time (int): The time interval start time.
            end_time (int): The time interval end time.

        Returns:
            tuple: A tuple containing the newly added DC Exclusion, response, and error.

        Examples:
            Add a multiple DC Exclusion

            >>> added_dc, _, error = client.zia.traffic_datacenters.add_dc_exclusion(
            ...     description=f"NewDCExclusion_{random.randint(1000, 10000)}",
            ...     start_time="Tue, 29 Apr 2025 14:51:00 PST",
            ...     end_time="Thu, 01 May 2025 14:00:00 PST",
            ... )
            >>> if error:
            ...     print(f"Error adding dc: {error}")
            ...     return
            ... for dc in added_dc:
            ...     print(dc.as_dict())

            Add a single DC Exclusion

            >>> added_dc, _, error = client.zia.traffic_datacenters.add_dc_exclusion(
            ...     description=f"NewDCExclusion_{random.randint(1000, 10000)}",
            ...     start_time="Tue, 29 Apr 2025 14:51:00 PST",
            ...     end_time="Thu, 01 May 2025 14:00:00 PST",
            ... )
            >>> if error:
            ...     print(f"Error adding dc: {error}")
            ...     return
            ... print(f"DC added successfully: {added_dc[0].as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dcExclusions
        """
        )

        try:
            start_time = kwargs.get("start_time")
            end_time = kwargs.get("end_time")
            time_zone = kwargs.get("time_zone", "UTC")

            if isinstance(start_time, str) and isinstance(end_time, str):
                start_epoch, end_epoch = validate_and_convert_times(start_time, end_time, time_zone)
            else:
                start_epoch = int(start_time)
                end_epoch = int(end_time)

            dcid = kwargs.get("dcid")
            if not dcid:
                dc_list, _, error = self.list_datacenters()
                if error:
                    return (None, None, error)
                if not dc_list:
                    return (None, None, ValueError("No data centers found to use as default."))
                dcid = dc_list[0].id

        except Exception as e:
            return (None, None, e)

        body = [
            {
                "dcid": dcid,
                "startTime": start_epoch,
                "endTime": end_epoch,
            }
        ]

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [TrafficDcExclusions(self.form_response_body(item)) for item in response.get_body()]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    # Submit JIRA Case - Method is returning 405.
    def update_dc_exclusion(self, dcid: int, **kwargs) -> tuple:
        """
        Updates a Zscaler data center DC Exclusion configuration based on the specified ID.

        Args:
            dc_id (int): The unique ID for the DC Exclusion.

        Returns:
            tuple: A tuple containing the updated DC Exclusion, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dcExclusions/{dcid}
        """
        )

        try:
            start_time = kwargs.get("start_time")
            end_time = kwargs.get("end_time")
            time_zone = kwargs.get("time_zone", "UTC")

            if isinstance(start_time, str) and isinstance(end_time, str):
                start_epoch, end_epoch = validate_and_convert_times(start_time, end_time, time_zone)
            else:
                start_epoch = int(start_time)
                end_epoch = int(end_time)

            dcid = kwargs.get("dcid")
            if not dcid:
                dc_list, _, error = self.list_datacenters()
                if error:
                    return (None, None, error)
                if not dc_list:
                    return (None, None, ValueError("No data centers found to use as default."))
                dcid = dc_list[0].id

        except Exception as e:
            return (None, None, e)

        body = [
            {
                "dcid": dcid,
                "startTime": start_epoch,
                "endTime": end_epoch,
            }
        ]

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TrafficDcExclusions)
        if error:
            return (None, response, error)

        try:
            result = TrafficDcExclusions(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_dc_exclusion(self, dc_id: int) -> tuple:
        """
        Deletes a Zscaler data center DC exclusion configuration based on the specified ID
        The DC exclusion configuration ID can be obtained by sending a GET via the method `list_dc_exclusions`.

        Args:
            dc_id (str): The unique identifier of the DC exclusion.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete DC Exclusion:

            >>> _, _, error = client.zia.traffic_datacenters.delete_dc_exclusion(added_dc[0].dcid)
            >>>     if error:
            ...         print(f"Error deleting dc: {error}")
            ...         return
            ...     print(f"DC with ID {added_dc[0].dcid} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dcExclusions/{dc_id}
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

    def list_datacenters(self, query_params=None) -> tuple:
        """
        Retrieves the list of Zscaler data centers (DCs) that can be excluded from service to your organization

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            tuple: A tuple containing (risk profile lite instance, Response, error).

        Examples:
            List datacenters:

            >>> dc_list, _, error = client.zia.traffic_datacenters.list_datacenters()
            >>> if error:
            ...     print(f"Error listing datacenters: {error}")
            ...     return
            ... print(f"Total datacenters found: {len(dc_list)}")
            ... for dc in dc_list:
            ...     print(dc.as_dict())
        """
        query_params = query_params or {}

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /datacenters
        """
        )

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
                result.append(TrafficDatacenters(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
