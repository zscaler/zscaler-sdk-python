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


class Activation(ZscalerObject):
    """
    A class for Activation objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Activation model based on API response.

        Args:
            config (dict): A dictionary representing the Activation status configuration.
        """
        super().__init__(config)

        if config:
            self.status = config.get("status", None)
        else:
            self.status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class EusaStatus(ZscalerObject):
    """
    A class for Eusa Status objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Eusa Status model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None

            if "version" in config:
                if isinstance(config["version"], common.CommonBlocks):
                    self.version = config["version"]
                elif config["version"] is not None:
                    self.version = common.CommonBlocks(config["version"])
                else:
                    self.version = None
            else:
                self.version = None

            self.accepted_status = config["acceptedStatus"] \
                if "acceptedStatus" in config else None
        else:
            self.id = None
            self.version = None
            self.accepted_status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "version": self.version,
            "acceptedStatus": self.accepted_status
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
