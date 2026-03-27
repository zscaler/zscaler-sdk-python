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

from typing import Dict, Any, Optional, List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.devices import (
    ActiveDevice,
    DeviceTags,
    OperatingSystemRow,
    GroupByRow,
    DeviceFilterValues,
)


class DevicesAPI(APIClient):
    """
    Client for the ZTB Devices resource.

    Provides operations for listing active devices, device tags, operating
    systems, device details, DHCP history, filter values, and group-by
    aggregations in the Zero Trust Branch API.
    """

    _ztb_base_v2 = "/ztb/api/v2"
    _ztb_base_v3 = "/ztb/api/v3"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_active_devices(self, query_params: Optional[dict] = None) -> APIResult:
        """
        List active devices with pagination and search.

        Args:
            query_params (dict, optional): Map of query parameters.
                ``[query_params.search]`` (str): Search filter.
                ``[query_params.tags]`` (str): Tags filter.
                ``[query_params.page]`` (int): Page number.
                ``[query_params.limit]`` (int): Page size.
                ``[query_params.sort]`` (str): Sort field.
                ``[query_params.sortdir]`` (str): Sort direction (asc/desc).
                ``[query_params.siteId]`` (str): Site ID filter.

        Returns:
            tuple: (list of ActiveDevice instances, Response, error).

        Examples:
            >>> devices, _, err = client.ztb.devices.list_active_devices()
            >>> devices, _, err = client.ztb.devices.list_active_devices(
            ...     query_params={"search": "DESKTOP", "page": 1, "limit": 25}
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v2}
            /devices/active
        """)
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
                result.append(ActiveDevice(self.form_response_body(item)))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def list_devices_by_category(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get devices by category or type (V3 endpoint).

        Args:
            query_params (dict, optional): Map of query parameters.
                ``[query_params.search]`` (str): Search filter.
                ``[query_params.page]`` (int): Page number.
                ``[query_params.limit]`` (int): Page size.
                ``[query_params.sort]`` (str): Sort field.
                ``[query_params.sortdir]`` (str): Sort direction.
                ``[query_params.type]`` (str): Device type filter.
                ``[query_params.category]`` (str): Category filter.
                ``[query_params.filters]`` (str): Filters.
                ``[query_params.osname]`` (str): OS name filter.
                ``[query_params.osversion]`` (str): OS version filter.
                ``[query_params.full]`` (bool): Full response.

        Returns:
            tuple: (response body as dict, Response, error).

        Examples:
            >>> body, _, err = client.ztb.devices.list_devices_by_category(
            ...     query_params={"type": "Computer", "page": 1}
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v3}
            /device
        """)
        query_params = query_params or {}
        body = {}
        headers = {}
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (response.get_body(), response, None)

    def get_device_tags(self) -> APIResult:
        """
        Get list of device tags.

        Returns:
            tuple: (DeviceTags instance, Response, error).

        Examples:
            >>> tags, _, err = client.ztb.devices.get_device_tags()
            >>> if not err and tags:
            ...     print(tags.tags)
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v2}
            /devices/tags
        """)
        body = {}
        headers = {}
        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = DeviceTags(self.form_response_body(payload))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_group_by_list(self) -> APIResult:
        """
        Get list of group names for graphs (e.g. categories, types).

        Returns:
            tuple: (list of group name strings, Response, error).

        Examples:
            >>> groups, _, err = client.ztb.devices.get_group_by_list()
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v3}
            /device/group-by/list
        """)
        body = {}
        headers = {}
        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result_wrap = payload.get("result") or {}
            rows = result_wrap.get("rows") or result_wrap.get("Rows") or []
            result = [r if isinstance(r, str) else str(r) for r in rows]
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def list_operating_systems(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get list of operating systems with device counts grouped by OS name and version.

        Args:
            query_params (dict, optional): Map of query parameters.
                ``[query_params.search]`` (str): Search filter.
                ``[query_params.page]`` (int): Page number.
                ``[query_params.limit]`` (int): Page size.
                ``[query_params.sort]`` (str): Sort field (e.g. os_name, count, version).
                ``[query_params.sortdir]`` (str): Sort direction.

        Returns:
            tuple: (list of OperatingSystemRow instances, Response, error).

        Examples:
            >>> os_list, _, err = client.ztb.devices.list_operating_systems(
            ...     query_params={"page": 1, "limit": 50}
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v3}
            /device/operating-systems
        """)
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
                result.append(OperatingSystemRow(self.form_response_body(item)))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_dhcp_history(self, device_id: str, minutes: str) -> APIResult:
        """
        Get DHCP history for a device (V2 endpoint).

        Args:
            device_id (str): Device ID.
            minutes (str): Time window in minutes.

        Returns:
            tuple: (result dict with audit_logs, traffic_data, etc., Response, error).

        Examples:
            >>> data, _, err = client.ztb.devices.get_dhcp_history(
            ...     "505d6556-92bd-4909-a774-d958606579fa", "60"
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v2}
            /devices/details/id/{device_id}/{minutes}
        """)
        body = {}
        headers = {}
        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = payload.get("result") or {}
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_device_details_v3(self, device_id: str) -> APIResult:
        """
        Get device details (V3 endpoint).

        Args:
            device_id (str): Device ID.

        Returns:
            tuple: (result dict with device info, Response, error).

        Examples:
            >>> details, _, err = client.ztb.devices.get_device_details_v3(
            ...     "505d6556-92bd-4909-a774-d958606579fa"
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v3}
            /device/details/{device_id}
        """)
        body = {}
        headers = {}
        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = payload.get("result") or {}
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_filter_values(self, field: str, query_params: Optional[dict] = None) -> APIResult:
        """
        Get filter values by field name.

        Args:
            field (str): Field name (e.g. type, category).
            query_params (dict, optional): Map of query parameters.
                ``[query_params.page]`` (int): Page number.
                ``[query_params.limit]`` (int): Page size.

        Returns:
            tuple: (DeviceFilterValues instance, Response, error).

        Examples:
            >>> fv, _, err = client.ztb.devices.get_filter_values("type")
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v3}
            /device/filters/{field}/values
        """)
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
            payload = response.get_body() or {}
            result_wrap = payload.get("result") or {}
            result = DeviceFilterValues(self.form_response_body(result_wrap))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def list_devices_group_by(self, group: str, query_params: Optional[dict] = None) -> APIResult:
        """
        Get devices grouped by category or type with counts.

        Args:
            group (str): Group name (e.g. type, category).
            query_params (dict, optional): Map of query parameters.
                ``[query_params.search]`` (str): Search filter.
                ``[query_params.page]`` (int): Page number.
                ``[query_params.limit]`` (int): Page size.
                ``[query_params.sort]`` (str): Sort field.
                ``[query_params.sortdir]`` (str): Sort direction.

        Returns:
            tuple: (list of GroupByRow instances, Response, error).

        Examples:
            >>> rows, _, err = client.ztb.devices.list_devices_group_by(
            ...     "type", query_params={"page": 1}
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v3}
            /device/{group}
        """)
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
                result.append(GroupByRow(self.form_response_body(item)))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_device_details_v2(self, device_id: str, minutes: str) -> APIResult:
        """
        Get device details with audit logs (V2 endpoint).

        Args:
            device_id (str): Device ID.
            minutes (str): Time window in minutes for audit data.

        Returns:
            tuple: (result dict with audit_logs, traffic_data, etc., Response, error).

        Examples:
            >>> data, _, err = client.ztb.devices.get_device_details_v2(
            ...     "505d6556-92bd-4909-a774-d958606579fa", "60"
            ... )
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_v2}
            /devices/active/details/{device_id}/{minutes}
        """)
        body = {}
        headers = {}
        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = payload.get("result") or {}
        except Exception as err:
            return (None, response, err)
        return (result, response, None)
