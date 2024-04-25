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


from typing import Union

from box import Box, BoxList
from requests import Response

from zscaler.zpa.client import ZPAClient


class TrustedNetworksAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_networks(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured trusted networks.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured trusted networks.

        Examples:
            >>> for trusted_network in zpa.trusted_networks.list_networks():
            ...    pprint(trusted_network)

        """
        list, _ = self.rest.get_paginated_data(path="/network", **kwargs, api_version="v2")
        return list

    def get_network_by_name(self, name):
        networks = self.list_networks()
        for network in networks:
            if network.get("name") == name:
                return network
        return None

    def get_network(self, network_id: str) -> Box:
        """
        Returns information on the specified trusted network.

        Args:
            network_id (str):
                The unique identifier for the trusted network.

        Returns:
            :obj:`Box`: The resource record for the trusted network.

        Examples:
            >>> pprint(zpa.trusted_networks.get_network('99999'))

        """
        response = self.rest.get("/network/%s" % (network_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def get_by_network_id(self, network_id: str, **kwargs) -> Union[Box, None]:
        """
        Returns the trusted network based on the networkId.

        Args:
            network_id (str): The unique Network ID for the network ID.

        Keyword Args:
            **max_items (int): The maximum number of items to request before stopping iteration.
            **max_pages (int): The maximum number of pages to request before stopping iteration.
            **pagesize (int): Specifies the page size. The default size is 100, but the maximum size is 500.
            **search (str, optional): The search string used to match against features and fields.

        Returns:
            Union[Box, None]: The resource record for the trusted networks.
        """

        page = 0
        page_size = kwargs.get("pagesize", 100)  # default page size changed to 100
        max_pages = kwargs.get("max_pages", None)

        while True:
            params = {
                "pagesize": page_size,
                "page": page,
                "search": network_id,  # use the search parameter if supported
                **kwargs,
            }
            networks = self.list_networks(**params)

            if not networks:
                break  # exit if no more networks

            for network in networks:
                if network.get("networkId") == network_id:
                    return Box(network)

            page += 1
            if max_pages and page >= max_pages:
                break

        return None
