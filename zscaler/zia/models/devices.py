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
from zscaler.zia.models import common as common


class RegisteredDevice(ZscalerObject):
    """
    A class representing a RegisteredDevice object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.active = config["active"] if "active" in config else False
            self.version = config["version"] if "version" in config else None
            self.hostname = config["hostname"] if "hostname" in config else None
            self.vendor = config["vendor"] if "vendor" in config else None
            self.model = config["model"] if "model" in config else None
            self.locale = config["locale"] if "locale" in config else None
            self.os = config["os"] if "os" in config else None
            self.udid = config["udid"] if "udid" in config else None
            self.hardware_id = config["hardwareId"] if "hardwareId" in config else None
            self.mac_address = config["macAddress"] if "macAddress" in config else None
            if "user" in config:
                if isinstance(config["user"], common.CommonBlocks):
                    self.user = config["user"]
                elif config["user"] is not None:
                    self.user = common.CommonBlocks(config["user"])
                else:
                    self.user = None
            else:
                self.user = None
            self.first_registration_timestamp = (
                config["firstRegistrationTimestamp"] if "firstRegistrationTimestamp" in config else None
            )
            self.last_registration_timestamp = (
                config["lastRegistrationTimestamp"] if "lastRegistrationTimestamp" in config else None
            )
            self.un_registration_timestamp = config["unRegistrationTimestamp"] if "unRegistrationTimestamp" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.rooted = config["rooted"] if "rooted" in config else False
        else:
            self.id = None
            self.name = None
            self.active = False
            self.version = None
            self.hostname = None
            self.vendor = None
            self.model = None
            self.locale = None
            self.os = None
            self.udid = None
            self.hardware_id = None
            self.mac_address = None
            self.user = None
            self.first_registration_timestamp = None
            self.last_registration_timestamp = None
            self.un_registration_timestamp = None
            self.deleted = False
            self.rooted = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "version": self.version,
            "hostname": self.hostname,
            "vendor": self.vendor,
            "model": self.model,
            "locale": self.locale,
            "os": self.os,
            "udid": self.udid,
            "hardwareId": self.hardware_id,
            "macAddress": self.mac_address,
            "user": self.user,
            "firstRegistrationTimestamp": self.first_registration_timestamp,
            "lastRegistrationTimestamp": self.last_registration_timestamp,
            "unRegistrationTimestamp": self.un_registration_timestamp,
            "deleted": self.deleted,
            "rooted": self.rooted,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
