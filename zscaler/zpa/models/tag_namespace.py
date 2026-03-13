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

from typing import Dict, Optional, Any
from zscaler.oneapi_object import ZscalerObject


class Namespace(ZscalerObject):
    """A class for individual Tag Namespace objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.id = config.get("id")
            self.name = config.get("name")
            self.description = config.get("description")
            self.enabled = config.get("enabled", False)
            self.origin = config.get("origin")
            self.type = config.get("type")
            self.microtenant_id = config.get("microtenantId")
            self.microtenant_name = config.get("microtenantName")
        else:
            self.id = None
            self.name = None
            self.description = None
            self.enabled = False
            self.origin = None
            self.type = None
            self.microtenant_id = None
            self.microtenant_name = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "origin": self.origin,
            "type": self.type,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class UpdateStatusRequest(ZscalerObject):
    """Request body for updating namespace status."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.enabled = config.get("enabled", False)
            self.namespace_id = config.get("namespaceId")
            self.microtenant_id = config.get("microtenantId")
            self.microtenant_name = config.get("microtenantName")
        else:
            self.enabled = False
            self.namespace_id = None
            self.microtenant_id = None
            self.microtenant_name = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "enabled": self.enabled,
            "namespaceId": self.namespace_id,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
