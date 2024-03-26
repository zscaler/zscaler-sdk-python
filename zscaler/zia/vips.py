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


            
    def list_region_geo_coordinates(self, latitude: int, longitude: int, **kwargs) -> BoxList:
            """
            Returns a list of recommended virtual IP addresses (VIPs) based on parameters.

            Args:
                latitude (int):
                    The latitude coordinate of the city.
                longitude (int):
                    The longitude coordinate of the city.
                **kwargs:
                    Optional keywords args.

            Keyword Args:
                city_geo_id (int):
                    The geographical ID of the city
                state_geo_id (int):
                    The geographical ID of the state
                city_name (str):
                    The name of the city
                state_name (str):
                    The name of the state, province, or territory of a country
                country_name (str):
                    The name of the country
                country_code (str):
                    The ISO standard two-letter country code.
                postal_code (str):
                    The postal code
                continent_code (str):
                    The ISO standard two-letter continent code

            Returns:
                :obj:`BoxList`: List of geographical data of the region or city that is located.

            Examples:
                Return recommended VIPs for a given source IP:

                >>> for geo in zia.vips.list_region_geo_coordinates(latitude='38.0', longitude='-123.0'):
                ...    pprint(geo)

            """
            params = {"latitude": latitude,
                      "longitude": longitude}

            for key, value in kwargs.items():
                params[snake_to_camel(key)] = value
            response = self.rest.get("/region/byGeoCoordinates", params=params)
            if response is not None:
                return response
            else:
                print("Failed to fetch region by geo coordinates. No response or error received.")
                return BoxList([])