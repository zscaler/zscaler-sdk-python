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
from zscaler.zpa.models import application_segment as application_segment


class SegmentGroup(ZscalerObject):
    """
    A class for Segment Group objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.policy_migrated = config["policyMigrated"] if "policyMigrated" in config else None
            self.config_space = config["configSpace"] if "configSpace" in config else None
            self.tcp_keep_alive_enabled = config["tcpKeepAliveEnabled"] if "tcpKeepAliveEnabled" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.skip_detailed_app_info = config["skipDetailedAppInfo"] if "skipDetailedAppInfo" in config else None

            self.applications = (
                ZscalerCollection.form_list(config["applications"], application_segment.ApplicationSegments)
                if "applications" in config
                else []
            )
        else:
            self.id = None
            self.name = None
            self.description = None
            self.enabled = None
            self.policy_migrated = None
            self.config_space = None
            self.tcp_keep_alive_enabled = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.skip_detailed_app_info = None
            self.applications = []

    def request_format(self):
        """
        Formats the Segment Group data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "policyMigrated": self.policy_migrated,
            "configSpace": self.config_space,
            "tcpKeepAliveEnabled": self.tcp_keep_alive_enabled,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "skipDetailedAppInfo": self.skip_detailed_app_info,
            "applications": [app.as_dict() for app in self.applications],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
