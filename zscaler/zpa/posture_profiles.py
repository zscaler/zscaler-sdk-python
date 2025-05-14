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
from zscaler.zpa.models.posture_profiles import PostureProfile
from zscaler.utils import format_url, remove_cloud_suffix


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

    def list_posture_profiles(self, query_params=None) -> tuple:
        """
        Returns a list of all configured posture profiles.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            list: A list of `PostureProfile` instances.

        Examples:
            Retrieve posture profiles with pagination parameters:

            >>> posture_list, _, err = client.zpa.posture_profile.list_posture_profiles(
            ... query_params={'search': 'pra_console01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing posture: {err}")
            ...     return
            ... print(f"Total posture profiles found: {len(posture_list)}")
            ... for posture in posture_list:
            ...     print(posture.as_dict())

            Retrieve posture profiles udid with:

            >>> posture_list, _, err = client.zpa.posture_profile.list_posture_profiles()
            ... if err:
            ...     print(f"Error listing profiles: {err}")
            ...     return
            ... print("Extracted posture_udid values:")
            ... for profile in profile_list:
            ...     if profile.posture_udid:
            ...         print(profile.posture_udid)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /posture
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PostureProfile)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PostureProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_profile(self, profile_id: str) -> tuple:
        """
        Gets a specific posture profile by its unique ID.

        Args:
            profile_id (str): The unique identifier of the posture profile.

        Returns:
            :obj:`Tuple`: A tuple containing (list of Posture Profile instances, Response, error)

        Examples:
            >>> fetched_posture, _, err = client.zpa.posture_profile.get_profile('999999')
            ... if err:
            ...     print(f"Error fetching posture by ID: {err}")
            ...     return
            ... print(fetched_profile.posture_udid)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /posture/{profile_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PostureProfile)

        if error:
            return (None, response, error)

        try:
            result = PostureProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
