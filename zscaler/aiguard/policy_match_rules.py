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

from zscaler.aiguard.models.policy_match_rules import PolicyMatchRules
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url


class PolicyMatchRulesAPI(APIClient):
    """
    A Client object for the AI Guard Policy Match Rules resource.
    """

    _aiguard_base_endpoint = "/aiguard/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(self, query_params: Optional[dict] = None) -> APIResult[List[PolicyMatchRules]]:
        """
        Lists the policy match rules configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of PolicyMatchRules instances, Response, error)

        Examples:
            List policy match rules:

            >>> rule_list, _, error = client.aiguard.policy_match_rules.list_rules()
            >>> if error:
            ...     print(f"Error listing policy match rules: {error}")
            ...     return
            ... print(f"Total policy match rules found: {len(rule_list)}")
            ... for rule in rule_list:
            ...     print(rule.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policy-match-rules
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
                result.append(PolicyMatchRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_rule(self, rule_id: int) -> APIResult[PolicyMatchRules]:
        """
        Fetches a specific policy match rule by ID.

        Args:
            rule_id (int): The unique identifier for the policy match rule.

        Returns:
            tuple: A tuple containing (PolicyMatchRules instance, Response, error).

        Examples:
            Print a specific policy match rule:

            >>> fetched_rule, _, error = client.aiguard.policy_match_rules.get_rule(1013)
            >>> if error:
            ...     print(f"Error fetching policy match rule by ID: {error}")
            ...     return
            ... print(f"Fetched policy match rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policy-match-rules/{rule_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyMatchRules)
        if error:
            return (None, response, error)

        try:
            result = PolicyMatchRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_rule_by_name(self, name: str) -> APIResult[PolicyMatchRules]:
        """
        Fetches a specific policy match rule by name.

        Args:
            name (str): The name of the policy match rule.

        Returns:
            tuple: A tuple containing (PolicyMatchRules instance, Response, error).

        Examples:
            Print a specific policy match rule by name:

            >>> fetched_rule, _, error = client.aiguard.policy_match_rules.get_rule_by_name('Rule01')
            >>> if error:
            ...     print(f"Error fetching policy match rule by name: {error}")
            ...     return
            ... print(f"Fetched policy match rule by name: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policy-match-rules/name/{name}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyMatchRules)
        if error:
            return (None, response, error)

        try:
            result = PolicyMatchRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(self, **kwargs) -> APIResult[PolicyMatchRules]:
        """
        Creates a new policy match rule.

        Args:
            name (str): The name of the policy match rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            policy_id (str): The policy id for this policy match rule.
            enabled (bool): Indicates whether the policy match rule is enabled.
            rule_order (str): The rule order for this policy match rule.
            version (str): The version for this policy match rule.
            match_criteria (str): The match criteria for this policy match rule.

        Returns:
            tuple: A tuple containing the newly added PolicyMatchRules instance, response, and error.

        Examples:
            Add a new policy match rule. ``policyId``, ``applicationId`` and
            ``applicationCredentialsIds`` must reference existing resources -- create the
            detection policy, the LLM application and the application credential first and
            reuse the ids returned by those calls:

            >>> added_rule, _, error = client.aiguard.policy_match_rules.add_rule(
            ...     policyId=2916,
            ...     name="PolicyRule01",
            ...     enabled=True,
            ...     ruleOrder=2,
            ...     matchCriteria={
            ...         "llmApplications": [
            ...             {
            ...                 "applicationId": 647,
            ...                 "applicationCredentialsIds": [1075],
            ...             }
            ...         ],
            ...         "type": "DAS_APPLICATION",
            ...     },
            ... )
            >>> if error:
            ...     print(f"Error adding policy match rule: {error}")
            ...     return
            ... print(f"Policy match rule added successfully: {added_rule.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policy-match-rules
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyMatchRules)
        if error:
            return (None, response, error)

        try:
            result = PolicyMatchRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> APIResult[PolicyMatchRules]:
        """
        Updates information for the specified policy match rule.

        Args:
            rule_id (int): The unique identifier for the policy match rule.

        Keyword Args:
            name (str): The name of the policy match rule.
            policy_id (str): The policy id for this policy match rule.
            enabled (bool): Indicates whether the policy match rule is enabled.
            rule_order (str): The rule order for this policy match rule.
            version (str): The version for this policy match rule.
            match_criteria (str): The match criteria for this policy match rule.

        Returns:
            tuple: A tuple containing the updated PolicyMatchRules instance, response, and error.

        Examples:
            Update an existing policy match rule. The update replaces the rule, so the
            match criteria are sent in full:

            >>> updated_rule, _, error = client.aiguard.policy_match_rules.update_rule(
            ...     rule_id=1013,
            ...     policyId=2916,
            ...     name="PolicyRule01_Updated",
            ...     enabled=True,
            ...     ruleOrder=2,
            ...     matchCriteria={
            ...         "llmApplications": [
            ...             {
            ...                 "applicationId": 647,
            ...                 "applicationCredentialsIds": [1075],
            ...             }
            ...         ],
            ...         "type": "DAS_APPLICATION",
            ...     },
            ... )
            >>> if error:
            ...     print(f"Error updating policy match rule: {error}")
            ...     return
            ... print(f"Policy match rule updated successfully: {updated_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policy-match-rules/{rule_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyMatchRules)
        if error:
            return (None, response, error)

        try:
            result = PolicyMatchRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> APIResult[None]:
        """
        Deletes the specified policy match rule.

        Args:
            rule_id (int): The unique identifier for the policy match rule.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a policy match rule:

            >>> _, _, error = client.aiguard.policy_match_rules.delete_rule(1013)
            >>> if error:
            ...     print(f"Error deleting policy match rule: {error}")
            ...     return
            ... print(f"Policy match rule deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policy-match-rules/{rule_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
