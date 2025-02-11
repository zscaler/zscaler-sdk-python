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
from zscaler.api_client import APIClient
from zscaler.zia.models.cloud_firewall_rules import FirewallRule
from zscaler.utils import format_url, transform_common_id_fields, reformat_params

class FirewallPolicyAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        List firewall rules in your organization.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:
            tuple: A tuple containing (list of firewall rules instances, Response, error)

        Examples:
        >>> rules, response, error = zia.zia.cloud_firewall_rules.list_rules()
        ...    pprint(rule)

        >>> rules, response, error = zia.zia.cloud_firewall_rules.list_rules(
            query_params={"search": "Block malicious IPs and domains"})
        ...    pprint(rule)
        
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /firewallFilteringRules
        """)

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(
            http_method,
            api_url,
            body,
            headers,
            params=query_params
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(FirewallRule(
                    self.form_response_body(item))
                )
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [
                r for r in results
                if lower_search in (r.name.lower() if r.name else "")
            ]

        return (results, response, None)

    def get_rule(
        self,
        rule_id: int,
    ) -> tuple:
        """
        Returns information for the specified firewall filter rule.

        Args:
            rule_id (str): The unique identifier for the firewall filter rule.

        Returns:
            :obj:`Tuple`: The resource record for the firewall filter rule.

        Examples:
            >>> pprint(zia.firewall.get_rule('431233'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /firewallFilteringRules/{rule_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.\
            execute(request, FirewallRule)

        if error:
            return (None, response, error)

        try:
            result = FirewallRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        **kwargs,
    ) -> tuple:
        """
        Adds a new firewall filter rule.

        Args:
            name (str): Name of the rule, max 31 chars.
            action (str): Action for the rule.
            device_trust_levels (list): Device trust levels for the rule application.
                Values: `ANY`, `UNKNOWN_DEVICETRUSTLEVEL`, `LOW_TRUST`, `MEDIUM_TRUST`,
                `HIGH_TRUST`.

        Keyword Args:
            order (str): Rule order, defaults to the bottom.
            rank (str): Admin rank of the rule.
            state (str): Rule state ('ENABLED' or 'DISABLED').
            description (str): Rule description.
            src_ips (list): Source IPs for the rule. Accepts IP addresses or CIDR.
            dest_addresses (list): Destination IPs for the rule. Accepts IP addresses or CIDR.
            dest_ip_categories (list): IP address categories for the rule.
            dest_countries (list): Destination countries for the rule.
            predefined (bool): Indicates that the rule is predefined by using a true value
            default_rule (bool): Indicates whether the rule is the Default Cloud IPS Rule or not
            enable_full_logging (bool): If True, enables full logging.
            nw_applications (list): Network service applications for the rule.
            app_services (list): IDs for application services for the rule.
            app_service_groups (list): IDs for app service groups.
            departments (list): IDs for departments the rule applies to.
            dest_ip_groups (list): IDs for destination IP groups.
            dest_ipv6_groups (list): IDs for destination IPV6 groups.
            devices (list): IDs for devices managed by Zscaler Client Connector.
            device_groups (list): IDs for device groups managed by Zscaler Client Connector.
            groups (list): IDs for groups the rule applies to.
            labels (list): IDs for labels the rule applies to.
            locations (list): IDs for locations the rule applies to.
            location_groups (list): IDs for location groups.
            nw_application_groups (list): IDs for network application groups.
            nw_services (list): IDs for network services the rule applies to.
            nw_service_groups (list): IDs for network service groups.
            time_windows (list): IDs for time windows the rule applies to.
            users (list): IDs for users the rule applies to.

        Returns:
            :obj:`Tuple`: New firewall filter rule resource record.

        Examples:
            Add a rule to allow all traffic to Google DNS:

            >>> zia.firewall.add_rule(rank='7', dest_addresses=['8.8.8.8', '8.8.4.4'],
            ...    name='ALLOW_ANY_TO_GOOG-DNS', action='ALLOW', description='TT#1965432122')

            Block traffic to Quad9 DNS for Finance Group, send ICMP error:

            >>> zia.firewall.add_rule(rank='7', dest_addresses=['9.9.9.9'],
            ...    name='BLOCK_GROUP-FIN_TO_Q9-DNS', action='BLOCK_ICMP', groups=['95016183'],
            ...    description='TT#1965432122')
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /firewallFilteringRules
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"
            
        transform_common_id_fields(reformat_params, body, body)

        # Create the request
        request, error = self._request_executor\
            .create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, FirewallRule)

        if error:
            return (None, response, error)

        try:
            # Parse the response and return it as a FirewallRule object
            result = FirewallRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> tuple:
        """
        Updates an existing firewall filter rule.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            order (str): Rule order, defaults to the bottom.
            rank (str): Admin rank of the rule.
            state (str): Rule state ('ENABLED' or 'DISABLED').
            description (str): Rule description.
            src_ips (list): Source IPs for the rule. Accepts IP addresses or CIDR.
            dest_addresses (list): Destination IPs for the rule. Accepts IP addresses or CIDR.
            dest_ip_categories (list): IP address categories for the rule.
            dest_countries (list): Destination countries for the rule.
            predefined (bool): Indicates that the rule is predefined by using a true value
            default_rule (bool): Indicates whether the rule is the Default Cloud IPS Rule or not
            enable_full_logging (bool): If True, enables full logging.
            nw_applications (list): Network service applications for the rule.
            app_services (list): IDs for application services for the rule.
            app_service_groups (list): IDs for app service groups.
            departments (list): IDs for departments the rule applies to.
            dest_ip_groups (list): IDs for destination IP groups.
            dest_ipv6_groups (list): IDs for destination IPV6 groups.
            devices (list): IDs for devices managed by Zscaler Client Connector.
            device_groups (list): IDs for device groups managed by Zscaler Client Connector.
            groups (list): IDs for groups the rule applies to.
            labels (list): IDs for labels the rule applies to.
            locations (list): IDs for locations the rule applies to.
            location_groups (list): IDs for location groups.
            nw_application_groups (list): IDs for network application groups.
            nw_services (list): IDs for network services the rule applies to.
            nw_service_groups (list): IDs for network service groups.
            time_windows (list): IDs for time windows the rule applies to.
            users (list): IDs for users the rule applies to.

        Returns:
            :obj:`Tuple`: The updated firewall filter rule resource record.

        Examples:
            Update the destination IP addresses for a rule:

            >>> zia.firewall.update_rule('976598',
            ...    dest_addresses=['1.1.1.1'],
            ...    description="TT#1965232865")

            Update a rule to enable full logging:

            >>> zia.firewall.update_rule('976597',
            ...    enable_full_logging=True,
            ...    description="TT#1965232866")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /firewallFilteringRules/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"
            
        transform_common_id_fields(reformat_params, body, body)

        # Create the request
        request, error = self._request_executor\
            .create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response, error = self._request_executor\
            .execute(request, FirewallRule)
        if error:
            return (None, response, error)

        try:
            result = FirewallRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> tuple:
        """
        Deletes the specified firewall filter rule.

        Args:
            rule_id (str): The unique identifier for the firewall filter rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.firewall.delete_rule('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /firewallFilteringRules/{rule_id}
        """
        )

        params = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

