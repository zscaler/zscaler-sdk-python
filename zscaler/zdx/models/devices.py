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

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.userid = config["userid"] if "userid" in config else None
            self.next_offset = config["next_offset"] if "next_offset" in config else None
        else:
            self.id = None
            self.name = None
            self.next_offset = None
            self.userid = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "next_offset": self.next_offset,
            "userid": self.userid,
        }
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
            
            self.network = ZscalerCollection.form_list(
                config["network"] if "network" in config else [], Network
            )

            if "hardware" in config:
                if isinstance(config["hardware"], Hardware):
                    self.hardware = config["hardware"]
                elif config["hardware"] is not None:
                    self.hardware = Hardware(config["hardware"])
                else:
                    self.hardware = None
            else:
                self.hardware = None

            if "software" in config:
                if isinstance(config["software"], Software):
                    self.software = config["software"]
                elif config["software"] is not None:
                    self.software = Software(config["software"])
                else:
                    self.software = None
            else:
                self.software = None
        else:
            self.id = None
            self.name = None
            self.hardware = None
            self.network = []
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


class Hardware(ZscalerObject):
    """
    A class for Hardware objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Hardware model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.hw_model = config["hw_model"] \
                if "hw_model" in config else None
            self.hw_mfg = config["hw_mfg"] \
                if "hw_mfg" in config else None
            self.hw_type = config["hw_type"] \
                if "hw_type" in config else None
            self.hw_serial = config["hw_serial"] \
                if "hw_serial" in config else None
            self.tot_mem = config["tot_mem"] \
                if "tot_mem" in config else None
            self.gpu = config["gpu"] \
                if "gpu" in config else None
            self.disk_size = config["disk_size"] \
                if "disk_size" in config else None
            self.disk_model = config["disk_model"] \
                if "disk_model" in config else None
            self.disk_type = config["disk_type"] \
                if "disk_type" in config else None
            self.cpu_mfg = config["cpu_mfg"] \
                if "cpu_mfg" in config else None
            self.cpu_model = config["cpu_model"] \
                if "cpu_model" in config else None
            self.speed_ghz = config["speed_ghz"] \
                if "speed_ghz" in config else None
            self.logical_proc = config["logical_proc"] \
                if "logical_proc" in config else None
            self.num_cores = config["num_cores"] \
                if "num_cores" in config else None
        else:
            self.hw_model = None
            self.hw_mfg = None
            self.hw_type = None
            self.hw_serial = None
            self.tot_mem = None
            self.gpu = None
            self.disk_size = None
            self.disk_model = None
            self.disk_type = None
            self.cpu_mfg = None
            self.cpu_model = None
            self.speed_ghz = None
            self.logical_proc = None
            self.num_cores = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "hw_model": self.hw_model,
            "hw_mfg": self.hw_mfg,
            "hw_type": self.hw_type,
            "hw_serial": self.hw_serial,
            "tot_mem": self.tot_mem,
            "gpu": self.gpu,
            "disk_size": self.disk_size,
            "disk_model": self.disk_model,
            "disk_type": self.disk_type,
            "cpu_mfg": self.cpu_mfg,
            "cpu_model": self.cpu_model,
            "speed_ghz": self.speed_ghz,
            "logical_proc": self.logical_proc,
            "num_cores": self.num_cores
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Network(ZscalerObject):
    """
    A class for Network objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Network model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.net_type = config["net_type"] \
                if "net_type" in config else None
            self.status = config["status"] \
                if "status" in config else None
            self.ipv4 = config["ipv4"] \
                if "ipv4" in config else None
            self.ipv6 = config["ipv6"] \
                if "ipv6" in config else None
            self.dns_srvs = config["dns_srvs"] \
                if "dns_srvs" in config else None
            self.dns_suffix = config["dns_suffix"] \
                if "dns_suffix" in config else None
            self.gateway = config["gateway"] \
                if "gateway" in config else None
            self.mac = config["mac"] \
                if "mac" in config else None
            self.guid = config["guid"] \
                if "guid" in config else None
        else:
            self.net_type = None
            self.status = None
            self.ipv4 = None
            self.ipv6 = None
            self.dns_srvs = None
            self.dns_suffix = None
            self.gateway = None
            self.mac = None
            self.guid = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "net_type": self.net_type,
            "status": self.status,
            "ipv4": self.ipv4,
            "ipv6": self.ipv6,
            "dns_srvs": self.dns_srvs,
            "dns_suffix": self.dns_suffix,
            "gateway": self.gateway,
            "mac": self.mac,
            "guid": self.guid
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
    
class Software(ZscalerObject):
    """
    A class for Software objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Software model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.os_name = config["os_name"] \
                if "os_name" in config else None
            self.os_ver = config["os_ver"] \
                if "os_ver" in config else None
            self.os_build = config["os_build"] \
                if "os_build" in config else None
            self.hostname = config["hostname"] \
                if "hostname" in config else None
            self.netbios = config["netbios"] \
                if "netbios" in config else None
            self.user = config["user"] \
                if "user" in config else None
            self.client_conn_ver = config["client_conn_ver"] \
                if "client_conn_ver" in config else None
            self.zdx_ver = config["zdx_ver"] \
                if "zdx_ver" in config else None
        else:
            self.os_name = None
            self.os_ver = None
            self.os_build = None
            self.hostname = None
            self.netbios = None
            self.user = None
            self.client_conn_ver = None
            self.zdx_ver = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "os_name": self.os_name,
            "os_ver": self.os_ver,
            "os_build": self.os_build,
            "hostname": self.hostname,
            "netbios": self.netbios,
            "user": self.user,
            "client_conn_ver": self.client_conn_ver,
            "zdx_ver": self.zdx_ver
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
