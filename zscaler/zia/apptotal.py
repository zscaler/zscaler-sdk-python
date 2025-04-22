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
from zscaler.zia.models.apptotal import AppTotal
from zscaler.zia.models.apptotal import AppTotalSearch
from zscaler.utils import format_url


class AppTotalAPI(APIClient):
    """
    A Client object for the predefined and custom Cloud Applications resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_app(self, app_id: str, verbose: bool = False) -> tuple:
        """
        Searches the AppTotal App Catalog by app ID. If the app exists in the catalog, the app's information is
        returned. If not, the app is submitted for analysis. After analysis is complete, a subsequent GET request is
        required to fetch the app's information.

        Args:
            app_id (str): The app ID to search for.
            verbose (bool, optional): Defaults to False.

        Returns:
            tuple: A tuple containing the AppTotal object and the response object.

        Examples:
            Return verbose information on an app with ID 12345::

                zia.apptotal.get_app(app_id="12345", verbose=True)

        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/apps/app")

        # Pass app_id and verbose as query parameters
        query_params = {"appId": app_id, "verbose": str(verbose).lower()}  # API may expect 'true' or 'false' in lowercase

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppTotal)

        if error:
            return (None, response, error)

        try:
            result = AppTotal(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def scan_app(self, app_id: str) -> tuple:
        """
        Submits an app for analysis in the AppTotal Sandbox. After analysis is complete, a subsequent GET request is
        required to fetch the app's information.

        Args:
            app_id (str): The app ID to scan.

        Returns:
            tuple: The response object.

        Examples:
            Scan an app with ID 12345::

                zia.apptotal.scan_app(app_id="12345")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /apps/app
        """
        )

        payload = {
            "appId": app_id,
        }

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppTotal)

        if error:
            return (None, response, error)

        try:
            result = AppTotal(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def search_app(self, app_name: str) -> tuple:
        """
        Searches for an app by name. Any app whose name contains the search term (app_name) is returned.
        Note: The maximum number of results that are returned is 200.

        Args:
            app_name (str): The app name to search for.

        Returns:
            tuple: A tuple containing the AppTotalSearch object and the response object.

        Examples:
            Search for an app by name "Slack"::

                zia.apptotal.search_app(app_name="Slack")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /apps/search
        """
        )

        query_params = {
            "appName": app_name,
        }

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppTotalSearch)

        if error:
            return (None, response, error)

        try:
            result = AppTotalSearch(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def app_views(self, app_view_id: str) -> tuple:
        """
        Searches for an app by name. Any app whose name contains the search term (app_name) is returned.
        Note: The maximum number of results that are returned is 200.

        Args:
            app_name (str): The app name to search for.

        Returns:
            tuple: A tuple containing the AppTotalSearch object and the response object.

        Examples:
            Search for an app by name "Slack"::

                zia.apptotal.search_app(app_name="Slack")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /app_views/{app_view_id}/apps
        """
        )

        query_params = {
            "appViewId": app_view_id,
        }

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AppTotalSearch)

        if error:
            return (None, response, error)

        try:
            result = AppTotalSearch(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
