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
from restfly.endpoint import APIEndpoint


class LocationGroupsAPI(APIEndpoint):
    def list_groups(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA DLP ICAP Server.

        Args:
            query (str): A search string used to match against a DLP ICAP Server's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP ICAP Server.

        Examples:
            Print all icap servers

            >>> for dlp icap in zia.dlp_icap_server.list_icaps():
            ...    pprint(icap)

            Print ICAP Server that match the name or description 'ZS_ICAP_01'

            >>> pprint(zia.dlp_icap_server.list_icaps('ZS_ICAP_01'))

        """
        payload = {"search": query}
        return self._get("icapServers", params=payload)

    def get_group(self, server_id: str) -> Box:
        """
        Returns the dlp icap server details for a given DLP ICAP Server.

        Args:
            server_id (str): The unique identifier for the DLP ICAP Server.

        Returns:
            :obj:`Box`: The DLP ICAP Server. resource record.

        Examples:
            >>> icap = zia.dlp_icap_server.get_icap('99999')

        """
        return self._get(f"icapServers/{server_id}")
