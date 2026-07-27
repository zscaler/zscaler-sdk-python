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


class LlmProviderCredentials(ZscalerObject):
    """
    A class for LlmProviderCredentials objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LlmProviderCredentials model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.provider_id = config["providerId"] if "providerId" in config else None
            self.name = config["name"] if "name" in config else None
            self.expire_time_millis = config["expireTimeMillis"] if "expireTimeMillis" in config else None

            if "apiCredentials" in config:
                if isinstance(config["apiCredentials"], ApiCredentials):
                    self.api_credentials = config["apiCredentials"]
                elif config["apiCredentials"] is not None:
                    self.api_credentials = ApiCredentials(config["apiCredentials"])
                else:
                    self.api_credentials = None
            else:
                self.api_credentials = None
        else:
            self.provider_id = None
            self.name = None
            self.expire_time_millis = None
            self.api_credentials = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "providerId": self.provider_id,
            "name": self.name,
            "expireTimeMillis": self.expire_time_millis,
            "apiCredentials": self.api_credentials,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApiCredentials(ZscalerObject):
    """
    A class for ApiCredentials objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ApiCredentials model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.type = config["type"] if "type" in config else None
        else:
            self.type = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "type": self.type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
