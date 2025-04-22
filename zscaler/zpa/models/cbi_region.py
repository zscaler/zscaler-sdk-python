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


class CBIRegion(ZscalerObject):
    """
    A class representing a Cloud Browser Isolation Region object.
    """

    def __init__(self, config=None):
        """
        Initialize the CBIRegion object.

        Args:
            config (dict): A dictionary representing the cloud browser isolation region.
        """
        super().__init__(config)

        # Defensive strategy for initializing each field
        self.id = config["id"] if config and "id" in config else None
        self.name = config["name"] if config and "name" in config else None

    def request_format(self):
        """
        Prepare the object in a format suitable for sending as a request payload.

        Returns:
            dict: A dictionary representing the CBI region for API requests.
        """
        return {"id": self.id, "name": self.name}
