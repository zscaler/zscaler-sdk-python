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

from zscaler.zpa.client import ZPAClient


class IDPControllerAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_idps(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured IdPs.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **scim_enabled (bool):
                Returns all SCIM IdPs if ``True``. Returns all non-SCIM IdPs if ``False``.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured IdPs.

        Examples:
            >>> for idp in zpa.idp.list_idps():
            ...    pprint(idp)

        """
        list, _ = self.rest.get_paginated_data(path="/idp", **kwargs, api_version="v2")
        return list

    def get_idp_by_name(self, name):
        idps = self.list_idps()
        for idp in idps:
            if idp.get("name") == name:
                return idp
        return None

    def get_idp(self, idp_id: str) -> Box:
        """
        Returns information on the specified IdP.

        Args:
            idp_id (str):
                The unique identifier for the IdP.

        Returns:
            :obj:`Box`: The resource record for the IdP.

        Examples:
            >>> pprint(zpa.idp.get_idp('99999'))

        """

        response = self.rest.get("/idp/%s" % (idp_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response
