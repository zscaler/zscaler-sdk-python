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
from zscaler.zidentity.models import common


class ResourceServers(ZscalerObject):
    """
    A class for Resource Servers objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Resource Servers model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.results_total = config["results_total"] \
                if "results_total" in config else None
            self.page_offset = config["pageOffset"] \
                if "pageOffset" in config else None
            self.page_size = config["pageSize"] \
                if "pageSize" in config else None
            self.next_link = config["next_link"] \
                if "next_link" in config else None
            self.prev_link = config["prev_link"] \
                if "prev_link" in config else None
            self.records = ZscalerCollection.form_list(
                config["records"] if "records" in config else [], ResourceServersRecord
            )
        else:
            self.results_total = None
            self.page_offset = None
            self.page_size = None
            self.next_link = None
            self.prev_link = None
            self.records = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "results_total": self.results_total,
            "pageOffset": self.page_offset,
            "pageSize": self.page_size,
            "next_link": self.next_link,
            "prev_link": self.prev_link,
            "records": self.records
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ResourceServersRecord(ZscalerObject):
    """
    A class for Resource Servers Record objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Resource Servers Record model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.display_name = config["displayName"] \
                if "displayName" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.primary_aud = config["primaryAud"] \
                if "primaryAud" in config else None
            self.default_api = config["defaultApi"] \
                if "defaultApi" in config else None
            self.service_scopes = ZscalerCollection.form_list(
                config["serviceScopes"] if "serviceScopes" in config else [], ServiceScopes
            )
        else:
            self.id = None
            self.name = None
            self.display_name = None
            self.description = None
            self.primary_aud = None
            self.default_api = None
            self.service_scopes = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "primaryAud": self.primary_aud,
            "defaultApi": self.default_api,
            "serviceScopes": self.service_scopes
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ServiceScopes(ZscalerObject):
    """
    A class for Service Scopes Record objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Service Scopes Record model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.scopes = ZscalerCollection.form_list(
                config["scopes"] if "scopes" in config else [], common.CommonIDName
            )
            if "service" in config:
                if isinstance(config["service"], Service):
                    self.service = config["service"]
                elif config["service"] is not None:
                    self.service = Service(config["service"])
                else:
                    self.service = None
            else:
                self.service = None
        else:
            self.service = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "service": self.service,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Service(ZscalerObject):
    """
    A class for Service objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Service model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.display_name = config["displayName"] \
                if "displayName" in config else None
            self.cloud_name = config["cloudName"] \
                if "cloudName" in config else None
            self.org_name = config["orgName"] \
                if "orgName" in config else None
        else:
            self.id = None
            self.name = None
            self.display_name = None
            self.cloud_name = None
            self.org_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "displayName": self.display_name,
            "cloudName": self.cloud_name,
            "orgName": self.org_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
