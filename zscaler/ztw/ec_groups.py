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
from zscaler.ztw.models.ecgroup import ECGroup
from zscaler.ztw.models.ec_group_vm import ECGroupVM
from zscaler.ztw.models.common import CommonIDNameExternalID
from zscaler.utils import format_url


class ECGroupsAPI(APIClient):
    """
    A Client object for the ECGroupsAPI resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_ec_groups(self, query_params=None) -> tuple:
        """
        List all Cloud & Branch Connector groups.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            :obj:`Tuple`: The list of ec groups.

        Examples:
            List all ec groups::

                for group in ztw.ecgroups.list_ec_group():
                    print(group)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecgroup
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
                result.append(ECGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ec_group(self, group_id: str) -> tuple:
        """
        Get details for a specific Cloud or Branch Connector group by ID.

        Args:
            group_id (str): ID of Cloud or Branch Connector group.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            :obj:`Tuple`: The ec group details.

        Examples:
            Get details of a specific ec group:

                print(ztw.ecgroups.get_ec_group("123456789"))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecgroup/{group_id}
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
                result.append(ECGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ec_group_lite(self, query_params=None) -> tuple:
        """
        Returns the list of a subset of Cloud & Branch Connector group information.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 20.

        Returns:
            :obj:`Tuple`: A subset of Cloud & Branch Connector group information.

        Examples:
            List subset of Cloud & Branch Connector group information:

            >>> for group in ztw.ecgroups.list_ec_group_lite():
            ...    print(group)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecgroup/lite
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
                result.append(ECGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ec_instance_lite(self) -> tuple:
        """
        Returns the list of a subset of Cloud & Branch Connector instance information.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.

        Returns:
            :obj:`Tuple`: A subset of Cloud & Branch Connector instance information.

        Examples:
            List subset of Cloud & Branch Connector instance information:

            >>> for instance in ztw.ecgroups.list_ec_instance_lite():
            ...    print(instance)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecInstance/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CommonIDNameExternalID)
        if error:
            return (None, response, error)

        try:
            result = CommonIDNameExternalID(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ec_group_vm(self, group_id: str, vm_id: str) -> tuple:
        """
        Gets a VM by specified Cloud or Branch Connector group ID and VM ID

        Args:
            ``group_id`` (str): Cloud or Branch Connector group ID.
            ``vm_id`` (str): Cloud or Branch Connector VM ID.

        Returns:
            :obj:`Tuple`: The ec group VM details.

        Examples:
            Get details of a specific ec group VM:

                print(ztw.ecgroups.get_ec_group_vm("123456789"))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecgroup/{group_id}/{vm_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ECGroupVM)
        if error:
            return (None, response, error)

        try:
            result = ECGroupVM(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_ec_group_vm(self, group_id: str, vm_id: str):
        """
        Deletes a VM specified by Cloud or Branch Connector group ID and VM ID.

        Args:
            template_id (str): The ID of the VM to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Delete a ec group VM::

                print(ztw.ecgroups.delete_ec_group_vm("123456789"))
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecgroup/{group_id}/{vm_id}
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
