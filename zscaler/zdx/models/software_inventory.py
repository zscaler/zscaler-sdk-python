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

import ast


class SoftwareList(ZscalerObject):
    """
    A class for SoftwareList objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SoftwareList model based on API response.

        Args:
            config (dict or str): A dictionary (or string representation of a dict)
                                  representing the Software configuration.
        """
        super().__init__(config)
        if config:
            if isinstance(config, str):
                try:
                    config = ast.literal_eval(config)
                except Exception:
                    config = {}
            self.software_key = config.get("software_key") or config.get("softwareKey")
            self.software_name = config.get("software_name") or config.get("softwareName")
            self.vendor = config.get("vendor")
            self.software_group = config.get("software_group") or config.get("softwareGroup")
            self.software_install_type = (
                config.get("software_install_type") or config.get("sw_install_type") or config.get("swInstallType")
            )
            self.user_total = config.get("user_total") or config.get("userTotal")
            self.device_total = config.get("device_total") or config.get("deviceTotal")
        else:
            self.software_key = None
            self.software_name = None
            self.vendor = None
            self.software_group = None
            self.software_install_type = None
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
            "software_install_type": self.software_install_type,
            "user_total": self.user_total,
            "device_total": self.device_total,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format

    def as_dict(self):
        """
        Return a dictionary representation with snake_case keys.
        """
        return {
            "software_key": self.software_key,
            "software_name": self.software_name,
            "vendor": self.vendor,
            "software_group": self.software_group,
            "software_install_type": self.software_install_type,
            "user_total": self.user_total,
            "device_total": self.device_total,
        }


class DeviceSoftwareInventory(ZscalerObject):
    """
    A class for DeviceSoftwareInventory objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DeviceSoftwareInventory model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.software = ZscalerCollection.form_list(config["software"] if "software" in config else [], str)
            self.next_offset = config["next_offset"] if "next_offset" in config else None
        else:
            self.software = ZscalerCollection.form_list([], str)
            self.next_offset = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"software": self.software, "next_offset": self.next_offset}
        parent_req_format.update(current_obj_format)
        return parent_req_format
