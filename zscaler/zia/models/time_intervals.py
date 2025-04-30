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
from zscaler.oneapi_collection import ZscalerCollection


class TimeIntervals(ZscalerObject):
    """
    A class for TimeIntervals objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TimeIntervals model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.start_time = config["startTime"] if "startTime" in config else None
            self.end_time = config["endTime"] if "endTime" in config else None

            self.days_of_week = ZscalerCollection.form_list(config["daysOfWeek"] if "daysOfWeek" in config else [], str)
        else:
            self.id = None
            self.name = None
            self.start_time = None
            self.end_time = None
            self.days_of_week = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "daysOfWeek": self.days_of_week,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
