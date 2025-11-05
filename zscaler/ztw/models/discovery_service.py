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


class DiscoveryService(ZscalerObject):
    """
    A class for DiscoveryService objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DiscoveryService model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.trusted_account_id = config["trustedAccountId"] \
                if "trustedAccountId" in config else None
            self.trusted_role_name = config["trustedRoleName"] \
                if "trustedRoleName" in config else None
        else:
            self.trusted_account_id = None
            self.trusted_role_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "trustedAccountId": self.trusted_account_id,
            "trustedRoleName": self.trusted_role_name
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DiscoveryServicePermissions(ZscalerObject):
    """
    A class for DiscoveryServicePermissions objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DiscoveryServicePermissions model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.discovery_role = config["discoveryRole"] \
                if "discoveryRole" in config else None
            self.external_id = config["externalId"] \
                if "externalId" in config else None
        else:
            self.discovery_role = None
            self.external_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "discoveryRole": self.discovery_role,
            "externalId": self.external_id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
