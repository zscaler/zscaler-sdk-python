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

    def list_http_header_action_profiles(self, query_params=None) -> APIResult[List[HttpHeaderActionProfile]]:
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
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

    def update_http_header_action_profile(
        self, http_header_action_profile_id: int, **kwargs
    ) -> APIResult[HttpHeaderActionProfile]:
        """
        Updates an existing http_header_action_profile.

        Args:
            http_header_action_profile_id (int): The unique ID for the http_header_action_profile being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated http_header_action_profile resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderActionProfile/{http_header_action_profile_id}
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

    def delete_http_header_action_profile(self, http_header_action_profile_id: int) -> APIResult[None]:
        """
        Deletes the specified http_header_action_profile.

        Args:
            http_header_action_profile_id (int): The unique identifier for the http_header_action_profile.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderActionProfile/{http_header_action_profile_id}
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
        List http_header_profiles.

        Args:
            query_params (dict): Map of query parameters for the request.

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
        Adds a new http_header_profile.

        Returns:
            tuple: The newly created http_header_profile resource record.
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

    def update_http_header_profile(self, http_header_profile_id: int, **kwargs) -> APIResult[HttpHeaderProfile]:
        """
        Updates an existing http_header_profile.

        Args:
            http_header_profile_id (int): The unique ID for the http_header_profile being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated http_header_profile resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderProfile/{http_header_profile_id}
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

    def delete_http_header_profile(self, http_header_profile_id: int) -> APIResult[None]:
        """
        Deletes the specified http_header_profile.

        Args:
            http_header_profile_id (int): The unique identifier for the http_header_profile.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /httpHeaderProfile/{http_header_profile_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
