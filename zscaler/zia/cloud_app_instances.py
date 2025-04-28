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
                        `WORKDAY`, `GDRIVE`, `GOOGLE_WEBMAIL`, `WINDOWS_LIVE_HOTMAIL`, `MSTEAM"

                ``[query_params.page]`` (int): Specifies the page offset.

                ``[query_params.page_size]`` (int): Specifies the page size. The default size is 255.

        Returns:
            tuple: A tuple containing (list of Device Group instances, Response, error)

        Examples:
            Print all device groups

            >>> for device group in zia.device_management.list_device_groups():
            ...    pprint(device)

            Print Device Groups that match the name or description 'Windows'

            >>> pprint(zia.device_management.list_device_groups('Windows'))

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

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CloudApplicationInstances(
                    self.form_response_body(item))
                )
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

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, CloudApplicationInstances)
        if error:
            return (None, response, error)

        try:
            result = CloudApplicationInstances(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_cloud_app_instances(self, **kwargs) -> tuple:
        """
        Add a new cloud application instance.

        Args:
            instance_id(str): Cloud application instance ID
            instance_type (str): Cloud application instance type
                Supported Values: `SHAREPOINTONLINE`, `ONEDRIVE`, `BOXNET`, `OKTA`,
                    `APPSPACE`, `BITBUCKET`, `GITHUB`, `SLACK`, `QUICK_BASE`,
                    `ZEPLIN`, `SOURCEFORGE`, `ZOOM`, `WORKDAY`, `GDRIVE`,
                    `GOOGLE_WEBMAIL`, `WINDOWS_LIVE_HOTMAIL`, `MSTEAM`

            instance_name (str): Cloud application instance name
            instance_identifiers (list): List of cloud application instance identifiers
                instance_identifier (str): Cloud application instance identifier, such as URL, IP address, or keyword.
                instance_identifier_name (str): Name of the cloud application instance identifier
                instance_type (str): Type of the cloud application instance identifier
                    Supported Values: `URL`, `REFURL`, `KEYWORD`

        Returns:
            tuple: A tuple containing the newly added cloud application instance, response, and error.
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

        response, error = self._request_executor.\
            execute(request, CloudApplicationInstances)
        if error:
            return (None, response, error)

        try:
            result = CloudApplicationInstances(
                self.form_response_body(response.get_body())
            )
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

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, CloudApplicationInstances)
        if error:
            return (None, response, error)

        try:
            result = CloudApplicationInstances(
                self.form_response_body(response.get_body())
            )
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
