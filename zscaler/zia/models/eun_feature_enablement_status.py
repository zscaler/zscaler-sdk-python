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

from zscaler.oneapi_object import ZscalerObject


class EunFeatureEnablementStatus(ZscalerObject):
    """
    A class for EunFeatureEnablementStatus objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EunFeatureEnablementStatus model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.inline_dlp_status = config["inlineDlpStatus"] if "inlineDlpStatus" in config else None
            self.ept_dlp_status = config["eptDlpStatus"] if "eptDlpStatus" in config else None
            self.cloud_app_status = config["cloudAppStatus"] if "cloudAppStatus" in config else None
            self.url_filtering_status = config["urlFilteringStatus"] if "urlFilteringStatus" in config else None
            self.dns_rule_status = config["dnsRuleStatus"] if "dnsRuleStatus" in config else None
            self.firewall_filtering_status = config["firewallFilteringStatus"] if "firewallFilteringStatus" in config else None
            self.ips_control_status = config["ipsControlStatus"] if "ipsControlStatus" in config else None
            self.file_type_filtering_status = (
                config["fileTypeFilteringStatus"] if "fileTypeFilteringStatus" in config else None
            )
        else:
            self.inline_dlp_status = None
            self.ept_dlp_status = None
            self.cloud_app_status = None
            self.url_filtering_status = None
            self.dns_rule_status = None
            self.firewall_filtering_status = None
            self.ips_control_status = None
            self.file_type_filtering_status = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "inlineDlpStatus": self.inline_dlp_status,
            "eptDlpStatus": self.ept_dlp_status,
            "cloudAppStatus": self.cloud_app_status,
            "urlFilteringStatus": self.url_filtering_status,
            "dnsRuleStatus": self.dns_rule_status,
            "firewallFilteringStatus": self.firewall_filtering_status,
            "ipsControlStatus": self.ips_control_status,
            "fileTypeFilteringStatus": self.file_type_filtering_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
