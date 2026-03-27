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

from typing import Optional, Any, Dict

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.zms.models.inputs import PolicyRuleFilter


class PolicyRulesAPI(APIClient):
    """
    A Client object for the ZMS Policy Rules domain.

    Provides access to policy rule operations including:
    - List policy rules with filtering and pagination
    - List default policy rules
    """

    _zms_base_endpoint = "/zms/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def list_policy_rules(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
        fetch_all: bool = False,
        filter_by: Optional[PolicyRuleFilter] = None,
    ) -> tuple:
        """
        Get policy rules for a given customer with optional filtering and pagination.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).
            fetch_all: Whether to fetch all rules ignoring pagination.
            filter_by: Filter options using PolicyRuleFilter.

        Returns:
            tuple: (policy_rules_connection dict, response, error)

        Examples:
            List policy rules::

                >>> result, _, err = client.zms.policy_rules.list_policy_rules(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for rule in result.get("nodes", []):
                ...     print(rule.get("name"), rule.get("action"))
        """
        query = """
            query ListPolicyRules(
                $customerId: ID!, $pageNum: Int, $pageSize: Int,
                $fetchAll: Boolean, $filter: PolicyRuleFilter
            ) {
                policyRules(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize,
                    fetchAll: $fetchAll,
                    filter: $filter
                ) {
                    nodes {
                        id
                        name
                        action
                        priority
                        description
                        deleted
                        sourceTargetType
                        destinationTargetType
                        appZoneScopeTargetType
                        creationTime
                        modifiedTime
                        lastHit
                        portAndProtocols {
                            protocol
                            portRanges {
                                startPort
                                endPort
                            }
                        }
                    }
                    pageInfo {
                        pageNumber
                        pageSize
                        totalCount
                        totalPages
                    }
                }
            }
        """

        variables: Dict[str, Any] = {
            "customerId": customer_id,
            "pageNum": page_num,
            "pageSize": page_size,
            "fetchAll": fetch_all,
        }
        if filter_by is not None:
            variables["filter"] = filter_by.as_dict()

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ListPolicyRules",
        }

        http_method = "POST"
        api_url = format_url(self._zms_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = response.get_body().get("data", {}).get("policyRules", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_default_policy_rules(
        self,
        customer_id: str,
        page_num: int = 1,
        page_size: int = 20,
    ) -> tuple:
        """
        Get default policy rules for a given customer.

        Args:
            customer_id: The customer ID.
            page_num: Page number (default 1).
            page_size: Number of items per page (default 20).

        Returns:
            tuple: (default_policy_rules_connection dict, response, error)

        Examples:
            List default policy rules::

                >>> result, _, err = client.zms.policy_rules.list_default_policy_rules(
                ...     customer_id="123456789"
                ... )
                >>> if err:
                ...     print(err)
                >>> for rule in result.get("nodes", []):
                ...     print(rule.get("name"), rule.get("direction"))
        """
        query = """
            query ListDefaultPolicyRules(
                $customerId: ID!, $pageNum: Int, $pageSize: Int
            ) {
                defaultPolicyRules(
                    customerId: $customerId,
                    pageNum: $pageNum,
                    pageSize: $pageSize
                ) {
                    nodes {
                        id
                        name
                        action
                        direction
                        description
                        scopeType
                        modifiedTime
                    }
                    pageInfo {
                        pageNumber
                        pageSize
                        totalCount
                        totalPages
                    }
                }
            }
        """

        variables: Dict[str, Any] = {
            "customerId": customer_id,
            "pageNum": page_num,
            "pageSize": page_size,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "ListDefaultPolicyRules",
        }

        http_method = "POST"
        api_url = format_url(self._zms_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = response.get_body().get("data", {}).get("defaultPolicyRules", {})
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
