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

from typing import List, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.web_dlp_global_options import WebDlpGlobalOptions


class WebDlpGlobalOptionsAPI(APIClient):
    """
    A Client object for the web_dlp_global_options resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_global_options(self, query_params: Optional[dict] = None) -> APIResult[List[WebDlpGlobalOptions]]:
        """
        Retrieves the DLP Advanced Settings information

        Returns:
            tuple: A tuple containing (list of WebDlpGlobalOptions instances, Response, error)

        Examples:
            Print the fetched global options:

            >>> fetched_options, _, error = client.zia.web_dlp_global_options.get_global_options()
            >>> if error:
            ...     print(f"Error fetching global options: {error}")
            ...     return
            ... print(f"Fetched global options: {fetched_options.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /webDlpGlobalOptions
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
                result.append(WebDlpGlobalOptions(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_option(self, **kwargs) -> APIResult[WebDlpGlobalOptions]:
        """
        Updates the existing DLP Advanced Settings.

        Args:
            name (str): Name to identify the time interval
            **kwargs: Optional keyword args.

        Keyword Args:
            applications (list): List of cloud applications exempted from DLP evaluation
            url_categories (list): List of custom URL categories exempted from DLP evaluation
            exempt_url_encoded_data (boolean): Indicates whether or not URL encoded data from DLP evaluation is exempted
            enable_npk_edm_templates (boolean): Indicates whether EDM with No Primary Keys is enabled.
            enable_npk_edm_templates_for_org (boolean): Indicates whether EDM with No Primary Keys is enabled for the organization.
            enable_inline_dlp_ocr (boolean): Indicates whether optical character recognition (OCR)
                for Zscaler DLP engines to scan images for text content in data in transit is enabled
            enable_casb_ocr (boolean): Indicates whether SaaS Security for Zscaler DLP engines to scan images for text content in data at rest is enabled
            enable_email_dlp_ocr (boolean): Indicates whether Outbound Email DLP for Zscaler DLP engines
                to scan images for text content in outbound emails is sent to external domains
            enable_evaluate_all_dlp_rules (boolean): Indicates whether DLP engines evaluate all rules or stop when a matching rule is found
            enable_edm_popular_format (boolean): Indicates whether EDM with popular formats is enabled.
            http_get_custom_url_categories (list): List of URL Categories to associate with Inspect HTTP GET Requests

        Returns:
            tuple: A tuple containing the WebDlpGlobalOptions instance, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /webDlpGlobalOptions
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WebDlpGlobalOptions)
        if error:
            return (None, response, error)

        try:
            result = WebDlpGlobalOptions(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
