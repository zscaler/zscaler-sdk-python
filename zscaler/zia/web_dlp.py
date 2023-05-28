# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import json

from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from zscaler.utils import snake_to_camel


class WebDLPAPI(APIEndpoint):
    _key_id_list = [
        "auditor",
        "departments",
        "dlp_engines",
        "exclude_departments",
        "exclude_groups",
        "exclude_users",
        "groups",
        "icap_server",
        "labels",
        "locations",
        "location_groups",
        "notification_template",
        "time_windows",
        "users",
        "url_categories",
    ]

    def list_rules(self, **kwargs) -> BoxList:
        """
        Returns a list of DLP policy rules, excluding SaaS Security API DLP policy rules.

        Returns:
            :obj:`BoxList`: List of Web DLP items.

        Examples:
            Get a list of all Web DLP rules

            >>> results = zia.web_dlp.list_rules()
            ... for item in results:
            ...    print(rule)

        """
        return self._get("webDlpRules")

    def get_rule(self, rule_id: str) -> Box:
        """
        Returns a DLP policy rule, excluding SaaS Security API DLP policy rules.

        Args:
            rule_id (str): The unique id for the Web DLP rule.

        Returns:
            :obj:`Box`: The Web DLP Rule resource record.

        Examples:
            >>> pprint(zia.web_dlp.get_rule('431233'))

        """
        return self._get(f"webDlpRules/{rule_id}")

    def list_rules_lite(self) -> BoxList:
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
        return self._get("webDlpRules/lite")

    def add_rule(self, name: str, action: str, **kwargs) -> Box:
        """
        Adds a new DLP policy rule.

        Args:
            name (str): The name of the filter rule. 31 char limit.
            action (str): The action for the filter rule.
            **kwargs: Optional keyword args

        Keyword Args:
            auditor (list): The IDs for the auditors that this rule applies to.
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            description (str): Additional information about the rule
            external_auditor_email (str): The email address of an external auditor to whom DLP email notifications are sent.
            cloud_applications (list): The list of cloud applications to which the DLP policy rule must be applied.
            file_types (list): The list of file types to which the DLP policy rule must be applied.
            groups (list): The IDs for the groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): The IDs for the time windows that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            protocols (list): The protocol criteria specified for the DLP policy rule. Accepted values are 'ANY_RULE', 'FTP_RULE', 'HTTP_RULE', 'HTTPS_RULE'.
            url_categories (list): The IDs for the URL Categories that this rule applies to.
            dlp_engines (list): The IDs for the URL Categories that this rule applies to.
            min_size (int): The minimum file size (in KB) used for evaluation of the DLP policy rule.
            notification_template (list): The IDs for the Notification Template that this rule applies to.
            match_only (bool): The match only criteria for DLP engines.
            ocr_enabled (bool): Enables or disables image file scanning
            without_content_inspection (bool): Indicates a DLP policy rule without content inspection, when the value is set to true.
            icap_server (list): The IDs for the ICAP Server that this rule applies to.
            excluded_groups (list): The IDs for the excluded groups that this rule applies to.
            excluded_departments (list): The IDs for the excluded departments that this rule applies to.
            excluded_users (list): The IDs for the excluded users that this rule applies to.
            zscaler_incident_receiver (bool): Indicates whether a Zscaler Incident Receiver is associated to the DLP policy rule.

        Returns:
            :obj:`Box`: The new web dlp rule resource record.

        Examples:
            Add a rule to allow all traffic to Google DNS (admin ranking is enabled):

            >>> zia.web_dlp.add_rule(rank='7',
            ...    name='ALLOW_ANY_TO_GOOG-DNS',
            ...    action='ALLOW'
            ...    description='TT#1965432122')

            Add a rule to block all traffic to Quad9 DNS for all users in Finance Group and send an ICMP error:

            >>> zia.web_dlp.add_rule(rank='7',
            ...    name='BLOCK_PCI_DATA',
            ...    action='BLOCK_ICMP'
            ...    groups=['95016183']
            ...    description='TT#1965432122')

        """
        payload = {
            "name": name,
            "action": action,
            "order": kwargs.pop("order", len(self.list_rules())),
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key in self._key_id_list:
                payload[snake_to_camel(key)] = []
                for item in value:
                    payload[snake_to_camel(key)].append({"id": item})
            else:
                payload[snake_to_camel(key)] = value

        return self._post("webDlpRules", json=payload)

    def update_rule(self, rule_id: str, payload: dict) -> Box:
        """
        Updates a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            rule_id (str): String of ID.
            **kwargs: Optional keyword args

        Keywork Args:
            auditor (list): The IDs for the auditors that this rule applies to.
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            description (str): Additional information about the rule
            external_auditor_email (str): The email address of an external auditor to whom DLP email notifications are sent.
            cloud_applications (list): The list of cloud applications to which the DLP policy rule must be applied.
            file_types (list): The list of file types to which the DLP policy rule must be applied.
            groups (list): The IDs for the groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            time_windows (list): The IDs for the time windows that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            protocols (list): The protocol criteria specified for the DLP policy rule. Accepted values are 'ANY_RULE', 'FTP_RULE', 'HTTP_RULE', 'HTTPS_RULE'.
            url_categories (list): The IDs for the URL Categories that this rule applies to.
            dlp_engines (list): The IDs for the URL Categories that this rule applies to.
            min_size (int): The minimum file size (in KB) used for evaluation of the DLP policy rule.
            notification_template (list): The IDs for the Notification Template that this rule applies to.
            match_only (bool): The match only criteria for DLP engines.
            ocr_enabled (bool): Enables or disables image file scanning
            without_content_inspection (bool): Indicates a DLP policy rule without content inspection, when the value is set to true.
            icap_server (list): The IDs for the ICAP Server that this rule applies to.
            excluded_groups (list): The IDs for the excluded groups that this rule applies to.
            excluded_departments (list): The IDs for the excluded departments that this rule applies to.
            excluded_users (list): The IDs for the excluded users that this rule applies to.
            zscaler_incident_receiver (bool): Indicates whether a Zscaler Incident Receiver is associated to the DLP policy rule.

        Returns:
            :obj:`Box`: The updated Web DLP Policy Rule resource record.

        Examples:
            Update a Web DLP Policy Rule::

                 payload = zia.web_dlp.get_rule('9999')
                 payload['name'] = "daxm updated name."
                 results = zia.web_dlp.update_rule(rule_id=9999, payload=payload)
                 print(results)

        """
        return self._put(f"webDlpRules/{rule_id}", json=payload)

    def delete_rule(self, rule_id: str) -> Box:
        """
        Deletes a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            rule_id (str): Unique id of the Web DLP Policy Rule that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Delete a rule with an id of 9999.

            >>> results = zia.web_dlp.delete_rule(rule_id=9999)
            ... print(results)


        """
        return self._delete(f"webDlpRules/{rule_id}")
