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


class TenantSubClouds(ZscalerObject):
    """
    A class for TenantSubClouds objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TenantSubClouds model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None

            self.dcs = ZscalerCollection.form_list(config["dcs"] if "dcs" in config else [], DCs)
            self.exclusions = ZscalerCollection.form_list(config["exclusions"] if "exclusions" in config else [], Exclusions)
        else:
            self.id = None
            self.name = None
            self.dcs = []
            self.exclusions = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"id": self.id, "name": self.name, "dcs": self.dcs, "exclusions": self.exclusions}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DCs(ZscalerObject):
    """
    A class for DCs objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DCs model based on API response.

        Args:
            config (dict): A dictionary representing the DCs configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.country = config["country"] if "country" in config else None

        else:
            self.id = None
            self.name = None
            self.country = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "country": self.country,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Exclusions(ZscalerObject):
    """
    A class for Exclusions objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Exclusions model based on API response.

        Args:
            config (dict): A dictionary representing the Exclusions configuration.
        """
        super().__init__(config)

        if config:
            self.country = config["country"] if "country" in config else None

            self.expired = config["expired"] if "expired" in config else False

            self.disabled_by_ops = config["disabledByOps"] if "disabledByOps" in config else False

            self.create_time = config["createTime"] if "createTime" in config else None

            self.start_time = config["startTime"] if "startTime" in config else None

            self.end_time = config["endTime"] if "endTime" in config else None

            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None

            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None

            if "datacenter" in config:
                if isinstance(config["datacenter"], Datacenter):
                    self.datacenter = config["datacenter"]
                elif config["datacenter"] is not None:
                    self.datacenter = Datacenter(config["datacenter"])
                else:
                    self.datacenter = None
            else:
                self.datacenter = None

            if "lastModifiedUser" in config:
                if isinstance(config["lastModifiedUser"], LastModifiedUser):
                    self.last_modified_user = config["lastModifiedUser"]
                elif config["lastModifiedUser"] is not None:
                    self.last_modified_user = LastModifiedUser(config["lastModifiedUser"])
                else:
                    self.last_modified_user = None
            else:
                self.last_modified_user = None

        else:
            self.country = None
            self.expired = None
            self.disabled_by_ops = None
            self.create_time = None
            self.start_time = None
            self.end_time = None
            self.last_modified_user = None
            self.last_modified_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "country": self.country,
            "expired": self.expired,
            "disabledByOps": self.disabled_by_ops,
            "createTime": self.create_time,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "lastModifiedUser": self.last_modified_user,
            "lastModifiedTime": self.last_modified_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Datacenter(ZscalerObject):
    """
    A class for Datacenter objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Datacenter model based on API response.

        Args:
            config (dict): A dictionary representing the Datacenter configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.external_id = config["externalId"] if "externalId" in config else None
            self.extensions = config if isinstance(config, dict) else {}

        else:
            self.id = None
            self.name = None
            self.external_id = None
            self.extensions = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "externalId": self.external_id,
            "extensions": self.extensions,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LastModifiedUser(ZscalerObject):
    """
    A class for LastModifiedUser objects.
    """

    def __init__(self, config=None):
        """
        Initialize the LastModifiedUser model based on API response.

        Args:
            config (dict): A dictionary representing the Last Modified User configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.external_id = config["externalId"] if "externalId" in config else None
            self.triggers = config if isinstance(config, dict) else {}

        else:
            self.id = None
            self.name = None
            self.external_id = None
            self.extensions = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"id": self.id, "name": self.name, "externalId": self.external_id, "extensions": self.extensions}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LastDCInCountry(ZscalerObject):
    """
    A class for LastDCInCountry objects.
    """

    def __init__(self, config=None):
        """
        Initialize the LastDCInCountry model based on API response.

        Args:
            config (dict): A dictionary representing the LastDCInCountry configuration.
        """
        super().__init__(config)

        if config:
            self.country = config["country"] if "country" in config else None
            self.last_dc_exclusion = config["lastDCExclusion"] if "lastDCExclusion" in config else None
            self.dc_ids = ZscalerCollection.form_list(config["dcIds"] if "dcIds" in config else [], str)
        else:
            self.country = None
            self.last_dc_exclusion = None
            self.dc_ids = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "country": self.country,
            "dcIds": self.dc_ids,
            "lastDCExclusion": self.last_dc_exclusion,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
