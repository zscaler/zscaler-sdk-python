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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.http_header_control import HttpHeaderActionProfile, HttpHeaderProfile


class HttpHeaderControlAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_http_header_action_profiles(
        self, query_params=None) -> APIResult[List[HttpHeaderActionProfile]]:
        """
        List http_header_action_profiles.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of HttpHeaderActionProfile instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderActionProfile
        """)

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(
            http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            result = []
            for item in response.get_results():
                result.append(HttpHeaderActionProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_http_header_action_profile(self, **kwargs) -> APIResult[HttpHeaderActionProfile]:
        """
        Adds a new http_header_action_profile.

        Returns:
            tuple: The newly created http_header_action_profile resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderActionProfile
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, HttpHeaderActionProfile)
        if error:
            return (None, response, error)
        try:
            result = HttpHeaderActionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_http_header_action_profile(self, profile_id: int, **kwargs) -> APIResult[HttpHeaderActionProfile]:
        """
        Updates an existing http_header_action_profile.

        Args:
            profile_id (int): The unique ID for the http_header_action_profile being updated.

        Keyword Args:
            slot_id (int): The slot ID assigned to the action profile. This value is required by the API
                and cannot be 0. If omitted, it is automatically resolved from the existing profile (the SDK
                lists the action profiles and matches on ``profile_id``), so callers normally do not need to set it.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated http_header_action_profile resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderActionProfile/{profile_id}
        """)

        body = kwargs

        # ``slotId`` is required by the PUT endpoint and cannot be 0. There is no
        # get-by-id endpoint, so when the caller does not supply it, look it up by
        # listing all action profiles and matching on the profile ID.
        if not body.get("slot_id") and not body.get("slotId"):
            profiles, _, list_error = self.list_http_header_action_profiles()
            if list_error:
                return (None, None, list_error)
            for profile in profiles or []:
                if str(profile.id) == str(profile_id):
                    body["slot_id"] = profile.slot_id
                    break

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, HttpHeaderActionProfile)
        if error:
            return (None, response, error)
        try:
            result = HttpHeaderActionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_http_header_action_profile(self, profile_id: int) -> APIResult[None]:
        """
        Deletes the specified http_header_action_profile.

        Args:
            profile_id (int): The unique identifier for the http_header_action_profile.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderActionProfile/{profile_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def list_http_header_profiles(self, query_params=None) -> APIResult[List[HttpHeaderProfile]]:
        """
        Retrieves a list of HTTP header profiles.

        Returns:
            tuple: (list of HttpHeaderProfile instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderProfile
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
                result.append(HttpHeaderProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_http_header_profile(self, **kwargs) -> APIResult[HttpHeaderProfile]:
        """
        Adds a new HTTP header insertion profile.

        Args:
            name (str): The HTTP header profile name.

        Keyword Args:
            description (str): Additional information about the HTTP header profile.
            slot_id (int): The slot ID assigned to the HTTP header profile.
            profile_ready_for_use (bool): Indicates whether the HTTP header profile is ready for use.
            http_header_profile_criteria (list[dict]): The list of matching criteria evaluated by the profile.
                Each criterion supports:

                ``header`` {str}: The header evaluated by the criteria.
                    Supported Values: `USERAGENT`, `REFERER`, `ORIGIN`
                ``operator`` {str}: The operator applied to the header criteria.
                    Supported Values: `UAVERSIONGT`, `UAVERSIONLT`, `UAVERSIONEQ`, `UAVERSIONNEQ`, `UAVERSIONANY`
                ``user_agent`` {str}: The user agent evaluated by the criteria.
                ``user_agent_bitmap`` {str}: The user agent bitmap evaluated by the criteria.
                    Supported Values: `OPERA`, `FIREFOX`, `MSIE`, `MSEDGE`, `CHROME`, `SAFARI`, `OTHER`,
                    `MSCHREDGE`, `BRAVE`
                ``user_agent_version`` {str}: The user agent version evaluated by the criteria.
                ``category_bitmap`` {list[str]}: The URL category bitmap evaluated by the criteria.
                ``cloud_app_bitmap`` {list[str]}: The cloud application bitmap evaluated by the criteria.

        Returns:
            tuple: The newly created HTTP header profile resource record.

        Examples:
            Add an HTTP header profile with ORIGIN, REFERER, and USERAGENT criteria::

                >>> added_profile, _, err = client.zia.http_header_control.add_http_header_profile(
                ...     name=f"Profile01_{random.randint(1000, 10000)}",
                ...     description="Example header profile",
                ...     http_header_profile_criteria=[
                ...         {
                ...             "header": "ORIGIN",
                ...             "cloud_app_bitmap": ["CHATGPT_AI"],
                ...             "category_bitmap": ["GENERAL_AI_ML", "AI_ML_APPS"],
                ...         },
                ...         {
                ...             "header": "REFERER",
                ...             "cloud_app_bitmap": ["CHATGPT_AI"],
                ...             "category_bitmap": ["GENERAL_AI_ML", "AI_ML_APPS"],
                ...         },
                ...         {
                ...             "header": "USERAGENT",
                ...             "user_agent_bitmap": "FIREFOX",
                ...             "operator": "UAVERSIONEQ",
                ...             "user_agent_version": "123.0",
                ...         },
                ...     ],
                ... )
                >>> if err:
                ...     print(f"Error adding profile: {err}")
                ...     return
                >>> print(f"Profile added successfully: {added_profile.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderProfile
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, HttpHeaderProfile)
        if error:
            return (None, response, error)
        try:
            result = HttpHeaderProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_http_header_profile(self, profile_id: int, **kwargs) -> APIResult[HttpHeaderProfile]:
        """
        Updates the HTTP header profile based on the specified ID.

        Args:
            profile_id (int): The unique ID for the HTTP header profile being updated.

        Keyword Args:
            name (str): The HTTP header profile name.
            description (str): Additional information about the HTTP header profile.
            slot_id (int): The slot ID assigned to the HTTP header profile. This value is required by the API
                and cannot be 0. If omitted, it is automatically resolved from the existing profile (the SDK
                lists the profiles and matches on ``profile_id``), so callers normally do not need to set it.
            profile_ready_for_use (bool): Indicates whether the HTTP header profile is ready for use.
            http_header_profile_criteria (list[dict]): The list of matching criteria evaluated by the profile.
                See :meth:`add_http_header_profile` for the full list of supported criterion fields and values.

        Returns:
            tuple: The updated HTTP header profile resource record.

        Examples:
            Update the name, description, and criteria of an existing HTTP header profile::

                >>> updated_profile, _, err = client.zia.http_header_control.update_http_header_profile(
                ...     profile_id='12345',
                ...     name=f"UpdatedProfile_{random.randint(1000, 10000)}",
                ...     description="Updated header profile",
                ...     http_header_profile_criteria=[
                ...         {
                ...             "header": "USERAGENT",
                ...             "user_agent_bitmap": "CHROME",
                ...             "operator": "UAVERSIONGT",
                ...             "user_agent_version": "120.0",
                ...         },
                ...     ],
                ... )
                >>> if err:
                ...     print(f"Error updating profile: {err}")
                ...     return
                >>> print(f"Profile updated successfully: {updated_profile.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderProfile/{profile_id}
        """)

        body = kwargs

        # ``slotId`` is required by the PUT endpoint and cannot be 0. There is no
        # get-by-id endpoint, so when the caller does not supply it, look it up by
        # listing all profiles and matching on the profile ID.
        if not body.get("slot_id") and not body.get("slotId"):
            profiles, _, list_error = self.list_http_header_profiles()
            if list_error:
                return (None, None, list_error)
            for profile in profiles or []:
                if str(profile.id) == str(profile_id):
                    body["slot_id"] = profile.slot_id
                    break

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, HttpHeaderProfile)
        if error:
            return (None, response, error)
        try:
            result = HttpHeaderProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_http_header_profile(self, profile_id: int) -> APIResult[None]:
        """
        Deletes the HTTP header profile based on the specified ID

        Args:
            profile_id (int): The unique identifier for the HTTP header profile.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderProfile/{profile_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
