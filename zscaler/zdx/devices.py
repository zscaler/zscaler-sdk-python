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
from zscaler.zdx.models.call_quality_metrics import CallQualityMetrics
from zscaler.zdx.models.devices import Devices
from zscaler.zdx.models.devices import DeviceModelInfo
from zscaler.zdx.models.devices import DeviceAppScoreTrend
from zscaler.zdx.models.devices import DeviceWebProbePageFetch
from zscaler.zdx.models.devices import DeviceAppCloudPathProbes
from zscaler.zdx.models.devices import DeviceCloudPathProbesMetric
from zscaler.zdx.models.devices import DeviceCloudPathProbesHopData
from zscaler.zdx.models.devices import DeviceActiveGeo
from zscaler.zdx.models.devices import DeviceAppWebProbes
from zscaler.zdx.models.devices import DeviceActiveApplications
from zscaler.zdx.models.devices import DeviceHealthMetrics
from zscaler.zdx.models.devices import DeviceEvents
from zscaler.utils import format_url, zdx_params


class DevicesAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zdx_base_endpoint = "/zdx/v1"

    @zdx_params
    def list_devices(self, query_params=None) -> tuple:
        """
        Returns a list of all active devices and its basic details.
        If the time range is not specified, the endpoint defaults to the previous 2 hours.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.location_id]`` {list}: The unique ID for the location.

                ``[query_params.department_id]`` {list}: The unique ID for the department.

                ``[query_params.geo_id]`` {list}: The unique ID for the geolocation.

                ``[query_params.user_ids]`` {list}: List of user IDs.

                ``[query_params.emails]`` {list}: List of email addresses.

                ``[query_params.mac_address]`` {str}: MAC address of the device.

                ``[query_params.private_ipv4]`` {str}: Private IPv4 address of the device.

                ``[query_params.offset]`` {str}: The next_offset value from the last request.
                    You must enter this value to get the next batch from the list.
                    When the next_offset value becomes null, the list is complete.

        Returns:
            :obj:`Tuple`: The list of devices in ZDX.

        Examples:
            List all devices in ZDX for the past 2 hours for the associated email addresses:

            >>> device_list, _, err = client.zdx.devices.list_devices(query_params={"emails": ['jdoe@acme.com']})
            ... if err:
            ...     print(f"Error listing devices: {err}")
            ...     return
            ... for dev in device_list:
            ...     print(dev.as_dict())

            List all devices in ZDX for the past 24 hours:

            >>> device_list, _, err = client.zdx.devices.list_devices(query_params={'since': 24})
            ... if err:
            ...     print(f"Error listing devices: {err}")
            ...     return
            ... for dev in device_list:
            ...     print(dev.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices
        """
        )

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
            result = [Devices(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_device(self, device_id: str, query_params=None) -> tuple:
        """
        Returns a single device in ZDX.

        Args:
            device_id (str): The unique ID for the device.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The ZDX device resource record.

        Examples:
            Get information for the device with an ID of 132559212.

            >>> device, _, err = client.zdx.devices.get_device('132559212')
            ... if err:
            ...     print(f"Error listing device details: {err}")
            ...     return
            ... for dev in device:
            ...     print(dev.as_dict())

            Get information for the device with an ID of 123456789 for the last 24 hours.

            >>> device, _, err = client.zdx.devices.get_device('132559212', query_params={'since': 24})
            ... if err:
            ...     print(f"Error listing device details: {err}")
            ...     return
            ... for dev in device:
            ...     print(dev.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}
        """
        )

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
            result = [DeviceModelInfo(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_device_apps(self, device_id: str, query_params=None) -> tuple:
        """
        Returns a list of all active applications for a device.

        Args:
            device_id (str): The unique ID for the device.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The list of active applications for the device.

        Examples:
            Print a list of active applications for a device.

            >>> device_app_list, _, err = client.zdx.devices.get_device_apps(
            ... '132559212', query_params={"since": 2})
            ... if err:
            ...     print(f"Error listing device app: {err}")
            ...     return
            ... for app in device_app_list:
            ...     print(app)

            Print a list of active applications for a device for the last 24 hours.

            >>> device_app_list, _, err = client.zdx.devices.get_device_apps(
            ... '132559212', query_params={"since": 24})
            ... if err:
            ...     print(f"Error listing device app: {err}")
            ...     return
            ... for app in device_app_list:
            ...     print(app)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/apps
        """
        )

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
            result = [DeviceActiveApplications(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_device_app(
        self,
        device_id: str,
        app_id: str,
        query_params=None,
    ) -> tuple:
        """
        Returns a single application for a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The application resource record.

        Examples:
            Print a single application for a device.

            >>> application, _, err = client.zdx.devices.get_device_app(device_id='1', app_id='3')
            ... if err:
            ...     print(f"Error listing application: {err}")
            ...     return
            ... for app in application:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/apps/{app_id}
        """
        )

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
            result = [DeviceAppScoreTrend(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_web_probes(self, device_id: str, app_id: str, query_params=None) -> tuple:
        """
        Returns a list of all active web probes for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The list of web probes for the application.

        Examples:
            Print a list of web probes for an application.

            >>> device_probe_list, _, err = client.zdx.devices.get_web_probes('132559212', '1')
            ... if err:
            ...     print(f"Error listing device web probes: {err}")
            ...     return
            ... for probe in device_probe_list:
            ...     print(probe)

            Print a list of web probes for an application for the past 2 hours.

            >>> device_probe_list, _, err = client.zdx.devices.get_web_probes(
            ... '132559212', '1', query_params={'since':2})
            ... if err:
            ...     print(f"Error listing device web probes: {err}")
            ...     return
            ... for probe in device_probe_list:
            ...     print(probe)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/apps/{app_id}/web-probes
        """
        )

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
            result = [DeviceAppWebProbes(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_web_probe(self, device_id: str, app_id: str, probe_id: str, query_params=None) -> tuple:
        """
        Returns a single web probe for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            probe_id (str): The unique ID for the web probe.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The web probe resource record.

        Examples:
            Print a single web probe for an application.

            >>> device_probe, _, err = client.zdx.devices.get_web_probe('132559212', '1', '33111')
            ... if err:
            ...     print(f"Error listing probe: {err}")
            ...     return
            ... for probe in device_probe:
            ...     print(probe)

            Print a single web probe for an application foir the past 2 hours.

            >>> device_probe, _, err = client.zdx.devices.get_web_probe(
            ... '132559212', '1', '33111', query_params={'since':2})
            ... if err:
            ...     print(f"Error listing probe: {err}")
            ...     return
            ... for probe in device_probe:
            ...     print(probe)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/apps/{app_id}/web-probes/{probe_id}
        """
        )

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
            result = [DeviceWebProbePageFetch(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def list_cloudpath_probes(self, device_id: str, app_id: str, query_params=None) -> tuple:
        """
        Returns a list of all active cloudpath probes for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {list}: The unique ID for the department.

        Returns:
            :obj:`Tuple`: The list of cloudpath probes for the application.

        Examples:
            Print a list of cloudpath probes for an application.

            >>> device_probe_list, _, err = client.zdx.devices.list_cloudpath_probes('132559212', '1')
            ... if err:
            ...     print(f"Error listing probe: {err}")
            ...     return
            ... for probe in device_probe_list:
            ...     print(probe)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/apps/{app_id}/cloudpath-probes
        """
        )

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
            result = [DeviceAppCloudPathProbes(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_cloudpath_probe(self, device_id: str, app_id: str, probe_id: str, query_params=None):
        """
        Returns a single cloudpath probe for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            probe_id (str): The unique ID for the cloudpath probe.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The cloudpath probe resource record.

        Examples:
            Print a single cloudpath probe for an application.

            >>> device_probe, _, err = client.zdx.devices.get_cloudpath_probe('132559212', '1', '33112')
            ... if err:
            ...     print(f"Error listing device probe: {err}")
            ...     return
            ... for probe in device_probe:
            ...     print(probe)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/apps/{app_id}/cloudpath-probes/{probe_id}
        """
        )

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
            result = [DeviceCloudPathProbesMetric(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_cloudpath(self, device_id: str, app_id: str, probe_id: str, query_params=None) -> tuple:
        """
        Returns a single cloudpath for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            probe_id (str): The unique ID for the cloudpath probe.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The cloudpath resource record.

        Examples:
            Print a single cloudpath for an application for the past 2 hours

            >>> device_probe, _, err = client.zdx.devices.get_cloudpath(
            ... '132559212', '1', '33112', query_params={"since": 2})
            ... if err:
            ...     print(f"Error listing device probe: {err}")
            ...     return
            ... for probe in device_probe:
            ...     print(probe)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/apps/{app_id}/cloudpath-probes/{probe_id}/cloudpath
        """
        )

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
            result = [DeviceCloudPathProbesHopData(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_call_quality_metrics(self, device_id: str, app_id: str, query_params=None) -> tuple:
        """
        Returns a single call quality metrics for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The call quality metrics resource record.

        Examples:
            Print call quality metrics for an application.

            >>> metrics = zdx.devices.get_call_quality_metrics('123456789', '987654321')
            ... print(metrics)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/apps/{app_id}/call-quality-metrics
        """
        )

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
            result = [CallQualityMetrics(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_health_metrics(self, device_id: str, query_params=None) -> tuple:
        """
        Returns health metrics trend for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The health metrics resource record.

        Examples:
            Print health metrics for an application.

            >>> metric_list, _, err = client.zdx.devices.get_health_metrics('132559212', query_params={"since": 2})
            ... if err:
            ...     print(f"Error listing health metrics: {err}")
            ...     return
            ... for metric in metric_list:
            ...     print(metric)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/health-metrics
        """
        )

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
            result = [DeviceHealthMetrics(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_events(self, device_id: str, query_params=None) -> tuple:
        """
        Returns a list of all events for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The list of events for the device.

        Examples:
            Print a list of events for a device.

            >>> device_event_list, _, err = client.zdx.devices.get_events('132559212', query_params={"since": 2})
            ... if err:
            ...     print(f"Error listing events: {err}")
            ...     return
            ... for event in device_event_list:
            ...     print(event)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /devices/{device_id}/events
        """
        )

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
            result = [DeviceEvents(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def list_geolocations(self, query_params=None) -> tuple:
        """
        Returns a list of all active geolocations configured within the ZDX tenant.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.location_id]`` {str}: The unique ID for the location.

                ``[query_params.parent_geo_id]`` {str}: The unique ID for the parent geolocation.

                ``[query_params.q]`` {str}: The search string to filter by name.

        Returns:
            :obj:`Tuple`: The list of geolocations in ZDX.

        Examples:
            List all geolocations in ZDX for the past 2 hours:

            >>> location_list, _, err = client.zdx.devices.list_geolocations(query_params={"parent_geo_id": '0.0.ca'})
            ... if err:
            ...     print(f"Error listing geolocations: {err}")
            ...     return
            ... for location in location_list:
            ...     print(location)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /active_geo
        """
        )

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
            result = [DeviceActiveGeo(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
