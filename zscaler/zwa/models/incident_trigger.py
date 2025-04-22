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


class IncidentTrigger(ZscalerObject):
    """
    A class for IncidentTrigger objects.
    Handles arbitrary keys dynamically.
    """

    def __init__(self, config=None):
        """
        Initialize the IncidentTrigger model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)

        # Store the entire dictionary since API does not return a fixed structure
        self.triggers = config if isinstance(config, dict) else {}

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"triggers": self.triggers}
        parent_req_format.update(current_obj_format)
        return parent_req_format
