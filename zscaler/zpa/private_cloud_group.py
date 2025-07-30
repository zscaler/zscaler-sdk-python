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

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.private_cloud_group import PrivateCloudGroup
from zscaler.zpa.models.common import CommonIDName
from zscaler.utils import format_url


class PrivateCloudGroupAPI(APIClient):
    """
    A Client object for the Private Cloud Group resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_cloud_groups(self, query_params=None) -> tuple:
        """
        Enumerates Private Cloud Groups in your organization with pagination.
        A subset of Private Cloud Groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (list of AppConnectorGroup instances, Response, error)

        Examples:
            >>> group_list, _, err = client.zpa.private_cloud_group.list_cloud_groups(
            ... query_params={'search': 'ConnectorGRP01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing app Private Cloud Group: {err}")
            ...     return
            ... print(f"Total app Private Cloud Groups found: {len(group_list)}")
            ... for group in groups:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /privateCloudControllerGroup
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloudGroup)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PrivateCloudGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_cloud_group(self, group_id: str, query_params=None) -> tuple:
        """
        Fetches a specific Private Cloud Group by ID.

        Args:
            group_id (str): The unique identifier for the Private Cloud Group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (AppConnectorGroup instance, Response, error).

        Examples:
            >>> fetched_group, _, err = client.zpa.private_cloud_group.get_cloud_group('999999')
            ... if err:
            ...     print(f"Error fetching group by ID: {err}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /privateCloudControllerGroup/{group_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloudGroup)
        if error:
            return (None, response, error)

        try:
            result = PrivateCloudGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_cloud_group(self, **kwargs) -> tuple:
        """
        Adds a new ZPA App Private Cloud Group.

        Args:
            name (str): The name of the App Private Cloud Group.
            latitude (int): The latitude representing the App Connector's physical location.
            location (str): The name of the location that the App Private Cloud Group represents.
            longitude (int): The longitude representing the App Connector's physical location.

        Keyword Args:
            **city_country (str):
                The City and Country for where the App Connectors are located. Format is:

                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
            **country_code (str):
                The ISO<std> Country Code that represents the country where the App Connectors are located.
            **description (str):
                Additional information about the App Private Cloud Group.
            **enabled (bool):
                Is the App Private Cloud Group enabled? Defaults to ``True``.
            **override_version_profile (bool):
                Override the local App Connector version according to ``version_profile_id``. Defaults to ``False``.
            **upgrade_day (str):
                The day of the week that upgrades will be pushed to the App Connector.
            **upgrade_time_in_secs (str):
                The time of the day that upgrades will be pushed to the App Connector.
            **version_profile_id (str):
                The version profile ID to use. This will automatically set ``override_version_profile`` to True.
            **microtenant_id (str):
                The unique identifier of the microtenant of ZPA tenant.
            **site (list):
                List of site configurations associated with this Private Cloud Group.
            **site_id (str):
                The unique identifier of the site associated with this Private Cloud Group.

        Returns:
            :obj:`Tuple`: A tuple containing (PrivateCloudGroup, Response, error)

        Examples:
            >>> added_group, _, err = client.zpa.private_cloud_group.add_cloud_group(
            ...     name=f"NewPrivateCloudGroup_{random.randint(1000, 10000)}",
            ...     description=f"NewPrivateCloudGroup_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     city_country="San Jose, US",
            ...     country_code="US",
            ...     latitude="37.3382082",
            ...     longitude="-121.8863286",
            ...     location="San Jose, CA, USA",
            ...     upgrade_day="SUNDAY",
            ...     site_id="72058304855088543",
            ...     site=[
            ...         {
            ...             "id": "72058304855088543",
            ...             "privateBrokerGroupIds": [
            ...                 {
            ...                     "id": "72058304855063609"
            ...                 }
            ...             ],
            ...         }
            ...     ]
            ... )
            ... if err:
            ...     print(f"Error adding private cloud group: {err}")
            ...     return
            ... print(f"private cloud group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /privateCloudControllerGroup
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloudGroup)
        if error:
            return (None, response, error)

        try:
            result = PrivateCloudGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_cloud_group(self, group_id: str, **kwargs) -> tuple:
        """
        Updates an existing ZPA App Private Cloud Group.

        Args:
            group_id (str): The unique id for the App Private Cloud Group in ZPA.

        Keyword Args:
            **city_country (str):
                The City and Country for where the App Connectors are located. Format is:

                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
            **country_code (str):
                The ISO<std> Country Code that represents the country where the App Connectors are located.
            **description (str):
                Additional information about the App Private Cloud Group.
            **enabled (bool):
                Is the App Private Cloud Group enabled? Defaults to ``True``.
            **name (str): The name of the App Private Cloud Group.
            **latitude (int): The latitude representing the App Connector's physical location.
            **location (str): The name of the location that the App Private Cloud Group represents.
            **longitude (int): The longitude representing the App Connector's physical location.
            **override_version_profile (bool):
                Override the local App Connector version according to ``version_profile_id``. Defaults to ``False``.
            **upgrade_day (str):
                The day of the week that upgrades will be pushed to the App Connector.
            **upgrade_time_in_secs (str):
                The time of the day that upgrades will be pushed to the App Connector.
            **version_profile_id (str):
                The version profile ID to use. This will automatically set ``override_version_profile`` to True.
            **microtenant_id (str):
                The unique identifier of the microtenant of ZPA tenant.
            **site (list):
                List of site configurations associated with this Private Cloud Group.
            **site_id (str):
                The unique identifier of the site associated with this Private Cloud Group.

        Returns:
            tuple: A tuple containing (PrivateCloudGroup, Response, error)

        Examples:
            >>> update_group, _, err = client.zpa.private_cloud_group.update_cloud_group(
            ...     group_id="999999",
            ...     name=f"UpdatePrivateCloudGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdatePrivateCloudGroup_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     city_country="San Jose, US",
            ...     country_code="US",
            ...     latitude="37.3382082",
            ...     longitude="-121.8863286",
            ...     location="San Jose, CA, USA",
            ...     upgrade_day="SUNDAY",
            ...     site_id="72058304855088543",
            ...     site=[
            ...         {
            ...             "id": "72058304855088543",
            ...             "privateBrokerGroupIds": [
            ...                 {
            ...                     "id": "72058304855063609"
            ...                 }
            ...             ],
            ...         }
            ...     ]
            ... )
            ... if err:
            ...     print(f"Error updating private cloud group: {err}")
            ...     return
            ... print(f"private cloud group updated successfully: {update_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /privateCloudControllerGroup/{group_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloudGroup)
        if error:
            return (None, response, error)

        if response is None:
            return (PrivateCloudGroup({"id": group_id}), None, None)

        try:
            result = PrivateCloudGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_cloud_group(self, group_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified App Private Cloud Group from ZPA.

        Args:
            group_id (str): The unique identifier for the App Private Cloud Group.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:
            tuple: A tuple containing the response and error (if any).

        Examples:
            >>> _, _, err = client.zpa.private_cloud_group.delete_cloud_group(
            ...     group_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting app Private Cloud Group: {err}")
            ...     return
            ... print(f"app Private Cloud Group with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /privateCloudControllerGroup/{group_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)

    def list_private_cloud_group_summary(self, query_params=None) -> tuple:
        """
        Returns the name and ID of the configured Private Cloud Group.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: PrivateCloudGroup: The resource record for the microtenant.

        Examples:
            >>> group_list, err = client.zpa.private_cloud_group.get_private_cloud_group_summary()
            ... if err:
            ...     print(f"Error listing groups: {err}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /privateCloudControllerGroup/summary
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CommonIDName)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CommonIDName(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
