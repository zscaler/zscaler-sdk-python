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


class IOTReport(ZscalerObject):
    """
    A class for IOTReport objects.
    """

    def __init__(self, config=None):
        """
        Initialize the IOTReport model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.cloud_name = config["cloudName"] if "cloudName" in config else None
            self.customer_id = config["customerId"] if "customerId" in config else None

            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], Devices)
        else:
            self.cloud_name = None
            self.customer_id = None
            self.devices = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "cloudName": self.cloud_name,
            "customerId": self.customer_id,
            "devices": self.devices,
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
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.location_id = config["locationId"] if "locationId" in config else None
            self.device_uuid = config["deviceUuid"] if "deviceUuid" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.device_type_uuid = config["deviceTypeUuid"] if "deviceTypeUuid" in config else None
            self.auto_label = config["autoLabel"] if "autoLabel" in config else None
            self.classification_uuid = config["classificationUuid"] if "classificationUuid" in config else None
            self.category_uuid = config["categoryUuid"] if "categoryUuid" in config else None
            self.flow_start_time = config["flowStartTime"] if "flowStartTime" in config else None
            self.flow_end_time = config["flowEndTime"] if "flowEndTime" in config else None
        else:
            self.location_id = None
            self.device_uuid = None
            self.ip_address = None
            self.device_type_uuid = None
            self.auto_label = None
            self.classification_uuid = None
            self.category_uuid = None
            self.flow_start_time = None
            self.flow_end_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "cloudName": self.location_id,
            "customerId": self.device_uuid,
            "devices": self.ip_address,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
