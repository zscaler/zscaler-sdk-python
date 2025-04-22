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

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.ztw.models.forwarding_rules import ForwardingControlRule
from zscaler.utils import format_url, transform_common_id_fields, reformat_params


class ForwardingControlRulesAPI(APIClient):

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists forwarding control rules rules in your organization with pagination.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of forwarding control rules instances, Response, error).

        Examples:
            Print all forwarding control rule

            >>> rule_list, response, error = ztw.forwarding_rules.list_rules()
            ... if error:
            ...     print(f"Error listing rules: {error}")
            ...     return
            ... print(f"Total rules found: {len(rule_list)}")
            ... for rule in rule_list:
            ...     print(rule.as_dict())

            Print a forwarding control rule that match the name 'Rule01'

            >>> rule_list, response, error = ztw.forwarding_rules.list_rules(query_params={"search": 'Rule01'})
            ... if error:
            ...     print(f"Error listing rules: {error}")
            ...     return
            ... print(f"Total rules found: {len(rule_list)}")
            ... for rule in rule_list:
            ...     print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecRules/ecRdr
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
                results.append(ForwardingControlRule(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def add_rule(self, **kwargs) -> tuple:
        """
        Adds a new forwarding control rule.

        Args:
            name (str): Name of the forwarding control rule, max 31 chars.
            action (str): Action to take place if the traffic matches the rule criteria

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule. Supported values 1-7
            forward_method (str): The type of traffic forwarding method selected from the available options
            Supported Values: `INVALID`, `DIRECT`, `PROXYCHAIN`, `ZIA`, `ZPA`, `ECZPA`, `ECSELF`, `DROP`

            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            description (str): Additional information about the rule
            groups (list): The IDs for the groups that this rule applies to.
            departments (list): IDs for departments the rule applies to.
            ec_groups (list): The IDs for the Zscaler Cloud Connector groups to which the forwarding rule applies.
            users (list): The IDs for the users that this rule applies to.
            protocols (list): The protocol criteria for the rule.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            src_ips (list): List of User-defined source IP addresses for which the rule is applicable.
            src_ip_groups (list): The IDs for the Source IP address groups for which the rule is applicable.
            src_ipv6_groups (list): The IDs for theSource IPv6 address groups for which the rule is applicable.
            dest_addresses (list): List of destination IP addresses, CIDRs or FQDNs for which the rule is applicable.
            dest_ip_categories (list): List of destination IP categories to which the rule applies.
            res_categories (list): List of destination domain categories to which the rule applies.
            dest_countries (list): List of Destination countries for which the rule is applicable.
            dest_countries (list): List of Destination countries for which the rule is applicable.
            dest_ip_groups (list): IDs for destination IP groups.
            dest_ipv6_groups (list): IDs for destination IPV6 groups.
            nw_services (list): IDs for network services the rule applies to.
            nw_service_groups (list): IDs for network service groups.
            nw_application_groups (list): IDs for network application groups.
            device_groups (list): Device groups managed using Zscaler Client Connector.
            devices (list): Devices managed using Zscaler Client Connector.

            zpa_app_segments (list[dict]): **ZPA Application Segments applicable to the rule.**
                - `external_id` (str): Indicates the external ID. Applicable only when this reference is of an external entity.
                - `name` (str): The name of the Application Segment.

            proxy_gateway (dict or list[dict]): **Proxy Gateway resource(s) applicable to the rule.**
                - `id` (int, optional): The unique identifier for the proxy gateway.
                - `name` (str): The name of the Proxy Gateway.

            zpa_gateway (dict or list[dict]): **ZPA Gateway resource(s) applicable to the rule.**
                - `id` (int, optional): The unique identifier for the ZPA Gateway.
                - `name` (str): The name of the ZPA Gateway.

        Returns:
            :obj:`Tuple`: New forwarding control rule resource record.

        Example:
            Add a DIRECT forwarding control rule:

            >>> ztw.forwarding_rules.add_rule(
            ...    name='FWD_DIRECT#01',
            ...    state="ENABLED",
            ...    order=1,
            ...    type="FORWARDING",
            ...    forward_method="DIRECT",
            ...    src_ips= ["192.168.200.200"],
            ...    dest_addresses=["192.168.255.1"],
            ...    dest_ip_categories=["ZSPROXY_IPS"],
            ...    dest_countries=["COUNTRY_CA", "COUNTRY_US"],
            ... )

            Add a ZPA forwarding control rule:

            >>> ztw.forwarding_rules.add_rule(
            ...    name='FWD_DIRECT#01',
            ...    state="ENABLED",
            ...    order=1,
            ...    type="FORWARDING",
            ...    forward_method="ZPA",
            ...    src_ips= ["192.168.200.200"],
            ...    dest_addresses=["192.168.255.1"],
            ...    dest_ip_categories=["ZSPROXY_IPS"],
            ...    dest_countries=["COUNTRY_CA", "COUNTRY_US"],
            ...    zpa_gateway={
            ...     "name": "ZPAGW01",
            ...     "external_id": "2"
            ...    }
            ...    zpa_app_segments=[
            ...    {
            ...     "name": "Inspect App Segments",
            ...     "external_id": "2"
            ...     }
            ...    ]
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecRules/ecRdr
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ForwardingControlRule)
        if error:
            return (None, response, error)

        try:
            result = ForwardingControlRule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: str, **kwargs) -> tuple:
        """
        Adds a new forwarding control rule.

        Args:
            name (str): Name of the forwarding control rule, max 31 chars.
            action (str): Action to take place if the traffic matches the rule criteria

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule. Supported values 1-7
            forward_method (str): The type of traffic forwarding method selected from the available options
            Supported Values: `INVALID`, `DIRECT`, `PROXYCHAIN`, `ZIA`, `ZPA`, `ECZPA`, `ECSELF`, `DROP`

            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            description (str): Additional information about the rule
            groups (list): The IDs for the groups that this rule applies to.
            departments (list): IDs for departments the rule applies to.
            ec_groups (list): The IDs for the Zscaler Cloud Connector groups to which the forwarding rule applies.
            users (list): The IDs for the users that this rule applies to.
            protocols (list): The protocol criteria for the rule.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            src_ips (list): List of User-defined source IP addresses for which the rule is applicable.
            src_ip_groups (list): The IDs for the Source IP address groups for which the rule is applicable.
            src_ipv6_groups (list): The IDs for theSource IPv6 address groups for which the rule is applicable.
            dest_addresses (list): List of destination IP addresses, CIDRs or FQDNs for which the rule is applicable.
            dest_ip_categories (list): List of destination IP categories to which the rule applies.
            res_categories (list): List of destination domain categories to which the rule applies.
            dest_countries (list): List of Destination countries for which the rule is applicable.
            dest_countries (list): List of Destination countries for which the rule is applicable.
            dest_ip_groups (list): IDs for destination IP groups.
            dest_ipv6_groups (list): IDs for destination IPV6 groups.
            nw_services (list): IDs for network services the rule applies to.
            nw_service_groups (list): IDs for network service groups.
            nw_application_groups (list): IDs for network application groups.
            device_groups (list): Device groups managed using Zscaler Client Connector.
            devices (list): Devices managed using Zscaler Client Connector.

            zpa_app_segments (list[dict]): **ZPA Application Segments applicable to the rule.**
                - `external_id` (str): Indicates the external ID. Applicable only when this reference is of an external entity.
                - `name` (str): The name of the Application Segment.

            proxy_gateway (dict or list[dict]): **Proxy Gateway resource(s) applicable to the rule.**
                - `id` (int, optional): The unique identifier for the proxy gateway.
                - `name` (str): The name of the Proxy Gateway.

            zpa_gateway (dict or list[dict]): **ZPA Gateway resource(s) applicable to the rule.**
                - `id` (int, optional): The unique identifier for the ZPA Gateway.
                - `name` (str): The name of the ZPA Gateway.

        Returns:
            :obj:`Tuple`: New forwarding control rule resource record.

        Example:
            Update the src_ips in the DIRECT forwarding control rule:

            >>> ztw.forwarding_rules.add_rule(
            ...    rule_id='282458',
            ...    name='FWD_DIRECT#01',
            ...    state="ENABLED",
            ...    order=1,
            ...    type="FORWARDING",
            ...    forward_method="DIRECT",
            ...    src_ips= ["192.168.200.205"],
            ...    dest_addresses=["192.168.255.1"],
            ...    dest_ip_categories=["ZSPROXY_IPS"],
            ...    dest_countries=["COUNTRY_CA", "COUNTRY_US"],
            ... )

            Update a ZPA forwarding control rule:

            >>> ztw.forwarding_rules.add_rule(
            ...    name='FWD_DIRECT#01',
            ...    state="ENABLED",
            ...    order=1,
            ...    type="FORWARDING",
            ...    forward_method="ZPA",
            ...    src_ips= ["192.168.200.200"],
            ...    dest_addresses=["192.168.255.1"],
            ...    dest_ip_categories=["ZSPROXY_IPS"],
            ...    dest_countries=["COUNTRY_CA", "COUNTRY_US"],
            ...    zpa_gateway={
            ...     "name": "ZPAGW01",
            ...     "external_id": "2"
            ...    }
            ...    zpa_app_segments=[
            ...    {
            ...     "name": "Inspect App Segments",
            ...     "external_id": "2"
            ...     }
            ...    ]
            ... )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /ecRules/ecRdr/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ForwardingControlRule)
        if error:
            return (None, response, error)

        try:
            result = ForwardingControlRule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
