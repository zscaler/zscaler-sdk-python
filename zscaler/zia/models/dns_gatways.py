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
from zscaler.zia.models import common


class DNSGateways(ZscalerObject):
    """
    A class for DNSGateways objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DNSGateways model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None

            self.name = config["name"] if "name" in config else None

            self.dns_gateway_type = config["dnsGatewayType"] if "dnsGatewayType" in config else None

            self.nat_ztr_gateway = config["natZtrGateway"] if "natZtrGateway" in config else False

            self.primary_ip_or_fqdn = config["primaryIpOrFqdn"] if "primaryIpOrFqdn" in config else None

            self.primary_ports = ZscalerCollection.form_list(config.get("primaryPorts", []), str)

            self.secondary_ip_or_fqdn = config["secondaryIpOrFqdn"] if "secondaryIpOrFqdn" in config else None

            self.secondary_ports = ZscalerCollection.form_list(config.get("secondaryPorts", []), str)

            self.failure_behavior = config["failureBehavior"] if "failureBehavior" in config else None

            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None

            self.auto_created = config["autoCreated"] if "autoCreated" in config else False

            self.protocols = ZscalerCollection.form_list(config.get("protocols", []), str)

            # Handle nested CommonBlocks for last_modified_by
            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None
        else:
            # Initialize all attributes to None or defaults
            self.id = None
            self.name = None
            self.dns_gateway_type = None
            self.primary_ip_or_fqdn = None
            self.primary_ports = []
            self.secondary_ip_or_fqdn = None
            self.secondary_ports = []
            self.failure_behavior = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.auto_created = None
            self.protocols = []
            self.nat_ztr_gateway = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "dnsGatewayType": self.dns_gateway_type,
            "primaryIpOrFqdn": self.primary_ip_or_fqdn,
            "primaryPorts": self.primary_ports,
            "secondaryIpOrFqdn": self.secondary_ip_or_fqdn,
            "secondaryPorts": self.secondary_ports,
            "failureBehavior": self.failure_behavior,
            "autoCreated": self.auto_created,
            "protocols": self.protocols,
            "natZtrGateway": self.nat_ztr_gateway,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
