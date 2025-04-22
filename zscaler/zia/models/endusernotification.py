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

from zscaler.oneapi_object import ZscalerObject


class EndUserNotification(ZscalerObject):
    """
    A class for EndUserNotification objects.
    """

    def __init__(self, config=None):
        """
        Initialize the EndUserNotification model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.aup_frequency = config["aupFrequency"] if "aupFrequency" in config else None
            self.aup_custom_frequency = config["aupCustomFrequency"] if "aupCustomFrequency" in config else None

            self.aup_day_offset = config.get("aupDayOffset")

            self.aup_message = config["aupMessage"] if "aupMessage" in config else None
            self.notification_type = config["notificationType"] if "notificationType" in config else None

            self.display_reason = config.get("displayReason")

            self.display_comp_name = config["displayCompName"] if "displayCompName" in config else False
            self.display_comp_logo = config["displayCompLogo"] if "displayCompLogo" in config else False
            self.custom_text = config["customText"] if "customText" in config else None
            self.url_cat_review_enabled = config["urlCatReviewEnabled"] if "urlCatReviewEnabled" in config else False
            self.url_cat_review_submit_to_security_cloud = (
                config["urlCatReviewSubmitToSecurityCloud"] if "urlCatReviewSubmitToSecurityCloud" in config else False
            )
            self.url_cat_review_custom_location = (
                config["urlCatReviewCustomLocation"] if "urlCatReviewCustomLocation" in config else None
            )
            self.url_cat_review_text = config["urlCatReviewText"] if "urlCatReviewText" in config else None
            self.security_review_enabled = config["securityReviewEnabled"] if "securityReviewEnabled" in config else False
            self.security_review_submit_to_security_cloud = (
                config["securityReviewSubmitToSecurityCloud"] if "securityReviewSubmitToSecurityCloud" in config else False
            )
            self.security_review_custom_location = (
                config["securityReviewCustomLocation"] if "securityReviewCustomLocation" in config else None
            )
            self.security_review_text = config["securityReviewText"] if "securityReviewText" in config else None
            self.web_dlp_review_enabled = config["webDlpReviewEnabled"] if "webDlpReviewEnabled" in config else False
            self.web_dlp_review_submit_to_security_cloud = (
                config["webDlpReviewSubmitToSecurityCloud"] if "webDlpReviewSubmitToSecurityCloud" in config else False
            )
            self.web_dlp_review_custom_location = (
                config["webDlpReviewCustomLocation"] if "webDlpReviewCustomLocation" in config else None
            )
            self.web_dlp_review_text = config["webDlpReviewText"] if "webDlpReviewText" in config else None
            self.redirect_url = config["redirectUrl"] if "redirectUrl" in config else None
            self.support_email = config["supportEmail"] if "supportEmail" in config else None
            self.support_phone = config["supportPhone"] if "supportPhone" in config else None
            self.org_policy_link = config["orgPolicyLink"] if "orgPolicyLink" in config else None
            self.caution_again_after = config["cautionAgainAfter"] if "cautionAgainAfter" in config else None
            self.caution_per_domain = config["cautionPerDomain"] if "cautionPerDomain" in config else False
            self.caution_custom_text = config["cautionCustomText"] if "cautionCustomText" in config else None
            self.idp_proxy_notification_text = (
                config["idpProxyNotificationText"] if "idpProxyNotificationText" in config else None
            )
            self.quarantine_custom_notification_text = (
                config["quarantineCustomNotificationText"] if "quarantineCustomNotificationText" in config else None
            )
        else:
            self.aup_frequency = None
            self.aup_custom_frequency = None
            self.aup_day_offset = None
            self.aup_message = None
            self.notification_type = None
            self.display_reason = False
            self.display_comp_name = False
            self.display_comp_logo = False
            self.custom_text = None
            self.url_cat_review_enabled = False
            self.url_cat_review_submit_to_security_cloud = False
            self.url_cat_review_custom_location = None
            self.url_cat_review_text = None
            self.security_review_enabled = None
            self.security_review_submit_to_security_cloud = False
            self.security_review_custom_location = None
            self.security_review_text = None
            self.web_dlp_review_enabled = False
            self.web_dlp_review_submit_to_security_cloud = False
            self.web_dlp_review_custom_location = None
            self.web_dlp_review_text = None
            self.redirect_url = None
            self.support_email = None
            self.support_phone = None
            self.org_policy_link = None
            self.caution_again_after = None
            self.caution_per_domain = False
            self.caution_custom_text = None
            self.idp_proxy_notification_text = None
            self.quarantine_custom_notification_text = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "aupFrequency": self.aup_frequency,
            "aupCustomFrequency": self.aup_custom_frequency,
            "aupDayOffset": self.aup_day_offset,
            "aupMessage": self.aup_message,
            "notificationType": self.notification_type,
            "displayReason": self.display_reason,
            "displayCompName": self.display_comp_name,
            "displayCompLogo": self.display_comp_logo,
            "customText": self.custom_text,
            "urlCatReviewEnabled": self.url_cat_review_enabled,
            "urlCatReviewSubmitToSecurityCloud": self.url_cat_review_submit_to_security_cloud,
            "urlCatReviewCustomLocation": self.url_cat_review_custom_location,
            "urlCatReviewText": self.url_cat_review_text,
            "securityReviewEnabled": self.security_review_enabled,
            "securityReviewSubmitToSecurityCloud": self.security_review_submit_to_security_cloud,
            "securityReviewCustomLocation": self.security_review_custom_location,
            "securityReviewText": self.security_review_text,
            "webDlpReviewEnabled": self.web_dlp_review_enabled,
            "webDlpReviewSubmitToSecurityCloud": self.web_dlp_review_submit_to_security_cloud,
            "webDlpReviewCustomLocation": self.web_dlp_review_custom_location,
            "webDlpReviewText": self.web_dlp_review_text,
            "redirectUrl": self.redirect_url,
            "supportEmail": self.support_email,
            "supportPhone": self.support_phone,
            "orgPolicyLink": self.org_policy_link,
            "cautionAgainAfter": self.caution_again_after,
            "cautionPerDomain": self.caution_per_domain,
            "cautionCustomText": self.caution_custom_text,
            "idpProxyNotificationText": self.idp_proxy_notification_text,
            "quarantineCustomNotificationText": self.quarantine_custom_notification_text,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
