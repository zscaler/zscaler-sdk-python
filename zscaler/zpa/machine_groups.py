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
from zscaler.zpa.models.machine_groups import MachineGroup
from zscaler.utils import format_url


class MachineGroupsAPI(APIClient):
    """
    A Client object for the Machine Groups resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_machine_groups(self, query_params: Optional[dict] = None) -> List[MachineGroup]:
        """
        Enumerates machine groups in your organization.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[MachineGroup]: A list of MachineGroup instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     groups = client.zpa.machine_groups.list_machine_groups()
            ...     for group in groups:
            ...         print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/machineGroup")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, MachineGroup)

        return [MachineGroup(self.form_response_body(item)) for item in response.get_results()]

    def list_machine_group_summary(self, query_params: Optional[dict] = None) -> List[MachineGroup]:
        """
        Retrieves all configured machine groups Name and IDs.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[MachineGroup]: A list of MachineGroup instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     groups = client.zpa.machine_groups.list_machine_group_summary()
            ...     for group in groups:
            ...         print(group.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/machineGroup/summary")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, MachineGroup)

        return [MachineGroup(self.form_response_body(item)) for item in response.get_results()]

    def get_group(self, group_id: str, query_params: Optional[dict] = None) -> MachineGroup:
        """
        Fetches information on the specified machine group.

        Args:
            group_id (str): The ID of the machine group.
            query_params (dict, optional): Map of query parameters.

        Returns:
            MachineGroup: The machine group object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     group = client.zpa.machine_groups.get_group('999999')
            ...     print(group.id)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/machineGroup/{group_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, MachineGroup)

        return MachineGroup(self.form_response_body(response.get_body()))
