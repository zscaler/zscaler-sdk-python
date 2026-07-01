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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.partner_integrations import SandboxMd5Detail


class PartnerIntegrationsAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_integration_partners(self, query_params=None) -> APIResult[List[SandboxMd5Detail]]:
        """
        List integration_partners.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of SandboxMd5Detail instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners
        """)

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
                result.append(SandboxMd5Detail(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_integration_partners_crowd_strike_whitelisted_base_urls(
        self, query_params=None
    ) -> APIResult[List[SandboxMd5Detail]]:
        """
        List integration_partners (crowdStrike/whitelistedBaseUrls).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of SandboxMd5Detail instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners/crowdStrike/whitelistedBaseUrls
        """)

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
                result.append(SandboxMd5Detail(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_integration_partners_crowd_strike_endpoints(self, query_params=None) -> APIResult[List[SandboxMd5Detail]]:
        """
        List integration_partners (crowdStrike/endpoints).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of SandboxMd5Detail instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners/crowdStrike/endpoints
        """)

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
                result.append(SandboxMd5Detail(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_integration_partners_sandbox_md5(self, query_params=None) -> APIResult[List[SandboxMd5Detail]]:
        """
        List integration_partners (sandbox/md5).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of SandboxMd5Detail instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners/sandbox/md5
        """)

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
                result.append(SandboxMd5Detail(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_integration_partner(self, **kwargs) -> APIResult[SandboxMd5Detail]:
        """
        Adds a new integration_partner.

        Returns:
            tuple: The newly created integration_partner resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SandboxMd5Detail)
        if error:
            return (None, response, error)
        try:
            result = SandboxMd5Detail(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
