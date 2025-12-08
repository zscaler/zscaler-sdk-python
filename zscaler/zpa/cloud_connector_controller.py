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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.cloud_connector_controller import CloudConnectorController
from zscaler.utils import format_url


class CloudConnectorControllerAPI(APIClient):
    """
    A Client object for the Cloud Connector Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_cloud_connectors(self, query_params: Optional[dict] = None) -> List[CloudConnectorController]:
        """
        Get all EdgeConnectors configured for a given customer.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            :obj:`Tuple`: A tuple containing List[CloudConnectorController]

        Examples:
            >>> try:
            ...     connector_list = client.zpa.cloud_connector_controller.list_cloud_connectors(
            ... query_params={'search': 'CloudConnector01', 'page': '1', 'page_size': '100'})
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Total cloud connectors found: {len(connector_list)}")
            ... for connector in connector_list:
            ...     print(connector.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /cloudConnector
        """
        )

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, CloudConnectorController)
        result = []
        for item in response.get_results():
            result.append(CloudConnectorController(self.form_response_body(item)))
        return result
