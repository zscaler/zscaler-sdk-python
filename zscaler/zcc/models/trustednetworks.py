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

from zscaler.oneapi_object import ZscalerObject


class TrustedNetworks(ZscalerObject):
    """
    A class for TrustedNetworks objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TrustedNetworks model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.company_id = config["companyId"] if "companyId" in config else None
            self.condition_type = config["conditionType"] if "conditionType" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.dns_search_domains = config["dnsSearchDomains"] if "dnsSearchDomains" in config else None
            self.dns_servers = config["dnsServers"] if "dnsServers" in config else None
            self.edited_by = config["editedBy"] if "editedBy" in config else None
            self.guid = config["guid"] if "guid" in config else None
            self.hostnames = config["hostnames"] if "hostnames" in config else None
            self.id = config["id"] if "id" in config else None
            self.network_name = config["networkName"] if "networkName" in config else None
            self.resolved_ips_for_hostname = config["resolvedIpsForHostname"] if "resolvedIpsForHostname" in config else None
            self.ssids = config["ssids"] if "ssids" in config else None
            self.trusted_dhcp_servers = config["trustedDhcpServers"] if "trustedDhcpServers" in config else None
            self.trusted_egress_ips = config["trustedEgressIps"] if "trustedEgressIps" in config else None
            self.trusted_gateways = config["trustedGateways"] if "trustedGateways" in config else None
            self.trusted_subnets = config["trustedSubnets"] if "trustedSubnets" in config else None
        else:
            self.active = None
            self.company_id = None
            self.condition_type = None
            self.created_by = None
            self.dns_search_domains = None
            self.dns_servers = None
            self.edited_by = None
            self.guid = None
            self.hostnames = None
            self.id = None
            self.network_name = None
            self.resolved_ips_for_hostname = None
            self.ssids = None
            self.trusted_dhcp_servers = None
            self.trusted_egress_ips = None
            self.trusted_gateways = None
            self.trusted_subnets = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "companyId": self.company_id,
            "conditionType": self.condition_type,
            "createdBy": self.created_by,
            "dnsSearchDomains": self.dns_search_domains,
            "dnsServers": self.dns_servers,
            "editedBy": self.edited_by,
            "guid": self.guid,
            "hostnames": self.hostnames,
            "id": self.id,
            "networkName": self.network_name,
            "resolvedIpsForHostname": self.resolved_ips_for_hostname,
            "ssids": self.ssids,
            "trustedDhcpServers": self.trusted_dhcp_servers,
            "trustedEgressIps": self.trusted_egress_ips,
            "trustedGateways": self.trusted_gateways,
            "trustedSubnets": self.trusted_subnets,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
