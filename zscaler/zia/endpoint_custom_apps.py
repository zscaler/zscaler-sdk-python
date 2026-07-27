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
from zscaler.zia.models.dlp_endpoint_resource import DlpEndpointResource
from zscaler.zia.models.endpoint_applications_custom_apps import EndpointApplicationsCustomApps


class EndpointCustomAppsAPI(APIClient):
    """
    A Client object for the Endpoint Custom Apps resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_custom_apps(self, query_params: Optional[dict] = None) -> APIResult[List[EndpointApplicationsCustomApps]]:
        """
        Lists the custom endpoint applications configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against application names.
                ``[query_params.os_type]`` {str}: Filters the results by operating system (e.g.

        Returns:
            tuple: A tuple containing (list of EndpointApplicationsCustomApps instances, Response, error)

        Examples:
            List custom endpoint applications:

            >>> custom_app_list, _, error = client.zia.endpoint_custom_apps.list_custom_apps()
            >>> if error:
            ...     print(f"Error listing custom endpoint applications: {error}")
            ...     return
            ... print(f"Total custom endpoint applications found: {len(custom_app_list)}")
            ... for custom_app in custom_app_list:
            ...     print(custom_app.as_dict())

            List custom endpoint applications using filters:

            >>> custom_app_list, _, error = client.zia.endpoint_custom_apps.list_custom_apps(
            ...     query_params={'search': 'Example'})
            >>> if error:
            ...     print(f"Error listing custom endpoint applications: {error}")
            ...     return
            ... print(f"Total custom endpoint applications found: {len(custom_app_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/customApps
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

    def get_custom_app(self, app_id: int) -> APIResult[EndpointApplicationsCustomApps]:
        """
        Fetches a specific custom endpoint application by ID.

        Args:
            app_id (int): The unique identifier for the custom endpoint application.

        Returns:
            tuple: A tuple containing (EndpointApplicationsCustomApps instance, Response, error).

        Examples:
            Print a specific custom endpoint application:

            >>> fetched_custom_app, _, error = client.zia.endpoint_custom_apps.get_custom_app(1013)
            >>> if error:
            ...     print(f"Error fetching custom endpoint application by ID: {error}")
            ...     return
            ... print(f"Fetched custom endpoint application by ID: {fetched_custom_app.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/customApp/{app_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndpointApplicationsCustomApps)
        if error:
            return (None, response, error)

        try:
            result = EndpointApplicationsCustomApps(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_custom_app(self, **kwargs) -> APIResult[DlpEndpointResource]:
        """
        Creates a new custom endpoint application.

        Args:
            name (str): The name of the custom endpoint application.
            **kwargs: Optional keyword args.

        Keyword Args:
            resource_id (int): The resource id for this custom endpoint application.
            description (str): Additional information about the custom endpoint application.
            os_type (str): The os type for this custom endpoint application. Accepted values include e.g. ``ANY``.
            application_name (str): The application name for this custom endpoint application.
            bundle_id (str): The bundle id for this custom endpoint application.
            filename (str): The filename for this custom endpoint application.
            original_file_name (str): The original file name for this custom endpoint application.
            digitally_signed (bool): A Boolean value indicating whether digitally signed applies to this custom endpoint application.
            mod_uid (int): The mod uid for this custom endpoint application.
            application_type (str): The application type for this custom endpoint application. Accepted values include e.g. ``WELLKNOWN``.
            zapp_id (str): The zapp id for this custom endpoint application.
            deleted (bool): A Boolean value indicating whether deleted applies to this custom endpoint application.
            versions (list): The list of versions for this custom endpoint application.
            version (dict): The version configuration for this custom endpoint application.

        Returns:
            tuple: A tuple containing the newly added DlpEndpointResource instance, response, and error.

        Examples:
            Add a new custom endpoint application:

            >>> added_custom_app, _, error = client.zia.endpoint_custom_apps.add_custom_app(
            ...     name=f"NewCustomApp_{random.randint(1000, 10000)}",
            ...     description=f"NewCustomApp_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding custom endpoint application: {error}")
            ...     return
            ... print(f"Custom endpoint application added successfully: {added_custom_app.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/customApp
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DlpEndpointResource)
        if error:
            return (None, response, error)

        try:
            result = DlpEndpointResource(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_custom_app(self, app_id: int, **kwargs) -> APIResult[DlpEndpointResource]:
        """
        Updates information for the specified custom endpoint application.

        Args:
            app_id (int): The unique identifier for the custom endpoint application.

        Keyword Args:
            name (str): The name of the custom endpoint application.
            resource_id (int): The resource id for this custom endpoint application.
            description (str): Additional information about the custom endpoint application.
            os_type (str): The os type for this custom endpoint application. Accepted values include e.g. ``ANY``.
            application_name (str): The application name for this custom endpoint application.
            bundle_id (str): The bundle id for this custom endpoint application.
            filename (str): The filename for this custom endpoint application.
            original_file_name (str): The original file name for this custom endpoint application.
            digitally_signed (bool): A Boolean value indicating whether digitally signed applies to this custom endpoint application.
            mod_uid (int): The mod uid for this custom endpoint application.
            application_type (str): The application type for this custom endpoint application. Accepted values include e.g. ``WELLKNOWN``.
            zapp_id (str): The zapp id for this custom endpoint application.
            deleted (bool): A Boolean value indicating whether deleted applies to this custom endpoint application.
            versions (list): The list of versions for this custom endpoint application.
            version (dict): The version configuration for this custom endpoint application.

        Returns:
            tuple: A tuple containing the updated DlpEndpointResource instance, response, and error.

        Examples:
            Update an existing custom endpoint application:

            >>> updated_custom_app, _, error = client.zia.endpoint_custom_apps.update_custom_app(
            ...     app_id=1013,
            ...     name=f"UpdatedCustomApp_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedCustomApp_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating custom endpoint application: {error}")
            ...     return
            ... print(f"Custom endpoint application updated successfully: {updated_custom_app.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/customApp/{app_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DlpEndpointResource)
        if error:
            return (None, response, error)

        try:
            result = DlpEndpointResource(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_custom_app(self, app_id: int) -> APIResult[None]:
        """
        Deletes the specified custom endpoint application.

        Args:
            app_id (int): The unique identifier for the custom endpoint application.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a custom endpoint application:

            >>> _, _, error = client.zia.endpoint_custom_apps.delete_custom_app(1013)
            >>> if error:
            ...     print(f"Error deleting custom endpoint application: {error}")
            ...     return
            ... print(f"Custom endpoint application deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplications/customApp/{app_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
