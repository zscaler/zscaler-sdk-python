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
from zscaler.utils import format_url
from zscaler.zcc.models.zdxgroupentitlements import ZdxGroupEntitlements
from zscaler.zcc.models.zpagroupentitlements import ZpaGroupEntitlements


class EntitlementAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def get_zdx_group_entitlements(self, query_params=None) -> tuple:
        """
        Returns the list ZDX group entitlements in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size.
                ``[query_params.search]`` {str}: The search string used to partially match.

        Returns:
            :obj:`list`: A list containing ZDX group entitlements in the Client Connector Portal.

        Examples:
            Prints all ZDX group entitlements in the Client Connector Portal to the console:

            >>> for group in zcc.entitlements.get_zdx_group_entitlements():
            ...    print(group)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getZdxGroupEntitlements
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
            result = []
            for item in response.get_results():
                result.append(ZdxGroupEntitlements(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_zdx_group_entitlement(self) -> tuple:
        """
        Updates ZDX Group Entitlement.

        Args:
            N/A

        Returns:
            tuple: A tuple containing the ZDX Group Entitlement.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /updateZdxGroupEntitlement
        """
        )
        body = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ZdxGroupEntitlements)
        if error:
            return (None, response, error)

        try:
            result = ZdxGroupEntitlements(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_zpa_group_entitlements(self, query_params=None) -> tuple:
        """
        Returns the list ZPA group entitlements in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size.
                ``[query_params.search]`` {str}: The search string used to partially match.

        Returns:
            :obj:`list`: A list containing ZPA group entitlements in the Client Connector Portal.

        Examples:
            Prints all ZPA group entitlements in the Client Connector Portal to the console:

            >>> for group in zcc.entitlements.get_zpa_group_entitlements():
            ...    print(group)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getZpaGroupEntitlements
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
            result = []
            for item in response.get_results():
                result.append(ZpaGroupEntitlements(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_zpa_group_entitlement(self) -> tuple:
        """
        Updates ZPA Group Entitlement.

        Args:
            N/A

        Returns:
            tuple: A tuple containing the ZPA Group Entitlement.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /updateZpaGroupEntitlement
        """
        )
        body = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ZpaGroupEntitlements)
        if error:
            return (None, response, error)

        try:
            result = ZpaGroupEntitlements(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
