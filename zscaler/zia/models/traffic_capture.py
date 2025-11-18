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
from zscaler.zia.models import common


class TrafficCapture(ZscalerObject):
    """
    A class for TrafficCapture objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TrafficCapture model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.order = config["order"] \
                if "order" in config else None
            self.rank = config["rank"] \
                if "rank" in config else None
            self.action = config["action"] \
                if "action" in config else None
            self.state = config["state"] \
                if "state" in config else None
            self.description = config["description"] \
                if "description" in config else None

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

            self.last_modified_time = config["lastModifiedTime"] \
                if "lastModifiedTime" in config else None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            self.src_ips = ZscalerCollection.form_list(
                config["srcIps"] if "srcIps" in config else [], str
            )
            self.src_ip_groups = ZscalerCollection.form_list(
                config["srcIpGroups"] if config and "srcIpGroups" in config else [], source_groups.IPSourceGroup
            )
            self.src_ipv6_groups = ZscalerCollection.form_list(
                config["srcIpv6Groups"] if "srcIpv6Groups" in config else [], source_groups.IPSourceGroup
            )
            self.dest_addresses = ZscalerCollection.form_list(
                config["destAddresses"] if "destAddresses" in config else [], str
            )
            self.dest_countries = ZscalerCollection.form_list(
                config["destCountries"] if "destCountries" in config else [], str
            )
            self.source_countries = ZscalerCollection.form_list(
                config["sourceCountries"] if "sourceCountries" in config else [], str
            )
            self.exclude_src_countries = config["excludeSrcCountries"] \
                if "excludeSrcCountries" in config else None

            self.dest_ip_groups = ZscalerCollection.form_list(
                config["destIpGroups"] if "destIpGroups" in config else [], destination_groups.IPDestinationGroups
            )
            self.dest_ipv6_groups = ZscalerCollection.form_list(
                config["destIpv6Groups"] if "destIpv6Groups" in config else [], destination_groups.IPDestinationGroups
            )
            self.nw_services = ZscalerCollection.form_list(
                config["nwServices"] if "nwServices" in config else [], str
            )
            self.nw_service_groups = ZscalerCollection.form_list(
                config["nwServiceGroups"] if "nwServiceGroups" in config else [], nw_service_groups.NetworkServiceGroups
            )
            self.nw_applications = ZscalerCollection.form_list(
                config["nwApplications"] if "nwApplications" in config else [], str
            )
            self.nw_application_groups = ZscalerCollection.form_list(
                config["nwApplicationGroups"] if "nwApplicationGroups" in config else [],
                nw_application_groups.NetworkApplicationGroups,
            )
            self.app_service_groups = ZscalerCollection.form_list(
                config["appServiceGroups"] if "appServiceGroups" in config else [], app_services.AppServices
            )
            self.device_groups = ZscalerCollection.form_list(
                config["deviceGroups"] if "deviceGroups" in config else [], device_groups.DeviceGroups
            )

            self.devices = ZscalerCollection.form_list(config["devices"] if "devices" in config else [], devices.Devices)

            self.device_trust_levels = ZscalerCollection.form_list(
                config["deviceTrustLevels"] if "deviceTrustLevels" in config else [], str
            )
            self.labels = ZscalerCollection.form_list(
                config["labels"] if "labels" in config else [], rule_labels.RuleLabels
            )
            self.txn_size_limit = config["txnSizeLimit"] \
                if "txnSizeLimit" in config else None
            self.txn_sampling = config["txnSampling"] \
                if "txnSampling" in config else None
            self.predefined = config["predefined"] \
                if "predefined" in config else None
            self.default_rule = config["defaultRule"] \
                if "defaultRule" in config else None
        else:
            self.id = None
            self.name = None
            self.order = None
            self.rank = None
            self.locations = ZscalerCollection.form_list([], location_management.LocationManagement)
            self.location_groups = ZscalerCollection.form_list([], location_group.LocationGroup)
            self.departments = ZscalerCollection.form_list([], user_management.Department)
            self.groups = ZscalerCollection.form_list([], user_management.Groups)
            self.users = ZscalerCollection.form_list([], user_management.UserManagement)
            self.time_windows = ZscalerCollection.form_list([], time_windows.TimeWindows)
            self.action = None
            self.state = None
            self.description = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.src_ips = ZscalerCollection.form_list([], str)
            self.src_ip_groups = ZscalerCollection.form_list([], source_groups.IPSourceGroup)
            self.src_ipv6_groups = ZscalerCollection.form_list([], source_groups.IPSourceGroup)
            self.dest_addresses = ZscalerCollection.form_list([], str)
            self.dest_countries = ZscalerCollection.form_list([], str)
            self.source_countries = ZscalerCollection.form_list([], str)
            self.exclude_src_countries = None
            self.dest_ip_groups = ZscalerCollection.form_list([], destination_groups.IPDestinationGroups)
            self.dest_ipv6_groups = ZscalerCollection.form_list([], destination_groups.IPDestinationGroups)
            self.nw_services = ZscalerCollection.form_list([], str)
            self.nw_service_groups = ZscalerCollection.form_list([], nw_service_groups.NetworkServiceGroups)
            self.nw_applications = ZscalerCollection.form_list([], str)
            self.nw_application_groups = ZscalerCollection.form_list([], nw_application_groups.NetworkApplicationGroups)
            self.app_service_groups = ZscalerCollection.form_list([], app_services.AppServices)
            self.devices = ZscalerCollection.form_list([], devices.Devices)
            self.device_groups = ZscalerCollection.form_list([], device_groups.DeviceGroups)
            self.device_trust_levels = ZscalerCollection.form_list([], str)
            self.labels = ZscalerCollection.form_list([], rule_labels.RuleLabels)
            self.txn_size_limit = None
            self.txn_sampling = None
            self.predefined = None
            self.default_rule = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "rank": self.rank,
            "locations": self.locations,
            "locationGroups": self.location_groups,
            "departments": self.departments,
            "groups": self.groups,
            "users": self.users,
            "timeWindows": self.time_windows,
            "action": self.action,
            "state": self.state,
            "description": self.description,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "srcIps": self.src_ips,
            "srcIpGroups": self.src_ip_groups,
            "srcIpv6Groups": self.src_ipv6_groups,
            "destAddresses": self.dest_addresses,
            "destCountries": self.dest_countries,
            "sourceCountries": self.source_countries,
            "excludeSrcCountries": self.exclude_src_countries,
            "destIpGroups": self.dest_ip_groups,
            "destIpv6Groups": self.dest_ipv6_groups,
            "nwServices": self.nw_services,
            "nwServiceGroups": self.nw_service_groups,
            "nwApplications": self.nw_applications,
            "nwApplicationGroups": self.nw_application_groups,
            "appServiceGroups": self.app_service_groups,
            "devices": self.devices,
            "deviceGroups": self.device_groups,
            "deviceTrustLevels": self.device_trust_levels,
            "labels": self.labels,
            "txnSizeLimit": self.txn_size_limit,
            "txnSampling": self.txn_sampling,
            "predefined": self.predefined,
            "defaultRule": self.default_rule
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TrafficCaptureRuleLabels(ZscalerObject):
    """
    A class for Traffic Capture Rule Labels objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Traffic Capture Rule Labels model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.org_id = config["orgId"] if "orgId" in config else None

        else:
            self.id = None
            self.name = None
            self.org_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "orgId": self.org_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
