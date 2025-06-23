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
from zscaler.utils import format_url, transform_common_id_fields, reformat_params
from zscaler.api_client import APIClient
from zscaler.zia.models.nat_control_policy import NatControlPolicy


class NatControlPolicyAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        List nat control rules in your organization.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:
            tuple: A tuple containing (list of nat control rules instances, Response, error).

        Example:
            List all nat control rules:

            >>> rules_list, response, error = client.zia.nat_control_policy.list_rules()
            ... if error:
            ...    print(f"Error listing nat control rules: {error}")
            ...    return
            ... print(f"Total rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...    print(rule.as_dict())

            filtering rule results by rule name :

            >>> rules_list, response, error = client.zia.nat_control_policy.list_rules(
                query_params={"search": Rule01}
            )
            ... if error:
            ...    print(f"Error listing nat control rules: {error}")
            ...    return
            ... print(f"Total rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnatRules
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(NatControlPolicy(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_rule(
        self,
        rule_id: int,
    ) -> tuple:
        """
        Returns information for the specified nat control rule.

        Args:
            rule_id (str): The unique identifier for the nat control rule.

        Returns:
            tuple: A tuple containing (nat control rule instance, Response, error).

        Example:
            Retrieve a nat control rules rule by its ID:

        >>> fetched_rule, response, error = client.zia.nat_control_policy.get_rule('960061')
        ... if error:
        ...     print(f"Error fetching rule by ID: {error}")
        ...     return
        ... print(f"Fetched rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnatRules/{rule_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, NatControlPolicy)

        if error:
            return (None, response, error)

        try:
            result = NatControlPolicy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        **kwargs,
    ) -> tuple:
        """
        Adds a new nat control rules rule.

        Args:
            name (str): Name of the rule, max 31 chars.

        Keyword Args:
            description (str): Additional information about the rule
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (int): The admin rank of the rule. Supported values 1-7
            redirect_ip (str): IP address to which the traffic is redirected to when the DNAT rule is triggered
            redirect_fqdn (str): FQDN to which the traffic is redirected to when the DNAT rule is triggered
            redirect_port (int): Port to which the traffic is redirected to when the DNAT rule is triggered
            enabled (bool): The rule state.
            dest_ip_groups (list): The IDs for the destination IP groups that this rule applies to.
            dest_ipv6_groups (list): The IDs for the destination IPV6 groups that this rule applies to.
            dest_countries (list): Destination countries for the rule.
            dest_addresses (list): Destination IPs for the rule. Accepts IP addresses or CIDR.
            src_ips (list): Source IPs for the rule. Accepts IP addresses or CIDR.
            src_ip_groups (list): The IDs for the source IP groups that this rule applies to.
            src_ipv6_groups (list): The IDs for the source IPV6 groups that this rule applies to.
            dest_ip_categories (list): IP address categories for the rule.
            groups (list): The IDs for the groups that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            res_categories (list): Resolved categories of destination for which the DNAT rule is applicable.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): IDs for time windows the rule applies to.
            nw_services (list): The IDs for the network services that this rule applies to.
            nw_service_groups (list): The IDs for the network service groups that this rule applies to.

        Returns:
            :obj:`tuple`: New nat control rule resource record.

        Example:
            Add a new nat control rule:

            >>> added_rule, _, error = client.zia.nat_control_policy.add_rule(
            ...     name=f"NewRule {random.randint(1000, 10000)}",
            ...     description=f"NewRule {random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     order=1,
            ...     rank=7,
            ...     redirect_port='2000',
            ...     redirect_ip='1.1.1.1',
            ...     src_ips=['192.168.100.0/24', '192.168.200.1'],
            ...     dest_addresses=['3.217.228.0-3.217.231.255', 'server1.acme.com', '*.acme.com'],
            ... )
            >>> if error:
            ...     print(f"Error adding rule: {error}")
            ...     return
            ... print(f"Rule added successfully: {added_rule.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnatRules
        """
        )

        body = kwargs

        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NatControlPolicy)
        if error:
            return (None, response, error)

        try:
            result = NatControlPolicy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> tuple:
        """
        Updates an existing nat control rule.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): Name of the rule, max 31 chars.
            description (str): Additional information about the rule
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (int): The admin rank of the rule. Supported values 1-7
            redirect_ip (str): IP address to which the traffic is redirected to when the DNAT rule is triggered
            redirect_fqdn (str): FQDN to which the traffic is redirected to when the DNAT rule is triggered
            redirect_port (int): Port to which the traffic is redirected to when the DNAT rule is triggered
            enabled (bool): The rule state.
            dest_ip_groups (list): The IDs for the destination IP groups that this rule applies to.
            dest_ipv6_groups (list): The IDs for the destination IPV6 groups that this rule applies to.
            dest_countries (list): Destination countries for the rule.
            dest_addresses (list): Destination IPs for the rule. Accepts IP addresses or CIDR.
            src_ips (list): Source IPs for the rule. Accepts IP addresses or CIDR.
            src_ip_groups (list): The IDs for the source IP groups that this rule applies to.
            src_ipv6_groups (list): The IDs for the source IPV6 groups that this rule applies to.
            dest_ip_categories (list): IP address categories for the rule.
            groups (list): The IDs for the groups that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            res_categories (list): Resolved categories of destination for which the DNAT rule is applicable.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): IDs for time windows the rule applies to.
            nw_services (list): The IDs for the network services that this rule applies to.
            nw_service_groups (list): The IDs for the network service groups that this rule applies to.

        Returns:
            tuple: Updated nat control rule resource record.

        Example:
            Update an existing nat control rule:

            >>> updated_rule, _, error = client.zia.nat_control_policy.add_rule(
            ...     rule_id='877846',
            ...     name=f"UpdateNewRule {random.randint(1000, 10000)}",
            ...     description=f"NewRule {random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     order=1,
            ...     rank=7,
            ...     redirect_port='2000',
            ...     redirect_ip='1.1.1.1',
            ...     src_ips=['192.168.100.0/24', '192.168.200.1'],
            ...     dest_addresses=['3.217.228.0-3.217.231.255', 'server1.acme.com', '*.acme.com'],
            ... )
            >>> if error:
            ...     print(f"Error adding rule: {error}")
            ...     return
            ... print(f"Rule added successfully: {updated_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnatRules/{rule_id}
        """
        )

        body = kwargs

        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NatControlPolicy)
        if error:
            return (None, response, error)

        try:
            result = NatControlPolicy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> tuple:
        """
        Deletes the specified nat control rule.

        Args:
            rule_id (str): The unique identifier for the nat control rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.nat_control_policy.delete_rule('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dnatRules/{rule_id}
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
