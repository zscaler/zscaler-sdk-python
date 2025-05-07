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

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (list of App Connector instances, Response, error)

        Examples:
            >>> connector_list, _, err = client.zpa.app_connectors.list_connectors(
            ... query_params={'search': 'Connector01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing app connector: {err}")
            ...     return
            ... print(f"Total app connector found: {len(connector_list)}")
            ... for connector in connector_list:
            ...     print(connector.as_dict())
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

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppConnectorController)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(AppConnectorController(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_connector(self, connector_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified App Connector.

        Args:
            connector_id (str): The unique id for the ZPA App Connector.

        Returns:
            :obj:`Tuple`: The specified App Connector resource record.

        Examples:
            >>> fetched_connector, _, err = client.zpa.app_connectors.get_connector('999999')
            ... if err:
            ...     print(f"Error fetching connector by ID: {err}")
            ...     return
            ... print(f"Fetched connector by ID: {fetched_connector.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /connector/{connector_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppConnectorController)
        if error:
            return (None, response, error)

        try:
            result = AppConnectorController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_connector(self, connector_id: str, **kwargs) -> tuple:
        """
        Updates an existing ZPA App Connector.

        Args:
            connector_id (str): The unique id of the ZPA App Connector.

        Keyword Args:
            **name (str): The name of the App Connector.
            **description (str): Additional information about the App Connector.
            **enabled (bool): True if the App Connector is enabled.

        Returns:
            :obj:`Tuple`: The updated App Connector resource record.

        Examples:
            Update an App Connector name, description and disable it.

            >>> update_group, _, err = client.zpa.app_connectors.update_connector(
            ...     connector_id='99999'
            ...     name=f"UpdateAppConnector_{random.randint(1000, 10000)}",
            ...     description=f"UpdateAppConnector_{random.randint(1000, 10000)}",
            ...     enabled=False,
            ... )
            ... if err:
            ...     print(f"Error creating connector: {err}")
            ...     return
            ... print(f"connector created successfully: {update_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /connector/{connector_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppConnectorController)
        if error:
            return (None, response, error)

        if response is None:
            return (AppConnectorController({"id": connector_id}), None, None)

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
            >>> _, _, err = client.zpa.app_connectors.delete_connector(
            ...     connector_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting app connector: {err}")
            ...     return
            ... print(f"app connector with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /connector/{connector_id}
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

    def bulk_delete_connectors(self, connector_ids: list, microtenant_id: str = None) -> tuple:
        """
        Deletes all specified App Connectors from ZPA.

        Args:
            connector_ids (list): The list of unique ids for the ZPA App Connectors that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, err = client.zpa.app_connectors.bulk_delete_connectors(
            ...     connector_ids=['72058304855098016', '72058304855098017'])
            ... if err:
            ...     print(f"Error deleting connectors: {err}")
            ...     return
            ... print("Connectors deleted successfully.")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /connector/bulkDelete
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {"ids": connector_ids}

        request, error = self._request_executor.create_request(http_method, api_url, payload, params=params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
