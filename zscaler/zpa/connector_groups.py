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

from zscaler.utils import Iterator, add_id_groups, pick_version_profile, snake_to_camel


class ConnectorGroupsAPI(APIEndpoint):
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
        return BoxList(Iterator(self._api, "appConnectorGroup", **kwargs))

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
        return self._get(f"appConnectorGroup/{group_id}")

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
            **pra_enabled (bool):
                Whether or not Privileged Remote Access is enabled on the App Connector Group? Defaults to ``False``.
            **waf_disabled (bool):
                Whether or not AppProtection is disabled for the App Connector Group. Defaults to ``False``.
            **use_in_dr_mode (bool):
                Whether or not the App Connector Group is designated for disaster recovery. Defaults to ``False``.
            **tcp_quick_ack_app (bool):
                Whether TCP Quick Acknowledgement is enabled or disabled for the application.
                The tcpQuickAckApp, tcpQuickAckAssistant, and tcpQuickAckReadAssistant fields must all share the same values.
            **tcp_quick_ack_assistant (bool):
                Whether TCP Quick Acknowledgement is enabled or disabled for the application.
                The tcpQuickAckApp, tcpQuickAckAssistant, and tcpQuickAckReadAssistant fields must all share the same values.
            **tcp_quick_ack_read_assistant (bool):
                Whether TCP Quick Acknowledgement is enabled or disabled for the application.
                The tcpQuickAckApp, tcpQuickAckAssistant, and tcpQuickAckReadAssistant fields must all share the same values.
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

        return self._post("appConnectorGroup", json=payload)

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
            **pra_enabled (bool):
                Whether or not Privileged Remote Access is enabled on the App Connector Group? Defaults to ``False``.
            **waf_disabled (bool):
                Whether or not AppProtection is disabled for the App Connector Group. Defaults to ``False``.
            **use_in_dr_mode (bool):
                Whether or not the App Connector Group is designated for disaster recovery. Defaults to ``False``.
            **tcp_quick_ack_app (bool):
                Whether TCP Quick Acknowledgement is enabled or disabled for the application.
                The tcpQuickAckApp, tcpQuickAckAssistant, and tcpQuickAckReadAssistant fields must all share the same values.
            **tcp_quick_ack_assistant (bool):
                Whether TCP Quick Acknowledgement is enabled or disabled for the application.
                The tcpQuickAckApp, tcpQuickAckAssistant, and tcpQuickAckReadAssistant fields must all share the same values.
            **tcp_quick_ack_read_assistant (bool):
                Whether TCP Quick Acknowledgement is enabled or disabled for the application.
                The tcpQuickAckApp, tcpQuickAckAssistant, and tcpQuickAckReadAssistant fields must all share the same values.
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

        resp = self._put(f"appConnectorGroup/{group_id}", json=payload).status_code

        if resp == 204:
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
        return self._delete(f"appConnectorGroup/{group_id}").status_code
