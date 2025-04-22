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


class AdminRoles(ZscalerObject):
    """
    A class for AdminRoles objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdminRoles model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.admin_management = config["adminManagement"] if "adminManagement" in config else None
            self.administrator_group = config["administratorGroup"] if "administratorGroup" in config else None
            self.android_profile = config["androidProfile"] if "androidProfile" in config else None
            self.app_bypass = config["appBypass"] if "appBypass" in config else None
            self.app_profile_group = config["appProfileGroup"] if "appProfileGroup" in config else None
            self.audit_logs = config["auditLogs"] if "auditLogs" in config else None
            self.auth_setting = config["authSetting"] if "authSetting" in config else None
            self.client_connector_app_store = (
                config["clientConnectorAppStore"] if "clientConnectorAppStore" in config else None
            )
            self.client_connector_idp = config["clientConnectorIdp"] if "clientConnectorIdp" in config else None
            self.client_connector_notifications = (
                config["clientConnectorNotifications"] if "clientConnectorNotifications" in config else None
            )
            self.client_connector_support = config["clientConnectorSupport"] if "clientConnectorSupport" in config else None
            self.company_id = config["companyId"] if "companyId" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.dashboard = config["dashboard"] if "dashboard" in config else None
            self.ddil_configuration = config["ddilConfiguration"] if "ddilConfiguration" in config else None
            self.dedicated_proxy_ports = config["dedicatedProxyPorts"] if "dedicatedProxyPorts" in config else None
            self.device_groups = config["deviceGroups"] if "deviceGroups" in config else None
            self.device_overview = config["deviceOverview"] if "deviceOverview" in config else None
            self.device_posture = config["devicePosture"] if "devicePosture" in config else None
            self.enrolled_devices_group = config["enrolledDevicesGroup"] if "enrolledDevicesGroup" in config else None
            self.forwarding_profile = config["forwardingProfile"] if "forwardingProfile" in config else None
            self.id = config["id"] if "id" in config else None
            self.ios_profile = config["iosProfile"] if "iosProfile" in config else None
            self.is_editable = config["isEditable"] if "isEditable" in config else None
            self.linux_profile = config["linuxProfile"] if "linuxProfile" in config else None
            self.mac_profile = config["macProfile"] if "macProfile" in config else None
            self.machine_tunnel = config["machineTunnel"] if "machineTunnel" in config else None
            self.obfuscate_data = config["obfuscateData"] if "obfuscateData" in config else None
            self.partner_device_overview = config["partnerDeviceOverview"] if "partnerDeviceOverview" in config else None
            self.public_api = config["publicApi"] if "publicApi" in config else None
            self.role_name = config["roleName"] if "roleName" in config else None
            self.trusted_network = config["trustedNetwork"] if "trustedNetwork" in config else None
            self.updated_by = config["updatedBy"] if "updatedBy" in config else None
            self.user_agent = config["userAgent"] if "userAgent" in config else None
            self.windows_profile = config["windowsProfile"] if "windowsProfile" in config else None
            self.zpa_partner_login = config["zpaPartnerLogin"] if "zpaPartnerLogin" in config else None
            self.zscaler_deception = config["zscalerDeception"] if "zscalerDeception" in config else None
            self.zscaler_entitlement = config["zscalerEntitlement"] if "zscalerEntitlement" in config else None
        else:
            self.admin_management = None
            self.administrator_group = None
            self.android_profile = None
            self.app_bypass = None
            self.app_profile_group = None
            self.audit_logs = None
            self.auth_setting = None
            self.client_connector_app_store = None
            self.client_connector_idp = None
            self.client_connector_notifications = None
            self.client_connector_support = None
            self.company_id = None
            self.created_by = None
            self.dashboard = None
            self.ddil_configuration = None
            self.dedicated_proxy_ports = None
            self.device_groups = None
            self.device_overview = None
            self.device_posture = None
            self.enrolled_devices_group = None
            self.forwarding_profile = None
            self.id = None
            self.ios_profile = None
            self.is_editable = None
            self.linux_profile = None
            self.mac_profile = None
            self.machine_tunnel = None
            self.obfuscate_data = None
            self.partner_device_overview = None
            self.public_api = None
            self.role_name = None
            self.trusted_network = None
            self.updated_by = None
            self.user_agent = None
            self.windows_profile = None
            self.zpa_partner_login = None
            self.zscaler_deception = None
            self.zscaler_entitlement = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "adminManagement": self.admin_management,
            "administratorGroup": self.administrator_group,
            "androidProfile": self.android_profile,
            "appBypass": self.app_bypass,
            "appProfileGroup": self.app_profile_group,
            "auditLogs": self.audit_logs,
            "authSetting": self.auth_setting,
            "clientConnectorAppStore": self.client_connector_app_store,
            "clientConnectorIdp": self.client_connector_idp,
            "clientConnectorNotifications": self.client_connector_notifications,
            "clientConnectorSupport": self.client_connector_support,
            "companyId": self.company_id,
            "createdBy": self.created_by,
            "dashboard": self.dashboard,
            "ddilConfiguration": self.ddil_configuration,
            "dedicatedProxyPorts": self.dedicated_proxy_ports,
            "deviceGroups": self.device_groups,
            "deviceOverview": self.device_overview,
            "devicePosture": self.device_posture,
            "enrolledDevicesGroup": self.enrolled_devices_group,
            "forwardingProfile": self.forwarding_profile,
            "id": self.id,
            "iosProfile": self.ios_profile,
            "isEditable": self.is_editable,
            "linuxProfile": self.linux_profile,
            "macProfile": self.mac_profile,
            "machineTunnel": self.machine_tunnel,
            "obfuscateData": self.obfuscate_data,
            "partnerDeviceOverview": self.partner_device_overview,
            "publicApi": self.public_api,
            "roleName": self.role_name,
            "trustedNetwork": self.trusted_network,
            "updatedBy": self.updated_by,
            "userAgent": self.user_agent,
            "windowsProfile": self.windows_profile,
            "zpaPartnerLogin": self.zpa_partner_login,
            "zscalerDeception": self.zscaler_deception,
            "zscalerEntitlement": self.zscaler_entitlement,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
