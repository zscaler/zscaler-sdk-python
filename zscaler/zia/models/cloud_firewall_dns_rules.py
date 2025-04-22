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
from zscaler.zia.models import workload_groups as workload_groups
from zscaler.zia.models import cloud_firewall_destination_groups as destination_groups
from zscaler.zia.models import cloud_firewall_source_groups as source_groups
from zscaler.zia.models import cloud_firewall_nw_application_groups as nw_application_groups
from zscaler.zia.models import common as common


class FirewallDNSRules(ZscalerObject):
    """
    A class for FirewallDNSRules objects.
    """

    def __init__(self, config=None):
        """
        Initialize the FirewallDNSRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.action = config["action"] if "action" in config else None
            self.capture_pcap = config["capturePCAP"] if "capturePCAP" in config else None
            self.access_control = config["accessControl"] if "accessControl" in config else None
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.order = config["order"] if "order" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.description = config["description"] if "description" in config else None
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.location_groups = ZscalerCollection.form_list(
                config["locationGroups"] if "locationGroups" in config else [], location_group.LocationGroup
            )
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], user_management.Groups)
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.protocols = ZscalerCollection.form_list(config["protocols"] if "protocols" in config else [], str)
            self.state = config["state"] if "state" in config else None
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            self.src_ips = ZscalerCollection.form_list(config["srcIps"] if "srcIps" in config else [], str)
            self.src_ip_groups = ZscalerCollection.form_list(
                config["srcIpGroups"] if "srcIpGroups" in config else [], source_groups.IPSourceGroup
            )
            self.src_ipv6_groups = ZscalerCollection.form_list(
                config["srcIpv6Groups"] if "srcIpv6Groups" in config else [], source_groups.IPSourceGroup
            )
            self.dest_addresses = ZscalerCollection.form_list(
                config["destAddresses"] if "destAddresses" in config else [], str
            )
            self.dest_ip_groups = ZscalerCollection.form_list(
                config["destIpGroups"] if "destIpGroups" in config else [], destination_groups.IPDestinationGroups
            )
            self.dest_ipv6_groups = ZscalerCollection.form_list(
                config["destIpv6Groups"] if "destIpv6Groups" in config else [], destination_groups.IPDestinationGroups
            )
            self.dest_countries = ZscalerCollection.form_list(
                config["destCountries"] if "destCountries" in config else [], str
            )
            self.source_countries = ZscalerCollection.form_list(
                config["sourceCountries"] if "sourceCountries" in config else [], str
            )
            self.dest_ip_categories = ZscalerCollection.form_list(
                config["destIpCategories"] if "destIpCategories" in config else [], str
            )
            self.res_categories = ZscalerCollection.form_list(
                config["resCategories"] if "resCategories" in config else [], str
            )
            self.redirect_ip = config["redirectIp"] if "redirectIp" in config else None

            self.applications = ZscalerCollection.form_list(config["applications"] if "applications" in config else [], str)

            # Need to create model to iterate through application_groups list
            self.application_groups = ZscalerCollection.form_list(
                config["applicationGroups"] if "applicationGroups" in config else [], common.CommonIDName
            )

            self.edns_ecs_object = common.ResourceReference(config["ednsEcsObject"]) if "ednsEcsObject" in config else None

            self.dns_rule_request_types = ZscalerCollection.form_list(
                config["dnsRuleRequestTypes"] if "dnsRuleRequestTypes" in config else [], str
            )

            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.last_modified_by = config["lastModifiedBy"] if "lastModifiedBy" in config else None
            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], rule_labels.RuleLabels)
            self.block_response_code = config["blockResponseCode"] if "blockResponseCode" in config else None
            self.predefined = config["predefined"] if "predefined" in config else False
            self.default_rule = config["defaultRule"] if "defaultRule" in config else False

            if "zpaIpGroup" in config:
                if isinstance(config["zpaIpGroup"], common.CommonIDName):
                    self.zpa_ip_group = config["zpaIpGroup"]
                elif config["zpaIpGroup"] is not None:
                    self.zpa_ip_group = common.CommonIDName(config["zpaIpGroup"])
                else:
                    self.zpa_ip_group = None
            else:
                self.zpa_ip_group = None

            if "dnsGateway" in config:
                if isinstance(config["dnsGateway"], common.CommonBlocks):
                    self.dns_gateway = config["dnsGateway"]
                elif config["dnsGateway"] is not None:
                    self.dns_gateway = common.CommonBlocks(config["dnsGateway"])
                else:
                    self.dns_gateway = None
            else:
                self.dns_gateway = None

            if "ednsEcsObject" in config:
                if isinstance(config["ednsEcsObject"], common.CommonBlocks):
                    self.edns_ecs_object = config["ednsEcsObject"]
                elif config["ednsEcsObject"] is not None:
                    self.edns_ecs_object = common.CommonBlocks(config["ednsEcsObject"])
                else:
                    self.edns_ecs_object = None
            else:
                self.edns_ecs_object = None

        else:
            self.action = None
            self.capture_pcap = None
            self.access_control = None
            self.id = None
            self.name = None
            self.order = None
            self.rank = None
            self.description = None
            self.locations = []
            self.location_groups = []
            self.groups = []
            self.departments = []
            self.users = []
            self.protocols = []
            self.state = None
            self.time_windows = []
            self.src_ips = []
            self.src_ip_groups = []
            self.src_ipv6_groups = []
            self.dest_addresses = []
            self.dest_ip_groups = []
            self.dest_ipv6_groups = []
            self.dest_countries = []
            self.source_countries = []
            self.dest_ip_categories = []
            self.res_categories = []
            self.redirect_ip = None
            self.applications = []
            self.application_groups = []
            self.dns_gateway = None
            self.dns_rule_request_types = []
            self.zpa_ip_group = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.devices = []
            self.device_groups = []
            self.labels = []
            self.edns_ecs_object = None
            self.block_response_code = None
            self.predefined = False
            self.default_rule = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "capturePCAP": self.capture_pcap,
            "accessControl": self.access_control,
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "rank": self.rank,
            "description": self.description,
            "locations": [loc.request_format() for loc in (self.locations or [])],
            "locationGroups": [lg.request_format() for lg in (self.location_groups or [])],
            "departments": [dept.request_format() for dept in (self.departments or [])],
            "groups": [grp.request_format() for grp in (self.groups or [])],
            "users": [user.request_format() for user in (self.users or [])],
            "protocols": self.protocols,
            "state": self.state,
            "timeWindows": self.time_windows,
            "srcIps": self.src_ips,
            "srcIpGroups": [sig.request_format() for sig in (self.src_ip_groups or [])],
            "srcIpv6Groups": [sig.request_format() for sig in (self.src_ipv6_groups or [])],
            "destAddresses": self.dest_addresses,
            "destIpGroups": [dig.request_format() for dig in (self.dest_ip_groups or [])],
            "destIpv6Groups": [dig.request_format() for dig in (self.dest_ipv6_groups or [])],
            "destCountries": self.dest_countries,
            "sourceCountries": self.source_countries,
            "destIpCategories": self.dest_ip_categories,
            "resCategories": self.res_categories,
            "redirectIp": self.redirect_ip,
            "applications": self.applications,
            "applicationGroups": self.application_groups,
            "dnsGateway": self.dns_gateway,
            "dnsRuleRequestTypes": self.dns_rule_request_types,
            "zpaIpGroup": self.zpa_ip_group,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "devices": [dg.request_format() for dg in (self.devices or [])],
            "deviceGroups": [dg.request_format() for dg in (self.device_groups or [])],
            "labels": self.labels,
            "ednsEcsObject": self.edns_ecs_object,
            "blockResponseCode": self.block_response_code,
            "predefined": self.predefined,
            "defaultRule": self.default_rule,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
