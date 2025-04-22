# flake8: noqa
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


class FailOpenPolicy(ZscalerObject):
    """
    A class for FailOpenPolicy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the FailOpenPolicy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active = config["active"] if "active" in config else None
            self.captive_portal_web_sec_disable_minutes = (
                config["captivePortalWebSecDisableMinutes"] if "captivePortalWebSecDisableMinutes" in config else None
            )
            self.company_id = config["companyId"] if "companyId" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.edited_by = config["editedBy"] if "editedBy" in config else None
            self.enable_captive_portal_detection = (
                config["enableCaptivePortalDetection"] if "enableCaptivePortalDetection" in config else None
            )
            self.enable_fail_open = config["enableFailOpen"] if "enableFailOpen" in config else None
            self.enable_strict_enforcement_prompt = (
                config["enableStrictEnforcementPrompt"] if "enableStrictEnforcementPrompt" in config else None
            )
            self.enable_web_sec_on_proxy_unreachable = (
                config["enableWebSecOnProxyUnreachable"] if "enableWebSecOnProxyUnreachable" in config else None
            )
            self.enable_web_sec_on_tunnel_failure = (
                config["enableWebSecOnTunnelFailure"] if "enableWebSecOnTunnelFailure" in config else None
            )
            self.id = config["id"] if "id" in config else None
            self.strict_enforcement_prompt_delay_minutes = (
                config["strictEnforcementPromptDelayMinutes"] if "strictEnforcementPromptDelayMinutes" in config else None
            )
            self.strict_enforcement_prompt_message = (
                config["strictEnforcementPromptMessage"] if "strictEnforcementPromptMessage" in config else None
            )
            self.tunnel_failure_retry_count = (
                config["tunnelFailureRetryCount"] if "tunnelFailureRetryCount" in config else None
            )
        else:
            self.active = None
            self.captive_portal_web_sec_disable_minutes = None
            self.company_id = None
            self.created_by = None
            self.edited_by = None
            self.enable_captive_portal_detection = None
            self.enable_fail_open = None
            self.enable_strict_enforcement_prompt = None
            self.enable_web_sec_on_proxy_unreachable = None
            self.enable_web_sec_on_tunnel_failure = None
            self.id = None
            self.strict_enforcement_prompt_delay_minutes = None
            self.strict_enforcement_prompt_message = None
            self.tunnel_failure_retry_count = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active": self.active,
            "captivePortalWebSecDisableMinutes": self.captive_portal_web_sec_disable_minutes,
            "companyId": self.company_id,
            "createdBy": self.created_by,
            "editedBy": self.edited_by,
            "enableCaptivePortalDetection": self.enable_captive_portal_detection,
            "enableFailOpen": self.enable_fail_open,
            "enableStrictEnforcementPrompt": self.enable_strict_enforcement_prompt,
            "enableWebSecOnProxyUnreachable": self.enable_web_sec_on_proxy_unreachable,
            "enableWebSecOnTunnelFailure": self.enable_web_sec_on_tunnel_failure,
            "id": self.id,
            "strictEnforcementPromptDelayMinutes": self.strict_enforcement_prompt_delay_minutes,
            "strictEnforcementPromptMessage": self.strict_enforcement_prompt_message,
            "tunnelFailureRetryCount": self.tunnel_failure_retry_count,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
