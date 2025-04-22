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
from zscaler.zia.models import cloud_firewall_destination_groups as destination_groups
from zscaler.zia.models import cloud_firewall_source_groups as source_groups
from zscaler.zia.models import cloud_firewall_time_windows as time_windows
from zscaler.zia.models import device_groups as device_groups
from zscaler.zia.models import devices as devices
from zscaler.zia.models import location_management as location_management
from zscaler.zia.models import location_group as location_group
from zscaler.zia.models import proxy_gatways as proxy_gatways
from zscaler.zia.models import rule_labels as rule_labels
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import workload_groups as workload_groups
from zscaler.zia.models import common as common_reference


class SSLInspectionRules(ZscalerObject):
    """
    A class for SSLInspectionRules objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SSLInspectionRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.access_control = config["accessControl"] if "accessControl" in config else None
            self.name = config["name"] if "name" in config else None
            self.order = config["order"] if "order" in config else None
            self.rank = config["rank"] if "rank" in config else None

            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.location_groups = ZscalerCollection.form_list(
                config["locationGroups"] if "locationGroups" in config else [], location_group.LocationGroup
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], user_management.Groups)
            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.platforms = ZscalerCollection.form_list(config["platforms"] if "platforms" in config else [], str)
            self.road_warrior_for_kerberos = config["roadWarriorForKerberos"] if "roadWarriorForKerberos" in config else False

            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], str
            )
            self.cloud_applications = ZscalerCollection.form_list(
                config["cloudApplications"] if "cloudApplications" in config else [], str
            )

            if "action" in config:
                if isinstance(config["action"], Action):
                    self.action = config["action"]
                elif config["action"] is not None:
                    self.action = Action(config["action"])
                else:
                    self.action = None
            else:
                self.action = None

            self.state = config["state"] if "state" in config else None
            self.description = config["description"] if "description" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.last_modified_by = config["lastModifiedBy"] if "lastModifiedBy" in config else None
            self.dest_ip_groups = ZscalerCollection.form_list(
                config["destIpGroups"] if "destIpGroups" in config else [], destination_groups.IPDestinationGroups
            )
            self.source_ip_groups = ZscalerCollection.form_list(
                config["sourceIpGroups"] if config and "sourceIpGroups" in config else [], source_groups.IPSourceGroup
            )

            self.proxy_gateways = ZscalerCollection.form_list(
                config["proxyGateways"] if "proxyGateways" in config else [], proxy_gatways.ProxyGatways
            )
            self.user_agent_types = ZscalerCollection.form_list(
                config["userAgentTypes"] if "userAgentTypes" in config else [], str
            )
            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )
            self.device_trust_levels = ZscalerCollection.form_list(
                config["deviceTrustLevels"] if "deviceTrustLevels" in config else [], str
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], rule_labels.RuleLabels)
            self.zpa_app_segments = ZscalerCollection.form_list(
                config["zpaAppSegments"] if "zpaAppSegments" in config else [], common_reference.ResourceReference
            )

            self.workload_groups = ZscalerCollection.form_list(
                config["workloadGroups"] if "workloadGroups" in config else [], workload_groups.WorkloadGroups
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            self.default_rule = config["defaultRule"] if "defaultRule" in config else False

            self.predefined = config["predefined"] if "predefined" in config else False
        else:
            self.id = None
            self.access_control = None
            self.name = None
            self.order = None
            self.rank = None
            self.locations = []
            self.location_groups = []
            self.departments = []
            self.groups = []
            self.users = []
            self.platforms = []
            self.road_warrior_for_kerberos = None
            self.url_categories = []
            self.cloud_applications = []
            self.action = None
            self.state = None
            self.description = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.dest_ip_groups = []
            self.source_ip_groups = []
            self.proxy_gateways = []
            self.user_agent_types = []
            self.devices = []
            self.device_groups = []
            self.device_trust_levels = []
            self.labels = []
            self.zpa_app_segments = []
            self.workload_groups = []
            self.time_windows = []
            self.predefined = None
            self.default_rule = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "accessControl": self.access_control,
            "name": self.name,
            "order": self.order,
            "rank": self.rank,
            "locations": [loc.request_format() for loc in (self.locations or [])],
            "locationGroups": [lg.request_format() for lg in (self.location_groups or [])],
            "departments": [dept.request_format() for dept in (self.departments or [])],
            "groups": [grp.request_format() for grp in (self.groups or [])],
            "users": [user.request_format() for user in (self.users or [])],
            "platforms": self.platforms,
            "roadWarriorForKerberos": self.road_warrior_for_kerberos,
            "urlCategories": self.url_categories,
            "cloudApplications": self.cloud_applications,
            "action": self.action,
            "state": self.state,
            "description": self.description,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "destIpGroups": [dig.request_format() for dig in (self.dest_ip_groups or [])],
            "sourceIpGroups": [sig.request_format() for sig in (self.source_ip_groups or [])],
            "proxyGateways": [proxy.as_dict() if isinstance(proxy, ZscalerObject) else proxy for proxy in self.proxy_gateways],
            "userAgentTypes": self.user_agent_types,
            "devices": self.devices,
            "deviceGroups": self.device_groups,
            "deviceTrustLevels": self.device_trust_levels,
            "labels": self.labels,
            "zpaAppSegments": [
                segment.as_dict() if isinstance(segment, ZscalerObject) else segment for segment in self.zpa_app_segments
            ],
            "workloadGroups": self.workload_groups,
            "timeWindows": self.time_windows,
            "predefined": self.predefined or False,
            "defaultRule": self.default_rule or False,  # Ensure `defaultRule` exists
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Action(ZscalerObject):
    """
    A class for Action objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the Action model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        # print("🚨 Raw config passed into Action:")
        # import pprint
        # pprint.pprint(config)
        if config:
            self.type = config["type"] if "type" in config else None

            # print("💥 showEUN Debug:",
            #     config.get("show_eun"),
            #     config.get("showEun"),
            #     config.get("showEUN"))

            self.show_eun = next((config[k] for k in ["show_eun", "showEun", "showEUN"] if k in config), False)

            self.show_eun = (
                config.get("show_eun")  # ← used by the converted keys
                or config.get("showEun")  # ← if not snake_cased
                or config.get("showEUN")  # ← raw from the API
                or False  # ← fallback
            )

            # print("💥 showEUNATP Debug:",
            #     config.get("show_eun_atp"),  # snake_case
            #     config.get("showEunatp"),    # camelCase (actual key)
            #     config.get("showEUNATP"))    # PascalCase (not used here)

            self.show_eun_atp = (
                config.get("show_eun_atp")
                or config.get("showEunatp")  # ← use this instead
                or config.get("showEUNATP")
                or False
            )

            self.override_default_certificate = (
                config["overrideDefaultCertificate"] if "overrideDefaultCertificate" in config else None
            )

            if "decryptSubActions" in config:
                if isinstance(config["decryptSubActions"], DecryptSubActions):
                    self.decrypt_sub_actions = config["decryptSubActions"]
                elif config["decryptSubActions"] is not None:
                    self.decrypt_sub_actions = DecryptSubActions(config["decryptSubActions"])
                else:
                    self.decrypt_sub_actions = None
            else:
                self.decrypt_sub_actions = None

            if "doNotDecryptSubActions" in config:
                if isinstance(config["doNotDecryptSubActions"], DoNotDecryptSubActions):
                    self.do_not_decrypt_sub_actions = config["doNotDecryptSubActions"]
                elif config["doNotDecryptSubActions"] is not None:
                    self.do_not_decrypt_sub_actions = DoNotDecryptSubActions(config["doNotDecryptSubActions"])
                else:
                    self.do_not_decrypt_sub_actions = None
            else:
                self.do_not_decrypt_sub_actions = None

            if "sslInterceptionCert" in config:
                if isinstance(config["sslInterceptionCert"], SSLInterceptionCert):
                    self.ssl_interception_cert = config["sslInterceptionCert"]
                elif config["sslInterceptionCert"] is not None:
                    self.ssl_interception_cert = SSLInterceptionCert(config["sslInterceptionCert"])
                else:
                    self.ssl_interception_cert = None
            else:
                self.ssl_interception_cert = None

            # ✅ Print debug values here after all parsing is done
            # print(f"✅ show_eun = {self.show_eun}")
            # print(f"✅ show_eun_atp = {self.show_eun_atp}")
            # print(f"✅ show_eun_atp = {self.show_eun_atp}")
        else:
            self.type = None
            self.show_eun = False
            self.show_eun_atp = False
            self.override_default_certificate = None
            self.decrypt_sub_actions = None
            self.do_not_decrypt_sub_actions = None
            self.ssl_interception_cert = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "type": self.type,
            "showEUN": self.show_eun,
            "showEUNATP": self.show_eun_atp,
            "overrideDefaultCertificate": self.override_default_certificate,
            "decryptSubActions": (self.decrypt_sub_actions.request_format() if self.decrypt_sub_actions else None),
            "doNotDecryptSubActions": (
                self.do_not_decrypt_sub_actions.request_format() if self.do_not_decrypt_sub_actions else None
            ),
            "sslInterceptionCert": (self.ssl_interception_cert.request_format() if self.ssl_interception_cert else None),
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SSLInterceptionCert(ZscalerObject):
    """
    A class for SSLInterceptionCert objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the SSLInterceptionCert model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.default_certificate = config["defaultCertificate"] if "defaultCertificate" in config else None

        else:
            self.id = None
            self.name = None
            self.default_certificate = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "defaultCertificate": self.default_certificate,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DoNotDecryptSubActions(ZscalerObject):
    """
    A class for DoNotDecryptSubActions objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the DoNotDecryptSubActions model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        # print("🚨 Raw config passed into DoNotDecryptSubActions:")
        # import pprint
        # pprint.pprint(config)
        if config:
            self.bypass_other_policies = config["bypassOtherPolicies"] if "bypassOtherPolicies" in config else None
            self.server_certificates = config["serverCertificates"] if "serverCertificates" in config else None
            self.ocsp_check = config["ocspCheck"] if "ocspCheck" in config else None
            self.block_ssl_traffic_with_no_sni_enabled = (
                config["blockSslTrafficWithNoSniEnabled"] if "blockSslTrafficWithNoSniEnabled" in config else None
            )

            # print("💥 minTLSVersion Debug:",
            #     config.get("min_tls_version"),
            #     config.get("minTlsVersion"),
            #     config.get("minTLSVersion"))

            self.min_tls_version = (
                config.get("min_tls_version")  # ← used by the converted keys
                or config.get("minTlsVersion")  # ← if not snake_cased
                or config.get("minTLSVersion")  # ← raw from the API
                or None  # ← fallback
            )

        else:
            self.bypass_other_policies = None
            self.server_certificates = None
            self.ocsp_check = None
            self.block_ssl_traffic_with_no_sni_enabled = None
            self.min_tls_version = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "bypassOtherPolicies": self.bypass_other_policies,
            "serverCertificates": self.server_certificates,
            "ocspCheck": self.ocsp_check,
            "blockSslTrafficWithNoSniEnabled": self.block_ssl_traffic_with_no_sni_enabled,
            "minTLSVersion": self.min_tls_version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DecryptSubActions(ZscalerObject):
    """
    A class for DoNotDecryptSubActions objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the DoNotDecryptSubActions model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        # print("🚨 Raw config passed into DoNotDecryptSubActions:")
        # import pprint
        # pprint.pprint(config)
        if config:
            self.server_certificates = config["serverCertificates"] if "serverCertificates" in config else None
            self.ocsp_check = config["ocspCheck"] if "ocspCheck" in config else None
            self.block_ssl_traffic_with_no_sni_enabled = (
                config["blockSslTrafficWithNoSniEnabled"] if "blockSslTrafficWithNoSniEnabled" in config else None
            )

            # print("💥 minServerTLSVersion Debug:",
            #     config.get("min_server_tls_version"),
            #     config.get("minServerTlsVersion"),
            #     config.get("minServerTLSVersion"))

            self.min_server_tls_version = (
                config.get("min_server_tls_version")
                or config.get("minServerTlsVersion")
                or config.get("minServerTLSVersion")
                or None
            )

            # print("💥 minClientTLSVersion Debug:",
            #     config.get("min_client_tls_version"),
            #     config.get("minClientTlsVersion"),
            #     config.get("minClientTLSVersion"))

            self.min_client_tls_version = (
                config.get("min_client_tls_version")  # ← snake_case
                or config.get("minClientTlsVersion")  # ← weird hybrid
                or config.get("minClientTLSVersion")  # ← API camelCase
                or None
            )

            self.block_undecrypt = config["blockUndecrypt"] if "blockUndecrypt" in config else None
            self.http2_enabled = config["http2Enabled"] if "http2Enabled" in config else None
            # ✅ Print debug values here after all parsing is done
            # print(f"✅ min_client_tls_version = {self.min_client_tls_version}")
            # print(f"✅ min_server_tls_version = {self.min_server_tls_version}")

        else:
            self.server_certificates = None
            self.ocsp_check = None
            self.block_ssl_traffic_with_no_sni_enabled = None
            self.min_client_tls_version = None
            self.min_server_tls_version = None
            self.block_undecrypt = None
            self.http2_enabled = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "serverCertificates": self.server_certificates,
            "ocspCheck": self.ocsp_check,
            "blockSslTrafficWithNoSniEnabled": self.block_ssl_traffic_with_no_sni_enabled,
            "minClientTLSVersion": self.min_client_tls_version,
            "minServerTLSVersion": self.min_server_tls_version,
            "blockUndecrypt": self.block_undecrypt,
            "http2Enabled": self.http2_enabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
