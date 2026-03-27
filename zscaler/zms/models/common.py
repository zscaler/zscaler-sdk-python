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

from typing import Dict, Any, List, Optional
from zscaler.oneapi_object import ZscalerObject


class PageInfo(ZscalerObject):
    """
    Pagination metadata for GraphQL Connection types.

    Attributes:
        page_number: Current page number.
        page_size: Number of items per page.
        total_count: Total number of items.
        total_pages: Total number of pages.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.page_number: Optional[int] = config.get("pageNumber")
            self.page_size: Optional[int] = config.get("pageSize")
            self.total_count: Optional[int] = config.get("totalCount")
            self.total_pages: Optional[int] = config.get("totalPages")
        else:
            self.page_number = None
            self.page_size = None
            self.total_count = None
            self.total_pages = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "pageNumber": self.page_number,
            "pageSize": self.page_size,
            "totalCount": self.total_count,
            "totalPages": self.total_pages,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AgentEntry(ZscalerObject):
    """
    An agent entry from the ZMS agents query.

    Attributes:
        name: The agent name.
        eyez_id: The agent eyez ID.
        connection_status: The agent connection status.
        agent_type: The agent type.
        host_os: The host operating system.
        current_software_version: Current software version.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.name: Optional[str] = config.get("name")
            self.eyez_id: Optional[str] = config.get("eyezId")
            self.connection_status: Optional[str] = config.get("connectionStatus")
            self.agent_type: Optional[str] = config.get("agentType")
            self.host_os: Optional[str] = config.get("hostOs")
            self.current_software_version: Optional[str] = config.get("currentSoftwareVersion")
            self.upgrade_status: Optional[str] = config.get("upgradeStatus")
            self.description: Optional[str] = config.get("description")
            self.cloud_provider: Optional[str] = config.get("cloudProvider")
            self.public_ip: Optional[str] = config.get("publicIp")
            self.private_ips: Optional[List[str]] = config.get("privateIps")
        else:
            self.name = None
            self.eyez_id = None
            self.connection_status = None
            self.agent_type = None
            self.host_os = None
            self.current_software_version = None
            self.upgrade_status = None
            self.description = None
            self.cloud_provider = None
            self.public_ip = None
            self.private_ips = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "eyezId": self.eyez_id,
            "connectionStatus": self.connection_status,
            "agentType": self.agent_type,
            "hostOs": self.host_os,
            "currentSoftwareVersion": self.current_software_version,
            "upgradeStatus": self.upgrade_status,
            "description": self.description,
            "cloudProvider": self.cloud_provider,
            "publicIp": self.public_ip,
            "privateIps": self.private_ips,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AgentGroupEntry(ZscalerObject):
    """
    An agent group entry from the ZMS agentGroups query.

    Attributes:
        name: The agent group name.
        eyez_id: The agent group eyez ID.
        agent_group_type: The agent group type (K8S, VM).
        cloud_provider: The cloud provider.
        admin_status: The admin status.
        agent_count: Number of agents in the group.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.name: Optional[str] = config.get("name")
            self.eyez_id: Optional[str] = config.get("eyezId")
            self.agent_group_type: Optional[str] = config.get("agentGroupType")
            self.cloud_provider: Optional[str] = config.get("cloudProvider")
            self.admin_status: Optional[str] = config.get("adminStatus")
            self.agent_count: Optional[int] = config.get("agentCount")
            self.description: Optional[str] = config.get("description")
            self.policy_status: Optional[str] = config.get("policyStatus")
            self.upgrade_status: Optional[str] = config.get("upgradeStatus")
            self.tamper_protection_status: Optional[str] = config.get("tamperProtectionStatus")
        else:
            self.name = None
            self.eyez_id = None
            self.agent_group_type = None
            self.cloud_provider = None
            self.admin_status = None
            self.agent_count = None
            self.description = None
            self.policy_status = None
            self.upgrade_status = None
            self.tamper_protection_status = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "eyezId": self.eyez_id,
            "agentGroupType": self.agent_group_type,
            "cloudProvider": self.cloud_provider,
            "adminStatus": self.admin_status,
            "agentCount": self.agent_count,
            "description": self.description,
            "policyStatus": self.policy_status,
            "upgradeStatus": self.upgrade_status,
            "tamperProtectionStatus": self.tamper_protection_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ResourceEntry(ZscalerObject):
    """
    A resource entry from the ZMS resources query.

    Attributes:
        id: The resource ID.
        name: The resource name.
        resource_type: The resource type (VM, NODE, POD, etc.).
        status: The resource status.
        cloud_provider: The cloud provider.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id: Optional[str] = config.get("id")
            self.name: Optional[str] = config.get("name")
            self.resource_type: Optional[str] = config.get("resourceType")
            self.status: Optional[str] = config.get("status")
            self.cloud_provider: Optional[str] = config.get("cloudProvider")
            self.cloud_region: Optional[str] = config.get("cloudRegion")
            self.resource_hostname: Optional[str] = config.get("resourceHostname")
            self.platform_os: Optional[str] = config.get("platformOs")
            self.local_ips: Optional[List[str]] = config.get("localIps")
            self.deleted: Optional[bool] = config.get("deleted")
        else:
            self.id = None
            self.name = None
            self.resource_type = None
            self.status = None
            self.cloud_provider = None
            self.cloud_region = None
            self.resource_hostname = None
            self.platform_os = None
            self.local_ips = None
            self.deleted = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "resourceType": self.resource_type,
            "status": self.status,
            "cloudProvider": self.cloud_provider,
            "cloudRegion": self.cloud_region,
            "resourceHostname": self.resource_hostname,
            "platformOs": self.platform_os,
            "localIps": self.local_ips,
            "deleted": self.deleted,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PolicyRuleEntry(ZscalerObject):
    """
    A policy rule entry from the ZMS policyRules query.

    Attributes:
        id: The policy rule ID.
        name: The policy rule name.
        action: The policy action (ALLOW, BLOCK, SIM_BLOCK).
        priority: The rule priority.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id: Optional[str] = config.get("id")
            self.name: Optional[str] = config.get("name")
            self.action: Optional[str] = config.get("action")
            self.priority: Optional[int] = config.get("priority")
            self.description: Optional[str] = config.get("description")
            self.deleted: Optional[bool] = config.get("deleted")
            self.source_target_type: Optional[str] = config.get("sourceTargetType")
            self.destination_target_type: Optional[str] = config.get("destinationTargetType")
        else:
            self.id = None
            self.name = None
            self.action = None
            self.priority = None
            self.description = None
            self.deleted = None
            self.source_target_type = None
            self.destination_target_type = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "action": self.action,
            "priority": self.priority,
            "description": self.description,
            "deleted": self.deleted,
            "sourceTargetType": self.source_target_type,
            "destinationTargetType": self.destination_target_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppZoneEntry(ZscalerObject):
    """
    An app zone entry from the ZMS appZones query.

    Attributes:
        id: The app zone ID.
        app_zone_name: The app zone name.
        description: The app zone description.
        member_count: Number of resources in the app zone.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id: Optional[str] = config.get("id")
            self.app_zone_name: Optional[str] = config.get("appZoneName")
            self.description: Optional[str] = config.get("description")
            self.member_count: Optional[int] = config.get("memberCount")
            self.include_all_vpcs: Optional[bool] = config.get("includeAllVpcs")
            self.include_all_subnets: Optional[bool] = config.get("includeAllSubnets")
        else:
            self.id = None
            self.app_zone_name = None
            self.description = None
            self.member_count = None
            self.include_all_vpcs = None
            self.include_all_subnets = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "appZoneName": self.app_zone_name,
            "description": self.description,
            "memberCount": self.member_count,
            "includeAllVpcs": self.include_all_vpcs,
            "includeAllSubnets": self.include_all_subnets,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppCatalogEntry(ZscalerObject):
    """
    An app catalog entry from the ZMS appCatalog query.

    Attributes:
        id: The app catalog ID.
        name: The application name.
        category: The application category.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id: Optional[str] = config.get("id")
            self.name: Optional[str] = config.get("name")
            self.category: Optional[str] = config.get("category")
        else:
            self.id = None
            self.name = None
            self.category = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "category": self.category,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TagNamespaceEntry(ZscalerObject):
    """
    A tag namespace entry from the ZMS tagNamespaces query.

    Attributes:
        id: The namespace ID.
        name: The namespace name.
        description: The namespace description.
        origin: The namespace origin (CUSTOM, EXTERNAL, ML).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id: Optional[str] = config.get("id")
            self.name: Optional[str] = config.get("name")
            self.description: Optional[str] = config.get("description")
            self.origin: Optional[str] = config.get("origin")
        else:
            self.id = None
            self.name = None
            self.description = None
            self.origin = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "origin": self.origin,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NonceEntry(ZscalerObject):
    """
    A nonce (provisioning key) entry from the ZMS nonces query.

    Attributes:
        eyez_id: The nonce eyez ID.
        name: The nonce name.
        key: The nonce key value.
        max_usage: Maximum usage count.
        usage_count: Current usage count.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.eyez_id: Optional[str] = config.get("eyezId")
            self.name: Optional[str] = config.get("name")
            self.key: Optional[str] = config.get("key")
            self.max_usage: Optional[int] = config.get("maxUsage")
            self.usage_count: Optional[int] = config.get("usageCount")
            self.agent_group_eyez_id: Optional[str] = config.get("agentGroupEyezId")
            self.agent_group_name: Optional[str] = config.get("agentGroupName")
            self.agent_group_type: Optional[str] = config.get("agentGroupType")
            self.product: Optional[str] = config.get("product")
        else:
            self.eyez_id = None
            self.name = None
            self.key = None
            self.max_usage = None
            self.usage_count = None
            self.agent_group_eyez_id = None
            self.agent_group_name = None
            self.agent_group_type = None
            self.product = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "eyezId": self.eyez_id,
            "name": self.name,
            "key": self.key,
            "maxUsage": self.max_usage,
            "usageCount": self.usage_count,
            "agentGroupEyezId": self.agent_group_eyez_id,
            "agentGroupName": self.agent_group_name,
            "agentGroupType": self.agent_group_type,
            "product": self.product,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


__all__ = [
    "PageInfo",
    "AgentEntry",
    "AgentGroupEntry",
    "ResourceEntry",
    "PolicyRuleEntry",
    "AppZoneEntry",
    "AppCatalogEntry",
    "TagNamespaceEntry",
    "NonceEntry",
]
