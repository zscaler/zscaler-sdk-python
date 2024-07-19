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

from box import BoxList
from requests import Response

from zscaler.zia import ZIAClient


class WorkloadGroupsAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all workload groups configured in the ZIA Admin Portal.

        Returns:
            :obj:`BoxList`: The list of workload groups

        Examples:
            >>> for workloads in zia.workload_groups.list_groups():
            ...    pprint(workloads)

        """
        response = self.rest.get("/workloadGroups")
        if isinstance(response, Response):
            return None
        return response

    # Search Workload Group By Name
    def get_group_by_name(self, name):
        """
        Retrieves a specific workload group by its name.

        Args:
            name (str): The name of the workload group  to retrieve.

        Returns:
            :obj:`Box`: The workload group  if found, otherwise None.

        Examples:
            >>> workload = zia.workload_groups.get_group_by_name('BD_WORKLOAD_GROUP01')
            ...    print(workload)
        """
        groups = self.list_groups()
        for group in groups:
            if group.get("name") == name:
                return group
        return None

    # Search Workload Group By ID
    def get_group_by_id(self, group_id):
        """
        Retrieves a specific workload group by its unique identifier.

        Args:
            profile_id (str): The ID of the workload group  to retrieve.

        Returns:
            :obj:`Box`: The workload group if found, otherwise None.

        Examples:
            >>> workload = zia.get_group_by_name.get_group_by_id('12345')
            ...    print(workload)
        """
        groups = self.list_groups()
        for group in groups:
            if group.get("id") == group_id:
                return group
        return None
