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
from zscaler.zia.models import cloud_firewall_nw_service_groups as nw_service_groups
from zscaler.zia.models import cloud_firewall_nw_service as nw_service
from zscaler.zia.models import common


class NatControlPolicy(ZscalerObject):
    """
    A class for NatControlPolicy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the NatControlPolicy model based on API response.

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
            self.state = config["state"] if "state" in config else None
            self.action = config["action"] if "action" in config else "ALLOW"
            self.enable_full_logging = config["enableFullLogging"] if "enableFullLogging" in config else False
            self.description = config["description"] if "description" in config else None

            self.redirect_ip = config["redirectIp"] if "redirectIp" in config else None
            self.redirect_port = config["redirectPort"] if "redirectPort" in config else None
            self.redirect_fqdn = config["redirectFqdn"] if "redirectFqdn" in config else None
            self.trusted_resolver_rule = config["trustedResolverRule"] if "trustedResolverRule" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None

            self.predefined = config["predefined"] if "predefined" in config else None
            self.default_rule = config["defaultRule"] if "defaultRule" in config else None

            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )

            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)

            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], rule_labels.RuleLabels)

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

            self.nw_services = ZscalerCollection.form_list(
                config["nwServices"] if "nwServices" in config else [], nw_service.NetworkServices
            )
            self.nw_service_groups = ZscalerCollection.form_list(
                config["nwServiceGroups"] if "nwServiceGroups" in config else [], nw_service_groups.NetworkServiceGroups
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

            self.src_ips = ZscalerCollection.form_list(config["srcIps"] if "srcIps" in config else [], str)
            self.dest_addresses = ZscalerCollection.form_list(
                config["destAddresses"] if "destAddresses" in config else [], str
            )

            self.dest_countries = ZscalerCollection.form_list(
                config["destCountries"] if "destCountries" in config else [], str
            )
            self.dest_ip_categories = ZscalerCollection.form_list(
                config["destIpCategories"] if "destIpCategories" in config else [], str
            )
            self.res_categories = ZscalerCollection.form_list(
                config["resCategories"] if "resCategories" in config else [], str
            )

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
            self.action = "ALLOW"
            self.access_control = None
            self.id = None
            self.name = None
            self.order = None
            self.rank = None
            self.description = None
            self.enable_full_logging = False
            self.locations = []
            self.location_groups = []
            self.groups = []
            self.departments = []
            self.users = []
            self.state = None
            self.time_windows = []
            self.src_ips = []
            self.src_ip_groups = []
            self.src_ipv6_groups = []
            self.dest_addresses = []
            self.dest_ip_groups = []
            self.dest_ipv6_groups = []
            self.dest_countries = []
            self.dest_ip_categories = []
            self.res_categories = []
            self.nw_services = []
            self.nw_service_groups = []
            self.redirect_ip = None
            self.redirect_port = None
            self.redirect_fqdn = None
            self.trusted_resolver_rule = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.devices = []
            self.device_groups = []
            self.labels = []
            self.predefined = None
            self.default_rule = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "accessControl": self.access_control,
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "rank": self.rank,
            "description": self.description,
            "enableFullLogging": self.enable_full_logging,
            "locations": self.locations,
            "locationGroups": self.location_groups,
            "groups": self.groups,
            "departments": self.departments,
            "users": self.users,
            "state": self.state,
            "timeWindows": self.time_windows,
            "srcIps": self.src_ips,
            "srcIpGroups": self.src_ip_groups,
            "srcIpv6Groups": self.src_ipv6_groups,
            "destAddresses": self.dest_addresses,
            "destIpGroups": self.dest_ip_groups,
            "destIpv6Groups": self.dest_ipv6_groups,
            "destCountries": self.dest_countries,
            "destIpCategories": self.dest_ip_categories,
            "resCategories": self.res_categories,
            "nwServices": self.nw_services,
            "nwServiceGroups": self.nw_service_groups,
            "redirectIp": self.redirect_ip,
            "redirectPort": self.redirect_port,
            "redirectFqdn": self.redirect_fqdn,
            "trustedResolverRule": self.trusted_resolver_rule,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "devices": self.devices,
            "deviceGroups": self.device_groups,
            "labels": self.labels,
            "predefined": self.predefined,
            "defaultRule": self.default_rule,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
