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

import logging
from typing import Dict, Any, Optional, List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.alarms import Alarms
from zscaler.ztb.models.alarms import AlarmBulkAcknowledge


class AlarmsAPI(APIClient):
    """
    Client for the ZTB Alarms resource.

    Provides CRUD operations for alarm notifications in the
    Zero Trust Branch API.

    ASSUMPTION: Endpoint paths are based on Swagger UI screenshots
    showing ``/api/v2/alarm`` and related sub-paths.
    """

    # ASSUMPTION: ZTB alarm endpoints live under /api/v2 based on Swagger docs.
    # When used via the OneAPI gateway the ``/ztb`` prefix is prepended by
    # the service routing layer.
    _ztb_base_endpoint = "/ztb/api/v2"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_alarms(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get all alarms.

        Returns:
            Tuple of (result_list, response, error).

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.search]`` (str): String used to partially match against a location's name and port attributes.

                ``[query_params.tab]`` (str): Parameter was deprecated and no longer has an effect on SSL policy.

                ``[query_params.page]`` (int):

                ``[query_params.size]`` (int):

                ``[query_params.sort]`` (str):

                ``[query_params.sortdir]`` (str):

                ``[query_params.site_id]`` (str):

                ``[query_params.severity]`` (str):

        Examples:
            >>> alarms, response, error = client.ztb.alarms.list_alarms()
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm
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
                result.append(Alarms(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_alarm(self, alarm_id: str) -> APIResult:
        """
        Get a single alarm by ID.

        Args:
            alarm_id: The alarm identifier.

        Returns:
            Tuple of (Alarm instance, response, error).

        Examples:
            >>> alarm, response, error = client.ztb.alarms.get_alarm("abc-123")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm/{alarm_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Alarms)
        if error:
            return (None, response, error)

        try:
            result = Alarms(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_alarm(self, **kwargs) -> APIResult:
        """
        Create a new alarm.

        Args:
            **kwargs: Alarm creation fields.

        Returns:
            Tuple of (Alarm instance, response, error).

        Examples:
            >>> alarm, response, error = client.ztb.alarms.create_alarm(name="test")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Alarms)
        if error:
            return (None, response, error)

        try:
            result = Alarms(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_alarm_patch(self, **kwargs) -> APIResult:
        """
        Update an alarm (PATCH).

        Args:
            alarm_id: The alarm identifier.
            **kwargs: Alarm update fields.

        Returns:
            Tuple of (Alarm instance, response, error).

        Examples:
            >>> alarm, response, error = client.ztb.alarms.update_alarm("abc-123", status="active")
        """
        http_method = "patch".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Alarms)
        if error:
            return (None, response, error)

        try:
            result = Alarms(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_alarm_put(self, **kwargs) -> APIResult:
        """
        Update an alarm (PUT).

        Args:
            alarm_id: The alarm identifier.
            **kwargs: Full alarm replacement fields.

        Returns:
            Tuple of (Alarm instance, response, error).

        Examples:
            >>> alarm, response, error = client.ztb.alarms.update_alarm_put("abc-123", name="new")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Alarms)
        if error:
            return (None, response, error)

        try:
            result = Alarms(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_alarm(self, alarm_id: int) -> APIResult[dict]:
        """
        Deletes the specified Alarm.

        Args:
            alarm_id (str): The unique identifier of the Alarm.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Alarm:

            >>> _, _, error = client.ztb.alarms.delete_alarm('73459')
            >>> if error:
            ...     print(f"Error deleting Alarm: {error}")
            ...     return
            ... print(f"Alarm with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm/{alarm_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def bulk_acknowledge(self, **kwargs) -> APIResult:
        """
        Bulk acknowledge alarms.

        Args:
            **kwargs: Bulk acknowledge payload fields.

        Returns:
            Tuple of (result, response, error).

        Examples:
            >>> result, response, error = client.ztb.alarms.bulk_acknowledge(ids=["a","b"])
        """
        http_method = "patch".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm/bulkAcknowledge
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlarmBulkAcknowledge)
        if error:
            return (None, response, error)

        try:
            result = AlarmBulkAcknowledge(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def bulk_acknowledge_all(self) -> APIResult:
        """
        Acknowledge all active alarms.

        Returns:
            Tuple of (result, response, error).

        Examples:
            >>> result, response, error = client.ztb.alarms.bulk_acknowledge_all()
        """
        http_method = "patch".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm/bulkAcknowledgeAll
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlarmBulkAcknowledge)
        if error:
            return (None, response, error)

        try:
            result = AlarmBulkAcknowledge(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def bulk_ignore(self, **kwargs) -> APIResult:
        """
        Bulk ignore alarms.

        Args:
            **kwargs: Bulk ignore payload fields.

        Returns:
            Tuple of (result, response, error).

        Examples:
            >>> result, response, error = client.ztb.alarms.bulk_ignore(ids=["a","b"])
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm/bulkIgnore
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlarmBulkAcknowledge)
        if error:
            return (None, response, error)

        try:
            result = AlarmBulkAcknowledge(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def bulk_ignore_all(self) -> APIResult:
        """
        Ignore all active alarms.

        Returns:
            Tuple of (result, response, error).

        Examples:
            >>> result, response, error = client.ztb.alarms.bulk_ignore_all()
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /alarm/bulkIgnoreAll
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlarmBulkAcknowledge)
        if error:
            return (None, response, error)

        try:
            result = AlarmBulkAcknowledge(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
