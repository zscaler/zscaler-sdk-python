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
from zscaler.zwa.models.audit_logs import AuditLogs
from zscaler.utils import format_url


class AuditLogsAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zwa_base_endpoint = "/zwa/dlp/v1"

    def audit_logs(self, query_params=None, fields=None, time_range=None, **kwargs) -> tuple:
        """
        Filters audit logs based on the specified time period and field values.

        The result includes audit information for every action made by the admins
        in the Workflow Automation Admin Portal and the actions made through APIs.

        **Supported field values**:

        - ``Action``
        - ``Resource``
        - ``Admin``
        - ``Module``

        **Supported time range values**:

        - ``Start date and time``
        - ``End date and time``

        Args:
            query_params (dict, optional): Map of query parameters for the request.

                - ``page`` (int, optional): Specifies the page number of the incident in a multi-paginated response.
                        This field is not required if ``page_id`` is used.

                - ``page_size`` (int, optional): Specifies the page size (i.e., number of incidents per page). Max: 100.

                - ``page_id`` (str, optional): Specifies the page ID of the incident in a multi-paginated response.
                        The page ID can be used instead of the page number.

            fields (list, optional): A list of field filters.

                Example:

                .. code-block:: python

                    [
                        {"name": "severity", "value": ["high"]},
                        {"name": "status", "value": ["open", "resolved"]}
                    ]

            time_range (dict, optional): Time range for filtering incidents.

                Example:

                .. code-block:: python

                    {
                        "startTime": "2025-03-03T18:04:52.074Z",
                        "endTime": "2025-03-03T18:04:52.074Z"
                    }

        Returns:
            tuple: The audit log search results.

        Examples:
            Perform an audit log search with a severity filter:

            .. code-block:: python

                search, _, error = client.zwa.incident_search.audit_logs(
                    fields=[{"name": "severity", "value": ["high"]}],
                    time_range={"startTime": "2025-03-03T18:04:52.074Z", "endTime": "2025-03-03T18:04:52.074Z"}
                )

            If an error occurs:

            .. code-block:: python

                if error:
                    print(f"Error fetching audit logs: {error}")
                else:
                    for log in search:
                        print(log.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zwa_base_endpoint}/customer/audit")

        query_params = query_params or {}

        body = {"fields": fields or [], "timeRange": time_range or {}}

        body.update(kwargs)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            params=query_params,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AuditLogs)
        if error:
            return (None, response, error)

        try:
            result = AuditLogs(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
