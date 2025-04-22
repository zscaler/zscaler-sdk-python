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


class WebPolicy(ZscalerObject):
    """
    A class for WebPolicy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the WebPolicy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.allow_unreachable_pac = config["allowUnreachablePac"] if "allowUnreachablePac" in config else None
            self.android_policy = config["androidPolicy"] if "androidPolicy" in config else None
            self.app_identity_names = ZscalerCollection.form_list(
                config["appIdentityNames"] if "appIdentityNames" in config else [], str
            )
            self.app_service_ids = ZscalerCollection.form_list(
                config["appServiceIds"] if "appServiceIds" in config else [], str
            )
            self.app_service_names = ZscalerCollection.form_list(
                config["appServiceNames"] if "appServiceNames" in config else [], str
            )
            self.bypass_app_ids = ZscalerCollection.form_list(config["bypassAppIds"] if "bypassAppIds" in config else [], str)
            self.bypass_custom_app_ids = ZscalerCollection.form_list(
                config["bypassCustomAppIds"] if "bypassCustomAppIds" in config else [], str
            )
            self.description = config["description"] if "description" in config else None
            self.device_group_ids = ZscalerCollection.form_list(
                config["deviceGroupIds"] if "deviceGroupIds" in config else [], str
            )
            self.device_group_names = ZscalerCollection.form_list(
                config["deviceGroupNames"] if "deviceGroupNames" in config else [], str
            )
            self.device_type = config["device_type"] if "device_type" in config else None
            self.disaster_recovery = config["disasterRecovery"] if "disasterRecovery" in config else None
            self.enable_device_groups = config["enableDeviceGroups"] if "enableDeviceGroups" in config else None
            self.forwarding_profile_id = config["forwardingProfileId"] if "forwardingProfileId" in config else None
            self.group_all = config["groupAll"] if "groupAll" in config else None
            self.group_ids = ZscalerCollection.form_list(config["groupIds"] if "groupIds" in config else [], str)
            self.group_names = ZscalerCollection.form_list(config["groupNames"] if "groupNames" in config else [], str)
            self.highlight_active_control = config["highlightActiveControl"] if "highlightActiveControl" in config else None
            self.id = config["id"] if "id" in config else None
            self.ios_policy = config["iosPolicy"] if "iosPolicy" in config else None
            self.linux_policy = config["linuxPolicy"] if "linuxPolicy" in config else None
            self.log_file_size = config["logFileSize"] if "logFileSize" in config else None
            self.log_level = config["logLevel"] if "logLevel" in config else None
            self.log_mode = config["logMode"] if "logMode" in config else None
            self.mac_policy = config["macPolicy"] if "macPolicy" in config else None
            self.name = config["name"] if "name" in config else None
            self.pac_url = config["pac_url"] if "pac_url" in config else None
            self.policy_extension = config["policyExtension"] if "policyExtension" in config else None
            self.reactivate_web_security_minutes = (
                config["reactivateWebSecurityMinutes"] if "reactivateWebSecurityMinutes" in config else None
            )
            self.reauth_period = config["reauth_period"] if "reauth_period" in config else None
            self.rule_order = config["ruleOrder"] if "ruleOrder" in config else None
            self.send_disable_service_reason = (
                config["sendDisableServiceReason"] if "sendDisableServiceReason" in config else None
            )
            self.tunnel_zapp_traffic = config["tunnelZappTraffic"] if "tunnelZappTraffic" in config else None
            self.user_ids = ZscalerCollection.form_list(config["userIds"] if "userIds" in config else [], str)
            self.user_names = ZscalerCollection.form_list(config["userNames"] if "userNames" in config else [], str)
            self.windows_policy = config["windowsPolicy"] if "windowsPolicy" in config else None
            self.zia_posture_config_id = config["ziaPostureConfigId"] if "ziaPostureConfigId" in config else None
        else:
            self.active = None
            self.allow_unreachable_pac = None
            self.android_policy = None
            self.app_identity_names = ZscalerCollection.form_list([], str)
            self.app_service_ids = ZscalerCollection.form_list([], str)
            self.app_service_names = ZscalerCollection.form_list([], str)
            self.bypass_app_ids = ZscalerCollection.form_list([], str)
            self.bypass_custom_app_ids = ZscalerCollection.form_list([], str)
            self.description = None
            self.device_group_ids = ZscalerCollection.form_list([], str)
            self.device_group_names = ZscalerCollection.form_list([], str)
            self.device_type = None
            self.disaster_recovery = None
            self.enable_device_groups = None
            self.forwarding_profile_id = None
            self.group_all = None
            self.group_ids = ZscalerCollection.form_list([], str)
            self.group_names = ZscalerCollection.form_list([], str)
            self.highlight_active_control = None
            self.id = None
            self.ios_policy = None
            self.linux_policy = None
            self.log_file_size = None
            self.log_level = None
            self.log_mode = None
            self.mac_policy = None
            self.name = None
            self.pac_url = None
            self.policy_extension = None
            self.reactivate_web_security_minutes = None
            self.reauth_period = None
            self.rule_order = None
            self.send_disable_service_reason = None
            self.tunnel_zapp_traffic = None
            self.user_ids = ZscalerCollection.form_list([], str)
            self.user_names = ZscalerCollection.form_list([], str)
            self.windows_policy = None
            self.zia_posture_config_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "allowUnreachablePac": self.allow_unreachable_pac,
            "androidPolicy": self.android_policy,
            "appIdentityNames": self.app_identity_names,
            "appServiceIds": self.app_service_ids,
            "appServiceNames": self.app_service_names,
            "bypassAppIds": self.bypass_app_ids,
            "bypassCustomAppIds": self.bypass_custom_app_ids,
            "description": self.description,
            "deviceGroupIds": self.device_group_ids,
            "deviceGroupNames": self.device_group_names,
            "device_type": self.device_type,
            "disasterRecovery": self.disaster_recovery,
            "enableDeviceGroups": self.enable_device_groups,
            "forwardingProfileId": self.forwarding_profile_id,
            "groupAll": self.group_all,
            "groupIds": self.group_ids,
            "groupNames": self.group_names,
            "highlightActiveControl": self.highlight_active_control,
            "id": self.id,
            "iosPolicy": self.ios_policy,
            "linuxPolicy": self.linux_policy,
            "logFileSize": self.log_file_size,
            "logLevel": self.log_level,
            "logMode": self.log_mode,
            "macPolicy": self.mac_policy,
            "name": self.name,
            "pac_url": self.pac_url,
            "policyExtension": self.policy_extension,
            "reactivateWebSecurityMinutes": self.reactivate_web_security_minutes,
            "reauth_period": self.reauth_period,
            "ruleOrder": self.rule_order,
            "sendDisableServiceReason": self.send_disable_service_reason,
            "tunnelZappTraffic": self.tunnel_zapp_traffic,
            "userIds": self.user_ids,
            "userNames": self.user_names,
            "windowsPolicy": self.windows_policy,
            "ziaPostureConfigId": self.zia_posture_config_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
