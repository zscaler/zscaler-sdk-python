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

    def list_server_groups(self, query_params=None) -> tuple:
        """
        Enumerates server groups in your organization with pagination.
        A subset of server groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.microtenant_id] {str}: ID of the microtenant, if applicable.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of ServerGroups instances, Response, error)

        Examples:
            >>> server_groups = zpa.server_groups.list_groups(search="example")
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

        # Prepare request
        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
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

        Returns:
            tuple: A tuple containing (ServerGroup, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /serverGroup/{group_id}
        """
        )

        # Handle optional query parameters
        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ServerGroup)
        if error:
            return (None, response, error)

        # Parse the response into an AppConnectorGroup instance
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
            app_connector_group_ids (list of str): A list of application connector IDs that will be attached to the server group.

        Returns:
            tuple: A tuple containing (ServerGroup, Response, error)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serverGroup
        """
        )

        # Construct the body from kwargs (as a dictionary)
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

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
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

        Returns:
            tuple: A tuple containing (ServerGroup, Response, error)
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

        # Use the existing group's data as the base body, to ensure mandatory fields are preserved
        body = existing_group.request_format()  # Fetch the current group representation

        # Update the body with the fields passed in kwargs (overwrite existing fields with updates)
        body.update(kwargs)

        # Ensure dynamicDiscovery is always included, default to True if not provided
        if "dynamicDiscovery" not in body:
            body["dynamicDiscovery"] = True

        # Check if microtenant_id is set in kwargs or the body, and use it to set query parameter
        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Reformat app_connector_group_ids to match the expected API format (appConnectorGroups)
        if "app_connector_group_ids" in body:
            body["appConnectorGroups"] = [{"id": group_id} for group_id in body.pop("app_connector_group_ids")]

        if "server_ids" in body:
            body["servers"] = [{"id": group_id} for group_id in body.pop("server_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, ServerGroup)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (ServerGroup({"id": group_id}), None, None)

        # Parse the response into a ServerGroup instance
        try:
            result = ServerGroup(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_group(self, group_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified server group.

        Args:
            group_id (str): The unique id for the server group to be deleted.

        Returns:
            tuple: A tuple containing (None, Response, error)
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

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
