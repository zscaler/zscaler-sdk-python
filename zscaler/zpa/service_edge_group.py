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
from zscaler.zpa.models.service_edge_groups import ServiceEdgeGroup
from zscaler.utils import format_url


class ServiceEdgeGroupAPI(APIClient):
    """
    A Client object for the Service Edge Group resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_service_edge_groups(self, query_params=None) -> tuple:
        """
        Enumerates connector groups in your organization with pagination.
        A subset of connector groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (list of ServiceEdgeGroup instances, Response, error)

        Examples:
            >>> group_list, _, err = client.zpa.service_edge_group.list_service_edge_groups(
            ... query_params={'search': 'ServiceEdgeGRP01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing app connector group: {err}")
            ...     return
            ... print(f"Total app connector groups found: {len(group_list)}")
            ... for group in groups:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serviceEdgeGroup
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServiceEdgeGroup)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ServiceEdgeGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_service_edge_group(self, group_id: str, query_params=None) -> tuple:
        """
        Retrieves information about a specific service edge group.

        Args:
            group_id (str): The unique identifier of the service edge group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: ServiceEdgeGroup: The service edge group object.

        Examples:
            >>> fetched_group, _, err = client.zpa.service_edge_group.get_service_edge_group('999999')
            ... if err:
            ...     print(f"Error fetching group by ID: {err}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /serviceEdgeGroup/{group_id}
        """
        )

        # Handle optional query parameters
        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServiceEdgeGroup)
        if error:
            return (None, response, error)

        # Parse the response into an AppConnectorGroup instance
        try:
            result = ServiceEdgeGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_service_edge_group(self, **kwargs) -> tuple:
        """
        Adds a new service edge group.

        Args:
            name (str): The name of the service edge group.
            latitude (str): The latitude of the physical location.
            longitude (str): The longitude of the physical location.
            location (str): The name of the location.

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
            **grace_distance_enabled (bool):
                If enabled, allows ZPA Private Service Edge Groups within the specified
                distance to be prioritized over a closer ZPA Public Service Edge.
            **grace_distance_value (int):
                Indicates the maximum distance in miles or kilometers to ZPA
                Private Service Edge groups that would override a ZPA Public Service Edge. i.e 1.0
            **grace_distance_value_unit (str):
                Indicates the grace distance unit of measure in miles or kilometers.
                This value is only required if graceDistanceEnabled is set to true.
                Supported Values: `MILES`, `KMS`

        Returns:
            :obj:`Tuple`: ServiceEdgeGroup: The newly created service edge group object.

        Examples:
            >>> added_group, _, err = client.zpa.service_edge_group.add_service_edge_group(
            ...     name=f"NewServiceEdgeGroup_{random.randint(1000, 10000)}",
            ...     description=f"NewServiceEdgeGroup_{random.randint(1000, 10000)}",
            ...     enabled= True,
            ...     city_country= "San Jose, US",
            ...     country_code= "US",
            ...     latitude= "37.3382082",
            ...     longitude= "-121.8863286",
            ...     location= "San Jose, CA, USA",
            ...     upgrade_day= "SUNDAY",
            ...     dns_query_type= "IPV4_IPV6",
            ... )
            ... if err:
            ...     print(f"Error creating service edge group: {err}")
            ...     return
            ... print(f"service edge group created successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serviceEdgeGroup
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "trusted_network_ids" in body:
            body["trustedNetworks"] = [{"id": network_id} for network_id in body.pop("trusted_network_ids")]

        if "service_edge_ids" in body:
            body["serviceEdges"] = [{"id": id} for id in body.pop("service_edge_ids")]

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServiceEdgeGroup)
        if error:
            return (None, response, error)

        try:
            result = ServiceEdgeGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_service_edge_group(self, group_id: str, **kwargs) -> tuple:
        """
        Updates a specified service edge group.

        Args:
            group_id (str): The unique ID of the service edge group.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            :obj:`Tuple`: ServiceEdgeGroup: The updated service edge group object.

        Examples:
            >>> update_group, _, err = client.zpa.service_edge_group.add_service_edge_group(
            ...     group_id='999999'
            ...     name=f"UpdateServiceEdgeGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdateServiceEdgeGroup_{random.randint(1000, 10000)}",
            ...     enabled= True,
            ...     city_country= "San Jose, US",
            ...     country_code= "US",
            ...     latitude= "37.3382082",
            ...     longitude= "-121.8863286",
            ...     location= "San Jose, CA, USA",
            ...     upgrade_day= "SUNDAY",
            ...     dns_query_type= "IPV4_IPV6",
            ... )
            ... if err:
            ...     print(f"Error creating service edge group: {err}")
            ...     return
            ... print(f"service edge group created successfully: {update_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serviceEdgeGroup/{group_id}
        """
        )

        # Start with an empty body or an existing resource's current data
        body = {}

        # Update the body with the fields passed in kwargs
        body.update(kwargs)

        # Use get instead of pop to keep microtenant_id in the body
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "trusted_network_ids" in body:
            body["trustedNetworks"] = [{"id": network_id} for network_id in body.pop("trusted_network_ids")]

        if "service_edge_ids" in body:
            body["serviceEdges"] = [{"id": id} for id in body.pop("service_edge_ids")]

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServiceEdgeGroup)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            return (ServiceEdgeGroup({"id": group_id}), None, None)

        # Parse the response into a ServiceEdgeGroup instance
        try:
            result = ServiceEdgeGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_service_edge_group(self, group_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified service edge group.

        Args:
            group_id (str): The unique ID of the service edge group to delete.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            int: Status code of the delete operation.

        Examples:
            >>> _, _, err = client.zpa.service_edge_group.delete_service_edge_group(
            ...     group_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting service edge group: {err}")
            ...     return
            ... print(f"service edge group with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serviceEdgeGroup/{group_id}
        """
        )

        # Handle microtenant_id in URL params if provided
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
