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
from zscaler.zcc.models.getcompanyinfo import GetCompanyInfo
from zscaler.utils import format_url


class CompanyInfoAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def get_company_info(self) -> tuple:
        """
        Gets information about your organization such as the name of the business, domains, etc.
        Note: This API endpoint is allowed if called via OneAPI or if the token has admin or read-only admin privileges.

        Args:
            N/A

        Returns:
            :obj:`list`: Returns company information in the Client Connector Portal.

        Examples:
            Prints all devices in the Client Connector Portal to the console:

            >>> company_info, _, err = client.zcc.company.get_company_info()
            >>> if err:
            ...     print(f"Error listing company information: {err}")
            ...     return
            ... for company in company_info:
            ...     print(company.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getCompanyInfo
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GetCompanyInfo)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(GetCompanyInfo(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
