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
from zscaler.ztw.models import traffic_vpn_credentials as vpn_credentials


class LocationManagement(ZscalerObject):
    """
    A class representing a Location object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.non_editable = config["nonEditable"] if "nonEditable" in config else False
            self.parent_id = config["parentId"] if "parentId" in config else 0
            self.up_bandwidth = config["upBandwidth"] if "upBandwidth" in config else 0
            self.dn_bandwidth = config["dnBandwidth"] if "dnBandwidth" in config else 0
            self.override_up_bandwidth = config["overrideUpBandwidth"] if "overrideUpBandwidth" in config else 0
            self.override_dn_bandwidth = config["overrideDnBandwidth"] if "overrideDnBandwidth" in config else 0
            self.shared_up_bandwidth = config["sharedUpBandwidth"] if "sharedUpBandwidth" in config else 0
            self.shared_down_bandwidth = config["sharedDownBandwidth"] if "sharedDownBandwidth" in config else 0
            self.unused_up_bandwidth = config["unusedUpBandwidth"] if "unusedUpBandwidth" in config else 0
            self.unused_dn_bandwidth = config["unusedDnBandwidth"] if "unusedDnBandwidth" in config else 0
            self.country = config["country"] if "country" in config else "NONE"
            self.language = config["language"] if "language" in config else "NONE"
            self.tz = config["tz"] if "tz" in config else "NOT_SPECIFIED"
            self.geo_override = config["geoOverride"] if "geoOverride" in config else False
            self.latitude = config["latitude"] if "latitude" in config else 0.0
            self.longitude = config["longitude"] if "longitude" in config else 0.0
            self.auth_required = config["authRequired"] if "authRequired" in config else False
            self.ssl_scan_enabled = config["sslScanEnabled"] if "sslScanEnabled" in config else False
            self.zapp_ssl_scan_enabled = config["zappSslScanEnabled"] if "zappSslScanEnabled" in config else False
            self.xff_forward_enabled = config["xffForwardEnabled"] if "xffForwardEnabled" in config else False
            self.other_sub_location = config["otherSubLocation"] if "otherSubLocation" in config else False
            self.ec_location = config["ecLocation"] if "ecLocation" in config else False
            self.surrogate_ip = config["surrogateIP"] if "surrogateIP" in config else False
            self.cookies_and_proxy = config["cookiesAndProxy"] if "cookiesAndProxy" in config else False
            self.idle_time_in_minutes = config["idleTimeInMinutes"] if "idleTimeInMinutes" in config else 0
            self.display_time_unit = config["displayTimeUnit"] if "displayTimeUnit" in config else "MINUTE"
            self.surrogate_ip_enforced_for_known_browsers = (
                config["surrogateIPEnforcedForKnownBrowsers"] if "surrogateIPEnforcedForKnownBrowsers" in config else False
            )
            self.surrogate_refresh_time_in_minutes = (
                config["surrogateRefreshTimeInMinutes"] if "surrogateRefreshTimeInMinutes" in config else 0
            )
            self.kerberos_auth = config["kerberosAuth"] if "kerberosAuth" in config else False
            self.digest_auth_enabled = config["digestAuthEnabled"] if "digestAuthEnabled" in config else False
            self.ofw_enabled = config["ofwEnabled"] if "ofwEnabled" in config else False
            self.ips_control = config["ipsControl"] if "ipsControl" in config else False
            self.aup_enabled = config["aupEnabled"] if "aupEnabled" in config else False
            self.caution_enabled = config["cautionEnabled"] if "cautionEnabled" in config else False
            self.aup_block_internet_until_accepted = (
                config["aupBlockInternetUntilAccepted"] if "aupBlockInternetUntilAccepted" in config else False
            )
            self.aup_force_ssl_inspection = config["aupForceSslInspection"] if "aupForceSslInspection" in config else False
            self.iot_discovery_enabled = config["iotDiscoveryEnabled"] if "iotDiscoveryEnabled" in config else False
            self.iot_enforce_policy_set = config["iotEnforcePolicySet"] if "iotEnforcePolicySet" in config else False
            self.aup_timeout_in_days = config["aupTimeoutInDays"] if "aupTimeoutInDays" in config else 0
            self.child_count = config["childCount"] if "childCount" in config else 0
            self.match_in_child = config["matchInChild"] if "matchInChild" in config else False
            self.exclude_from_dynamic_groups = (
                config["excludeFromDynamicGroups"] if "excludeFromDynamicGroups" in config else False
            )
            self.exclude_from_manual_groups = (
                config["excludeFromManualGroups"] if "excludeFromManualGroups" in config else False
            )
            self.profile = config["profile"] if "profile" in config else "WORKLOAD"
            self.description = config["description"] if "description" in config else None

            self.ipv6_enabled = config["ipv6Enabled"] if "ipv6Enabled" in config else None

            self.ipv6_dns64_prefix = config["ipv6Dns64Prefix"] if "ipv6Dns64Prefix" in config else None

            self.managed_by = config["managedBy"] if "managedBy" in config else None

            self.multi_tenant_vpn_credential = (
                config["multiTenantVpnCredential"] if "multiTenantVpnCredential" in config else None
            )

            self.vpc_info = config["vpcInfo"] if "vpcInfo" in config else None

            self.public_cloud_account_id = config["publicCloudAccountId"] if "publicCloudAccountId" in config else None

            # Handling nested lists and collections
            self.static_location_groups = ZscalerCollection.form_list(
                config["staticLocationGroups"] if "staticLocationGroups" in config else [], dict
            )
            self.dynamic_location_groups = ZscalerCollection.form_list(
                config["dynamiclocationGroups"] if "dynamiclocationGroups" in config else [], dict
            )

            self.vpn_credentials = ZscalerCollection.form_list(
                config["vpnCredentials"] if "vpnCredentials" in config else [], vpn_credentials.TrafficVPNCredentials
            )

            self.ip_addresses = ZscalerCollection.form_list(config["ipAddresses"] if "ipAddresses" in config else [], str)

            self.ports = ZscalerCollection.form_list(config["ports"] if "ports" in config else [], str)

            self.virtual_zens = ZscalerCollection.form_list(config["virtualZens"] if "virtualZens" in config else [], str)

            self.virtual_zen_clusters = ZscalerCollection.form_list(
                config["virtualZenClusters"] if "virtualZenClusters" in config else [], str
            )

        else:
            self.id = None
            self.name = None
            self.non_editable = False
            self.parent_id = 0
            self.up_bandwidth = 0
            self.dn_bandwidth = 0
            self.override_up_bandwidth = 0
            self.override_dn_bandwidth = 0
            self.shared_up_bandwidth = 0
            self.shared_down_bandwidth = 0
            self.unused_up_bandwidth = 0
            self.unused_dn_bandwidth = 0
            self.country = "NONE"
            self.language = "NONE"
            self.tz = "NOT_SPECIFIED"
            self.geo_override = False
            self.latitude = 0.0
            self.longitude = 0.0
            self.auth_required = False
            self.ssl_scan_enabled = False
            self.zapp_ssl_scan_enabled = False
            self.xff_forward_enabled = False
            self.other_sub_location = False
            self.other6_sub_location = False
            self.ec_location = False
            self.surrogate_ip = False
            self.cookies_and_proxy = False
            self.idle_time_in_minutes = 0
            self.display_time_unit = "MINUTE"
            self.surrogate_ip_enforced_for_known_browsers = False
            self.surrogate_refresh_time_in_minutes = 0
            self.kerberos_auth = False
            self.digest_auth_enabled = False
            self.ofw_enabled = False
            self.ips_control = False
            self.aup_enabled = False
            self.caution_enabled = False
            self.aup_block_internet_until_accepted = False
            self.aup_force_ssl_inspection = False
            self.iot_discovery_enabled = False
            self.iot_enforce_policy_set = False
            self.aup_timeout_in_days = 0
            self.child_count = 0
            self.match_in_child = False
            self.exclude_from_dynamic_groups = False
            self.exclude_from_manual_groups = False
            self.managed_by = None
            self.profile = "WORKLOAD"
            self.description = None
            self.ipv6_enabled = None
            self.ipv6_dns64_prefix = None
            self.multi_tenant_vpn_credential = None
            self.vpc_info = None
            self.public_cloud_account_id = None
            self.virtual_zens = []
            self.virtual_zen_clusters = []
            self.static_location_groups = []
            self.dynamic_location_groups = []
            self.vpn_credentials = []
            self.ip_addresses = []
            self.ports = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "nonEditable": self.non_editable,
            "parentId": self.parent_id,
            "upBandwidth": self.up_bandwidth,
            "dnBandwidth": self.dn_bandwidth,
            "overrideUpBandwidth": self.override_up_bandwidth,
            "overrideDnBandwidth": self.override_dn_bandwidth,
            "sharedUpBandwidth": self.shared_up_bandwidth,
            "sharedDownBandwidth": self.shared_down_bandwidth,
            "unusedUpBandwidth": self.unused_up_bandwidth,
            "unusedDnBandwidth": self.unused_dn_bandwidth,
            "country": self.country,
            "language": self.language,
            "tz": self.tz,
            "geoOverride": self.geo_override,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "authRequired": self.auth_required,
            "sslScanEnabled": self.ssl_scan_enabled,
            "zappSslScanEnabled": self.zapp_ssl_scan_enabled,
            "xffForwardEnabled": self.xff_forward_enabled,
            "otherSubLocation": self.other_sub_location,
            "other6SubLocation": self.other6_sub_location,
            "ecLocation": self.ec_location,
            "surrogateIP": self.surrogate_ip,
            "cookiesAndProxy": self.cookies_and_proxy,
            "idleTimeInMinutes": self.idle_time_in_minutes,
            "displayTimeUnit": self.display_time_unit,
            "surrogateIPEnforcedForKnownBrowsers": self.surrogate_ip_enforced_for_known_browsers,
            "surrogateRefreshTimeInMinutes": self.surrogate_refresh_time_in_minutes,
            "kerberosAuth": self.kerberos_auth,
            "digestAuthEnabled": self.digest_auth_enabled,
            "ofwEnabled": self.ofw_enabled,
            "ipsControl": self.ips_control,
            "aupEnabled": self.aup_enabled,
            "cautionEnabled": self.caution_enabled,
            "aupBlockInternetUntilAccepted": self.aup_block_internet_until_accepted,
            "aupForceSslInspection": self.aup_force_ssl_inspection,
            "iotDiscoveryEnabled": self.iot_discovery_enabled,
            "iotEnforcePolicySet": self.iot_enforce_policy_set,
            "aupTimeoutInDays": self.aup_timeout_in_days,
            "childCount": self.child_count,
            "matchInChild": self.match_in_child,
            "virtualZens": self.virtual_zens,
            "virtualZenClusters": self.virtual_zen_clusters,
            "profile": self.profile,
            "description": self.description,
            "ipAddresses": self.ip_addresses,
            "ports": self.ports,
            "ipv6Enabled": self.ipv6_enabled,
            "ipv6Dns64Prefix": self.ipv6_dns64_prefix,
            "multiTenantVpnCredential": self.multi_tenant_vpn_credential,
            "vpcInfo": self.vpc_info,
            "publicCloudAccountId": self.public_cloud_account_id,
            "excludeFromDynamicGroups": self.exclude_from_dynamic_groups,
            "excludeFromManualGroups": self.exclude_from_manual_groups,
            "staticLocationGroups": [static.request_format() for static in (self.static_location_groups or [])],
            "dynamiclocationGroups": [dyn.request_format() for dyn in (self.dynamic_location_groups or [])],
            "vpnCredentials": [vpn.request_format() for vpn in (self.vpn_credentials or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
