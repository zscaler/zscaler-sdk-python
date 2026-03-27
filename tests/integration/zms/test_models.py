# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import pytest

from zscaler.zms.models.enums import (
    AgentAdminStatus,
    AgentType,
    CloudProvider,
    PolicyAction,
    ResourceType,
    SortDirection,
)
from zscaler.zms.models.inputs import (
    StringExpression,
    IntegerExpression,
    ResourceQueryFilter,
    PolicyRuleFilter,
    AppZoneFilter,
    NamespaceFilter,
)
from zscaler.zms.models.common import (
    AgentEntry,
    AgentGroupEntry,
    ResourceEntry,
    PolicyRuleEntry,
    AppZoneEntry,
    PageInfo,
)


@pytest.fixture
def fs():
    yield


class TestEnums:
    """Test ZMS enum types."""

    def test_agent_admin_status_values(self, fs):
        assert AgentAdminStatus.ENABLED.value == "ENABLED"
        assert AgentAdminStatus.DISABLED.value == "DISABLED"

    def test_agent_type_values(self, fs):
        assert AgentType.HOST.value == "HOST"
        assert AgentType.CLUSTER.value == "CLUSTER"
        assert AgentType.KUBE_CONNECTOR.value == "KUBE_CONNECTOR"

    def test_cloud_provider_values(self, fs):
        assert CloudProvider.AWS.value == "AWS"
        assert CloudProvider.AZURE.value == "AZURE"
        assert CloudProvider.GCP.value == "GCP"
        assert CloudProvider.ON_PREMISES.value == "ON_PREMISES"

    def test_policy_action_values(self, fs):
        assert PolicyAction.ALLOW.value == "ALLOW"
        assert PolicyAction.BLOCK.value == "BLOCK"
        assert PolicyAction.SIM_BLOCK.value == "SIM_BLOCK"

    def test_resource_type_values(self, fs):
        assert ResourceType.VM.value == "VM"
        assert ResourceType.NODE.value == "NODE"
        assert ResourceType.POD.value == "POD"

    def test_sort_direction_values(self, fs):
        assert SortDirection.ASC.value == "ASC"
        assert SortDirection.DESC.value == "DESC"


class TestInputs:
    """Test ZMS input types."""

    def test_string_expression_equals(self, fs):
        expr = StringExpression(equals="test")
        result = expr.as_dict()
        assert result == {"equals": "test"}

    def test_string_expression_contains(self, fs):
        expr = StringExpression(contains="test")
        result = expr.as_dict()
        assert result == {"contains": "test"}

    def test_string_expression_in_list(self, fs):
        expr = StringExpression(in_list=["a", "b"])
        result = expr.as_dict()
        assert result == {"in": ["a", "b"]}

    def test_string_expression_empty(self, fs):
        expr = StringExpression()
        result = expr.as_dict()
        assert result is None

    def test_integer_expression(self, fs):
        expr = IntegerExpression(eq=5, gt=3)
        result = expr.as_dict()
        assert result == {"eq": 5, "gt": 3}

    def test_resource_query_filter(self, fs):
        f = ResourceQueryFilter(name=StringExpression(contains="test"))
        result = f.as_dict()
        assert result == {"name": {"contains": "test"}}

    def test_policy_rule_filter(self, fs):
        f = PolicyRuleFilter(name=StringExpression(equals="rule-1"))
        result = f.as_dict()
        assert result == {"name": {"equals": "rule-1"}}

    def test_app_zone_filter(self, fs):
        f = AppZoneFilter(app_zone_name=StringExpression(contains="zone"))
        result = f.as_dict()
        assert result == {"appZoneName": {"contains": "zone"}}

    def test_namespace_filter(self, fs):
        f = NamespaceFilter(name=StringExpression(equals="custom-ns"))
        result = f.as_dict()
        assert result == {"name": {"equals": "custom-ns"}}


class TestCommonModels:
    """Test ZMS common model classes."""

    def test_agent_entry(self, fs):
        config = {"name": "agent-1", "eyezId": "abc", "connectionStatus": "CONNECTED"}
        entry = AgentEntry(config)
        assert entry.name == "agent-1"
        assert entry.eyez_id == "abc"
        assert entry.connection_status == "CONNECTED"
        req = entry.request_format()
        assert req["name"] == "agent-1"
        assert req["eyezId"] == "abc"

    def test_agent_entry_empty(self, fs):
        entry = AgentEntry()
        assert entry.name is None
        assert entry.eyez_id is None

    def test_agent_group_entry(self, fs):
        config = {"name": "group-1", "eyezId": "def", "agentGroupType": "VM"}
        entry = AgentGroupEntry(config)
        assert entry.name == "group-1"
        assert entry.agent_group_type == "VM"

    def test_resource_entry(self, fs):
        config = {"id": "r-1", "name": "resource-1", "resourceType": "VM", "status": "ACTIVE"}
        entry = ResourceEntry(config)
        assert entry.id == "r-1"
        assert entry.resource_type == "VM"
        assert entry.status == "ACTIVE"

    def test_policy_rule_entry(self, fs):
        config = {"id": "pr-1", "name": "rule-1", "action": "ALLOW", "priority": 1}
        entry = PolicyRuleEntry(config)
        assert entry.id == "pr-1"
        assert entry.action == "ALLOW"
        assert entry.priority == 1

    def test_app_zone_entry(self, fs):
        config = {"id": "az-1", "appZoneName": "zone-1", "memberCount": 5}
        entry = AppZoneEntry(config)
        assert entry.id == "az-1"
        assert entry.app_zone_name == "zone-1"
        assert entry.member_count == 5

    def test_page_info(self, fs):
        config = {"pageNumber": 1, "pageSize": 20, "totalCount": 100, "totalPages": 5}
        page = PageInfo(config)
        assert page.page_number == 1
        assert page.total_count == 100
        assert page.total_pages == 5
