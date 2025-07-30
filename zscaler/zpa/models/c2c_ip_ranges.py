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


class IpRanges(ZscalerObject):
    """
    A class for IpRanges objects.
    """

    def __init__(self, config=None):
        """
        Initialize the IpRanges model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.available_ips = config["availableIps"] \
                if "availableIps" in config else None
            self.country_code = config["countryCode"] \
                if "countryCode" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.customer_id = config["customerId"] \
                if "customerId" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.ip_range_begin = config["ipRangeBegin"] \
                if "ipRangeBegin" in config else None
            self.ip_range_end = config["ipRangeEnd"] \
                if "ipRangeEnd" in config else None
            self.is_deleted = config["isDeleted"] \
                if "isDeleted" in config else None
            self.latitude_in_db = config["latitudeInDb"] \
                if "latitudeInDb" in config else None
            self.location = config["location"] \
                if "location" in config else None
            self.location_hint = config["locationHint"] \
                if "locationHint" in config else None
            self.longitude_in_db = config["longitudeInDb"] \
                if "longitudeInDb" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.sccm_flag = config["sccmFlag"] \
                if "sccmFlag" in config else None
            self.subnet_cidr = config["subnetCidr"] \
                if "subnetCidr" in config else None
            self.total_ips = config["totalIps"] \
                if "totalIps" in config else None
            self.used_ips = config["usedIps"] \
                if "usedIps" in config else None
        else:
            self.available_ips = None
            self.country_code = None
            self.creation_time = None
            self.customer_id = None
            self.description = None
            self.enabled = None
            self.id = None
            self.ip_range_begin = None
            self.ip_range_end = None
            self.is_deleted = None
            self.latitude_in_db = None
            self.location = None
            self.location_hint = None
            self.longitude_in_db = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.sccm_flag = None
            self.subnet_cidr = None
            self.total_ips = None
            self.used_ips = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "availableIps": self.available_ips,
            "countryCode": self.country_code,
            "creationTime": self.creation_time,
            "customerId": self.customer_id,
            "description": self.description,
            "enabled": self.enabled,
            "id": self.id,
            "ipRangeBegin": self.ip_range_begin,
            "ipRangeEnd": self.ip_range_end,
            "isDeleted": self.is_deleted,
            "latitudeInDb": self.latitude_in_db,
            "location": self.location,
            "locationHint": self.location_hint,
            "longitudeInDb": self.longitude_in_db,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "sccmFlag": self.sccm_flag,
            "subnetCidr": self.subnet_cidr,
            "totalIps": self.total_ips,
            "usedIps": self.used_ips
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
