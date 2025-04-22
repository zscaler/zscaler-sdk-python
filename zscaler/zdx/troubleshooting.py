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
from zscaler.zdx.models.troubleshooting import DeviceDeepTraces
from zscaler.zdx.models.troubleshooting import StartDeepTrace
from zscaler.zdx.models.troubleshooting import DeviceTopProcesses
from zscaler.zdx.models.troubleshooting import DeepTraceWebProbeMetrics
from zscaler.zdx.models.troubleshooting import DeepTraceCloudPathMetric
from zscaler.zdx.models.troubleshooting import DeepTraceCloudPath
from zscaler.zdx.models.troubleshooting import DeepTraceHealthMetrics
from zscaler.zdx.models.troubleshooting import DeepTraceEvents
from zscaler.zdx.models.troubleshooting import DeviceApplicationAnalysis
from zscaler.utils import format_url, zdx_params


class TroubleshootingAPI(APIClient):
    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zdx_base_endpoint = "/zdx/v1"

    @zdx_params
    def list_deeptraces(self, device_id: str, query_params=None) -> tuple:
        """
        Returns a list of all deep traces for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Returns:
            :obj:`Tuple`:: The list of deep traces for the device.

        Examples:
            Print a list of deep traces for a device.

            >>> trace_list, _, err = client.zdx.troubleshooting.list_deeptraces('132559212')
            ... if err:
            ...     print(f"Error listing deep traces: {err}")
            ...     return
            ... for trace in trace_list:
            ...     print(trace.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces
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
                results.append(DeviceDeepTraces(item))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_deeptrace(self, device_id: str, trace_id: str) -> tuple:
        """
        Returns information on a single deeptrace for a specific device.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace resource record.

        Examples:
            Print a single deeptrace for a device.

            >>> device_trace, _, error = client.zdx.troubleshooting.get_deeptrace('132559212', '342941739947287')
            ... if error:
            ...         print(f"Error: {error}")
            ... else:
            ...         for trace in device_trace:
            ...             print(trace.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces/{trace_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [DeviceDeepTraces(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def start_deeptrace(self, device_id: str, **kwargs) -> tuple:
        """
        Starts a deep trace for a specific device and application.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            session_name (str): The name of the deeptrace session.

        Keyword Args:
            web_probe_id (str): The unique ID for the Web probe.
            cloudpath_probe_id (str): The unique ID for the Cloudpath probe.
            session_length_minutes (int): The duration of the deeptrace session in minutes. Defaults to 5.
                Supported values: `5`, `15`, `30`, `60`
            probe_device (bool): Whether to probe the device.

        Returns:
            :obj:`Tuple`: The deeptrace resource record.

        Examples:
            Start a deeptrace for a device.

            >>> start_trace, response, error = client.zdx.troubleshooting.start_deeptrace(
            ...     device_id='132559212',
            ...     session_name='DeepTrace01',
            ...     session_length_minutes=5,
            ...     probe_device=True
        )
            ... if error:
            ...     print(f"Error starting trace: {error}")
            ...     return
            ... print(f"Trace Started successfully: {start_trace.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces
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

        response, error = self._request_executor.execute(request, StartDeepTrace)
        if error:
            return (None, response, error)

        try:
            result = StartDeepTrace(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_deeptrace(self, device_id: str, trace_id: str) -> tuple:
        """
        Deletes a single deeptrace session and associated data for a specific device.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`str`: The trace ID that was deleted.

        Examples:
            Delete a single deeptrace for a device.

            >>> _, zscaler_resp, err = client.zdx.troubleshooting.delete_deeptrace('123456789', '987654321')
            ... if err:
            ...     print(f"Error deleting trace: {err}")
            ...     return
            ... print(f"Trace with ID {trace_id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces/{trace_id}
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

    def list_top_processes(
        self,
        device_id: str,
        trace_id: str,
    ) -> tuple:
        """
        Returns a list of all deep traces for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Returns:
            :obj:`Tuple`:: The list of deep traces for the device.

        Examples:
            Print a list of deep traces for a device.

            >>> processes_list, _, err = client.zdx.troubleshooting.list_top_processes('132559212', '342821739939272')
            ... if err:
            ...     print(f"Error listing top processes: {err}")
            ...     return
            ... for process in processes_list:
            ...     print(process.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces/{trace_id}/top-processes
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [DeviceTopProcesses(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_deeptrace_webprobe_metrics(self, device_id: str, trace_id: str) -> tuple:
        """
        Returns web probe metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace web probe metrics.

        Examples:
            Print web probe metrics for a deeptrace.

            >>> metrics_list, _, err = client.zdx.troubleshooting.get_deeptrace_webprobe_metrics(
                '132559212', '342941739947287')
            ... if err:
            ...     print(f"Error listing web probe metrics: {err}")
            ...     return
            ... for metric in metrics_list:
            ...     print(metric.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces/{trace_id}/webprobe-metrics
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [DeepTraceWebProbeMetrics(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_deeptrace_cloudpath_metrics(self, device_id: str, trace_id: str) -> tuple:
        """
        Returns cloudpath metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace cloudpath metrics.

        Examples:
            Print cloudpath metrics for a deeptrace.

            >>> path_matric, _, err = client.zdx.troubleshooting.get_deeptrace_cloudpath_metrics(
                '132559212', '342941739947287')
            ... if err:
            ...     print(f"Error listing cloud path metrics: {err}")
            ...     return
            ... for process in path_matric:
            ...     print(process.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces/{trace_id}/cloudpath-metrics
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [DeepTraceCloudPathMetric(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_deeptrace_cloudpath(self, device_id: str, trace_id: str) -> tuple:
        """
        Returns cloudpath for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace cloudpath.

        Examples:
            Print cloudpath for a deeptrace.

            >>> cloud_path_list, _, err = client.zdx.troubleshooting.get_deeptrace_cloudpath('132559212', '342941739947287')
            ... if err:
            ...     print(f"Error listing cloud path: {err}")
            ...     return
            ... for process in cloud_path_list:
            ...     print(process.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces/{trace_id}/cloudpath
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [DeepTraceCloudPath(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_deeptrace_health_metrics(self, device_id: str, trace_id: str) -> tuple:
        """
        Returns health metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace health metrics.

        Examples:
            Print health metrics for a deeptrace.

            >>> health_metrics, _, err = client.zdx.troubleshooting.get_deeptrace_health_metrics(
                '132559212', '342941739947287')
            ... if err:
            ...     print(f"Error listing health metrics: {err}")
            ...     return
            ... for metric in health_metrics:
            ...     print(metric.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces/{trace_id}/health-metrics
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [DeepTraceHealthMetrics(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_deeptrace_events(self, device_id: str, trace_id: str) -> tuple:
        """
        Returns events for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace events.

        Examples:
            Print events for a deeptrace.

            >>> trace_events_list, _, err = client.zdx.troubleshooting.get_deeptrace_events('132559212', '342941739947287')
            ... if err:
            ...     print(f"Error listing trace event list: {err}")
            ...     return
            ... for event in trace_events_list:
            ...     print(event.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/deeptraces/{trace_id}/events
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [DeepTraceEvents(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def start_analysis(self, **kwargs) -> tuple:
        """
        Starts a ZDX Score analysis on a device for a specific application.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            t0 (int):
            t1 (int):

        Returns:
            :obj:`Tuple`: The deeptrace resource record.

        Examples:
            Start a deeptrace for a device.

            >>> start_analysis, response, error = client.zdx.troubleshooting.start_analysis(
            ...     device_id='132559212',
            ...     app_id='1',
            ... )
            ... if error:
            ...     print(f"Error starting analysis: {error}")
            ...     return
            ... print(f"Analysis Started successfully: {start_analysis.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /analysis
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

        response, error = self._request_executor.execute(request, DeviceApplicationAnalysis)
        if error:
            return (None, response, error)

        try:
            result = DeviceApplicationAnalysis(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_analysis(
        self,
        analysis_id: str,
    ) -> tuple:
        """
        Returns status of the score analysis (e.g., progress or results).
        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace health metrics.

        Examples:
            Print health metrics for a deeptrace.

            >>> trace_analysis_list, _, err = client.zdx.troubleshooting.get_analysis('132559212', '342821739939272')
            ...  if err:
            ...     print(f"Error listing trace analysis list: {err}")
            ...     return
            ... for trace in trace_analysis_list:
            ...     print(trace.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /analysis/{analysis_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [self.form_response_body(response.get_body())]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_analysis(
        self,
        analysis_id: str,
    ) -> tuple:
        """
        Stop the score analysis that is currently running.

        Args:
            analysis_id (str): The unique ID for the device.

        Returns:
            :obj:`str`: The analysis ID that was deleted.

        Examples:
            Delete a single deeptrace for a device.

            >>> _, zscaler_resp, err = client.zdx.troubleshooting.delete_analysis('123456789')
            ... if err:
            ...     print(f"Error deleting trace: {err}")
            ...     return
            ... print(f"Trace Analysis with ID {trace_id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /analysis/{analysis_id}
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
