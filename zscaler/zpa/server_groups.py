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

from zscaler.utils import add_id_groups, snake_to_camel
from zscaler.zpa.client import ZPAClient


class ServerGroupsAPI:
    reformat_params = [
        ("application_ids", "applications"),
        ("server_ids", "servers"),
        ("app_connector_group_ids", "appConnectorGroups"),
    ]

    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured server groups.

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
            :obj:`BoxList`: A list of all configured server groups.

        Examples:
            >>> for server_group in zpa.server_groups.list_groups():
            ...    pprint(server_group)

        """
        list, _ = self.rest.get_paginated_data(path="/serverGroup", **kwargs, api_version="v1")
        return list

    def get_group(self, group_id: str, **kwargs) -> Box:
        """
        Provides information on the specified server group.

        Args:
            group_id (str):
                The unique id for the server group.

        Returns:
            :obj:`Box`: The resource record for the server group.

        Examples:
            >>> pprint(zpa.server_groups.get_group('99999'))

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get(f"serverGroup/{group_id}", params=params)

    def get_server_group_by_name(self, name):
        """
        Returns information on the server group with the specified name.

        Args:
            name (str): The name of the server group.

        Returns:
            :obj:`Box` or None: The resource record for the server group if found, otherwise None.

        Examples:
            >>> group = zpa.server_groups.get_server_group_by_name('example_name')
            >>> if group:
            ...     pprint(group)
            ... else:
            ...     print("server group not found")
        """
        groups = self.list_groups()
        for group in groups:
            if group.get("name") == name:
                return group
        return None

    def add_group(self, app_connector_group_ids: list, name: str, **kwargs) -> Box:
        """
        Adds a server group.

        Args:
            name (str):
                The name for the server group.
            app_connector_group_ids (:obj:`list` of :obj:`str`):
                A list of application connector IDs that will be attached to the server group.
            **kwargs:
                Optional params.

        Keyword Args:
            application_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of applications to associate with this server group.
            config_space (str): The configuration space. Accepted values are `DEFAULT` or `SIEM`.
            description (str): Additional information about the server group.
            enabled (bool): Enable the server group.
            ip_anchored (bool): Enable IP Anchoring.
            dynamic_discovery (bool): Enable Dynamic Discovery.
            server_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of servers to associate with this server group.

        Returns:
            :obj:`Box`: The resource record for the newly created server group.

        Examples:
            Create a server group with the minimum params:

            >>> zpa.server_groups.add_group('new_server_group'
            ...    app_connector_group_ids['99999'])

            Create a server group and define a new server on the fly:

            >>> zpa.server_groups.add_group('new_server_group',
            ...    app_connector_group_ids=['99999'],
            ...    enabled=True,
            ...    servers=[{
            ...      'name': 'new_server',
            ...      'address': '10.0.0.30',
            ...      'enabled': True}])

        """
        payload = {
            "name": name,
            "appConnectorGroups": [{"id": group_id} for group_id in app_connector_group_ids],
        }

        add_id_groups(self.reformat_params, kwargs, payload)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post("serverGroup", json=payload, params=params)
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_group(self, group_id: str, **kwargs) -> Box:
        """
        Updates a server group.

        Args:
            group_id (str, required):
                The unique identifier for the server group.
            **kwargs: Optional keyword args.

        Keyword Args:
            app_connector_group_ids (:obj:`list` of :obj:`str`):
                A list of application connector IDs that will be attached to the server group.
            application_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of applications to associate with this server group.
            config_space (str): The configuration space. Accepted values are `DEFAULT` or `SIEM`.
            description (str): Additional information about the server group.
            enabled (bool): Enable the server group.
            ip_anchored (bool): Enable IP Anchoring.
            dynamic_discovery (bool): Enable Dynamic Discovery.
            server_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of servers to associate with this server group

        Returns:
            :obj:`Box`: The resource record for the updated server group.

        Examples:
            Update the name of a server group:

            >>> zpa.server_groups.update_group(name='Updated Name')

            Enable IP anchoring and Dynamic Discovery:

            >>> zpa.server_groups.update_group(ip_anchored=True,
            ...    dynamic_discovery=True)

        """
        payload = {snake_to_camel(k): v for k, v in self.get_group(group_id).items()}

        add_id_groups(self.reformat_params, kwargs, payload)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        resp = self.rest.put(f"serverGroup/{group_id}", json=payload, params=params).status_code
        if not isinstance(resp, Response):
            return self.get_group(group_id)

    def delete_group(self, group_id: str, **kwargs) -> int:
        """
        Deletes the specified server group.

        Args:
            group_id (str):
                The unique id for the server group to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.server_groups.delete_group('99999')

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.delete(f"serverGroup/{group_id}", params=params).status_code
