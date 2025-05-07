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

    def list_scim_attributes(self, idp_id: str, query_params=None) -> tuple:
        """
        Returns a list of all configured SCIM attributes for the specified IdP.

        Args:
            idp_id (str): The unique id of the IdP to retrieve SCIM attributes for.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            list: A list of SCIMAttributeHeader instances.

        Examples:
            >>> attributes_list, _, err = client.zpa.scim_attributes.list_scim_attributes(
            ...     idp_id=idp_id, query_params={"page": '1', "page_size": '10'}
            ... )
            ... if err:
            ...     print(f"Error listing SCIM Attributes: {err}")
            ...     return
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /idp/{idp_id}/scimattribute
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SCIMAttributeHeader)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(SCIMAttributeHeader(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_scim_attribute(self, idp_id: str, attribute_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified SCIM attribute.

        Args:
            idp_id (str): The unique id of the Idp corresponding to the SCIM attribute.
            attribute_id (str): The unique id of the SCIM attribute.

        Returns:
            SCIMAttributeHeader: The SCIMAttributeHeader resource object.

        Examples:
            >>> attribute = zpa.scim_attributes.get_attribute('99999', scim_attribute_id="88888")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /idp/{idp_id}/scimattribute/{attribute_id}
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SCIMAttributeHeader)
        if error:
            return (None, response, error)

        try:
            result = SCIMAttributeHeader(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_scim_values(self, idp_id: str, attribute_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified SCIM attribute values.

        Args:
            idp_id (str): The unique identifier for the IDP.
            attribute_id (str): The unique identifier for the attribute.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

        Returns:
            list: A list of attribute values for the SCIM attribute.

        Examples:
            >>> fetched_attribute, _, err = client.zpa.scim_attributes.get_scim_values()
            >>> if err:
            ...     print(f"Error fetching SCIM Attribute by ID: {err}")
            ...     return
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_userconfig}
            /scimattribute/idpId/{idp_id}/attributeId/{attribute_id}
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            body = response.get_body()
            # Assuming the API returns a list in the 'list' field as per the Postman response
            result = body.get("list", [])
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
