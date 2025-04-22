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
from zscaler.zia.models import gre_tunnels as gre_tunnels


class TrafficVips(ZscalerObject):
    """
    A class for TrafficVips objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TrafficVips model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.cloud_name = config["cloudName"] if "cloudName" in config else None
            self.region = config["region"] if "region" in config else None
            self.country = config["country"] if "country" in config else None
            self.city = config["city"] if "city" in config else None
            self.data_center = config["dataCenter"] if "dataCenter" in config else None
            self.location = config["location"] if "location" in config else None

            self.vpn_ips = ZscalerCollection.form_list(config["vpnIps"] if "vpnIps" in config else [], str)
            self.vpn_domain_name = config["vpnDomainName"] if "vpnDomainName" in config else None
            self.gre_ips = ZscalerCollection.form_list(config["greIps"] if "greIps" in config else [], str)
            self.gre_domain_name = config["greDomainName"] if "greDomainName" in config else None

            self.pac_ips = ZscalerCollection.form_list(config["pacIps"] if "pacIps" in config else [], str)
            self.pac_domain_name = config["pacDomainName"] if "pacDomainName" in config else None

            self.svpn_ips = ZscalerCollection.form_list(config["svpnIps"] if "svpnIps" in config else [], str)
            self.svpn_domain_name = config["svpnDomainName"] if "svpnDomainName" in config else None
        else:
            self.cloud_name = None
            self.region = None
            self.country = None
            self.city = None
            self.data_center = None
            self.location = None
            self.vpn_ips = ZscalerCollection.form_list([], str)
            self.vpn_domain_name = None
            self.gre_ips = ZscalerCollection.form_list([], str)
            self.gre_domain_name = None
            self.pac_ips = ZscalerCollection.form_list([], str)
            self.pac_domain_name = None
            self.svpn_ips = ZscalerCollection.form_list([], str)
            self.svpn_domain_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "cloudName": self.cloud_name,
            "region": self.region,
            "country": self.country,
            "city": self.city,
            "dataCenter": self.data_center,
            "location": self.location,
            "vpnIps": self.vpn_ips,
            "vpnDomainName": self.vpn_domain_name,
            "greIps": self.gre_ips,
            "greDomainName": self.gre_domain_name,
            "pacIps": self.pac_ips,
            "pacDomainName": self.pac_domain_name,
            "svpnIps": self.svpn_ips,
            "svpnDomainName": self.svpn_domain_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GroupByDatacenter(ZscalerObject):
    """
    A class for GroupByDatacenter objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the GroupByDatacenter model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            if "datacenter" in config:
                if isinstance(config["datacenter"], DataCenter):
                    self.datacenter = config["datacenter"]
                elif config["datacenter"] is not None:
                    self.datacenter = DataCenter(config["datacenter"])
                else:
                    self.datacenter = None

            self.gre_vips = ZscalerCollection.form_list(
                config["greVips"] if "greVips" in config else [], gre_tunnels.GreVirtualIP
            )

        else:
            self.datacenter = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "datacenter": self.datacenter,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DataCenter(ZscalerObject):
    """
    A class for DataCenter objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the DataCenter model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.datacenter = config["datacenter"] if "datacenter" in config else None

        else:
            self.datacenter = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "datacenter": self.datacenter,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
