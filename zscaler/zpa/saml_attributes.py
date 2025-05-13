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

    def list_saml_attributes(self, query_params=None) -> tuple:
        """
        Returns a list of all configured SAML attributes.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            list: A list of SAMLAttribute instances.

        Examples:
            >>> attributes_list, _, err = client.zpa.saml_attributes.list_saml_attributes(
            ...     query_params={"page": '1', "page_size": '10'}
            ... )
            ... if err:
            ...     print(f"Error listing SAML Attributes: {err}")
            ...     return
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /samlAttribute
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SAMLAttribute)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(SAMLAttribute(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_saml_attributes_by_idp(self, idp_id: str, query_params=None) -> tuple:
        """
        Returns a list of all configured SAML attributes for the specified IdP.

        Args:
            idp_id (str): The unique id of the IdP to retrieve SAML attributes from.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            list: A list of SAMLAttribute instances.

        Examples:
            >>> attributes_list, _, err = client.zpa.saml_attributes.list_saml_attributes_by_idp(
            ...     idp_id='15548452', query_params={"page": '1', "page_size": '10'}
            ... )
            ... if err:
            ...     print(f"Error listing SAML Attributes: {err}")
            ...     return
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /samlAttribute/idp/{idp_id}
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(SAMLAttribute(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_saml_attribute(self, attribute_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified SAML attribute.

        Args:
            attribute_id (str): The unique identifier for the SAML attribute.

        Returns:
            tuple: A tuple containing the raw response data (dict), response object, and error if any.

        Examples:
            >>> fetched_admin, _, err = client.zpa.saml_attributes.get_saml_attribute('72058304855114335')
            >>> if err:
            ...     print(f"Error fetching saml attribute by ID: {err}")
            ...     return
            ... print(f"Fetched saml attribute by ID: {fetched_admin.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /samlAttribute/{attribute_id}
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SAMLAttribute)
        if error:
            return (None, response, error)

        try:
            result = SAMLAttribute(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_saml_attribute(self, **kwargs) -> tuple:
        """
        Add a new saml attribute for a given customer

        Args:
            name (str): The customer-defined name for a SAML attribute.
            user_attribute (bool): Whether or not the user attribute is used.
            idp_id (str): The unique identifier of the IdP.
            idp_name (str): The name of the IdP.
            saml_name (str): Whether to enable the cloud browser isolation banner.

        Returns:
            tuple: A tuple containing the `SAMLAttribute` instance, response object, and error if any.

        Examples:
            >>> added_saml_attribute, _, err = client.zpa.saml_attributes.add_saml_attribute(
            ...     name='Custom_LastName_BD_Okta_Users',
            ...     idp_id='72058304855015574',
            ...     user_attribute=True,
            ... )
            ... if err:
            ...     print(f"Error configuring Saml Attribute: {err}")
            ...     return
            ... print(f"Saml Attribute added successfully: {added_saml_attribute.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /samlAttribute
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SAMLAttribute)
        if error:
            return (None, response, error)

        try:
            result = SAMLAttribute(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_saml_attribute(self, attribute_id: str, **kwargs) -> tuple:
        """
        Updates the specified Saml Attribute.

        Args:
            attribute_id (str): The unique identifier of the SAML attribute.

        Returns:
            :obj:`Tuple`: SAMLAttribute: The updated Saml Attribute object.

        Example:
            Basic example: Update an existing Saml Attribute

            >>> updated_attribute, _, err = zpa.saml_attributes.update_saml_attribute(
            ...     attribute_id='72058304855114335',
            ...     name='Custom_LastName_BD_Okta_Users',
            ...     idp_id='72058304855015574',
            ...     user_attribute=True,
            ... )
            ... if err:
            ...     print(f"Error updating Saml Attribute: {err}")
            ...     return
            ... print(f"Saml Attribute updated successfully: {updated_attribute.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /samlAttribute/{attribute_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SAMLAttribute)
        if error:
            return (None, response, error)

        if response is None:
            return (SAMLAttribute({"id": attribute_id}), None, None)

        try:
            result = SAMLAttribute(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_saml_attribute(self, attribute_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified Saml Attribute.

        Args:
            attribute_id (str): The unique identifier for the Saml Attribute to be deleted.

        Returns:
            int: Status code of the delete operation.

        Example:
            Delete a Saml Attribute by ID

            >>> _, _, err = client.zpa.saml_attributes.delete_saml_attribute('72058304855114335')
            ... if err:
            ...     print(f"Error deleting saml attribute: {err}")
            ...     return
            ... print(f"SAml Attribute with ID '72058304855114335' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /samlAttribute/{attribute_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {})
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        return (None, response, error)
