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


class AppConnectorControllerAPI:
    reformat_params = [
        ("connector_ids", "connectors"),
        ("server_group_ids", "serverGroups"),
    ]

    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_connectors(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured App Connectors.

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
            :obj:`BoxList`: List containing all configured ZPA App Connectors.

        Examples:
            List all configured App Connectors:

            >>> for connector in zpa.connectors.list_connectors():
            ...    print(connector)

        """
        list, _ = self.rest.get_paginated_data(path="/connector", **kwargs, api_version="v1")
        return list

    def get_connector(self, connector_id: str) -> Box:
        """
        Returns information on the specified App Connector.

        Args:
            connector_id (str): The unique id for the ZPA App Connector.

        Returns:
            :obj:`Box`: The specified App Connector resource record.

        Examples:
            >>> app_connector = zpa.connectors.get_connector('99999')

        """
        response = self.rest.get("/connector/%s" % (connector_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def get_connector_by_name(self, name):
        apps = self.list_connectors()
        for app in apps:
            if app.get("name") == name:
                return app
        return None

    def update_connector(self, connector_id: str, **kwargs):
        """
        Updates an existing ZPA App Connector.

        Args:
            connector_id (str): The unique id of the ZPA App Connector.
            **kwargs: Optional keyword args.

        Keyword Args:
            **description (str): Additional information about the App Connector.
            **enabled (bool): True if the App Connector is enabled.
            **name (str): The name of the App Connector.

        Returns:
            :obj:`Box`: The updated App Connector resource record.

        Examples:
            Update an App Connector name and disable it.

            >>> app_connector = zpa.connectors.update_connector('999999',
            ...    name="Updated App Connector Name",
            ...    enabled=False)

        """
        # Set payload to equal existing record
        payload = {snake_to_camel(k): v for k, v in self.get_connector(connector_id).items()}

        # Perform formatting on simplified params
        add_id_groups(self.reformat_params, kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put("/connector/%s" % (connector_id), json=payload).status_code
        if not isinstance(resp, Response):
            return self.get_connector(connector_id)

    def delete_connector(self, connector_id: str) -> int:
        """
        Deletes the specified App Connector from ZPA.

        Args:
            connector_id (str): The unique id for the ZPA App Connector that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zpa.connectors.delete_connector('999999')

        """
        return self.rest.delete(f"connector/{connector_id}").status_code

    def bulk_delete_connectors(self, connector_ids: list) -> int:
        """
        Deletes all specified App Connectors from ZPA.

        Args:
            connector_ids (list): The list of unique ids for the ZPA App Connectors that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zpa.connectors.bulk_delete_connectors(['111111', '222222', '333333'])

        """
        payload = {"ids": connector_ids}
        return self.rest.post("connector/bulkDelete", json=payload).status_code

    def list_connector_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all connector groups.

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
            :obj:`BoxList`: List of all configured connector groups.

        Examples:
            >>> connector_groups = zpa.connectors.list_connector_groups()

        """
        list, _ = self.rest.get_paginated_data(path="/appConnectorGroup", **kwargs, api_version="v1")
        return list

    def get_connector_group(self, group_id: str) -> Box:
        """
        Gets information for a specified connector group.

        Args:
            group_id (str):
                The unique identifier for the connector group.

        Returns:
            :obj:`Box`:
                The connector group resource record.

        Examples:
            >>> connector_group = zpa.connectors.get_connector_group('99999')

        """
        response = self.rest.get("/appConnectorGroup/%s" % (group_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def get_connector_group_by_name(self, name):
        groups = self.list_connector_groups()
        for group in groups:
            if group.get("name") == name:
                return group
        return None

    def add_connector_group(self, name: str, latitude: int, location: str, longitude: int, **kwargs) -> Box:
        """
        Adds a new ZPA App Connector Group.

        Args:
            name (str): The name of the App Connector Group.
            latitude (int): The latitude representing the App Connector's physical location.
            location (str): The name of the location that the App Connector Group represents.
            longitude (int): The longitude representing the App Connector's physical location.
            **kwargs: Optional keyword args.

        Keyword Args:
            **connector_ids (list):
                The unique ids for the App Connectors that will be added to this App Connector Group.
            **city_country (str):
                The City and Country for where the App Connectors are located. Format is:

                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
            **country_code (str):
                The ISO<std> Country Code that represents the country where the App Connectors are located.
            **description (str):
                Additional information about the App Connector Group.
            **dns_query_type (str):
                The type of DNS queries that are enabled for this App Connector Group. Accepted values are:
                ``IPV4_IPV6``, ``IPV4`` and ``IPV6``
            **enabled (bool):
                Is the App Connector Group enabled? Defaults to ``True``.
            **override_version_profile (bool):
                Override the local App Connector version according to ``version_profile``. Defaults to ``False``.
            **server_group_ids (list):
                The unique ids of the Server Groups that are associated with this App Connector Group
            **lss_app_connector_group (bool):
            **upgrade_day (str):
                The day of the week that upgrades will be pushed to the App Connector.
            **upgrade_time_in_secs (str):
                The time of the day that upgrades will be pushed to the App Connector.
            **version_profile (str):
                The version profile to use. This will automatically set ``override_version_profile`` to True.
                Accepted values are:
                ``default``, ``previous_default`` and ``new_release``

        Returns:
            :obj:`Box`: The resource record of the newly created App Connector Group.

        Examples:
            Add a new ZPA App Connector Group with parameters.

            >>> group = zpa.connectors.add_connector_group(name="New App Connector Group",
            ...    location="Sydney",
            ...    latitude="33.8688",
            ...    longitude="151.2093",
            ...    version_profile="default")

        """
        payload = {
            "name": name,
            "latitude": latitude,
            "location": location,
            "longitude": longitude,
        }

        # Perform formatting on simplified params
        add_id_groups(self.reformat_params, kwargs, payload)
        pick_version_profile(kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("appConnectorGroup", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_connector_group(self, group_id: str, **kwargs) -> Box:
        """
        Updates an existing ZPA App Connector Group.

        Args:
            group_id (str): The unique id for the App Connector Group in ZPA.
            **kwargs: Optional keyword args.

        Keyword Args:
            **connector_ids (list):
                The unique ids for the App Connectors that will be added to this App Connector Group.
            **city_country (str):
                The City and Country for where the App Connectors are located. Format is:

                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
            **country_code (str):
                The ISO<std> Country Code that represents the country where the App Connectors are located.
            **description (str):
                Additional information about the App Connector Group.
            **dns_query_type (str):
                The type of DNS queries that are enabled for this App Connector Group. Accepted values are:
                ``IPV4_IPV6``, ``IPV4`` and ``IPV6``
            **enabled (bool):
                Is the App Connector Group enabled? Defaults to ``True``.
            **name (str): The name of the App Connector Group.
            **latitude (int): The latitude representing the App Connector's physical location.
            **location (str): The name of the location that the App Connector Group represents.
            **longitude (int): The longitude representing the App Connector's physical location.
            **override_version_profile (bool):
                Override the local App Connector version according to ``version_profile``. Defaults to ``False``.
            **server_group_ids (list):
                The unique ids of the Server Groups that are associated with this App Connector Group
            **lss_app_connector_group (bool):
            **upgrade_day (str):
                The day of the week that upgrades will be pushed to the App Connector.
            **upgrade_time_in_secs (str):
                The time of the day that upgrades will be pushed to the App Connector.
            **version_profile (str):
                The version profile to use. This will automatically set ``override_version_profile`` to True.
                Accepted values are:

                ``default``, ``previous_default`` and ``new_release``

        Returns:
            :obj:`Box`: The updated ZPA App Connector Group resource record.

        Examples:
            Update the name of an App Connector Group in ZPA, change the version profile to new releases and disable
            the group.

            >>> group = zpa.connectors.update_connector_group('99999',
            ...    name="Updated App Connector Group",
            ...    version_profile="new_release",
            ...    enabled=False)

        """

        # Set payload to equal existing record
        payload = {snake_to_camel(k): v for k, v in self.get_connector_group(group_id).items()}

        # Perform formatting on simplified params
        add_id_groups(self.reformat_params, kwargs, payload)
        pick_version_profile(kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"appConnectorGroup/{group_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_connector_group(group_id)

    def delete_connector_group(self, group_id: str) -> int:
        """
        Deletes the specified App Connector Group from ZPA.

        Args:
            group_id (str): The unique identifier for the App Connector Group.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zpa.connectors.delete_connector_group('1876541121')

        """
        return self.rest.delete(f"appConnectorGroup/{group_id}").status_code

    def get_connector_schedule(self, customer_id=None) -> Box:
        """
        Returns the configured App Connector Schedule frequency.

        Args:
            id (str): Unique identifier for the App Connector auto deletion config.
                Required for the PUT request to update the App Connector Settings frequency.
            customer_id (str): Unique identifier of the ZPA tenant.
            delete_disabled (bool): If true, includes App Connectors for deletion if
                they are disconnected, based on frequencyInterval and frequency values.
            enabled (bool): If true, the deletion of App Connectors setting is enabled.
            frequency (str): Frequency at which disconnected App Connectors are deleted.
            frequency_interval (str): Interval for the frequency value, minimum is 5.

        Returns:
            :obj:`Box`: The Auto Delete frequency of the App Connector for the specified customer.

        Examples:
            >>> pprint(zpa.connectors.get_connector_schedule)
        """

        # Fetch customer_id from environment if not provided
        if customer_id is None:
            customer_id = os.getenv("ZPA_CUSTOMER_ID")

        if not customer_id:
            raise ValueError(
                "customer_id is required either as a function argument or as an environment variable ZPA_CUSTOMER_ID"
            )

        response = self.rest.get("/connectorSchedule")
        if isinstance(response, Response):
            return None
        return response

    def add_connector_schedule(self, frequency, interval, disabled, **kwargs) -> Box:
        """
        Configure an App Connector schedule frequency to delete inactive connectors based on
        the configured frequency.

        Args:
            frequency (str): Frequency at which disconnected App Connectors are deleted.
            interval (str): Interval for the frequency value, minimum supported is 5.
            disabled (bool): If true, includes connectors for deletion if disconnected.
            **kwargs: Optional keyword arguments.

        Keyword Args:
            name (str): Name of the schedule.
            customer_id (str): Unique identifier of the ZPA tenant.
            delete_disabled (bool): Includes App Connectors for deletion if they are
                disconnected, based on frequency and interval values.
            enabled (bool): Enables or disables the deletion setting for App Connectors.
            description (str): Additional information about the Connector Schedule.

        Returns:
            :obj:`Box`: Auto Delete frequency of the App Connector for the specified customer.

        Examples:
            >>> schedule = zpa.connectors.add_connector_schedule(
            ...    frequency='weekly',
            ...    interval='5',
            ...    disabled=False,
            ...    name='Weekly Deletion',
            ...    description='Deletes disconnected connectors weekly.'
            )
        """
        payload = {
            "frequency": frequency,
            "frequencyInterval": interval,
            "deleteDisabled": disabled,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("connectorSchedule", json=payload)
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code >= 400:  # Check if status code indicates an error
                raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_connector_schedule(self, scheduler_id: str, **kwargs) -> bool:
        """
        Updates App Connector schedule frequency to delete the inactive connectors based on
        the configured frequency.

        Args:
            scheduler_id (str): Unique identifier for the scheduler.
            customer_id (str): Unique identifier of the ZPA tenant.
            delete_disabled (bool): Include App Connectors for deletion if disconnected,
                based on frequencyInterval and frequency values.
            enabled (bool): Enable or disable deletion of App Connectors.
            frequency (str): Frequency at which disconnected App Connectors are deleted.
            frequency_interval (str): Interval for the frequency value, minimum is 5.
                Supported: 5, 7, 14, 30, 60, 90.

        Keyword Args:
            description (str): Additional information about the Connector Schedule.

        Returns:
            bool: True if update was successful, False otherwise.

        Examples:
            Updating connector schedule:

            >>> result = zpa.connectors.update_schedule('10', frequency_interval='10')
            >>> print(result)  # True if successful, False otherwise
        """
        # Get the current schedule by customer ID
        customer_id = kwargs.get("customer_id")
        if not customer_id:
            raise ValueError("customer_id must be provided as a keyword argument.")

        current_schedule = self.get_connector_schedule(customer_id=customer_id)

        if not current_schedule:
            raise ValueError("No existing schedule found for the provided customer ID.")

        # Update the schedule with provided arguments
        for key, value in kwargs.items():
            current_schedule[snake_to_camel(key)] = value

        # Send the updated schedule to the server
        response = self.rest.put(f"connectorSchedule/{scheduler_id}", json=current_schedule.to_dict())

        # Return True if the update was successful (204 No Content), False otherwise
        return response.status_code == 204
