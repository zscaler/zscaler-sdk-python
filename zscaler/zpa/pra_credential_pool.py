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
from zscaler.zpa.models.pra_cred_pool_controller import PRACredentialPoolController
from zscaler.utils import format_url


class PRACredentialPoolAPI(APIClient):
    """
    A Client object for the Privileged Remote Access Credential Pool resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/waap-pra-config/v1/admin/customers/{customer_id}"

    def list_credential_pool(self, query_params=None) -> tuple:
        """
        Returns a list of all privileged remote access credential pool details.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.
                ``[query_params.sort_by]`` {str}: Indicates the parameter to sort by.
                ``[query_params.sort_dir]`` {str}: Specifies the sort direction. Supported Values: ASC and DESC

        Returns:
            tuple: A tuple containing (list of PrivilegedRemoteAccessCredential instances, Response, error)
            
        Examples:
            >>> credential_list, _, err = client.zpa.pra_credential.list_credentials(
            ... query_params={'search': 'pra_console01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing pra credentials: {err}")
            ...     return
            ... print(f"Total pra credentials found: {len(credential_list)}")
            ... for pra in credential_list:
            ...     print(pra.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential-pool
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

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
                result.append(PRACredentialPoolController(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)