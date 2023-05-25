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

from zscaler.utils import Iterator


class MachineGroupsAPI(APIEndpoint):
    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured machine groups.

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
            :obj:`list`: A list of all configured machine groups.

        Examples:
            >>> for machine_group in zpa.machine_groups.list_groups():
            ...    pprint(machine_group)

        """
        return BoxList(Iterator(self._api, "machineGroup", **kwargs))

    def get_group(self, group_id: str) -> Box:
        """
        Returns information on the specified machine group.

        Args:
            group_id (str):
                The unique identifier for the machine group.

        Returns:
            :obj:`Box`: The resource record for the machine group.

        Examples:
            >>> pprint(zpa.machine_groups.get_group('99999'))

        """

        return self._get(f"machineGroup/{group_id}")