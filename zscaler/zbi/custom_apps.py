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

from typing import Dict, List, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zbi.models.custom_apps import CustomApp


class CustomAppsAPI(APIClient):
    """
    A Client object for the Business Insights Custom Applications resource.

    Provides CRUD operations for managing custom applications used
    to track specific web traffic in Zscaler Business Insights.
    """

    _zbi_base_endpoint = "/bi/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_custom_apps(self, query_params: Optional[dict] = None) -> APIResult[List[CustomApp]]:
        """
        Retrieves all custom applications.

        Args:
            query_params (dict, optional): Map of query parameters.

                ``[query_params.id]`` (int): Optional Custom App ID
                to retrieve a specific app.

        Returns:
            tuple: (list of CustomApp instances, Response, error).

        Examples:
            List all custom apps::

                >>> apps, _, err = client.zbi.custom_apps.list_custom_apps()
                >>> if err:
                ...     print(f"Error: {err}")
                >>> for app in apps:
                ...     print(app.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /customapps
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
            results = [CustomApp(self.form_response_body(item)) for item in response.get_results()]
        except Exception as exc:
            return (None, response, exc)

        return (results, response, None)

    def get_custom_app(self, app_id: int) -> APIResult[CustomApp]:
        """
        Retrieves a specific custom application by ID.

        Args:
            app_id (int): The unique identifier of the custom application.

        Returns:
            tuple: (CustomApp instance, Response, error).

        Examples:
            Get a custom app by ID::

                >>> app, _, err = client.zbi.custom_apps.get_custom_app(101)
                >>> if err:
                ...     print(f"Error: {err}")
                >>> print(app.as_dict())
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /customapps
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params={"id": app_id})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result_list = response.get_results()
            if result_list:
                result = CustomApp(self.form_response_body(result_list[0]))
            else:
                result = None
        except Exception as exc:
            return (None, response, exc)

        return (result, response, None)

    def create_custom_app(self, **kwargs) -> APIResult[CustomApp]:
        """
        Creates a custom application.

        Args:
            name (str): The custom application name. Must be unique,
                max 128 characters.
            description (str): Description of the custom application.
                Max 1024 characters.
            signatures (list): List of signature dicts, each with
                ``type``, ``matchLevel``, and ``value`` keys.

        Returns:
            tuple: (CustomApp instance, Response, error).

        Examples:
            Create a custom app::

                >>> app, _, err = client.zbi.custom_apps.create_custom_app(
                ...     name="My App",
                ...     description="Tracks traffic",
                ...     signatures=[
                ...         {"type": "HOST", "matchLevel": "EXACT",
                ...          "value": "example.com"}
                ...     ]
                ... )
                >>> if err:
                ...     print(f"Error: {err}")
                >>> print(app.as_dict())
        """
        http_method = "POST"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /customapps
        """)
        body = kwargs
        headers = {"Content-Type": "application/json"}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result_list = response.get_results()
            if result_list:
                result = CustomApp(self.form_response_body(result_list[0]))
            else:
                result = CustomApp(self.form_response_body(response.get_body()))
        except Exception as exc:
            return (None, response, exc)

        return (result, response, None)

    def update_custom_app(self, app_id: int, **kwargs) -> APIResult[CustomApp]:
        """
        Updates a custom application by ID.

        Args:
            app_id (int): The unique identifier of the custom application.
            name (str): Updated name.
            description (str): Updated description.
            signatures (list): Updated list of signature dicts.

        Returns:
            tuple: (CustomApp instance, Response, error).

        Examples:
            Update a custom app::

                >>> app, _, err = client.zbi.custom_apps.update_custom_app(
                ...     101,
                ...     name="Updated App",
                ...     description="Updated description",
                ...     signatures=[
                ...         {"type": "HOST", "matchLevel": "EXACT",
                ...          "value": "updated.com"}
                ...     ]
                ... )
        """
        http_method = "PUT"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /customapps
            /{app_id}
        """)
        body = kwargs
        headers = {"Content-Type": "application/json"}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = CustomApp(self.form_response_body(response.get_body()))
        except Exception as exc:
            return (None, response, exc)

        return (result, response, None)

    def delete_custom_app(self, app_id: int) -> APIResult[int]:
        """
        Deletes a custom application by ID.

        Args:
            app_id (int): The unique identifier of the custom application
                to delete.

        Returns:
            tuple: (status_code, Response, error).

        Examples:
            Delete a custom app::

                >>> _, _, err = client.zbi.custom_apps.delete_custom_app(101)
                >>> if err:
                ...     print(f"Error: {err}")
        """
        http_method = "DELETE"
        api_url = format_url(f"""
            {self._zbi_base_endpoint}
            /customapps
            /{app_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.status, response, None)
