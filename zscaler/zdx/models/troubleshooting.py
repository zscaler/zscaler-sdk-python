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

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class DeviceDeepTraces(ZscalerObject):
    """
    A class for DeviceDeepTraces objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceDeepTraces model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.trace_id = config.get("trace_id")
            self.trace_details = config.get("trace_details")
            self.status = config.get("status")
            self.created_at = config.get("created_at")
            self.started_at = config.get("started_at")
            self.ended_at = config.get("ended_at")
            self.expected_time_minutes = config.get("expected_time_minutes")
        else:
            self.trace_id = None
            self.trace_details = None
            self.status = None
            self.created_at = None
            self.started_at = None
            self.ended_at = None
            self.expected_time_minutes = None


class StartDeepTrace(ZscalerObject):
    """
    A class for StartDeepTrace objects.
    """

    def __init__(self, config=None):
        """
        Initialize the StartDeepTrace model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.trace_id = config["trace_id"] if "trace_id" in config else None
            self.session_name = (
                config["trace_details"]["session_name"]
                if "trace_details" in config and "session_name" in config["trace_details"]
                else None
            )
            self.user_id = (
                config["trace_details"]["user_id"]
                if "trace_details" in config and "user_id" in config["trace_details"]
                else None
            )
            self.username = (
                config["trace_details"]["username"]
                if "trace_details" in config and "username" in config["trace_details"]
                else None
            )
            self.device_id = (
                config["trace_details"]["device_id"]
                if "trace_details" in config and "device_id" in config["trace_details"]
                else None
            )
            self.device_name = (
                config["trace_details"]["device_name"]
                if "trace_details" in config and "device_name" in config["trace_details"]
                else None
            )
            self.session_length_minutes = (
                config["trace_details"]["session_length_minutes"]
                if "trace_details" in config and "session_length_minutes" in config["trace_details"]
                else None
            )
            self.probe_device = (
                config["trace_details"]["probe_device"]
                if "trace_details" in config and "probe_device" in config["trace_details"]
                else None
            )
            self.status = config["status"] if "status" in config else None
            self.expected_time_minutes = config["expected_time_minutes"] if "expected_time_minutes" in config else None
            self.created_at = config["created_at"] if "created_at" in config else None
            self.started_at = config["started_at"] if "started_at" in config else None
            self.ended_at = config["ended_at"] if "ended_at" in config else None
        else:
            self.trace_id = None
            self.session_name = None
            self.user_id = None
            self.username = None
            self.device_id = None
            self.device_name = None
            self.session_length_minutes = None
            self.probe_device = None
            self.status = None
            self.expected_time_minutes = None
            self.created_at = None
            self.started_at = None
            self.ended_at = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "trace_id": self.trace_id,
            "session_name": self.session_name,
            "user_id": self.user_id,
            "username": self.username,
            "device_id": self.device_id,
            "device_name": self.device_name,
            "session_length_minutes": self.session_length_minutes,
            "probe_device": self.probe_device,
            "status": self.status,
            "expected_time_minutes": self.expected_time_minutes,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceTopProcesses(ZscalerObject):
    """
    A class for DeviceTopProcesses objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceTopProcesses model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.timestamp = config["timestamp"] if "timestamp" in config else None
            self.top_processes = ZscalerCollection.form_list(config["top_processes"] if "top_processes" in config else [], str)
        else:
            self.timestamp = None
            self.top_processes = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"timestamp": self.timestamp, "top_processes": self.top_processes}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeepTraceWebProbeMetrics(ZscalerObject):
    """
    A class for DeepTraceWebProbeMetrics objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeepTraceWebProbeMetrics model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.metric = config["metric"] if "metric" in config else None
            self.unit = config["unit"] if "unit" in config else None
            self.datapoints = ZscalerCollection.form_list(config["datapoints"] if "datapoints" in config else [], str)
        else:
            self.metric = None
            self.unit = None
            self.datapoints = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"metric": self.metric, "unit": self.unit, "datapoints": self.datapoints}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeepTraceCloudPathMetric(ZscalerObject):
    """
    A class for DeepTraceCloudPathMetric objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeepTraceCloudPathMetric model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.leg_src = config["leg_src"] if "leg_src" in config else None
            self.leg_dst = config["leg_dst"] if "leg_dst" in config else None
            self.stats = ZscalerCollection.form_list(config["stats"] if "stats" in config else [], str)
        else:
            self.leg_src = None
            self.leg_dst = None
            self.stats = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"leg_src": self.leg_src, "leg_dst": self.leg_dst, "stats": self.stats}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeepTraceCloudPath(ZscalerObject):
    """
    A class for DeepTraceCloudPath objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeepTraceCloudPath model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.timestamp = config["timestamp"] if "timestamp" in config else None
            self.cloudpath = config["cloudpath"] if "cloudpath" in config else None
        else:
            self.timestamp = None
            self.cloudpath = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"timestamp": self.timestamp, "cloudpath": self.cloudpath}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeepTraceHealthMetrics(ZscalerObject):
    """
    A class for DeepTraceHealthMetrics objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeepTraceHealthMetrics model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.category = config["category"] if "category" in config else None
            self.instances = ZscalerCollection.form_list(config["instances"] if "instances" in config else [], str)
        else:
            self.category = None
            self.instances = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"category": self.category, "instances": self.instances}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeepTraceEvents(ZscalerObject):
    """
    A class for DeepTraceEvents objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeepTraceEvents model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.timestamp = config["timestamp"] if "timestamp" in config else None
            self.events = ZscalerCollection.form_list(config["events"] if "events" in config else [], str)
        else:
            self.timestamp = None
            self.events = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"timestamp": self.timestamp, "events": self.events}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceApplicationAnalysis(ZscalerObject):
    """
    A class for DeviceApplicationAnalysis objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceApplicationAnalysis model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.device_id = config["device_id"] if "device_id" in config else None
            self.app_id = config["app_id"] if "app_id" in config else None
            self.t0 = config["t0"] if "t0" in config else None
            self.t1 = config["t1"] if "t1" in config else None
        else:
            self.device_id = None
            self.app_id = None
            self.t0 = None
            self.t1 = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"device_id": self.device_id, "app_id": self.app_id, "t0": self.t0, "t1": self.t1}
        parent_req_format.update(current_obj_format)
        return parent_req_format
