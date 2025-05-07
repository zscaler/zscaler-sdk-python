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
from zscaler.utils import format_url


class ServiceEdgeControllerAPI(APIClient):
    reformat_params = [
        ("service_edge_ids", "serviceEdges"),
        ("trusted_network_ids", "trustedNetworks"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_service_edges(self, query_params=None) -> tuple:
        """
        Enumerates service edges in your organization with pagination.
        A subset of service edges can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string used to support search by features.

        Returns:
            :obj:`Tuple`: A tuple containing (list of ServiceEdge instances, Response, error)

        Examples:
            >>> service_edge_list, _, err = client.zpa.service_edges.list_service_edges(
            ... query_params={'search': 'ServiceEdge01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing service edges: {err}")
            ...     return
            ... print(f"Total service edges found: {len(service_edge_list)}")
            ... for edge in service_edge_list:
            ...     print(edge.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa}
            /serviceEdge
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.pop("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServiceEdge)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ServiceEdge(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_service_edge(self, service_edge_id: str, **kwargs) -> tuple:
        """
        Returns information on the specified Service Edge.

        Args:
            service_edge_id (str): The unique ID of the ZPA Service Edge.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: ServiceEdge: The corresponding Service Edge object.

        Examples:
            >>> fetched_service_edge, _, err = client.zpa.service_edges.get_service_edge('999999')
            ... if err:
            ...     print(f"Error fetching service edge by ID: {err}")
            ...     return
            ... print(f"Fetched service edge by ID: {fetched_service_edge.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._base_endpoint}/serviceEdge/{service_edge_id}
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

    def update_service_edge(self, service_edge_id: str, **kwargs) -> tuple:
        """
        Updates the specified ZPA Service Edge.

        Args:
            service_edge_id (str): The unique ID of the Service Edge.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Keyword Args:
            **name (str): The name of the Service Edge
            **description (str): Additional information about the Service Edge
            **enabled (bool): True if the Service Edge is enabled.

        Returns:
            :obj:`Tuple`: ServiceEdge: The updated Service Edge object.

        Examples:
            Update an Service Edge name, description and disable it.

            >>> update_service_edge, _, err = client.zpa.service_edges.update_service_edge(
            ...     service_edge_id='99999'
            ...     name=f"UpdateServiceEdge_{random.randint(1000, 10000)}",
            ...     description=f"UpdateServiceEdge_{random.randint(1000, 10000)}",
            ...     enabled=False,
            ... )
            ... if err:
            ...     print(f"Error creating service edge: {err}")
            ...     return
            ... print(f"Service Edge created successfully: {update_service_edge.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""{
            self._base_endpoint}/serviceEdge/{service_edge_id}"
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ServiceEdge)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (ServiceEdge({"id": service_edge_id}), None, None)

        try:
            result = ServiceEdge(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_service_edge(self, service_edge_id: str, **kwargs) -> int:
        """
        Deletes the specified ZPA Service Edge.

        Args:
            service_edge_id (str): The unique ID of the Service Edge to be deleted.

        Returns:
            int: Status code of the delete operation.

        Examples:
            >>> _, _, err = client.zpa.service_edges.delete_service_edge(
            ...     service_edge_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting service edge: {err}")
            ...     return
            ... print(f"Service Edge with ID {'999999'} deleted successfully.")
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
