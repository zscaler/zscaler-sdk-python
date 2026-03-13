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

from typing import Any, Dict, List, Optional
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class TemplateRouter(ZscalerObject):
    """
    A class for individual ZTB Template Router objects (single item).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.connect_to_hub = config["connectToHub"] if "connectToHub" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None
            self.deployment_type = config["deploymentType"] if "deploymentType" in config else None
            self.dhcp_service = config["dhcpService"] if "dhcpService" in config else None
            self.id = config["id"] if "id" in config else None
            self.is_default = config["isDefault"] if "isDefault" in config else None
            self.name = config["name"] if "name" in config else None
            self.nat_enabled = config["natEnabled"] if "natEnabled" in config else None
            self.permissions = config["permissions"] if "permissions" in config else None
            self.platform_type = config["platformType"] if "platformType" in config else None
            self.private_dns = config["privateDns"] if "privateDns" in config else None
            self.sites_count = config["sitesCount"] if "sitesCount" in config else 0
            self.updated_at = config["updatedAt"] if "updatedAt" in config else None
        else:
            self.connect_to_hub = None
            self.created_at = None
            self.deployment_type = None
            self.dhcp_service = None
            self.id = None
            self.is_default = None
            self.name = None
            self.nat_enabled = None
            self.permissions = None
            self.platform_type = None
            self.private_dns = None
            self.sites_count = 0
            self.updated_at = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "connectToHub": self.connect_to_hub,
            "createdAt": self.created_at,
            "deploymentType": self.deployment_type,
            "dhcpService": self.dhcp_service,
            "id": self.id,
            "isDefault": self.is_default,
            "name": self.name,
            "natEnabled": self.nat_enabled,
            "permissions": self.permissions,
            "platformType": self.platform_type,
            "privateDns": self.private_dns,
            "sitesCount": self.sites_count,
            "updatedAt": self.updated_at,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TemplateRouterResult(ZscalerObject):
    """
    A class for the list response envelope.

    GET response shape::

        {
            "cluster_token": "string",
            "count": 0,
            "result": [...],
            "token": "string"
        }
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.cluster_token = config["clusterToken"] if "clusterToken" in config else None
            self.count = config["count"] if "count" in config else 0
            self.token = config["token"] if "token" in config else None
            self.result = ZscalerCollection.form_list(config["result"] if "result" in config else [], TemplateRouter)
        else:
            self.cluster_token = None
            self.count = 0
            self.token = None
            self.result = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "clusterToken": self.cluster_token,
            "count": self.count,
            "token": self.token,
            "result": [item.request_format() for item in (self.result or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
