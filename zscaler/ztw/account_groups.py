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
from typing import List, Optional
from zscaler.api_client import APIClient
from zscaler.ztw.models.account_groups import AccountGroups
from zscaler.utils import format_url
from zscaler.types import APIResult


class AccountGroupsAPI(APIClient):

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_account_groups(self, query_params: Optional[dict] = None) -> APIResult[List[AccountGroups]]:
        """
        Retrieves the details of AWS account groups with metadata.

        See the
        `Partner Integrations API reference (accountGroups-get):
        <https://help.zscaler.com/cloud-branch-connector/partner-integrations#/accountGroups-get>`_
        for further detail on payload structure.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            tuple: A tuple containing (list of AccountGroups instances, Response, error)

        Examples:
            Gets a list of all account groups.

            >>> account_groups_list, response, error = ztw.account_groups.list_account_groups()
            ... if error:
            ...     print(f"Error listing account groups: {error}")
            ...     return
            ... print(f"Total account groups found: {len(account_groups_list)}")
            ... for account_group in account_groups_list:
            ...     print(account_group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /accountGroups
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
                result.append(AccountGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_account_groups_lite(self) -> APIResult[List[AccountGroups]]:
        """
        Retrieves the ID and name of all the AWS account groups.

        This endpoint returns a lightweight version of account groups containing
        only the essential information (ID and name) for all account groups.

        Returns:
            tuple: A tuple containing (list of AccountGroups instances, Response, error)

        Examples:
            Get a list of all account groups (lite version):

            >>> account_groups_list, _, error = client.ztw.account_groups.list_account_groups_lite()
            ... if error:
            ...     print(f"Error listing account groups: {error}")
            ...     return
            ... print(f"Total account groups found: {len(account_groups_list)}")
            ... for account_group in account_groups_list:
            ...     print(account_group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /accountGroups/lite
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
                result.append(AccountGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_account_group(self, account_group_id: int) -> APIResult[AccountGroups]:
        """
        Retrieves the existing AWS account group based on the provided ID.

        Args:
            account_group_id (int): The ID of the AWS account group.

        Returns:
            tuple: A tuple containing (AccountGroups instance, Response, error)

        Examples:
            >>> fetched_public_cloud_info, response, error = (
            ...     client.ztw.account_groups.get_account_group(18382907)
            ... )
            ... if error:
            ...     print(f"Error fetching account group by ID: {error}")
            ...     return
            ... print(f"Fetched account group by ID: {fetched_account_group.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /accountGroups/{account_group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AccountGroups)

        if error:
            return (None, response, error)

        try:
            result = AccountGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_account_group(self, **kwargs) -> APIResult[AccountGroups]:
        """
        Creates an AWS account group. You can create a maximum of 128 groups in each organization.

        See the
        `Partner Integrations API reference (accountGroups-post):
        <https://help.zscaler.com/cloud-branch-connector/partner-integrations#/accountGroups-post>`_
        for further detail on payload structure.

        Keyword Args:
            name (str): The name of the public cloud account.
            cloud_type (str): The cloud provider type (e.g., "AWS").

        Returns:
            tuple: A tuple containing (AccountGroups instance, Response, error)

        Examples:
            Add a new Account Group:

            >>> new_account_group, response, error = ztw.account_groups.add_account_group(
            ...     name="Account Group 01",
            ...     description="This is an account group for demonstration"
            ... )
            ... if error:
            ...     print(f"Error adding account group: {error}")
            ...     return
            ... print(f"Created public cloud info: {new_cloud_info.as_dict()}")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /accountGroups
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

        response, error = self._request_executor.execute(request, AccountGroups)
        if error:
            return (None, response, error)

        try:
            result = AccountGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_account_group(self, account_group_id: int, **kwargs) -> APIResult[AccountGroups]:
        """
        Updates the existing AWS account group details based on the provided ID.

        Args:
            account_group_id (int): The unique ID of the AWS account group.

        Keyword Args:
            name (str, optional): The name of the public cloud account.
            cloud_type (str, optional): The cloud provider type (e.g., "AWS").

        Returns:
            tuple: A tuple containing (AccountGroups instance, Response, error)

        Examples:
            Update account group:

            >>> updated_account_group, _, error = client.ztw.account_groups.update_account_group(
            ...     account_group_id=452125,
            ...     name="Updated Account Group",
            ... )
            ... if error:
            ...     print(f"Error updating account group: {error}")
            ...     return
            ... print(f"Account group updated: {updated_account_group.as_dict()}")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /accountGroups/{account_group_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AccountGroups)
        if error:
            return (None, response, error)

        try:
            result = AccountGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_account_group(self, account_group_id: int) -> APIResult[None]:
        """
        Removes a specific AWS account group based on the provided ID.

        Args:
            account_group_id (int): The unique ID of the AWS account group.

        Returns:
            tuple: A tuple containing (None, Response, error). The API returns 204 No Content on success.

        Examples:
            >>> _, _, error = client.ztw.account_groups.delete_account_group(545845)
            ... if error:
            ...     print(f"Error deleting account group: {error}")
            ...     return
            ... print("Account group deleted successfully")

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /accountGroups/{account_group_id}
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

    def get_account_group_count(self) -> APIResult[List[dict]]:
        """
        Retrieves the total number of AWS account groups.

        Returns:
            :obj:`Tuple`: A tuple containing a list of dictionaries with configuration
            count information, the response object, and error if any.

        Examples:
            >>> count, _, error = client.ztw.account_groups.get_account_group_count()
            ... if error:
            ...     print(f"Error getting account group count: {error}")
            ...     return
            ... print(f"Total account groups found: {count}")
        Examples:
            >>> count, _, error = client.ztw.account_groups.get_account_group_count()
            ... if error:
            ...     print(f"Error getting account group count: {error}")
            ...     return
            ... print(f"Total account groups found: {count}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /accountGroups/count
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(self.form_response_body(item))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
