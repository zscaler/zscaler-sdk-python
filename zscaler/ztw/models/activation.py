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


class Activation(ZscalerObject):
    """
    A class for Activation objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Activation model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.org_edit_status = config["orgEditStatus"] if "orgEditStatus" in config else None
            self.org_last_activate_status = config["orgLastActivateStatus"] if "orgLastActivateStatus" in config else None
            self.admin_status_map = config["adminStatusMap"] if "adminStatusMap" in config else None
            self.admin_activate_status = config["adminActivateStatus"] if "adminActivateStatus" in config else None
        else:
            self.org_edit_status = None
            self.org_last_activate_status = None
            self.admin_status_map = None
            self.admin_activate_status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "orgEditStatus": self.org_edit_status,
            "orgLastActivateStatus": self.org_last_activate_status,
            "adminStatusMap": self.admin_status_map,
            "adminActivateStatus": self.admin_activate_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
