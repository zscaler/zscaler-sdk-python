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
from zscaler.utils import snake_to_camel, format_url
from zscaler.api_client import APIClient
from zscaler.zia.models.cloud_firewall_rules import FirewallRule
from zscaler.zia.models.cloud_firewall_destination_groups import IPDestinationGroups
from zscaler.zia.models.cloud_firewall_source_groups import IPSourceGroup
from zscaler.zia.models.cloud_firewall_nw_application_groups import NetworkApplicationGroups
from zscaler.zia.models.cloud_firewall_nw_applications import NetworkApplications
from zscaler.zia.models.cloud_firewall_nw_service_groups import NetworkServiceGroups
from zscaler.zia.models.cloud_firewall_nw_service import NetworkServices
from zscaler.zia.models.cloud_firewall_time_windows import TimeWindows
import logging

class FirewallPolicyAPI(APIClient):
    # Firewall filter rule keys that only require an ID to be provided.
    reformat_params = [
        ("app_services", "appServices"),
        ("app_service_groups", "appServiceGroups"),
        ("departments", "departments"),
        ("devices", "devices"),
        ("device_groups", "deviceGroups"),
        ("dest_ip_groups", "destIpGroups"),
        ("dest_ipv6_groups", "destIpv6Groups"),
        ("groups", "groups"),
        ("labels", "labels"),
        ("locations", "locations"),
        ("location_groups", "locationGroups"),
        ("nw_application_groups", "nwApplicationGroups"),
        ("nw_service_groups", "nwServiceGroups"),
        ("src_ip_groups", "srcIpGroups"),
        ("src_ipv6_groups", "srcIpv6Groups"),
        ("time_windows", "timeWindows"),
        ("users", "users"),
    ]

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists firewall rules in your organization with pagination.
        A subset of firewall rules  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of firewall rules instances, Response, error)

        Examples:
            >>> for rule in zia.firewall.list_rules():
            ...    pprint(rule)

        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /firewallFilteringRules
        """)

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(FirewallRule(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_rule(
        self,
        rule_id: int,
    ) -> tuple:
        """
        Returns information for the specified firewall filter rule.

        Args:
            rule_id (str): The unique identifier for the firewall filter rule.

        Returns:
            :obj:`Box`: The resource record for the firewall filter rule.

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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, FirewallRule)

        if error:
            return (None, response, error)

        try:
            result = FirewallRule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        rule: dict,
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
            :obj:`Box`: New firewall filter rule resource record.

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

        # Ensure the rule is passed as a dictionary
        if isinstance(rule, dict):
            body = rule
        else:
            body = rule.as_dict()

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, FirewallRule)

        if error:
            return (None, response, error)

        try:
            # Parse the response and return it as a FirewallRule object
            result = FirewallRule(self.form_response_body(response.get_body()))
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
            :obj:`Box`: The updated firewall filter rule resource record.

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
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        # transform_common_id_fields(self.reformat_params, payload, payload)

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

    def list_ip_destination_groups(self, exclude_type: str = None, query_params=None) -> tuple:
        """
        Returns a list of IP Destination Groups.

        Args:
            exclude_type (str): Exclude all groups that match the specified IP destination group's type.
                Accepted values are: `DSTN_IP`, `DSTN_FQDN`, `DSTN_DOMAIN`, and `DSTN_OTHER`.
            query_params (dict, optional): Additional query parameters for pagination or filtering.

        Returns:
            tuple: A tuple containing (list of IP Destination Group records, Response object, error).

            The list of IP Destination Group records is a list of dictionaries, each representing a group.
            Example:
            [
                {'id': 2590357, 'name': 'example100', 'type': 'DSTN_IP', 'addresses': ['1.1.1.1'], 'countries': [], 'ipCategories': []}
            ]

        Examples:
            >>> for group in zia.firewall.list_ip_destination_groups():
            ...    pprint(group)

        Raises:
            ValueError: If the exclude_type is not one of the supported values.

        """
        # Define supported values for exclude_type
        valid_exclude_types = {"DSTN_IP", "DSTN_FQDN", "DSTN_DOMAIN", "DSTN_OTHER"}

        # Validate exclude_type if provided
        if exclude_type and exclude_type not in valid_exclude_types:
            raise ValueError(f"Invalid exclude_type: {exclude_type}. Supported values are: {', '.join(valid_exclude_types)}")

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups
        """
        )

        query_params = query_params or {}

        # Add excludeType to query_params if it's provided
        if exclude_type:
            query_params["excludeType"] = exclude_type

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        # Parse the response into IPDestinationGroups instances
        try:
            result = []
            for item in response.get_results():
                result.append(IPDestinationGroups(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ip_destination_group(self, group_id: int) -> tuple:
        """
        Returns information on the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.

        Returns:
            tuple: The IP Destination Group resource record.

        Examples:
            >>> pprint(zia.firewall.get_ip_destination_group('287342'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, IPDestinationGroups)

        if error:
            return (None, response, error)

        try:
            result = IPDestinationGroups(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_ip_destination_group(self, **kwargs) -> tuple:
        """
        Adds a new IP Destination Group.

        Args:
            name (str): The name of the IP Destination Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            type (str): Destination IP group type. Allowed values are DSTN_IP and DSTN_FQDN.
            addresses (list): Destination IP addresses or FQDNs within the group.
            description (str): Additional information about the destination IP group.
            ip_categories (list): Destination IP address URL categories.
            countries (list): Destination IP address counties.

        Returns:
            :obj:`Box`: The newly created IP Destination Group resource record.

        Examples:
            Add a Destination IP Group with IP addresses:

            >>> zia.firewall.add_ip_destination_group(name='Destination Group - IP',
            ...    addresses=['203.0.113.0/25', '203.0.113.131'],
            ...    type='DSTN_IP')

            Add a Destination IP Group with FQDN:

            >>> zia.firewall.add_ip_destination_group(name='Destination Group - FQDN',
            ...    description='Covers domains for Example Inc.',
            ...    addresses=['example.com', 'example.edu'],
            ...    type='DSTN_FQDN')

            Add a Destionation IP Group for the US:

            >>> zia.firewall.add_ip_destination_group(name='Destination Group - US',
            ...    description='Covers the US',
            ...    countries=['COUNTRY_US'])

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups
        """
        )

        body = kwargs

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
            .execute(request, IPDestinationGroups)

        if error:
            return (None, response, error)

        try:
            result = IPDestinationGroups(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_ip_destination_group(
        self,
        group_id: str,
        **kwargs
    ) -> tuple:
        """
        Updates the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the IP Destination Group.
            addresses (list): Destination IP addresses or FQDNs within the group.
            description (str): Additional information about the IP Destination Group.
            ip_categories (list): Destination IP address URL categories.
            countries (list): Destination IP address countries.

        Returns:
            :obj:`Box`: The updated IP Destination Group resource record.

        Examples:
            Update the name of an IP Destination Group:

            >>> zia.firewall.update_ip_destination_group('9032667',
            ...    name="Updated IP Destination Group")

            Update the description and FQDNs for an IP Destination Group:

            >>> zia.firewall.update_ip_destination_group('9032668',
            ...    description="Tech News",
            ...    addresses=['arstechnica.com', 'slashdot.org'])

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/{group_id}
        """
        )

        body = {}

        body.update(kwargs)

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, IPDestinationGroups)
        if error:
            return (None, response, error)

        # Parse the response into a RuleLabels instance
        try:
            result = IPDestinationGroups(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_ip_destination_group(self, group_id: int) -> tuple:
        """
        Deletes the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            >>> zia.firewall.delete_ip_destination_group('287342')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/{group_id}
        """
        )
        params = {}
        
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=params)
        if error:
            return None, error

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def list_ip_source_groups(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns a list of all IP Source Groups.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.page] {int}: Specifies the page offset.
                [query_params.pagesize] {int}: Specifies the page size. The default size is 100, but the maximum size is 1000.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of IP Source Groups instances, Response, error)

        Examples:
            List all IP Source Groups:

            >>> for group in zia.firewall.list_ip_source_groups():
            ...    pprint(group)

            Use search parameter to find IP Source Groups with `fiji` in the name:

            >>> for group in zia.firewall.list_ip_source_groups('fiji'):
            ...    pprint(group)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(IPSourceGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ip_source_group(self, group_id: int) -> tuple:
        """
        Returns information for the specified IP Source Group.

        Args:
            group_id (str): The unique identifier for the source group.

        Examples:
            >>> pprint(zia.firewall.get_ip_source_group('762398')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, IPSourceGroup)

        if error:
            return (None, response, error)

        try:
            result = IPSourceGroup(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_ip_source_group(self, **kwargs) -> tuple:
        """
        Adds a new IP Source Group.

        Args:
            name (str): The name of the IP Source Group.
            ip_addresses (str): The list of IP addresses for the IP Source Group.
            description (str): Additional information for the IP Source Group.

        Returns:
            tuple: The new IP Source Group resource record.

        Examples:
            Add a new IP Source Group:

            >>> zia.firewall.add_ip_source_group(name='My IP Source Group',
            ...    ip_addresses=['198.51.100.0/24', '192.0.2.1'],
            ...    description='Contains the IP addresses for the local network.')

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups
        """
        )

        body = kwargs

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
            .execute(request, IPSourceGroup)
        if error:
            return (None, response, error)

        try:
            result = IPSourceGroup(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_ip_source_group(
        self,
        group_id: str, 
        **kwargs
    ) -> tuple:
        """
        Update an IP Source Group.

        This method supports updating individual fields in the IP Source Group resource record.

        Args:
            group_id (str): The unique ID for the IP Source Group to update.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the IP Source Group.
            ip_addresses (list): The list of IP addresses for the IP Source Group.
            description (str): Additional information for the IP Source Group.

        Returns:
            :obj:`Box`: The updated IP Source Group resource record.

        Examples:
            Update the name of an IP Source Group:

            >>> zia.firewall.update_ip_source_group('9032674',
            ...    name='Updated Name')

            Update the description and IP addresses of an IP Source Group:

            >>> zia.firewall.update_ip_source_group('9032674',
            ...    description='Local subnets, updated on 3 JUL 21'
            ...    ip_addresses=['192.0.2.0/29', '192.0.2.8/29', '192.0.2.128/25'])

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/{group_id}
        """
        )
        body = kwargs

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
            .execute(request, IPSourceGroup)
        if error:
            return (None, response, error)

        try:
            result = IPSourceGroup(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_ip_source_group(self, group_id: int) -> tuple:
        """
        Deletes an IP Source Group.

        Args:
            group_id (str): The unique ID of the IP Source Group to be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.firewall.delete_ip_source_group('762398')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/{group_id}
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

    def list_network_app_groups(self, query_params=None) -> tuple:
        """
        Returns a list of all Network Application Groups.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.page] {int}: Specifies the page offset.
                [query_params.pagesize] {int}: Specifies the page size. The default size is 100, but the maximum size is 1000.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of Network Application Group instances, Response, error)

        Examples:
            >>> for group in zia.firewall.list_network_app_groups():
            ...    pprint(group)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(NetworkApplicationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_network_app_group(
        self,
        group_id: int,
    ) -> tuple:
        """
        Returns information for the specified Network Application Group.

        Args:
            group_id (str):
                The unique ID for the Network Application Group.

        Returns:
             :obj:`FirewallRule`: The Network Application Group resource record.

        Examples:
            >>> pprint(zia.firewall.get_network_app_group('287342'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups/{group_id}
        """
        )
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkApplicationGroups)

        if error:
            return (None, response, error)

        try:
            result = NetworkApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_network_app_group(
        self,
        name: str,
        network_applications: list,
        **kwargs
    ) -> tuple:
        """
        Adds a new Network Application Group.

        Args:
            name (str): The name of the Network Application Group.
            description (str): Additional information about the Network Application Group.
            network_applications (list): A list of Application IDs to add to the group.

        Returns:
            :obj:`Box`: The newly created Network Application Group resource record.

        Examples:
            Add a new Network Application Group:

            >>> zia.firewall.add_network_app_group(name='New Network Application Group',
            ...    network_applications=['SALESFORCE', 'GOOGLEANALYTICS', 'OFFICE365'],
            ...    description='Additional information about the Network Application Group.')

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups
        """
        )

        payload = {
            "name": name,
            "networkApplications": network_applications,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        request, error = self._request_executor\
            .create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = NetworkApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_network_app_group(
        self,
        group_id: int,
        **kwargs
    ) -> tuple:
        """
        Update an Network Application Group.

        This method supports updating individual fields in the Network Application Group resource record.

        Args:
            group_id (str): The unique ID for the Network Application Group to update.

        Keyword Args:
            name (str): The name of the Network Application Group.
            network_applications (list): The list of applications for the Network Application Group.
            description (str): Additional information for the Network Application Group.

        Returns:
            :obj:`Box`: The updated Network Application Group resource record.

        Examples:
            Update the name of an Network Application Group:

            >>> zia.firewall.update_network_app_group('9032674',
            ...    name='Updated Network Application Group Name')

            Update the description and applications for a Network Application Group:

            >>> zia.firewall.update_network_app_group('9032674',
            ...    description='Network Application Group, updated on May 27, 2023'
            ...    network_applications=['SALESFORCE', 'GOOGLEANALYTICS', 'OFFICE365'])

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups/{group_id}
        """
        )

        body = {}

        body.update(kwargs)

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, NetworkApplicationGroups)

        if error:
            return (None, response, error)

        try:
            result = NetworkApplicationGroups(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_network_app_group(
        self,
        group_id: int,
    ) -> tuple:
        """
        Deletes the specified Network Application Group.

        Args:
            group_id (str): The unique identifier for the Network Application Group.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zia.firewall.delete_network_app_group('762398')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups/{group_id}
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

    def list_network_apps(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists Network Applications in your organization with pagination.
        A subset of Network Applications can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.locale] {str}: When set to one of the supported locales
                    (i.e., en-US, de-DE, es-ES, fr-FR, ja-JP, zh-CN), the network application
                    description is localized into the requested language.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of firewall rules instances, Response, error)

        Examples:
            >>> for app in zia.firewall.list_network_apps():
            ...    pprint(app)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplications
        """
        )

        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(NetworkApplications(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_network_app(self, app_id: int) -> tuple:
        """
        Returns information for the specified Network Application.

        Args:
            app_id (str): The unique ID for the Network Application.

        Examples:
            >>> pprint(zia.firewall.get_network_app('762398'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplications/{app_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, NetworkApplications)
        if error:
            return (None, response, error)

        try:
            result = NetworkApplications(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_network_svc_groups(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists network service groups in your organization with pagination.
        A subset of network service groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: List of Network Service Group resource records.

        Examples:
            >>> for group in zia.firewall.list_network_svc_groups():
            ...    pprint(group)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(NetworkServiceGroups(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_network_svc_group(self, group_id: int) -> tuple:
        """
        Returns information for the specified Network Service Group.

        Args:
            group_id (str): The unique ID for the Network Service Group.

        Examples:
            >>> pprint(zia.firewall.get_network_svc_group('762398'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, NetworkServiceGroups)

        if error:
            return (None, response, error)

        try:
            result = NetworkServiceGroups(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_network_svc_group(self, **kwargs) -> tuple:
        """
        Adds a new Network Service Group.

        Args:
            name (str): The name of the Network Service Group.
            service_ids (list): A list of Network Service IDs to add to the group.
            description (str): Additional information about the Network Service Group.

        Returns:
            :obj:`Box`: The newly created Network Service Group resource record.

        Examples:
            Add a new Network Service Group:

            >>> zia.firewall.add_network_svc_group(name='New Network Service Group',
            ...    service_ids=['159143', '159144', '159145'],
            ...    description='Group for the new Network Service.')

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups
        """
        )

        body = kwargs

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
            .execute(request, NetworkServiceGroups)

        if error:
            return (None, response, error)

        try:
            result = NetworkServiceGroups(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_network_svc_group(
        self,
        group_id: int,
        **kwargs
    ) -> tuple:
        """
        Update a Network Service Group.

        Args:
            group_id (str): The unique ID of the Network Service Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the Network Service Group.
            service_ids (list): A list of Network Service IDs to add to the group.
            description (str): Additional information about the Network Service Group.

        Returns:
            :obj:`Box`: The updated Network Service Group resource record.

        Examples:
            Update the name Network Service Group:

            >>> zia.firewall.update_network_svc_group(name='Update Network Service Group',
            ...    service_ids=['159143', '159144', '159145'],
            ...    description='Group for the new Network Service.')

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups/{group_id}
        """
        )

        body = kwargs

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, NetworkServiceGroups)
        if error:
            return (None, response, error)

        # Parse the response into a RuleLabels instance
        try:
            result = NetworkServiceGroups(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_network_svc_group(self, group_id: int) -> tuple:
        """
        Deletes the specified Network Service Group.

        Args:
            group_id (str): The unique identifier for the Network Service Group.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zia.firewall.delete_network_svc_group('762398')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups/{group_id}
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

    def list_network_services(self, query_params=None) -> tuple:
        """
        Lists network services in your organization with pagination.
        A subset of network services  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of network services instances, Response, error)

        Examples:
            >>> for service in zia.firewall.list_network_services():
            ...    pprint(service)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices
        """
        )
        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(NetworkServices(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_network_service(self, service_id: int) -> tuple:
        """
        Returns information for the specified Network Service.

        Args:
            service_id (str): The unique ID for the Network Service.

        Returns:
            :obj:`Box`: The Network Service resource record.

        Examples:
            >>> pprint(zia.firewall.get_network_service('762398'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices/{service_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, NetworkServices)

        if error:
            return (None, response, error)

        try:
            result = NetworkServices(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_network_service(
        self,
        ports: list = None,
        **kwargs
    ) -> tuple:
        """
        Adds a new Network Service.

        Args:
            name: The name of the Network Service
            ports (list):
                A list of port protocol tuples. Tuples must follow the convention `src/dest`, `protocol`,
                `start port`, `end port`. If this is a single port and not a port range then `end port` can be omitted.
                E.g.

                .. code-block:: python

                    ('src', 'tcp', '49152', '65535'),
                    ('dest', 'tcp', '22),
                    ('dest', 'tcp', '9010', '9012'),
                    ('dest', 'udp', '9010', '9012')

            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information on the Network Service.

        Returns:
            :obj:`Box`: The newly created Network Service resource record.

        Examples:
            Add Network Service for Microsoft Exchange:

            >>> zia.firewall.add_network_service('MS LDAP',
            ...    description='Covers all ports used by MS LDAP',
            ...    ports=[
            ...        ('dest', 'tcp', '389'),
            ...        ('dest', 'udp', '389'),
            ...        ('dest', 'tcp', '636'),
            ...        ('dest', 'tcp', '3268', '3269')])

            Add Network Service designed to match inbound SSH traffic:

            >>> zia.firewall.add_network_service('Inbound SSH',
            ...    description='Inbound SSH',
            ...    ports=[
            ...        ('src', 'tcp', '22'),
            ...        ('dest', 'tcp', '1024', '65535')])

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices
        """
        )

        # Set the payload based on the network_service argument
        body = kwargs

        # Add ports to the payload if provided
        if ports is not None:
            for items in ports:
                port_dict = {"start": int(items[2])}
                if len(items) == 4:
                    port_dict["end"] = int(items[3])
                body.setdefault(f"{items[0]}{items[1].title()}Ports", []).append(port_dict)

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
            .execute(request, NetworkServices)

        if error:
            return (None, response, error)

        try:
            result = NetworkServices(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_network_service(
        self,
        service_id: str,
        ports: list = None,
        **kwargs
    ) -> tuple:
        """
        Updates the specified Network Service.

        If ports aren't provided then no changes will be made to the ports already defined. If ports are provided then
        the existing ports will be overwritten.

        Args:
            service_id (str): The unique ID for the Network Service.
            ports (list):
                A list of port protocol tuples. Tuples must follow the convention `src/dest`, `protocol`, `start port`,
                `end port`. If this is a single port and not a port range then `end port` can be omitted. E.g.

                .. code-block:: python

                    ('src', 'tcp', '49152', '65535'),
                    ('dest', 'tcp', '22),
                    ('dest', 'tcp', '9010', '9012'),
                    ('dest', 'udp', '9010', '9012')

            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information on the Network Service.

        Returns:
            :obj:`dict`: The updated Network Service resource record.

        Examples:
            Update the name and description for a Network Service:

            >>> zia.firewall.update_network_service('959093',
            ...    name='MS Exchange',
            ...    description='All ports related to the MS Exchange service.')

            Updates the ports for a Network Service, leaving other fields intact:

            >>> zia.firewall.update_network_service('959093',
            ...    ports=[
            ...        ('dest', 'tcp', '500', '510')])

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices/{service_id}
        """
        )

        body = {}

        body.update(kwargs)

        # Add ports to the payload if provided
        if ports is not None:
            for items in ports:
                port_dict = {"start": int(items[2])}
                if len(items) == 4:
                    port_dict["end"] = int(items[3])
                body.setdefault(f"{items[0]}{items[1].title()}Ports", []).append(port_dict)

        # Create and send the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, {})

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, NetworkServices)

        if error:
            return (None, response, error)

        try:
            result = NetworkServices(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_network_service(self, service_id: int) -> tuple:
        """
        Deletes the specified Network Service.

        Args:
            service_id (str): The unique ID for the Network Service.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.firewall.delete_network_service('762398')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices/{service_id}
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

    def list_time_windows(self) -> tuple:
        """
        Returns a list of time intervals used by the Firewall policy or the URL Filtering policy.

        Returns:
            tuple: A list of TimeWindow model instances, the response object, and any error encountered.

        Examples:
            >>> result, response, error = zia.firewall.list_time_windows()

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeWindows
        """
        )

        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_body():
                result.append(TimeWindows(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_time_windows_lite(self) -> tuple:
        """
        Returns name and ID dictionary of time intervals used by the Firewall policy or the URL Filtering policy.

        Returns:
            tuple: A list of TimeWindowLite model instances, the response object, and any error encountered.

        Examples:
            >>> result, response, error = zia.firewall.list_time_windows_lite()

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeWindows/lite
        """
        )

        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request, associating with the TimeWindowLite model
        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TimeWindows(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
