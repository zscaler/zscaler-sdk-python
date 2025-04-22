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
from zscaler.zia.models import common as common


class ZPAGateway(ZscalerObject):
    """
    A class representing a ZPA Gateway object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.type = config["type"] if "type" in config else None
            self.description = config["description"] if "description" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.zpa_tenant_id = config["zpaTenantId"] if "zpaTenantId" in config else None

            if "zpaServerGroup" in config:
                if isinstance(config["zpaServerGroup"], common.CommonBlocks):
                    self.zpa_server_group = config["zpaServerGroup"]
                elif config["zpaServerGroup"] is not None:
                    self.zpa_server_group = common.CommonBlocks(config["zpaServerGroup"])
                else:
                    self.zpa_server_group = None
            else:
                self.zpa_server_group = None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None

            self.zpa_app_segments = ZscalerCollection.form_list(
                config["zpaAppSegments"] if "zpaAppSegments" in config else [], common.ResourceReference
            )
        else:
            # Defaults when config is None
            self.id = None
            self.name = None
            self.type = None
            self.description = None
            self.last_modified_time = None
            self.zpa_tenant_id = None
            self.zpa_server_group = None
            self.zpa_app_segments = []
            self.last_modified_by = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "lastModifiedTime": self.last_modified_time,
            "zpaTenantId": self.zpa_tenant_id,
            "zpaServerGroup": self.zpa_server_group,
            "zpaAppSegments": self.zpa_app_segments,
            "lastModifiedBy": self.last_modified_by,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
