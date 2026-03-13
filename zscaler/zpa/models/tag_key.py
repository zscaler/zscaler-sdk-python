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

from typing import Dict, List, Optional, Any
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class TagValue(ZscalerObject):
    """A class for TagValue objects within a TagKey."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id = config.get("id")
            self.name = config.get("name")
        else:
            self.id = None
            self.name = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {"id": self.id, "name": self.name}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TagKey(ZscalerObject):
    """A class for individual Tag Key objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.id = config.get("id")
            self.customer_id = config.get("customerId")
            self.name = config.get("name")
            self.description = config.get("description")
            self.enabled = config.get("enabled", False)
            self.namespace_id = config.get("namespaceId")
            self.origin = config.get("origin")
            self.type = config.get("type")
            self.microtenant_id = config.get("microtenantId")
            self.microtenant_name = config.get("microtenantName")
            self.skip_audit = config.get("skipAudit", False)
            self.tag_values = ZscalerCollection.form_list(config.get("tagValues", []), TagValue)
        else:
            self.id = None
            self.customer_id = None
            self.name = None
            self.description = None
            self.enabled = False
            self.namespace_id = None
            self.origin = None
            self.type = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.skip_audit = False
            self.tag_values = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        tag_values_fmt = [v.request_format() if hasattr(v, "request_format") else v for v in (self.tag_values or [])]
        current_obj_format = {
            "id": self.id,
            "customerId": self.customer_id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "namespaceId": self.namespace_id,
            "origin": self.origin,
            "type": self.type,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "skipAudit": self.skip_audit,
            "tagValues": tag_values_fmt,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class BulkUpdateStatusRequest(ZscalerObject):
    """Request body for bulk updating tag key status."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.enabled = config.get("enabled", False)
            self.tag_key_ids = config.get("tagKeyIds", []) or []
        else:
            self.enabled = False
            self.tag_key_ids = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "enabled": self.enabled,
            "tagKeyIds": self.tag_key_ids,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
