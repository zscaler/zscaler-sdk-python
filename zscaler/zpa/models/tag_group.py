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


class TagGroupNamespace(ZscalerObject):
    """Namespace reference within a Tag (used in TagGroup)."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id = config.get("id")
            self.name = config.get("name")
            self.enabled = config.get("enabled", False)
        else:
            self.id = None
            self.name = None
            self.enabled = False

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TagGroupTagKey(ZscalerObject):
    """TagKey reference within a Tag (used in TagGroup)."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id = config.get("id")
            self.name = config.get("name")
            self.enabled = config.get("enabled", False)
        else:
            self.id = None
            self.name = None
            self.enabled = False

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TagGroupTagValue(ZscalerObject):
    """TagValue reference within a Tag (used in TagGroup)."""

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


class TagGroupTag(ZscalerObject):
    """A Tag within a TagGroup (namespace + tagKey + tagValue)."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.origin = config.get("origin")
            if config.get("namespace"):
                self.namespace = TagGroupNamespace(config["namespace"])
            else:
                self.namespace = None
            if config.get("tagKey"):
                self.tag_key = TagGroupTagKey(config["tagKey"])
            else:
                self.tag_key = None
            if config.get("tagValue"):
                self.tag_value = TagGroupTagValue(config["tagValue"])
            else:
                self.tag_value = None
        else:
            self.namespace = None
            self.origin = None
            self.tag_key = None
            self.tag_value = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "namespace": self.namespace.request_format() if self.namespace else None,
            "origin": self.origin,
            "tagKey": self.tag_key.request_format() if self.tag_key else None,
            "tagValue": self.tag_value.request_format() if self.tag_value else None,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TagGroup(ZscalerObject):
    """A class for individual Tag Group objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.id = config.get("id")
            self.name = config.get("name")
            self.description = config.get("description")
            self.microtenant_id = config.get("microtenantId")
            self.microtenant_name = config.get("microtenantName")
            self.tags = ZscalerCollection.form_list(config.get("tags", []), TagGroupTag)
        else:
            self.id = None
            self.name = None
            self.description = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.tags = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        tags_fmt = [t.request_format() if hasattr(t, "request_format") else t for t in (self.tags or [])]
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "tags": tags_fmt,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
