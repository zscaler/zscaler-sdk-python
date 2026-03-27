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

from zscaler.zms.zms_service import ZMSService
from zscaler.zms.agents import AgentsAPI
from zscaler.zms.agent_groups import AgentGroupsAPI
from zscaler.zms.nonces import NoncesAPI
from zscaler.zms.resources import ResourcesAPI
from zscaler.zms.resource_groups import ResourceGroupsAPI
from zscaler.zms.policy_rules import PolicyRulesAPI
from zscaler.zms.app_zones import AppZonesAPI
from zscaler.zms.app_catalog import AppCatalogAPI
from zscaler.zms.tags import TagsAPI


@pytest.fixture
def fs():
    yield


class TestZMSService:
    """
    Unit Tests for the ZMS Service container.
    """

    def test_service_has_agents(self, fs):
        """Test that ZMSService exposes agents property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.agents, AgentsAPI)

    def test_service_has_agent_groups(self, fs):
        """Test that ZMSService exposes agent_groups property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.agent_groups, AgentGroupsAPI)

    def test_service_has_nonces(self, fs):
        """Test that ZMSService exposes nonces property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.nonces, NoncesAPI)

    def test_service_has_resources(self, fs):
        """Test that ZMSService exposes resources property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.resources, ResourcesAPI)

    def test_service_has_resource_groups(self, fs):
        """Test that ZMSService exposes resource_groups property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.resource_groups, ResourceGroupsAPI)

    def test_service_has_policy_rules(self, fs):
        """Test that ZMSService exposes policy_rules property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.policy_rules, PolicyRulesAPI)

    def test_service_has_app_zones(self, fs):
        """Test that ZMSService exposes app_zones property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.app_zones, AppZonesAPI)

    def test_service_has_app_catalog(self, fs):
        """Test that ZMSService exposes app_catalog property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.app_catalog, AppCatalogAPI)

    def test_service_has_tags(self, fs):
        """Test that ZMSService exposes tags property"""
        mock_executor = Mock()
        service = ZMSService(mock_executor)
        assert isinstance(service.tags, TagsAPI)
