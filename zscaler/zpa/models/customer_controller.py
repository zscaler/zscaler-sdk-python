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


class AuthDomain(ZscalerObject):

    def __init__(self, config=None):
        """
        Initialize the Auth Domain model based on API response.
        Args:
            config (list): A list representing the authentication domains.
        """
        super().__init__(config)

        if config:
            self.auth_domains = ZscalerCollection.form_list(config["authDomains"] if "authDomains" in config else [], str)

        else:
            self.auth_domains = []

    def request_format(self):
        """
        Formats the Auth Domain data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "authDomains": self.auth_domains,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class RemoteAssistance(ZscalerObject):
    """
    A class for RemoteAssistance objects.
    """

    def __init__(self, config=None):
        """
        Initialize the RemoteAssistance model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.access_type = config["accessType"] \
                if "accessType" in config else None
            self.access_mappings = ZscalerCollection.form_list(
                config["accessMappings"] if "accessMappings" in config else [], AccessMappings
            )
        else:
            self.access_type = None
            self.access_mappings = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "accessType": self.access_type,
            "accessMappings": self.access_mappings
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AccessMappings(ZscalerObject):
    """
    A class for AccessMappings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AccessMappings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.remote_assistance_customer_id = config["remoteAssistanceCustomerId"] \
                if "remoteAssistanceCustomerId" in config else None
            self.role_id = config["roleId"] \
                if "roleId" in config else None
            self.customer_id = config["customerId"] \
                if "customerId" in config else None
        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.remote_assistance_customer_id = None
            self.role_id = None
            self.customer_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "remoteAssistanceCustomerId": self.remote_assistance_customer_id,
            "roleId": self.role_id,
            "customerId": self.customer_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
