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
from zscaler.zpa.models.server_group import ServerGroup
from zscaler.utils import format_url, add_id_groups


class ServerGroupsAPI(APIClient):
    """
    A client object for the Server Groups resource.
    """

    reformat_params = [
        ("server_ids", "servers"),
        ("app_connector_group_ids", "appConnectorGroups"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_groups(self, query_params=None) -> tuple:
        """
        Enumerates server groups in your organization with pagination.
        A subset of server groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (list of ServerGroups instances, Response, error)

        Examples:
            >>> groups_list, _, err = client.zpa.server_groups.list_groups(
            ... query_params={'search': 'Group01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing server groups: {err}")
            ...     return
            ... print(f"Total server groups found: {len(groups_list)}")
            ... for group in groups_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serverGroup
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request, ServerGroup)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ServerGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_group(self, group_id: str, query_params=None) -> tuple:
        """
        Provides information on the specified server group.

        Args:
            group_id (str): The unique id for the server group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (ServerGroup, Response, error)

        Examples:
            >>> fetched_group, _, err = client.zpa.server_groups.get_group('999999')
            ... if err:
            ...     print(f"Error fetching server group by ID: {err}")
            ...     return
            ... print(f"Fetched server group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /serverGroup/{group_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServerGroup)
        if error:
            return (None, response, error)

        try:
            result = ServerGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_group(self, **kwargs) -> tuple:
        """
        Adds a server group.

        Args:
            name (str): The name for the server group.
            app_connector_group_ids (list of str): A list of App connector IDs that will be attached to the server group.

            **kwargs:
                Optional params.

        Keyword Args:
            **application_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of applications to associate with this server group.
            **config_space (str): The configuration space. Accepted values are `DEFAULT` or `SIEM`.
            **description (str): Additional information about the server group.
            **enabled (bool): Enable the server group.
            **ip_anchored (bool): Enable IP Anchoring.
            **dynamic_discovery (bool): Enable Dynamic Discovery.
            **server_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of servers to associate with this server group.
            **microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (ServerGroup, Response, error)

        Examples:
            Create a server group with the minimum params:

            >>> added_group, _, err = client.zpa.server_groups.add_group(
            ...    name='new_server_group',
            ...    app_connector_group_ids=['99999'],
            ... )
            ... if err:
            ...     print(f"Error adding server group: {err}")
            ...     return
            ... print(f"Server Group added successfully: {added_group.as_dict()}")

            Create a server group and define a new application server on the fly:

            >>> added_group, _, err = client.zpa.server_groups.add_group(
            ...    name='new_server_group',
            ...    description='new_server_group',
            ...    enabled=True,
            ...    dynamic_discovery=False,
            ...    app_connector_group_ids=['99999'],
            ...    server_ids=['99999'],
            ... if err:
            ...     print(f"Error adding server group: {err}")
            ...     return
            ... print(f"Server Group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serverGroup
        """
        )

        body = kwargs

        # Check if microtenant_id is set in kwargs or the body, and use it to set query parameter
        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Reformat server_group_ids to match the expected API format (serverGroups)
        if "app_connector_group_ids" in body:
            body["appConnectorGroups"] = [{"id": group_id} for group_id in body.pop("app_connector_group_ids")]

        if "server_ids" in body:
            body["servers"] = [{"id": group_id} for group_id in body.pop("server_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServerGroup)
        if error:
            return (None, response, error)

        try:
            result = ServerGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_id: str, **kwargs) -> tuple:
        """
        Updates a server group.

        Args:
            group_id (str): The unique identifier for the server group.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (ServerGroup, Response, error)

        Examples:

            >>> update_group, _, err = client.zpa.server_groups.update_group(
            ...    group_id="999999",
            ...    name='update_server_group',
            ...    description='update_server_group',
            ...    enabled=True,
            ...    dynamic_discovery=True,
            ...    app_connector_group_ids=['99999'],
            ... if err:
            ...     print(f"Error adding server group: {err}")
            ...     return
            ... print(f"Server Group added successfully: {added_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serverGroup/{group_id}
        """
        )

        # Fetch the existing group to ensure mandatory fields like appConnectorGroups are preserved
        existing_group, _, err = self.get_group(group_id)
        if err:
            return (None, None, f"Error fetching the existing group: {err}")

        body = existing_group.request_format()

        body.update(kwargs)

        if "dynamicDiscovery" not in body:
            body["dynamicDiscovery"] = True

        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "app_connector_group_ids" in body:
            body["appConnectorGroups"] = [{"id": group_id} for group_id in body.pop("app_connector_group_ids")]

        if "server_ids" in body:
            body["servers"] = [{"id": group_id} for group_id in body.pop("server_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServerGroup)
        if error:
            return (None, response, error)

        if response is None:
            return (ServerGroup({"id": group_id}), None, None)

        try:
            result = ServerGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_group(self, group_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified server group.

        Args:
            group_id (str): The unique id for the server group to be deleted.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            tuple: A tuple containing (None, Response, error)

        Examples:
            >>> _, _, err = client.zpa.server_groups.delete_group(
            ...     group_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting server groups: {err}")
            ...     return
            ... print(f"server groups with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serverGroup/{group_id}
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
