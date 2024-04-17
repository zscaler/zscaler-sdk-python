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
        Returns a list of all firewall filter rules.

        Returns:
            :obj:`BoxList`: The list of firewall filter rules

        Examples:
            >>> for rule in zia.workload_groups.list_groups():
            ...    pprint(rule)

        """
        response = self.rest.get("/workloadGroups")
        if isinstance(response, Response):
            return None
        return response

    # Search Workload Group By Name
    def get_group_by_name(self, name):
        groups = self.list_groups()
        for group in groups:
            if group.get("name") == name:
                return group
        return None

    # Search Workload Group By ID
    def get_group_by_id(self, group_id):
        groups = self.list_groups()
        for group in groups:
            if group.get("id") == group_id:
                return group
        return None
