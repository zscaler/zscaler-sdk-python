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

from typing import Any, Dict, List, Optional

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject


class Signature(ZscalerObject):
    """A class for Custom App Signature objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.type = config["type"] if "type" in config else None
            self.match_level = config["matchLevel"] if "matchLevel" in config else None
            self.value = config["value"] if "value" in config else None
        else:
            self.type = None
            self.match_level = None
            self.value = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "type": self.type,
            "matchLevel": self.match_level,
            "value": self.value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CustomApp(ZscalerObject):
    """A class for Custom Application objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.associated_app_name = config["associatedAppName"] if "associatedAppName" in config else None
            self.associated_app_category = config["associatedAppCategory"] if "associatedAppCategory" in config else None
            self.description = config["description"] if "description" in config else None
            self.signatures = ZscalerCollection.form_list(
                config["signatures"] if "signatures" in config else [],
                Signature,
            )
        else:
            self.id = None
            self.name = None
            self.associated_app_name = None
            self.associated_app_category = None
            self.description = None
            self.signatures = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "associatedAppName": self.associated_app_name,
            "associatedAppCategory": self.associated_app_category,
            "description": self.description,
            "signatures": [s.request_format() if hasattr(s, "request_format") else s for s in (self.signatures or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
