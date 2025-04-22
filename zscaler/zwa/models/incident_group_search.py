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
from zscaler.zwa.models import common as common


class IncidentGroupSearch(ZscalerObject):
    """
    A class for IncidentGroupSearch objects.
    """

    def __init__(self, config=None):
        """
        Initialize the IncidentGroupSearch model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.incident_groups = ZscalerCollection.form_list(
                config["incidentGroups"] if "incidentGroups" in config else [], common.IncidentGroups
            )

            self.incident_group_ids = ZscalerCollection.form_list(
                config["incidentGroupIds"] if "incidentGroupIds" in config else [], str
            )

        else:
            self.incident_groups = []
            self.incident_group_ids = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "incidentGroups": self.incident_groups,
            "incidentGroupIds": self.incident_group_ids,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
