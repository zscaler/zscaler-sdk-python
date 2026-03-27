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

from typing import List, Literal, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url

ReportType = Literal["APPLICATION", "DATA_EXPLORER", "WORKPLACE"]
SubType = Literal["CustomDataFeed", "ScheduledReports", "SaveAndSchedule"]


class ReportsAPI(APIClient):
    """
    A Client object for the Business Insights Reports resource.

    Provides operations to list available reports and download
    report files from Zscaler Business Insights.
    """

    _zbi_base_endpoint = "/bi/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_reports(self, query_params: Optional[dict] = None) -> APIResult[List[dict]]:
        """
        Retrieves a list of available reports.

        Args:
            query_params (dict, optional): Map of query parameters.

                ``[query_params.reportType]`` (str): Type of report.
                One of: APPLICATION, DATA_EXPLORER, WORKPLACE.
                Default: APPLICATION.

                ``[query_params.subType]`` (str): Subtype of report.
                One of: CustomDataFeed, ScheduledReports,
                SaveAndSchedule. Default: CustomDataFeed.

                ``[query_params.startTime]`` (int): Report start time
                as Unix timestamp (seconds). Defaults to midnight UTC
                of the 1st day of the previous month.

                ``[query_params.endTime]`` (int): Report end time as
                Unix timestamp (seconds). Defaults to current time.

                ``[query_params.reportName]`` (str): Filter by report
                name (optional).

        Returns:
            tuple: (list of report dicts, Response, error).

        Examples:
            List all DATA_EXPLORER reports::

                >>> reports, _, err = client.zbi.reports.list_reports(
                ...     query_params={
                ...         "reportType": "DATA_EXPLORER",
                ...         "subType": "SaveAndSchedule"
                ...     }
                ... )
                >>> if err:
                ...     print(f"Error: {err}")
                >>> for r in reports:
                ...     print(r)
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /report
            /all
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
            results = response.get_results()
        except Exception as exc:
            return (None, response, exc)

        return (results, response, None)

    def download_report(
        self,
        file_name: str,
        report_type: ReportType,
        sub_type: Optional[SubType] = "CustomDataFeed",
        compression: Optional[Literal["gzip"]] = None,
        save_path: Optional[str] = None,
    ) -> str:
        """
        Downloads a specific report file from Business Insights.

        Sends a POST request to ``/bi/api/v1/report/download`` with a
        JSON body and accepts binary (application/octet-stream) response.

        Args:
            file_name (str): The file name of the report to download
                (server-side identifier).
            report_type (str): The report type. One of: APPLICATION,
                DATA_EXPLORER, WORKPLACE.
            sub_type (str, optional): The report subtype. One of:
                CustomDataFeed, ScheduledReports, SaveAndSchedule.
                Defaults to CustomDataFeed.
            compression (str, optional): Compression type. Only
                ``gzip`` is supported.
            save_path (str, optional): Local path to save the
                downloaded file. Defaults to file_name.

        Returns:
            str: Path to the saved file.

        Raises:
            ValueError: If file_name is empty or types are invalid.
            Exception: If the request fails or response is invalid.

        Examples:
            Download an APPLICATION report::

                >>> path = client.zbi.reports.download_report(
                ...     file_name="my-report.csv",
                ...     report_type="APPLICATION",
                ...     sub_type="CustomDataFeed",
                ...     save_path="./reports/my-report.csv"
                ... )
                >>> print(f"Report saved to {path}")
        """
        if not file_name:
            raise ValueError("file_name is required.")

        valid_report_types = ("APPLICATION", "DATA_EXPLORER", "WORKPLACE")
        if report_type not in valid_report_types:
            raise ValueError(f"report_type must be one of {valid_report_types}, " f"got: {report_type}")

        valid_sub_types = (
            "CustomDataFeed",
            "ScheduledReports",
            "SaveAndSchedule",
        )
        if sub_type is not None and sub_type not in valid_sub_types:
            raise ValueError(f"sub_type must be one of {valid_sub_types}, " f"got: {sub_type}")

        body = {
            "fileName": file_name,
            "reportType": report_type,
            "subType": sub_type or "CustomDataFeed",
        }

        query_params = {}
        if compression == "gzip":
            query_params["compression"] = "gzip"

        api_url = format_url(f"{self._zbi_base_endpoint}/report/download")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/octet-stream",
        }

        request, error = self._request_executor.create_request(
            method="POST",
            endpoint=api_url,
            body=body,
            headers=headers,
            params=query_params if query_params else None,
        )

        if error:
            raise Exception("Error creating request for downloading report.")

        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            raise error
        if response is None:
            raise Exception("No response received when downloading report.")

        content_type = response.headers.get("Content-Type", "").lower()
        if not content_type.startswith("application/octet-stream"):
            raise Exception("Invalid response content type. Expected " "application/octet-stream, got: " f"{content_type}")

        output_path = save_path or file_name
        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path
