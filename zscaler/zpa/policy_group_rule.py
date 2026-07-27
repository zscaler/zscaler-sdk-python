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
from zscaler.zpa.models.policy_rule import PolicyRule


class PolicyGroupRuleAPI(APIClient):
    """
    A Client object for the Policy Group Rule resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_rules(self, group_set_id: str, group_id: str, query_params: Optional[dict] = None) -> APIResult[List[PolicyRule]]:
        """
        Get All Policy Groups Rules within a Policy Group with advanced search and pagination.

        Args:
            group_set_id (str): The group set id.
            group_id (str): The group id.
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {string}: The search string used to support search by features and fields for the API.
                ``[query_params.page]`` {integer}: Specifies the page number.
                ``[query_params.pagesize]`` {integer}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.

        Returns:
            tuple: A tuple containing (list of PolicyRule instances, Response, error)

        Examples:
            List policy group rules:

            >>> rule_list, _, error = client.zpa.policy_group_rule.list_rules('VALUE', 'VALUE')
            >>> if error:
            ...     print(f"Error listing policy group rules: {error}")
            ...     return
            ... print(f"Total policy group rules found: {len(rule_list)}")
            ... for rule in rule_list:
            ...     print(rule.as_dict())

            List policy group rules using filters:

            >>> rule_list, _, error = client.zpa.policy_group_rule.list_rules(
            ...     'VALUE', 'VALUE', query_params={'search': 'Example'})
            >>> if error:
            ...     print(f"Error listing policy group rules: {error}")
            ...     return
            ... print(f"Total policy group rules found: {len(rule_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}/rule
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

    def add_rule(self, group_set_id: str, group_id: str, **kwargs) -> APIResult[PolicyRule]:
        """
        Add a new policy rule for a given policy group.

        Args:
            group_set_id (str): The group set id.
            group_id (str): The group id.
            name (str): The name of the policy group rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            action (str): The action taken when traffic matches the policy group rule criteria.
            action_id (int): The action id for this policy group rule.
            browser_posture_profile_id (str): The browser posture profile id for this policy group rule.
            browser_posture_profile_name (str): The browser posture profile name for this policy group rule.
            button_text (str): The button text for this policy group rule.
            custom_msg (str): The custom msg for this policy group rule.
            default_rule (bool): A Boolean value indicating whether default rule applies to this policy group rule.
            default_rule_name (str): The default rule name for this policy group rule.
            description (str): Additional information about the policy group rule.
            device_posture_failure_notification_enabled (bool): A Boolean value indicating whether device posture failure notification is enabled for this policy group rule.
            disabled (int): The disabled for this policy group rule.
            extranet_enabled (bool): A Boolean value indicating whether extranet is enabled for this policy group rule.
            group_id (int): The group id for this policy group rule.
            name_without_trim (str): The name without trim for this policy group rule.
            operator (str): The operator for this policy group rule. Accepted values include e.g. ``AND``.
            policy_group_name (str): The policy group name for this policy group rule.
            policy_set_id (int): The policy set id for this policy group rule.
            policy_type (int): The policy type for this policy group rule.
            post_actions (dict): The post actions configuration for this policy group rule.
            priority (int): The priority for this policy group rule.
            read_only (bool): A Boolean value indicating whether read only applies to this policy group rule.
            reauth_idle_timeout (int): The reauth idle timeout for this policy group rule.
            reauth_timeout (int): The reauth timeout for this policy group rule.
            restriction_type (str): The restriction type for this policy group rule.
            rule_order (int): The rule order for this policy group rule.
            rule_type (str): The rule type for this policy group rule. Accepted values include e.g. ``STANDARD``.
            microtenant_name (str): The microtenant name for this policy group rule.
            url (str): The url for this policy group rule.
            zpn_isolation_profile_id (int): The zpn isolation profile id for this policy group rule.
            zpn_inspection_profile_id (int): The zpn inspection profile id for this policy group rule.
            zpn_inspection_profile_name (str): The zpn inspection profile name for this policy group rule.
            zscaler_managed (bool): A Boolean value indicating whether zscaler managed applies to this policy group rule.
            app_server_groups (list): The IDs for the app server groups that this policy group rule applies to.
            app_connector_groups (list): The IDs for the app connector groups that this policy group rule applies to.
            conditions (list): The IDs for the conditions that this policy group rule applies to.
            desktop_policy_mappings (list): The IDs for the desktop policy mappings that this policy group rule applies to.
            post_action_types (list): The list of post action types for this policy group rule.
            service_edge_groups (list): The IDs for the service edge groups that this policy group rule applies to.
            credential (dict): The ID of the credential for this policy group rule, e.g. ``{'id': 12345}``.
            credential_pool (dict): The ID of the credential pool for this policy group rule, e.g. ``{'id': 12345}``.
            extranet_dto (dict): The ID of the extranet dto for this policy group rule, e.g. ``{'id': 12345}``.
            inconsistent_config_details (dict): The inconsistent config details configuration for this policy group rule.
            privileged_capabilities (dict): The privileged capabilities configuration for this policy group rule.
            privileged_portal_capabilities (dict): The privileged portal capabilities configuration for this policy group rule.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            tuple: A tuple containing the newly added PolicyRule instance, response, and error.

        Examples:
            Add a new policy group rule:

            >>> added_rule, _, error = client.zpa.policy_group_rule.add_rule(
            ...     'VALUE', 'VALUE',
            ...     name=f"NewRule_{random.randint(1000, 10000)}",
            ...     description=f"NewRule_{random.randint(1000, 10000)}",
            ...     action='ALLOW',
            ... )
            >>> if error:
            ...     print(f"Error adding policy group rule: {error}")
            ...     return
            ... print(f"Policy group rule added successfully: {added_rule.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}/rule
        """)

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicyRule)
        if error:
            return (None, response, error)

        try:
            result = PolicyRule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, group_set_id: str, group_id: str, rule_id: str, microtenant_id: str = None) -> APIResult[None]:
        """
        Delete a policy rule within a policy group

        Args:
            group_set_id (str): The group set id.
            group_id (str): The group id.
            rule_id (str): The unique identifier for the policy group rule.
            microtenant_id (str, optional): The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a policy group rule:

            >>> _, _, error = client.zpa.policy_group_rule.delete_rule('VALUE', 'VALUE', '216196257331370181')
            >>> if error:
            ...     print(f"Error deleting policy group rule: {error}")
            ...     return
            ... print(f"Policy group rule deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}/rule/{rule_id}
        """)

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_rule(
        self, group_set_id: str, group_id: str, rule_id: str, query_params: Optional[dict] = None
    ) -> APIResult[PolicyRule]:
        """
        Get a policy rule within a policy group

        Args:
            group_set_id (str): The group set id.
            group_id (str): The group id.
            rule_id (str): The unique identifier for the policy group rule.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (PolicyRule instance, Response, error).

        Examples:
            Print a specific policy group rule:

            >>> fetched_rule, _, error = client.zpa.policy_group_rule.get_rule('VALUE', 'VALUE', '216196257331370181')
            >>> if error:
            ...     print(f"Error fetching policy group rule by ID: {error}")
            ...     return
            ... print(f"Fetched policy group rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}/rule/{rule_id}
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
            result = PolicyRule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def reorder_rule(
        self, group_set_id: str, group_id: str, rule_id: str, new_order: str, microtenant_id: str = None
    ) -> APIResult[None]:
        """
        Update rule order of a rule within policy group

        Args:
            group_set_id (str): The group set id.
            group_id (str): The group id.
            rule_id (str): The unique identifier for the policy group rule.
            new_order (str): The new order position for the policy group rule.
            microtenant_id (str, optional): The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            >>> _, _, error = client.zpa.policy_group_rule.reorder_rule('VALUE', 'VALUE', '216196257331370181', '2')
            >>> if error:
            ...     print(f"Error reordering policy group rule: {error}")
            ...     return
            ... print(f"Policy group rule reordered successfully.")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /policyGroupSet/{group_set_id}/group/{group_id}/rule/{rule_id}/reorder/{new_order}
        """)

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body={}, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
