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
from zscaler.zia.models import urlcategory as urlcategory


class WebDlpGlobalOptions(ZscalerObject):
    """
    A class for WebDlpGlobalOptions objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the WebDlpGlobalOptions model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.exempt_url_encoded_data = config["exemptUrlEncodedData"] if "exemptUrlEncodedData" in config else None
            self.enable_npk_edm_templates = config["enableNpkEdmTemplates"] if "enableNpkEdmTemplates" in config else None
            self.enable_npk_edm_templates_for_org = (
                config["enableNpkEdmTemplatesForOrg"] if "enableNpkEdmTemplatesForOrg" in config else None
            )
            self.enable_inline_dlp_ocr = config["enableInlineDlpOcr"] if "enableInlineDlpOcr" in config else None
            self.enable_casb_ocr = config["enableCasbOcr"] if "enableCasbOcr" in config else None
            self.enable_email_dlp_ocr = config["enableEmailDlpOcr"] if "enableEmailDlpOcr" in config else None
            self.enable_evaluate_all_dlp_rules = (
                config["enableEvaluateAllDlpRules"] if "enableEvaluateAllDlpRules" in config else None
            )
            self.enable_edm_popular_format = config["enableEdmPopularFormat"] if "enableEdmPopularFormat" in config else None
            self.applications = ZscalerCollection.form_list(config["applications"] if "applications" in config else [], str)
            self.urls = ZscalerCollection.form_list(config["urls"] if "urls" in config else [], str)
            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], urlcategory.URLCategory
            )
            self.http_get_custom_url_categories = ZscalerCollection.form_list(
                config["httpGetCustomUrlCategories"] if "httpGetCustomUrlCategories" in config else [], str
            )
        else:
            self.exempt_url_encoded_data = None
            self.enable_npk_edm_templates = None
            self.enable_npk_edm_templates_for_org = None
            self.enable_inline_dlp_ocr = None
            self.enable_casb_ocr = None
            self.enable_email_dlp_ocr = None
            self.enable_evaluate_all_dlp_rules = None
            self.enable_edm_popular_format = None
            self.applications = []
            self.urls = []
            self.url_categories = []
            self.http_get_custom_url_categories = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "exemptUrlEncodedData": self.exempt_url_encoded_data,
            "enableNpkEdmTemplates": self.enable_npk_edm_templates,
            "enableNpkEdmTemplatesForOrg": self.enable_npk_edm_templates_for_org,
            "enableInlineDlpOcr": self.enable_inline_dlp_ocr,
            "enableCasbOcr": self.enable_casb_ocr,
            "enableEmailDlpOcr": self.enable_email_dlp_ocr,
            "enableEvaluateAllDlpRules": self.enable_evaluate_all_dlp_rules,
            "enableEdmPopularFormat": self.enable_edm_popular_format,
            "applications": self.applications,
            "urls": self.urls,
            "urlCategories": [item.request_format() for item in (self.url_categories or [])],
            "httpGetCustomUrlCategories": self.http_get_custom_url_categories,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
