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
from zscaler.zpa.models.service_edges import ServiceEdge
from zscaler.utils import format_url, snake_to_camel


class ServiceEdgeControllerAPI(APIClient):
    # Parameter names that will be reformatted to be compatible with ZPAs API
    reformat_params = [
        ("service_edge_ids", "serviceEdges"),
        ("trusted_network_ids", "trustedNetworks"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_service_edges(self, query_params=None) -> tuple:
        """
        Enumerates service edges in your organization with pagination.
        A subset of service edges can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.microtenant_id] {str}: ID of the microtenant, if applicable.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of AppConnectorGroup instances, Response, error)
        """
        http_method = "get".upper()
        api_url = f"{self._base_endpoint}/serviceEdge"

        # Handle query parameters (including microtenant_id if provided)
        query_params = query_params or {}
        microtenant_id = query_params.pop("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        # Prepare request body and headers
        body = {}
        headers = {}
        form = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, form, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ServiceEdge)

        if error:
            return (None, response, error)

        # Parse the response into AppConnectorGroup instances
        try:
            result = []
            for item in response.get_results():
                result.append(ServiceEdge(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_service_edge(self, service_edge_id: str, **kwargs) -> ServiceEdge:
        """
        Returns information on the specified Service Edge.

        Args:
            service_edge_id (str): The unique ID of the ZPA Service Edge.

        Returns:
            ServiceEdge: The corresponding Service Edge object.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._base_endpoint}/serviceEdge/{service_edge_id}"
            """
        )

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return None

        response, error = self._request_executor.execute(request)
        if error:
            return None

        return ServiceEdge(response.get_body())

    def get_service_edge_by_name(self, name: str, **kwargs) -> ServiceEdge:
        """
        Returns information on the service edge with the specified name.

        Args:
            name (str): The name of the service edge.

        Returns:
            ServiceEdge: The corresponding Service Edge object or None if not found.
        """
        service_edges = self.list_service_edges(**kwargs)
        for edge in service_edges:
            if edge.name == name:
                return edge
        return None

    def update_service_edge(self, service_edge_id: str, **kwargs) -> ServiceEdge:
        """
        Updates the specified ZPA Service Edge.

        Args:
            service_edge_id (str): The unique ID of the Service Edge.

        Returns:
            ServiceEdge: The updated Service Edge object.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._base_endpoint}/serviceEdge/{service_edge_id}"
            """
        )

        # Fetch the current service edge data and update it with kwargs
        existing_edge = self.get_service_edge(service_edge_id)
        payload = existing_edge.request_format()

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, json=payload, params=params)
        if error:
            return None

        _, error = self._request_executor.execute(request)
        if error:
            return None

        return self.get_service_edge(service_edge_id)

    def delete_service_edge(self, service_edge_id: str, **kwargs) -> int:
        """
        Deletes the specified ZPA Service Edge.

        Args:
            service_edge_id (str): The unique ID of the Service Edge to be deleted.

        Returns:
            int: Status code of the delete operation.
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._base_endpoint}/serviceEdge/{service_edge_id}"
            """
        )

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return None

        response, error = self._request_executor.execute(request)
        if error:
            return None

        return response.get_status_code()

    def bulk_delete_service_edges(self, service_edge_ids: list, **kwargs) -> int:
        """
        Bulk deletes the specified Service Edges from ZPA.

        Args:
            service_edge_ids (list): A list of Service Edge IDs to be deleted.

        Returns:
            int: Status code for the operation.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._base_endpoint}/serviceEdge/bulkDelete"
            """
        )

        payload = {"ids": service_edge_ids}

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, json=payload, params=params)
        if error:
            return None

        response, error = self._request_executor.execute(request)
        if error:
            return None

        return response.get_status_code()
