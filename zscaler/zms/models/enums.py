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

from enum import Enum


class AgentAdminStatus(str, Enum):
    """Agent admin status enum."""

    DISABLED = "DISABLED"
    DISABLED_INHERITED = "DISABLED_INHERITED"
    ENABLED = "ENABLED"
    ENABLED_INHERITED = "ENABLED_INHERITED"
    INHERITED = "INHERITED"


class AgentAutoUpgrade(str, Enum):
    """Agent auto upgrade enum."""

    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class AgentConnectionStatus(str, Enum):
    """Agent connection status enum."""

    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


class AgentGroupAdminStatus(str, Enum):
    """Agent group admin status enum."""

    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class AgentGroupType(str, Enum):
    """Agent group type enum."""

    K8S = "K8S"
    UNKNOWN = "UNKNOWN"
    VM = "VM"


class AgentManagerStatus(str, Enum):
    """Agent manager status enum."""

    CONTINUE_PENDING = "CONTINUE_PENDING"
    PAUSED = "PAUSED"
    PAUSE_PENDING = "PAUSE_PENDING"
    RUNNING = "RUNNING"
    START_PENDING = "START_PENDING"
    STOPPED = "STOPPED"
    STOP_PENDING = "STOP_PENDING"
    UNKNOWN = "UNKNOWN"
    UNRECOGNIZED = "UNRECOGNIZED"


class AgentPolicyStatus(str, Enum):
    """Agent policy status enum."""

    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class AgentType(str, Enum):
    """Agent type enum."""

    CLUSTER = "CLUSTER"
    HOST = "HOST"
    KUBE_CONNECTOR = "KUBE_CONNECTOR"
    UNKNOWN = "UNKNOWN"


class AppZoneMappingState(str, Enum):
    """App zone mapping state enum."""

    CONFLICTING = "CONFLICTING"
    MAPPED = "MAPPED"
    UNMAPPED = "UNMAPPED"


class CloudProvider(str, Enum):
    """Cloud provider enum."""

    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"
    ON_PREMISES = "ON_PREMISES"


class ComponentGroupUpgradeFailureStrategy(str, Enum):
    """Component group upgrade failure strategy enum."""

    HALT = "HALT"
    SKIP = "SKIP"


class ComponentUpgradeSequence(str, Enum):
    """Component upgrade sequence enum."""

    PARALLEL = "PARALLEL"
    SERIAL = "SERIAL"


class ComponentUpgradeStatus(str, Enum):
    """Component upgrade status enum."""

    COMPLETED_WITH_FAILURES = "COMPLETED_WITH_FAILURES"
    FAILED = "FAILED"
    FORCED_UPGRADE = "FORCED_UPGRADE"
    IN_PROGRESS = "IN_PROGRESS"
    UP_TO_DATE = "UP_TO_DATE"


class DefaultPolicyRuleAction(str, Enum):
    """Default policy rule action enum."""

    ALLOW = "ALLOW"
    BLOCK = "BLOCK"


class DefaultPolicyRuleDirection(str, Enum):
    """Default policy rule direction enum."""

    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"


class DefaultPolicyRuleScopeType(str, Enum):
    """Default policy rule scope type enum."""

    CUSTOMER = "CUSTOMER"


class NamespaceOrigin(str, Enum):
    """Namespace origin enum."""

    CUSTOM = "CUSTOM"
    EXTERNAL = "EXTERNAL"
    ML = "ML"
    UNKNOWN = "UNKNOWN"


class NetworkProtocol(str, Enum):
    """Network protocol enum."""

    TCP = "TCP"
    UDP = "UDP"


class NonceProduct(str, Enum):
    """Nonce product types."""

    EYEZ = "EYEZ"
    EYEZ_LEGACY = "EYEZ_LEGACY"


class PodPhase(str, Enum):
    """Pod phase enum."""

    FAILED = "FAILED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    UNKNOWN = "UNKNOWN"


class PolicyAction(str, Enum):
    """Policy action enum."""

    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    SIM_BLOCK = "SIM_BLOCK"


class PolicyRuleAppZoneScopeType(str, Enum):
    """Policy rule app zone scope type enum."""

    ANY = "ANY"
    APP_ZONE = "APP_ZONE"


class PolicyRuleTargetType(str, Enum):
    """Policy rule target type enum."""

    ANY = "ANY"
    RESOURCE_GROUP = "RESOURCE_GROUP"


class RecommendedResourceGroupUserActionType(str, Enum):
    """Recommended resource group user action type enum."""

    ACCEPTED = "ACCEPTED"
    CREATED = "CREATED"
    EDITED = "EDITED"
    IGNORED = "IGNORED"
    MERGED = "MERGED"


class RecommendedTagUserActionType(str, Enum):
    """Recommended tag user action type enum."""

    ACCEPTED = "ACCEPTED"
    ACCEPT_IGNORED = "ACCEPT_IGNORED"
    CREATED = "CREATED"
    IGNORED = "IGNORED"


class ResourceGroupOrigin(str, Enum):
    """Resource group origin enum."""

    ML_RECOMMENDED = "ML_RECOMMENDED"
    USER_DEFINED = "USER_DEFINED"


class ResourceGroupType(str, Enum):
    """Resource group type enum."""

    MANAGED = "MANAGED"
    UNMANAGED = "UNMANAGED"


class ResourceStatus(str, Enum):
    """Resource status enum."""

    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    INACTIVE = "INACTIVE"


class ResourceType(str, Enum):
    """Resource type enum."""

    K8S_NODE = "K8S_NODE"
    K8S_SERVICE = "K8S_SERVICE"
    K8S_WORKLOAD = "K8S_WORKLOAD"
    NODE = "NODE"
    POD = "POD"
    UNKNOWN = "UNKNOWN"
    VM = "VM"


class SortDirection(str, Enum):
    """Sort direction enum."""

    ASC = "ASC"
    DESC = "DESC"


class TagAssignmentUserAction(str, Enum):
    """Tag assignment user action enum."""

    ASSIGN = "ASSIGN"
    UNASSIGN = "UNASSIGN"


class TagScope(str, Enum):
    """Tag scope enum."""

    HOST = "HOST"
    K8S_POD_TEMPLATE = "K8S_POD_TEMPLATE"
    K8S_SERVICE = "K8S_SERVICE"
    K8S_WORKLOAD = "K8S_WORKLOAD"
    POD = "POD"


class TamperProtectionStatus(str, Enum):
    """Tamper protection status enum."""

    DISABLED = "DISABLED"
    DISABLED_INHERITED = "DISABLED_INHERITED"
    ENABLED = "ENABLED"
    ENABLED_INHERITED = "ENABLED_INHERITED"
    INHERITED = "INHERITED"


class MLRunStatus(str, Enum):
    """ML run status enum."""

    FAILED = "FAILED"
    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"
    SUCCESS = "SUCCESS"


class MLRunType(str, Enum):
    """ML run type enum."""

    RESOURCE_GROUP = "RESOURCE_GROUP"
    TAG = "TAG"


__all__ = [
    "AgentAdminStatus",
    "AgentAutoUpgrade",
    "AgentConnectionStatus",
    "AgentGroupAdminStatus",
    "AgentGroupType",
    "AgentManagerStatus",
    "AgentPolicyStatus",
    "AgentType",
    "AppZoneMappingState",
    "CloudProvider",
    "ComponentGroupUpgradeFailureStrategy",
    "ComponentUpgradeSequence",
    "ComponentUpgradeStatus",
    "DefaultPolicyRuleAction",
    "DefaultPolicyRuleDirection",
    "DefaultPolicyRuleScopeType",
    "MLRunStatus",
    "MLRunType",
    "NamespaceOrigin",
    "NetworkProtocol",
    "NonceProduct",
    "PodPhase",
    "PolicyAction",
    "PolicyRuleAppZoneScopeType",
    "PolicyRuleTargetType",
    "RecommendedResourceGroupUserActionType",
    "RecommendedTagUserActionType",
    "ResourceGroupOrigin",
    "ResourceGroupType",
    "ResourceStatus",
    "ResourceType",
    "SortDirection",
    "TagAssignmentUserAction",
    "TagScope",
    "TamperProtectionStatus",
]
