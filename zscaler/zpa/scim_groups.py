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


import asyncio
from concurrent.futures import ThreadPoolExecutor

from box import Box, BoxList
from restfly.endpoint import APIEndpoint, APISession

from zscaler.utils import Iterator


class SCIMGroupsAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)
        self.user_config_url = api.user_config_url

    def list_groups(self, idp_id: str, **kwargs) -> BoxList:
        """
        Returns a list of all configured SCIM groups for the specified IdP.

        Args:
            idp_id (str):
                The unique id of the IdP.

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
        return BoxList(Iterator(self._api, f"{self.user_config_url}/scimgroup/idpId/{idp_id}", **kwargs))

    def get_group(self, group_id: str, **kwargs) -> Box:
        """
        Returns information on the specified SCIM group.

        Args:
            group_id (str):
                The unique identifier for the SCIM group.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            all_entries (bool):
                Return all SCIM groups including the deleted ones if ``True``. Defaults to ``False``.

        Returns:
            :obj:`dict`: The resource record for the SCIM group.

        Examples:
            >>> pprint(zpa.scim_groups.get_group('99999'))

        """

        return self._get(f"{self.user_config_url}/scimgroup/{group_id}")

    def search_group(self, idp_id: str, group_name: str, **kwargs) -> dict:
        """
        Searches and returns the SCIM group with the specified name for the given IdP.
        """
        # Assuming the API supports setting a max item count
        page_size = kwargs.get("pagesize", 500)  # Adjust the page size as needed

        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            # Ensure that idp_id is the numeric ID, and search parameter is the group_name.
            pages = loop.run_until_complete(self._get_pages(executor, idp_id, group_name, page_size))

        for page in pages:
            for group in page.get("list", []):
                if group.get("name") == group_name:
                    return group  # Return the found group immediately
        return None  # Return None if the group wasn't found

    async def _get_pages(self, executor, idp_id, search, page_size):
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, self._get_page, idp_id, page_number, search, page_size)
            for page_number in range(1, self._get_total_pages(idp_id, page_size) + 1)
        ]
        return await asyncio.gather(*futures)

    def _get_page(self, idp_id, page_number, search, page_size):
        params = {"page": page_number, "search": search, "pagesize": page_size}  # Ensure this is being set correctly
        url = f"{self.user_config_url}/scimgroup/idpId/{idp_id}"
        # Print or log the URL and params for debugging
        print(f"URL: {url}, Params: {params}")
        return self._api.get(url, params=params)

    def _get_total_pages(self, idp_id, page_size):
        # Implement logic to get total pages, possibly by making a request to get total count of groups and dividing by page_size.
        # This is a placeholder; adjust it as necessary.
        total_groups = 1000  # Replace this with actual logic to get total group count
        return (total_groups // page_size) + (total_groups % page_size > 0)
