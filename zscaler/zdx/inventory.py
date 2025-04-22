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
from zscaler.zdx.models.software_inventory import SoftwareList
from zscaler.zdx.models.software_inventory import DeviceSoftwareInventory
from zscaler.utils import format_url, zdx_params


class InventoryAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zdx_base_endpoint = "/zdx/v1"

    @zdx_params
    def list_softwares(self, query_params=None) -> tuple:
        """
        Returns a list of all software in ZDX.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.location_id]`` {list}: The unique ID for the department.

                ``[query_params.department_id]`` {list}: The unique ID for the department.

                ``[query_params.geo_id]`` {list}: List of unique ID for the geolocation.

                ``[query_params.user_ids]`` {list}: List of user IDs.

                ``[query_params.device_ids]`` {list}: List of device IDs.

        Returns:
            :obj:`Tuple`: The list of software in ZDX.

        Examples:
            List all software in ZDX for the past 2 hours:

            >>> software_list, _, err = client.zdx.inventory.list_softwares()
            ... if err:
            ...     print(f"Error listing softwares: {err}")
            ...     return
            ... for software in software_list:
            ...     print(software)

            List all software in ZDX for the past 24 hours:

            >>> software_list, _, err = client.zdx.inventory.list_softwares(query_params={"since": 24})
            ... if err:
            ...     print(f"Error listing softwares: {err}")
            ...     return
            ... for software in software_list:
            ...     print(software)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /inventory/software
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
            # Convert the response body into a dictionary
            data = self.form_response_body(response.get_body())
            # Extract the list of software items (each as a dict)
            software_items = data.get("software", [])
            # Instantiate a SoftwareList object for each item using the defensive model
            result = [SoftwareList(item) for item in software_items]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def list_software_keys(self, software_key: str, query_params=None) -> tuple:
        """
        Returns a list of all users and devices for the given software name and version.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.department_id]`` {str}: The unique ID for the department.

                ``[query_params.geo_id]`` {int}: The unique ID for the geolocation.

                ``[query_params.user_ids]`` {list}: List of user IDs.

                ``[query_params.device_ids]`` {list}: List of device IDs.

        Returns:
            :obj:`tuple`: The list of software in ZDX.

        Examples:
            List all software keys in ZDX for the past 2 hours:

            >>> software_key, _, error = client.zdx.inventory.list_software_keys(
                software_key='screencaptureui2')
            ... if error:
            ...    print(f"Error: {error}")
            ... else:
            ...     for software in software_key:
            ...         print(software.as_dict())

            List all software keys in ZDX for the past 24 hours:

            >>> software_key, _, error = client.zdx.inventory.list_software_keys(
                software_key='screencaptureui2', query_params={"since": 24})
            ... if error:
            ...    print(f"Error: {error}")
            ... else:
            ...     for software in software_key:
            ...         print(software.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /inventory/software/{software_key}
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
            result = [DeviceSoftwareInventory(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
