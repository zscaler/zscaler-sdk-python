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
from zscaler.zdx.models.users import Users
from zscaler.zdx.models.users import UserDetails
from zscaler.utils import format_url, zdx_params


class UsersAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zdx_base_endpoint = "/zdx/v1"

    @zdx_params
    def list_users(self, query_params=None) -> tuple:
        """
        Returns a list of all active users configured within the ZDX tenant.

        Keyword Args:
        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.location_id]`` {list}: The unique ID for the location. You can add multiple location IDs.

                ``[query_params.exclude_loc]`` {list}: The location IDs. You can exclude multiple location IDs.

                ``[query_params.department_id]`` {list}: The unique ID for the department. You can add multiple location IDs.

                ``[query_params.exclude_dept]`` {list}: The department IDs. You can exclude multiple department IDs.

                ``[query_params.geo_id]`` {list}: The unique ID for the geolocation. You can add multiple location IDs.

                ``[query_params.offset]`` {str}: The next_offset value from the last request.
                    You must enter this value to get the next batch from the list.
                    When the next_offset value becomes null, the list is complete.

                ``[query_params.limit]`` {int}: The number of items that must be returned per request from the list.
                    Minimum: 1

        Returns:
            :obj:`Tuple`: The list of users in ZDX.

        Examples:
            List all users in ZDX for the past 2 hours:

            >>> user_list, _, err = client.zdx.users.list_users()
            ... if err:
            ...     print(f"Error listing users: {err}")
            ...     return
            ... for user in user_list:
            ...     print(user)

            List all users in ZDX for the past 2 hours:

            >>> user_list, _, err = client.zdx.users.list_users(query_params={"since": 2})
            ... if err:
            ...     print(f"Error listing users: {err}")
            ...     return
            ... for user in user_list:
            ...     print(user)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /users
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
            parsed_response = self.form_response_body(response.get_body())
            users_list = parsed_response.get("users", [])
            result = [UserDetails(user) for user in users_list]

        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_user(self, user_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified user configured within the ZDX tenant.

        Args:
            user_id (str): The unique ID for the ZDX user.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.

        Returns:
            :obj:`Tuple`: The user information.

        Examples:
            Return information on the user with the ID of 999999999:

            >>> user_details, _, err = client.zdx.users.get_user('24328827')
            ... if err:
            ...     print(f"Error listing user details: {err}")
            ...     return
            ... for user in user_details:
            ...     print(user)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /users/{user_id}
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
            result = [UserDetails(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
