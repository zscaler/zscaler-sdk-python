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
from zscaler.zpa.models.posture_profiles import PostureProfile
from zscaler.utils import format_url


class PostureProfilesAPI(APIClient):
    """
    A Client object for the Posture Profiles resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_posture_profiles(self, query_params: Optional[dict] = None) -> List[PostureProfile]:
        """
        Returns a list of all configured posture profiles.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[PostureProfile]: A list of PostureProfile instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     profiles = client.zpa.posture_profiles.list_posture_profiles()
            ...     for profile in profiles:
            ...         print(profile.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_v2}/posture")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        response = self._request_executor.execute(request, PostureProfile)

        return [PostureProfile(self.form_response_body(item)) for item in response.get_results()]

    def get_profile(self, profile_id: str) -> PostureProfile:
        """
        Gets a specific posture profile by its unique ID.

        Args:
            profile_id (str): The unique identifier of the posture profile.

        Returns:
            PostureProfile: The posture profile object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     profile = client.zpa.posture_profiles.get_profile('999999')
            ...     print(profile.posture_udid)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/posture/{profile_id}")

        request = self._request_executor.create_request(http_method, api_url, {}, {})
        response = self._request_executor.execute(request, PostureProfile)

        return PostureProfile(self.form_response_body(response.get_body()))
