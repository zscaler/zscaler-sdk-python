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
from zscaler.zia.models.url_filtering_rules import URLFilteringRule
from zscaler.zia.models.url_filter_cloud_app_settings import AdvancedUrlFilterAndCloudAppSettings
from zscaler.utils import format_url, transform_common_id_fields, reformat_params


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
        >>> rules_list, _, error = client.zia.url_filtering.list_rules()
        >>> if error:
        ...     print(f"Error listing url filtering rules: {error}")
        ...     return
        ... print(f"Total rules found: {len(rules_list)}")
        ... for rule in rules_list:
        ...     print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlFilteringRules
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
                results.append(URLFilteringRule(self.form_response_body(item)))
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
        Returns information on the specified URL Filtering Policy rule.

        Args:
            rule_id (str): The unique ID for the URL Filtering Policy rule.

        Returns:
            :obj:`Tuple`: The URL Filtering Policy rule.

        Examples:
            >>> fetched_rule, _, error = client.zia.url_filtering.get_rule('2524554')
            >>> if error:
            ...     print(f"Error fetching rule by ID: {error}")
            ...     return
            ... print(f"Fetched rule by ID: {fetched_rule.as_dict()}")
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, URLFilteringRule)

        if error:
            return (None, response, error)

        try:
            result = URLFilteringRule(self.form_response_body(response.get_body()))
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
            Add a url filtering rule:

            >>> added_rule, _, error = client.zia.url_filtering.add_rule(
            ...     name=f"NewRule {random.randint(1000, 10000)}",
            ...     description=f"NewRule {random.randint(1000, 10000)}",
            ...     state="ENABLED",
            ...     order=1,
            ...     rank=7,
            ...     action='ALLOW',
            ...     url_categories = ["OTHER_ADULT_MATERIAL"],
            ...     protocols = ["ANY_RULE"],
            ...     device_trust_levels=["UNKNOWN_DEVICETRUSTLEVEL", "LOW_TRUST", "MEDIUM_TRUST", "HIGH_TRUST"],
            ...     user_agent_types = [	"OPERA", "FIREFOX", "MSIE", "MSEDGE", "CHROME", "SAFARI", "MSCHREDGE", "OTHER" ],
            ...     request_methods = [ "CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "OTHER", "POST", "PUT", "TRACE"],
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
            /urlFilteringRules
        """
        )

        body = kwargs

        # Convert 'enabled' to 'state' (ENABLED/DISABLED) if it's present in the payload
        if "enabled" in body:
            body["state"] = "ENABLED" if body.pop("enabled") else "DISABLED"

        # Filter out the url_categories mapping so it doesn't get processed
        local_reformat_params = [param for param in reformat_params if param[0] != "url_categories"]
        transform_common_id_fields(local_reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, URLFilteringRule)
        if error:
            return (None, response, error)

        try:
            result = URLFilteringRule(self.form_response_body(response.get_body()))
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
            Updating an exiisting url filtering rule:

            >>> updated_rule, _, error = client.zia.url_filtering.add_rule(
            ...     name=f"UpdateRule_{random.randint(1000, 10000)}",
            ...     description=f"UpdateRule_{random.randint(1000, 10000)}",
            ...     state="ENABLED",
            ...     order=1,
            ...     rank=7,
            ...     action='ALLOW',
            ...     url_categories = ["OTHER_ADULT_MATERIAL"],
            ...     protocols = ["ANY_RULE"],
            ...     device_trust_levels=["UNKNOWN_DEVICETRUSTLEVEL", "LOW_TRUST", "MEDIUM_TRUST", "HIGH_TRUST"],
            ...     user_agent_types = [	"OPERA", "FIREFOX", "MSIE", "MSEDGE", "CHROME", "SAFARI", "MSCHREDGE", "OTHER" ],
            ...     request_methods = [ "CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "OTHER", "POST", "PUT", "TRACE"],
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

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, URLFilteringRule)
        if error:
            return (None, response, error)

        try:
            result = URLFilteringRule(self.form_response_body(response.get_body()))
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
            >>> _, _, error = client.zia.url_filtering.delete_rule('524558')
            >>> if error:
            ...     print(f"Error deleting rule: {error}")
            ...     return
            ... print(f"Rule with ID {'524558'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlFilteringRules/{rule_id}
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

    def get_url_and_app_settings(self) -> tuple:
        """
        Retrieves information about URL and Cloud App Control advanced policy settings

        Returns:
            tuple: A tuple containing:
                - AdvancedUrlFilterAndCloudAppSettings: The current advanced settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current url and app settings:

            >>> settings, response, err = client.zia.url_filtering.get_update_url_and_app_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /advancedUrlFilterAndCloudAppSettings
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = AdvancedUrlFilterAndCloudAppSettings(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_url_and_app_settings(self, **kwargs) -> tuple:
        """
        Updates the URL and Cloud App Control advanced policy settings

        Args:
            settings (:obj:`AdvancedUrlFilterAndCloudAppSettings`):
                An instance of `AdvancedSettings` containing the updated configuration.

        Supported attributes:
            - enable_dynamic_content_cat (bool): Enables dynamic categorization of URLs using AI/ML analysis.
            - consider_embedded_sites (bool): Apply URL filtering to sites translated with translation services.
            - enforce_safe_search (bool): Only return safe web, image, and video content in search results.
            - enable_office365 (bool): Enables Microsoft Office 365 configuration in the policy.
            - enable_msft_o365 (bool): Enables Microsoft-recommended one-click Office 365 configuration.
            - enable_ucaas_zoom (bool): Automatically permit secure breakout for Zoom traffic.
            - enable_ucaas_log_me_in (bool): Automatically permit secure breakout for GoTo traffic.
            - enable_ucaas_ring_central (bool): Automatically permit secure breakout for RingCentral traffic.
            - enable_ucaas_webex (bool): Automatically permit secure breakout for Webex traffic.
            - enable_ucaas_talkdesk (bool): Automatically permit secure breakout for Talkdesk traffic.
            - enable_chat_gpt_prompt (bool): Categorize and log user prompts sent to ChatGPT.
            - enable_microsoft_copilot_prompt (bool): Categorize and log user prompts sent to Microsoft Copilot.
            - enable_gemini_prompt (bool): Categorize and log user prompts sent to Google Gemini.
            - enable_poe_prompt (bool): Categorize and log user prompts sent to Poe AI.
            - enable_meta_prompt (bool): Categorize and log user prompts sent to Meta AI.
            - enable_perplexity_prompt (bool): Categorize and log user prompts sent to Perplexity AI.
            - block_skype (bool): Specifies whether Skype access is blocked.
            - enable_newly_registered_domains (bool): Block or allow domains identified shortly after registration.
            - enable_block_override_for_non_auth_user (bool): Allow authenticated users to override website blocks.
            - enable_cipa_compliance (bool): Enables the predefined CIPA Compliance Rule.

        Returns:
            tuple:
                - **AdvancedUrlFilterAndCloudAppSettings**: The updated URL and Cloud App Control advanced object.
                - **Response**: The raw HTTP response returned by the API.
                - **error**: An error message if the update failed; otherwise, `None`.

        Examples:
            Update URL and Cloud App Control advanced by enabling Office365 and adjusting the session timeout:

            >>> settings, response, err = client.zia.url_filtering.get_advanced_settings()
            >>> if not err:
            ...     settings.enable_office365 = True
            ...     settings.ui_session_timeout = 7200
            ...     updated_settings, response, err = client.zia.url_filtering.update_url_and_app_settings(settings)
            ...     if not err:
            ...         print(f"Updated Enable Office365: {updated_settings.enable_office365}")
            ...     else:
            ...         print(f"Failed to update settings: {err}")
        """
        if kwargs.get("enable_cipa_compliance") is True:
            mutually_exclusive = [
                "enable_newly_registered_domains",
                "consider_embedded_sites",
                "enforce_safe_search",
                "enable_dynamic_content_cat",
            ]
            for key in mutually_exclusive:
                if kwargs.get(key) is True:
                    return (
                        None,
                        None,
                        ValueError(f"Invalid configuration: '{key}' cannot be True when 'enable_cipa_compliance' is True"),
                    )

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /advancedUrlFilterAndCloudAppSettings
            """
        )
        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdvancedUrlFilterAndCloudAppSettings)
        if error:
            return (None, response, error)

        try:
            result = AdvancedUrlFilterAndCloudAppSettings(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
