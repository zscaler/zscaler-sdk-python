# flake8: noqa
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

from typing import Any, Dict, Optional
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class AppConnectorConfig(ZscalerObject):
    """
    A class for individual ZTB App Connector Config objects (single item).

    Used for each item in the list response and for single-object get/create.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.app_connector_id = config["appConnectorId"] if "appConnectorId" in config else None
            self.cluster_id = config["clusterId"] if "clusterId" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None
            self.name = config["name"] if "name" in config else None
            self.provision_key = config["provisionKey"] if "provisionKey" in config else None
            self.status = config["status"] if "status" in config else None
            self.updated_at = config["updatedAt"] if "updatedAt" in config else None
        else:
            self.app_connector_id = None
            self.cluster_id = None
            self.created_at = None
            self.name = None
            self.provision_key = None
            self.status = None
            self.updated_at = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "appConnectorId": self.app_connector_id,
            "clusterId": self.cluster_id,
            "createdAt": self.created_at,
            "name": self.name,
            "provisionKey": self.provision_key,
            "status": self.status,
            "updatedAt": self.updated_at,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppConnectorConfigResult(ZscalerObject):
    """
    A class for the list response envelope with cluster_id and result array.

    GET response shape::

        {
            "cluster_id": "string",
            "result": [
                {
                    "app_connector_id": 0,
                    "cluster_id": 0,
                    "created_at": "2026-02-27T04:17:04.646Z",
                    "name": "string",
                    "provision_key": "string",
                    "status": "string",
                    "updated_at": "2026-02-27T04:17:04.646Z"
                }
            ]
        }
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.cluster_id = config["clusterId"] if "clusterId" in config else None
            self.result = ZscalerCollection.form_list(config["result"] if "result" in config else [], AppConnectorConfig)
        else:
            self.cluster_id = None
            self.result = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "clusterId": self.cluster_id,
            "result": [item.request_format() for item in (self.result or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
