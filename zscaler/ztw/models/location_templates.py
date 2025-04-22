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
from zscaler.ztw.models import common as common


class LocationTemplate(ZscalerObject):
    """
    A class for LocationTemplate objects.
    """

    def __init__(self, config=None):
        """
        Initialize the LocationTemplate model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.desc = config["desc"] if "desc" in config else None
            self.editable = config["editable"] if "editable" in config else False
            self.last_mod_time = config["lastModTime"] if "lastModTime" in config else None

            if "template" in config:
                if isinstance(config["template"], Template):
                    self.template = config["template"]
                elif config["template"] is not None:
                    self.template = Template(config["template"])
                else:
                    self.template = None
            else:
                self.template = None

            if "lastModUid" in config:
                if isinstance(config["lastModUid"], common.CommonIDNameExternalID):
                    self.last_mod_uid = config["lastModUid"]
                elif config["lastModUid"] is not None:
                    self.last_mod_uid = common.CommonIDNameExternalID(config["lastModUid"])
                else:
                    self.last_mod_uid = None
            else:
                self.last_mod_uid = None
        else:
            self.id = None
            self.name = None
            self.desc = None
            self.template = None
            self.editable = None
            self.last_mod_uid = None
            self.last_mod_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "template": self.template,
            "editable": self.editable,
            "lastModUid": self.last_mod_uid,
            "lastModTime": self.last_mod_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Template(ZscalerObject):
    """
    A class for Template objects.

    This model wraps a plain dictionary of template settings and converts internal
    snake_case attribute names to the expected camelCase keys for the API.
    """

    def __init__(self, config=None):
        """
        Initialize the Template model based on API response or a plain dict.

        Args:
            config (dict): A dictionary representing the template settings.
        """
        super().__init__(config)
        if config:
            self.template_prefix = config.get("templatePrefix")
            self.xff_forward_enabled = config.get("xffForwardEnabled", False)
            self.auth_required = config.get("authRequired", False)
            self.caution_enabled = config.get("cautionEnabled", False)
            self.aup_enabled = config.get("aupEnabled", False)
            self.aup_timeout_in_days = config.get("aupTimeoutInDays")
            self.ofw_enabled = config.get("ofwEnabled", False)
            self.ips_control = config.get("ipsControl", False)
            self.enforce_bandwidth_control = config.get("enforceBandwidthControl", False)
            self.up_bandwidth = config.get("upBandwidth")
            self.dn_bandwidth = config.get("dnBandwidth")
            self.display_time_unit = config.get("displayTimeUnit")
            self.idle_time_in_minutes = config.get("idleTimeInMinutes")
            self.surrogate_i_p_enforced_for_known_browsers = config.get("surrogateIPEnforcedForKnownBrowsers", False)
            self.surrogate_refresh_time_unit = config.get("surrogateRefreshTimeUnit")
            self.surrogate_refresh_time_in_minutes = config.get("surrogateRefreshTimeInMinutes")
            self.surrogate_i_p = config.get("surrogateIP", False)
        else:
            self.template_prefix = None
            self.xff_forward_enabled = False
            self.auth_required = False
            self.caution_enabled = False
            self.aup_enabled = False
            self.aup_timeout_in_days = None
            self.ofw_enabled = False
            self.ips_control = False
            self.enforce_bandwidth_control = False
            self.up_bandwidth = None
            self.dn_bandwidth = None
            self.display_time_unit = None
            self.idle_time_in_minutes = None
            self.surrogate_i_p_enforced_for_known_browsers = False
            self.surrogate_refresh_time_unit = None
            self.surrogate_refresh_time_in_minutes = None
            self.surrogate_i_p = False

    def request_format(self):
        """
        Return the object as a dictionary with the correct camelCase keys
        expected by the API.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "templatePrefix": self.template_prefix,
            "xffForwardEnabled": self.xff_forward_enabled,
            "authRequired": self.auth_required,
            "cautionEnabled": self.caution_enabled,
            "aupEnabled": self.aup_enabled,
            "aupTimeoutInDays": self.aup_timeout_in_days,
            "ofwEnabled": self.ofw_enabled,
            "ipsControl": self.ips_control,
            "enforceBandwidthControl": self.enforce_bandwidth_control,
            "upBandwidth": self.up_bandwidth,
            "dnBandwidth": self.dn_bandwidth,
            "displayTimeUnit": self.display_time_unit,
            "idleTimeInMinutes": self.idle_time_in_minutes,
            "surrogateIPEnforcedForKnownBrowsers": self.surrogate_i_p_enforced_for_known_browsers,
            "surrogateRefreshTimeUnit": self.surrogate_refresh_time_unit,
            "surrogateRefreshTimeInMinutes": self.surrogate_refresh_time_in_minutes,
            "surrogateIP": self.surrogate_i_p,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format

    def as_dict(self):
        """
        Return the same formatted dictionary.
        """
        return self.request_format()
