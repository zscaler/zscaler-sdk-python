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
from zscaler.zpa.models.scim_groups import SCIMGroup
from zscaler.utils import format_url


class SCIMGroupsAPI(APIClient):
    """
    A client object for the SCIM Groups resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint_userconfig = f"/zpa/userconfig/v1/customers/{customer_id}"

    def list_scim_groups(self, idp_id: str, query_params: Optional[dict] = None) -> List[SCIMGroup]:
        """
        Returns a list of all configured SCIM groups for the specified IdP.

        Args:
            idp_id (str): The unique id of the IdP.
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[SCIMGroup]: A list of SCIMGroup instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     groups = client.zpa.scim_groups.list_scim_groups('999999')
            ...     for group in groups:
            ...         print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_userconfig}/scimgroup/idpId/{idp_id}")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        response = self._request_executor.execute(request, SCIMGroup)

        return [SCIMGroup(self.form_response_body(item)) for item in response.get_results()]

    def get_scim_group(self, group_id: str, query_params: Optional[dict] = None) -> SCIMGroup:
        """
        Returns information on the specified SCIM group.

        Args:
            group_id (str): The unique identifier for the SCIM group.
            query_params (dict, optional): Map of query parameters.

        Returns:
            SCIMGroup: The SCIM group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.scim_groups.get_scim_group('99999')
            ...     print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_userconfig}/scimgroup/{group_id}")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, SCIMGroup)

        return SCIMGroup(self.form_response_body(response.get_body()))
