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

from zscaler.request_executor import RequestExecutor
from zscaler.api_client import APIClient
from zscaler.zia.models.cloud_app_instances import CloudApplicationInstances
from zscaler.utils import format_url


class CloudApplicationInstancesAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_cloud_app_instances(
        self,
        query_params=None,
    ) -> tuple:
        """
        Retrieves the list of cloud application instances configured in the ZIA Admin Portal

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.instance_name]`` {str}: The cloud application instance name

                ``[query_params.instance_type]`` {bool}: The cloud application instance type
                    Supported values: `SHAREPOINTONLINE`, `ONEDRIVE`, `BOXNET`, `OKTA`, `APPSPACE`,
                        `BITBUCKET`, `GITHUB`, `SLACK`, `QUICK_BASE`, `ZEPLIN`, `SOURCEFORGE`, `ZOOM`,
                        `WORKDAY`, `GDRIVE`, `GOOGLE_WEBMAIL`, `WINDOWS_LIVE_HOTMAIL`, `MSTEAM`

                ``[query_params.page]`` (int): Specifies the page offset.

                ``[query_params.page_size]`` (int): Specifies the page size.

        Returns:
            tuple: A tuple containing (list of Cloud application instances, Response, error)

        Examples:
            Print all Cloud application instances

            >>> instance_list, _, error = client.zia.cloud_app_instances.list_cloud_app_instances()
            >>> if error:
            ...     print(f"Error listing cloud application instances: {error}")
            ...     return
            ... print(f"Total cloud application instances found: {len(instance_list)}")
            ... for app in instance_list:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudApplicationInstances
        """
        )

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
                result.append(CloudApplicationInstances(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_cloud_app_instances(self, instance_id: int) -> tuple:
        """
        Retrieves information about a cloud application instance based on the specified ID

        Args:
            instance_id (int): The unique identifier for the cloud application instance.

        Returns:
            tuple: A tuple containing (cloud application instance, Response, error).

        Examples:
            Print a specific Cloud application instances

            >>> fetched_instance, _, error = client.zia.cloud_app_instances.get_cloud_app_instances(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching cloud application instance by ID: {error}")
            ...     return
            ... print(f"Fetched cloud application instance by ID: {fetched_instance.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudApplicationInstances/{instance_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CloudApplicationInstances)
        if error:
            return (None, response, error)

        try:
            result = CloudApplicationInstances(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_cloud_app_instances(self, **kwargs) -> tuple:
        """
        Add a new cloud application instance.

        Args:
            instance_id (str): Cloud application instance ID.
            instance_type (str): Cloud application instance type.
                Supported values: SHAREPOINTONLINE, ONEDRIVE, BOXNET, OKTA, APPSPACE,
                BITBUCKET, GITHUB, SLACK, QUICK_BASE, ZEPLIN, SOURCEFORGE, ZOOM,
                WORKDAY, GDRIVE, GOOGLE_WEBMAIL, WINDOWS_LIVE_HOTMAIL, MSTEAM.
            instance_name (str): Cloud application instance name.
            instance_identifiers (list): List of instance identifiers. Each identifier must include:
                * instance_identifier (str): URL, IP address, or keyword.
                * instance_identifier_name (str): Name of the identifier.
                * instance_type (str): Type of identifier (URL, REFURL, or KEYWORD).

        Returns:
            tuple: A tuple containing:
                - CloudApplicationInstances: The newly added instance.
                - Response: The raw API response object.
                - Error: An error message, if applicable.

        Examples:
            Add a new cloud application instance

            >>> added_instance, _, error = client.zia.cloud_app_instances.add_cloud_app_instances(
            ...     instance_name=f"Instance01_{random.randint(1000, 10000)}",
            ...     instance_type='SHAREPOINTONLINE',
            ...     instance_identifiers=[
            ...         {
            ...             "instance_identifier_name": 'instance01',
            ...             "instance_identifier": 'instance01.sharepoint.com',
            ...             "identifier_type": 'URL',
            ...         }
            ...     ]
            ... )
            >>> if error:
            ...     print(f"Error adding cloud application instance: {error}")
            ...     return
            ... print(f"cloud application instance added successfully: {added_instance.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudApplicationInstances
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CloudApplicationInstances)
        if error:
            return (None, response, error)

        try:
            result = CloudApplicationInstances(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_cloud_app_instances(self, instance_id: int, **kwargs) -> tuple:
        """
        Updates information about a cloud application instance based on the specified ID

        Args:
            instance_id (int): The unique ID for the cloud application instance.

        Returns:
            tuple: A tuple containing the updated cloud application instance, response, and error.

        Examples:
            Update a cloud application instance

            >>> updated_instance, _, error = client.zia.cloud_app_instances.add_cloud_app_instances(
            ...     instance_id='458554'
            ...     instance_name=f"Instance01_{random.randint(1000, 10000)}",
            ...     instance_type='SHAREPOINTONLINE',
            ...     instance_identifiers=[
            ...         {
            ...             "instance_identifier_name": 'instance01',
            ...             "instance_identifier": 'instance01.sharepoint.com',
            ...             "identifier_type": 'URL',
            ...         }
            ...     ]
            ... )
            >>> if error:
            ...     print(f"Error updating cloud application instance: {error}")
            ...     return
            ... print(f"cloud application instance updated successfully: {updated_instance.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudApplicationInstances/{instance_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CloudApplicationInstances)
        if error:
            return (None, response, error)

        try:
            result = CloudApplicationInstances(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_cloud_app_instances(self, instance_id: int) -> tuple:
        """
        Deletes a cloud application instance based on the specified ID

        Args:
            instance_id (str): The unique identifier of the cloud application instance.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a specific Cloud application instances

            >>> _, _, error = client.zia.cloud_app_instances.delete_cloud_app_instances(
                '1254654')
            >>> if error:
            ...     print(f"Error deleting cloud application instance: {error}")
            ...     return
            ... print(f"cloud application instance with ID {'1254654'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudApplicationInstances/{instance_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
