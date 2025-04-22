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
from zscaler.zia.models import cloud_firewall_nw_service_groups as nw_service_groups
from zscaler.zia.models import cloud_firewall_nw_service as nw_service
from zscaler.zia.models import cloud_firewall_nw_application_groups as nw_application_groups
from zscaler.zia.models import zpa_gateway as zpa_gateway
from zscaler.zia.models import common as common_reference


class ForwardingControlRule(ZscalerObject):
    """
    A class representing a Forwarding Control Rule object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.type = config["type"] if "type" in config else None
            self.order = config["order"] if "order" in config else None
            self.rank = config["rank"] if "rank" in config else None
            self.state = config["state"] if "state" in config else None
            self.forward_method = config["forwardMethod"] if "forwardMethod" in config else None
            self.description = config["description"] if "description" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.last_modified_by = config["lastModifiedBy"] if "lastModifiedBy" in config else None
            self.zpa_broker_rule = config["zpaBrokerRule"] if "zpaBrokerRule" in config else None

            # Handling lists of simple values
            self.src_ips = ZscalerCollection.form_list(config["srcIps"] if "srcIps" in config else [], str)

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
            self.nw_applications = ZscalerCollection.form_list(
                config["nwApplications"] if "nwApplications" in config else [], str
            )

            # Handling nested lists of objects
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.location_groups = ZscalerCollection.form_list(
                config["locationGroups"] if "locationGroups" in config else [], location_group.LocationGroup
            )
            self.ec_groups = ZscalerCollection.form_list(
                config["ecGroups"] if "ecGroups" in config else [], common_reference.ResourceReference
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.groups = ZscalerCollection.form_list(config["groups"] if "groups" in config else [], user_management.Groups)

            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.src_ip_groups = ZscalerCollection.form_list(
                config["srcIpGroups"] if "srcIpGroups" in config else [], common_reference.ResourceReference
            )
            self.src_ipv6_groups = ZscalerCollection.form_list(
                config["srcIpv6Groups"] if "srcIpv6Groups" in config else [], common_reference.ResourceReference
            )
            self.dest_ip_groups = ZscalerCollection.form_list(
                config["destIpGroups"] if "destIpGroups" in config else [], common_reference.ResourceReference
            )
            self.dest_ipv6_groups = ZscalerCollection.form_list(
                config["destIpv6Groups"] if "destIpv6Groups" in config else [], common_reference.ResourceReference
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
            self.time_windows = ZscalerCollection.form_list(
                config["timeWindows"] if "timeWindows" in config else [], time_windows.TimeWindows
            )
            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], rule_labels.RuleLabels)
            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )
            self.zpa_app_segments = ZscalerCollection.form_list(
                config["zpaAppSegments"] if "zpaAppSegments" in config else [], common_reference.ResourceReference
            )
            self.zpa_application_segments = ZscalerCollection.form_list(
                config["zpaApplicationSegments"] if "zpaApplicationSegments" in config else [],
                common_reference.ResourceReference,
            )
            self.zpa_application_segment_groups = ZscalerCollection.form_list(
                config["zpaApplicationSegmentGroups"] if "zpaApplicationSegmentGroups" in config else [],
                common_reference.ResourceReference,
            )

            if "proxyGateway" in config:
                if isinstance(config["proxyGateway"], common_reference.CommonBlocks):
                    self.proxy_gateway = config["proxyGateway"]
                elif config["proxyGateway"] is not None:
                    self.proxy_gateway = common_reference.CommonBlocks(config["proxyGateway"])
                else:
                    self.proxy_gateway = None
            else:
                self.proxy_gateway = None

            if "zpaGateway" in config:
                if isinstance(config["zpaGateway"], common_reference.CommonBlocks):
                    self.zpa_gateway = config["zpaGateway"]
                elif config["zpaGateway"] is not None:
                    self.zpa_gateway = common_reference.CommonBlocks(config["zpaGateway"])
                else:
                    self.zpa_gateway = None
            else:
                self.zpa_gateway = None

        else:
            # Defaults when config is None
            self.id = None
            self.name = None
            self.type = None
            self.order = None
            self.rank = None
            self.state = None
            self.forward_method = None
            self.description = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.src_ips = []
            self.dest_addresses = []
            self.dest_ip_categories = []
            self.res_categories = []
            self.dest_countries = []
            self.nw_applications = []
            self.locations = []
            self.location_groups = []
            self.ec_groups = []
            self.departments = []
            self.groups = []
            self.users = []
            self.src_ip_groups = []
            self.src_ipv6_groups = []
            self.dest_ip_groups = []
            self.dest_ipv6_groups = []
            self.nw_services = []
            self.nw_service_groups = []
            self.nw_application_groups = []
            self.time_windows = []
            self.labels = []
            self.devices = []
            self.device_groups = []
            self.zpa_app_segments = []
            self.zpa_application_segments = []
            self.zpa_application_segment_groups = []
            self.proxy_gateway = None
            self.zpa_gateway = None
            self.zpa_broker_rule = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "order": self.order,
            "rank": self.rank,
            "state": self.state,
            "forwardMethod": self.forward_method,
            "description": self.description,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "srcIps": self.src_ips,
            "destAddresses": self.dest_addresses,
            "destIpCategories": self.dest_ip_categories,
            "resCategories": self.res_categories,
            "destCountries": self.dest_countries,
            "nwApplications": self.nw_applications,
            "locations": [loc.request_format() for loc in (self.locations or [])],
            "locationGroups": [loc_group.request_format() for loc_group in (self.location_groups or [])],
            "ecGroups": [ec_group.request_format() for ec_group in (self.ec_groups or [])],
            "departments": [dept.request_format() for dept in (self.departments or [])],
            "groups": [group.request_format() for group in (self.groups or [])],
            "users": [user.request_format() for user in (self.users or [])],
            "srcIpGroups": [sig.request_format() for sig in (self.src_ip_groups or [])],
            "srcIpv6Groups": [sig.request_format() for sig in (self.src_ipv6_groups or [])],
            "destIpGroups": [dig.request_format() for dig in (self.dest_ip_groups or [])],
            "destIpv6Groups": [dig.request_format() for dig in (self.dest_ipv6_groups or [])],
            "nwServices": [service.request_format() for service in (self.nw_services or [])],
            "nwServiceGroups": [service_group.request_format() for service_group in (self.nw_service_groups or [])],
            "nwApplicationGroups": [app_group.request_format() for app_group in (self.nw_application_groups or [])],
            "timeWindows": [window.request_format() for window in (self.time_windows or [])],
            "labels": [label.request_format() for label in (self.labels or [])],
            "devices": [device.request_format() for device in (self.devices or [])],
            "deviceGroups": [dg.request_format() for dg in (self.device_groups or [])],
            "zpaAppSegments": [zpa.request_format() for zpa in (self.zpa_app_segments or [])],
            "zpaApplicationSegments": [zpa_app.request_format() for zpa_app in (self.zpa_application_segments or [])],
            "zpaApplicationSegmentGroups": [
                zpa_app_group.request_format() for zpa_app_group in (self.zpa_application_segment_groups or [])
            ],
            "proxyGateway": self.proxy_gateway.request_format() if self.proxy_gateway else None,
            "zpaGateway": self.zpa_gateway.request_format() if self.zpa_gateway else None,
            "zpaBrokerRule": self.zpa_broker_rule,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
