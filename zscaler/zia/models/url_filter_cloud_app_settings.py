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


class AdvancedUrlFilterAndCloudAppSettings(ZscalerObject):
    """
    A class for AdvancedUrlFilterAndCloudAppSettings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdvancedUrlFilterAndCloudAppSettings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.enable_dynamic_content_cat = (
                config["enableDynamicContentCat"] if "enableDynamicContentCat" in config else False
            )
            self.consider_embedded_sites = config["considerEmbeddedSites"] if "considerEmbeddedSites" in config else False
            self.enforce_safe_search = config["enforceSafeSearch"] if "enforceSafeSearch" in config else False
            self.enable_office365 = config["enableOffice365"] if "enableOffice365" in config else False
            self.enable_msft_o365 = config["enableMsftO365"] if "enableMsftO365" in config else False
            self.enable_ucaas_zoom = config["enableUcaasZoom"] if "enableUcaasZoom" in config else False
            self.enable_ucaas_log_me_in = config["enableUcaasLogMeIn"] if "enableUcaasLogMeIn" in config else False
            self.enable_ucaas_ring_central = config["enableUcaasRingCentral"] if "enableUcaasRingCentral" in config else False
            self.enable_ucaas_webex = config["enableUcaasWebex"] if "enableUcaasWebex" in config else False
            self.enable_ucaas_talkdesk = config["enableUcaasTalkdesk"] if "enableUcaasTalkdesk" in config else False
            self.enable_chat_gpt_prompt = config["enableChatGptPrompt"] if "enableChatGptPrompt" in config else False
            self.enable_microsoft_copilot_prompt = (
                config["enableMicrosoftCoPilotPrompt"] if "enableMicrosoftCoPilotPrompt" in config else False
            )
            self.enable_gemini_prompt = config["enableGeminiPrompt"] if "enableGeminiPrompt" in config else False
            self.enable_poe_prompt = config["enablePOEPrompt"] if "enablePOEPrompt" in config else False
            self.enable_meta_prompt = config["enableMetaPrompt"] if "enableMetaPrompt" in config else False
            self.enable_perplexity_prompt = config["enablePerPlexityPrompt"] if "enablePerPlexityPrompt" in config else False
            self.block_skype = config["blockSkype"] if "blockSkype" in config else False
            self.enable_newly_registered_domains = (
                config["enableNewlyRegisteredDomains"] if "enableNewlyRegisteredDomains" in config else False
            )
            self.enable_block_override_for_non_auth_user = (
                config["enableBlockOverrideForNonAuthUser"] if "enableBlockOverrideForNonAuthUser" in config else False
            )
            self.enable_cipa_compliance = config["enableCIPACompliance"] if "enableCIPACompliance" in config else False
        else:
            self.enable_dynamic_content_cat = False
            self.consider_embedded_sites = False
            self.enforce_safe_search = False
            self.enable_office365 = False
            self.enable_msft_o365 = False
            self.enable_ucaas_zoom = False
            self.enable_ucaas_log_me_in = False
            self.enable_ucaas_ring_central = False
            self.enable_ucaas_webex = False
            self.enable_ucaas_talkdesk = False
            self.enable_chat_gpt_prompt = False
            self.enable_microsoft_copilot_prompt = False
            self.enable_gemini_prompt = False
            self.enable_poe_prompt = False
            self.enable_meta_prompt = False
            self.enable_perplexity_prompt = False
            self.block_skype = False
            self.enable_newly_registered_domains = False
            self.enable_block_override_for_non_auth_user = False
            self.enable_cipa_compliance = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "enableDynamicContentCat": self.enable_dynamic_content_cat,
            "considerEmbeddedSites": self.consider_embedded_sites,
            "enforceSafeSearch": self.enforce_safe_search,
            "enableOffice365": self.enable_office365,
            "enableMsftO365": self.enable_msft_o365,
            "enableUcaasZoom": self.enable_ucaas_zoom,
            "enableUcaasLogMeIn": self.enable_ucaas_log_me_in,
            "enableUcaasRingCentral": self.enable_ucaas_ring_central,
            "enableUcaasWebex": self.enable_ucaas_webex,
            "enableUcaasTalkdesk": self.enable_ucaas_talkdesk,
            "enableChatGptPrompt": self.enable_chat_gpt_prompt,
            "enableMicrosoftCoPilotPrompt": self.enable_microsoft_copilot_prompt,
            "enableGeminiPrompt": self.enable_gemini_prompt,
            "enablePOEPrompt": self.enable_poe_prompt,
            "enableMetaPrompt": self.enable_meta_prompt,
            "enablePerPlexityPrompt": self.enable_perplexity_prompt,
            "blockSkype": self.block_skype,
            "enableNewlyRegisteredDomains": self.enable_newly_registered_domains,
            "enableBlockOverrideForNonAuthUser": self.enable_block_override_for_non_auth_user,
            "enableCIPACompliance": self.enable_cipa_compliance,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
