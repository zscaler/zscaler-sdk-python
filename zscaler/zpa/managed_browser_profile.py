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
from zscaler.zpa.models.managed_browser_profile import ManagedBrowserProfile
from zscaler.utils import format_url
from zscaler.types import APIResult


class ManagedBrowserProfileAPI(APIClient):
    """
    A Client object for the Managed Browser Profile resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_managed_browser_profiles(self, query_params: Optional[dict] = None) -> APIResult[List[ManagedBrowserProfile]]:
        """
        Gets all the managed browser profiles for a customer

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            tuple: A tuple containing (list of ManagedBrowserProfile instances, Response, error)

        Examples:
            Retrieve machine groups with pagination parameters:

            >>> profile_list, _, err = client.zpa.managed_browser_profile.list_managed_browser_profiles(
            ... query_params={'search': 'Profile01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing managed browser profiles: {err}")
            ...     return
            ... print(f"Total managed browser profiles found: {len(profile_list)}")
            ... for profile in profile_list:
            ...     print(profile.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /managedBrowserProfile/search
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ManagedBrowserProfile)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ManagedBrowserProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
