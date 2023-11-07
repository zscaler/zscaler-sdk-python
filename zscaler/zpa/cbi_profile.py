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
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from box import Box, BoxList
from requests import Response
from zscaler.utils import snake_to_camel
from zscaler.zpa.client import ZPAClient

class CBIProfileAPIControllerAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_all_regions(self, **kwargs) -> BoxList:
        """
        Returns a list of all available cloud browser isolation regions.

        Keyword Args:
            **id (str):
                The unique identifier of the Cloud Browser Isolation region.
            **name (str):
                The name of the Cloud Browser Isolation region.

        Returns:
            :obj:`list`: A list of all available cloud browser isolation regions.

        Examples:
            >>> for region in zpa.cbi_profile.get_regions():
            ...    pprint(region)

        """
        return self.rest.get(path="/regions", **kwargs, api_version="cbiconfig_v1")

    def get_server(self, server_id: str) -> Box:
        """
        Gets information on the specified server.

        Args:
            server_id (str):
                The unique identifier for the server.

        Returns:
            :obj:`Box`: The resource record for the server.

        Examples:
            >>> server = zpa.servers.get_server('99999')

        """
        response = self.rest.get("/server/%s" % (server_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response
    def get_regions_by_name(self, name):
        regions = self.list_all_regions()
        for region in regions:
            if region.get("name") == name:
                return region
        return None

    def list_zpa_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all available Cloud Browser Isolation ZPA profiles.

        Keyword Args:
            **id (str):
                The unique identifier of the Cloud Browser Isolation ZPA profiles.
            **name (str):
                The name of the Cloud Browser Isolation ZPA profiles.

        Returns:
            :obj:`list`: A list of all available cloud browser isolation ZPA profiles.

        Examples:
            >>> for region in zpa.cbi_profile.get_zpa_profiles():
            ...    pprint(region)

        """
        return self.rest.get(path="/zpaprofiles", **kwargs, api_version="cbiconfig_v1")

    def get_zpa_profile_by_name(self, name):
        profiles = self.list_zpa_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                return profile
        return None

    def list_all_cbi_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all available Cloud Browser Isolation ZPA profiles.

        Keyword Args:
            **id (str):
                The unique identifier of the Cloud Browser Isolation ZPA profiles.
            **name (str):
                The name of the Cloud Browser Isolation ZPA profiles.

        Returns:
            :obj:`list`: A list of all available cloud browser isolation ZPA profiles.

        Examples:
            >>> for region in zpa.cbi_profile.get_zpa_profiles():
            ...    pprint(region)

        """
        return self.rest.get(path="/profiles", **kwargs, api_version="cbiconfig_v1")

    def get_cbi_profile_by_name(self, name):
        profiles = self.list_all_cbi_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                return profile
        return None

    def add_cbi_profile(self, name: str, regions: list, **kwargs) -> Box:
        """
        Add a new application server.

        Args:
            name (str):
                The name of the server.
            regions (list):
                The IP address of the server.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            description (str):
                A description for the server.
            config_space (str):
                The configuration space for the server. Defaults to DEFAULT.

        Returns:
            :obj:`Box`: The resource record for the newly created server.

        Examples:
            Create a server with the minimum required parameters:

            >>> zpa.servers.add_server(
            ...   name='myserver.example',
            ...   address='192.0.2.10',
            ...   enabled=True)

        """
        payload = {"name": name, "regions": regions}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("/profiles", json=payload)
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                return None
        return self.get(response.get("id"))