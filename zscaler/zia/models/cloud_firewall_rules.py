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
from zscaler.zia.models import workload_groups as workload_groups
from zscaler.zia.models import cloud_firewall_app_services as app_services
from zscaler.zia.models import cloud_firewall_destination_groups as destination_groups
from zscaler.zia.models import cloud_firewall_source_groups as source_groups
from zscaler.zia.models import cloud_firewall_nw_service_groups as nw_service_groups
from zscaler.zia.models import cloud_firewall_nw_service as nw_service
from zscaler.zia.models import cloud_firewall_nw_application_groups as nw_application_groups
from zscaler.zia.models import common as common_reference
from zscaler.zia.models import common as common


class FirewallRule(ZscalerObject):
    """
    A class representing a Firewall Rule object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.access_control = config["accessControl"] if "accessControl" in config else None
            self.enable_full_logging = config["enableFullLogging"] if "enableFullLogging" in config else False
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.order = config["order"] if "order" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.action = config["action"] if "action" in config else None
            # self.capture_pcap = config["capturePCAP"]\
            #     if "capturePCAP" in config else False
            self.state = config["state"] if "state" in config else None
            self.description = config["description"] if "description" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.exclude_src_countries = config["excludeSrcCountries"] if "excludeSrcCountries" in config else False
            # Handling lists of simple values
            self.dest_ip_categories = ZscalerCollection.form_list(
                config["destIpCategories"] if "destIpCategories" in config else [], str
            )
            self.dest_countries = ZscalerCollection.form_list(
                config["destCountries"] if "destCountries" in config else [], str
            )
            self.source_countries = ZscalerCollection.form_list(
                config["sourceCountries"] if "sourceCountries" in config else [], str
            )
            # self.exclude_src_countries = ZscalerCollection.form_list(
            #     config["excludeSrcCountries"] if "excludeSrcCountries" in config else [], str
            # )
            self.device_trust_levels = ZscalerCollection.form_list(
                config["deviceTrustLevels"] if "deviceTrustLevels" in config else [], str
            )
            self.nw_applications = ZscalerCollection.form_list(
                config["nwApplications"] if "nwApplications" in config else [], str
            )
            self.src_ips = ZscalerCollection.form_list(config["srcIps"] if "srcIps" in config else [], str)
            self.dest_addresses = ZscalerCollection.form_list(
                config["destAddresses"] if "destAddresses" in config else [], str
            )

            self.dest_addresses = ZscalerCollection.form_list(
                config["destAddresses"] if "destAddresses" in config else [], str
            )

            self.app_service_groups = ZscalerCollection.form_list(
                config["appServiceGroups"] if "appServiceGroups" in config else [], app_services.AppServices
            )
            self.app_services = ZscalerCollection.form_list(
                config["appServices"] if "appServices" in config else [], app_services.AppServices
            )
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
            self.dest_ip_groups = ZscalerCollection.form_list(
                config["destIpGroups"] if "destIpGroups" in config else [], destination_groups.IPDestinationGroups
            )
            self.src_ip_groups = ZscalerCollection.form_list(
                config["srcIpGroups"] if config and "srcIpGroups" in config else [], source_groups.IPSourceGroup
            )
            self.src_ipv6_groups = ZscalerCollection.form_list(
                config["srcIpv6Groups"] if "srcIpv6Groups" in config else [], source_groups.IPSourceGroup
            )
            self.dest_ipv6_groups = ZscalerCollection.form_list(
                config["destIpv6Groups"] if "destIpv6Groups" in config else [], destination_groups.IPDestinationGroups
            )
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            self.workload_groups = ZscalerCollection.form_list(
                config["workloadGroups"] if "workloadGroups" in config else [], workload_groups.WorkloadGroups
            )
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )

            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)

            self.labels = ZscalerCollection.form_list(
                config["labels"] if "labels" in config else [], rule_labels.RuleLabels
            )

            self.nw_services = ZscalerCollection.form_list(
                config["nwServices"] if "nwServices" in config else [], nw_service.NetworkServices
            )
            self.nw_service_groups = ZscalerCollection.form_list(
                config["nwServiceGroups"] if "nwServiceGroups" in config else [], nw_service_groups.NetworkServiceGroups
            )
            self.nw_application_groups = ZscalerCollection.form_list(
                config["nwApplicationGroups"] if "nwApplicationGroups" in config else [],
                nw_application_groups.NetworkApplicationGroups,
            )
            # Reuse the external ZPAAppSegment class
            self.zpa_app_segments = ZscalerCollection.form_list(
                config["zpaAppSegments"] if "zpaAppSegments" in config else [], common_reference.ResourceReference
            )

            self.default_rule = config["defaultRule"] if "defaultRule" in config else False

            self.predefined = config["predefined"] if "predefined" in config else False

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
            # Defaults if config is None
            self.access_control = None
            self.enable_full_logging = False
            self.id = None
            self.name = None
            self.order = None
            self.rank = None
            self.action = None
            # self.capture_pcap = None
            self.state = None
            self.description = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.dest_ip_categories = []
            self.dest_countries = []
            self.source_countries = []
            self.device_trust_levels = []
            self.nw_applications = []
            self.src_ips = []
            self.dest_addresses = []
            self.app_service_groups = []
            self.locations = []
            self.location_groups = []
            self.departments = []
            self.groups = []
            self.users = []
            self.nw_services = []
            self.nw_service_groups = []
            self.nw_application_groups = []
            self.src_ip_groups = []
            self.dest_ip_groups = []
            self.zpa_app_segments = []
            self.workload_groups = []
            self.device_groups = []
            self.src_ipv6_groups = []
            self.dest_ipv6_groups = []
            self.default_rule = False
            self.exclude_src_countries = False
            self.predefined = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "accessControl": self.access_control,
            "enableFullLogging": self.enable_full_logging,
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "rank": self.rank,
            "action": self.action,
            # "capturePCAP": self.capture_pcap,
            "state": self.state,
            "description": self.description,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "destIpCategories": self.dest_ip_categories,
            "destCountries": self.dest_countries,
            "sourceCountries": self.source_countries,
            "deviceTrustLevels": self.device_trust_levels,
            "nwApplications": self.nw_applications,
            "srcIps": self.src_ips,
            "destAddresses": self.dest_addresses,
            # Applying fallback to all attributes with similar structure
            "appServiceGroups": [asg.request_format() for asg in (self.app_service_groups or [])],
            "locations": [loc.request_format() for loc in (self.locations or [])],
            "locationGroups": [lg.request_format() for lg in (self.location_groups or [])],
            "departments": [dept.request_format() for dept in (self.departments or [])],
            "groups": [grp.request_format() for grp in (self.groups or [])],
            "users": [user.request_format() for user in (self.users or [])],
            "nwServices": [service.request_format() for service in (self.nw_services or [])],
            "nwServiceGroups": [sg.request_format() for sg in (self.nw_service_groups or [])],
            "nwApplicationGroups": [ag.request_format() for ag in (self.nw_application_groups or [])],
            "srcIpGroups": [sig.request_format() for sig in (self.src_ip_groups or [])],
            "destIpGroups": [dig.request_format() for dig in (self.dest_ip_groups or [])],
            "srcIpv6Groups": [sig.request_format() for sig in (self.src_ipv6_groups or [])],
            "destIpv6Groups": [dig.request_format() for dig in (self.dest_ipv6_groups or [])],
            "zpaAppSegments": [zpa.request_format() for zpa in (self.zpa_app_segments or [])],
            "workloadGroups": [wg.request_format() for wg in (self.workload_groups or [])],
            "deviceGroups": [dg.request_format() for dg in (self.device_groups or [])],
            "devices": [dg.request_format() for dg in (self.devices or [])],
            "defaultRule": self.default_rule,
            "excludeSrcCountries": self.exclude_src_countries,
            "predefined": self.predefined,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
