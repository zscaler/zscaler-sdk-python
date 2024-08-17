# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from box import Box, BoxList
from zscaler.utils import Iterator

from zscaler.zcon import ZCONClient


class EcGroupAPI:
    def __init__(self, client: ZCONClient):
        self.rest = client

    def list_ec_groups(self, **kwargs) -> BoxList:
        """
        List all Cloud & Branch Connector groups.

        Args:
            **kwargs: Optional keyword args to filter the results.

        Keyword Args:
            page (int): The page number to return.
            page_size (int): The number of items to return per page.

        Returns:
            :obj:`BoxList`: The list of ec groups.

        Examples:
            List all ec groups::

                for group in zcon.ecgroups.list_ec_group():
                    print(group)

        """
        return self.rest.get("ecgroup", params=kwargs)

    def get_ec_group(self, group_id: str) -> Box:
        """
        Get details for a specific Cloud or Branch Connector group by ID.

        Args:
            group_id (str): ID of Cloud or Branch Connector group.

        Returns:
            :obj:`Box`: The ec group details.

        Examples:
            Get details of a specific ec group:

                print(zcon.ecgroups.get_ec_group("123456789"))

        """
        return self.rest.get(f"ecgroup/{group_id}")

    def list_ec_group_lite(self, **kwargs) -> BoxList:
        """
        Returns the list of a subset of Cloud & Branch Connector group information.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.

        Returns:
            :obj:`BoxList`: A subset of Cloud & Branch Connector group information.

        Examples:
            List subset of Cloud & Branch Connector group information:

            >>> for group in zcon.ecgroups.list_ec_group_lite():
            ...    print(group)

        """
        return BoxList(Iterator(self.rest, "ecgroup/lite", **kwargs))

    def list_ec_instance_lite(self, **kwargs) -> BoxList:
        """
        Returns the list of a subset of Cloud & Branch Connector instance information.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.

        Returns:
            :obj:`BoxList`: A subset of Cloud & Branch Connector instance information.

        Examples:
            List subset of Cloud & Branch Connector instance information:

            >>> for instance in zcon.ecgroups.list_ec_instance_lite():
            ...    print(instance)

        """
        return self.rest.get("ecInstance/lite", params=kwargs)

    def get_ec_group_vm(self, group_id: str, vm_id: str) -> Box:
        """
        Gets a VM by specified Cloud or Branch Connector group ID and VM ID

        Args:
            ``group_id`` (str): Cloud or Branch Connector group ID.
            ``vm_id`` (str): Cloud or Branch Connector VM ID.

        Returns:
            :obj:`Box`: The ec group VM details.

        Examples:
            Get details of a specific ec group VM:

                print(zcon.ecgroups.get_ec_group_vm("123456789"))

        """
        return self.rest.get(f"ecgroup/{group_id}/{vm_id}")

    def delete_ec_group_vm(self, group_id: str, vm_id: str):
        """
        Deletes a VM specified by Cloud or Branch Connector group ID and VM ID.

        Args:
            template_id (str): The ID of the VM to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Delete a ec group VM::

                print(zcon.ecgroups.delete_ec_group_vm("123456789"))
        """
        return self.rest.delete(f"ecgroup/{group_id}/{vm_id}").status_code

    def list_ecvm_lite(self, **kwargs) -> BoxList:
        """
        Returns the list of a subset of Cloud & Branch Connector instance information.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.

        Returns:
            :obj:`BoxList`: A subset of Cloud & Branch Connector instance information.

        Examples:
            List subset of Cloud & Branch Connector instance information:

            >>> for instance in zcon.ecgroups.list_ec_instance_lite():
            ...    print(instance)

        """
        return self.rest.get("ecVm/lite", params=kwargs)
