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


class Entitlement(ZscalerObject):
    """
    A class for Entitlement objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Entitlement model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.roles = ZscalerCollection.form_list(
                config["roles"] if "roles" in config else [], common.CommonIDNameDisplayName
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

            if "scope" in config:
                if isinstance(config["scope"], common.CommonIDNameDisplayName):
                    self.scope = config["scope"]
                elif config["scope"] is not None:
                    self.scope = common.CommonIDNameDisplayName(config["scope"])
                else:
                    self.scope = None
            else:
                self.scope = None

        else:
            self.roles = []
            self.scope = None
            self.service = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "roles": self.roles,
            "scope": self.scope,
            "service": self.service
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
            self.service_name = config["serviceName"] \
                if "serviceName" in config else None
            self.cloud_name = config["cloudName"] \
                if "cloudName" in config else None
            self.cloud_domain_name = config["cloudDomainName"] \
                if "cloudDomainName" in config else None
            self.org_name = config["orgName"] \
                if "orgName" in config else None
            self.org_id = config["orgId"] \
                if "orgId" in config else None
        else:
            self.id = None
            self.service_name = None
            self.cloud_name = None
            self.cloud_domain_name = None
            self.org_name = None
            self.org_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "serviceName": self.service_name,
            "cloudName": self.cloud_name,
            "cloudDomainName": self.cloud_domain_name,
            "orgName": self.org_name,
            "orgId": self.org_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Entitlements(ZscalerObject):
    """
    A class for Entitlements collection objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Entitlements collection model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.entitlements = ZscalerCollection.form_list(
                config if isinstance(config, list) else [], Entitlement
            )
        else:
            self.entitlements = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "entitlements": self.entitlements
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
