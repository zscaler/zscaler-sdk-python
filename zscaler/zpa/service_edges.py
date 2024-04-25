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

from zscaler.utils import add_id_groups, pick_version_profile, snake_to_camel
from zscaler.zpa.client import ZPAClient


class ServiceEdgesAPI:
    # Parameter names that will be reformatted to be compatible with ZPAs API
    reformat_params = [
        ("service_edge_ids", "serviceEdges"),
        ("trusted_network_ids", "trustedNetworks"),
    ]

    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_service_edges(self, **kwargs) -> BoxList:
        """
        Returns information on all configured ZPA Service Edges.

        Args:
            **kwargs: Optional keyword args.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to match against a department's name or comments attributes.

        Returns:
            :obj:`BoxList`: List containing information on all configured ZPA Service Edges.

        Examples:
            >>> for service_edge in zpa.service_edges.list_service_edges():
            ...    print(service_edge)

        """
        list, _ = self.rest.get_paginated_data(path="/serviceEdge", **kwargs, api_version="v1")
        return list

    def get_service_edge(self, service_edge_id: str) -> Box:
        """
        Returns information on the specified Service Edge.

        Args:
            service_edge_id (str): The unique id of the ZPA Service Edge.

        Returns:
            :obj:`Box`: The Service Edge resource record.

        Examples:
            >>> service_edge = zpa.service_edges.get_service_edge('999999')

        """
        response = self.rest.get("/serviceEdge/%s" % (service_edge_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def get_service_edge_by_name(self, name):
        apps = self.list_service_edges()
        for app in apps:
            if app.get("name") == name:
                return app
        return None

    def update_service_edge(self, service_edge_id: str, **kwargs) -> Box:
        """
        Updates the specified ZPA Service Edge.

        Args:
            service_edge_id (str): The unique id of the Service Edge that will be updated in ZPA.
            **kwargs: Optional keyword args.

        Keyword Args:
            **description (str): Additional information about the Service Edge.
            **enabled (bool): Enable the Service Edge. Defaults to ``True``.
            **name (str): The name of the Service Edge in ZPA.

        Returns:
            :obj:`Box`: The updated Service Edge resource record.

        Examples:
            >>> updated_service_edge = zpa.service_edge.update_service_edge('99999',
            ...    description="Updated Description",
            ...    name="Updated Name")

        """

        # Set payload to equal existing record
        payload = {snake_to_camel(k): v for k, v in self.get_service_edge(service_edge_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put("/serviceEdge/%s" % (service_edge_id), json=payload).status_code
        if not isinstance(resp, Response):
            return self.get_service_edge(service_edge_id)

    def delete_service_edge(self, service_edge_id: str) -> int:
        """
        Deletes the specified Service Edge from ZPA.

        Args:
            service_edge_id (str): The unique id of the ZPA Service Edge that will be deleted.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            >>> zpa.service_edges.delete_service_edge('99999')

        """
        return self.rest.delete(f"serviceEdge/{service_edge_id}").status_code

    def bulk_delete_service_edges(self, service_edge_ids: list) -> int:
        """
        Bulk deletes the specified Service Edges from ZPA.

        Args:
            service_edge_ids (list): A list of Service Edge ids that will be deleted from ZPA.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zpa.service_edges.bulk_delete_service_edges(['99999', '88888'])

        """
        payload = {
            "ids": service_edge_ids,
        }

        return self.rest.post("connector/bulkDelete", json=payload).status_code

    def list_service_edge_groups(self, **kwargs) -> BoxList:
        """
        Returns information on all configured Service Edge Groups in ZPA.

        Args:
            **kwargs: Optional keyword args.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to match against a department's name or comments attributes.

        Returns:
            :obj:`BoxList`: A list of all ZPA Service Edge Group resource records.

        Examples:
            Print all Service Edge Groups in ZPA.

            >>> for group in zpa.service_edges.list_service_edge_groups():
            ...    print(group)

        """
        list, _ = self.rest.get_paginated_data(path="/serviceEdgeGroup", **kwargs, api_version="v1")
        return list

    def get_service_edge_group(self, group_id: str) -> Box:
        """
        Returns information on the specified ZPA Service Edge Group.

        Args:
            group_id (str): The unique id of the ZPA Service Edge Group.

        Returns:
            :obj:`Box`: The specified ZPA Service Edge Group resource record.

        Examples:
            >>> group = zpa.service_edges.get_service_edge_group("99999")

        """
        response = self.rest.get("/serviceEdgeGroup/%s" % (group_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def get_service_edge_group_by_name(self, name):
        groups = self.list_service_edge_groups()
        for group in groups:
            if group.get("name") == name:
                return group
        return None

    def add_service_edge_group(self, name: str, latitude: str, longitude: str, location: str, **kwargs):
        """
        Adds a new Service Edge Group to ZPA.

        Args:
            latitude (str): The latitude representing the physical location of the ZPA Service Edges in this group.
            longitude (str): The longitude representing the physical location of the ZPA Service Edges in this group.
            location (str): The name of the physical location of the ZPA Service Edges in this group.
            name (str): The name of the Service Edge Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            **cityCountry (str):
                The City and Country for where the App Connectors are located. Format is:

                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
            **country_code (str):
                The ISO<std> Country Code that represents the country where the App Connectors are located.
            **enabled (bool):
                Is the Service Edge Group enabled? Defaults to ``True``.
            **is_public (bool):
                Is the Service Edge publicly accessible? Defaults to ``False``.
            **override_version_profile (bool):
                Override the local App Connector version according to ``version_profile``. Defaults to ``False``.
            **service_edge_ids (list):
                A list of unique ids of ZPA Service Edges that belong to this Service Edge Group.
            **trusted_network_ids (list):
                A list of unique ids of Trusted Networks that are associated with this Service Edge Group.
            **upgrade_day (str):
                The day of the week that upgrades will be pushed to the App Connector.
            **upgrade_time_in_secs (str):
                The time of the day that upgrades will be pushed to the App Connector.
            **version_profile (str):
                The version profile to use. This will automatically set ``override_version_profile`` to True.
                Accepted values are:

                ``default``, ``previous_default`` and ``new_release``

        Returns:
            :obj:`Box`: The resource record of the newly created Service Edge Group.

        Examples:
            Add a new Service Edge Group for Service Edges in Sydney and set the version profile to new releases.

            >>> group = zpa.service_edges.add_service_edge_group(name="My SE Group",
            ...    latitude="33.8688",
            ...    longitude="151.2093",
            ...    location="Sydney",
            ...    version_profile="new_release)

        """
        payload = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "location": location,
        }

        # Perform formatting on simplified params
        add_id_groups(self.reformat_params, kwargs, payload)
        pick_version_profile(kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("serviceEdgeGroup", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_service_edge_group(self, group_id: str, **kwargs) -> Box:
        """
        Updates the specified ZPA Service Edge Group.

        Args:
            group_id (str): The unique id of the ZPA Service Edge Group that will be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            **cityCountry (str):
                The City and Country for where the App Connectors are located. Format is:

                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
            **country_code (str):
                The ISO<std> Country Code that represents the country where the App Connectors are located.
            **enabled (bool):
                Is the Service Edge Group enabled? Defaults to ``True``.
            **is_public (bool):
                Is the Service Edge publicly accessible? Defaults to ``False``.
            **latitude (str):
                The latitude representing the physical location of the ZPA Service Edges in this group.
            **longitude (str):
                The longitude representing the physical location of the ZPA Service Edges in this group.
            **location (str): T
                he name of the physical location of the ZPA Service Edges in this group.
            **name (str):
                The name of the Service Edge Group.
            **override_version_profile (bool):
                Override the local App Connector version according to ``version_profile``. Defaults to ``False``.
            **service_edge_ids (list):
                A list of unique ids of ZPA Service Edges that belong to this Service Edge Group.
            **trusted_network_ids (list):
                A list of unique ids of Trusted Networks that are associated with this Service Edge Group.
            **upgrade_day (str):
                The day of the week that upgrades will be pushed to the Service Edges in this group.
            **upgrade_time_in_secs (str):
                The time of the day that upgrades will be pushed to the Service Edges in this group.
            **version_profile (str):
                The version profile to use. This will automatically set ``override_version_profile`` to True.
                Accepted values are:

                ``default``, ``previous_default`` and ``new_release``

        Returns:
            :obj:`Box`: The updated ZPA Service Edge Group resource record.

        Examples:
            Update the name of a Service Edge Group, change the Version Profile to 'default' and the upgrade day to
            Friday.

            >>> group = zpa.service_edges.update_service_edge_group('99999',
            ...    name="Updated Name",
            ...    version_profile="default",
            ...    upgrade_day="friday")

        """
        # Set payload to equal existing record
        payload = {snake_to_camel(k): v for k, v in self.get_service_edge_group(group_id).items()}

        # Perform formatting on simplified params
        add_id_groups(self.reformat_params, kwargs, payload)
        pick_version_profile(kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"serviceEdgeGroup/{group_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_service_edge_group(group_id)

    def delete_service_edge_group(self, service_edge_group_id: str) -> int:
        """
        Deletes the specified Service Edge Group from ZPA.

        Args:
            service_edge_group_id (str): The unique id of the ZPA Service Edge Group.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zpa.service_edges.delete_service_edge_group("99999")

        """
        return self.rest.delete(f"serviceEdgeGroup/{service_edge_group_id}").status_code
