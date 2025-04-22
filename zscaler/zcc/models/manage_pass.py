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


class ManagePass(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the ManagePass model based on API response.

        Args:
            config (dict): A dictionary representing the ManagePass configuration.
        """
        super().__init__(config)

        if config:
            self.company_id = config["companyId"] if "companyId" in config else None
            self.device_type = config["deviceType"] if "deviceType" in config else None
            self.exit_pass = config["exitPass"] if "exitPass" in config else None
            self.logout_pass = config["logoutPass"] if "logoutPass" in config else None
            self.policy_name = config["policyName"] if "policyName" in config else None
            self.uninstall_pass = config["uninstallPass"] if "uninstallPass" in config else None
            self.zad_disable_pass = config["zadDisablePass"] if "zadDisablePass" in config else None
            self.zdp_disable_pass = config["zdpDisablePass"] if "zdpDisablePass" in config else None
            self.zdx_disable_pass = config["zdxDisablePass"] if "zdxDisablePass" in config else None
            self.zia_disable_pass = config["ziaDisablePass"] if "ziaDisablePass" in config else None
            self.zpa_disable_pass = config["zpaDisablePass"] if "zpaDisablePass" in config else None

        else:
            self.company_id = None
            self.device_type = None
            self.exit_pass = None
            self.logout_pass = None
            self.policy_name = None
            self.uninstall_pass = None
            self.zad_disable_pass = None
            self.zdp_disable_pass = None
            self.zdx_disable_pass = None
            self.zia_disable_pass = None
            self.zpa_disable_pass = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "companyId": self.company_id,
            "deviceType": self.device_type,
            "exitPass": self.exit_pass,
            "logoutPass": self.logout_pass,
            "policyName": self.policy_name,
            "uninstallPass": self.uninstall_pass,
            "zadDisablePass": self.zad_disable_pass,
            "zdpDisablePass": self.zdp_disable_pass,
            "zdxDisablePass": self.zdx_disable_pass,
            "ziaDisablePass": self.zia_disable_pass,
            "zpaDisablePass": self.zpa_disable_pass,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ManagePassResponseContract(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the ManagePassResponseContract model based on API response.

        Args:
            config (dict): A dictionary representing the ManagePassResponseContract configuration.
        """
        super().__init__(config)

        if config:
            self.error_message = config.get("errorMessage")
        else:
            self.error_message = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "errorMessage": self.error_message,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
