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

    def list_idps(self, query_params=None) -> tuple:
        """
        Enumerates identity provider in your organization with pagination.
        A subset of identity provider can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.

                ``[query_params.scim_enabled]`` {bool}: Returns all SCIM IdPs if set to true.
                    Returns all non SCIM IdPs if set to false.

                ``[query_params.user_attributes]`` {bool}: Returns user attributes.

        Returns:
            :obj:`Tuple`: A tuple containing (list of IDP instances, Response, error)

        Examples:
            Retrieve enrollment certificates with pagination parameters:

            >>> idp_list, _, err = client.zpa.idp.list_idps(
            ... query_params={'search': 'IDP01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing idps: {err}")
            ...     return
            ... print(f"Total certificates found: {len(idp_list)}")
            ... for idp in idp_list:
            ...     print(idp.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /idp
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IDPController)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(IDPController(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_idp(self, idp_id: str) -> tuple:
        """
        Returns information on the specified identity provider (IdP).

        Args:
            idp_id (str): The unique identifier for the identity provider.

        Returns:
            :obj:`Tuple`: The corresponding identity provider object.

        Examples:
            >>> fetched_cert, _, err = client.zpa.certificates.get_enrolment('999999')
            ... if err:
            ...     print(f"Error fetching certificate by ID: {err}")
            ...     return
            ... print(fetched_cert.id)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /idp/{idp_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IDPController)

        if error:
            return (None, response, error)

        try:
            result = IDPController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
