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
from zscaler.utils import format_url, zcc_param_mapper
from zscaler.zcc.models.webpolicy import WebPolicy


class WebPolicyAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    @zcc_param_mapper
    def list_by_company(self, query_params=None) -> tuple:
        """
        Returns the list of Web Policy By Company ID in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.

                ``[query_params.device_type]`` {str}: Filter by device operating system type. Valid options are:
                    ios, android, windows, macos, linux.

                ``[query_params.search]`` {str}: The search string used to partially match.

                ``[query_params.search_type]`` {str}: The search string used to partially match.

        Returns:
            :obj:`list`: A list containing Web Policy By Company ID in the Client Connector Portal.

        Examples:
            Prints Web Policy By Company ID in the Client Connector Portal to the console:

            >>> policy_list, _, err = client.zcc.web_policy.list_by_company(query_params={'device_type': 'windows'})
            >>> if err:
            ...     print(f"Error listing company policies: {err}")
            ...     return
            ... for policy in policy_list:
            ...     print(policy.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /web/policy/listByCompany
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WebPolicy)
        if error:
            return (None, response, error)

        try:
            result = response.get_results()
        except Exception as error:
            return None, response, error

        return result, response, None

    def activate_web_policy(self, **kwargs) -> tuple:
        """
        Enables or disables a policy or app profile for the company by platform (iOS, Android, Windows, macOS, and Linux).

        Args:
           device_type: (int):
           policy_id: (int):

        Returns:
            tuple: A tuple containing the updated Activation Web Policy, response, and error.

        Examples:
            Activate Web Policy in the Client Connector Portal to the console:

            >>> web_policy, _, error = client.zcc.web_policy.activate_web_policy(
            ...     device_type='3',
            ...     policy_id='1',
            ... )
            >>> if error:
            ...     print(f"Error activating web policy: {error}")
            ...     return
            ... print(f"web policy Info activated successfully: {web_policy.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /web/policy/activate
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WebPolicy)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = WebPolicy(self.form_response_body(response.get_body()))
            else:
                result = WebPolicy()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def web_policy_edit(self, **kwargs) -> tuple:
        """
        Adds or updates a policy or app profile for the company by platform (iOS, Android, Windows, macOS, and Linux).

        Args:

        Returns:
            tuple: A tuple containing the updated Web Policy, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /web/policy/edit
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WebPolicy)
        if error:
            return (None, response, error)

        try:
            result = WebPolicy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_web_policy(self, policy_id: int) -> tuple:
        """
        Deletes the specified Web Policy.

        Args:
            policy_id (str): The unique identifier of the  Web Policy.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /web/policy/{policy_id}/delete
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
