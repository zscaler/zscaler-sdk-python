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
from zscaler.utils import format_url
from zscaler.zia.models.cloud_app_policy import CloudApplicationPolicy


class CloudApplicationsAPI(APIClient):
    """
    A Client object for the Cloud Applications resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_cloud_app_policy(self, query_params=None) -> tuple:
        """
        Return a list of of Predefined and User Defined Cloud Applications associated with the DLP rules,
        Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Filter application by name

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 200, but the maximum size is 1000.

                ``[query_params.app_class]`` {str}: Filter application by application category

                ``[query_params.group_results]`` {bool}: Show count of applications grouped by application category

        Returns:
            tuple: A tuple containing (list of Cloud Application Policies instances, Response, error)


        Examples:
            Get a list of all cloud application policies:

            >>> applications_list, response, error = client.zia.cloud_applications.list_cloud_app_policy()
            ... if error:
            ...     print(f"Error listing applications list: {error}")
            ...     return
            ... print(f"Total applications found: {len(applications_list)}")
            ... for app in applications_list:
            ...     print(app.as_dict())

            Get a list of cloud application policies using pagination and application class:

            >>> applications_list, response, error = client.zia.cloud_applications.list_cloud_app_policy(
                query_params={"app_class": "WEB_MAIL", 'page': 1, 'page_size': 10})
            ... if error:
            ...     print(f"Error listing applications list: {error}")
            ...     return
            ... print(f"Total applications found: {len(applications_list)}")
            ... for app in applications_list:
            ...     print(app.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudApplications/policy
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
            result = []
            for item in response.get_results():
                result.append(CloudApplicationPolicy(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_cloud_app_ssl_policy(self, query_params=None) -> tuple:
        """
        Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.
        Retrives AppInfo when groupResults is set to false and retrieves the application count grouped by application
        category when groupResults is set to true.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Filter application by name

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size
                    The default size is 200, but the maximum size is 1000.

                ``[query_params.app_class]`` {str}: Filter application by application category.

                ``[query_params.group_results]`` {bool}: Show count of applications grouped by application category

        Returns:
            tuple: A tuple containing (list of Cloud Application SSL Policies instances, Response, error)

        Examples:
            Get a list of all cloud application policies:

            >>> applications_list, response, error = client.zia.cloud_applications.list_cloud_app_policy()
            ... if error:
            ...     print(f"Error listing applications list: {error}")
            ...     return
            ... print(f"Total applications found: {len(applications_list)}")
            ... for app in applications_list:
            ...     print(app.as_dict())

            Get a list of cloud application policies using pagination and application class:

            >>> applications_list, response, error = client.zia.cloud_applications.list_cloud_app_policy(
                query_params={"app_class": "WEB_MAIL", 'page': 1, 'page_size': 10})
            ... if error:
            ...     print(f"Error listing applications list: {error}")
            ...     return
            ... print(f"Total applications found: {len(applications_list)}")
            ... for app in applications_list:
            ...     print(app.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudApplications/sslPolicy
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
            result = []
            for item in response.get_results():
                result.append(CloudApplicationPolicy(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
