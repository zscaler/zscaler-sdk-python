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

from zscaler.zia.models import common as common


class LocationManagement(ZscalerObject):
    """
    A class representing a Location object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        # print("🚨 Raw config passed into LocationManagement:")
        # import pprint
        # pprint.pprint(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.non_editable = config["nonEditable"] if "nonEditable" in config else False
            self.parent_id = config["parentId"] if "parentId" in config else None
            self.up_bandwidth = config["upBandwidth"] if "upBandwidth" in config else None
            self.dn_bandwidth = config["dnBandwidth"] if "dnBandwidth" in config else None
            self.country = config["country"] if "country" in config else None
            self.language = config["language"] if "language" in config else None
            self.tz = config["tz"] if "tz" in config else None
            self.geo_override = config["geoOverride"] if "geoOverride" in config else False
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.auth_required = config["authRequired"] if "authRequired" in config else False
            self.ssl_scan_enabled = config["sslScanEnabled"] if "sslScanEnabled" in config else False
            self.zapp_ssl_scan_enabled = config["zappSslScanEnabled"] if "zappSslScanEnabled" in config else False
            self.xff_forward_enabled = config["xffForwardEnabled"] if "xffForwardEnabled" in config else False
            self.other_sub_location = config["otherSubLocation"] if "otherSubLocation" in config else False
            self.ec_location = config["ecLocation"] if "ecLocation" in config else False

            # self.surrogate_ip = config["surrogateIP"] \
            #     if "surrogateIP" in config else False

            # print("💥 SurrogateIP Debug:",
            #     config.get("surrogate_ip"),
            #     config.get("surrogateIp"),
            #     config.get("surrogateIP"))

            self.surrogate_ip = (
                config.get("surrogate_ip")  # ← used by the converted keys
                or config.get("surrogateIp")  # ← if not snake_cased
                or config.get("surrogateIP")  # ← raw from the API
                or False  # ← fallback
            )

            self.cookies_and_proxy = config["cookiesAndProxy"] if "cookiesAndProxy" in config else None
            self.idle_time_in_minutes = config["idleTimeInMinutes"] if "idleTimeInMinutes" in config else None
            self.display_time_unit = config["displayTimeUnit"] if "displayTimeUnit" in config else None
            self.surrogate_ip_enforced_for_known_browsers = (
                config["surrogateIPEnforcedForKnownBrowsers"] if "surrogateIPEnforcedForKnownBrowsers" in config else False
            )
            self.surrogate_refresh_time_in_minutes = (
                config["surrogateRefreshTimeInMinutes"] if "surrogateRefreshTimeInMinutes" in config else None
            )
            self.kerberos_auth = config["kerberosAuth"] if "kerberosAuth" in config else False
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
            self.aup_timeout_in_days = config["aupTimeoutInDays"] if "aupTimeoutInDays" in config else None
            self.child_count = config["childCount"] if "childCount" in config else None
            self.match_in_child = config["matchInChild"] if "matchInChild" in config else False
            self.exclude_from_dynamic_groups = (
                config["excludeFromDynamicGroups"] if "excludeFromDynamicGroups" in config else None
            )
            self.exclude_from_manual_groups = (
                config["excludeFromManualGroups"] if "excludeFromManualGroups" in config else None
            )
            self.profile = config["profile"] if "profile" in config else None

            self.default_extranet_ts_pool = config["defaultExtranetTsPool"] if "defaultExtranetTsPool" in config else False

            self.default_extranet_dns = config["defaultExtranetDns"] if "defaultExtranetDns" in config else False

            self.ipv6_enabled = config["ipv6Enabled"] if "ipv6Enabled" in config else False

            self.basic_auth_enabled = config["basicAuthEnabled"] if "basicAuthEnabled" in config else False

            self.digest_auth_enabled = config["digestAuthEnabled"] if "digestAuthEnabled" in config else False

            # Handling nested lists and collections
            self.static_location_groups = ZscalerCollection.form_list(
                config["staticLocationGroups"] if "staticLocationGroups" in config else [], common.CommonIDName
            )

            self.dynamic_location_groups = ZscalerCollection.form_list(
                config["dynamiclocationGroups"] if "dynamiclocationGroups" in config else [], common.CommonIDName
            )

            self.vpn_credentials = ZscalerCollection.form_list(
                config["vpnCredentials"] if "vpnCredentials" in config else [], VPNCredentials
            )

            self.ip_addresses = ZscalerCollection.form_list(config["ipAddresses"] if "ipAddresses" in config else [], str)

            if "extranet" in config:
                if isinstance(config["extranet"], common.CommonIDName):
                    self.extranet = config["extranet"]
                elif config["extranet"] is not None:
                    self.extranet = common.CommonIDName(config["extranet"])
                else:
                    self.extranet = None
            else:
                self.extranet = None

            if "extranetIpPool" in config:
                if isinstance(config["extranetIpPool"], common.CommonIDName):
                    self.extranet_ip_pool = config["extranetIpPool"]
                elif config["extranetIpPool"] is not None:
                    self.extranet_ip_pool = common.CommonIDName(config["extranetIpPool"])
                else:
                    self.extranet_ip_pool = None
            else:
                self.extranet_ip_pool = None

            if "extranetDns" in config:
                if isinstance(config["extranetDns"], common.CommonIDName):
                    self.extranet_dns = config["extranetDns"]
                elif config["extranetDns"] is not None:
                    self.extranet_dns = common.CommonIDName(config["extranetDns"])
                else:
                    self.extranet_dns = None
            else:
                self.extranet_dns = None

        else:
            self.id = None
            self.name = None
            self.description = None
            self.non_editable = False
            self.parent_id = None
            self.up_bandwidth = None
            self.dn_bandwidth = None
            self.country = None
            self.language = None
            self.tz = None
            self.geo_override = False
            self.latitude = None
            self.longitude = None
            self.auth_required = False
            self.ssl_scan_enabled = False
            self.zapp_ssl_scan_enabled = False
            self.xff_forward_enabled = False
            self.other_sub_location = None
            self.ec_location = None
            self.surrogate_ip = False
            self.cookies_and_proxy = None
            self.idle_time_in_minutes = None
            self.display_time_unit = None
            self.surrogate_ip_enforced_for_known_browsers = False
            self.surrogate_refresh_time_in_minutes = None
            self.kerberos_auth = False
            self.basic_auth_enabled = False
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
            self.ipv6_enabled = False
            self.exclude_from_dynamic_groups = None
            self.exclude_from_manual_groups = None
            self.profile = None
            self.extranet = None
            self.extranet_ip_pool = None
            self.extranet_dns = None
            self.static_location_groups = []
            self.dynamic_location_groups = []
            self.vpn_credentials = []
            self.ip_addresses = []

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
            "ecLocation": self.ec_location,
            "surrogateIP": self.surrogate_ip,
            "cookiesAndProxy": self.cookies_and_proxy,
            "idleTimeInMinutes": self.idle_time_in_minutes,
            "displayTimeUnit": self.display_time_unit,
            "surrogateIPEnforcedForKnownBrowsers": self.surrogate_ip_enforced_for_known_browsers,
            "surrogateRefreshTimeInMinutes": self.surrogate_refresh_time_in_minutes,
            "kerberosAuth": self.kerberos_auth,
            "basicAuthEnabled": self.basic_auth_enabled,
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
            "excludeFromDynamicGroups": self.exclude_from_dynamic_groups,
            "excludeFromManualGroups": self.exclude_from_manual_groups,
            "profile": self.profile,
            "description": self.description,
            "ipAddresses": self.ip_addresses,
            "ipv6Enabled": self.ipv6_enabled,
            "extranet": self.extranet,
            "extranetIpPool": self.extranet_ip_pool,
            "extranetDns": self.extranet_dns,
            "defaultExtranetTsPool": self.default_extranet_ts_pool,
            "defaultExtranetDns": self.default_extranet_dns,
            "staticLocationGroups": [static.request_format() for static in (self.static_location_groups or [])],
            "dynamiclocationGroups": [dyn.request_format() for dyn in (self.dynamic_location_groups or [])],
            "vpnCredentials": [vpn.request_format() for vpn in (self.vpn_credentials or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class VPNCredentials(ZscalerObject):
    """
    A class representing a VPN Credentials object.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.type = config["type"] if "type" in config else None
            self.fqdn = config["fqdn"] if "fqdn" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.comments = config["comments"] if "comments" in config else None

        else:
            self.id = None
            self.type = None
            self.fqdn = None
            self.ip_address = None
            self.comments = None
            self.location = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "type": self.type,
            "fqdn": self.fqdn,
            "ipAddress": self.ip_address,
            "comments": self.comments,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
