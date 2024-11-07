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
import time
from zscaler.zpa.client import ZPAClient


class SCIMGroupsAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_groups(self, idp_id: str, **kwargs) -> BoxList:
        """
        Returns a list of all configured SCIM groups for the specified IdP.

        Args:
            idp_id (str):
                The unique id of the IdP.
            sort_by (str):
                The field name to sort by, supported values: id, name, creationTime or modifiedTime (default to name)
            sort_order (str):
                The sort order, values: ASC or DSC (default DSC)


        Keyword Args:
            **end_time (str):
                The end of a time range for requesting last updated data (modified_time) for the SCIM group.
                This requires setting the ``start_time`` parameter as well.
            **idp_group_id (str):
                The unique id of the IdP group.
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **scim_user_id (str):
                The unique id for the SCIM user.
            **search (str, optional):
                The search string used to match against features and fields.
            **sort_order (str):
                Sort the last updated time (modified_time) by ascending ``ASC`` or descending ``DSC`` order. Defaults to
                ``DSC``.
            **start_time (str):
                The start of a time range for requesting last updated data (modified_time) for the SCIM group.
                This requires setting the ``end_time`` parameter as well.

        Returns:
            :obj:`list`: A list of all configured SCIM groups.

        Examples:
            >>> for scim_group in zpa.scim_groups.list_groups("999999"):
            ...    pprint(scim_group)

        """
        list, _ = self.rest.get_paginated_data(
            path=f"/scimgroup/idpId/{idp_id}",
            **kwargs,
            api_version="userconfig_v1",
        )
        return list

    def get_group(self, group_id: str, **kwargs) -> Box:
        """
        Returns information on the specified SCIM group.

        Args:
            group_id (str):
                The unique identifier for the SCIM group.
            **kwargs:
                Optional keyword args.

        Returns:
            :obj:`dict`: The resource record for the SCIM group.

        Examples:
            >>> pprint(zpa.scim_groups.get_group('99999'))

        """
        response = self.rest.get(f"/scimgroup/{group_id}", **kwargs, api_version="userconfig_v1")
        return response
