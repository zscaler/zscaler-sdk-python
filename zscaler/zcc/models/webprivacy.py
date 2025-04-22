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


class WebPrivacy(ZscalerObject):
    """
    A class for WebPrivacy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the WebPrivacy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.collect_machine_hostname = config["collectMachineHostname"] if "collectMachineHostname" in config else None
            self.collect_user_info = config["collectUserInfo"] if "collectUserInfo" in config else None
            self.collect_zdx_location = config["collectZdxLocation"] if "collectZdxLocation" in config else None
            self.disable_crashlytics = config["disableCrashlytics"] if "disableCrashlytics" in config else None
            self.enable_packet_capture = config["enablePacketCapture"] if "enablePacketCapture" in config else None
            self.export_logs_for_non_admin = config["exportLogsForNonAdmin"] if "exportLogsForNonAdmin" in config else None
            self.grant_access_to_zscaler_log_folder = (
                config["grantAccessToZscalerLogFolder"] if "grantAccessToZscalerLogFolder" in config else None
            )
            self.id = config["id"] if "id" in config else None
            self.override_t2_protocol_setting = (
                config["overrideT2ProtocolSetting"] if "overrideT2ProtocolSetting" in config else None
            )
            self.restrict_remote_packet_capture = (
                config["restrictRemotePacketCapture"] if "restrictRemotePacketCapture" in config else None
            )
        else:
            self.active = None
            self.collect_machine_hostname = None
            self.collect_user_info = None
            self.collect_zdx_location = None
            self.disable_crashlytics = None
            self.enable_packet_capture = None
            self.export_logs_for_non_admin = None
            self.grant_access_to_zscaler_log_folder = None
            self.id = None
            self.override_t2_protocol_setting = None
            self.restrict_remote_packet_capture = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "collectMachineHostname": self.collect_machine_hostname,
            "collectUserInfo": self.collect_user_info,
            "collectZdxLocation": self.collect_zdx_location,
            "disableCrashlytics": self.disable_crashlytics,
            "enablePacketCapture": self.enable_packet_capture,
            "exportLogsForNonAdmin": self.export_logs_for_non_admin,
            "grantAccessToZscalerLogFolder": self.grant_access_to_zscaler_log_folder,
            "id": self.id,
            "overrideT2ProtocolSetting": self.override_t2_protocol_setting,
            "restrictRemotePacketCapture": self.restrict_remote_packet_capture,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
