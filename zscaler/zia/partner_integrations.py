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
from zscaler.zia.models.partner_integrations import (
    CrowdStrikeEndpoint,
    IntegrationPartner,
    MicrosoftDefenderEndpoint,
    SandboxMd5Detail)


class PartnerIntegrationsAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_integration_partners(self, query_params=None) -> APIResult[List[IntegrationPartner]]:
        """
        Retrieves the MD5 hash of the file required to view the Sandbox Detail Report.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.api_key_provisioned]`` {bool}: Filters the partners list based on the provisioned API key

                ``[query_params.partner_type]`` {int}: Filters the partners list based on the partner type
                    Supported Values: `ANY`, `ORG_ADMIN`, `SDWAN`, `MSFT_VIRTUAL_WAN`, `PUBLIC_API`, `EXEC_INSIGHT`
                        `EXEC_INSIGHT_AND_ORG_ADMIN`, `ZSCALER_DECEPTION_ADMIN`, `ZSCALER_DECEPTION_SUPER_ADMIN`
                        `ZDX_ADMIN`, `EDGE_CONNECTOR_ADMIN`, `CSPM_ADMIN`

        Returns:
            tuple: (list of IntegrationPartner instances, Response, error)
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
                result.append(IntegrationPartner(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_crowdstrike_whitelisted_base_urls(self, query_params=None) -> APIResult[List[str]]:
        """
        Retrieves a list of CrowdStrike configured whitelisted base URLs (allowlist URLs).

        The API returns a plain JSON array of URL strings; no model is attached.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.partner_json_type]`` {str}: Optional. Filters based on the partner JSON type.
                    Supported Values: `CROWDSTRIKE_CREDENTIALS`, `CARBON_BLACK_CREDENTIALS`,
                    `ATP_DEFENDER_CREDENTIALS`, `UNIT_TESTING_CS`, `UNIT_TESTING_CB`

        Returns:
            tuple: (list of base URL strings, Response, error)

        Examples:
            List all CrowdStrike whitelisted base URLs::

                >>> urls, _, err = client.zia.partner_integrations.list_crowdstrike_whitelisted_base_urls()
                >>> if err:
                ...     print(f"Error listing whitelisted base URLs: {err}")
                ...     return
                >>> for url in urls:
                ...     print(url)

            Filter by partner JSON type::

                >>> urls, _, err = client.zia.partner_integrations.list_crowdstrike_whitelisted_base_urls(
                ...     query_params={'partner_json_type': 'CROWDSTRIKE_CREDENTIALS'}
                ... )
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
        return (response.get_results(), response, None)

    def list_crowdstrike_endpoints(self, query_params=None) -> APIResult[List[CrowdStrikeEndpoint]]:
        """
        Retrieves the list of CrowdStrike endpoints based on the indicator of compromise (IOC) query, with pagination support.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.type]`` {str}: Filters based on the IOC type. Supported Values: `MD5`
                ``[query_params.value]`` {str}: Filters based on the IOC value
                ``[query_params.limit]`` {int}: Specifies the page size
                ``[query_params.offset]`` {str}: Specifies the page offset
                ``[query_params.partner_json_type]`` {str}: Filters based on the partner JSON type
                    `CROWDSTRIKE_CREDENTIALS`, `CARBON_BLACK_CREDENTIALS`, `ATP_DEFENDER_CREDENTIALS`
                    `UNIT_TESTING_CS`, `UNIT_TESTING_CB`

        Returns:
            tuple: (list of CrowdStrikeEndpoint instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners/crowdStrike/endpoints
        """)

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(
            http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            result = []
            for item in response.get_results():
                result.append(CrowdStrikeEndpoint(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def accepts_crowdstrike_endpoint_list(self, **kwargs) -> APIResult[CrowdStrikeEndpoint]:
        """
        Accepts a list of CrowdStrike endpoint or device IDs in the request body and
        fetches detailed endpoint or device data for those IDs.

        Returns:
            tuple: The newly created CrowdStrikeEndpoint resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners/crowdStrike/endpoints
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CrowdStrikeEndpoint)
        if error:
            return (None, response, error)
        try:
            result = CrowdStrikeEndpoint(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_defender_endpoints(self, **kwargs) -> APIResult[MicrosoftDefenderEndpoint]:
        """
        Configures the integration of Microsoft Defender for Endpoint APIs with Zscaler.

        Returns:
            tuple: The newly created CrowdStrikeEndpoint resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners/microsoftDefender/endpoints
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, MicrosoftDefenderEndpoint)
        if error:
            return (None, response, error)
        try:
            result = MicrosoftDefenderEndpoint(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_md5_hash_report(self, md5_hash: str) -> APIResult[List[SandboxMd5Detail]]:
        """
        Retrieves the MD5 hash of the file required to view the Sandbox Detail Report.

        Args:
            md5_hash (str): Filters the Sandbox report based on the MD5 hash of the file

        Returns:
            tuple: (list of SandboxMd5Detail instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /integrationPartners/sandbox/report/{md5_hash}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

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
