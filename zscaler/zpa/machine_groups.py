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

    def list_machine_groups(self, query_params=None) -> tuple:
        """
        Enumerates machine groups in your organization with pagination.
        A subset of machine groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            tuple: A tuple containing (list of AppConnectorGroup instances, Response, error)

        Examples:
            Retrieve machine groups with pagination parameters:

            >>> group_list, _, err = client.zpa.machine_groups.list_machine_groups(
            ... query_params={'search': 'MGRP01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing machine groups: {err}")
            ...     return
            ... print(f"Total certificates found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /machineGroup
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, MachineGroup)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(MachineGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_group(self, group_id: str, query_params=None) -> tuple:
        """
        Fetches information on the specified machine group.

        Args:
            group_id (str): The ID of the machine group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            dict: The machine group object.

        Examples:
            >>> fetched_group, _, err = client.zpa.machine_groups.get_group('999999')
            ... if err:
            ...     print(f"Error fetching machine group by ID: {err}")
            ...     return
            ... print(fetched_group.id)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /machineGroup/{group_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, MachineGroup)
        if error:
            return (None, response, error)

        try:
            result = MachineGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
