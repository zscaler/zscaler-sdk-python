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
from zscaler.zia.models.forwarding_control_policy import ForwardingControlRule
from zscaler.zia.models.proxy_gatways import ProxyGatways
from zscaler.utils import format_url
from zscaler.utils import (
    convert_keys,
    recursive_snake_to_camel,
    snake_to_camel,
    transform_common_id_fields,
)




class ForwardingControlAPI(APIClient):
    # Forwarding Control filter rule keys that only require an ID to be provided.
    reformat_params = [
        ("app_service_groups", "appServiceGroups"),
        ("departments", "departments"),
        ("devices", "devices"),
        ("device_groups", "deviceGroups"),
        ("dest_ip_groups", "destIpGroups"),
        ("dest_ipv6_groups", "destIpv6Groups"),
        ("ec_groups", "ecGroups"),
        ("groups", "groups"),
        ("labels", "labels"),
        ("locations", "locations"),
        ("location_groups", "locationGroups"),
        ("nw_application_groups", "nwApplicationGroups"),
        ("nw_services", "nwServices"),
        ("nw_service_groups", "nwServiceGroups"),
        ("proxy_gateway", "proxyGateway"),
        ("src_ip_groups", "srcIpGroups"),
        ("src_ipv6_groups", "srcIpv6Groups"),
        ("users", "users"),
        ("zpa_gateway", "zpaGateway"),
        ("zpa_app_segments", "zpaAppSegments"),
        ("zpa_application_segments", "zpaApplicationSegments"),
        ("zpa_application_segment_groups", "zpaApplicationSegmentGroups"),
    ]

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(self) -> tuple:
        """
        Lists forwarding control rules rules in your organization with pagination.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of forwarding control rules instances, Response, error).
        """
        http_method = "get".upper()
        api_url = f"{self._zia_base_endpoint}/forwardingRules"

        request, error = self._request_executor.\
            create_request(http_method, api_url, {}, {})
        if error:
            return error

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ForwardingControlRule(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_rule(self, rule_id: str) -> tuple:
        """
        Returns information for the specified forwarding control filter rule.
        """
        http_method = "get".upper()
        api_url = f"{self._zia_base_endpoint}/forwardingRules/{rule_id}"

        request, error = self._request_executor.\
            create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, ForwardingControlRule)
        if error:
            return (None, response, error)
        try:
            result = ForwardingControlRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(self, name: str, forward_method: str, **kwargs) -> tuple:
        """
        Adds a new forwarding control filter rule.
        """
        http_method = "post".upper()
        api_url = f"{self._zia_base_endpoint}/forwardingRules"

        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        payload = {
            "name": name,
            "forwardMethod": forward_method,
            "order": kwargs.pop("order", len(self.list_rules())),
        }

        transform_common_id_fields(self.reformat_params, kwargs, payload)
        for key, value in kwargs.items():
            if value is not None:
                payload[snake_to_camel(key)] = value

        camel_payload = recursive_snake_to_camel(payload)

        request, error = self._request_executor\
            .create_request(http_method, api_url, camel_payload, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = ForwardingControlRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: str, **kwargs) -> tuple:
        """
        Updates an existing forwarding control filter rule.
        """
        http_method = "put".upper()
        api_url = f"{self._zia_base_endpoint}/forwardingRules/{rule_id}"

        payload = convert_keys(self.get_rule(rule_id))

        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        transform_common_id_fields(self.reformat_params, kwargs, payload)
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        request, error = self._request_executor.\
            create_request(http_method, api_url, payload, {})
        if error:
            return error

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (None, response, error)

        try:
            result = ForwardingControlRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: str) -> tuple:
        """
        Deletes the specified forwarding control filter rule.
        """
        http_method = "delete".upper()
        api_url = f"{self._zia_base_endpoint}/forwardingRules/{rule_id}"

        request, error = self._request_executor.\
            create_request(http_method, api_url, {}, {})
        if error:
            return (None, error)

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (response, error)

        return (response, None)

    def get_proxy_gateways(self) -> tuple:
        """
        Retrieves a list of Proxy Gateways.

        Returns:
            tuple: A tuple containing:
                N/A

        Examples:
            >>> proxy, response, err = client.zia.forwarding_control.get_proxy_gateways()

        """

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /proxyGateways
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers)

        if error:
            return None

        response, error = self._request_executor.execute(request)
        if error:
            return None

        try:
            result = []
            for item in response.get_results():
                result.append(ProxyGatways(self.form_response_body(item))
            )
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
