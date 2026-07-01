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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zpa.models.policy_group_set import PolicyGroupSetSummaryStat


class PolicyGroupSetAPI(APIClient):

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_policy_group_sets(self, query_params=None) -> APIResult[List[PolicyGroupSetSummaryStat]]:
        """
        List policy_group_sets.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of PolicyGroupSetSummaryStat instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet
        """)

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
                result.append(PolicyGroupSetSummaryStat(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_policy_group_sets_policy_type_rules(self, query_params=None) -> APIResult[List[PolicyGroupSetSummaryStat]]:
        """
        List policy_group_sets (policyType/rules).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of PolicyGroupSetSummaryStat instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/policyType/rules
        """)

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
                result.append(PolicyGroupSetSummaryStat(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_policy_group_sets_policy_type_summary(self, query_params=None) -> APIResult[List[PolicyGroupSetSummaryStat]]:
        """
        List policy_group_sets (policyType/summary).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of PolicyGroupSetSummaryStat instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/policyType/summary
        """)

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
                result.append(PolicyGroupSetSummaryStat(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_policy_group_sets_policy_type(self, query_params=None) -> APIResult[List[PolicyGroupSetSummaryStat]]:
        """
        List policy_group_sets (policyType).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of PolicyGroupSetSummaryStat instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/policyType
        """)

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
                result.append(PolicyGroupSetSummaryStat(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_policy_group_sets_policy_type_summary_stats(
        self, query_params=None
    ) -> APIResult[List[PolicyGroupSetSummaryStat]]:
        """
        List policy_group_sets (policyType/summaryStats).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of PolicyGroupSetSummaryStat instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/policyType/summaryStats
        """)

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
                result.append(PolicyGroupSetSummaryStat(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_policy_group_set(self, policy_group_set_id: str) -> APIResult[PolicyGroupSetSummaryStat]:
        """
        Returns information for the specified policy_group_set.

        Args:
            policy_group_set_id (str): The unique identifier for the policy_group_set.

        Returns:
            tuple: The resource record for the policy_group_set.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{policy_group_set_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
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
