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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zdx.models.troubleshooting import DeviceDeepTraces
from zscaler.zdx.models.troubleshooting import TraceDetails
from zscaler.zdx.models.troubleshooting import DeviceTopProcesses
from zscaler.zdx.models.troubleshooting import DeepTraceWebProbeMetrics
from zscaler.zdx.models.troubleshooting import DeepTraceCloudPathMetric
from zscaler.zdx.models.troubleshooting import DeepTraceCloudPath
from zscaler.zdx.models.troubleshooting import DeepTraceHealthMetrics
from zscaler.zdx.models.troubleshooting import DeepTraceEvents
from zscaler.zdx.models.troubleshooting import DeviceApplicationAnalysis
from zscaler.utils import format_url, zdx_params


class TroubleshootingAPI(APIClient):
    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zdx_base_endpoint = "/zdx/v1"

    def list_deeptraces(self, device_id: str) -> List[DeviceDeepTraces]:
        """
        Returns a list of all deep traces for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Returns:
            :obj:`Tuple`:: The list of deep traces for the device.

        Examples:
            Print a list of deep traces for a device.

            >>> try:
            ...     trace_list = client.zdx.troubleshooting.list_deeptraces('132559212')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request, DeviceDeepTraces)
        results = []
        for item in response.get_results():
            results.append(DeviceDeepTraces(item))
        return (results, response, None)

    def get_deeptrace(self, device_id: str, trace_id: str) -> Any:
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

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [DeviceDeepTraces(self.form_response_body(response.get_body()))]
        return result

    def start_deeptrace(self, device_id: str, **kwargs) -> TraceDetails:
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

        request = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response = self._request_executor.execute(request, TraceDetails)
        result = TraceDetails(self.form_response_body(response.get_body()))
        return result

    def delete_deeptrace(self, device_id: str, trace_id: str) -> None:
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
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None

    def list_top_processes(
        self,
        device_id: str,
        trace_id: str,
    ) -> List[DeviceTopProcesses]:
        """
        Returns a list of all deep traces for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Returns:
            :obj:`Tuple`:: The list of deep traces for the device.

        Examples:
            Print a list of deep traces for a device.

            >>> try:
            ...     processes_list = client.zdx.troubleshooting.list_top_processes('132559212', '342821739939272')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [DeviceTopProcesses(self.form_response_body(response.get_body()))]
        return result

    def get_deeptrace_webprobe_metrics(self, device_id: str, trace_id: str) -> Any:
        """
        Returns web probe metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace web probe metrics.

        Examples:
            Print web probe metrics for a deeptrace.

            >>> try:
            ...     metrics_list = client.zdx.troubleshooting.get_deeptrace_webprobe_metrics(
                '132559212', '342941739947287')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [DeepTraceWebProbeMetrics(self.form_response_body(response.get_body()))]
        return result

    def get_deeptrace_cloudpath_metrics(self, device_id: str, trace_id: str) -> Any:
        """
        Returns cloudpath metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace cloudpath metrics.

        Examples:
            Print cloudpath metrics for a deeptrace.

            >>> try:
            ...     path_matric = client.zdx.troubleshooting.get_deeptrace_cloudpath_metrics(
                '132559212', '342941739947287')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [DeepTraceCloudPathMetric(self.form_response_body(response.get_body()))]
        return result

    def get_deeptrace_cloudpath(self, device_id: str, trace_id: str) -> Any:
        """
        Returns cloudpath for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace cloudpath.

        Examples:
            Print cloudpath for a deeptrace.

            >>> try:
            ...     cloud_path_list = client.zdx.troubleshooting.get_deeptrace_cloudpath('132559212', '342941739947287')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [DeepTraceCloudPath(self.form_response_body(response.get_body()))]
        return result

    def get_deeptrace_health_metrics(self, device_id: str, trace_id: str) -> Any:
        """
        Returns health metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace health metrics.

        Examples:
            Print health metrics for a deeptrace.

            >>> try:
            ...     health_metrics = client.zdx.troubleshooting.get_deeptrace_health_metrics(
                '132559212', '342941739947287')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [DeepTraceHealthMetrics(self.form_response_body(response.get_body()))]
        return result

    def get_deeptrace_events(self, device_id: str, trace_id: str) -> Any:
        """
        Returns events for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace events.

        Examples:
            Print events for a deeptrace.

            >>> try:
            ...     trace_events_list = client.zdx.troubleshooting.get_deeptrace_events('132559212', '342941739947287')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [DeepTraceEvents(self.form_response_body(response.get_body()))]
        return result

    def start_analysis(self, **kwargs) -> DeviceApplicationAnalysis:
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

        request = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response = self._request_executor.execute(request, DeviceApplicationAnalysis)
        result = DeviceApplicationAnalysis(self.form_response_body(response.get_body()))
        return result

    def get_analysis(
        self,
        analysis_id: str,
    ) -> Any:
        """
        Returns status of the score analysis (e.g., progress or results).
        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Tuple`: The deeptrace health metrics.

        Examples:
            Print health metrics for a deeptrace.

            >>> try:
            ...     trace_analysis_list = client.zdx.troubleshooting.get_analysis('132559212', '342821739939272')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [self.form_response_body(response.get_body())]
        return result

    def delete_analysis(
        self,
        analysis_id: str,
    ) -> None:
        """
        Stop the score analysis that is currently running.

        Args:
            analysis_id (str): The unique ID for the device.

        Returns:
            :obj:`str`: The analysis ID that was deleted.

        Examples:
            Delete a single deeptrace for a device.

            >>> _, zscaler_resp, err = client.zdx.troubleshooting.delete_analysis('123456789')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None
