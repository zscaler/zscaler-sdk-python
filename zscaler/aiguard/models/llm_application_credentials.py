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


class LlmApplicationCredentials(ZscalerObject):
    """
    A class for LlmApplicationCredentials objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LlmApplicationCredentials model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.application_id = config["applicationId"] if "applicationId" in config else None
            self.provider_id = config["providerId"] if "providerId" in config else None
            self.provider_credentials_id = config["providerCredentialsId"] if "providerCredentialsId" in config else None
            self.name = config["name"] if "name" in config else None
            self.mode = config["mode"] if "mode" in config else None
            self.create_time_millis = config["createTimeMillis"] if "createTimeMillis" in config else None
            self.update_time_millis = config["updateTimeMillis"] if "updateTimeMillis" in config else None
        else:
            self.id = None
            self.application_id = None
            self.provider_id = None
            self.provider_credentials_id = None
            self.name = None
            self.mode = None
            self.create_time_millis = None
            self.update_time_millis = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "applicationId": self.application_id,
            "providerId": self.provider_id,
            "providerCredentialsId": self.provider_credentials_id,
            "name": self.name,
            "mode": self.mode,
            "createTimeMillis": self.create_time_millis,
            "updateTimeMillis": self.update_time_millis,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
