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

from zscaler.zia.models.url_filtering_rules import URLFilteringRule
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url, transform_common_id_fields, reformat_params
from zscaler.api_client import APIClient


class URLFilteringAPI(APIClient):
    """
    A Client object for the URL Filtering Rule resources.
    """

    reformat_params = [
        ("cbi_profile", "cbiProfile"),
        ("departments", "departments"),
        ("devices", "devices"),
        ("device_groups", "deviceGroups"),
        ("groups", "groups"),
        ("labels", "labels"),
        ("locations", "locations"),
        ("location_groups", "locationGroups"),
        ("override_users", "overrideUsers"),
        ("override_groups", "overrideGroups"),
        ("time_windows", "timeWindows"),
        ("workload_groups", "workloadGroups"),
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
        Lists url filtering rules in your organization.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:
            tuple: A tuple containing (list of url filtering rules instances, Response, error)

        Examples:
        >>> rules, response, error = zia.url_filtering.list_rules()
        ...    pprint(rule)

        >>> rules, response, error = zia.url_filtering.list_rules(
            query_params={"search": "Block malicious IPs and domains"})
        ...    pprint(rule)
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /urlFilteringRules
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

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(URLFilteringRule(
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
        Returns information on the specified URL Filtering Policy rule.

        Args:
            rule_id (str): The unique ID for the URL Filtering Policy rule.

        Returns:
            :obj:`Tuple`: The URL Filtering Policy rule.

        Examples:
            >>> pprint(zia.url_filtering.get_rule('977469'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlFilteringRules/{rule_id}
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
            execute(request, URLFilteringRule)

        if error:
            return (None, response, error)

        try:
            result = URLFilteringRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_rule(self, **kwargs) -> tuple:
        """
        Adds a new URL Filtering Policy rule.

        Args:
            rank (str): The admin rank of the user who creates the rule.
            name (str): The name of the rule.
            action (str): Action taken when traffic matches rule criteria. Accepted values are:
                `ANY`, `NONE`, `BLOCK`, `CAUTION`, `ALLOW` and `ICAP_RESPONSE`

            device_trust_levels (list): List of device trust levels for which the rule must be applied. Accepted values are:
                `ANY`, `UNKNOWN_DEVICETRUSTLEVEL`, `LOW_TRUST`, `MEDIUM_TRUST`, and `HIGH_TRUST`

            protocols (list): The protocol criteria for the rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            block_override (bool): When set to true, a 'BLOCK' action triggered by the rule could be overridden.
                Defaults to `False`.
            ciparule (bool): The CIPA compliance rule is enabled if this is set to `True`. Defaults to `False`.
            departments (list): The IDs for the departments that this rule applies to.
            devices (list): The IDs for the devices that this rule applies to.
            device_groups (list): The IDs for the device groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            description (str): Additional information about the URL Filtering rule.
            end_user_notification_url (str): URL of end user notification page to be displayed when the rule is matched.
                Not applicable if either ``override_users`` or ``override_groups`` is specified.
            enforce_time_validity (bool): Enforce a set validity time period for the URL Filtering rule.
            groups (list): The IDs for the groups that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            order (str): Order of execution of rule with respect to other URL Filtering rules. Defaults to placing rule
                at the bottom of the list.
            override_users (:obj:`list` of :obj:`int`): The IDs of users that this rule can be overridden for.
                Only applies if ``block_override`` is True, ``action`` is `BLOCK` and ``override_groups`` is not set.
            override_groups (:obj:`list` of :obj:`int`): The IDs of groups that this rule can be overridden for.
                Only applies if ``block_override`` is True and ``action`` is `BLOCK`.
            request_methods (list): The request methods that this rule will apply to. If not specified, the rule will
                apply to all methods. Accepted values are:
                `CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `OTHER`, `POST`, `PUT`, `TRACE`
            user_agent_types (list): User Agent types on which this rule will be applied. Accepted values are:
                `OPERA`, `FIREFOX`, `MSIE`, `MSEDGE`, `CHROME`, `SAFARI`, `OTHER`, `MSCHREDGE`
            size_quota (str): Size quota in KB for applying the URL Filtering rule.
            time_quota (str): Time quota in minutes elapsed after the URL Filtering rule is applied.
            time_windows (list): The IDs for the time windows that this rule applies to.
            url_categories (list): The names of URL categories that this rule applies to.
            url_categories2 (list): The names of URL categories that this rule applies to.
                Note: The urlCategories and urlCategories2 parameters are connected with a logical AND operator
            users (list): The IDs for the users that this rule applies to.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The URL Filter rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`Tuple`: The newly created URL Filtering Policy rule.

        Examples:
            Add a rule with the minimum required parameters:

            >>> zia.url_filtering.add_rule(rank='7',
            ...    name="Empty URL Filter",
            ...    action="ALLOW",
            ...    protocols=['ANY_RULE']

            Add a rule to block HTTP POST to Social Media sites for the Finance department.

            >>> zia.url_filtering.add_rule(rank='7',
            ...    name="Block POST to Social Media",
            ...    action="BLOCK",
            ...    protocols=["HTTP_PROXY", "HTTP_RULE", "HTTPS_RULE"],
            ...    request_methods=['POST'],
            ...    departments=["95022175"],
            ...    url_categories=["SOCIAL_NETWORKING"])

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlFilteringRules
        """
        )

        body = kwargs
        
        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in kwargs:
            kwargs["state"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"
            
        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)
        
        request, error = self._request_executor\
            .create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, URLFilteringRule)
        if error:
            return (None, response, error)

        try:
            result = URLFilteringRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_rule(self, rule_id: str, **kwargs) -> tuple:
        """
        Updates the specified URL Filtering Policy rule.

        Args:
            rule_id: The unique ID of the URL Filtering Policy rule to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the rule.
            action (str): Action taken when traffic matches rule criteria. Accepted values are:
                `ANY`, `NONE`, `BLOCK`, `CAUTION`, `ALLOW` and `ICAP_RESPONSE`

            device_trust_levels (list): List of device trust levels for which the rule must be applied. Accepted values are:
                `ANY`, `UNKNOWN_DEVICETRUSTLEVEL`, `LOW_TRUST`, `MEDIUM_TRUST`, and `HIGH_TRUST`

            protocols (list): The protocol criteria for the rule.
            request_methods (list): The request methods that this rule will apply to. If not specified, the rule will
                apply to all methods. Accepted values are:
                `CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `OTHER`, `POST`, `PUT`, `TRACE`
            user_agent_types (list): User Agent types on which this rule will be applied. Accepted values are:
                `OPERA`, `FIREFOX`, `MSIE`, `MSEDGE`, `CHROME`, `SAFARI`, `OTHER`, `MSCHREDGE`
            block_override (bool): When set to true, a 'BLOCK' action triggered by the rule could be overridden.
                Defaults to `False`.
            ciparule (bool): The CIPA compliance rule is enabled if this is set to `True`. Defaults to `False`.
            departments (list): The IDs for the departments that this rule applies to.
            devices (list): The IDs for the devices that this rule applies to.
            device_groups (list): The IDs for the device groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            description (str): Additional information about the URL Filtering rule.
            end_user_notification_url (str): URL of end user notification page to be displayed when the rule is matched.
                Not applicable if either ``override_users`` or ``override_groups`` is specified.
            enforce_time_validity (bool): Enforce a set validity time period for the URL Filtering rule.
            groups (list): The IDs for the groups that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            order (str): Order of execution of rule with respect to other URL Filtering rules. Defaults to placing rule
                at the bottom of the list.
            override_users (:obj:`list` of :obj:`int`):
                The IDs of users that this rule can be overridden for.
                Only applies if ``block_override`` is True, ``action`` is `BLOCK` and ``override_groups`` is not set.
            override_groups (:obj:`list` of :obj:`int`):
                The IDs of groups that this rule can be overridden for.
                Only applies if ``block_override`` is True and ``action`` is `BLOCK`.
            size_quota (str): Size quota in KB for applying the URL Filtering rule.
            time_quota (str): Time quota in minutes elapsed after the URL Filtering rule is applied.
            time_windows (list): The IDs for the time windows that this rule applies to.
            url_categories (list): The names of URL categories that this rule applies to.
            url_categories2 (list): The names of URL categories that this rule applies to.
                Note: The urlCategories and urlCategories2 parameters are connected with a logical AND operator
            users (list): The IDs for the users that this rule applies to.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The URL Filter rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`Tuple`: The updated URL Filtering Policy rule.

        Examples:
            Update the name of a URL Filtering Policy rule:

            >>> zia.url_filtering.update_rule('977467',
            ...    name="Updated Name")

            Add GET to request methods and change action to ALLOW:

            >>> zia.url_filtering.update_rule('977468',
            ...    request_methods=['POST', 'GET'],
            ...    action="ALLOW")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlFilteringRules/{rule_id}
        """
        )
        
        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)
        
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
        response, error = self._request_executor.\
            execute(request, URLFilteringRule)
        if error:
            return (None, response, error)

        try:
            result = URLFilteringRule(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_id: str) -> tuple:
        """
        Deletes the specified url filtering filter rule.

        Args:
            rule_id (str): The unique identifier for the url filtering rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.url_filtering.delete_rule('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlFilteringRules/{rule_id}
        """
        )

        params = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
