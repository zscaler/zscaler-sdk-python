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
from zscaler.request_executor import RequestExecutor
from zscaler.api_client import APIClient
from zscaler.zia.models.traffic_capture import TrafficCapture, TrafficCaptureRuleLabels
from zscaler.utils import format_url, transform_common_id_fields, reformat_params
from zscaler.types import APIResult


class TrafficCaptureAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params: Optional[dict] = None,
    ) -> APIResult[List[TrafficCapture]]:
        """
       Retrieves the list of Traffic Capture policy rules configured in the ZIA Admin Portal

        See the
        `Traffic Capture Policy API reference (list rules):
        <https://help.zscaler.com/zia/traffic-capture-policy#/trafficCaptureRules-get>`_
        for further detail on optional keyword parameter structures.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.rule_name]`` {str}: Filters rules based on rule names using the specified keywords
                ``[query_params.rule_label]`` {str}: Filters rules based on rule labels using the specified keywords
                ``[query_params.rule_id]`` {str}: Filter based on the rule label ID
                ``[query_params.rule_order]`` {str}: Filters rules based on rule order using the specified keywords
                ``[query_params.rule_description]`` {str}: Filters rules based on descriptions using the specified keywords
                ``[query_params.rule_action]`` {str}: Filters rules based on rule actions using the specified keywords
                ``[query_params.location]`` {str}: Filters rules based on locations using the specified keywords
                ``[query_params.department]`` {str}: Filters rules based on user departments using the specified keywords
                ``[query_params.group]`` {str}: Filters rules based on user groups using the specified keywords
                ``[query_params.user]`` {str}: Filters rules based on users using the specified keywords
                ``[query_params.device]`` {str}: Filters rules based on devices using the specified keywords
                ``[query_params.device_group]`` {str}: Filters rules based on device groups using the specified keywords
                ``[query_params.device_trust_level]`` {str}: Filters rules based on device trust levels using keywords
                ``[query_params.page]`` {str}: Specifies the page offset
                ``[query_params.page_size]`` {str}: Specifies the page size. Default size is set to 5,000 if not specified.

        Returns:
            tuple: A tuple containing (list of traffic capture rules instances, Response, error)

        Examples:
        >>> rules, response, error = zia.traffic_capture.list_rules()
        ...    pprint(rule)

        >>> rules, response, error = zia.traffic_capture.list_rules(
            query_params={"group": "Engineering"})
        ...    pprint(rule)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /trafficCaptureRules
        """
        )

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
                result.append(TrafficCapture(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_rule(
        self,
        rule_id: int,
    ) -> APIResult[TrafficCapture]:
        """
        Retrieves the Traffic Capture policy rule based on the specified rule ID

        Args:
            rule_id (str): Specifies the rule ID. This value can be obtained using the GET /trafficCaptureRules request.

        Returns:
            :obj:`Tuple`: The resource record for the traffic capture rule.

        Examples:
            >>> fetched_rule, _, error = client.zia.traffic_capture.get_rule('1456549')
            >>> if error:
            ...     print(f"Error fetching rule by ID: {error}")
            ...     return
            ... print(f"Fetched rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /trafficCaptureRules/{rule_id}
            """
        )
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TrafficCapture)

        if error:
            return (None, response, error)

        try:
            result = TrafficCapture(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(
        self,
        **kwargs,
    ) -> APIResult[TrafficCapture]:
        """
        Adds a new traffic Capture Policy Rule.

        See the
        `Traffic Capture Policy API reference (add rule):
        <https://help.zscaler.com/zia/traffic-capture-policy#/trafficCaptureRules-post>`_
        for further detail on optional keyword parameter structures.

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
            predefined (bool): Indicates whether this is a predefined rule by using the true value
            default_rule (bool): Indicates whether this is a default rule by using the true value
            nw_applications (list): Network service applications for the rule.
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

            txn_size_limit (str): The maximum size of traffic to capture per
                connection. Supported values: `NONE`, `UNLIMITED`,
                `THIRTY_TWO_KB`, `TWO_FIFTY_SIX_KB`, `TWO_MB`, `FOUR_MB`,
                `THIRTY_TWO_MB`, `SIXTY_FOUR_MB`

            txn_sampling (str): The percentage of connections sampled for
                capturing each time the rule is triggered. Supported values:
                `NONE`, `ONE_PERCENT`, `TWO_PERCENT`, `FIVE_PERCENT`,
                `TEN_PERCENT`, `TWENTY_FIVE_PERCENT`, `HUNDRED_PERCENT`

        Returns:
            :obj:`Tuple`: New traffic capturerule resource record.

        Examples:
            Add a rule to allow all traffic to Google DNS:

            >>> added_rule, _, error = client.zia.traffic_capture.add_rule(
            ...     name=f"NewRule {random.randint(1000, 10000)}",
            ...     description=f"NewRule {random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     order=1,
            ...     rank=7,
            ...     action='ALLOW',
            ...     enable_full_logging=True,
            ...     src_ips=['192.168.100.0/24', '192.168.200.1'],
            ...     dest_addresses=['3.217.228.0-3.217.231.255', 'server1.acme.com', '*.acme.com'],
            ...     exclude_src_countries=True,
            ...     source_countries=['COUNTRY_AD', 'COUNTRY_AE', 'COUNTRY_AF'],
            ...     dest_countries=['COUNTRY_BR', 'COUNTRY_CA', 'COUNTRY_US'],
            ...     device_trust_levels=['UNKNOWN_DEVICETRUSTLEVEL', 'LOW_TRUST', 'MEDIUM_TRUST', 'HIGH_TRUST'],
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
            /trafficCaptureRules
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

        response, error = self._request_executor.execute(request, TrafficCapture)

        if error:
            return (None, response, error)

        try:
            result = TrafficCapture(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> APIResult[TrafficCapture]:
        """
        Updates an existing traffic capturerule.

        See the
        `Traffic Capture Policy API reference (update rule):
        <https://help.zscaler.com/zia/traffic-capture-policy#/trafficCaptureRules/{ruleId}-put>`_
        for further detail on optional keyword parameter structures.

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
            predefined (bool): Indicates whether this is a predefined rule by using the true value
            default_rule (bool): Indicates whether this is a default rule by using the true value
            nw_applications (list): Network service applications for the rule.
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

            txn_size_limit (str): The maximum size of traffic to capture per
                connection. Supported values: `NONE`, `UNLIMITED`,
                `THIRTY_TWO_KB`, `TWO_FIFTY_SIX_KB`, `TWO_MB`, `FOUR_MB`,
                `THIRTY_TWO_MB`, `SIXTY_FOUR_MB`

            txn_sampling (str): The percentage of connections sampled for
                capturing each time the rule is triggered. Supported values:
                `NONE`, `ONE_PERCENT`, `TWO_PERCENT`, `FIVE_PERCENT`,
                `TEN_PERCENT`, `TWENTY_FIVE_PERCENT`, `HUNDRED_PERCENT`

        Returns:
            :obj:`Tuple`: The updated traffic capturerule resource record.

        Examples:
            Update the destination IP addresses for a rule:

            >>>  added_rule, _, error = client.zia.traffic_capture.update_rule(
            ...     rule_id='12455'
            ...     name=f"NewRule {random.randint(1000, 10000)}",
            ...     description=f"NewRule {random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     order=1,
            ...     rank=7,
            ...     action='ALLOW',
            ...     enable_full_logging=True,
            ...     src_ips=['192.168.100.0/24', '192.168.200.1'],
            ...     dest_addresses=['3.217.228.0-3.217.231.255', 'server1.acme.com', '*.acme.com'],
            ...     exclude_src_countries=True,
            ...     source_countries=['COUNTRY_AD', 'COUNTRY_AE', 'COUNTRY_AF'],
            ...     dest_countries=['COUNTRY_BR', 'COUNTRY_CA', 'COUNTRY_US'],
            ...     dest_ip_categories=['BOTNET', 'MALWARE_SITE', 'PHISHING', 'SUSPICIOUS_DESTINATION'],
            ...     device_trust_levels=['UNKNOWN_DEVICETRUSTLEVEL', 'LOW_TRUST', 'MEDIUM_TRUST', 'HIGH_TRUST'],
            ... )
            >>> if error:
            ...     print(f"Error adding rule: {error}")
            ...     return
            ... print(f"Rule added successfully: {added_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /trafficCaptureRules/{rule_id}
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response, error = self._request_executor.execute(request, TrafficCapture)
        if error:
            return (None, response, error)

        try:
            result = TrafficCapture(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> APIResult[None]:
        """
        Deletes the specified traffic capturerule.

        See the
        `Traffic Capture Policy API reference (delete rule):
        <https://help.zscaler.com/zia/traffic-capture-policy#/trafficCaptureRules/{ruleId}-delete>`_
        for further detail.

        Args:
            rule_id (str): The unique identifier for the traffic capturerule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, error = client.zia.traffic_capture.delete_rule('54528')
            >>> if error:
            ...     print(f"Error deleting rule: {error}")
            ...     return
            ... print(f"Rule with ID {updated_rule.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /trafficCaptureRules/{rule_id}
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

    def list_traffic_capture_rule_order(self) -> APIResult[dict]:
        """
        Retrieves the rule order information for the Traffic Capture policy, including the admin rank
        and rule order mappings and the maximum configured rule order.

        See the
        `Traffic Capture Policy API reference (rule order):
        <https://help.zscaler.com/zia/traffic-capture-policy#/trafficCaptureRules/order-get>`_
        for further detail.

        Returns:
            :obj:`Tuple`: A tuple containing a dictionary with rule order information, the response
            object, and error if any.

            The dictionary contains:
                - ``ruleOrderRange`` (dict): Admin rank mapping with the rule order (represented
                  in a range) where keys are admin ranks and values are rule order strings.
                - ``maxOrderConfigured`` (int): The maximum rule order assigned to the Traffic
                  Capture policy rules.

        Examples:
            >>> rule_order_info, _, error = client.zia.traffic_capture.list_traffic_capture_rule_order()
            ... if error:
            ...     print(f"Error getting traffic capture rule order: {error}")
            ...     return
            ... print(f"Rule order range: {rule_order_info.get('ruleOrderRange')}")
            ... print(f"Max order configured: {rule_order_info.get('maxOrderConfigured')}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /trafficCaptureRules/order
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def traffic_capture_rule_count(self) -> APIResult[List[TrafficCapture]]:
        """
        Retrieves the rule count for Traffic Capture policy based on the specified search criteria

        If no search criteria are specified, the total number of Traffic Capture policy rules is retrieved by default.

        See the
        `Traffic Capture Policy API reference (rule count):
        <https://help.zscaler.com/zia/traffic-capture-policy#/trafficCaptureRules/count-get>`_
        for further detail.

        Returns:
            :obj:`Tuple`: A tuple containing a list of TrafficCapture instances with configuration
            count information, the response object, and error if any.

        Examples:
            >>> counts, _, error = client.zia.traffic_capture.traffic_capture_rule_count()
            ... if error:
            ...     print(f"Error getting traffic capture rule count: {error}")
            ...     return
            ... print(f"Found {len(counts)} count records:")
            ... for count in counts:
            ...     print(count.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /trafficCaptureRules/count
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TrafficCapture(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_rule_labels(
        self,
        query_params: Optional[dict] = None,
    ) -> APIResult[List[TrafficCapture]]:
        """
       Retrieves the list of Traffic Capture policy rules configured in the ZIA Admin Portal

        See the
        `Traffic Capture Policy API reference (rule labels):
        <https://help.zscaler.com/zia/traffic-capture-policy#/trafficCaptureRules/ruleLabels-get>`_
        for further detail on optional keyword parameter structures.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search_by_field]`` (str, optional): Search option based on specific rule fields
                    Supported values: `RULE_NAME`, `RULE_LABEL`, `RULE_ORDER`, `RULE_DESCRIPTION`, `RULE_ACTION`,
                        `LOCATION`, `DEPARTMENT`, `GROUP`, `USER`, `DEVICE`

                ``[query_params.search_by_value]`` {str}: Search option based on specified values for rule fields
                ``[query_params.page]`` {str}: Specifies the page offset
                ``[query_params.page_size]`` {str}: Specifies the page size. Default size is 1024

        Returns:
            tuple: A tuple containing (list of traffic capture rule labels instances, Response, error)

        Examples:
        >>> rules, response, error = zia.traffic_capture.list_rule_labels()
        ...    pprint(rule)

        >>> rules, response, error = zia.traffic_capture.list_rule_labels(
            query_params={"search_by_field": "RULE_NAME"})
        ...    pprint(rule)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /trafficCaptureRules/ruleLabels
        """
        )

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
                result.append(TrafficCaptureRuleLabels(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
