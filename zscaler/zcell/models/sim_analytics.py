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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject


class SimAnalytics(ZscalerObject):
    """
    A class representing a SimAnalytics object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.iccid = ZscalerCollection.form_list(config["iccid"] if "iccid" in config else [], str)
            self.imsi = ZscalerCollection.form_list(config["imsi"] if "imsi" in config else [], str)
            self.lat = config["lat"] if "lat" in config else None
            self.lng = config["lng"] if "lng" in config else None
            self.tags = ZscalerCollection.form_list(config["tags"] if "tags" in config else [], str)
        else:
            self.iccid = []
            self.imsi = []
            self.lat = None
            self.lng = None
            self.tags = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iccid": self.iccid,
            "imsi": self.imsi,
            "lat": self.lat,
            "lng": self.lng,
            "tags": self.tags,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MapCoordinateRequest(ZscalerObject):
    """
    A class representing a MapCoordinateRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.icc_ids = ZscalerCollection.form_list(config["iccIds"] if "iccIds" in config else [], str)
        else:
            self.icc_ids = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iccIds": self.icc_ids,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimSummary(ZscalerObject):
    """
    A class representing a SimSummary object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.total = config["total"] if "total" in config else None
            self.used = config["used"] if "used" in config else None
            self.active = config["active"] if "active" in config else None
            self.inactive = config["inactive"] if "inactive" in config else None
        else:
            self.total = None
            self.used = None
            self.active = None
            self.inactive = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "total": self.total,
            "used": self.used,
            "active": self.active,
            "inactive": self.inactive,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimCountryUsage(ZscalerObject):
    """
    A class representing a SimCountryUsage object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.country = config["country"] if "country" in config else None
            self.usage = config["usage"] if "usage" in config else None
        else:
            self.country = None
            self.usage = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "country": self.country,
            "usage": self.usage,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimDayUsage(ZscalerObject):
    """
    A class representing a SimDayUsage object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.usage = config["usage"] if "usage" in config else None
        else:
            self.creation_time = None
            self.usage = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "usage": self.usage,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimUsage(ZscalerObject):
    """
    A class representing a SimUsage object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.iccid = config["iccid"] if "iccid" in config else None
            self.usage = config["usage"] if "usage" in config else None
        else:
            self.iccid = None
            self.usage = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iccid": self.iccid,
            "usage": self.usage,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
