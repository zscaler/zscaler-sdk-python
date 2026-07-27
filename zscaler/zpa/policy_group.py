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
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zpa.models.common import CommonFilterSearch
from zscaler.zpa.models.policy_group import PolicyGroup


class PolicyGroupAPI(APIClient):
    """
    A Client object for the Policy Group resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def add_group(self, group_set_id: str, **kwargs) -> APIResult[PolicyGroup]:
        """
        Add a new Policy Group to a Policy Group Set.

        Args:
            group_set_id (str): The group set id.
            name (str): The name of the policy group.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the policy group.
            group_criteria_rule_gid (int): The group criteria rule gid for this policy group.
            group_order (int): The group order for this policy group.
            policy_group_set_gid (int): The policy group set gid for this policy group.
            microtenant_name (str): The microtenant name for this policy group.
            type (str): The type for this policy group. Accepted values include e.g. ``GLOBAL``.
            group_criteria_rule (dict): The ID of the group criteria rule for this policy group, e.g. ``{'id': 12345}``.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            tuple: A tuple containing the newly added PolicyGroup instance, response, and error.

        Examples:
            Add a new policy group:

            >>> added_group, _, error = client.zpa.policy_group.add_group(
            ...     'VALUE',
            ...     name=f"NewGroup_{random.randint(1000, 10000)}",
            ...     description=f"NewGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding policy group: {error}")
            ...     return
            ... print(f"Policy group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group
        """)

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroup)
        if error:
            return (None, response, error)

        try:
            result = PolicyGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_groups(self, group_set_id: str, query_params: Optional[dict] = None) -> APIResult[List[PolicyGroup]]:
        """
        Get All Policy Groups within a Policy Group Set.

        Args:
            group_set_id (str): The group set id.
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            tuple: A tuple containing (list of PolicyGroup instances, Response, error)

        Examples:
            List policy groups:

            >>> group_list, _, error = client.zpa.policy_group.list_groups('VALUE')
            >>> if error:
            ...     print(f"Error listing policy groups: {error}")
            ...     return
            ... print(f"Total policy groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            List policy groups using filters:

            >>> group_list, _, error = client.zpa.policy_group.list_groups(
            ...     'VALUE', query_params={'page': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing policy groups: {error}")
            ...     return
            ... print(f"Total policy groups found: {len(group_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/all
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroup)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PolicyGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def search_groups(self, group_set_id: str, **kwargs) -> APIResult[CommonFilterSearch]:
        """
        Get All Policy Groups within a Policy Group Set with advanced search and pagination.

        Args:
            group_set_id (str): The group set id.
            **kwargs: The advanced filter/page/sort payload, e.g. ``filter_and_sort_dto`` with ``filter_by`` / ``page_by`` / ``sort_by``.

        Returns:
            tuple: A tuple containing the CommonFilterSearch instance (filter results, paging, sorting), response, and error.

        Examples:
            >>> result, _, error = client.zpa.policy_group.search_groups(
            ...     filter_and_sort_dto={
            ...         "filter_by": [{"filter_name": "name", "operator": "LIKE", "values": ["Test"]}],
            ...         "page_by": {"page": 1, "page_size": 20},
            ...     },
            ... )
            >>> if error:
            ...     print(f"Error searching policy groups: {error}")
            ...     return
            ... print(result.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/search
        """)

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CommonFilterSearch)
        if error:
            return (None, response, error)

        try:
            result = CommonFilterSearch(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_set_id: str, group_id: str, microtenant_id: str = None) -> APIResult[None]:
        """
        Delete a Policy Group.

        Args:
            group_set_id (str): The group set id.
            group_id (str): The unique identifier for the policy group.
            microtenant_id (str, optional): The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a policy group:

            >>> _, _, error = client.zpa.policy_group.delete_group('VALUE', '216196257331370181')
            >>> if error:
            ...     print(f"Error deleting policy group: {error}")
            ...     return
            ... print(f"Policy group deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}
        """)

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_group(self, group_set_id: str, group_id: str, query_params: Optional[dict] = None) -> APIResult[PolicyGroup]:
        """
        Get a specific Policy Group by ID within a Policy Group Set.

        Args:
            group_set_id (str): The group set id.
            group_id (str): The unique identifier for the policy group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (PolicyGroup instance, Response, error).

        Examples:
            Print a specific policy group:

            >>> fetched_group, _, error = client.zpa.policy_group.get_group('VALUE', '216196257331370181')
            >>> if error:
            ...     print(f"Error fetching policy group by ID: {error}")
            ...     return
            ... print(f"Fetched policy group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroup)
        if error:
            return (None, response, error)

        try:
            result = PolicyGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_set_id: str, group_id: str, **kwargs) -> APIResult[PolicyGroup]:
        """
        Update an existing Policy Group.

        Args:
            group_set_id (str): The group set id.
            group_id (str): The unique identifier for the policy group.

        Keyword Args:
            name (str): The name of the policy group.
            description (str): Additional information about the policy group.
            group_criteria_rule_gid (int): The group criteria rule gid for this policy group.
            group_order (int): The group order for this policy group.
            policy_group_set_gid (int): The policy group set gid for this policy group.
            microtenant_name (str): The microtenant name for this policy group.
            type (str): The type for this policy group. Accepted values include e.g. ``GLOBAL``.
            group_criteria_rule (dict): The ID of the group criteria rule for this policy group, e.g. ``{'id': 12345}``.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            tuple: A tuple containing the updated PolicyGroup instance, response, and error.

        Examples:
            Update an existing policy group:

            >>> updated_group, _, error = client.zpa.policy_group.update_group(
            ...     'VALUE',
            ...     group_id='216196257331370181',
            ...     name=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating policy group: {error}")
            ...     return
            ... print(f"Policy group updated successfully: {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}
        """)

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroup)
        if error:
            return (None, response, error)

        # Handle 204 No Content - response exists but body is empty
        if response is None or not response.get_body():
            return (PolicyGroup({"id": group_id}), response, None)

        try:
            result = PolicyGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def reorder_group(self, group_set_id: str, group_id: str, new_order: str, microtenant_id: str = None) -> APIResult[None]:
        """
        Update an existing Policy Group Order.

        Args:
            group_set_id (str): The group set id.
            group_id (str): The unique identifier for the policy group.
            new_order (str): The new order position for the policy group.
            microtenant_id (str, optional): The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            >>> _, _, error = client.zpa.policy_group.reorder_group('VALUE', '216196257331370181', '2')
            >>> if error:
            ...     print(f"Error reordering policy group: {error}")
            ...     return
            ... print(f"Policy group reordered successfully.")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}/reorder/{new_order}
        """)

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body={}, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
