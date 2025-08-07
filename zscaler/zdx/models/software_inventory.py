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


class SoftwareList(ZscalerObject):
    """
    A class for SoftwareList objects.
    """

    def __init__(self, config=None):
        """
                Initialize the SoftwareList model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.next_offset = config["next_offset"] if "next_offset" in config else None

            self.software = ZscalerCollection.form_list(
                config["software"] if "software" in config else [], DeviceSoftwareInventory
            )
        else:
            self.next_offset = None
            self.devices = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "next_offset": self.next_offset,
            "software": self.software,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeviceSoftwareInventory(ZscalerObject):
    """
    A class for DeviceSoftwareInventory objects.
    """

    def __init__(self, config=None):
        """
        Initialize the overview about your organization's distribution of software associated with an alert rule model

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.software_key = config["software_key"] if "software_key" in config else None
            self.software_name = config["software_name"] if "software_name" in config else None
            self.vendor = config["vendor"] if "vendor" in config else None
            self.software_group = config["software_group"] if "software_group" in config else None
            self.sw_install_type = config["software_install_type"] if "software_install_type" in config else None
            self.user_total = config["user_total"] if "user_total" in config else None
            self.device_total = config["device_total"] if "device_total" in config else None
        else:
            self.software_key = None
            self.software_name = None
            self.vendor = None
            self.software_group = None
            self.sw_install_type = None
            self.user_total = None
            self.device_total = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "software_key": self.software_key,
            "software_name": self.software_name,
            "vendor": self.vendor,
            "software_group": self.software_group,
            "sw_install_type": self.sw_install_type,
            "user_total": self.user_total,
            "device_total": self.device_total,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
