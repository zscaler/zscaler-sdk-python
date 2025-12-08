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
from zscaler.zpa.models.saml_attributes import SAMLAttribute
from zscaler.utils import format_url


class SAMLAttributesAPI(APIClient):
    """
    A client object for the SAML Attribute resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_saml_attributes(self, query_params: Optional[dict] = None) -> List[SAMLAttribute]:
        """
        Returns a list of all configured SAML attributes.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[SAMLAttribute]: A list of SAMLAttribute instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     attributes = client.zpa.saml_attributes.list_saml_attributes()
            ...     for attr in attributes:
            ...         print(attr.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_v2}/samlAttribute")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, SAMLAttribute)

        return [SAMLAttribute(self.form_response_body(item)) for item in response.get_results()]

    def list_saml_attributes_by_idp(self, idp_id: str, query_params: Optional[dict] = None) -> List[SAMLAttribute]:
        """
        Returns a list of all configured SAML attributes for the specified IdP.

        Args:
            idp_id (str): The unique id of the IdP.
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[SAMLAttribute]: A list of SAMLAttribute instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     attributes = client.zpa.saml_attributes.list_saml_attributes_by_idp('15548452')
            ...     for attr in attributes:
            ...         print(attr.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_v2}/samlAttribute/idp/{idp_id}")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request)

        return [SAMLAttribute(self.form_response_body(item)) for item in response.get_results()]

    def get_saml_attribute(self, attribute_id: str, query_params: Optional[dict] = None) -> SAMLAttribute:
        """
        Returns information on the specified SAML attribute.

        Args:
            attribute_id (str): The unique identifier for the SAML attribute.
            query_params (dict, optional): Map of query parameters.

        Returns:
            SAMLAttribute: The SAML attribute object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     attr = client.zpa.saml_attributes.get_saml_attribute('72058304855114335')
            ...     print(attr.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/samlAttribute/{attribute_id}")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, SAMLAttribute)

        return SAMLAttribute(self.form_response_body(response.get_body()))

    def add_saml_attribute(self, **kwargs) -> SAMLAttribute:
        """
        Add a new SAML attribute.

        Args:
            name (str): The customer-defined name for a SAML attribute.
            user_attribute (bool): Whether the user attribute is used.
            idp_id (str): The unique identifier of the IdP.
            idp_name (str): The name of the IdP.
            saml_name (str): The SAML name.

        Returns:
            SAMLAttribute: The created SAML attribute object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     attr = client.zpa.saml_attributes.add_saml_attribute(
            ...         name='Custom_LastName_BD_Okta_Users',
            ...         idp_id='72058304855015574',
            ...         user_attribute=True
            ...     )
            ...     print(attr.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/samlAttribute")

        body = kwargs

        request = self._request_executor.create_request(http_method, api_url, body=body)
        response = self._request_executor.execute(request, SAMLAttribute)

        return SAMLAttribute(self.form_response_body(response.get_body()))

    def update_saml_attribute(self, attribute_id: str, **kwargs) -> SAMLAttribute:
        """
        Updates the specified SAML attribute.

        Args:
            attribute_id (str): The unique identifier of the SAML attribute.
            **kwargs: Fields to update.

        Returns:
            SAMLAttribute: The updated SAML attribute object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     attr = client.zpa.saml_attributes.update_saml_attribute(
            ...         '72058304855114335',
            ...         name='Updated_SAML_Attribute',
            ...         user_attribute=True
            ...     )
            ...     print(attr.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/samlAttribute/{attribute_id}")

        body = dict(kwargs)

        request = self._request_executor.create_request(http_method, api_url, body, {}, {})
        response = self._request_executor.execute(request, SAMLAttribute)

        if response is None:
            return SAMLAttribute({"id": attribute_id})

        return SAMLAttribute(self.form_response_body(response.get_body()))

    def delete_saml_attribute(self, attribute_id: str) -> None:
        """
        Deletes the specified SAML attribute.

        Args:
            attribute_id (str): The unique identifier for the SAML attribute.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.saml_attributes.delete_saml_attribute('72058304855114335')
            ...     print("SAML Attribute deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/samlAttribute/{attribute_id}")

        request = self._request_executor.create_request(http_method, api_url, {})
        self._request_executor.execute(request)
