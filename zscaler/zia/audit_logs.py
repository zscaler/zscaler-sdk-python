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
import time


class AuditLogsAPI(APIClient):
    """
    A Client object for Audit Logs resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_status(self) -> tuple:
        """
        Get the status of a request for an audit log report.

        Returns:
            :obj:`tuple`: Audit log report request status.

        Examples:
            >>> print(zia.audit_logs.status())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /auditlogEntryReport
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, {})
        if error:
            return None

        response, error = self._request_executor.execute(request)
        if error:
            return None

        return response.get_body()

    def create(self, start_time: str, end_time: str) -> tuple:
        """
        Creates an audit log report for the specified time period and saves it as a CSV file.

        Args:
            start_time (str): The timestamp, in epoch, of the admin's last login.
            end_time (str): The timestamp, in epoch, of the admin's last logout.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.audit_logs.create(start_time='1627221600000', end_time='1627271676622')

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /auditlogEntryReport"
            """
        )

        payload = {
            "startTime": start_time,
            "endTime": end_time,
        }

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return None

        response, error = self._request_executor.execute(request, None)
        if error:
            return None
        time.sleep(2)
        return response.get_status()

    def cancel(self) -> tuple:
        """
        Cancels the request to create an audit log report.

        Returns:
            :obj:`int`: The operation response code.

        Examples:
            >>> zia.audit_logs.cancel()

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /auditlogEntryReport"
            """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, {})
        if error:
            return None

        response, error = self._request_executor.execute(request, None)
        if error:
            return None

        return response.status_code

    def get_report(self) -> tuple:
        """
        Returns the most recently created audit log report.

        Returns:
            :obj:`str`: String representation of CSV file.

        Examples:
            Write report to CSV file:

            >>> with open("audit_log.csv", "w+") as fh:
            ...    fh.write(zia.audit_logs.get_report())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /auditlogEntryReport/download
            """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, {})
        if error:
            return None

        response, error = self._request_executor.execute(request, None)
        if error:
            return None

        return response.get_body()
