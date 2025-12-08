"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from typing import List, Optional
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.app_connector_groups import AppConnectorGroup
from zscaler.utils import format_url


class AppConnectorGroupAPI(APIClient):
    """
    A Client object for the App Connector Groups resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_connector_groups(self, query_params: Optional[dict] = None) -> List[AppConnectorGroup]:
        """
        Enumerates connector groups in your organization with pagination.
        A subset of connector groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant.

        Returns:
            List[AppConnectorGroup]: A list of AppConnectorGroup instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     groups = client.zpa.app_connector_groups.list_connector_groups(
            ...         query_params={'search': 'ConnectorGRP01', 'page': '1', 'page_size': '100'}
            ...     )
            ...     print(f"Total app connector groups found: {len(groups)}")
            ...     for group in groups:
            ...         print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error listing app connector groups: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/appConnectorGroup")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppConnectorGroup)

        return [AppConnectorGroup(self.form_response_body(item)) for item in response.get_results()]

    def list_connector_groups_summary(self, query_params: Optional[dict] = None) -> List[AppConnectorGroup]:
        """
        Retrieves all configured app connector groups Name and IDs.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.
                ``[query_params.search]`` {str}: The search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant.

        Returns:
            List[AppConnectorGroup]: A list of AppConnectorGroup instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     groups = client.zpa.app_connector_groups.list_connector_groups_summary(
            ...         query_params={'search': 'Group01', 'page': '1', 'page_size': '100'}
            ...     )
            ...     print(f"Total app connector groups found: {len(groups)}")
            ...     for group in groups:
            ...         print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error listing app connector groups: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/appConnectorGroup/summary")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppConnectorGroup)

        return [AppConnectorGroup(self.form_response_body(item)) for item in response.get_results()]

    def get_connector_group(self, group_id: str, query_params: Optional[dict] = None) -> AppConnectorGroup:
        """
        Fetches a specific connector group by ID.

        Args:
            group_id (str): The unique identifier for the connector group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            AppConnectorGroup: The connector group instance.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.app_connector_groups.get_connector_group('999999')
            ...     print(f"Fetched group: {group.as_dict()}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error fetching group: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/appConnectorGroup/{group_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppConnectorGroup)

        return AppConnectorGroup(self.form_response_body(response.get_body()))

    def get_connector_group_sg(self, group_id: str, query_params: Optional[dict] = None) -> AppConnectorGroup:
        """
        Fetches a specific connector group by ID with server group details.

        Args:
            group_id (str): The unique identifier for the connector group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            AppConnectorGroup: The connector group instance with server group details.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.app_connector_groups.get_connector_group_sg('999999')
            ...     print(f"Fetched group: {group.as_dict()}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error fetching group: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/appConnectorGroup/{group_id}/sg")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AppConnectorGroup)

        return AppConnectorGroup(self.form_response_body(response.get_body()))

    def add_connector_group(self, **kwargs) -> AppConnectorGroup:
        """
        Adds a new ZPA App Connector Group.

        Args:
            name (str): The name of the App Connector Group.
            latitude (int): The latitude representing the App Connector's physical location.
            location (str): The name of the location that the App Connector Group represents.
            longitude (int): The longitude representing the App Connector's physical location.

        Keyword Args:
            **connector_ids (list): The unique ids for the App Connectors to add.
            **city_country (str): The City and Country. Format: ``<City>, <Country Code>``
            **country_code (str): The ISO Country Code.
            **description (str): Additional information about the App Connector Group.
            **dns_query_type (str): DNS query type. Values: ``IPV4_IPV6``, ``IPV4``, ``IPV6``
            **enabled (bool): Is the App Connector Group enabled? Defaults to ``True``.
            **override_version_profile (bool): Override version profile. Defaults to ``False``.
            **server_group_ids (list): Server Group IDs associated with this group.
            **lss_app_connector_group (bool): LSS App Connector Group flag.
            **upgrade_day (str): Day of the week for upgrades.
            **upgrade_time_in_secs (str): Time of day for upgrades.
            **version_profile (str): Version profile. Values: ``default``, ``previous_default``, ``new_release``

        Returns:
            AppConnectorGroup: The created App Connector Group.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.app_connector_groups.add_connector_group(
            ...         name="NewAppConnectorGroup",
            ...         description="New connector group",
            ...         enabled=True,
            ...         city_country="San Jose, US",
            ...         country_code="US",
            ...         latitude="37.3382082",
            ...         longitude="-121.8863286",
            ...         location="San Jose, CA, USA",
            ...         upgrade_day="SUNDAY",
            ...         dns_query_type="IPV4_IPV6",
            ...     )
            ...     print(f"Created group: {group.as_dict()}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error creating group: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/appConnectorGroup")

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, AppConnectorGroup)

        return AppConnectorGroup(self.form_response_body(response.get_body()))

    def update_connector_group(self, group_id: str, **kwargs) -> AppConnectorGroup:
        """
        Updates an existing ZPA App Connector Group.

        Args:
            group_id (str): The unique id for the App Connector Group in ZPA.

        Keyword Args:
            **connector_ids (list): The unique ids for the App Connectors to add.
            **city_country (str): The City and Country. Format: ``<City>, <Country Code>``
            **country_code (str): The ISO Country Code.
            **description (str): Additional information about the App Connector Group.
            **dns_query_type (str): DNS query type. Values: ``IPV4_IPV6``, ``IPV4``, ``IPV6``
            **enabled (bool): Is the App Connector Group enabled?
            **name (str): The name of the App Connector Group.
            **latitude (int): The latitude of the App Connector's location.
            **location (str): The location name.
            **longitude (int): The longitude of the App Connector's location.
            **override_version_profile (bool): Override version profile.
            **server_group_ids (list): Server Group IDs.
            **lss_app_connector_group (bool): LSS flag.
            **upgrade_day (str): Day of the week for upgrades.
            **upgrade_time_in_secs (str): Time of day for upgrades.
            **version_profile (str): Version profile.

        Returns:
            AppConnectorGroup: The updated App Connector Group.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.app_connector_groups.update_connector_group(
            ...         "999999",
            ...         name="UpdatedConnectorGroup",
            ...         description="Updated description",
            ...         enabled=True,
            ...     )
            ...     print(f"Updated group: {group.as_dict()}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error updating group: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/appConnectorGroup/{group_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, AppConnectorGroup)

        if response is None:
            return AppConnectorGroup({"id": group_id})

        return AppConnectorGroup(self.form_response_body(response.get_body()))

    def delete_connector_group(self, group_id: str, microtenant_id: Optional[str] = None) -> None:
        """
        Deletes the specified App Connector Group from ZPA.

        Args:
            group_id (str): The unique identifier for the App Connector Group.
            microtenant_id (str, optional): The optional ID of the microtenant.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.app_connector_groups.delete_connector_group('999999')
            ...     print("App connector group deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error deleting app connector group: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/appConnectorGroup/{group_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
