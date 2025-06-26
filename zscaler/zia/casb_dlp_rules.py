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
from zscaler.utils import format_url, transform_common_id_fields, reformat_params
from zscaler.api_client import APIClient
from zscaler.zia.models.casb_dlp_rules import CasbdDlpRules


class CasbdDlpRulesAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_rules(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns a list of all Casb DLP Rules for the specified rule type.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

                ``[query_params.rule_type]`` {str}: The type of rules to retrieve (e.g., "OFLCASB_DLP_ITSM").

                    Supported Values: `ANY`, `NONE`, `OFLCASB_DLP_FILE`, `OFLCASB_DLP_EMAIL`, `OFLCASB_DLP_CRM`,
                        `OFLCASB_DLP_ITSM`, `OFLCASB_DLP_COLLAB`, `OFLCASB_DLP_REPO`, `OFLCASB_DLP_STORAGE`,
                        `OFLCASB_DLP_GENAI`

        Returns:
            tuple: The list of Casb DLP Rules.

        Examples:
            List all rules for a specific type::

                >>> rules_list, _, error = client.zia.casb_dlp_rules.list_rules(
                ...     query_params={'rule_type': 'OFLCASB_DLP_ITSM'})
                >>> if error:
                ...     print(f"Error listing casb dlp rules rules: {error}")
                ...     return
                ... print(f"Total rules found: {len(rules_list)}")
                ... for rule in rules_list:
                ...     print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /casbDlpRules
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
                result.append(CasbdDlpRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_rule(
        self,
        rule_id: int,
        rule_type: str,
    ) -> tuple:
        """
        Returns information for the specified Casb DLP Rule under the specified rule type.

        Args:
            rule_id (int): The unique identifier for the Casb DLP Rule.

            rule_type (str): The type of the rule (e.g., "OFLCASB_DLP_ITSM").

                Supported Values: `ANY`, `NONE`, `OFLCASB_DLP_FILE`, `OFLCASB_DLP_EMAIL`, `OFLCASB_DLP_CRM`,
                    `OFLCASB_DLP_ITSM`, `OFLCASB_DLP_COLLAB`, `OFLCASB_DLP_REPO`, `OFLCASB_DLP_STORAGE`,
                    `OFLCASB_DLP_GENAI`

        Returns:
            :obj:`Tuple`: The resource record for the Casb DLP Rule.

        Examples:
            Get a specific rule by ID and type::

                >>> fetched_rule, _, error = client.zia.casb_dlp_rules.get_rule(
                ...     rule_type='OFLCASB_DLP_ITSM',
                ...     rule_id='1070199'
                ... )
                >>> if error:
                ...     print(f"Error fetching rule by ID: {error}")
                ...     return
                ... print(f"Fetched rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /casbDlpRules/{rule_id}
        """
        )

        params = {"ruleType": rule_type}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CasbdDlpRules)

        if error:
            return (None, response, error)

        try:
            result = CasbdDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_all_rules(
        self,
    ) -> tuple:
        """
        Returns a list of all Casb DLP Rules.

        Args:
            N/A

        Returns:
            tuple: The list of all Casb DLP Rules.

        Examples:
            List all rules for a specific type::

                >>> rules_list, _, error = client.zia.casb_dlp_rules.list_all_rules(
                >>> if error:
                ...     print(f"Error listing all casb dlp rules rules: {error}")
                ...     return
                ... print(f"Total rules found: {len(rules_list)}")
                ... for rule in rules_list:
                ...     print(rule.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /casbDlpRules/all
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
            result = []
            for item in response.get_results():
                result.append(CasbdDlpRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_rule(self, **kwargs) -> tuple:
        """
        Adds a new cloud app control rule.

        Args:
            name (str): Name of the rule.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list
            rank (str): The admin rank of the rule
            enabled (bool): The rule state
            description (str): Additional information about the rule
            bucket_owner (str): A user who inspect their buckets for sensitive data.
            external_auditor_email (str): Email address of the external auditor to whom the DLP email alerts are sent
            quarantine_location (str): Location where all the quarantined files are moved and necessary actions are taken
            include_entity_groups (bool): entity_groups included as part of the criteria, else are excluded from the criteria
            without_content_inspection (bool): If true, Content Matching is set to None
            include_criteria_domain_profile (bool): If true, criteria_domain_profiles is included as part of the criteria.
            watermark_delete_old_version (bool): Specifies whether to delete an old version of the watermarked file

            type (str): The type of the rule (e.g., "OFLCASB_DLP_ITSM").

                Supported Values: `ANY`, `NONE`, `OFLCASB_DLP_FILE`, `OFLCASB_DLP_EMAIL`,
                `OFLCASB_DLP_CRM`, `OFLCASB_DLP_ITSM`, `OFLCASB_DLP_COLLAB`, `OFLCASB_DLP_REPO`,
                `OFLCASB_DLP_STORAGE`, `OFLCASB_DLP_GENAI`

            recipient (str): Specifies if the email recipient is internal or external

                Supported Values:
                    - `EMAIL_RECIPIENT_INTERNAL`,
                    - `EMAIL_RECIPIENT_EXTERNAL`

            number_of_internal_collaborators (str): Selects the number of internal collaborators for
                files that are shared with specific collaborators or are discoverable within an organization

                Supported Values:
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_1_TO_10`,
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_11_TO_100`
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_101_TO_1000`
                    - `CASB_FILE_TYPE_COLLAB_RANGE_1001_PLUS`

            number_of_external_collaborators (str): Selects the number of external collaborators for
                files that are shared with specific collaborators or are discoverable within an organization

                Supported Values:
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_1_TO_10`,
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_11_TO_100`
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_101_TO_1000`
                    - `CASB_FILE_TYPE_COLLAB_RANGE_1001_PLUS`

            content_location (str): Location for the content that the Zscaler service inspects for sensitive data

                Supported Values:
                    - `ANY`,
                    - `CONTENT_LOCATION_PRIVATE_CHANNEL`
                    - `CONTENT_LOCATION_PUBLIC_CHANNEL`
                    - `CONTENT_LOCATION_SHARED_CHANNEL`
                    - `CONTENT_LOCATION_DIRECT_MESSAGE`
                    - `CONTENT_LOCATION_MULTI_PERSON_DIRECT_MESSAGE`

            cloud_app_tenant_ids (list): The IDs of cloud application tenants for which the rule is applied
            included_domain_profile_ids (list): The IDs of domain profiles included in the criteria for the rule
            excluded_domain_profile_ids (list): The IDs of domain profiles excluded in the criteria for the rule
            criteria_domain_profile_ids (list): The IDs of domain profiles that are mandatory in the criteria for the rule
            email_recipient_profile_ids (list): The IDs of recipient profiles for which the rule is applied
            buckets (list): The IDs buckets for the Zscaler service to inspect for sensitive data
            dlp_engines (list): The IDs of DLP engines to which the DLP policy rule must be applied
            object_type_ids (list): The IDs of object types for which the rule is applied.
            entity_group_ids (list): The IDs of entity groups that are part of the rule criteria.
            labels (list): The IDs for the labels that this rule applies to
            entity_groups (list): The IDs for entity groups that are part of the rule criteria
            departments (list): The IDs for the departments that this rule applies to
            groups (list): The IDs for the groups that this rule applies to
            users (list): The IDs for the users that this rule applies to

            auditor (dict): Selects an auditor for the rule.
            redaction_profile (dict): Name-ID of the redaction profile in the criteria
            casb_email_label (dict): Name-ID of the email label associated with the rule
            casb_tombstone_template (dict): Name-ID of the quarantine tombstone template associated with the rule
            zscaler_incident_receiver (dict): The Zscaler Incident Receiver details
            tag (dict): Tag applied to the rule
            watermark_profile (dict): Watermark profile applied to the rule

            domains (list[str]): The domain for the external organization sharing the channel.
                This field is applicable only when you select `CONTENT_LOCATION_SHARED_CHANNEL`
                in the 'content_location' field

            file_types (list[str]): List of file types to which the rule must be applied.
                See the `Casb DLP Rule API reference:
                <https://https://help.zscaler.com/zia/saas-security-api#/casbDlpRules-post>`_
                for the supported values.

            collaboration_scope (list[str]): List of file types to which the rule must be applied.

                Supported Values:
                    - `ANY`,
                    - `COLLABORATION_SCOPE_EXTERNAL_COLLAB_VIEW`
                    - `COLLABORATION_SCOPE_EXTERNAL_COLLAB_EDIT`
                    - `COLLABORATION_SCOPE_EXTERNAL_LINK_VIEW`
                    - `COLLABORATION_SCOPE_EXTERNAL_LINK_EDIT`
                    - `COLLABORATION_SCOPE_INTERNAL_COLLAB_VIEW`
                    - `COLLABORATION_SCOPE_INTERNAL_COLLAB_EDIT`
                    - `COLLABORATION_SCOPE_INTERNAL_LINK_VIEW`
                    - `COLLABORATION_SCOPE_INTERNAL_LINK_EDIT`
                    - `COLLABORATION_SCOPE_PRIVATE_EDIT`
                    - `COLLABORATION_SCOPE_PRIVATE`
                    - `COLLABORATION_SCOPE_PUBLIC`

            components (list[str]): List of components for which the rule is applied.
                Zscaler service inspects these components for sensitive data

                Supported Values:
                    - `ANY`,
                    - `COMPONENT_EMAIL_BODY`
                    - `COMPONENT_EMAIL_ATTACHMENT`
                    - `COMPONENT_EMAIL_SUBJECT`
                    - `COMPONENT_ITSM_OBJECTS`
                    - `COMPONENT_ITSM_ATTACHMENTS`
                    - `COMPONENT_CRM_CHATTER_MESSAGES`
                    - `COMPONENT_CRM_ATTACHMENTS_IN_OBJECTS`
                    - `COMPONENT_COLLAB_MESSAGES`
                    - `COMPONENT_COLLAB_ATTACHMENTS`
                    - `COMPONENT_CRM_CASES`
                    - `COMPONENT_GENAI_MESSAGES`
                    - `COMPONENT_GENAI_ATTACHMENTS`
                    - `COMPONENT_FILE_ATTACHMENTS`

        Returns:
            :obj:`Tuple`: New casb dlp rule resource.

        Examples:
            CASB DLP Rule for ITSM Access::

                >>> added_rule, _, error = client.zia.casb_dlp_rules.add_rule(
                ...     name=f"NewRule_{random.randint(1000, 10000)}",
                ...     description=f"NewRule_{random.randint(1000, 10000)}",
                ...     type = "OFLCASB_DLP_ITSM",
                ...     enabled=True,
                ...     order=1,
                ...     rank=7,
                ...     action = "OFLCASB_DLP_REPORT_INCIDENT",
                ...     severity = "RULE_SEVERITY_HIGH",
                ...     without_content_inspection = False,
                ...     external_auditor_email = "jdoe@acme.com",
                ...     file_types = ["FTCATEGORY_APPX","FTCATEGORY_SQL"],
                ...     collaboration_scope = ["ANY"],
                ...     components = ["COMPONENT_ITSM_OBJECTS", "COMPONENT_ITSM_ATTACHMENTS"],
                ...     cloud_app_tenant_ids = [15881081],
                ...     dlp_engines = [62, 63],
                ...     object_type_ids = [32, 33, 34],
                ...     labels = [1441065],
                ...     users = [1441095],
                ...     groups = [1441085],
                ...     departments = [1441075],
                ...     zscaler_incident_receiver = {
                ...         "id": 2020
                ...     },
                ...     auditor_notification = {
                ...         "id": 64282
                ...     },
                ... )
                >>> if error:
                ...     print(f"Error adding rule: {error}")
                ...     return
                ... print(f"Rule added successfully: {added_rule.as_dict()}")
                ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /casbDlpRules
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

        response, error = self._request_executor.execute(request, CasbdDlpRules)
        if error:
            return (None, response, error)

        try:
            result = CasbdDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_rule(self, rule_id: str, **kwargs) -> tuple:
        """
        Updates an existing casb dlp rule.

        Args:
            name (str): Name of the rule.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list
            rank (str): The admin rank of the rule
            enabled (bool): The rule state
            description (str): Additional information about the rule
            bucket_owner (str): A user who inspect their buckets for sensitive data.
            external_auditor_email (str): Email address of the external auditor to whom the DLP email alerts are sent
            quarantine_location (str): Location where all the quarantined files are moved and necessary actions are taken.
            include_entity_groups (bool): entity_groups included as part of the criteria, else are excluded from the criteria.
            without_content_inspection (bool): If true, Content Matching is set to None
            include_criteria_domain_profile (bool): If true, criteria_domain_profiles is included as part of the criteria.
            watermark_delete_old_version (bool): Specifies whether to delete an old version of the watermarked file

            type (str): The type of the rule (e.g., "OFLCASB_DLP_ITSM").

                Supported Values: `ANY`, `NONE`, `OFLCASB_DLP_FILE`, `OFLCASB_DLP_EMAIL`,
                `OFLCASB_DLP_CRM`, `OFLCASB_DLP_ITSM`, `OFLCASB_DLP_COLLAB`, `OFLCASB_DLP_REPO`,
                `OFLCASB_DLP_STORAGE`, `OFLCASB_DLP_GENAI`

            recipient (str): Specifies if the email recipient is internal or external

                Supported Values:
                    - `EMAIL_RECIPIENT_INTERNAL`,
                    - `EMAIL_RECIPIENT_EXTERNAL`

            number_of_internal_collaborators (str): Selects the number of internal collaborators for
                files that are shared with specific collaborators or are discoverable within an organization

                Supported Values:
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_1_TO_10`,
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_11_TO_100`
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_101_TO_1000`
                    - `CASB_FILE_TYPE_COLLAB_RANGE_1001_PLUS`

            number_of_external_collaborators (str): Selects the number of external collaborators for
                files that are shared with specific collaborators or are discoverable within an organization

                Supported Values:
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_1_TO_10`,
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_11_TO_100`
                    - `CASB_FILE_TYPE_COLLAB_COUNT_RANGE_101_TO_1000`
                    - `CASB_FILE_TYPE_COLLAB_RANGE_1001_PLUS`

            content_location (str): Location for the content that the Zscaler service inspects for sensitive data

                Supported Values:
                    - `ANY`,
                    - `CONTENT_LOCATION_PRIVATE_CHANNEL`
                    - `CONTENT_LOCATION_PUBLIC_CHANNEL`
                    - `CONTENT_LOCATION_SHARED_CHANNEL`
                    - `CONTENT_LOCATION_DIRECT_MESSAGE`
                    - `CONTENT_LOCATION_MULTI_PERSON_DIRECT_MESSAGE`

            cloud_app_tenant_ids (list): The IDs of cloud application tenants for which the rule is applied
            included_domain_profile_ids (list): The IDs of domain profiles included in the criteria for the rule
            excluded_domain_profile_ids (list): The IDs of domain profiles excluded in the criteria for the rule
            criteria_domain_profile_ids (list): The IDs of domain profiles that are mandatory in the criteria for the rule
            email_recipient_profile_ids (list): The IDs of recipient profiles for which the rule is applied
            buckets (list): The IDs buckets for the Zscaler service to inspect for sensitive data
            dlp_engines (list): The IDs of DLP engines to which the DLP policy rule must be applied
            object_type_ids (list): The IDs of object types for which the rule is applied.
            entity_group_ids (list): The IDs of entity groups that are part of the rule criteria.
            labels (list): The IDs for the labels that this rule applies to
            entity_groups (list): The IDs for entity groups that are part of the rule criteria
            departments (list): The IDs for the departments that this rule applies to
            groups (list): The IDs for the groups that this rule applies to
            users (list): The IDs for the users that this rule applies to

            auditor (dict): Selects an auditor for the rule.
            redaction_profile (dict): Name-ID of the redaction profile in the criteria
            casb_email_label (dict): Name-ID of the email label associated with the rule
            casb_tombstone_template (dict): Name-ID of the quarantine tombstone template associated with the rule
            zscaler_incident_receiver (dict): The Zscaler Incident Receiver details
            tag (dict): Tag applied to the rule
            watermark_profile (dict): Watermark profile applied to the rule

            domains (list[str]): The domain for the external organization sharing the channel.
                This field is applicable only when you select `CONTENT_LOCATION_SHARED_CHANNEL`
                in the 'content_location' field

            file_types (list[str]): List of file types to which the rule must be applied.
                See the `Casb DLP Rule API reference:
                <https://https://help.zscaler.com/zia/saas-security-api#/casbDlpRules-post>`_
                for the supported values.

            collaboration_scope (list[str]): List of file types to which the rule must be applied.

                Supported Values:
                    - `ANY`,
                    - `COLLABORATION_SCOPE_EXTERNAL_COLLAB_VIEW`
                    - `COLLABORATION_SCOPE_EXTERNAL_COLLAB_EDIT`
                    - `COLLABORATION_SCOPE_EXTERNAL_LINK_VIEW`
                    - `COLLABORATION_SCOPE_EXTERNAL_LINK_EDIT`
                    - `COLLABORATION_SCOPE_INTERNAL_COLLAB_VIEW`
                    - `COLLABORATION_SCOPE_INTERNAL_COLLAB_EDIT`
                    - `COLLABORATION_SCOPE_INTERNAL_LINK_VIEW`
                    - `COLLABORATION_SCOPE_INTERNAL_LINK_EDIT`
                    - `COLLABORATION_SCOPE_PRIVATE_EDIT`
                    - `COLLABORATION_SCOPE_PRIVATE`
                    - `COLLABORATION_SCOPE_PUBLIC`

            components (list[str]): List of components for which the rule is applied.
                Zscaler service inspects these components for sensitive data

                Supported Values:
                    - `ANY`,
                    - `COMPONENT_EMAIL_BODY`
                    - `COMPONENT_EMAIL_ATTACHMENT`
                    - `COMPONENT_EMAIL_SUBJECT`
                    - `COMPONENT_ITSM_OBJECTS`
                    - `COMPONENT_ITSM_ATTACHMENTS`
                    - `COMPONENT_CRM_CHATTER_MESSAGES`
                    - `COMPONENT_CRM_ATTACHMENTS_IN_OBJECTS`
                    - `COMPONENT_COLLAB_MESSAGES`
                    - `COMPONENT_COLLAB_ATTACHMENTS`
                    - `COMPONENT_CRM_CASES`
                    - `COMPONENT_GENAI_MESSAGES`
                    - `COMPONENT_GENAI_ATTACHMENTS`
                    - `COMPONENT_FILE_ATTACHMENTS`

        Returns:
            :obj:`Tuple`: New casb dlp rules resource.

        Examples:
            Update an existing CASB DLP Rule for ITSM Access::

                >>> updated_rule, _, error = client.zia.casb_dlp_rules.update_rule(
                ...     rule_id='1072324',
                ...     name=f"UpdateRule_{random.randint(1000, 10000)}",
                ...     description=f"UpdateRule_{random.randint(1000, 10000)}",
                ...     type = "OFLCASB_DLP_ITSM",
                ...     enabled=True,
                ...     order=1,
                ...     rank=7,
                ...     action = "OFLCASB_DLP_REPORT_INCIDENT",
                ...     severity = "RULE_SEVERITY_HIGH",
                ...     without_content_inspection = False,
                ...     external_auditor_email = "jdoe@acme.com",
                ...     file_types = ["FTCATEGORY_APPX","FTCATEGORY_SQL"],
                ...     collaboration_scope = ["ANY"],
                ...     components = ["COMPONENT_ITSM_OBJECTS", "COMPONENT_ITSM_ATTACHMENTS"],
                ...     cloud_app_tenant_ids = [15881081],
                ...     dlp_engines = [62, 63],
                ...     object_type_ids = [32, 33, 34],
                ...     labels = [1441065],
                ...     users = [1441095],
                ...     groups = [1441085],
                ...     departments = [1441075],
                ...     zscaler_incident_receiver = {
                ...         "id": 2020
                ...     },
                ...     auditor_notification = {
                ...         "id": 64282
                ...     },
                ... )
                >>> if error:
                ...     print(f"Error adding rule: {error}")
                ...     return
                ... print(f"Rule added successfully: {added_rule.as_dict()}")
                ... )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /casbDlpRules/{rule_id}
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

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = CasbdDlpRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_rule(self, rule_type: str, rule_id: int) -> tuple:
        """
        Deletes the specified casb dlp rules.

        Args:
            rule_id (int): The unique identifier for the casb dlp rules.

            rule_type (str): The type of the rule (e.g., "OFLCASB_DLP_ITSM").

                Supported Values: `ANY`, `NONE`, `OFLCASB_DLP_FILE`, `OFLCASB_DLP_EMAIL`, `OFLCASB_DLP_CRM`,
                    `OFLCASB_DLP_ITSM`, `OFLCASB_DLP_COLLAB`, `OFLCASB_DLP_REPO`, `OFLCASB_DLP_STORAGE`,
                    `OFLCASB_DLP_GENAI`

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, error = client.zia.casb_dlp_rules.delete_rule(
            ...     rule_type='OFLCASB_DLP_ITSM',
            ...     rule_id='1072324'
            ... )
            >>> if error:
            ...     print(f"Error deleting rule: {error}")
            ...     return
            ... print(f"Rule with ID 1072324 deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /casbDlpRules/{rule_id}
        """
        )
        params = {"ruleType": rule_type}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
