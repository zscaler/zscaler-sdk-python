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
from zscaler.zia.models import common


class TrafficDcExclusions(ZscalerObject):
    """
    A class for TrafficDcExclusions objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TrafficDcExclusions model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.dcid = config["dcid"] if "dcid" in config else None
            self.expired = config["expired"] if "expired" in config else None
            self.start_time = config["startTime"] if "startTime" in config else None
            self.end_time = config["endTime"] if "endTime" in config else None
            self.description = config["description"] if "description" in config else None
            self.expired = config["expired"] if "expired" in config else None

            if "dcName" in config:
                if isinstance(config["dcName"], common.CommonBlocks):
                    self.dc_name = config["dcName"]
                elif config["dcName"] is not None:
                    self.dc_name = common.CommonBlocks(config["dcName"])
                else:
                    self.dc_name = None
            else:
                self.dc_name = None
        else:
            self.dcid = None
            self.expired = None
            self.start_time = None
            self.end_time = None
            self.description = None
            self.dc_name = None
            self.expired = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "dcid": self.dcid,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "description": self.description,
            "dcName": self.dc_name,
            "expired": self.expired,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
