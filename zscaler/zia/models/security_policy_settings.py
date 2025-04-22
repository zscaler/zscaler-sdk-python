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


class SecurityPolicySettings(ZscalerObject):
    """
    A class for Security Policy Settings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Security Policy Settings model based on API response.

        Args:
            config (dict): A dictionary representing the Security Policy Settings configuration.
        """
        super().__init__(config)

        # Defensive programming strategy with conditionals
        if config and isinstance(config, dict):
            self.whitelist_urls = config.get("whitelistUrls", []) if isinstance(config.get("whitelistUrls"), list) else []
            self.blacklist_urls = config.get("blacklistUrls", []) if isinstance(config.get("blacklistUrls"), list) else []
        else:
            self.whitelist_urls = []
            self.blacklist_urls = []

    def request_format(self):
        """
        Return the formatted representation of the Security Policy Settings object for request payload.
        """
        return {
            "whitelistUrls": self.whitelist_urls if isinstance(self.whitelist_urls, list) else [],
            "blacklistUrls": self.blacklist_urls if isinstance(self.blacklist_urls, list) else [],
        }
