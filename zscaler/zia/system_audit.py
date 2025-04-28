# """
# Copyright (c) 2023, Zscaler Inc.

# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# """

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.system_audit import ConfigAudit
from zscaler.utils import format_url


class SystemAuditReportAPI(APIClient):
    """
    A Client object for the System Audit Report resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    # Returning {"code":"RBA_LIMITED","message":"Functional scope restriction requires Reports"}
    def get_config_audit(self, query_params=None) -> tuple:
        """
        Retrieves the System Audit Report.

        Keyword Args:

        Returns:
            :obj:`Tuple`: Config Audit Report ZIA.

        Examples:
            List Sub Clouds with default settings:

            >>> subcloud_list, zscaler_resp, err = client.zia.sub_clouds.list_sub_clouds()
            ... if err:
            ...     print(f"Error listing sub clouds: {err}")
            ...     return
            ... print(f"Total sub clouds found: {len(subcloud_list)}")
            ... for cloud in subcloud_list:
            ...     print(cloud.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /configAudit
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
                result.append(ConfigAudit(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
