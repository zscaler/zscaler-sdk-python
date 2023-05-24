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
from restfly import APISession
from restfly.endpoint import APIEndpoint

from zscaler.utils import Iterator


class IDPControllerAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.v2_url = api.v2_url

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
        return BoxList(Iterator(self._api, f"{self.v2_url}/idp", **kwargs))

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

        return self._get(f"idp/{idp_id}")
