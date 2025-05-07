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
from zscaler.utils import format_url, zcc_param_map, zcc_param_mapper
from zscaler.zcc.models.devices import Device
from zscaler.zcc.models.devices import ForceRemoveDevices
from zscaler.zcc.models.devices import SetDeviceCleanupInfo
from zscaler.zcc.models.devices import DeviceCleanup
from zscaler.zcc.models.devices import DeviceDetails
from datetime import datetime


class DevicesAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def download_devices(
        self,
        filename: str = None,
        os_types: list = None,
        registration_types: list = None,
    ):
        """
        Downloads the list of devices as a CSV file from the ZCC portal.
        """
        if not filename:
            filename = f"zcc-devices-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.csv"

        params = {}

        # Handle OS types
        if os_types:
            os_types_resolved = [str(zcc_param_map["os"].get(item)) for item in os_types if zcc_param_map["os"].get(item)]
            if not os_types_resolved:
                raise ValueError("Invalid os_type specified.")
            params["osTypes"] = ",".join(os_types_resolved)

        # Handle Registration types
        if registration_types:
            reg_types_resolved = [
                str(zcc_param_map["reg_type"].get(item)) for item in registration_types if zcc_param_map["reg_type"].get(item)
            ]
            if not reg_types_resolved:
                raise ValueError("Invalid registration_type specified.")
            params["registrationTypes"] = ",".join(reg_types_resolved)

        # Correct the API URL
        http_method = "get".upper()
        api_url = format_url(f"{self._zcc_base_endpoint}/downloadDevices")

        # Create the request properly
        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            raise Exception("Error creating request for downloading devices.")

        # Execute request and download file
        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error or response is None:
            raise Exception("Error executing request for downloading devices.")

        # Validate the response content
        content_type = response.headers.get("Content-Type", "").lower()

        # Check for valid CSV-like content
        if not content_type.startswith("application/octet-stream") and not response.text.startswith('"User","Device type"'):
            raise Exception("Invalid response content type or unexpected response format.")

        # Save file to disk
        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    @zcc_param_mapper
    def list_devices(self, query_params=None) -> tuple:
        """
        Returns the list of devices enrolled in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.os_type]`` {str}: Filter by device operating system type. Valid options are:
                    - ios
                    - android
                    - windows
                    - macos
                    - linux
                ``[query_params.username]`` {str}: Filter by enrolled user name for the device.

                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {str}: Specifies the page size. The default page size is 50.
                    The max page size is 5000.

        Returns:
            :obj:`list`: A list containing devices using ZCC enrolled in the Client Connector Portal.

        Examples:
            Prints all devices in the Client Connector Portal to the console:

            >>> device_list, _, err = client.zcc.devices.list_devices(
            ... query_params = { "os_type": "3", 'page': 1, 'page_size': 1})
            >>> if err:
            ...     print(f"Error listing devices: {err}")
            ...     return
            ... print(f"Total devices found: {len(device_list)}")
            ... for device in device_list:
            ...     print(device.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getDevices
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Device)
        if error:
            return (None, response, error)

        try:
            result = response.get_results() 
        except Exception as error:
            return None, response, error

        return result, response, None

    def get_device_cleanup_info(self) -> tuple:
        """
        Returns device cleanup sync information from the Client Connector Portal.

        Args:
            N/A

        Returns:
            :obj:`list`: Returns device cleanup sync information in the Client Connector Portal.

        Examples:
            Prints all devices in the Client Connector Portal to the console:

            >>> for device in zcc.devices.get_device_cleanup_info():
            ...    print(device)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getDeviceCleanupInfo
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DeviceCleanup)
        if error:
            return (None, response, error)

        try:
            result = response.get_results() 
        except Exception as error:
            return None, response, error

        return result, response, None

    def update_device_cleanup_info(self, **kwargs) -> tuple:
        """
        Set Device Cleaup Information

        Args:
           N/A

        Returns:
            tuple: A tuple containing the updated Device Cleaup Information, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /setDeviceCleanupInfo
        """
        )
        body = {}

        body.update(kwargs)

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, SetDeviceCleanupInfo)
        if error:
            return (None, response, error)

        try:
            result = SetDeviceCleanupInfo(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_device_details(self, query_params=None) -> tuple:
        """
       Lists device details of enrolled devices of your organization.

        Keyword Args:
                ``[query_params.username]`` {str, optional}: Filter by enrolled user name for the device.
                ``[query_params.udid]`` {str, optional}: Filter by unique device identifier.

        Returns:
            :obj:`list`: Returns device detail information in the Client Connector Portal.

        Examples:
            Prints all devices in the Client Connector Portal to the console:

            >>> details, _, err = client.zcc.devices.get_device_details()
            >>> if err:
            ...     print(f"Error listing device details: {err}")
            ...     return
            ...  for device in details:
            ...     print(device.as_dict())
            
            Prints all devices in the Client Connector Portal to the console:

            >>> details, _, err = client.zcc.devices.get_device_details(
            ... query_params:{'username': 'jdoe'})
            >>> if err:
            ...     print(f"Error listing device details: {err}")
            ...     return
            ...  for device in details:
            ...     print(device.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /getDeviceDetails
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DeviceDetails)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(DeviceDetails(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def download_service_status(
        self,
        filename: str = None,
        os_types: list = None,
        registration_types: list = None,
    ):
        """
        Downloads service status for all devices from the ZCC portal.
        """
        if not filename:
            filename = f"zcc-devices-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.csv"

        params = {}

        # Handle OS types
        if os_types:
            os_types_resolved = [str(zcc_param_map["os"].get(item)) for item in os_types if zcc_param_map["os"].get(item)]
            if not os_types_resolved:
                raise ValueError("Invalid os_type specified.")
            params["osTypes"] = ",".join(os_types_resolved)

        # Handle Registration types
        if registration_types:
            reg_types_resolved = [
                str(zcc_param_map["reg_type"].get(item)) for item in registration_types if zcc_param_map["reg_type"].get(item)
            ]
            if not reg_types_resolved:
                raise ValueError("Invalid registration_type specified.")
            params["registrationTypes"] = ",".join(reg_types_resolved)

        # Correct the API URL
        http_method = "get".upper()
        api_url = format_url(f"{self._zcc_base_endpoint}/downloadServiceStatus")

        # Create the request properly
        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            raise Exception("Error creating request for downloading devices.")

        # Execute request and download file
        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error or response is None:
            raise Exception("Error executing request for downloading devices.")

        # Validate the response content
        content_type = response.headers.get("Content-Type", "").lower()

        # Check for valid CSV-like content
        if not content_type.startswith("application/octet-stream") and not response.text.startswith('"User","Device type"'):
            raise Exception("Invalid response content type or unexpected response format.")

        # Save file to disk
        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    def remove_devices(self, query_params=None) -> tuple:
        """
        Remove of the devices from the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page_size]`` {int}: Specifies the page size.

        Returns:
            :obj:`list`: Remove devices from the Client Connector Portal.

        Examples:
            Prints all removed devices in the Client Connector Portal to the console:

            >>> for device in zcc.devices.remove_devices():
            ...    print(device)

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /removeDevices
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
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
                result.append(ForceRemoveDevices(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def force_remove_devices(self, query_params=None) -> tuple:
        """
        Force remove of the devices from the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page_size]`` {int}: Specifies the page size.

        Returns:
            :obj:`list`:Remove devices from the Client Connector Portal.

        Examples:
            Prints all admin roles in the Client Connector Portal to the console:

            >>> for role in zcc.devices.force_remove_devices():
            ...    print(role)

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /forceRemoveDevices
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
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
                result.append(ForceRemoveDevices(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def remove_machine_tunnel(self) -> tuple:
        """
        Remove machine tunnel devices from the Client Connector Portal.

        Keyword Args:
            hostnames (str): The hostname of the machine tunnel to be removed.
            machine_token (str): The machine tunnel token to be removed.

        Returns:
            :obj:`list`: Remove machine tunnel devices from the Client Connector Portal.

        Examples:
            Prints all removed machine tunnel devices in the Client Connector Portal to the console:

            >>> for tunnel in zcc.devices.remove_machine_tunnel():
            ...    print(tunnel)

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /removeMachineTunnel
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, {})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append((self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
