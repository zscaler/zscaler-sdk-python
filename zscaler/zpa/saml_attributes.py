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
                ``[query_params.page_size]`` {int}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.
                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            list: A list of SAMLAttribute instances.

        Examples:
            >>> for saml_attribute in zpa.saml_attributes.list_attributes():
            ...    pprint(saml_attribute)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /samlAttribute
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(SAMLAttribute(
                    self.form_response_body(item))
                )
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
                ``[query_params.page_size]`` {int}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.
                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            list: A list of SAMLAttribute instances.

        Examples:
            >>> for saml_attribute in zpa.saml_attributes.list_attributes_by_idp('99999'):
            ...    pprint(saml_attribute)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /samlAttribute/idp/{idp_id}
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(
                    SAMLAttribute(self.form_response_body(item))
                )
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
            >>> attribute, response, error = zpa.saml_attributes.get_attribute('99999')
            >>> if attribute:
            ...    pprint(attribute)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /samlAttribute/{attribute_id}
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (None, response, error)

        try:
            # Directly return the raw response data as a dictionary
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
