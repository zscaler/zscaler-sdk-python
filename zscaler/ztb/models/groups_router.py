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


class GroupsRouter(ZscalerObject):
    """
    A class for individual ZTB Groups Router objects (single item).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            if "result" in config and isinstance(config["result"], dict):
                config = config["result"]
            self.autonomous = config["autonomous"] if "autonomous" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None
            self.display_name = config["displayName"] if "displayName" in config else None
            self.group_id = config["groupId"] if "groupId" in config else None
            self.has_groups = config["hasGroups"] if "hasGroups" in config else None
            self.hidden = config["hidden"] if "hidden" in config else None
            self.is_deleted = config["isDeleted"] if "isDeleted" in config else None
            self.member_attributes = config["memberAttributes"] if "memberAttributes" in config else None
            self.member_groups = config["memberGroups"] if "memberGroups" in config else None
            self.members = config["members"] if "members" in config else None
            self.members_count = config["membersCount"] if "membersCount" in config else 0
            self.name = config["name"] if "name" in config else None
            self.owner = config["owner"] if "owner" in config else None
            self.parent_groups = config["parentGroups"] if "parentGroups" in config else None
            self.permissions = config["permissions"] if "permissions" in config else None
            self.policy_count = config["policyCount"] if "policyCount" in config else 0
            self.policy_names = config["policyNames"] if "policyNames" in config else None
            self.shadow_grpid = config["shadowGrpid"] if "shadowGrpid" in config else None
            self.type = config["type"] if "type" in config else None
            self.updated_at = config["updatedAt"] if "updatedAt" in config else None
        else:
            self.autonomous = None
            self.created_at = None
            self.display_name = None
            self.group_id = None
            self.has_groups = None
            self.hidden = None
            self.is_deleted = None
            self.member_attributes = None
            self.member_groups = None
            self.members = None
            self.members_count = 0
            self.name = None
            self.owner = None
            self.parent_groups = None
            self.permissions = None
            self.policy_count = 0
            self.policy_names = None
            self.shadow_grpid = None
            self.type = None
            self.updated_at = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "autonomous": self.autonomous,
            "createdAt": self.created_at,
            "displayName": self.display_name,
            "groupId": self.group_id,
            "hasGroups": self.has_groups,
            "hidden": self.hidden,
            "isDeleted": self.is_deleted,
            "memberAttributes": self.member_attributes,
            "memberGroups": self.member_groups,
            "members": self.members,
            "membersCount": self.members_count,
            "name": self.name,
            "owner": self.owner,
            "parentGroups": self.parent_groups,
            "permissions": self.permissions,
            "policyCount": self.policy_count,
            "policyNames": self.policy_names,
            "shadowGrpid": self.shadow_grpid,
            "type": self.type,
            "updatedAt": self.updated_at,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GroupsRouterResult(ZscalerObject):
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
            self.result = ZscalerCollection.form_list(config["result"] if "result" in config else [], GroupsRouter)
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
