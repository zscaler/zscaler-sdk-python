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


class TrafficGRERecommendedVIP(ZscalerObject):
    """
    A class for Traffic GRE Recommended VIPs objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TrafficGRERecommendedVIP model based on API response.

        Args:
            config (dict): A dictionary representing the GRE VIP configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.virtual_ip = config["virtualIp"] if "virtualIp" in config else None
            self.private_service_edge = config["privateServiceEdge"] if "privateServiceEdge" in config else None
            self.datacenter = config["datacenter"] if "datacenter" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.city = config["city"] if "city" in config else None
            self.country_code = config["countryCode"] if "countryCode" in config else None
            self.region = config["region"] if "region" in config else None
        else:
            # Initialize with default None or 0 values
            self.id = None
            self.virtual_ip = None
            self.private_service_edge = False
            self.datacenter = None
            self.latitude = None
            self.longitude = None
            self.city = None
            self.country_code = None
            self.region = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "virtualIp": self.virtual_ip,
            "privateServiceEdge": self.private_service_edge,
            "datacenter": self.datacenter,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city": self.city,
            "countryCode": self.country_code,
            "region": self.region,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
