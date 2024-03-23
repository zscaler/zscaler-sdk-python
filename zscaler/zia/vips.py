# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE


from box import Box, BoxList
from zscaler.zia import ZIAClient
from requests import Response
import json
from zscaler.utils import snake_to_camel

class DataCenterVIPSAPI:

    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_public_se(self, cloud: str, continent: str = None) -> Box:
        """
        Returns a list of the Zscaler Public Service Edge information for the specified cloud.

        Args:
            cloud (str): The ZIA cloud that this request applies to.
            continent (str, opt):
                Filter entries by the specified continent. Accepted values are `apac`, `emea` and `amer`.

        Returns:
            :obj:`Box`: The Public Service Edge VIPs

        Examples:
            Print all Public Service Edge information for ``zscaler.net``:

            >>> pprint(zia.vips.list_public_se('zscaler'))

            Print all Public Service Edge information for ``zscalerthree.net`` in ``apac``:

            >>> pprint(zia.vips.list_public_se('zscalerthree',
            ...    continent='apac')

        """

        if continent is not None:
            if continent == "amer":
                # This return is an edge-case to handle the JSON structure for _americas which is in the format
                # continent :_americas. All other continents have whitespace, e.g. continent : emea.
                return self._get(f"https://api.config.zscaler.com/{cloud}.net/cenr/json")[f"{cloud}.net"][
                    "continent :_americas"
                ]

            return self._get(f"https://api.config.zscaler.com/{cloud}.net/cenr/json")[f"{cloud}.net"][
                f"continent : {continent}"
            ]

        return self._get(f"https://api.config.zscaler.com/{cloud}.net/cenr/json")[f"{cloud}.net"]

    def list_ca(self, cloud: str) -> BoxList:
        """
        Returns a list of Zscaler Central Authority server IPs for the specified cloud.

        Args:
            cloud (str):  The ZIA cloud that this request applies to.

        Returns:
            :obj:`BoxList`: A list of CA server IPs.

        Examples:
            Print the IP address of Central Authority servers in `zscalertwo.net`:

            >>> for ip in zia.vips.list_ca('zscalertwo'):
            ...    print(ip)

        """
        return self._get(f"https://api.config.zscaler.com/{cloud}.net/ca/json")["ranges"]

    def list_pac(self, cloud: str) -> BoxList:
        """
        Returns a list of Proxy Auto-configuration (PAC) server IPs for the specified cloud.

        Args:
            cloud (str): The ZIA cloud that this request applies to.

        Returns:
            :obj:`BoxList`: A list of PAC server IPs.

        Examples:
            Print the IP address of PAC servers in `zscloud.net`:

            >>> for ip in zia.vips.list_pac('zscloud'):
            ...    print(ip)

        """
        return self._get(f"https://api.config.zscaler.com/{cloud}.net/pac/json")["ip"]

    def list_vips(self, **kwargs) -> BoxList:
        """
        Returns a list of virtual IP addresses (VIPs) available in the Zscaler cloud.

        Keyword Args:
            **dc (str, optional):
                Filter based on data center.
            **include (str, optional):
                Include all, private, or public VIPs in the list. Available choices are `all`, `private`, `public`.
                Defaults to `public`.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **region (str, optional):
                Filter based on region.

        Returns:
            :obj:`BoxList`: List of VIP resource records.

        Examples:
            List VIPs using default settings:

            >>> for vip in zia.traffic.list_vips():
            ...    pprint(vip)

            List VIPs, limiting to a maximum of 10 items:

            >>> for vip in zia.traffic.list_vips(max_items=10):
            ...    print(vip)

            List VIPs, returning 200 items per page for a maximum of 2 pages:

            >>> for vip in zia.traffic.list_vips(page_size=200, max_pages=2):
            ...    print(vip)

        """
        response = self.rest.get("/vips", **kwargs)
        if isinstance(response, Response):
            return None
        return response

    def list_vips_recommended(self, source_ip: str, **kwargs) -> BoxList:
        """
        Returns a list of recommended virtual IP addresses (VIPs) based on parameters.

        Args:
            source_ip (str):
                The source IP address.
            **kwargs:
                Optional keywords args.

        Keyword Args:
            routable_ip (bool):
                The routable IP address. Default: True.
            within_country_only (bool):
                Search within country only. Default: False.
            include_private_service_edge (bool):
                Include ZIA Private Service Edge VIPs. Default: True.
            include_current_vips (bool):
                Include currently assigned VIPs. Default: True.
            latitude (str):
                Latitude coordinate of GRE tunnel source.
            longitude (str):
                Longitude coordinate of GRE tunnel source.
            geo_override (bool):
                Override the geographic coordinates. Default: False.

        Returns:
            :obj:`BoxList`: List of VIP resource records.

        Examples:
            Return recommended VIPs for a given source IP:

            >>> for vip in zia.traffic.list_vips_recommended(source_ip='203.0.113.30'):
            ...    pprint(vip)

        """
        payload = {"sourceIp": source_ip}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.get("vips/recommendedList", params=payload, **kwargs)
        if isinstance(response, Response):
            return None
        return response

    def get_closest_diverse_vip_ids(self, ip_address: str) -> tuple:
        """
        Returns the closest diverse Zscaler destination VIPs for a given IP address.

        Args:
            ip_address (str):
                The IP address used for locating the closest diverse VIPs.

        Returns:
            :obj:`tuple`: Tuple containing the preferred and secondary VIP IDs.

        Examples:
            >>> closest_vips = zia.traffic.get_closest_diverse_vip_ids('203.0.113.20')

        """
        vips_list = self.list_vips_recommended(source_ip=ip_address)
        preferred_vip = vips_list[0]  # First entry is closest vip

        # Generator to find the next closest vip not in the same city as our preferred
        secondary_vip = next((vip for vip in vips_list if vip.city != preferred_vip.city))
        recommended_vips = (preferred_vip.id, secondary_vip.id)

        return recommended_vips

    def get_closest_diverse_vip_ids(self, ip_address: str) -> tuple:
        """
        Returns the closest diverse Zscaler destination VIPs for a given IP address.

        Args:
            ip_address (str):
                The IP address used for locating the closest diverse VIPs.

        Returns:
            :obj:`tuple`: Tuple containing the preferred and secondary VIP IDs.

        Examples:
            >>> closest_vips = zia.traffic.get_closest_diverse_vip_ids('203.0.113.20')

        """
        vips_list = self.list_vips_recommended(source_ip=ip_address)
        preferred_vip = vips_list[0]  # First entry is closest vip

        # Generator to find the next closest vip not in the same city as our preferred
        secondary_vip = next((vip for vip in vips_list if vip.city != preferred_vip.city))
        recommended_vips = (preferred_vip.id, secondary_vip.id)

        return recommended_vips
    
    def list_vip_group_by_dc(self, source_ip: str, **kwargs) -> BoxList:
        """
        Returns a list of recommended virtual IP addresses (VIPs) based on parameters.

        Args:
            source_ip (str):
                The source IP address.
            **kwargs:
                Optional keywords args.

        Keyword Args:
            routable_ip (bool):
                The routable IP address. Default: True.
            within_country_only (bool):
                Search within country only. Default: False.
            include_private_service_edge (bool):
                Include ZIA Private Service Edge VIPs. Default: True.
            include_current_vips (bool):
                Include currently assigned VIPs. Default: True.
            latitude (str):
                Latitude coordinate of GRE tunnel source.
            longitude (str):
                Longitude coordinate of GRE tunnel source.
            geo_override (bool):
                Override the geographic coordinates. Default: False.

        Returns:
            :obj:`BoxList`: List of VIP resource records.

        Examples:
            Return recommended VIPs for a given source IP:

            >>> for vip in zia.traffic.list_vips_recommended(source_ip='203.0.113.30'):
            ...    pprint(vip)

        """
        payload = {"sourceIp": source_ip}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.get("vips/groupByDatacenter", params=payload, **kwargs)
        if isinstance(response, Response):
            return None
        return response