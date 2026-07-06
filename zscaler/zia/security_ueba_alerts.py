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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.security_ueba_alerts import AlertDefinition, AlertRuleConfigurationWebhook


class SecurityUebaAlertsAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_alert_definitions(self, query_params=None) -> APIResult[List[AlertDefinition]]:
        """
        List alert_definitions.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AlertDefinition instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertDefinitions
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
                result.append(AlertDefinition(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_alert_definition(self, alert_definition_id: int) -> APIResult[AlertDefinition]:
        """
        Returns information for the specified alert_definition.

        Args:
            alert_definition_id (int): The unique identifier for the alert_definition.

        Returns:
            tuple: The resource record for the alert_definition.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertDefinitions/{alert_definition_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertDefinition)
        if error:
            return (None, response, error)
        try:
            result = AlertDefinition(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_alert_definition(self, **kwargs) -> APIResult[AlertDefinition]:
        """
        Adds a new alert_definition.

        Returns:
            tuple: The newly created alert_definition resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertDefinitions
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertDefinition)
        if error:
            return (None, response, error)
        try:
            result = AlertDefinition(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_alert_definition(self, alert_definition_id: int, **kwargs) -> APIResult[AlertDefinition]:
        """
        Updates an existing alert_definition.

        Args:
            alert_definition_id (int): The unique ID for the alert_definition being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated alert_definition resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertDefinitions/{alert_definition_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertDefinition)
        if error:
            return (None, response, error)
        try:
            result = AlertDefinition(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_alert_definition(self, alert_definition_id: int) -> APIResult[None]:
        """
        Deletes the specified alert_definition.

        Args:
            alert_definition_id (int): The unique identifier for the alert_definition.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertDefinitions/{alert_definition_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def list_alert_rule_configurations_rules(self, query_params=None) -> APIResult[List[AlertRuleConfigurationWebhook]]:
        """
        List alert_rule_configurations (rules).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AlertRuleConfigurationWebhook instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertRuleConfiguration/rules
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
                result.append(AlertRuleConfigurationWebhook(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_alert_rule_configurations_rules_rulestatus(
        self, query_params=None
    ) -> APIResult[List[AlertRuleConfigurationWebhook]]:
        """
        List alert_rule_configurations (rules/rulestatus).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AlertRuleConfigurationWebhook instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertRuleConfiguration/rules/rulestatus
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
                result.append(AlertRuleConfigurationWebhook(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_alert_rule_configurations_ueba_rules(self, query_params=None) -> APIResult[List[AlertRuleConfigurationWebhook]]:
        """
        List alert_rule_configurations (uebaRules).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AlertRuleConfigurationWebhook instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertRuleConfiguration/uebaRules
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
                result.append(AlertRuleConfigurationWebhook(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_alert_rule_configurations_webhooks(self, query_params=None) -> APIResult[List[AlertRuleConfigurationWebhook]]:
        """
        List alert_rule_configurations (webhooks).

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (list of AlertRuleConfigurationWebhook instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertRuleConfiguration/webhooks
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
                result.append(AlertRuleConfigurationWebhook(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_alert_rule_configuration(self, **kwargs) -> APIResult[AlertRuleConfigurationWebhook]:
        """
        Adds a new alert_rule_configuration.

        Returns:
            tuple: The newly created alert_rule_configuration resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertRuleConfiguration
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertRuleConfigurationWebhook)
        if error:
            return (None, response, error)
        try:
            result = AlertRuleConfigurationWebhook(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_alert_rule_configuration(
        self, alert_rule_configuration_id: int, **kwargs
    ) -> APIResult[AlertRuleConfigurationWebhook]:
        """
        Updates an existing alert_rule_configuration.

        Args:
            alert_rule_configuration_id (int): The unique ID for the alert_rule_configuration being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated alert_rule_configuration resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertRuleConfiguration/{alert_rule_configuration_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertRuleConfigurationWebhook)
        if error:
            return (None, response, error)
        try:
            result = AlertRuleConfigurationWebhook(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_alert_rule_configuration(self, alert_rule_configuration_id: int) -> APIResult[None]:
        """
        Deletes the specified alert_rule_configuration.

        Args:
            alert_rule_configuration_id (int): The unique identifier for the alert_rule_configuration.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /alertRuleConfiguration/{alert_rule_configuration_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
