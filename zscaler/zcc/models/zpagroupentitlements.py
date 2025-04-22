# flake8: noqa
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

# AUTO-GENERATED! DO NOT EDIT FILE DIRECTLY
# SEE CONTRIBUTOR DOCUMENTATION
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class ZpaGroupEntitlements(ZscalerObject):
    """
    A class for ZpaGroupEntitlements objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ZpaGroupEntitlements model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.compute_device_groups_for_zpa = (
                config["computeDeviceGroupsForZPA"] if "computeDeviceGroupsForZPA" in config else None
            )
            self.device_group_list = ZscalerCollection.form_list(
                config["deviceGroupList"] if "deviceGroupList" in config else [], str
            )
            self.group_list = ZscalerCollection.form_list(config["groupList"] if "groupList" in config else [], str)
            self.machine_tun_enabled_for_all = (
                config["machineTunEnabledForAll"] if "machineTunEnabledForAll" in config else None
            )
            self.total_count = config["totalCount"] if "totalCount" in config else None
            self.zpa_enable_for_all = config["zpaEnableForAll"] if "zpaEnableForAll" in config else None
        else:
            self.compute_device_groups_for_zpa = None
            self.device_group_list = ZscalerCollection.form_list([], str)
            self.group_list = ZscalerCollection.form_list([], str)
            self.machine_tun_enabled_for_all = None
            self.total_count = None
            self.zpa_enable_for_all = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "computeDeviceGroupsForZPA": self.compute_device_groups_for_zpa,
            "deviceGroupList": self.device_group_list,
            "groupList": self.group_list,
            "machineTunEnabledForAll": self.machine_tun_enabled_for_all,
            "totalCount": self.total_count,
            "zpaEnableForAll": self.zpa_enable_for_all,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
