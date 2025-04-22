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


class AccountDetailsAPI(APIClient):
    """
    A Client object for the AccountDetails resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_public_account_details(self, query_params=None) -> tuple:
        """
        Returns a list of public cloud account information.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            :obj:`Tuple`: List of configured public account details.

        Examples:

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in ztw.provisioning.list_public_account_details(page_size=200, max_pages=2):
            ...    print(location)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudAccountDetails
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
                result.append((self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_public_account_details(self, account_id: str, query_params=None) -> tuple:
        """
        Returns information for the public (Cloud Connector) cloud account information for the specified ID.

        Args:
            **account_id (str, optional): Account or subscription ID of public cloud account.
            **platform_id (string): Public cloud platform (AWS or Azure).

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            :obj:`Tuple`: The requested public account record.

        Examples:
            >>> location = ztw.provisioning.get_public_account_details('97456691')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudAccountDetails/{account_id}
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
                result.append((self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_public_account_details_lite(self, query_params=None) -> tuple:
        """
        Returns a subset of public (Cloud Connector) cloud account information.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            :obj:`Tuple`: A lite list of public account details.

        Examples:
            List accounts with default settings:

            >>> for account in ztw.provisioning.list_public_account_details_lite():
            ...    print(account)

            List accounts, limiting to a maximum of 10 items:

            >>> for account in ztw.provisioning.list_public_account_details_lite(max_items=10):
            ...    print(account)

            List accounts, returning 200 items per page for a maximum of 2 pages:

            >>> for account in ztw.provisioning.list_public_account_details_lite(page_size=200, max_pages=2):
            ...    print(account)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudAccountDetails/lite
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
                result.append((self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_public_account_status(self) -> tuple:
        """
        Returns a List of public (Cloud Connector) cloud account status information (enabled/disabled).

        Returns:
            :obj:`Tuple`: List of configured public account status.

        Examples:
            List public account status:
            >>> status = ztw.provisioning.list_public_account_status()
            ...    print(status)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudAccountIdStatus
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = response.get_body()
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_public_account_status(self, **kwargs) -> tuple:
        """
        Update an existing public account status.

        Keyword Args:
            account_id_enabled (bool): Indicates whether public cloud account is enabled.
            sub_id_enabled (bool): Indicates whether public cloud subscription is enabled.

        Returns:
            :obj:`Tuple`: The updated public account status details.

        Examples:
            Update the public account status::

                print(ztw.provisioning.update_public_account_status(account_id_enabled=True, sub_id_enabled=False))
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudAccountIdStatus
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
