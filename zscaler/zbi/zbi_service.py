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

from zscaler.request_executor import RequestExecutor
from zscaler.zbi.custom_apps import CustomAppsAPI
from zscaler.zbi.report_configs import ReportConfigsAPI
from zscaler.zbi.reports import ReportsAPI


class ZBIService:
    """Zscaler Business Insights (ZBI) service client."""

    def __init__(self, request_executor: RequestExecutor) -> None:
        self._request_executor = request_executor

    @property
    def custom_apps(self) -> CustomAppsAPI:
        """
        The interface object for the
        :ref:`ZBI Custom Applications API <zbi-custom_apps>`.
        """
        return CustomAppsAPI(self._request_executor)

    @property
    def report_configs(self) -> ReportConfigsAPI:
        """
        The interface object for the
        :ref:`ZBI Report Configurations API <zbi-report_configs>`.
        """
        return ReportConfigsAPI(self._request_executor)

    @property
    def reports(self) -> ReportsAPI:
        """
        The interface object for the
        :ref:`ZBI Reports API <zbi-reports>`.
        """
        return ReportsAPI(self._request_executor)
