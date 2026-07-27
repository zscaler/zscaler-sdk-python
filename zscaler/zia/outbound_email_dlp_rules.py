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
from zscaler.zia.models.outbound_email_dlp_rules import OutboundEmailDlpRules


class OutboundEmailDLPRulesAPI(APIClient):
    """
    A Client object for the Outbound Email DLP Rules resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(self, query_params: Optional[dict] = None) -> APIResult[List[OutboundEmailDlpRules]]:
        """
        Lists the outbound email DLP rules configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.org_id]`` {int}: Filters the results for the specified organization.

        Returns:
            tuple: A tuple containing (list of OutboundEmailDlpRules instances, Response, error)

        Examples:
            List outbound email DLP rules:

            >>> rule_list, _, error = client.zia.outbound_email_dlp_rules.list_rules()
            >>> if error:
            ...     print(f"Error listing outbound email DLP rules: {error}")
            ...     return
            ... print(f"Total outbound email DLP rules found: {len(rule_list)}")
            ... for rule in rule_list:
            ...     print(rule.as_dict())

            List outbound email DLP rules using filters:

            >>> rule_list, _, error = client.zia.outbound_email_dlp_rules.list_rules(
            ...     query_params={'org_id': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing outbound email DLP rules: {error}")
            ...     return
            ... print(f"Total outbound email DLP rules found: {len(rule_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailDlpRules
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
                result.append(OutboundEmailDlpRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_rule(self, rule_id: int) -> APIResult[OutboundEmailDlpRules]:
        """
        Fetches a specific outbound email DLP rule by ID.

        Args:
            rule_id (int): The unique identifier for the outbound email DLP rule.

        Returns:
            tuple: A tuple containing (OutboundEmailDlpRules instance, Response, error).

        Examples:
            Print a specific outbound email DLP rule:

            >>> fetched_rule, _, error = client.zia.outbound_email_dlp_rules.get_rule(1013)
            >>> if error:
            ...     print(f"Error fetching outbound email DLP rule by ID: {error}")
            ...     return
            ... print(f"Fetched outbound email DLP rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailDlpRules/{rule_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, OutboundEmailDlpRules)
        if error:
            return (None, response, error)

        try:
            result = OutboundEmailDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_rules_lite(self, query_params: Optional[dict] = None) -> APIResult[List[OutboundEmailDlpRules]]:
        """
        Lists a lightweight version of the outbound email DLP rules.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of OutboundEmailDlpRules instances, Response, error)

        Examples:
            List outbound email DLP rules:

            >>> rule_list, _, error = client.zia.outbound_email_dlp_rules.list_rules_lite()
            >>> if error:
            ...     print(f"Error listing outbound email DLP rules: {error}")
            ...     return
            ... print(f"Total outbound email DLP rules found: {len(rule_list)}")
            ... for rule in rule_list:
            ...     print(rule.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailDlpRules/lite
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
                result.append(OutboundEmailDlpRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(self, **kwargs) -> APIResult[OutboundEmailDlpRules]:
        """
        Creates a new outbound email DLP rule.

        Args:
            name (str): The name of the outbound email DLP rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            order (int): The order of the outbound email DLP rule, defaults to adding the outbound email DLP rule to the bottom of the list.
            description (str): Additional information about the outbound email DLP rule.
            state (str): The outbound email DLP rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            action (str): The action taken when traffic matches the outbound email DLP rule criteria.
            min_size (int): The min size for this outbound email DLP rule.
            without_content_inspection (bool): A Boolean value indicating whether without content inspection applies to this outbound email DLP rule.
            external_auditor_email (str): The email address of an external auditor to whom DLP email notifications are sent.
            severity (str): The severity level assigned to the outbound email DLP rule.
            parent_rule (int): The parent rule for this outbound email DLP rule.
            custom_header (str): The custom header for this outbound email DLP rule.
            groups (list): The IDs for the groups that this outbound email DLP rule applies to.
            departments (list): The IDs for the departments that this outbound email DLP rule applies to.
            users (list): The IDs for the users that this outbound email DLP rule applies to.
            excluded_groups (list): The IDs for the excluded groups that this outbound email DLP rule applies to.
            excluded_departments (list): The IDs for the excluded departments that this outbound email DLP rule applies to.
            excluded_users (list): The IDs for the excluded users that this outbound email DLP rule applies to.
            time_windows (list): The IDs for the time windows that this outbound email DLP rule applies to.
            dlp_engines (list): The IDs for the dlp engines that this outbound email DLP rule applies to.
            file_types (list): The list of file types for this outbound email DLP rule.
            labels (list): The IDs for the labels that this outbound email DLP rule applies to.
            included_domain_profiles (list): The IDs for the included domain profiles that this outbound email DLP rule applies to.
            user_risk_score_levels (list): The list of user risk score levels for this outbound email DLP rule. Accepted values include e.g. ``LOW``.
            email_tenants (list): The IDs for the email tenants that this outbound email DLP rule applies to.
            content_locations (list): The list of content locations for this outbound email DLP rule. Accepted values include e.g. ``ANY``.
            sub_rules (list): The IDs for the sub rules that this outbound email DLP rule applies to.
            email_recipient_profiles (list): The IDs for the email recipient profiles that this outbound email DLP rule applies to.
            auditor (dict): The ID of the auditor for this outbound email DLP rule, e.g. ``{'id': 12345}``.
            notification_template (dict): The ID of the notification template for this outbound email DLP rule, e.g. ``{'id': 12345}``.
            receiver (dict): The ID of the receiver for this outbound email DLP rule, e.g. ``{'id': 12345}``.

        Returns:
            tuple: A tuple containing the newly added OutboundEmailDlpRules instance, response, and error.

        Examples:
            Add a new outbound email DLP rule:

            >>> added_rule, _, error = client.zia.outbound_email_dlp_rules.add_rule(
            ...     name=f"NewRule_{random.randint(1000, 10000)}",
            ...     description=f"NewRule_{random.randint(1000, 10000)}",
            ...     state='ENABLED',
            ...     action='ALLOW',
            ...     order=1,
            ...     severity='RULE_SEVERITY_HIGH',
            ...     user_risk_score_levels=['LOW'],
            ... )
            >>> if error:
            ...     print(f"Error adding outbound email DLP rule: {error}")
            ...     return
            ... print(f"Outbound email dlp rule added successfully: {added_rule.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailDlpRules
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, OutboundEmailDlpRules)
        if error:
            return (None, response, error)

        try:
            result = OutboundEmailDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: int, **kwargs) -> APIResult[OutboundEmailDlpRules]:
        """
        Updates information for the specified outbound email DLP rule.

        Args:
            rule_id (int): The unique identifier for the outbound email DLP rule.

        Keyword Args:
            name (str): The name of the outbound email DLP rule.
            order (int): The order of the outbound email DLP rule, defaults to adding the outbound email DLP rule to the bottom of the list.
            description (str): Additional information about the outbound email DLP rule.
            state (str): The outbound email DLP rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            action (str): The action taken when traffic matches the outbound email DLP rule criteria.
            min_size (int): The min size for this outbound email DLP rule.
            without_content_inspection (bool): A Boolean value indicating whether without content inspection applies to this outbound email DLP rule.
            external_auditor_email (str): The email address of an external auditor to whom DLP email notifications are sent.
            severity (str): The severity level assigned to the outbound email DLP rule.
            parent_rule (int): The parent rule for this outbound email DLP rule.
            custom_header (str): The custom header for this outbound email DLP rule.
            groups (list): The IDs for the groups that this outbound email DLP rule applies to.
            departments (list): The IDs for the departments that this outbound email DLP rule applies to.
            users (list): The IDs for the users that this outbound email DLP rule applies to.
            excluded_groups (list): The IDs for the excluded groups that this outbound email DLP rule applies to.
            excluded_departments (list): The IDs for the excluded departments that this outbound email DLP rule applies to.
            excluded_users (list): The IDs for the excluded users that this outbound email DLP rule applies to.
            time_windows (list): The IDs for the time windows that this outbound email DLP rule applies to.
            dlp_engines (list): The IDs for the dlp engines that this outbound email DLP rule applies to.
            file_types (list): The list of file types for this outbound email DLP rule.
            labels (list): The IDs for the labels that this outbound email DLP rule applies to.
            included_domain_profiles (list): The IDs for the included domain profiles that this outbound email DLP rule applies to.
            user_risk_score_levels (list): The list of user risk score levels for this outbound email DLP rule. Accepted values include e.g. ``LOW``.
            email_tenants (list): The IDs for the email tenants that this outbound email DLP rule applies to.
            content_locations (list): The list of content locations for this outbound email DLP rule. Accepted values include e.g. ``ANY``.
            sub_rules (list): The IDs for the sub rules that this outbound email DLP rule applies to.
            email_recipient_profiles (list): The IDs for the email recipient profiles that this outbound email DLP rule applies to.
            auditor (dict): The ID of the auditor for this outbound email DLP rule, e.g. ``{'id': 12345}``.
            notification_template (dict): The ID of the notification template for this outbound email DLP rule, e.g. ``{'id': 12345}``.
            receiver (dict): The ID of the receiver for this outbound email DLP rule, e.g. ``{'id': 12345}``.

        Returns:
            tuple: A tuple containing the updated OutboundEmailDlpRules instance, response, and error.

        Examples:
            Update an existing outbound email DLP rule:

            >>> updated_rule, _, error = client.zia.outbound_email_dlp_rules.update_rule(
            ...     rule_id=1013,
            ...     name=f"UpdatedRule_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedRule_{random.randint(1000, 10000)}",
            ...     state='ENABLED',
            ...     action='ALLOW',
            ... )
            >>> if error:
            ...     print(f"Error updating outbound email DLP rule: {error}")
            ...     return
            ... print(f"Outbound email dlp rule updated successfully: {updated_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailDlpRules/{rule_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, OutboundEmailDlpRules)
        if error:
            return (None, response, error)

        try:
            result = OutboundEmailDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> APIResult[None]:
        """
        Deletes the specified outbound email DLP rule.

        Args:
            rule_id (int): The unique identifier for the outbound email DLP rule.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a outbound email DLP rule:

            >>> _, _, error = client.zia.outbound_email_dlp_rules.delete_rule(1013)
            >>> if error:
            ...     print(f"Error deleting outbound email DLP rule: {error}")
            ...     return
            ... print(f"Outbound email dlp rule deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailDlpRules/{rule_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_actions(self, query_params: Optional[dict] = None, output_file: str = None) -> APIResult[bytes]:
        """
        Retrieves a mapping of supported outbound email DLP rule actions for the specified email tenant applications. The response body is a CSV file.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.tenantIds]`` {list}: One or more email tenant application IDs (required
            output_file (str): Optional path; when given, the downloaded bytes are written to this file.

        Returns:
            tuple: A 2-tuple of (the CSV mapping of supported outbound email DLP rule actions as bytes, error).

        Examples:
            >>> content, error = client.zia.outbound_email_dlp_rules.get_actions(output_file='get_actions.csv')
            >>> if error:
            ...     print(f"Error downloading outbound email DLP rule: {error}")
            ...     return
            ... print("Downloaded successfully.")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailDlpRules/actions
        """)

        query_params = query_params or {}

        headers = {
            "Accept": "application/octet-stream",
            "Content-Type": "application/json",
        }

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body={},
            headers=headers,
            params=query_params,
        )
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            return (None, f"Request failed: {error}")

        content = response.content

        if output_file:
            with open(output_file, "wb") as f:
                f.write(content)

        return (content, None)
