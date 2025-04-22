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
from zscaler.zia.models.devices import Devices
from zscaler.zia.models.device_groups import DeviceGroups
from zscaler.utils import format_url


class DeviceManagementAPI(APIClient):
    """
    A Client object for the Device Management resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_device_groups(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns the list of ZIA Device Groups.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.include_device_info]`` {bool}: Include or exclude device information.

                ``[query_params.include_pseudo_groups]`` {bool}: Include or exclude Zscaler Client Connector and
                    Cloud Browser Isolation-related device groups.

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
            /deviceGroups
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
                result.append(DeviceGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_devices(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns the list of Devices.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.name]`` {str}: The device group name. This is a `starts with` match.

                ``[query_params.user_ids]`` {list}: Used to list devices for specific users.

                ``[query_params.include_all]`` {bool}: Used to include or exclude Cloud Browser Isolation devices.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 100, but the maximum size is 1000.

        Returns:
            tuple: A tuple containing (list of Devices instances, Response, error)

        Examples:
            Print all devices

            >>> for dlp device in zia.device_management.list_devices():
            ...    pprint(device)

            Print Devices that match the name or description 'WINDOWS_OS'

            >>> pprint(zia.device_management.list_devices('WINDOWS_OS'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /deviceGroups/devices
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
                result.append(Devices(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_device_lite(self) -> tuple:
        """
        Returns the list of devices that includes device ID, name, and owner name.

        Returns:
            tuple: List of Device/ids.

        Examples:
            Get Device Lite results

            >>> results = zia.device.list_device_lite()
            ... for item in results:
            ...    print(item)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /deviceGroups/devices/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(DeviceGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
