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
from zscaler.zpa.models import trusted_network as trusted_networks
from zscaler.zpa.models import service_edges as service_edges


class ServiceEdgeGroup(ZscalerObject):
    """
    A class representing the Service Edge Group.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.location = config["location"] if "location" in config else None
            self.version_profile_id = config["versionProfileId"] if "versionProfileId" in config else None
            self.version_profile_name = config["versionProfileName"] if "versionProfileName" in config else None
            self.override_version_profile = config["overrideVersionProfile"] if "overrideVersionProfile" in config else None
            self.version_profile_visibility_scope = (
                config["versionProfileVisibilityScope"] if "versionProfileVisibilityScope" in config else None
            )
            self.alt_cloud = config["altCloud"] if "altCloud" in config else None
            self.city_country = config["cityCountry"] if "cityCountry" in config else None
            self.country_code = config["countryCode"] if "countryCode" in config else None
            self.upgrade_day = config["upgradeDay"] if "upgradeDay" in config else None
            self.upgrade_time_in_secs = config["upgradeTimeInSecs"] if "upgradeTimeInSecs" in config else None
            self.is_public = config["isPublic"] if "isPublic" in config else None
            self.geolocation_id = config["geoLocationId"] if "geoLocationId" in config else None
            self.grace_distance_enabled = config["graceDistanceEnabled"] if "graceDistanceEnabled" in config else False
            self.grace_distance_value = config["graceDistanceValue"] if "graceDistanceValue" in config else None
            self.grace_distance_value_unit = config["graceDistanceValueUnit"] if "graceDistanceValueUnit" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.site_id = config["siteId"] if "siteId" in config else None
            self.site_name = config["siteName"] if "siteName" in config else None
            self.upgrade_priority = config["upgradePriority"] if "upgradePriority" in config else None
            self.upgrade_time_in_secs = config["upgradeTimeInSecs"] if "upgradeTimeInSecs" in config else None
            self.use_in_dr_mode = config["useInDrMode"] if "useInDrMode" in config else False
            self.use_in_dr_mode = config["useInDrMode"] if "useInDrMode" in config else False

            self.trusted_networks = ZscalerCollection.form_list(
                config["trustedNetworks"] if "trustedNetworks" in config else [], trusted_networks.TrustedNetwork
            )

            self.service_edges = ZscalerCollection.form_list(
                config["serviceEdges"] if "serviceEdges" in config else [], service_edges.ServiceEdge
            )

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.description = None
            self.enabled = True
            self.latitude = None
            self.longitude = None
            self.location = None
            self.version_profile_id = None
            self.override_version_profile = None
            self.version_profile_name = None
            self.upgrade_priority = None
            self.version_profile_visibility_scope = None
            self.alt_cloud = None
            self.city_country = None
            self.country_code = None
            self.upgrade_day = None
            self.upgrade_priority = None
            self.upgrade_time_in_secs = None
            self.is_public = None
            self.geolocation_id = None
            self.graceDistanceEnabled = False
            self.graceDistanceValue = None
            self.graceDistanceValueUnit = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.site_id = None
            self.site_name = None
            self.use_in_dr_mode = None
            self.trusted_networks = []
            self.service_edges = []

    def request_format(self):
        """
        Formats the Service Edge Group data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location": self.location,
            "versionProfileId": self.version_profile_id,
            "overrideVersionProfile": self.override_version_profile,
            "versionProfileName": self.version_profile_name,
            "upgradePriority": self.upgrade_priority,
            "versionProfileVisibilityScope": self.version_profile_visibility_scope,
            "altCloud": self.alt_cloud,
            "cityCountry": self.city_country,
            "countryCode": self.country_code,
            "upgradeDay": self.upgrade_day,
            "upgradeTimeInSecs": self.upgrade_time_in_secs,
            "isPublic": self.is_public,
            "geoLocationId": self.geolocation_id,
            "graceDistanceEnabled": self.grace_distance_enabled,
            "graceDistanceValue": self.grace_distance_value,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "siteId": self.site_id,
            "siteName": self.site_name,
            "useInDrMode": self.use_in_dr_mode,
            "trustedNetworks": [tn.request_format() for tn in self.trusted_networks],
            "serviceEdges": [se.request_format() for se in self.service_edges],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
