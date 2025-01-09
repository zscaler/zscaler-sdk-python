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
from zscaler.zpa.models.app_connectors import AppConnectorController
from zscaler.utils import format_url


class AppConnectorControllerAPI(APIClient):
    """
    A Client object for the App Connectors resource.
    """

    reformat_params = [
        ("connector_ids", "connectors"),
        ("server_group_ids", "serverGroups"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_connectors(self, query_params=None) -> tuple:
        """
        Enumerates app connectors in your organization with pagination.
        A subset of app connectors can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.microtenant_id] {str}: ID of the microtenant, if applicable.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of App Connector instances, Response, error)

        Examples:
            List all configured App Connectors:

            >>> for connector in zpa.connectors.list_connectors():
            ...    print(connector)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /connector
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
                result.append(AppConnectorController(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_connector(self, connector) -> tuple:
        """
        Returns information on the specified App Connector.

        Args:
            connector_id (str): The unique id for the ZPA App Connector.

        Returns:
            :obj:`Box`: The specified App Connector resource record.

        Examples:
            >>> app_connector = zpa.connectors.get_connector('99999')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /connector
        """
        )

        # Ensure connector_group is a dictionary
        if isinstance(connector, dict):
            body = connector
        else:
            body = connector.as_dict()

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, AppConnectorController)
        if error:
            return (None, response, error)

        try:
            result = AppConnectorController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_connector(self, connector_id: str, connector) -> tuple:
        """
        Updates an existing ZPA App Connector.

        Args:
            connector_id (str): The unique id of the ZPA App Connector.

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
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /connector/{connector_id}
        """
        )

        # Ensure the connector_group is in dictionary format
        if isinstance(connector, dict):
            body = connector
        else:
            body = connector.as_dict()

        # Use get instead of pop to keep microtenant_id in the body
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, AppConnectorController)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (AppConnectorController({"id": connector_id}), None, None)

        # Parse the response into an AppConnectorGroup instance
        try:
            result = AppConnectorController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_connector(self, connector_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified App Connector from ZPA.

        Args:
            connector_id (str): The unique id for the ZPA App Connector that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zpa.connectors.delete_connector('999999')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /connector/{connector_id}
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

    def bulk_delete_connectors(self, connector_ids: list, microtenant_id: str = None) -> tuple:
        """
        Deletes all specified App Connectors from ZPA.

        Args:
            connector_ids (list): The list of unique ids for the ZPA App Connectors that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zpa.connectors.bulk_delete_connectors(['111111', '222222', '333333'])

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /connector/bulkDelete
        """
        )

        # Handle microtenant_id in URL params if provided
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {"ids": connector_ids}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, payload, params=params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
