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
from zscaler.helpers import convert_keys_to_camel_case
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

    @zcc_param_mapper
    def download_devices(self, query_params=None, filename: str = None):
        """
        Downloads the list of devices as a CSV file from the ZCC portal.

        Args:
            query_params (dict, optional): A dictionary containing supported filters.

                ``[query_params.os_types]`` {str}: Filter by OS type. Valid values:
                    ios, android, windows, macos, linux.

                ``[query_params.registration_types]`` {str}: Filter by registration type. Valid values:
                    all, registered, unregistered, removal_pending, removed, quarantined.

            filename (str, optional): Custom filename for the CSV file. Defaults to timestamped name.

        Returns:
            str: Path to the downloaded CSV file.

        Examples:
            Download list of devices as a CSV:

            >>> try:
            ...     filename = client.zcc.devices.download_devices(
            ...         query_params={
            ...             "os_types": ["windows"],
            ...             "registration_types": ["unregistered"]
            ...         },
            ...         filename="unregistered_devices.csv"
            ...     )
            ...     print(f"Devices downloaded successfully: {filename}")
            ... except Exception as e:
            ...     print(f"Error during download: {e}")
        """
        query_params = query_params or {}

        if not filename:
            filename = f"zcc-devices-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.csv"

        # Translate os_types
        params = {}
        os_types = query_params.get("os_types")
        if os_types:
            os_types_resolved = [str(zcc_param_map["os"].get(item)) for item in os_types if zcc_param_map["os"].get(item)]
            if not os_types_resolved:
                raise ValueError("Invalid os_type specified.")
            params["osTypes"] = ",".join(os_types_resolved)

        # Translate registration_types
        registration_types = query_params.get("registration_types")
        if registration_types:
            reg_types_resolved = [
                str(zcc_param_map["reg_type"].get(item))
                for item in registration_types
                if zcc_param_map["reg_type"].get(item)
            ]
            if not reg_types_resolved:
                raise ValueError("Invalid registration_type specified.")
            params["registrationTypes"] = ",".join(reg_types_resolved)

        http_method = "get".upper()
        api_url = format_url(f"{self._zcc_base_endpoint}/downloadDevices")

        request, error = self._request_executor.create_request(
            http_method,
            api_url,
            params=params,
            headers={"Accept": "*/*"}
        )

        if error:
            raise Exception("Error creating request for downloading devices.")

        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            raise error
        if response is None:
            raise Exception("No response received when downloading devices.")

        content_type = response.headers.get("Content-Type", "").lower()
        if not content_type.startswith("application/octet-stream") and not response.text.startswith('"User","Device type"'):
            raise Exception("Invalid response content type or unexpected response format.")

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    @zcc_param_mapper
    def download_service_status(self, query_params=None, filename: str = None):
        """
        Downloads service status for all devices from the ZCC portal.

        Args:
            query_params (dict, optional): A dictionary containing supported filters.

                ``[query_params.os_types]`` {str}: Filter by OS type. Valid values:
                    ios, android, windows, macos, linux.

                ``[query_params.registration_types]`` {str}: Filter by registration type. Valid values:
                    all, registered, unregistered, removal_pending, removed, quarantined.

                filename (str, optional): Custom filename for the CSV file. Defaults to timestamped name.

        Returns:
            str: Path to the downloaded CSV file.

        Examples:
            Download list of devices as a CSV:

            >>> try:
            ...     filename = client.zcc.devices.download_service_status(
            ...         query_params={
            ...             "os_types": ["windows"],
            ...             "registration_types": ["unregistered"]
            ...         },
            ...         filename="unregistered_devices.csv"
            ...     )
            ...     print(f"Device Service Status downloaded successfully: {filename}")
            ... except Exception as e:
            ...     print(f"Error during download: {e}")
        """
        from datetime import datetime

        query_params = query_params or {}

        if not filename:
            filename = f"zcc-service-status-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.csv"

        params = {}
        os_types = query_params.get("os_types")
        if os_types:
            os_types_resolved = [str(zcc_param_map["os"].get(item)) for item in os_types if zcc_param_map["os"].get(item)]
            if not os_types_resolved:
                raise ValueError("Invalid os_type specified.")
            params["osTypes"] = ",".join(os_types_resolved)

        registration_types = query_params.get("registration_types")
        if registration_types:
            reg_types_resolved = [
                str(zcc_param_map["reg_type"].get(item))
                for item in registration_types
                if zcc_param_map["reg_type"].get(item)
            ]
            if not reg_types_resolved:
                raise ValueError("Invalid registration_type specified.")
            params["registrationTypes"] = ",".join(reg_types_resolved)

        http_method = "get".upper()
        api_url = format_url(f"{self._zcc_base_endpoint}/downloadServiceStatus")

        request, error = self._request_executor.create_request(
            http_method,
            api_url,
            params=params,
            headers={"Accept": "*/*"}
        )

        if error:
            raise Exception("Error creating request for downloading service status.")

        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            raise error
        if response is None:
            raise Exception("No response received when downloading devices.")

        content_type = response.headers.get("Content-Type", "").lower()
        if not content_type.startswith("application/octet-stream") and not response.text.startswith('"User","Device type"'):
            raise Exception("Invalid response content type or unexpected response format.")

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    @zcc_param_mapper
    def list_devices(self, query_params=None) -> tuple:
        """
        Returns the list of devices enrolled in the Client Connector Portal.

        Args:
            query_params (dict, optional): A dictionary containing supported filters.

                ``[query_params.os_type]`` {str}: Filter by device operating system type. Valid options are:
                    ios, android, windows, macos, linux.

                ``[query_params.username]`` {str}:  Filter by enrolled username for the device.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    The default page size is 50.
                    The max page size is 5000.

        Returns:
            :obj:`list`: A list containing devices using ZCC enrolled in the Client Connector Portal.

        Examples:
            Prints all devices in the Client Connector Portal to the console:

            >>> device_list, _, err = client.zcc.devices.list_devices(
            ... query_params = {'username': 'jdoe@acme.com', "os_type": "3", 'page': 1, 'page_size': 1})
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

            >>> devices, _, err = client.zcc.devices.get_device_cleanup_info()
            >>>     if err:
            ...         print(f"Error fetching device clean up: {err}")
            ...         return
            ...     print("Device clean up fetched successfully.")
            ...     print(devices)
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

        Examples:
            Updated Device Cleaup Information:

            >>> device, _, err = client.zcc.devices.update_device_cleanup_info(
            ...     active=1,
            ...     force_remove_type=1,
            ...     device_exceed_limit=16
            ... )
            >>> if err:
            ...     print(f"Error fetching device cleanup info: {err}")
            ...     return
            ... print("Current device cleanup info fetched successfully.")
            ... print(device)
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

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

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

    @zcc_param_mapper
    def remove_devices(self, query_params=None, **kwargs) -> tuple:
        """
        Remove of the devices from the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 30.
                    The max page size is 5000.

                client_connector_version (list[str]): List of the client connector agent versions
                os_type (int): Valid options are: ios, android, windows, macos, linux.
                udids (list[str]): The list of udids for the devices to be removed
                user_name (str): The username i.e jdoe@acme.com of the user to which the device is associated with.

        Returns:
            :obj:`list`: Remove devices from the Client Connector Portal.

        Examples:
            Removes devices in the Client Connector Portal to the console:

            >>> remove_devices, _, error = client.zcc.devices.remove_devices(
            ...     client_connector_version=['3.0.0.57'],
            ...     os_type='3',
            ...     udids='VMware-42-02-38-a5-5f-9c-86-39-ff-5a-d0-60-5c-35-68-90:D630C3617830C5C0B2DDE986EA7D994324C4EC1D',
            ...     username='jdoe@acme.com'
            ... )
            >>> if error:
            ...     print(f"Error removing device: {error}")
            ...     return
            ... for device in remove_devices:
            ...     print(f"Removed device: {device.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /removeDevices
        """
        )

        query_params = query_params or {}

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            params=query_params
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ForceRemoveDevices)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ForceRemoveDevices(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @zcc_param_mapper
    def force_remove_devices(self, query_params=None, **kwargs) -> tuple:
        """
        Force remove of the devices from the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 30.
                    The max page size is 5000.

                client_connector_version (list[str]): List of the client connector agent versions
                os_type (int): Valid options are: ios, android, windows, macos, linux.
                udids (list[str]): The list of udids for the devices to be removed
                user_name (str): The username i.e jdoe@acme.com of the user to which the device is associated with.

        Returns:
            :obj:`list`: Forces the removal of devices from the Client Connector Portal.

        Examples:
            Removes devices in the Client Connector Portal to the console:

            >>> remove_devices, _, error = client.zcc.devices.force_remove_devices(
            ...     client_connector_version=['3.0.0.57'],
            ...     os_type='windows',
            ...     udids='VMware-42-02-38-a5-5f-9c-86-39-ff-5a-d0-60-5c-35-68-90:D630C3617830C5C0B2DDE986EA7D994324C4EC1D',
            ...     user_name='jdoe@acme.com'
            ... )
            >>> if error:
            ...     print(f"Error removing device: {error}")
            ...     return
            ... for device in remove_devices:
            ...     print(f"Removed device: {device.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /forceRemoveDevices
        """
        )

        query_params = query_params or {}

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            params=query_params
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ForceRemoveDevices)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ForceRemoveDevices(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def remove_machine_tunnel(self, query_params=None, **kwargs) -> tuple:
        """
        Remove machine tunnel devices from the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.hostname]`` {int}: Comma-separated list of hostnames for the device.
                ``[query_params.machine_token]`` {int}: Comma-separated list of hostnames for the device.

        Keyword Args:
            hostnames (str): The hostname of the machine tunnel to be removed.
            machine_token (str): The machine tunnel token to be removed.

        Returns:
            :obj:`list`: Remove machine tunnel devices from the Client Connector Portal.

        Examples:
            Removes machine tunnels in the Client Connector Portal to the console:

            >>> remove_tunnels, _, error = client.zcc.devices.remove_machine_tunnel(
            ...     host_names=['FXJ14JLFQW'],
            ... )
            >>> if error:
            ...     print(f"Error removing machine tunnel: {error}")
            ...     return
            ... print("Removed machine tunnel:", remove_tunnels)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /removeMachineTunnel
        """
        )

        query_params = convert_keys_to_camel_case(query_params or {})
        body = convert_keys_to_camel_case(kwargs or {})
        headers = {}

        request, error = self._request_executor.create_request(
            http_method,
            api_url,
            body=body,
            headers=headers,
            params=query_params,
        )

        if error:
            return None, None, error

        response, error = self._request_executor.execute(request)
        if error:
            return None, response, error

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return None, response, error

        return result, response, None
