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
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.endpoint_applications_custom_apps import EndpointApplicationsCustomApps
from zscaler.zia.models.endpoint_applications_custom_apps_lite import EndpointApplicationsCustomAppsLite
from zscaler.zia.models.endpoint_applications_policies import EndpointApplicationsPolicies


class EndpointApplicationsAPI(APIClient):
    """
    A Client object for the Endpoint Applications resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_applications(self, query_params: Optional[dict] = None) -> APIResult[List[EndpointApplicationsCustomApps]]:
        """
        Lists the endpoint applications configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against application names.
                ``[query_params.os_type]`` {str}: Filters the results by operating system (e.g.
                ``[query_params.application_type]`` {str}: Filters the results by application type (e.g.

        Returns:
            tuple: A tuple containing (list of EndpointApplicationsCustomApps instances, Response, error)

        Examples:
            List endpoint applications:

            >>> application_list, _, error = client.zia.endpoint_applications.list_applications()
            >>> if error:
            ...     print(f"Error listing endpoint applications: {error}")
            ...     return
            ... print(f"Total endpoint applications found: {len(application_list)}")
            ... for application in application_list:
            ...     print(application.as_dict())

            List endpoint applications using filters:

            >>> application_list, _, error = client.zia.endpoint_applications.list_applications(
            ...     query_params={'search': 'Example'})
            >>> if error:
            ...     print(f"Error listing endpoint applications: {error}")
            ...     return
            ... print(f"Total endpoint applications found: {len(application_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications
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
                result.append(EndpointApplicationsCustomApps(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_applications_lite(
        self, query_params: Optional[dict] = None
    ) -> APIResult[List[EndpointApplicationsCustomAppsLite]]:
        """
        Lists a lightweight version of the endpoint applications.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against application names.
                ``[query_params.os_type]`` {str}: Filters the results by operating system (e.g.
                ``[query_params.application_type]`` {str}: Filters the results by application type (e.g.

        Returns:
            tuple: A tuple containing (list of EndpointApplicationsCustomAppsLite instances, Response, error)

        Examples:
            List endpoint applications:

            >>> application_list, _, error = client.zia.endpoint_applications.list_applications_lite()
            >>> if error:
            ...     print(f"Error listing endpoint applications: {error}")
            ...     return
            ... print(f"Total endpoint applications found: {len(application_list)}")
            ... for application in application_list:
            ...     print(application.as_dict())

            List endpoint applications using filters:

            >>> application_list, _, error = client.zia.endpoint_applications.list_applications_lite(
            ...     query_params={'search': 'Example'})
            >>> if error:
            ...     print(f"Error listing endpoint applications: {error}")
            ...     return
            ... print(f"Total endpoint applications found: {len(application_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/lite
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
                result.append(EndpointApplicationsCustomAppsLite(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_application_count(self, query_params: Optional[dict] = None) -> APIResult[dict]:
        """
        Retrieves the count of all endpoint applications.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against application names.
                ``[query_params.os_type]`` {str}: Filters the results by operating system.
                ``[query_params.application_type]`` {str}: Filters the results by application type.

        Returns:
            tuple: A tuple containing (int: the count of all endpoint applications, Response, error).

        Examples:
            >>> result, _, error = client.zia.endpoint_applications.get_application_count()
            >>> if error:
            ...     print(f"Error calling get_application_count: {error}")
            ...     return
            ... print(f"Result: {result}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/count
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
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_cloud_apps_count(self, query_params: Optional[dict] = None) -> APIResult[dict]:
        """
        Retrieves the count of well-known and discovered endpoint applications as determined by the Zscaler service.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against application names.
                ``[query_params.os_type]`` {str}: Filters the results by operating system.
                ``[query_params.application_type]`` {str}: Filters the results by application type.

        Returns:
            tuple: A tuple containing (int: the count of well-known and discovered endpoint applications, Response, error).

        Examples:
            >>> result, _, error = client.zia.endpoint_applications.get_cloud_apps_count()
            >>> if error:
            ...     print(f"Error calling get_cloud_apps_count: {error}")
            ...     return
            ... print(f"Result: {result}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/cloudApps/count
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
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_application_policies(self, query_params: Optional[dict] = None) -> APIResult[List[EndpointApplicationsPolicies]]:
        """
        Lists the policy rules currently associated with the endpoint application(s) identified by the given resource IDs.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.resourceId]`` {list}: One or more endpoint application resource IDs (repeated query parameter).

        Returns:
            tuple: A tuple containing (list of EndpointApplicationsPolicies instances, Response, error)

        Examples:
            List endpoint applications:

            >>> application_list, _, error = client.zia.endpoint_applications.get_application_policies()
            >>> if error:
            ...     print(f"Error listing endpoint applications: {error}")
            ...     return
            ... print(f"Total endpoint applications found: {len(application_list)}")
            ... for application in application_list:
            ...     print(application.as_dict())

            List endpoint applications using filters:

            >>> application_list, _, error = client.zia.endpoint_applications.get_application_policies(
            ...     query_params={'resourceId': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing endpoint applications: {error}")
            ...     return
            ... print(f"Total endpoint applications found: {len(application_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/policies
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
                result.append(EndpointApplicationsPolicies(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_categories_with_non_empty_apps(self, query_params: Optional[dict] = None) -> APIResult[list]:
        """
        Lists the categories that currently have endpoint applications grouped within them.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against application names.
                ``[query_params.os_type]`` {str}: Filters the results by operating system.

        Returns:
            tuple: A tuple containing (list of category name strings, Response, error)

        Examples:
            List endpoint applications:

            >>> application_list, _, error = client.zia.endpoint_applications.list_categories_with_non_empty_apps()
            >>> if error:
            ...     print(f"Error listing endpoint applications: {error}")
            ...     return
            ... print(f"Total endpoint applications found: {len(application_list)}")
            ... for application in application_list:
            ...     print(application.as_dict())

            List endpoint applications using filters:

            >>> application_list, _, error = client.zia.endpoint_applications.list_categories_with_non_empty_apps(
            ...     query_params={'search': 'Example'})
            >>> if error:
            ...     print(f"Error listing endpoint applications: {error}")
            ...     return
            ... print(f"Total endpoint applications found: {len(application_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/getCategoriesWithNonEmptyApps
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
            result = response.get_results()
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
