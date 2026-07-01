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


class DeviceGroup(ZscalerObject):
    """
    A class representing a DeviceGroup object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.group_type = config["groupType"] if "groupType" in config else None
            self.description = config["description"] if "description" in config else None
            self.os_type = config["osType"] if "osType" in config else None
            self.predefined = config["predefined"] if "predefined" in config else False
            self.device_count = config["deviceCount"] if "deviceCount" in config else None
        else:
            self.id = None
            self.name = None
            self.group_type = None
            self.description = None
            self.os_type = None
            self.predefined = False
            self.device_count = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "groupType": self.group_type,
            "description": self.description,
            "osType": self.os_type,
            "predefined": self.predefined,
            "deviceCount": self.device_count,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Device(ZscalerObject):
    """
    A class representing a Device object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.device_group_type = config["deviceGroupType"] if "deviceGroupType" in config else None
            self.device_model = config["deviceModel"] if "deviceModel" in config else None
            self.os_type = config["osType"] if "osType" in config else None
            self.os_version = config["osVersion"] if "osVersion" in config else None
            self.description = config["description"] if "description" in config else None
            self.owner_user_id = config["ownerUserId"] if "ownerUserId" in config else None
            self.owner_name = config["ownerName"] if "ownerName" in config else None
            self.host_name = config["hostName"] if "hostName" in config else None
        else:
            self.id = None
            self.name = None
            self.device_group_type = None
            self.device_model = None
            self.os_type = None
            self.os_version = None
            self.description = None
            self.owner_user_id = None
            self.owner_name = None
            self.host_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "deviceGroupType": self.device_group_type,
            "deviceModel": self.device_model,
            "osType": self.os_type,
            "osVersion": self.os_version,
            "description": self.description,
            "ownerUserId": self.owner_user_id,
            "ownerName": self.owner_name,
            "hostName": self.host_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
