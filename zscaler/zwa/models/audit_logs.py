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


class AuditLogs(ZscalerObject):
    """
    A class for AuditLogs objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AuditLogs model based on API response.

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

            self.logs = ZscalerCollection.form_list(config["logs"] if "logs" in config else [], Logs)

        else:
            self.cursor = None
            self.logs = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"cursor": self.cursor, "logs": self.logs}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Logs(ZscalerObject):
    """
    A class for Logs objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Logs model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            if "action" in config:
                if isinstance(config["action"], Action):
                    self.action = config["action"]
                elif config["action"] is not None:
                    self.action = Action(config["action"])
                else:
                    self.action = None

            self.module = config["module"] if "module" in config else None
            self.resource = config["resource"] if "resource" in config else None
        else:
            self.action = None
            self.module = None
            self.resource = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "module": self.module,
            "resource": self.resource,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Action(ZscalerObject):
    """
    A class for Action objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Action model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.action = config["action"] if "action" in config else None
        else:
            self.action = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
