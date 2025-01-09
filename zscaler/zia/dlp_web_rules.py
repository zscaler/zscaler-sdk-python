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
from zscaler.zia.models.dlp_web_rules import DLPWebRules

from zscaler.utils import convert_keys, recursive_snake_to_camel, snake_to_camel, transform_common_id_fields, format_url


class DLPWebRuleAPI(APIClient):
    """
    A Client object for the DLP Web Rule resource.
    """

    reformat_params = [
        ("auditor", "auditor"),
        ("dlp_engines", "dlpEngines"),
        ("departments", "departments"),
        ("excluded_departments", "excludedDepartments"),
        ("excluded_groups", "excludedGroups"),
        ("excluded_users", "excludedUsers"),
        ("groups", "groups"),
        ("labels", "labels"),
        ("locations", "locations"),
        ("location_groups", "locationGroups"),
        ("notification_template", "notificationTemplate"),
        ("time_windows", "timeWindows"),
        ("users", "users"),
        ("url_categories", "urlCategories"),
    ]

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(self, query_params=None) -> tuple:
        """
        Enumerates dlp web rules in your organization with pagination.
        A subset of dlp web rules can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of DLP Web Rules instances, Response, error)


        Examples:
            Get a list of all Web DLP Items

            >>> results = zia.web_dlp.list_rules()
            ... for item in results:
            ...    print(item)

        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/webDlpRules")
        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, DLPWebRules)

        if error:
            return (None, response, error)

        # Parse the response into AppConnectorGroup instances
        try:
            result = []
            for item in response.get_results():
                result.append(DLPWebRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_rule(self, rule_id: str) -> tuple:
        """
        Returns a DLP policy rule, excluding SaaS Security API DLP policy rules.

        Args:
            rule_id (str): The unique id for the Web DLP rule.

        Returns:
            :obj:`Box`: The Web DLP Rule resource record.

        Examples:
            Get information on a Web DLP item by ID

            >>> results = zia.web_dlp.get_rule(rule_id='9999')
            ... print(results)

        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/webDlpRules/{rule_id}")

        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, DLPWebRules)

        if error:
            return (None, response, error)

        # Parse the response
        try:
            result = DLPWebRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_rules_lite(self, query_params: dict = None) -> tuple:
        """
        Returns the name and ID for all DLP policy rules, excluding SaaS Security API DLP policy rules.

        Returns:
            :obj:`BoxList`: List of Web DLP name/ids.

        Examples:
            Get Web DLP Lite results

            >>> results = zia.web_dlp.list_rules_lite()
            ... for item in results:
            ...    print(item)

        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/webDlpRules/lite")
        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, DLPWebRules)

        if error:
            return (None, response, error)

        # Parse the response into AdminUser instances
        try:
            result = []
            for item in response.get_results():
                result.append(DLPWebRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_rule(self, name: str, action: str, **kwargs) -> tuple:
        """
        Adds a new DLP policy rule.

        Args:
            name (str): The name of the filter rule. 31 char limit.
            action (str): The action for the filter rule.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            auditor (:obj:`list` of :obj:`int`): IDs for the auditors this rule applies to.
            cloud_applications (list): IDs for cloud applications this rule applies to.
            description (str): Additional information about the rule
            departments (:obj:`list` of :obj:`int`): IDs for departments this rule applies to.
            dlp_engines (:obj:`list` of :obj:`int`): IDs for DLP engines this rule applies to.
            excluded_groups (:obj:`list` of :obj:`int`): IDs for excluded groups.
            excluded_departments (:obj:`list` of :obj:`int`): IDs for excluded departments.
            excluded_users (:obj:`list` of :obj:`int`): IDs for excluded users.
            file_types (list): List of file types the DLP policy rule applies to.
            groups (:obj:`list` of :obj:`int`): IDs for groups this rule applies to.
            icap_server (:obj:`list` of :obj:`int`): IDs for the icap server this rule applies to.
            labels (:obj:`list` of :obj:`int`): IDs for labels this rule applies to.
            locations (:obj:`list` of :obj:`int`): IDs for locations this rule applies to.
            location_groups (:obj:`list` of :obj:`int`): IDs for location groups this rule applies to.
            notification_template (:obj:`list` of :obj:`int`): IDs for the notification template.
            time_windows (:obj:`list` of :obj:`int`): IDs for time windows this rule applies to.
            users (:obj:`list` of :obj:`int`): IDs for users this rule applies to.
            url_categories (list): IDs for URL categories the rule applies to.
            external_auditor_email (str): Email of an external auditor for DLP notifications.
            dlp_download_scan_enabled (bool): True enables DLP scan for file downloads.
            min_size (str): Minimum file size (in KB) for DLP policy rule evaluation.
            match_only (bool): If true, matches file size for DLP policy rule evaluation.
            ocr_enabled (bool): True allows OCR scanning of image files.
            without_content_inspection (bool): True indicates a DLP rule without content inspection.
            zcc_notifications_enabled (bool): True enables Zscaler Client Connector notification.

        Returns:
            :obj:`Box`: The new dlp web rule resource record.

        Examples:
            Add a rule to allow all traffic to Google DNS (admin ranking is enabled):

            >>> zia.web_dlp.add_rule(rank='7',
            ...    file_types=['BITMAP', 'JPEG', 'PNG'],
            ...    name='ALLOW_ANY_TO_GOOG-DNS',
            ...    action='ALLOW',
            ...    description='TT#1965432122')

            Add a rule to block all traffic to Quad9 DNS for Finance Group:

            >>> zia.web_dlp.add_rule(rank='7',
            ...    file_types=['BITMAP', 'JPEG', 'PNG'],
            ...    name='BLOCK_GROUP-FIN_TO_Q9-DNS',
            ...    action='BLOCK_ICMP',
            ...    groups=['95016183'],
            ...    description='TT#1965432122')
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/webDlpRules")

        # Convert enabled to API format if present
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        payload = {
            "name": name,
            "action": action,
            "order": kwargs.pop("order", len(self.list_rules())),
        }

        # Transform ID fields in kwargs
        transform_common_id_fields(self.reformat_params, kwargs, payload)
        for key, value in kwargs.items():
            if value is not None:
                payload[snake_to_camel(key)] = value

        # Convert the entire payload's keys to camelCase before sending
        camel_payload = recursive_snake_to_camel(payload)
        for key, value in kwargs.items():
            if value is not None:
                camel_payload[snake_to_camel(key)] = value

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPWebRules)

        if error:
            return (None, response, error)

        try:
            result = DLPWebRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_rule(self, rule_id: str, **kwargs) -> tuple:
        """
        Updates an existing DLP policy rule. Not applicable to SaaS Security API DLP policy rules.

        Args:
            rule_id (str): ID of the rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            order (str): Rule order, defaults to bottom of list.
            rank (str): Admin rank of the rule.
            state (str): Rule state ('ENABLED' or 'DISABLED').
            auditor (list): IDs for auditors this rule applies to.
            cloud_applications (list): IDs for cloud applications rule applies to.
            description (str): Additional information about the rule.
            departments (list): IDs for departments rule applies to.
            dlp_engines (list): IDs for DLP engines rule applies to.
            excluded_groups (list): IDs for excluded groups.
            excluded_departments (list): IDs for excluded departments.
            excluded_users (list): IDs for excluded users.
            file_types (list): List of file types the rule applies to.
            groups (list): IDs for groups rule applies to.
            icap_server (list): IDs for the ICAP server rule applies to.
            labels (list): IDs for labels rule applies to.
            locations (list): IDs for locations rule applies to.
            location_groups (list): IDs for location groups rule applies to.
            notification_template (list): IDs for the notification template.
            time_windows (list): IDs for time windows rule applies to.
            users (list): IDs for users rule applies to.
            url_categories (list): IDs for URL categories rule applies to.
            external_auditor_email (str): Email of external auditor for DLP notifications.
            dlp_download_scan_enabled (bool): True enables DLP scan for file downloads.
            min_size (str): Minimum file size (in KB) for rule evaluation.
            match_only (bool): If true, uses min_size for rule evaluation.
            ocr_enabled (bool): True allows OCR scanning of image files.
            without_content_inspection (bool): True for DLP rule without content inspection.
            zcc_notifications_enabled (bool): True enables ZCC notification for block action.

        Returns:
            :obj:`Box`: The updated web dlp rule resource record.

        Examples:
            Update a Web DLP Policy Rule:

                >>> zia.web_dlp.get_rule('9999')
                ... name="updated name."
                ... description="updated name."

            Update a web dlp policy rule to update description:

                >>> zia.web_dlp.update_rule('976597', description="TT#1965232866")
        """
        http_method = "put".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/webDlpRules/{rule_id}")

        # Set payload to value of existing record and convert nested dict keys.
        payload = convert_keys(self.get_rule(rule_id))

        # Convert enabled to API format if present in kwargs
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        # Transform ID fields in kwargs
        transform_common_id_fields(self.reformat_params, kwargs, payload)

        # Add remaining optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPWebRules)

        if error:
            return (None, response, error)

        try:
            result = DLPWebRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: int) -> tuple:
        """
        Deletes a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            rule_id (str): Unique id of the Web DLP Policy Rule that will be deleted.

        Returns:
            :obj:`Box`: Response message from the ZIA API endpoint.

        Examples:
            Delete a rule with an id of 9999.

            >>> results = zia.web_dlp.delete_rule(rule_id=9999)
            ... print(results)


        """
        http_method = "delete".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/webDlpRules/{rule_id}")

        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, {})
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, error)

        return (response, None)
