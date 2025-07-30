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
from zscaler.zpa.models.npn_client_controller import NPNClientController
from zscaler.utils import format_url


class NPNClientControllerAPI(APIClient):
    """
    A Client object for the NPN Client Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_vpn_connected_users(self, query_params=None) -> tuple:
        """
        Returns a list of all configured applications configured.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Page size for pagination.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            list: A list of `NPNClientController` instances.

        Examples:
            Retrieve all applications configured with pagination parameters:

            >>> vpn_list, _, err = client.zpa.npn_client_controller.list_vpn_connected_users()
            ... if err:
            ...     print(f"Error listing vpn connected users: {err}")
            ...     return
            ... print(f"Total vpn connected users found: {len(vpn_list)}")
            ... for vpn in vpn_list:
            ...     print(vpn.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /vpnConnectedUsers
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NPNClientController)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(NPNClientController(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
