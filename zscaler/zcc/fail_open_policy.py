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
from zscaler.zcc.models.failopenpolicy import FailOpenPolicy


class FailOpenPolicyAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def list_by_company(self, query_params=None) -> tuple:
        """
        Returns the list of Fail Open Policy By Company in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size.

        Returns:
            :obj:`list`: A list containing Fail Open Policy By Company in the Client Connector Portal.

        Examples:
            List all Fail Open Policies:

            >>> policy_list, response, error = client.zcc.fail_open_policy.list_by_company()
            >>>     if error:
            ...         print(f"Error listing trusted networks: {error}")
            ...         return
            ...     for policy in policy_list:
            ...         print(policy.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webFailOpenPolicy/listByCompany
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
                result.append(FailOpenPolicy(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_failopen_policy(self, **kwargs) -> tuple:
        """
        Update Fail Open Policy

        Args:
           device_type: (int):
           policy_id: (int):

        Returns:
            tuple: A tuple containing the Updated Fail Open Policy, response, and error.

        Examples:
           Updates a fail open policy.

            >>> updated_policy, _, error = client.zcc.fail_open_policy.update_failopen_policy(
            ...     id='4441',
            ...     active='1',
            ...     captive_portal_web_sec_disable_minutes='10',
            ...     enable_captive_portal_detection='1',
            ...     enable_fail_open='1',
            ...     enable_strict_enforcement_prompt='0',
            ...     enable_web_sec_on_proxy_unreachable='0',
            ...     enable_web_sec_on_tunnel_failure='0',
            ...     strict_enforcement_prompt_delay_minutes='2',
            ...     strict_enforcement_prompt_message='',
            ...     tunnel_failure_retry_count='25',
            ... )
            >>> if error:
            ...         print(f"Error updating Fail Open Policy: {error}")
            ...         return
            ... print(f"Fail Open Policy updated successfully: {updated_policy.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webFailOpenPolicy/edit
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, FailOpenPolicy)
        if error:
            return (None, response, error)

        try:
            result = FailOpenPolicy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
