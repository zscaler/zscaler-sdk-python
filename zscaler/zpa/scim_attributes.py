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

from zscaler.zpa.client import ZPAClient


class ScimAttributeHeaderAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_attributes_by_idp(self, idp_id: str, **kwargs) -> BoxList:
        """
        Returns a list of all configured SCIM attributes for the specified IdP.

        Args:
            idp_id (str): The unique id of the IdP to retrieve SCIM attributes for.
            **kwargs: Optional keyword args.

        Keyword Args:
            max_items (int):
                The maximum number of items to request before stopping iteration.
            max_pages (int):
                The maximum number of pages to request before stopping iteration.
            pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured SCIM attributes for the specified IdP.

        Examples:
            >>> for scim_attribute in zpa.scim_attributes.list_attributes_by_idp('99999'):
            ...    pprint(scim_attribute)

        """
        list, _ = self.rest.get_paginated_data(
            path=f"/idp/{idp_id}/scimattribute",
            **kwargs,
            api_version="v1",
        )
        return list

    def get_attribute(self, idp_id: str, attribute_id: str) -> Box:
        """
        Returns information on the specified SCIM attribute.

        Args:
            idp_id (str):
                The unique id of the Idp corresponding to the SCIM attribute.
            attribute_id (str):
                The unique id of the SCIM attribute.

        Returns:
            :obj:`Box`: The resource record for the SCIM attribute.

        Examples:
            >>> pprint(zpa.scim_attributes.get_attribute('99999',
            ...    scim_attribute_id="88888"))

        """
        response = self.rest.get(f"/idp/{idp_id}/scimattribute/{attribute_id}", api_version="v1")
        return response

    def get_values(self, idp_id: str, attribute_id: str, **kwargs) -> BoxList:
        """
        Returns information on the specified SCIM attributes.

        Args:
            idp_id (str):
                The unique identifier for the IDP.
            attribute_id (str):
                The unique identifier for the attribute.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            max_items (int):
                The maximum number of items to request before stopping iteration.
            max_pages (int):
                The maximum number of pages to request before stopping iteration.
            pagesize (int):
                Specifies the page size. Default is 20, maximum is 500.
            search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: The resource record for the SCIM attribute values.

        Examples:
            >>> pprint(zpa.scim_attributes.get_values('99999', '88888'))

        """
        list, _ = self.rest.get_paginated_data(
            path=f"/scimattribute/idpId/{idp_id}/attributeId/{attribute_id}",
            **kwargs,
            api_version="userconfig_v1",
        )
        return list
