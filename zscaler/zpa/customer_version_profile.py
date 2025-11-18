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
from zscaler.zpa.models.customer_version_profile import CustomerVersionProfile
from zscaler.utils import format_url
from zscaler.types import APIResult


class CustomerVersionProfileAPI(APIClient):
    """
    A Client object for the Customer Version Profile resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_version_profiles(self, query_params: Optional[dict] = None) -> APIResult[List[CustomerVersionProfile]]:
        """
        Returns a list of all visible version profiles.

        Args:
            **kwargs: Optional keyword args.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of Customer Profiles instances, Response, error)

        Examples:
            List all visibile version profiles:

        Examples:
            >>> version_list, _, err = client.zpa.customer_version_profile.list_version_profiles(
            ... query_params={'search': 'Default', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing version profiles: {err}")
            ...     return
            ... print(f"Total version profiles found: {len(version_list)}")
            ... for pra in version_list:
            ...     print(pra.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /visible/versionProfiles
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CustomerVersionProfile)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CustomerVersionProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_associated_version_profile(self) -> APIResult[CustomerVersionProfile]:
        """
        Get associated version profile for a customer.

        This endpoint retrieves the version profile associated with the customer.
        The API does not require any parameters.

        Returns:
            :obj:`Tuple`: A tuple containing (CustomerVersionProfile instance, Response, error)

        Examples:
            Get associated version profile for a customer:

            >>> version_profile, _, err = client.zpa.customer_version_profile.get_associated_version_profile()
            ... if err:
            ...     print(f"Error getting associated version profile: {err}")
            ...     return
            ... print(version_profile.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /versionProfile
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CustomerVersionProfile)
        if error:
            return (None, response, error)

        try:
            result = CustomerVersionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_version_profile(self, profile_id: str, remove_override_flag: bool) -> APIResult[None]:
        """
        Update the version profile for a given customer.

        This endpoint allows you to update the version profile for a given customer.
        The API requires the `remove_override_flag` attribute to be passed in the body.

        Args:
            profile_id (str): The unique identifier for the version profile.
            remove_override_flag (bool): Whether to remove the override flag for the version profile.

        Returns:
            :obj:`Tuple`: A tuple containing None (API returns 204 No Content), response object, and error if any.

            Note: This API returns 204 No Content on success, so the result will be None. To get the
            updated version profile, call `get_associated_version_profile()` after this operation.

        Examples:
            >>> updated_profile, _, err = client.zpa.customer_version_profile.update_version_profile(
            ...     profile_id='0',
            ...     remove_override_flag=True
            ... )
            ... if err:
            ...     print(f"Error updating version profile: {err}")
            ...     return
            ... print(f"Version profile updated: {updated_profile.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /versionProfiles/{profile_id}
        """
        )

        body = {"removeOverrideFlag": remove_override_flag}

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
