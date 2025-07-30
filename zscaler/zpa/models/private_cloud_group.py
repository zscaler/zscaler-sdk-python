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


class PrivateCloudGroup(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the PrivateCloudGroup model based on API response.

        Args:
            config (dict): A dictionary representing the Private Cloud Group configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.name = config["name"] if "name" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.description = config["description"] if "description" in config else None
            self.version_profile_id = config["versionProfileId"] if "versionProfileId" in config else None
            self.override_version_profile = config["overrideVersionProfile"] if "overrideVersionProfile" in config else None
            self.upgrade_time_in_secs = config["upgradeTimeInSecs"] if "upgradeTimeInSecs" in config else None
            self.upgrade_day = config["upgradeDay"] if "upgradeDay" in config else None
            self.location = config["location"] if "location" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.city_country = config["cityCountry"] if "cityCountry" in config else None
            self.country_code = config["countryCode"] if "countryCode" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.site_id = config["siteId"] if "siteId" in config else None
            self.site_name = config["siteName"] if "siteName" in config else None
            self.read_only = config["readOnly"] if "readOnly" in config else None
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else None

            self.site = ZscalerCollection.form_list(
                config["site"] if "site" in config else [], PrivateCloudGroupSite
            )

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.enabled = None
            self.description = None
            self.version_profile_id = None
            self.override_version_profile = None
            self.upgrade_time_in_secs = None
            self.upgrade_day = None
            self.location = None
            self.latitude = None
            self.longitude = None
            self.city_country = None
            self.country_code = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.site_id = None
            self.site_name = None
            self.read_only = None
            self.restriction_type = None
            self.zscaler_managed = None
            self.site = []

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
            "versionProfileId": self.version_profile_id,
            "overrideVersionProfile": self.override_version_profile,
            "upgradeTimeInSecs": self.upgrade_time_in_secs,
            "upgradeDay": self.upgrade_day,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "cityCountry": self.city_country,
            "countryCode": self.country_code,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "siteId": self.site_id,
            "siteName": self.site_name,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "zscalerManaged": self.zscaler_managed,
            "site": self.site,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PrivateCloudGroupSite(ZscalerObject):
    """
    A class for PrivateCloudGroupSite objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PrivateCloudGroupSite model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.re_enroll_period = config["reEnrollPeriod"] \
                if "reEnrollPeriod" in config else None
            self.fire_drill_enabled = config["fireDrillEnabled"] \
                if "fireDrillEnabled" in config else None
            self.sitec_preferred = config["sitecPreferred"] \
                if "sitecPreferred" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.read_only = config["readOnly"] \
                if "readOnly" in config else None
            self.restricted_entity = config["restrictedEntity"] \
                if "restrictedEntity" in config else None
            self.zscaler_managed = config["zscalerManaged"] \
                if "zscalerManaged" in config else None

            self.private_broker_group_ids = ZscalerCollection.form_list(
                config["privateBrokerGroupIds"] if "privateBrokerGroupIds" in config else [], PrivateBrokerGroupID
            )

        else:
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.id = None
            self.name = None
            self.description = None
            self.re_enroll_period = None
            self.fire_drill_enabled = None
            self.sitec_preferred = None
            self.enabled = None
            self.read_only = None
            self.restricted_entity = None
            self.zscaler_managed = None
            self.private_broker_group_ids = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "reEnrollPeriod": self.re_enroll_period,
            "privateBrokerGroupIds": self.private_broker_group_ids,
            "fireDrillEnabled": self.fire_drill_enabled,
            "sitecPreferred": self.sitec_preferred,
            "enabled": self.enabled,
            "readOnly": self.read_only,
            "restrictedEntity": self.restricted_entity,
            "zscalerManaged": self.zscaler_managed
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PrivateBrokerGroupID(ZscalerObject):
    """
    A class for PrivateBrokerGroupID objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PrivateBrokerGroupID model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
        else:
            self.id = None
            self.name = None
            self.enabled = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
