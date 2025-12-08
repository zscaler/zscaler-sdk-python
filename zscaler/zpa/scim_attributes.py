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
from zscaler.zpa.models.scim_attributes import SCIMAttributeHeader
from zscaler.utils import format_url


class ScimAttributeHeaderAPI(APIClient):
    """
    A client object for the SCIM Attribute Header resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_userconfig = f"/zpa/userconfig/v1/customers/{customer_id}"

    def list_scim_attributes(self, idp_id: str, query_params: Optional[dict] = None) -> List[SCIMAttributeHeader]:
        """
        Returns a list of all configured SCIM attributes for the specified IdP.

        Args:
            idp_id (str): The unique id of the IdP.
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[SCIMAttributeHeader]: A list of SCIMAttributeHeader instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     attributes = client.zpa.scim_attributes.list_scim_attributes('99999')
            ...     for attr in attributes:
            ...         print(attr.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/idp/{idp_id}/scimattribute")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        response = self._request_executor.execute(request, SCIMAttributeHeader)

        return [SCIMAttributeHeader(self.form_response_body(item)) for item in response.get_results()]

    def get_scim_attribute(self, idp_id: str, attribute_id: str, query_params: Optional[dict] = None) -> SCIMAttributeHeader:
        """
        Returns information on the specified SCIM attribute.

        Args:
            idp_id (str): The unique id of the IdP.
            attribute_id (str): The unique id of the SCIM attribute.
            query_params (dict, optional): Map of query parameters.

        Returns:
            SCIMAttributeHeader: The SCIM attribute object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     attr = client.zpa.scim_attributes.get_scim_attribute('99999', '88888')
            ...     print(attr.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/idp/{idp_id}/scimattribute/{attribute_id}")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, SCIMAttributeHeader)

        return SCIMAttributeHeader(self.form_response_body(response.get_body()))

    def get_scim_values(self, idp_id: str, attribute_id: str, query_params: Optional[dict] = None) -> List:
        """
        Returns information on the specified SCIM attribute values.

        Args:
            idp_id (str): The unique identifier for the IDP.
            attribute_id (str): The unique identifier for the attribute.
            query_params (dict): Map of query parameters for the request.

        Returns:
            List: A list of attribute values for the SCIM attribute.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     values = client.zpa.scim_attributes.get_scim_values('99999', '88888')
            ...     for value in values:
            ...         print(value)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_userconfig}/scimattribute/idpId/{idp_id}/attributeId/{attribute_id}")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        response = self._request_executor.execute(request)

        body = response.get_body()
        return body.get("list", [])
