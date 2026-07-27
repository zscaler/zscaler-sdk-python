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

from typing import Any, Dict, Optional

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject


class PolicyMatchRules(ZscalerObject):
    """
    A class for PolicyMatchRules objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the PolicyMatchRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.policy_id = config["policyId"] if "policyId" in config else None
            self.name = config["name"] if "name" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.rule_order = config["ruleOrder"] if "ruleOrder" in config else None
            self.version = config["version"] if "version" in config else None

            if "matchCriteria" in config:
                if isinstance(config["matchCriteria"], MatchCriteria):
                    self.match_criteria = config["matchCriteria"]
                elif config["matchCriteria"] is not None:
                    self.match_criteria = MatchCriteria(config["matchCriteria"])
                else:
                    self.match_criteria = None
            else:
                self.match_criteria = None
        else:
            self.id = None
            self.policy_id = None
            self.name = None
            self.enabled = None
            self.rule_order = None
            self.version = None
            self.match_criteria = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "policyId": self.policy_id,
            "name": self.name,
            "enabled": self.enabled,
            "ruleOrder": self.rule_order,
            "version": self.version,
            "matchCriteria": self.match_criteria,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MatchCriteria(ZscalerObject):
    """
    A class for MatchCriteria objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the MatchCriteria model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.type = config["type"] if "type" in config else None
            self.llm_applications = ZscalerCollection.form_list(
                config["llmApplications"] if "llmApplications" in config else [], LlmApplication
            )
            self.source_ip_addresses = ZscalerCollection.form_list(
                config["sourceIpAddresses"] if "sourceIpAddresses" in config else [], str
            )
            self.application_groups = ZscalerCollection.form_list(
                config["applicationGroups"] if "applicationGroups" in config else [], str
            )
            self.custom_request_headers = ZscalerCollection.form_list(
                config["customRequestHeaders"] if "customRequestHeaders" in config else [], str
            )
        else:
            self.type = None
            self.llm_applications = []
            self.source_ip_addresses = []
            self.application_groups = []
            self.custom_request_headers = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "type": self.type,
            "llmApplications": [item.request_format() for item in (self.llm_applications or [])],
            "sourceIpAddresses": self.source_ip_addresses,
            "applicationGroups": self.application_groups,
            "customRequestHeaders": self.custom_request_headers,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LlmApplication(ZscalerObject):
    """
    A class for LlmApplication objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LlmApplication model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.application_id = config["applicationId"] if "applicationId" in config else None
            self.application_credentials_ids = ZscalerCollection.form_list(
                config["applicationCredentialsIds"] if "applicationCredentialsIds" in config else [], int
            )
        else:
            self.application_id = None
            self.application_credentials_ids = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "applicationId": self.application_id,
            "applicationCredentialsIds": self.application_credentials_ids,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
