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


class DLPIDMProfileAPI(APIEndpoint):
    def list_profiles(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA DLP IDM Profiles.

        Args:
            query (str): A search string used to match against a DLP IDM Profile's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP IDM Profiles.

        Examples:
            Print all idm profiles

            >>> for dlp idm in zia.dlp_idm_profile.list_profiles():
            ...    pprint(idm)

            Print IDM profiles that match the name or description 'IDM_PROFILE_TEMPLATE'

            >>> pprint(zia.dlp_idm_profile.list_profiles('IDM_PROFILE_TEMPLATE'))

        """
        payload = {"search": query}
        return self._get("idmprofile", params=payload)

    def get_profile(self, profile_id: str) -> Box:
        """
        Returns the dlp idm profile details for a given DLP IDM Profile.

        Args:
            icap_server_id (str): The unique identifier for the DLP IDM Profile.

        Returns:
            :obj:`Box`: The DLP IDM Profile resource record.

        Examples:
            >>> idm = zia.dlp.get_dlp_idm_profiles('99999')

        """
        return self._get(f"idmprofile/{profile_id}")
