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


class OtpResponse(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the OtpResponse model based on API response.

        Args:
            config (dict): A dictionary representing the OtpResponse configuration.
        """
        super().__init__(config)

        if config:
            self.anti_tempering_disable_otp = (
                config["antiTemperingDisableOtp"] if "antiTemperingDisableOtp" in config else None
            )
            self.deception_settings_otp = config["deceptionSettingsOtp"] if "deceptionSettingsOtp" in config else None
            self.exit_otp = config["exitOtp"] if "exitOtp" in config else None
            self.logout_otp = config["logoutOtp"] if "logoutOtp" in config else None
            self.otp = config["otp"] if "otp" in config else None
            self.revert_otp = config["revertOtp"] if "revertOtp" in config else None
            self.uninstall_otp = config["uninstallOtp"] if "uninstallOtp" in config else None
            self.zdp_disable_otp = config["zdpDisableOtp"] if "zdpDisableOtp" in config else None
            self.zdx_disable_otp = config["zdxDisableOtp"] if "zdxDisableOtp" in config else None
            self.zia_disable_otp = config["ziaDisableOtp"] if "ziaDisableOtp" in config else None
            self.zpa_disable_otp = config["zpaDisableOtp"] if "zpaDisableOtp" in config else None

        else:
            self.anti_tempering_disable_otp = None
            self.deception_settings_otp = None
            self.exit_otp = None
            self.logout_otp = None
            self.otp = None
            self.revert_otp = None
            self.uninstall_otp = None
            self.zdp_disable_otp = None
            self.zdx_disable_otp = None
            self.zia_disable_otp = None
            self.zpa_disable_otp = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "antiTemperingDisableOtp": self.anti_tempering_disable_otp,
            "deceptionSettingsOtp": self.deception_settings_otp,
            "exitOtp": self.exit_otp,
            "logoutOtp": self.logout_otp,
            "otp": self.otp,
            "revertOtp": self.revert_otp,
            "uninstallOtp": self.uninstall_otp,
            "zdpDisableOtp": self.zdp_disable_otp,
            "zdxDisableOtp": self.zdx_disable_otp,
            "ziaDisableOtp": self.zia_disable_otp,
            "zpaDisableOtp": self.zpa_disable_otp,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
