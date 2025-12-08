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
from zscaler.zpa.models.microtenants import Microtenant
from zscaler.zpa.models.common import CommonFilterSearch
from zscaler.utils import format_url


class MicrotenantsAPI(APIClient):
    """
    A client object for the Microtenants resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_microtenants(self, query_params: Optional[dict] = None) -> List[Microtenant]:
        """
        Enumerates microtenants in your organization.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[Microtenant]: A list of Microtenant instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     tenants = client.zpa.microtenants.list_microtenants()
            ...     for tenant in tenants:
            ...         print(tenant.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/microtenants")

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, Microtenant)

        return [Microtenant(self.form_response_body(item)) for item in response.get_results()]

    def get_microtenant(self, microtenant_id: str) -> Microtenant:
        """
        Returns information on the specified microtenant.

        Args:
            microtenant_id (str): The unique identifier for the microtenant.

        Returns:
            Microtenant: The microtenant object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     tenant = client.zpa.microtenants.get_microtenant('999999')
            ...     print(tenant.id)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/microtenants/{microtenant_id}")

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request, Microtenant)

        return Microtenant(self.form_response_body(response.get_body()))

    def get_microtenant_summary(self) -> List[Microtenant]:
        """
        Returns the name and ID of configured Microtenants.

        Returns:
            List[Microtenant]: A list of Microtenant instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     tenants = client.zpa.microtenants.get_microtenant_summary()
            ...     for tenant in tenants:
            ...         print(tenant.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/microtenants/summary")

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request)

        response_body = response.get_body()
        if isinstance(response_body, list):
            return [Microtenant(item) for item in response_body]
        return []

    def get_microtenant_search(self, **kwargs) -> CommonFilterSearch:
        """
        Gets all configured Microtenants based on given filters.

        Args:
            **kwargs: Filtering, pagination, and sorting parameters.

        Returns:
            CommonFilterSearch: The search result object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     search_payload = {
            ...         "filter_and_sort_dto": {
            ...             "filter_by": [{"filter_name": "name", "operator": "LIKE", "values": ["Test"]}],
            ...             "page_by": {"page": 1, "page_size": 20}
            ...         }
            ...     }
            ...     result = client.zpa.microtenants.get_microtenant_search(**search_payload)
            ...     print(result.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/microtenants/search")

        body = kwargs

        request = self._request_executor.create_request(http_method, api_url, body=body)
        response = self._request_executor.execute(request, CommonFilterSearch)

        return CommonFilterSearch(self.form_response_body(response.get_body()))

    def add_microtenant(self, **kwargs) -> Microtenant:
        """
        Add a new microtenant.

        Args:
            name (str): The name of the microtenant.
            criteria_attribute (str): The criteria attribute.
            criteria_attribute_values (list): The values for the criteria attribute.

        Returns:
            Microtenant: The created microtenant object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     tenant = client.zpa.microtenants.add_microtenant(
            ...         name="Microtenant_A",
            ...         criteria_attribute="AuthDomain",
            ...         criteria_attribute_values=["acme.com"]
            ...     )
            ...     print(tenant.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/microtenants")

        body = kwargs

        request = self._request_executor.create_request(http_method, api_url, body=body)
        response = self._request_executor.execute(request, Microtenant)

        return Microtenant(self.form_response_body(response.get_body()))

    def update_microtenant(self, microtenant_id: str, **kwargs) -> Microtenant:
        """
        Updates the specified microtenant.

        Args:
            microtenant_id (str): The unique identifier for the microtenant.
            **kwargs: Fields to update.

        Returns:
            Microtenant: The updated microtenant object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     tenant = client.zpa.microtenants.update_microtenant(
            ...         '999999',
            ...         name="Updated_Tenant",
            ...         enabled=False
            ...     )
            ...     print(tenant.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/microtenants/{microtenant_id}")

        body = dict(kwargs)
        microtenant_id_param = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id_param} if microtenant_id_param else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, Microtenant)

        if response is None:
            return Microtenant({"id": microtenant_id})

        return Microtenant(self.form_response_body(response.get_body()))

    def delete_microtenant(self, microtenant_id: str) -> None:
        """
        Deletes the specified microtenant.

        Args:
            microtenant_id (str): The unique identifier for the microtenant.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.microtenants.delete_microtenant('99999')
            ...     print("Microtenant deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/microtenants/{microtenant_id}")

        request = self._request_executor.create_request(http_method, api_url)
        self._request_executor.execute(request)
