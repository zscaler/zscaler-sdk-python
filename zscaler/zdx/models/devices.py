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
from zscaler.zdx.models import common as common_reference


class Devices(ZscalerObject):
    """
    A class for Devices objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Devices model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)
        print(f"DEBUG: Raw config received in devices: {config}")  # Debugging input

        if config:
            self.users = ZscalerCollection.form_list(config.get("devices", []), common_reference.Common)
            self.next_offset = config["next_offset"] if "next_offset" in config else None
        else:
            self.devices = ZscalerCollection.form_list([], str)
            self.next_offset = None

        print(f"DEBUG: Parsed Devices object - {len(self.devices)} devices found")

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"devices": [device.as_dict() for device in self.devices], "next_offset": self.next_offset}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceModelInfo(ZscalerObject):
    """
    A class for DeviceModelInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceModelInfo model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.hardware = config["hardware"] if "hardware" in config else None
            self.network = ZscalerCollection.form_list(config["network"] if "network" in config else [], str)
            self.software = config["software"] if "software" in config else None
        else:
            self.id = None
            self.name = None
            self.hardware = None
            self.network = ZscalerCollection.form_list([], str)
            self.software = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "hardware": self.hardware,
            "network": self.network,
            "software": self.software,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceActiveApplications(ZscalerObject):
    """
    A class for DeviceActiveApplications objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceActiveApplications model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.score = config["score"] if "score" in config else None
        else:
            self.id = None
            self.name = None
            self.score = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"id": self.id, "name": self.name, "score": self.score}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceAppScoreTrend(ZscalerObject):
    """
    A class for DeviceAppScoreTrend objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceAppScoreTrend model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.metric = config["metric"] if "metric" in config else None
            self.datapoints = ZscalerCollection.form_list(config["datapoints"] if "datapoints" in config else [], str)
        else:
            self.metric = None
            self.datapoints = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"metric": self.metric, "datapoints": self.datapoints}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceHealthMetrics(ZscalerObject):
    """
    A class for DeviceHealthMetrics objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceHealthMetrics model based on API response.

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


class DeviceAppCloudPathProbes(ZscalerObject):
    """
    A class for DeviceAppCloudPathProbes objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceAppCloudPathProbes model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.num_probes = config["num_probes"] if "num_probes" in config else None
            self.avg_latencies = ZscalerCollection.form_list(config["avg_latencies"] if "avg_latencies" in config else [], str)
        else:
            self.id = None
            self.name = None
            self.num_probes = None
            self.avg_latencies = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "num_probes": self.num_probes,
            "avg_latencies": self.avg_latencies,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceAppWebProbes(ZscalerObject):
    """
    A class for DeviceAppWebProbes objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceAppWebProbes model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.num_probes = config["num_probes"] if "num_probes" in config else None
            self.avg_score = config["avg_score"] if "avg_score" in config else None
            self.avg_pft = config["avg_pft"] if "avg_pft" in config else None
        else:
            self.id = None
            self.name = None
            self.num_probes = None
            self.avg_score = None
            self.avg_pft = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "num_probes": self.num_probes,
            "avg_score": self.avg_score,
            "avg_pft": self.avg_pft,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceWebProbePageFetch(ZscalerObject):
    """
    A class for DeviceWebProbePageFetch objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceWebProbePageFetch model based on API response.

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


class DeviceCloudPathProbesMetric(ZscalerObject):
    """
    A class for DeviceCloudPathProbesMetric objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceCloudPathProbesMetric model based on API response.

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


class DeviceEvents(ZscalerObject):
    """
    A class for DeviceEvents objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceEvents model based on API response.

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


class DeviceCloudPathProbesHopData(ZscalerObject):
    """
    A class for DeviceCloudPathProbesHopData objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceCloudPathProbesHopData model based on API response.

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


class DeviceActiveGeo(ZscalerObject):
    """
    A class for DeviceActiveGeo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceActiveGeo model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.geo_type = config["geo_type"] if "geo_type" in config else None
            self.children = ZscalerCollection.form_list(config["children"] if "children" in config else [], str)
        else:
            self.id = None
            self.name = None
            self.geo_type = None
            self.children = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"id": self.id, "name": self.name, "geo_type": self.geo_type, "children": self.children}
        parent_req_format.update(current_obj_format)
        return parent_req_format
