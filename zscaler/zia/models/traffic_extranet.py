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

# AUTO-GENERATED! DO NOT EDIT FILE DIRECTLY
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class TrafficExtranet(ZscalerObject):
    """
    A class for TrafficExtranet objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TrafficExtranet model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None

            self.extranet_dns_list = ZscalerCollection.form_list(
                config["extranetDNSList"] if "extranetDNSList" in config else [], ExtranetDNSList
            )

            self.extranet_ip_pool_list = ZscalerCollection.form_list(
                config["extranetIpPoolList"] if "extranetIpPoolList" in config else [], ExtranetIPPoolList
            )

            self.created_at = config["createdAt"] if "createdAt" in config else None
            self.modified_at = config["modifiedAt"] if "modifiedAt" in config else None
        else:
            self.id = None
            self.name = None
            self.description = None
            self.extranet_dns_list = []
            self.extranet_ip_pool_list = []
            self.created_at = None
            self.modified_at = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "extranetDNSList": [
                dns_list.as_dict() if isinstance(dns_list, ZscalerObject) else dns_list for dns_list in self.extranet_dns_list
            ],
            "extranetIpPoolList": [
                pool_list.as_dict() if isinstance(pool_list, ZscalerObject) else pool_list
                for pool_list in self.extranet_ip_pool_list
            ],
            "createdAt": self.created_at,
            "modifiedAt": self.modified_at,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ExtranetDNSList(ZscalerObject):
    """
    A class for ExtranetDNSList objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ExtranetDNSList model based on API response.

        Args:
            config (dict): A dictionary representing the ExtranetDNSList configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.primary_dns_server = config["primaryDNSServer"] if "primaryDNSServer" in config else None
            self.secondary_dns_server = config["secondaryDNSServer"] if "secondaryDNSServer" in config else None
            self.use_as_default = config["useAsDefault"] if "useAsDefault" in config else False
        else:
            self.id = None
            self.name = None
            self.primary_dns_server = None
            self.secondary_dns_server = None
            self.use_as_default = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "primaryDNSServer": self.primary_dns_server,
            "secondaryDNSServer": self.secondary_dns_server,
            "useAsDefault": self.use_as_default,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ExtranetIPPoolList(ZscalerObject):
    """
    A class for ExtranetIPPoolList objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ExtranetIPPoolList model based on API response.

        Args:
            config (dict): A dictionary representing the ExtranetIPPoolList configuration.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.ip_start = config["ipStart"] if "ipStart" in config else None
            self.ip_end = config["ipEnd"] if "ipEnd" in config else None
            self.use_as_default = config["useAsDefault"] if "useAsDefault" in config else False
        else:
            self.id = None
            self.name = None
            self.ip_start = None
            self.ip_end = None
            self.use_as_default = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "ipStart": self.ip_start,
            "ipEnd": self.ip_end,
            "useAsDefault": self.use_as_default,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
