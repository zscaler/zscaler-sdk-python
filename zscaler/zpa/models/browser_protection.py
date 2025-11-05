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

from typing import Dict, List, Optional, Any, Union
from zscaler.oneapi_object import ZscalerObject


class BrowserProtectionProfile(ZscalerObject):
    """
    A class for BrowserProtectionProfile objects.
    """

    def __init__(self, config=None):
        """
        Initialize the BrowserProtectionProfile model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.criteria_flags_mask = config["criteriaFlagsMask"] \
                if "criteriaFlagsMask" in config else None
            self.default_csp = config["defaultCSP"] \
                if "defaultCSP" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None

            if "criteria" in config:
                if isinstance(config["criteria"], Criteria):
                    self.criteria = config["criteria"]
                elif config["criteria"] is not None:
                    self.criteria = Criteria(config["criteria"])
                else:
                    self.criteria = None
            else:
                self.criteria = None

        else:
            self.creation_time = None
            self.criteria = None
            self.criteria_flags_mask = None
            self.default_csp = None
            self.description = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.criteria = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "criteria": self.criteria,
            "criteriaFlagsMask": self.criteria_flags_mask,
            "defaultCSP": self.default_csp,
            "description": self.description,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Criteria(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            if "fingerPrintCriteria" in config:
                if isinstance(config["fingerPrintCriteria"], FingerPrintCriteria):
                    self.finger_print_criteria = config["fingerPrintCriteria"]
                elif config["fingerPrintCriteria"] is not None:
                    self.finger_print_criteria = FingerPrintCriteria(config["fingerPrintCriteria"])
                else:
                    self.finger_print_criteria = None
            else:
                self.finger_print_criteria = None
        else:
            self.finger_print_criteria = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "fingerPrintCriteria": self.finger_print_criteria,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class FingerPrintCriteria(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            if "browser" in config:
                if isinstance(config["browser"], Browser):
                    self.browser = config["browser"]
                elif config["browser"] is not None:
                    self.browser = Browser(config["browser"])
                else:
                    self.browser = None
            else:
                self.browser = None

            self.collect_location = config["collect_location"] \
                if "collect_location" in config else None
            self.fingerprint_timeout = config["fingerprint_timeout"] \
                if "fingerprint_timeout" in config else None

            if "location" in config:
                if isinstance(config["location"], Location):
                    self.location = config["location"]
                elif config["location"] is not None:
                    self.location = Location(config["location"])
                else:
                    self.location = None
            else:
                self.location = None

            if "system" in config:
                if isinstance(config["system"], System):
                    self.system = config["system"]
                elif config["system"] is not None:
                    self.system = System(config["system"])
                else:
                    self.system = None
            else:
                self.system = None
        else:
            self.browser = None
            self.collect_location = None
            self.fingerprint_timeout = None
            self.location = None
            self.system = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "browser": self.browser,
            "collect_location": self.collect_location,
            "fingerprint_timeout": self.fingerprint_timeout,
            "location": self.location,
            "system": self.system,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Browser(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.browser_eng = config["browser_eng"] \
                if "browser_eng" in config else None
            self.browser_eng_ver = config["browser_eng_ver"] \
                if "browser_eng_ver" in config else None
            self.browser_name = config["browser_name"] \
                if "browser_name" in config else None
            self.browser_version = config["browser_version"] \
                if "browser_version" in config else None
            self.canvas = config["canvas"] \
                if "canvas" in config else None
            self.flash_ver = config["flash_ver"] \
                if "flash_ver" in config else None
            self.fp_usr_agent_str = config["fp_usr_agent_str"] \
                if "fp_usr_agent_str" in config else None
            self.is_cookie = config["is_cookie"] \
                if "is_cookie" in config else None
            self.is_local_storage = config["is_local_storage"] \
                if "is_local_storage" in config else None
            self.is_sess_storage = config["is_sess_storage"] \
                if "is_sess_storage" in config else None
            self.ja3 = config["ja3"] \
                if "ja3" in config else None
            self.mime = config["mime"] \
                if "mime" in config else None
            self.plugin = config["plugin"] \
                if "plugin" in config else None
            self.silverlight_ver = config["silverlight_ver"] \
                if "silverlight_ver" in config else None
        else:
            self.browser_eng = None
            self.browser_eng_ver = None
            self.browser_name = None
            self.browser_version = None
            self.canvas = None
            self.flash_ver = None
            self.fp_usr_agent_str = None
            self.is_cookie = None
            self.is_local_storage = None
            self.is_sess_storage = None
            self.ja3 = None
            self.mime = None
            self.plugin = None
            self.silverlight_ver = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "browser_eng": self.browser_eng,
            "browser_eng_ver": self.browser_eng_ver,
            "browser_name": self.browser_name,
            "browser_version": self.browser_version,
            "canvas": self.canvas,
            "flash_ver": self.flash_ver,
            "fp_usr_agent_str": self.fp_usr_agent_str,
            "is_cookie": self.is_cookie,
            "is_local_storage": self.is_local_storage,
            "is_sess_storage": self.is_sess_storage,
            "ja3": self.ja3,
            "mime": self.mime,
            "plugin": self.plugin,
            "silverlight_ver": self.silverlight_ver,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Location(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.lat = config["lat"] \
                if "lat" in config else None
            self.lon = config["lon"] \
                if "lon" in config else None
        else:
            self.lat = None
            self.lon = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "lat": self.lat,
            "lon": self.lon,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class System(ZscalerObject):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.avail_screen_resolution = config["avail_screen_resolution"] \
                if "avail_screen_resolution" in config else None
            self.cpu_arch = config["cpu_arch"] \
                if "cpu_arch" in config else None
            self.curr_screen_resolution = config["curr_screen_resolution"] \
                if "curr_screen_resolution" in config else None
            self.font = config["font"] \
                if "font" in config else None
            self.java_ver = config["java_ver"] \
                if "java_ver" in config else None
            self.mobile_dev_type = config["mobile_dev_type"] \
                if "mobile_dev_type" in config else None
            self.monitor_mobile = config["monitor_mobile"] \
                if "monitor_mobile" in config else None
            self.os_name = config["os_name"] \
                if "os_name" in config else None
            self.os_version = config["os_version"] \
                if "os_version" in config else None
            self.sys_lang = config["sys_lang"] \
                if "sys_lang" in config else None
            self.tz = config["tz"] \
                if "tz" in config else None
            self.usr_lang = config["usr_lang"] \
                if "usr_lang" in config else None
        else:
            self.avail_screen_resolution = None
            self.cpu_arch = None
            self.curr_screen_resolution = None
            self.font = None
            self.java_ver = None
            self.mobile_dev_type = None
            self.monitor_mobile = None
            self.os_name = None
            self.os_version = None
            self.sys_lang = None
            self.tz = None
            self.usr_lang = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "avail_screen_resolution": self.avail_screen_resolution,
            "cpu_arch": self.cpu_arch,
            "curr_screen_resolution": self.curr_screen_resolution,
            "font": self.font,
            "java_ver": self.java_ver,
            "mobile_dev_type": self.mobile_dev_type,
            "monitor_mobile": self.monitor_mobile,
            "os_name": self.os_name,
            "os_version": self.os_version,
            "sys_lang": self.sys_lang,
            "tz": self.tz,
            "usr_lang": self.usr_lang,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
