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

# AUTO-GENERATED! DO NOT EDIT FILE DIRECTLY
# SEE CONTRIBUTOR DOCUMENTATION
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class Advancedurlfilterandcloudappsettings(ZscalerObject):
    """
    A class for Advancedurlfilterandcloudappsettings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Advancedurlfilterandcloudappsettings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.enable_dynamic_content_cat = config["enableDynamicContentCat"] \
                if "enableDynamicContentCat" in config else None
            self.consider_embedded_sites = config["considerEmbeddedSites"] \
                if "considerEmbeddedSites" in config else None
            self.enforce_safe_search = config["enforceSafeSearch"] \
                if "enforceSafeSearch" in config else None
            self.enable_office365 = config["enableOffice365"] \
                if "enableOffice365" in config else None
            self.enable_msft_o365 = config["enableMsftO365"] \
                if "enableMsftO365" in config else None
            self.enable_ucaas_zoom = config["enableUcaasZoom"] \
                if "enableUcaasZoom" in config else None
            self.enable_ucaas_log_me_in = config["enableUcaasLogMeIn"] \
                if "enableUcaasLogMeIn" in config else None
            self.enable_ucaas_ring_central = config["enableUcaasRingCentral"] \
                if "enableUcaasRingCentral" in config else None
            self.enable_ucaas_webex = config["enableUcaasWebex"] \
                if "enableUcaasWebex" in config else None
            self.enable_ucaas_talkdesk = config["enableUcaasTalkdesk"] \
                if "enableUcaasTalkdesk" in config else None
            self.enable_chat_gpt_prompt = config["enableChatGptPrompt"] \
                if "enableChatGptPrompt" in config else None
            self.enable_microsoft_co_pilot_prompt = config["enableMicrosoftCoPilotPrompt"] \
                if "enableMicrosoftCoPilotPrompt" in config else None
            self.enable_gemini_prompt = config["enableGeminiPrompt"] \
                if "enableGeminiPrompt" in config else None
            self.enable_p_o_e_prompt = config["enablePOEPrompt"] \
                if "enablePOEPrompt" in config else None
            self.enable_meta_prompt = config["enableMetaPrompt"] \
                if "enableMetaPrompt" in config else None
            self.enable_per_plexity_prompt = config["enablePerPlexityPrompt"] \
                if "enablePerPlexityPrompt" in config else None
            self.block_skype = config["blockSkype"] \
                if "blockSkype" in config else None
            self.enable_newly_registered_domains = config["enableNewlyRegisteredDomains"] \
                if "enableNewlyRegisteredDomains" in config else None
            self.enable_block_override_for_non_auth_user = config["enableBlockOverrideForNonAuthUser"] \
                if "enableBlockOverrideForNonAuthUser" in config else None
            self.enable_c_i_p_a_compliance = config["enableCIPACompliance"] \
                if "enableCIPACompliance" in config else None
        else:
            self.enable_dynamic_content_cat = None
            self.consider_embedded_sites = None
            self.enforce_safe_search = None
            self.enable_office365 = None
            self.enable_msft_o365 = None
            self.enable_ucaas_zoom = None
            self.enable_ucaas_log_me_in = None
            self.enable_ucaas_ring_central = None
            self.enable_ucaas_webex = None
            self.enable_ucaas_talkdesk = None
            self.enable_chat_gpt_prompt = None
            self.enable_microsoft_co_pilot_prompt = None
            self.enable_gemini_prompt = None
            self.enable_p_o_e_prompt = None
            self.enable_meta_prompt = None
            self.enable_per_plexity_prompt = None
            self.block_skype = None
            self.enable_newly_registered_domains = None
            self.enable_block_override_for_non_auth_user = None
            self.enable_c_i_p_a_compliance = None

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
            "enableMicrosoftCoPilotPrompt": self.enable_microsoft_co_pilot_prompt,
            "enableGeminiPrompt": self.enable_gemini_prompt,
            "enablePOEPrompt": self.enable_p_o_e_prompt,
            "enableMetaPrompt": self.enable_meta_prompt,
            "enablePerPlexityPrompt": self.enable_per_plexity_prompt,
            "blockSkype": self.block_skype,
            "enableNewlyRegisteredDomains": self.enable_newly_registered_domains,
            "enableBlockOverrideForNonAuthUser": self.enable_block_override_for_non_auth_user,
            "enableCIPACompliance": self.enable_c_i_p_a_compliance
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format