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
from unittest.mock import Mock


@pytest.fixture
def fs():
    yield


class TestAgentsUnit:
    """
    Unit Tests for the ZMS Agents API.
    """

    def test_list_agents_request_error(self, fs):
        """Test list_agents handles request creation errors correctly"""
        from zscaler.zms.agents import AgentsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        agents_api = AgentsAPI(mock_executor)
        result, response, err = agents_api.list_agents(customer_id="123")

        assert result is None
        assert err is not None

    def test_list_agents_execute_error(self, fs):
        """Test list_agents handles execution errors correctly"""
        from zscaler.zms.agents import AgentsAPI

        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))

        agents_api = AgentsAPI(mock_executor)
        result, response, err = agents_api.list_agents(customer_id="123")

        assert result is None
        assert err is not None

    def test_list_agents_graphql_error(self, fs):
        """Test list_agents handles GraphQL errors returned by the centralized error handler"""
        from zscaler.zms.agents import AgentsAPI
        from zscaler.errors.graphql_error import GraphQLAPIError

        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))

        graphql_error = GraphQLAPIError(
            url="/zms/graphql",
            response_details=Mock(status_code=200, headers={}),
            response_body={"errors": [{"message": "GraphQL error"}]},
            service_type="zms",
        )
        mock_executor.execute = Mock(return_value=(None, graphql_error))

        agents_api = AgentsAPI(mock_executor)
        result, response, err = agents_api.list_agents(customer_id="123")

        assert result is None
        assert err is not None
        assert isinstance(err, GraphQLAPIError)

    def test_list_agents_success(self, fs):
        """Test list_agents returns data on success"""
        from zscaler.zms.agents import AgentsAPI

        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))

        mock_response = Mock()
        mock_response.get_body = Mock(
            return_value={
                "data": {
                    "agents": {
                        "nodes": [{"name": "test-agent", "eyezId": "abc-123"}],
                        "pageInfo": {"pageNumber": 1, "pageSize": 20, "totalCount": 1, "totalPages": 1},
                    }
                }
            }
        )
        mock_executor.execute = Mock(return_value=(mock_response, None))

        agents_api = AgentsAPI(mock_executor)
        result, response, err = agents_api.list_agents(customer_id="123")

        assert err is None
        assert result is not None
        assert len(result.get("nodes", [])) == 1
        assert result["nodes"][0]["name"] == "test-agent"

    def test_get_agent_connection_status_statistics_request_error(self, fs):
        """Test get_agent_connection_status_statistics handles request errors"""
        from zscaler.zms.agents import AgentsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        agents_api = AgentsAPI(mock_executor)
        result, response, err = agents_api.get_agent_connection_status_statistics(customer_id="123")

        assert result is None
        assert err is not None

    def test_get_agent_version_statistics_request_error(self, fs):
        """Test get_agent_version_statistics handles request errors"""
        from zscaler.zms.agents import AgentsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        agents_api = AgentsAPI(mock_executor)
        result, response, err = agents_api.get_agent_version_statistics(customer_id="123")

        assert result is None
        assert err is not None


class TestAgentGroupsUnit:
    """
    Unit Tests for the ZMS Agent Groups API.
    """

    def test_list_agent_groups_request_error(self, fs):
        """Test list_agent_groups handles request creation errors"""
        from zscaler.zms.agent_groups import AgentGroupsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = AgentGroupsAPI(mock_executor)
        result, response, err = api.list_agent_groups(customer_id="123")

        assert result is None
        assert err is not None

    def test_list_agent_groups_execute_error(self, fs):
        """Test list_agent_groups handles execution errors"""
        from zscaler.zms.agent_groups import AgentGroupsAPI

        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))

        api = AgentGroupsAPI(mock_executor)
        result, response, err = api.list_agent_groups(customer_id="123")

        assert result is None
        assert err is not None


class TestResourcesUnit:
    """
    Unit Tests for the ZMS Resources API.
    """

    def test_list_resources_request_error(self, fs):
        """Test list_resources handles request creation errors"""
        from zscaler.zms.resources import ResourcesAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = ResourcesAPI(mock_executor)
        result, response, err = api.list_resources(customer_id="123")

        assert result is None
        assert err is not None

    def test_list_resources_execute_error(self, fs):
        """Test list_resources handles execution errors"""
        from zscaler.zms.resources import ResourcesAPI

        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))

        api = ResourcesAPI(mock_executor)
        result, response, err = api.list_resources(customer_id="123")

        assert result is None
        assert err is not None

    def test_get_resource_protection_status_request_error(self, fs):
        """Test get_resource_protection_status handles request errors"""
        from zscaler.zms.resources import ResourcesAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = ResourcesAPI(mock_executor)
        result, response, err = api.get_resource_protection_status(customer_id="123")

        assert result is None
        assert err is not None


class TestPolicyRulesUnit:
    """
    Unit Tests for the ZMS Policy Rules API.
    """

    def test_list_policy_rules_request_error(self, fs):
        """Test list_policy_rules handles request creation errors"""
        from zscaler.zms.policy_rules import PolicyRulesAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = PolicyRulesAPI(mock_executor)
        result, response, err = api.list_policy_rules(customer_id="123")

        assert result is None
        assert err is not None

    def test_list_default_policy_rules_request_error(self, fs):
        """Test list_default_policy_rules handles request errors"""
        from zscaler.zms.policy_rules import PolicyRulesAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = PolicyRulesAPI(mock_executor)
        result, response, err = api.list_default_policy_rules(customer_id="123")

        assert result is None
        assert err is not None


class TestAppZonesUnit:
    """
    Unit Tests for the ZMS App Zones API.
    """

    def test_list_app_zones_request_error(self, fs):
        """Test list_app_zones handles request creation errors"""
        from zscaler.zms.app_zones import AppZonesAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = AppZonesAPI(mock_executor)
        result, response, err = api.list_app_zones(customer_id="123")

        assert result is None
        assert err is not None


class TestAppCatalogUnit:
    """
    Unit Tests for the ZMS App Catalog API.
    """

    def test_list_app_catalog_request_error(self, fs):
        """Test list_app_catalog handles request creation errors"""
        from zscaler.zms.app_catalog import AppCatalogAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = AppCatalogAPI(mock_executor)
        result, response, err = api.list_app_catalog(customer_id="123")

        assert result is None
        assert err is not None


class TestTagsUnit:
    """
    Unit Tests for the ZMS Tags API.
    """

    def test_list_tag_namespaces_request_error(self, fs):
        """Test list_tag_namespaces handles request creation errors"""
        from zscaler.zms.tags import TagsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = TagsAPI(mock_executor)
        result, response, err = api.list_tag_namespaces(customer_id="123")

        assert result is None
        assert err is not None

    def test_list_tag_keys_request_error(self, fs):
        """Test list_tag_keys handles request creation errors"""
        from zscaler.zms.tags import TagsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = TagsAPI(mock_executor)
        result, response, err = api.list_tag_keys(customer_id="123", namespace_id="ns-1")

        assert result is None
        assert err is not None

    def test_list_tag_values_request_error(self, fs):
        """Test list_tag_values handles request creation errors"""
        from zscaler.zms.tags import TagsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = TagsAPI(mock_executor)
        result, response, err = api.list_tag_values(customer_id="123", tag_id="tag-1", namespace_origin="CUSTOM")

        assert result is None
        assert err is not None


class TestNoncesUnit:
    """
    Unit Tests for the ZMS Nonces API.
    """

    def test_list_nonces_request_error(self, fs):
        """Test list_nonces handles request creation errors"""
        from zscaler.zms.nonces import NoncesAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = NoncesAPI(mock_executor)
        result, response, err = api.list_nonces(customer_id="123")

        assert result is None
        assert err is not None

    def test_get_nonce_request_error(self, fs):
        """Test get_nonce handles request creation errors"""
        from zscaler.zms.nonces import NoncesAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = NoncesAPI(mock_executor)
        result, response, err = api.get_nonce(customer_id="123", eyez_id="nonce-1")

        assert result is None
        assert err is not None


class TestResourceGroupsUnit:
    """
    Unit Tests for the ZMS Resource Groups API.
    """

    def test_list_resource_groups_request_error(self, fs):
        """Test list_resource_groups handles request creation errors"""
        from zscaler.zms.resource_groups import ResourceGroupsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = ResourceGroupsAPI(mock_executor)
        result, response, err = api.list_resource_groups(customer_id="123")

        assert result is None
        assert err is not None

    def test_get_resource_group_members_request_error(self, fs):
        """Test get_resource_group_members handles request errors"""
        from zscaler.zms.resource_groups import ResourceGroupsAPI

        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))

        api = ResourceGroupsAPI(mock_executor)
        result, response, err = api.get_resource_group_members(customer_id="123", group_id="rg-1")

        assert result is None
        assert err is not None


class TestBodyParsingError:
    """
    Unit Tests for body parsing error handling.
    """

    def test_body_parsing_exception(self, fs):
        """Test that body parsing exceptions are handled correctly"""
        from zscaler.zms.agents import AgentsAPI

        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))

        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))

        agents_api = AgentsAPI(mock_executor)
        result, response, err = agents_api.list_agents(customer_id="123")

        assert result is None
        assert err is not None
