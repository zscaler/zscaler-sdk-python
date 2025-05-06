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
from zscaler.zia.models.cloud_firewall_dns_rules import FirewallDNSRules


class FirewallDNSRulesAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        List firewall dns rules in your organization.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:
            tuple: A tuple containing (list of cloud firewall dns rules instances, Response, error).

        Example:
            List all cloud firewall dns rules:

            >>> rules_list, response, error = client.zia.cloud_firewall_dns.list_rules()
            ... if error:
            ...    print(f"Error listing cloud firewall dns: {error}")
            ...    return
            ... print(f"Total rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...    print(rule.as_dict())

            filtering rule results by rule name :

            >>> rules_list, response, error = client.zia.cloud_firewall_dns.list_rules(
                query_params={"search": Rule01}
            )
            ... if error:
            ...    print(f"Error listing cloud firewall dns: {error}")
            ...    return
            ... print(f"Total rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...    print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /firewallDnsRules
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
                results.append(FirewallDNSRules(self.form_response_body(item)))
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
        Returns information for the specified cloud firewall dns filter rule.

        Args:
            rule_id (str): The unique identifier for the cloud firewall dns filter rule.

        Returns:
            tuple: A tuple containing (cloud firewall dns rule instance, Response, error).

        Example:
            Retrieve a cloud firewall dns rule by its ID:

        >>> fetched_rule, response, error = client.zia.cloud_firewall_dns.get_rule('960061')
        >>> if error:
        ...     print(f"Error fetching rule by ID: {error}")
        ...     return
        ... print(f"Fetched rule by ID: {fetched_rule.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /firewallDnsRules/{rule_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, FirewallDNSRules)

        if error:
            return (None, response, error)

        try:
            result = FirewallDNSRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        **kwargs,
    ) -> tuple:
        """
        Adds a new cloud firewall dns rule.

        Args:
            name (str): Name of the rule, max 31 chars.

        Keyword Args:
            description (str): Additional information about the rule.
            order (int): The order of the rule, defaults to adding the rule to the bottom of the list.
            rank (int): The admin rank of the rule. Supported values are 1-7.
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            redirect_ip (str): The IP address to which the traffic is redirected when the DNAT rule is triggered.
            enable_full_logging (bool): If True, enables full logging.
            capture_pcap (bool): Indicates whether packet capture (PCAP) is enabled or not.
            predefined (bool): Indicates if the rule is predefined.
            default_rule (bool): Indicates if the rule is the default Cloud DNS rule.
            action (str): Action when traffic matches the rule criteria.
                Supported values: ALLOW, BLOCK, REDIR_REQ, REDIR_RES, REDIR_ZPA, REDIR_REQ_DOH, REDIR_REQ_KEEP_SENDER,
                REDIR_REQ_TCP, REDIR_REQ_UDP, BLOCK_WITH_RESPONSE.
            applications (list[str]): DNS tunnels and network applications to which the rule applies.
            dest_ip_groups (list[str]): IDs for destination IP groups the rule applies to.
            dest_ipv6_groups (list[str]): IDs for destination IPv6 groups the rule applies to.
            dest_countries (list[str]): Destination countries for the rule.
            dest_addresses (list[str]): Destination IPs. Accepts IPs or CIDR.
            src_ips (list[str]): Source IPs. Accepts IPs or CIDR.
            source_countries (list[str]): Source countries of origin for the rule.
            src_ip_groups (list[str]): IDs for source IP groups the rule applies to.
            src_ipv6_groups (list[str]): IDs for source IPv6 groups the rule applies to.
            dest_ip_categories (list[str]): IP address categories for the rule.
            res_categories (list[str]): Categories of IP addresses resolved by DNS.
            dns_rule_request_types (list[str]): DNS request types the rule applies to.
            protocols (list[str]): Protocols the rule applies to (e.g., TCP, UDP, DOHTTPS).
            block_response_code (str): DNS response code sent when the rule action is BLOCK.
            devices (list[str]): IDs for devices managed by Zscaler Client Connector.
            device_groups (list[str]): IDs for device groups managed by Zscaler Client Connector.
            labels (list[str]): IDs for labels associated with this rule.
            locations (list[str]): IDs for locations the rule applies to.
            location_groups (list[str]): IDs for location groups the rule applies to.
            edns_ecs_object (str): ID for EDNS ECS object for DNS resolution.
            time_windows (list[str]): IDs for time windows the rule applies to.
            application_groups (list[str]): IDs for DNS application groups the rule applies to.
            dns_gateway (str): DNS gateway for redirecting traffic when the action is set to redirect DNS requests.
            zpa_ip_group (str): ZPA IP pool specified when resolving domain names of ZPA applications.
        Returns:
            tuple: Updated firewall dns filtering rule resource record.

        Example:
            Add a new rule to change its name and action:

            >>> added_rule, _, error = client.zia.cloud_firewall_dns.add_rule(
            ...     name=f"NewRule_{random.randint(1000, 10000)}",
            ...     description=f"NewRule_{random.randint(1000, 10000)}",
            ...     action='REDIR_REQ',
            ...     state="ENABLED",
            ...     order=1,
            ...     rank=7,
            ...     redirect_ip = "8.8.8.8"
            ...     protocols = ["ANY_RULE"]
            ...     dest_countries=["COUNTRY_CA", "COUNTRY_US", "COUNTRY_MX", "COUNTRY_AU", "COUNTRY_GB"],
            ...     locations=['54528', '5485857']
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
            /firewallDnsRules
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, FirewallDNSRules)
        if error:
            return (None, response, error)

        try:
            result = FirewallDNSRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> tuple:
        """
        Updates an existing cloud firewall dns rule.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): Name of the rule, max 31 chars.
            description (str): Additional information about the rule.
            order (int): The order of the rule, defaults to adding the rule to the bottom of the list.
            rank (int): The admin rank of the rule. Supported values are 1-7.
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            redirect_ip (str): The IP address to which the traffic is redirected when the DNAT rule is triggered.
            enable_full_logging (bool): If True, enables full logging.
            capture_pcap (bool): Indicates whether packet capture (PCAP) is enabled or not.
            predefined (bool): Indicates if the rule is predefined.
            default_rule (bool): Indicates if the rule is the default Cloud DNS rule.
            action (str): Action when traffic matches the rule criteria.
                Supported values: ALLOW, BLOCK, REDIR_REQ, REDIR_RES, REDIR_ZPA, REDIR_REQ_DOH, REDIR_REQ_KEEP_SENDER,
                REDIR_REQ_TCP, REDIR_REQ_UDP, BLOCK_WITH_RESPONSE.
            applications (list[str]): DNS tunnels and network applications to which the rule applies.
            dest_ip_groups (list[str]): IDs for destination IP groups the rule applies to.
            dest_ipv6_groups (list[str]): IDs for destination IPv6 groups the rule applies to.
            dest_countries (list[str]): Destination countries for the rule.
            dest_addresses (list[str]): Destination IPs. Accepts IPs or CIDR.
            src_ips (list[str]): Source IPs. Accepts IPs or CIDR.
            source_countries (list[str]): Source countries of origin for the rule.
            src_ip_groups (list[str]): IDs for source IP groups the rule applies to.
            src_ipv6_groups (list[str]): IDs for source IPv6 groups the rule applies to.
            dest_ip_categories (list[str]): IP address categories for the rule.
            res_categories (list[str]): Categories of IP addresses resolved by DNS.
            dns_rule_request_types (list[str]): DNS request types the rule applies to.
            protocols (list[str]): Protocols the rule applies to (e.g., TCP, UDP, DOHTTPS).
            block_response_code (str): DNS response code sent when the rule action is BLOCK.
            devices (list[str]): IDs for devices managed by Zscaler Client Connector.
            device_groups (list[str]): IDs for device groups managed by Zscaler Client Connector.
            labels (list[str]): IDs for labels associated with this rule.
            locations (list[str]): IDs for locations the rule applies to.
            location_groups (list[str]): IDs for location groups the rule applies to.
            edns_ecs_object (str): ID for EDNS ECS object for DNS resolution.
            time_windows (list[str]): IDs for time windows the rule applies to.
            application_groups (list[str]): IDs for DNS application groups the rule applies to.
            dns_gateway (str): DNS gateway for redirecting traffic when the action is set to redirect DNS requests.
            zpa_ip_group (str): ZPA IP pool specified when resolving domain names of ZPA applications.

        Returns:
            tuple: Updated firewall dns filtering rule resource record.

        Example:
            Update an existing rule to change its name and action:

            >>> updated_rule, _, error = client.zia.cloud_firewall_dns.add_rule(
            ...     rule_id='12455'
            ...     name=f"UpdateRule_{random.randint(1000, 10000)}",
            ...     description=f"UpdateRule_{random.randint(1000, 10000)}",
            ...     action='REDIR_REQ',
            ...     state="ENABLED",
            ...     order=1,
            ...     rank=7,
            ...     redirect_ip = "8.8.8.8"
            ...     protocols = ["ANY_RULE"]
            ...     dest_countries=["COUNTRY_CA", "COUNTRY_MX", "COUNTRY_AU", "COUNTRY_GB"],
            ...     locations=['54528', '5485857']
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
            /firewallDnsRules/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, FirewallDNSRules)
        if error:
            return (None, response, error)

        try:
            result = FirewallDNSRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> tuple:
        """
        Deletes the specified cloud firewall dns filter rule.

        Args:
            rule_id (str): The unique identifier for the cloud firewall dns rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.cloud_firewall_dns.delete_rule('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /firewallDnsRules/{rule_id}
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
