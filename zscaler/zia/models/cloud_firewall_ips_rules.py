# flake8: noqa
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
from zscaler.zia.models import device_groups as device_groups
from zscaler.zia.models import devices as devices
from zscaler.zia.models import location_management as location_management
from zscaler.zia.models import location_group as location_group
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import rule_labels as rule_labels
from zscaler.zia.models import cloud_firewall_time_windows as time_windows
from zscaler.zia.models import cloud_firewall_destination_groups as destination_groups
from zscaler.zia.models import cloud_firewall_source_groups as source_groups
from zscaler.zia.models import cloud_firewall_nw_service_groups as nw_service_groups
from zscaler.zia.models import cloud_firewall_nw_service as nw_service
from zscaler.zia.models import common as common


class FirewallIPSrules(ZscalerObject):
    """
    A class for FirewallIPSrules objects.
    """

    def __init__(self, config=None):
        """
        Initialize the FirewallIPSrules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.access_control = config["accessControl"] if "accessControl" in config else None
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.order = config["order"] if "order" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.action = config["action"] if "action" in config else None
            self.capture_pcap = config["capturePCAP"] if "capturePCAP" in config else None
            self.state = config["state"] if "state" in config else None
            self.description = config["description"] if "description" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None

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
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            self.src_ips = ZscalerCollection.form_list(config["srcIps"] if "srcIps" in config else [], str)
            self.src_ip_groups = ZscalerCollection.form_list(
                config["srcIpGroups"] if config and "srcIpGroups" in config else [], source_groups.IPSourceGroup
            )
            self.src_ipv6_groups = ZscalerCollection.form_list(
                config["srcIpv6Groups"] if "srcIpv6Groups" in config else [], source_groups.IPSourceGroup
            )
            self.dest_addresses = ZscalerCollection.form_list(
                config["destAddresses"] if "destAddresses" in config else [], str
            )
            self.dest_ip_categories = ZscalerCollection.form_list(
                config["destIpCategories"] if "destIpCategories" in config else [], str
            )
            self.res_categories = ZscalerCollection.form_list(
                config["resCategories"] if "resCategories" in config else [], str
            )
            self.dest_countries = ZscalerCollection.form_list(
                config["destCountries"] if "destCountries" in config else [], str
            )
            self.source_countries = ZscalerCollection.form_list(
                config["sourceCountries"] if "sourceCountries" in config else [], str
            )
            self.dest_ip_groups = ZscalerCollection.form_list(
                config["destIpGroups"] if "destIpGroups" in config else [], destination_groups.IPDestinationGroups
            )
            self.dest_ipv6_groups = ZscalerCollection.form_list(
                config["destIpv6Groups"] if "destIpv6Groups" in config else [], destination_groups.IPDestinationGroups
            )
            self.nw_services = ZscalerCollection.form_list(
                config["nwServices"] if "nwServices" in config else [], nw_service.NetworkServices
            )
            self.nw_service_groups = ZscalerCollection.form_list(
                config["nwServiceGroups"] if "nwServiceGroups" in config else [], nw_service_groups.NetworkServiceGroups
            )

            self.threat_categories = ZscalerCollection.form_list(
                config["threatCategories"] if "threatCategories" in config else [], common.CommonIDNameTag
            )
            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], rule_labels.RuleLabels)
            # Reuse the external ZPAAppSegment class
            self.zpa_app_segments = ZscalerCollection.form_list(
                config["zpaAppSegments"] if "zpaAppSegments" in config else [], common.ResourceReference
            )
            self.enable_full_logging = config["enableFullLogging"] if "enableFullLogging" in config else None
            self.predefined = config["predefined"] if "predefined" in config else False
            self.default_rule = config["defaultRule"] if "defaultRule" in config else False

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None
        else:
            self.access_control = None
            self.id = None
            self.name = None
            self.order = None
            self.rank = None
            self.locations = []
            self.location_groups = []
            self.departments = []
            self.groups = []
            self.users = []
            self.time_windows = []
            self.action = None
            self.capture_pcap = None
            self.state = None
            self.description = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.src_ips = []
            self.src_ip_groups = []
            self.src_ipv6_groups = []
            self.dest_addresses = []
            self.dest_ip_categories = []
            self.res_categories = []
            self.dest_countries = []
            self.source_countries = []
            self.dest_ip_groups = []
            self.dest_ipv6_groups = []
            self.nw_services = []
            self.nw_service_groups = []
            self.threat_categories = []
            self.devices = []
            self.device_groups = []
            self.labels = []
            self.zpa_app_segments = []
            self.enable_full_logging = False
            self.predefined = False
            self.default_rule = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "accessControl": self.access_control,
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "rank": self.rank,
            "action": self.action,
            "capturePCAP": self.capture_pcap,
            "state": self.state,
            "description": self.description,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "srcIps": self.src_ips,
            "destAddresses": self.dest_addresses,
            "destIpCategories": self.dest_ip_categories,
            "resCategories": self.res_categories,
            "destCountries": self.dest_countries,
            "sourceCountries": self.source_countries,
            "locations": [loc.request_format() for loc in (self.locations or [])],
            "locationGroups": [loc_group.request_format() for loc_group in (self.location_groups or [])],
            "departments": [dept.request_format() for dept in (self.departments or [])],
            "groups": [group.request_format() for group in (self.groups or [])],
            "users": [user.request_format() for user in (self.users or [])],
            "timeWindows": [window.request_format() for window in (self.time_windows or [])],
            "srcIpGroups": [sig.request_format() for sig in (self.src_ip_groups or [])],
            "srcIpv6Groups": [sig.request_format() for sig in (self.src_ipv6_groups or [])],
            "destIpGroups": [dig.request_format() for dig in (self.dest_ip_groups or [])],
            "destIpv6Groups": [dig.request_format() for dig in (self.dest_ipv6_groups or [])],
            "nwServices": [service.request_format() for service in (self.nw_services or [])],
            "nwServiceGroups": [sg.request_format() for sg in (self.nw_service_groups or [])],
            "threatCategories": [tc.request_format() for tc in (self.threat_categories or [])],
            "devices": [device.request_format() for device in (self.devices or [])],
            "deviceGroups": [dg.request_format() for dg in (self.device_groups or [])],
            "labels": [label.request_format() for label in (self.labels or [])],
            "zpaAppSegments": [zpa.request_format() for zpa in (self.zpa_app_segments or [])],
            "enableFullLogging": self.enable_full_logging,
            "predefined": self.predefined,
            "defaultRule": self.default_rule,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
