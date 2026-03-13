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


class APIKeyAuthRouter(ZscalerObject):
    """
    A class for individual ZTB API Key objects returned by the list endpoint.

    Swagger response shape for ``GET /api/v3/api-key-auth/list``::

        {
            "count": 0,
            "rows": [
                {
                    "created_at": "string",
                    "id": "string",
                    "name": "string"
                }
            ]
        }
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None
        else:
            self.id = None
            self.name = None
            self.created_at = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "createdAt": self.created_at,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class APIKeyCreateResponse(ZscalerObject):
    """
    A class for the response returned by ``POST /api/v3/api-key-auth/create``.

    Swagger response shape::

        {
            "key": "string"
        }
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.key = config["key"] if "key" in config else None
        else:
            self.key = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "key": self.key,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
