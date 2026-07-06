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
from zscaler.zia.models import common as common


class SmpcInstance(ZscalerObject):
    """
    A class representing a SmpcInstance object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.status = config["status"] if "status" in config else None
            self.alert_name = config["alertName"] if "alertName" in config else None
            self.occurrence = config["occurrence"] if "occurrence" in config else None
            self.traffic_change_percent = config["trafficChangePercent"] if "trafficChangePercent" in config else None
            self.interval = config["interval"] if "interval" in config else None
            self.scope = config["scope"] if "scope" in config else None
            if "entity" in config:
                if isinstance(config["entity"], common.CommonBlocks):
                    self.entity = config["entity"]
                elif config["entity"] is not None:
                    self.entity = common.CommonBlocks(config["entity"])
                else:
                    self.entity = None
            else:
                self.entity = None
            self.severity = config["severity"] if "severity" in config else None
            self.comments = config["comments"] if "comments" in config else None
        else:
            self.id = None
            self.status = None
            self.alert_name = None
            self.occurrence = None
            self.traffic_change_percent = None
            self.interval = None
            self.scope = None
            self.entity = None
            self.severity = None
            self.comments = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "status": self.status,
            "alertName": self.alert_name,
            "occurrence": self.occurrence,
            "trafficChangePercent": self.traffic_change_percent,
            "interval": self.interval,
            "scope": self.scope,
            "entity": self.entity,
            "severity": self.severity,
            "comments": self.comments,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
