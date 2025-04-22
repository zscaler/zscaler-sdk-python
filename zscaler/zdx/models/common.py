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
            self.groups = Common(config["groups"]) if "groups" in config else None
            self.application = Common(config["application"]) if "application" in config else None
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


class Common(ZscalerObject):
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
        else:
            self.id = None
            self.name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
