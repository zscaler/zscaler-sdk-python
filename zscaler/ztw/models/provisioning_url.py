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
from zscaler.ztw.models import location_templates as location_templates
from zscaler.ztw.models import common as common
from zscaler.ztw.models import ecgroup as ecgroup


class ProvisioningURL(ZscalerObject):
    """
    A class for ProvisioningURL objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ProvisioningURL model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.desc = config["desc"] if "desc" in config else None
            self.prov_url = config["provUrl"] if "provUrl" in config else None
            self.prov_url_type = config["provUrlType"] if "provUrlType" in config else None
            self.used_in_ec_groups = ZscalerCollection.form_list(
                config["usedInEcGroups"] if "usedInEcGroups" in config else [], str
            )
            self.status = config["status"] if "status" in config else None
            self.last_mod_time = config["lastModTime"] if "lastModTime" in config else None

            if "provUrlData" in config:
                if isinstance(config["provUrlData"], ProvURLData):
                    self.prov_url_data = config["provUrlData"]
                elif config["provUrlData"] is not None:
                    self.prov_url_data = ProvURLData(config["provUrlData"])
                else:
                    self.prov_url_data = None
            else:
                self.prov_url_data = None

            if "location" in config:
                if isinstance(config["location"], common.CommonIDNameExternalID):
                    self.location = config["location"]
                elif config["location"] is not None:
                    self.location = common.CommonIDNameExternalID(config["location"])
                else:
                    self.location = None
            else:
                self.location = None

            if "lastModUid" in config:
                if isinstance(config["lastModUid"], common.CommonIDNameExternalID):
                    self.last_mod_uid = config["lastModUid"]
                elif config["lastModUid"] is not None:
                    self.last_mod_uid = common.CommonIDNameExternalID(config["lastModUid"])
                else:
                    self.last_mod_uid = None
            else:
                self.last_mod_uid = None

        else:
            self.id = None
            self.name = None
            self.desc = None
            self.prov_url = None
            self.prov_url_type = None
            self.prov_url_data = None
            self.used_in_ec_groups = ZscalerCollection.form_list([], str)
            self.status = None
            self.last_mod_uid = None
            self.last_mod_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "provUrl": self.prov_url,
            "provUrlType": self.prov_url_type,
            "provUrlData": self.prov_url_data,
            "usedInEcGroups": self.used_in_ec_groups,
            "status": self.status,
            "lastModUid": self.last_mod_uid,
            "lastModTime": self.last_mod_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ProvURLData(ZscalerObject):
    """
    A class for ProvURLData objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ProvURLData model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.zs_cloud_domain = config["zsCloudDomain"] if "zsCloudDomain" in config else None
            self.org_id = config["orgId"] if "orgId" in config else None
            self.config_server = config["configServer"] if "configServer" in config else None
            self.registration_server = config["registrationServer"] if "registrationServer" in config else None
            self.api_server = config["apiServer"] if "apiServer" in config else None
            self.pac_server = config["pacServer"] if "pacServer" in config else None
            self.editable = config["editable"] if "editable" in config else None
            self.last_mod_time = config["lastModTime"] if "lastModTime" in config else None
            self.cloud_provider_type = config["cloudProviderType"] if "cloudProviderType" in config else None
            self.form_factor = config["formFactor"] if "formFactor" in config else None
            self.hypervisors = config["hyperVisors"] if "hyperVisors" in config else None

            if "locationTemplate" in config:
                if isinstance(config["locationTemplate"], location_templates.LocationTemplate):
                    self.location_template = config["locationTemplate"]
                elif config["locationTemplate"] is not None:
                    self.location_template = location_templates.LocationTemplate(config["locationTemplate"])
                else:
                    self.location_template = None
            else:
                self.location_template = None

            if "cloudProvider" in config:
                if isinstance(config["cloudProvider"], common.CommonIDNameExternalID):
                    self.cloud_provider = config["cloudProvider"]
                elif config["cloudProvider"] is not None:
                    self.cloud_provider = common.CommonIDNameExternalID(config["cloudProvider"])
                else:
                    self.cloud_provider = None
            else:
                self.cloud_provider = None

            if "lastModUid" in config:
                if isinstance(config["lastModUid"], common.CommonIDNameExternalID):
                    self.last_mod_uid = config["lastModUid"]
                elif config["lastModUid"] is not None:
                    self.last_mod_uid = common.CommonIDNameExternalID(config["lastModUid"])
                else:
                    self.last_mod_uid = None
            else:
                self.last_mod_uid = None

            if "location" in config:
                if isinstance(config["location"], common.CommonIDNameExternalID):
                    self.location = config["location"]
                elif config["location"] is not None:
                    self.location = common.CommonIDNameExternalID(config["location"])
                else:
                    self.location = None
            else:
                self.location = None

            if "bcGroup" in config:
                if isinstance(config["bcGroup"], ecgroup.ECGroup):
                    self.bc_group = config["bcGroup"]
                elif config["bcGroup"] is not None:
                    self.bc_group = ecgroup.ECGroup(config["bcGroup"])
                else:
                    self.bc_group = None
            else:
                self.bc_group = None

        else:
            self.zs_cloud_domain = None
            self.org_id = None
            self.config_server = None
            self.registration_server = None
            self.api_server = None
            self.pac_server = None
            self.editable = None
            self.last_mod_time = None
            self.cloud_provider_type = None
            self.form_factor = None
            self.hypervisors = None
            self.location = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "zsCloudDomain": self.zs_cloud_domain,
            "orgId": self.org_id,
            "configServer": self.config_server,
            "registrationServer": self.registration_server,
            "apiServer": self.api_server,
            "pacServer": self.pac_server,
            "editable": self.editable,
            "lastModTime": self.last_mod_time,
            "cloudProviderType": self.cloud_provider_type,
            "formFactor": self.form_factor,
            "hyperVisors": self.hypervisors,
            "location": self.location,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
