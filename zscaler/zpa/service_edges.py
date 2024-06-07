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
import os
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

    def get_service_edge(self, service_edge_id: str, **kwargs) -> Box:
        """
        Returns information on the specified Service Edge.

        Args:
            service_edge_id (str): The unique id of the ZPA Service Edge.

        Returns:
            :obj:`Box`: The Service Edge resource record.

        Examples:
            >>> service_edge = zpa.service_edges.get_service_edge('999999')

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get(f"serviceEdge/{service_edge_id}", params=params)

    def get_service_edge_by_name(self, name, **kwargs):
        """
        Returns information on the private service edge with the specified name.

        Args:
            name (str): The name of the private service edge.

        Returns:
            :obj:`Box` or None: The resource record for the private service edge if found, otherwise None.

        Examples:
            >>> pse = zpa.service_edges.get_service_edge_by_name('example_name')
            >>> if pse:
            ...     pprint(pse)
            ... else:
            ...     print("Private Service Edge not found")

        """
        pses = self.list_service_edges(**kwargs)
        for pse in pses:
            if pse.get("name") == name:
                return pse
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
        payload = {snake_to_camel(k): v for k, v in self.get_service_edge(service_edge_id).items()}

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}
        resp = self.rest.put(f"serviceEdge/{service_edge_id}", json=payload, params=params).status_code
        if not isinstance(resp, Response):
            return self.get_service_edge(service_edge_id)

    def delete_service_edge(self, service_edge_id: str, **kwargs) -> int:
        """
        Deletes the specified Private Service Edge from ZPA.

        Args:
            service_edge_id (str): The unique id of the ZPA Private Service that will be deleted.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            >>> zpa.service_edges.delete_service_edge('99999')

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.delete(f"serviceEdge/{service_edge_id}", params=params).status_code

    def bulk_delete_service_edges(self, service_edge_ids: list, **kwargs) -> int:
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

        payload = {"ids": service_edge_ids}
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.post("serviceEdge/bulkDelete", json=payload)

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

    def get_service_edge_group(self, group_id: str, **kwargs) -> Box:
        """
        Returns information on the specified ZPA Service Edge Group.

        Args:
            group_id (str): The unique id of the ZPA Service Edge Group.

        Returns:
            :obj:`Box`: The specified ZPA Service Edge Group resource record.

        Examples:
            >>> group = zpa.service_edges.get_service_edge_group("99999")

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get(f"serviceEdgeGroup/{group_id}", params=params)

    def get_service_edge_group_by_name(self, name, **kwargs) -> Box:
        """
        Returns information on the private service edge group with the specified name.

        Args:
            name (str): The name of the private service edge group.

        Returns:
            :obj:`Box` or None: The resource record for the private service edge group if found, otherwise None.

        Examples:
            >>> group = zpa.service_edges.get_service_edge_group_by_name('example_name')
            >>> if group:
            ...     pprint(group)
            ... else:
            ...     print("Private Service Edge Group not found")
        """
        groups = self.list_service_edge_groups(**kwargs)
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
                The City and Country for where the Service Edges are located. Format is:

                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
            **country_code (str):
                The ISO<std> Country Code that represents the country where the Service Edges are located.
            **enabled (bool):
                Is the Service Edge Group enabled? Defaults to ``True``.
            **is_public (bool):
                Is the Service Edge publicly accessible? Defaults to ``False``.
            **override_version_profile (bool):
                Override the local Service Edge version according to ``version_profile``. Defaults to ``False``.
            **service_edge_ids (list):
                A list of unique ids of ZPA Service Edges that belong to this Service Edge Group.
            **trusted_network_ids (list):
                A list of unique ids of Trusted Networks that are associated with this Service Edge Group.
            **upgrade_day (str):
                The day of the week that upgrades will be pushed to the Service Edge.
            **upgrade_time_in_secs (str):
                The time of the day that upgrades will be pushed to the Service Edge.
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
        add_id_groups(self.reformat_params, kwargs, payload)
        pick_version_profile(kwargs, payload)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post("serviceEdgeGroup", json=payload, params=params)
        if isinstance(response, Response):
            status_code = response.status_code
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
                The City and Country for where the Service Edges are located. Format is:

                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
            **country_code (str):
                The ISO<std> Country Code that represents the country where the Service Edges are located.
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
                Override the local Service Edge version according to ``version_profile``. Defaults to ``False``.
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
        payload = {snake_to_camel(k): v for k, v in self.get_service_edge_group(group_id).items()}

        add_id_groups(self.reformat_params, kwargs, payload)
        pick_version_profile(kwargs, payload)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        resp = self.rest.put(f"serviceEdgeGroup/{group_id}", json=payload, params=params).status_code
        if not isinstance(resp, Response):
            return self.get_service_edge_group(group_id)

    def delete_service_edge_group(self, group_id: str, **kwargs) -> int:
        """
        Deletes the specified Service Edge Group from ZPA.

        Args:
            service_edge_group_id (str): The unique id of the ZPA Service Edge Group.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zpa.service_edges.delete_service_edge_group("99999")
        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.delete(f"serviceEdgeGroup/{group_id}", params=params).status_code

    def get_service_edge_schedule(self, customer_id=None, **kwargs) -> Box:
        """
        Returns the configured Service Edge Schedule frequency.

        Args:
            id (str): Unique identifier for the Service Edge auto deletion config.
                Required for the PUT request to update the Service Edge Settings frequency.
            customer_id (str): Unique identifier of the ZPA tenant.
            delete_disabled (bool): If true, includes Service Edges for deletion if
                they are disconnected, based on frequencyInterval and frequency values.
            enabled (bool): If true, the deletion of Service Edges setting is enabled.
            frequency (str): Frequency at which disconnected Service Edges are deleted.
            frequency_interval (str): Interval for the frequency value, minimum is 5.

        Returns:
            :obj:`Box`: The Auto Delete frequency of the Service Edge for the specified customer.

        Examples:
            >>> pprint(zpa.service_edges.get_service_edge_schedule)
        """

        if customer_id is None:
            customer_id = os.getenv("ZPA_CUSTOMER_ID")

        if not customer_id:
            raise ValueError(
                "customer_id is required either as a function argument or as an environment variable ZPA_CUSTOMER_ID"
            )

        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get("serviceEdgeSchedule", params=params)

    def add_service_edge_schedule(self, frequency, interval, disabled, enabled, **kwargs) -> Box:
        """
        Configure an Service Edge schedule frequency to delete inactive Service Edge based on
        the configured frequency.

        Args:
            frequency (str): Frequency at which disconnected Service Edges are deleted.
            interval (str): Interval for the frequency value, minimum supported is 5.
            disabled (bool): If true, includes service edges for deletion if disconnected.
            enabled (bool): Enables or disables the deletion setting for Service Edges.
            **kwargs: Optional keyword arguments.

        Keyword Args:
            name (str): Name of the schedule.
            customer_id (str): Unique identifier of the ZPA tenant.
            delete_disabled (bool): Includes Service Edges for deletion if they are
                disconnected, based on frequency and interval values.
            description (str): Additional information about the Service Edge Schedule.

        Returns:
            :obj:`Box`: Auto Delete frequency of the Service Edge for the specified customer.

        Examples:
            >>> schedule = zpa.service_edges.add_service_edge_schedule(
            ...    frequency='days',
            ...    interval='5',
            ...    disabled=False,
            ...    enabled=True,
            )
        """
        customer_id = kwargs.get("customer_id") or os.getenv("ZPA_CUSTOMER_ID")

        if not customer_id:
            raise ValueError(
                "customer_id is required either as a function argument or as an environment variable ZPA_CUSTOMER_ID"
            )

        payload = {
            "customerId": customer_id,
            "frequency": frequency,
            "frequencyInterval": interval,
            "deleteDisabled": disabled,
            "enabled": enabled,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("serviceEdgeSchedule", json=payload)

        if response.status_code == 204:
            return Box(payload)
        elif response.status_code == 400:
            error_response = response.json()
            if error_response.get("id") == "resource.already.exist":
                print("The schedule is already enabled.")
                return None
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def update_service_edge_schedule(self, scheduler_id: str, frequency, interval, disabled, enabled, **kwargs) -> Box:
        """
        Updates Service Edge schedule frequency to delete the inactive service edges based on
        the configured frequency.

        Args:
            scheduler_id (str): Unique identifier for the scheduler.
            **kwargs: Optional keyword arguments.

        Keyword Args:
            customer_id (str): Unique identifier of the ZPA tenant.
            delete_disabled (bool): Include Service Edges for deletion if disconnected,
                based on frequencyInterval and frequency values.
            enabled (bool): Enable or disable deletion of Service Edges.
            frequency (str): Frequency at which disconnected Service Edges are deleted.
            frequency_interval (str): Interval for the frequency value, minimum is 5.
                Supported: 5, 7, 14, 30, 60, 90.
            description (str): Additional information about the Service Edge Schedule.

        Returns:
            :obj:`Box`: The updated schedule record if successful, otherwise an error.

        Examples:
            Updating Service Edge schedule:

            >>> schedule = zpa.service_edges.update_service_edge_schedule(
            ...    scheduler_id='10',
            ...    frequency_interval='10',
            ...    frequency='days',
            ...    enabled=True,
            ...    delete_disabled=False
            )
            >>> print(schedule)  # Prints the updated schedule record
        """
        customer_id = kwargs.get("customer_id") or os.getenv("ZPA_CUSTOMER_ID")

        if not customer_id:
            raise ValueError(
                "customer_id is required either as a function argument or as an environment variable ZPA_CUSTOMER_ID"
            )

        payload = {
            "customerId": customer_id,
            "frequency": frequency,
            "frequencyInterval": interval,
            "enabled": enabled,
            "deleteDisabled": disabled,
        }

        response = self.rest.put(f"serviceEdgeSchedule/{scheduler_id}", json=payload)

        if response.status_code == 204:
            updated_schedule = self.get_service_edge_schedule(customer_id=customer_id)
            return updated_schedule
        elif response.status_code == 400:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
