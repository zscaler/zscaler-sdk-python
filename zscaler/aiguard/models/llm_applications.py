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


class LlmApplications(ZscalerObject):
    """
    A class for LlmApplications objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LlmApplications model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.owner_email = config["ownerEmail"] if "ownerEmail" in config else None
            self.create_time_millis = config["createTimeMillis"] if "createTimeMillis" in config else None
            self.update_time_millis = config["updateTimeMillis"] if "updateTimeMillis" in config else None

            if "applicationSettings" in config:
                if isinstance(config["applicationSettings"], ApplicationSettings):
                    self.application_settings = config["applicationSettings"]
                elif config["applicationSettings"] is not None:
                    self.application_settings = ApplicationSettings(config["applicationSettings"])
                else:
                    self.application_settings = None
            else:
                self.application_settings = None
        else:
            self.id = None
            self.name = None
            self.owner_email = None
            self.create_time_millis = None
            self.update_time_millis = None
            self.application_settings = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "ownerEmail": self.owner_email,
            "createTimeMillis": self.create_time_millis,
            "updateTimeMillis": self.update_time_millis,
            "applicationSettings": self.application_settings,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationSettings(ZscalerObject):
    """
    A class for ApplicationSettings objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ApplicationSettings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.include_event_contents = config["includeEventContents"] if "includeEventContents" in config else None
            self.encrypt_event_contents = config["encryptEventContents"] if "encryptEventContents" in config else None
        else:
            self.include_event_contents = None
            self.encrypt_event_contents = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "includeEventContents": self.include_event_contents,
            "encryptEventContents": self.encrypt_event_contents,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
