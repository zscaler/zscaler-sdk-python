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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zcc.models.custom_ip_base_apps import CustomIpBaseApps
from zscaler.utils import format_url
from zscaler.types import APIResult


class CustomIPBasedAppsAPI(APIClient):

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def get_custom_ip_base_apps(self) -> APIResult[dict]:
        """
        Retrieves the list of custom IP-based applications.

        Args:
            query_params (dict, optional): A dictionary containing supported filters.

                ``[query_params.page]`` {str}: Specifies the page offset.

                ``[query_params.page_size]`` {str}: Specifies the page size. The default size is 50.

                ``[query_params.search]`` {str}: The search string used to match against the policies.

        Returns:
            :obj:`list`: Retrieves the list of custom IP-based applications.

        Examples:
            Prints all custom IP-based applications:

            >>> apps_list, _, err = client.zcc.custom_ip_base_apps.get_custom_ip_base_apps()
            >>> if err:
            ...     print(f"Error listing custom IP-based applications: {err}")
            ...     return
            ... for app in apps_list:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /custom-ip-based-apps
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
            response_body = response.get_body() or {}
            items = response_body.get("customAppContracts", []) or []
            result = [CustomIpBaseApps(item) for item in items if isinstance(item, dict)]
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_custom_ip_base_app(self, app_id: str) -> APIResult[dict]:
        """
        Retrieves the custom IP-based application using app ID.

        Args:
            app_id (str): The unique identifier of the custom IP-based application.

        Returns:
            :obj:`list`: Retrieves the custom IP-based application.

        Examples:
            Prints the custom IP-based application:

            >>> app, _, err = client.zcc.custom_ip_base_apps.get_custom_ip_base_app('1234567890')
            >>> if err:
            ...     print(f"Error listing custom IP-based application: {err}")
            ...     return
            ... print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /custom-ip-based-apps/{app_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CustomIpBaseApps)
        if error:
            return (None, response, error)

        try:
            result = CustomIpBaseApps(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
