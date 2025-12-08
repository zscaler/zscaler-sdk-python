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
from zscaler.zpa.models.idp import IDPController
from zscaler.utils import format_url


class IDPControllerAPI(APIClient):
    """
    A Client object for the Identity Provider (IdP) resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_idps(self, query_params: Optional[dict] = None) -> List[IDPController]:
        """
        Enumerates identity providers in your organization with pagination.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[IDPController]: A list of IDP instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     idps = client.zpa.idp.list_idps()
            ...     for idp in idps:
            ...         print(idp.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_v2}/idp")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        response = self._request_executor.execute(request, IDPController)

        return [IDPController(self.form_response_body(item)) for item in response.get_results()]

    def get_idp(self, idp_id: str) -> IDPController:
        """
        Returns information on the specified identity provider (IdP).

        Args:
            idp_id (str): The unique identifier for the identity provider.

        Returns:
            IDPController: The corresponding identity provider object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     idp = client.zpa.idp.get_idp('999999')
            ...     print(idp.id)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/idp/{idp_id}")

        request = self._request_executor.create_request(http_method, api_url, {}, {})
        response = self._request_executor.execute(request, IDPController)

        return IDPController(self.form_response_body(response.get_body()))
