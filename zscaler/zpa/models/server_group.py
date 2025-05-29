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
from zscaler.zpa.models import app_connector_groups as app_connector_groups
from zscaler.zpa.models import common as common


class ServerGroup(ZscalerObject):
    """
    A class for ServerGroup objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.ip_anchored = config["ipAnchored"] if "ipAnchored" in config else None
            self.config_space = config["configSpace"] if "configSpace" in config else None
            self.weight = config["weight"] if "weight" in config else None
            self.extranet_enabled = config["extranetEnabled"] if "extranetEnabled" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.dynamic_discovery = config["dynamicDiscovery"] if "dynamicDiscovery" in config else True
            self.read_only = config["readOnly"] if "readOnly" in config else None
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else None

            self.applications = ZscalerCollection.form_list(
                config["applications"] if "applications" in config else [], application_segment.ApplicationSegments
            )

            self.app_connector_groups = ZscalerCollection.form_list(
                config["appConnectorGroups"] if "appConnectorGroups" in config else [], app_connector_groups.AppConnectorGroup
            )
            if "extranetDTO" in config:
                if isinstance(config["extranetDTO"], common.ExtranetDTO):
                    self.extranet_dto = config["extranetDTO"]
                elif config["extranetDTO"] is not None:
                    self.extranet_dto = common.ExtranetDTO(config["extranetDTO"])
                else:
                    self.extranet_dto = None
            else:
                self.extranet_dto = None
        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.enabled = True
            self.name = None
            self.description = None
            self.ip_anchored = None
            self.config_space = None
            self.extranet_enabled = None
            self.microtenant_name = None
            self.weight = None
            self.dynamic_discovery = True
            self.applications = []
            self.app_connector_groups = []
            self.extranet_dto = None
            self.read_only = None
            self.restriction_type = None
            self.zscaler_managed = None

    def request_format(self):
        """
        Formats the current object for making requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "enabled": self.enabled,
            "name": self.name,
            "description": self.description,
            "ipAnchored": self.ip_anchored,
            "configSpace": self.config_space,
            "weight": self.weight,
            "extranetEnabled": self.extranet_enabled,
            "microtenantName": self.microtenant_name,
            "extranetDTO": self.extranet_dto,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "zscalerManaged": self.zscaler_managed,
            "dynamicDiscovery": True if self.dynamic_discovery else False,
            "applications": [app.request_format() for app in self.applications],
            "appConnectorGroups": [group.request_format() for group in self.app_connector_groups],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
