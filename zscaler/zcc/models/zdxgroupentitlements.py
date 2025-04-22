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

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class ZdxGroupEntitlements(ZscalerObject):
    """
    A class for ZdxGroupEntitlements objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ZdxGroupEntitlements model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.collect_zdx_location = config["collectZdxLocation"] if "collectZdxLocation" in config else None
            self.compute_device_groups_for_zdx = (
                config["computeDeviceGroupsForZDX"] if "computeDeviceGroupsForZDX" in config else None
            )
            self.logout_zcc_for_zdx_service = config["logoutZCCForZDXService"] if "logoutZCCForZDXService" in config else None
            self.total_count = config["totalCount"] if "totalCount" in config else None
            self.upm_device_group_list = ZscalerCollection.form_list(
                config["upmDeviceGroupList"] if "upmDeviceGroupList" in config else [], str
            )
            self.upm_enable_for_all = config["upmEnableForAll"] if "upmEnableForAll" in config else None
            self.upm_group_list = ZscalerCollection.form_list(config["upmGroupList"] if "upmGroupList" in config else [], str)
        else:
            self.collect_zdx_location = None
            self.compute_device_groups_for_zdx = None
            self.logout_zcc_for_zdx_service = None
            self.total_count = None
            self.upm_device_group_list = ZscalerCollection.form_list([], str)
            self.upm_enable_for_all = None
            self.upm_group_list = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "collectZdxLocation": self.collect_zdx_location,
            "computeDeviceGroupsForZDX": self.compute_device_groups_for_zdx,
            "logoutZCCForZDXService": self.logout_zcc_for_zdx_service,
            "totalCount": self.total_count,
            "upmDeviceGroupList": self.upm_device_group_list,
            "upmEnableForAll": self.upm_enable_for_all,
            "upmGroupList": self.upm_group_list,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
