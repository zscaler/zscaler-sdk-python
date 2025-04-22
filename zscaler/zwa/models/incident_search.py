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
from zscaler.zwa.models import incident_details as incident_details


class IncidentSearch(ZscalerObject):
    """
    A class for IncidentSearch objects.
    """

    def __init__(self, config=None):
        """
        Initialize the IncidentSearch model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            if "cursor" in config:
                if isinstance(config["cursor"], common.Common):
                    self.cursor = config["cursor"]
                elif config["cursor"] is not None:
                    self.cursor = common.Common(config["cursor"])
                else:
                    self.cursor = None
            else:
                self.cursor = None

            self.incidents = ZscalerCollection.form_list(config["incidents"] if "incidents" in config else [], Incidents)
        else:
            self.cursor = None
            self.incidents = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"cursor": self.cursor, "incidents": self.incidents}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Incidents(ZscalerObject):
    """
    A class for Incidents objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Incidents model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.incidents = ZscalerCollection.form_list(
                config["incidents"] if "incidents" in config else [], incident_details.IncidentDLPDetails
            )
        else:
            self.incidents = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "incidents": self.incidents,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
