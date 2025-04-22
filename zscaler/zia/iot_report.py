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


class IOTReportAPI(APIClient):
    """
    A Client object for the IOT Report resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_device_types(self) -> tuple:
        """
        Retrieve the mapping between device type universally unique identifier (UUID)
        values and the device type names for all the device types supported by the Zscaler AI/ML.

        Returns:
            tuple: A tuple containing:
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current device types:

            >>> devices, response, err = client.zia.iot_report.get_device_types()
            >>> if err:
            ...     print(f"Error fetching devices: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /iotDiscovery/deviceTypes
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            iot_report = response.get_body()
            return (iot_report, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_categories(self) -> tuple:
        """
        Retrieve the mapping between the device category universally unique identifier (UUID)
        values and the category names for all the device categories supported by the Zscaler AI/ML.
        The parent of device category is device type.

        Returns:
            tuple: A tuple containing:
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current device types:

            >>> categories, response, err = client.zia.iot_report.get_categories()
            >>> if err:
            ...     print(f"Error fetching categories: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /iotDiscovery/categories
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            iot_report = response.get_body()
            return (iot_report, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_classifications(self) -> tuple:
        """
        Retrieve the mapping between the device classification universally unique identifier (UUID)
        values and the classification names for all the device classifications supported by Zscaler AI/ML.
        The parent of device classification is device category.

        Returns:
            tuple: A tuple containing:
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current classifications:

            >>> categories, response, err = client.zia.iot_report.get_classifications()
            >>> if err:
            ...     print(f"Error fetching categories: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /iotDiscovery/classifications
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            iot_report = response.get_body()
            return (iot_report, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_device_list(self) -> tuple:
        """
        Retrieve a list of discovered devices with the following key contexts, IP address,
        location, ML auto-label, classification, category, and type.

        Returns:
            tuple: A tuple containing:
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current classifications:

            >>> categories, response, err = client.zia.iot_report.get_device_list()
            >>> if err:
            ...     print(f"Error fetching categories: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /iotDiscovery/deviceList
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            iot_report = response.get_body()
            return (iot_report, response, None)
        except Exception as ex:
            return (None, response, ex)
