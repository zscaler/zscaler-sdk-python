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


class TenancyRestrictionProfile(ZscalerObject):
    """
    A class for TenancyRestrictionProfile objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TenancyRestrictionProfile model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.app_type = config["appType"] if "appType" in config else None
            self.description = config["description"] if "description" in config else None
            self.item_type_primary = config["itemTypePrimary"] if "itemTypePrimary" in config else None
            self.item_data_primary = ZscalerCollection.form_list(
                config["itemDataPrimary"] if "itemDataPrimary" in config else [], str
            )
            self.item_type_secondary = config["itemTypeSecondary"] if "itemTypeSecondary" in config else None

            self.item_data_secondary = ZscalerCollection.form_list(
                config["itemDataSecondary"] if "itemDataSecondary" in config else [], str
            )
            self.item_value = ZscalerCollection.form_list(config["itemValue"] if "itemValue" in config else [], str)
            self.restrict_personal_o365_domains = (
                config["restrictPersonalO365Domains"] if "restrictPersonalO365Domains" in config else None
            )
            self.allow_google_consumers = config["allowGoogleConsumers"] if "allowGoogleConsumers" in config else None
            self.ms_login_services_tr_v2 = config["msLoginServicesTrV2"] if "msLoginServicesTrV2" in config else None
            self.allow_google_visitors = config["allowGoogleVisitors"] if "allowGoogleVisitors" in config else None
            self.allow_gcp_cloud_storage_read = (
                config["allowGcpCloudStorageRead"] if "allowGcpCloudStorageRead" in config else None
            )
        else:
            self.id = None
            self.name = None
            self.app_type = None
            self.description = None
            self.item_type_primary = None
            self.item_data_primary = []
            self.item_type_secondary = None
            self.item_data_secondary = []
            self.item_value = []
            self.restrict_personal_o365_domains = None
            self.allow_google_consumers = None
            self.ms_login_services_tr_v2 = None
            self.allow_google_visitors = None
            self.allow_gcp_cloud_storage_read = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "appType": self.app_type,
            "description": self.description,
            "itemTypePrimary": self.item_type_primary,
            "itemDataPrimary": self.item_data_primary,
            "itemTypeSecondary": self.item_type_secondary,
            "itemDataSecondary": self.item_data_secondary,
            "itemValue": self.item_value,
            "restrictPersonalO365Domains": self.restrict_personal_o365_domains,
            "allowGoogleConsumers": self.allow_google_consumers,
            "msLoginServicesTrV2": self.ms_login_services_tr_v2,
            "allowGoogleVisitors": self.allow_google_visitors,
            "allowGcpCloudStorageRead": self.allow_gcp_cloud_storage_read,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
