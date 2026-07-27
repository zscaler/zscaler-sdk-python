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
from zscaler.zpa.models.policy_group_set import PolicyGroupSet
from zscaler.zpa.models.policy_group_set_summary import PolicyGroupSetSummary
from zscaler.zpa.models.policy_group_set_summary_stat import PolicyGroupSetSummaryStat
from zscaler.zpa.models.policy_rule import PolicyRule


class PolicyGroupSetAPI(APIClient):
    """
    A Client object for the Policy Group Set resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_sets(self, query_params: Optional[dict] = None) -> APIResult[List[PolicyGroupSetSummary]]:
        """
        Get all Policy Group Sets for a customer.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.create_if_not_exist]`` {boolean}: create resource if missing

        Returns:
            tuple: A tuple containing (list of PolicyGroupSetSummary instances, Response, error)

        Examples:
            List policy group sets:

            >>> set_list, _, error = client.zpa.policy_group_set.list_sets()
            >>> if error:
            ...     print(f"Error listing policy group sets: {error}")
            ...     return
            ... print(f"Total policy group sets found: {len(set_list)}")
            ... for set in set_list:
            ...     print(set.as_dict())

            List policy group sets using filters:

            >>> set_list, _, error = client.zpa.policy_group_set.list_sets(
            ...     query_params={'create_if_not_exist': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing policy group sets: {error}")
            ...     return
            ... print(f"Total policy group sets found: {len(set_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroupSetSummary)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PolicyGroupSetSummary(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_set_by_policy_type(
        self, policy_type: str, query_params: Optional[dict] = None
    ) -> APIResult[PolicyGroupSetSummary]:
        """
        Get Policy Group Set fo a customer for policy type.

        Args:
            policy_type (str): The policy type.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (PolicyGroupSetSummary instance, Response, error).

        Examples:
            Print a specific policy group set:

            >>> fetched_set, _, error = client.zpa.policy_group_set.get_set_by_policy_type('VALUE')
            >>> if error:
            ...     print(f"Error fetching policy group set: {error}")
            ...     return
            ... print(f"Fetched policy group set: {fetched_set.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/policyType/{policy_type}
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroupSetSummary)
        if error:
            return (None, response, error)

        try:
            result = PolicyGroupSetSummary(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_rules(self, policy_type: str, query_params: Optional[dict] = None) -> APIResult[List[PolicyRule]]:
        """
        Get paginated rules across groups within a Policy Group Set.

        Args:
            policy_type (str): The policy type.
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {string}: The search string used to support search by features and fields for the API.
                ``[query_params.page]`` {integer}: Specifies the page number.
                ``[query_params.pagesize]`` {integer}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.

        Returns:
            tuple: A tuple containing (list of PolicyRule instances, Response, error)

        Examples:
            List policy group sets:

            >>> set_list, _, error = client.zpa.policy_group_set.list_rules('VALUE')
            >>> if error:
            ...     print(f"Error listing policy group sets: {error}")
            ...     return
            ... print(f"Total policy group sets found: {len(set_list)}")
            ... for set in set_list:
            ...     print(set.as_dict())

            List policy group sets using filters:

            >>> set_list, _, error = client.zpa.policy_group_set.list_rules(
            ...     'VALUE', query_params={'search': 'Example'})
            >>> if error:
            ...     print(f"Error listing policy group sets: {error}")
            ...     return
            ... print(f"Total policy group sets found: {len(set_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/policyType/{policy_type}/rules
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyRule)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PolicyRule(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_set_summary(self, policy_type: str, query_params: Optional[dict] = None) -> APIResult[PolicyGroupSetSummary]:
        """
        Get Policy Group Set Summary fo a customer for policy type.

        Args:
            policy_type (str): The policy type.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (PolicyGroupSetSummary instance, Response, error).

        Examples:
            Print a specific policy group set:

            >>> fetched_set, _, error = client.zpa.policy_group_set.get_set_summary('VALUE')
            >>> if error:
            ...     print(f"Error fetching policy group set: {error}")
            ...     return
            ... print(f"Fetched policy group set: {fetched_set.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/policyType/{policy_type}/summary
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroupSetSummary)
        if error:
            return (None, response, error)

        try:
            result = PolicyGroupSetSummary(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_set_summary_stats(
        self, policy_type: str, query_params: Optional[dict] = None
    ) -> APIResult[PolicyGroupSetSummaryStat]:
        """
        Get summary stats for groups and rules within a Policy Group Set.

        Args:
            policy_type (str): The policy type.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (PolicyGroupSetSummaryStat instance, Response, error).

        Examples:
            Print a specific policy group set:

            >>> fetched_set, _, error = client.zpa.policy_group_set.get_set_summary_stats('VALUE')
            >>> if error:
            ...     print(f"Error fetching policy group set: {error}")
            ...     return
            ... print(f"Fetched policy group set: {fetched_set.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/policyType/{policy_type}/summaryStats
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroupSetSummaryStat)
        if error:
            return (None, response, error)

        try:
            result = PolicyGroupSetSummaryStat(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_set(self, group_set_id: str, query_params: Optional[dict] = None) -> APIResult[PolicyGroupSet]:
        """
        Get a specific Policy Group Set by ID.

        Args:
            group_set_id (str): The unique identifier for the policy group set.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (PolicyGroupSet instance, Response, error).

        Examples:
            Print a specific policy group set:

            >>> fetched_set, _, error = client.zpa.policy_group_set.get_set('216196257331370181')
            >>> if error:
            ...     print(f"Error fetching policy group set by ID: {error}")
            ...     return
            ... print(f"Fetched policy group set by ID: {fetched_set.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}
        """)

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyGroupSet)
        if error:
            return (None, response, error)

        try:
            result = PolicyGroupSet(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
