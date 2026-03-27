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

from typing import Dict, List, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zbi.models.report_configs import ReportConfig


class ReportConfigsAPI(APIClient):
    """
    A Client object for the Business Insights Report Configurations resource.

    Provides CRUD operations for managing report configurations
    associated with custom applications.
    """

    _zbi_base_endpoint = "/bi/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_report_configs(
        self,
        report_type: str = "customapps",
        query_params: Optional[dict] = None,
    ) -> APIResult[List[ReportConfig]]:
        """
        Retrieves report configurations along with their associated
        custom apps.

        Args:
            report_type (str): The report type path segment.
                Currently only ``customapps`` is supported.
            query_params (dict, optional): Map of query parameters.

                ``[query_params.id]`` (int): Optional report config ID.

        Returns:
            tuple: (list of ReportConfig instances, Response, error).

        Examples:
            List all report configurations::

                >>> configs, _, err = client.zbi.report_configs.list_report_configs()
                >>> if err:
                ...     print(f"Error: {err}")
                >>> for cfg in configs:
                ...     print(cfg.as_dict())
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /reports
            /{report_type}
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
            results = [ReportConfig(self.form_response_body(item)) for item in response.get_results()]
        except Exception as exc:
            return (None, response, exc)

        return (results, response, None)

    def get_report_config(
        self,
        config_id: int,
        report_type: str = "customapps",
    ) -> APIResult[ReportConfig]:
        """
        Retrieves a specific report configuration by ID.

        Args:
            config_id (int): The unique identifier of the report
                configuration.
            report_type (str): The report type path segment.
                Currently only ``customapps`` is supported.

        Returns:
            tuple: (ReportConfig instance, Response, error).

        Examples:
            Get a report configuration by ID::

                >>> cfg, _, err = client.zbi.report_configs.get_report_config(1)
                >>> if err:
                ...     print(f"Error: {err}")
                >>> print(cfg.as_dict())
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /reports
            /{report_type}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params={"id": config_id})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result_list = response.get_results()
            if result_list:
                result = ReportConfig(self.form_response_body(result_list[0]))
            else:
                result = None
        except Exception as exc:
            return (None, response, exc)

        return (result, response, None)

    def create_report_config(
        self,
        report_type: str = "customapps",
        **kwargs,
    ) -> APIResult[ReportConfig]:
        """
        Creates a report configuration associated with custom apps.

        Args:
            report_type (str): The report type path segment.
                Currently only ``customapps`` is supported.
            name (str): Report name.
            sub_type (str): Report subtype. One of: OVERVIEW, USERS.
            enabled (bool): Whether the report is enabled.
            custom_ids (list[int]): Custom app reference IDs.
            delivery_information (list[dict]): Delivery settings with
                ``delivery_method`` and ``emails``.
            schedule_params (dict, optional): Schedule settings with
                ``timezone``, ``frequency``, and optional ``weekday``.
            backfill_params (dict, optional): Backfill settings with
                ``timezone``, ``stime``, and ``etime``.

        Returns:
            tuple: (ReportConfig instance, Response, error).

        Examples:
            Create a scheduled report configuration::

                >>> cfg, _, err = client.zbi.report_configs.create_report_config(
                ...     name="Daily report",
                ...     sub_type="USERS",
                ...     enabled=True,
                ...     custom_ids=[1234],
                ...     delivery_information=[{
                ...         "delivery_method": "EMAIL",
                ...         "emails": ["admin@example.com"]
                ...     }],
                ...     schedule_params={
                ...         "timezone": "UTC",
                ...         "frequency": "DAILY"
                ...     }
                ... )
        """
        http_method = "POST"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /reports
            /{report_type}
        """)
        body = kwargs
        headers = {"Content-Type": "application/json"}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result_list = response.get_results()
            if result_list:
                result = ReportConfig(self.form_response_body(result_list[0]))
            else:
                result = ReportConfig(self.form_response_body(response.get_body()))
        except Exception as exc:
            return (None, response, exc)

        return (result, response, None)

    def update_report_config(
        self,
        config_id: int,
        report_type: str = "customapps",
        **kwargs,
    ) -> APIResult[ReportConfig]:
        """
        Updates a report configuration by ID.

        Args:
            config_id (int): The unique identifier of the report
                configuration to update.
            report_type (str): The report type path segment.
                Currently only ``customapps`` is supported.
            name (str): Updated report name.
            sub_type (str): Updated subtype.
            enabled (bool): Whether the report is enabled.
            custom_ids (list[int]): Updated custom app IDs.
            delivery_information (list[dict]): Updated delivery settings.
            schedule_params (dict, optional): Updated schedule.

        Returns:
            tuple: (ReportConfig instance, Response, error).

        Examples:
            Update a report configuration::

                >>> cfg, _, err = client.zbi.report_configs.update_report_config(
                ...     1,
                ...     name="Weekly report",
                ...     sub_type="USERS",
                ...     enabled=True,
                ...     custom_ids=[1234],
                ...     delivery_information=[{
                ...         "delivery_method": "EMAIL",
                ...         "emails": ["admin@example.com"]
                ...     }],
                ...     schedule_params={
                ...         "timezone": "UTC",
                ...         "frequency": "WEEKLY",
                ...         "weekday": "MON"
                ...     }
                ... )
        """
        http_method = "PUT"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /reports
            /{report_type}
            /{config_id}
        """)
        body = kwargs
        headers = {"Content-Type": "application/json"}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = ReportConfig(self.form_response_body(response.get_body()))
        except Exception as exc:
            return (None, response, exc)

        return (result, response, None)

    def delete_report_config(
        self,
        config_id: int,
        report_type: str = "customapps",
    ) -> APIResult[int]:
        """
        Deletes a report configuration by ID.

        Args:
            config_id (int): The unique identifier of the report
                configuration to delete.
            report_type (str): The report type path segment.
                Currently only ``customapps`` is supported.

        Returns:
            tuple: (status_code, Response, error).

        Examples:
            Delete a report configuration::

                >>> _, _, err = client.zbi.report_configs.delete_report_config(1)
                >>> if err:
                ...     print(f"Error: {err}")
        """
        http_method = "DELETE"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /reports
            /{report_type}
            /{config_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.status, response, None)
