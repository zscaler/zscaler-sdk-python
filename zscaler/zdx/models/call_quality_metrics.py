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


class CallQualityMetrics(ZscalerObject):
    """
    A class for CallQualityMetrics objects.
    """

    def __init__(self, config=None):
        """
        Initialize the CallQualityMetrics model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.meet_id = config["meet_id"] if "meet_id" in config else None
            self.meet_session_id = config["meet_session_id"] if "meet_session_id" in config else None
            self.meet_subject = config["meet_subject"] if "meet_subject" in config else None
            self.metrics = ZscalerCollection.form_list(config["metrics"] if "metrics" in config else [], str)
        else:
            self.meet_id = None
            self.meet_session_id = None
            self.meet_subject = None
            self.metrics = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "meet_id": self.meet_id,
            "meet_session_id": self.meet_session_id,
            "meet_subject": self.meet_subject,
            "metrics": self.metrics,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
