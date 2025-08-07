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


class GeoLocations(ZscalerObject):
    """
    A class for GeoLocations objects.
    """

    def __init__(self, config=None):
        """
        Initialize the GeoLocations model based on API response.

        Args:
            config (dict): A dictionary representing the Department configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.city = config["city"] if "city" in config else None
            self.state = config["state"] if "state" in config else None
            self.country = config["country"] if "country" in config else None
            self.num_devices = config["num_devices"] if "num_devices" in config else None
        else:
            self.id = None
            self.city = None
            self.state = None
            self.country = None
            self.num_devices = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "num_devices": self.num_devices,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Departments(ZscalerObject):
    """
    A class for Departments objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Departments model based on API response.

        Args:
            config (dict): A dictionary representing the Department configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.num_devices = config["num_devices"] if "num_devices" in config else None
        else:
            self.id = None
            self.name = None
            self.num_devices = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "num_devices": self.num_devices,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Locations(ZscalerObject):
    """
    A class for Locations objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Locations model based on API response.

        Args:
            config (dict): A dictionary representing the Department configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.num_devices = config["num_devices"] if "num_devices" in config else None

            if "groups" in config:
                if isinstance(config["groups"], CommonIDName):
                    self.groups = config["groups"]
                elif config["groups"] is not None:
                    self.groups = CommonIDName(config["groups"])
                else:
                    self.groups = None
            else:
                self.groups = None
        else:
            self.id = None
            self.name = None
            self.num_devices = None
            self.groups = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "num_devices": self.num_devices,
            "groups": self.groups,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CommonIDName(ZscalerObject):
    """
    A class for Groups objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Common model based on API response.

        Args:
            config (dict): A dictionary representing the Department configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.email = config["email"] if "email" in config else None
            self.score = config["score"] if "score" in config else None
        else:
            self.id = None
            self.name = None
            self.email = None
            self.score = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "score": self.score,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MostImpactedGeos(ZscalerObject):
    """
    A class for Most Impacted Geos objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Most Impacted Geos model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.city = config["city"] if "city" in config else None
            self.state = config["state"] if "state" in config else None
            self.region = config["region"] if "region" in config else None
            self.country = config["country"] if "country" in config else None
            self.geo_type = config["geo_type"] if "geo_type" in config else None
            self.geo_lat = config["geo_lat"] if "geo_lat" in config else None
            self.geo_long = config["geo_long"] if "geo_long" in config else None
            self.geo_detection = config["geo_detection"] if "geo_detection" in config else None
        else:
            self.id = None
            self.city = None
            self.state = None
            self.region = None
            self.country = None
            self.geo_type = None
            self.geo_lat = None
            self.geo_long = None
            self.geo_detection = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "city": self.city,
            "state": self.state,
            "region": self.region,
            "country": self.country,
            "geo_type": self.geo_type,
            "geo_lat": self.geo_lat,
            "geo_long": self.geo_long,
            "geo_detection": self.geo_detection,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MostImpactedRegion(ZscalerObject):
    """
    A class for Most Impacted Region objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Most Impacted Region model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.country = config["country"] if "country" in config else None

        else:
            self.id = None
            self.country = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "country": self.country,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DataPoints(ZscalerObject):
    """
    A class for DataPoints objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DataPoints model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.timestamp = config["timestamp"] if "timestamp" in config else None
            self.value = config["value"] if "value" in config else None
        else:
            self.timestamp = None
            self.value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "timestamp": self.timestamp,
            "value": self.value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


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

            self.devices = ZscalerCollection.form_list(
                config["devices"] if "devices" in config else [], CommonIDName
            )
            self.zs_loc = ZscalerCollection.form_list(
                config["zs_loc"] if "zs_loc" in config else [], CommonIDName
            )
            self.geo_loc = ZscalerCollection.form_list(
                config["geo_loc"] if "geo_loc" in config else [], MostImpactedGeos
            )
        else:
            self.devices = []
            self.zs_loc = []
            self.geo_loc = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "devices": self.devices,
            "zs_loc": self.zs_loc,
            "geo_loc": self.geo_loc,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CommonMetrics(ZscalerObject):
    """
    A class for Metrics objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Metrics model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.metric = config["metric"] if "metric" in config else None
            self.unit = config["unit"] if "unit" in config else None
            self.datapoints = ZscalerCollection.form_list(
                config["datapoints"] if "datapoints" in config else [], DataPoints
            )

        else:
            self.metric = None
            self.unit = None
            self.datapoints = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "metric": self.metric,
            "unit": self.unit,
            "datapoints": self.datapoints,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
