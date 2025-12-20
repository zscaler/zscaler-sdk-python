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
from unittest.mock import Mock, patch, MagicMock
import time


@pytest.fixture
def fs():
    yield


class TestShadowItUnit:
    """
    Unit Tests for the ZInsights Shadow IT API to increase coverage
    """

    def test_get_apps_request_error(self, fs):
        """Test get_apps handles request creation errors correctly"""
        from zscaler.zinsights.shadow_it import ShadowItAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        shadow_api = ShadowItAPI(mock_executor)
        result, response, err = shadow_api.get_apps(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_apps_execute_error(self, fs):
        """Test get_apps handles execution errors correctly"""
        from zscaler.zinsights.shadow_it import ShadowItAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        shadow_api = ShadowItAPI(mock_executor)
        result, response, err = shadow_api.get_apps(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_apps_graphql_error(self, fs):
        """Test get_apps handles GraphQL errors correctly"""
        from zscaler.zinsights.shadow_it import ShadowItAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response with GraphQL error
        mock_response = Mock()
        mock_response.get_body = Mock(return_value={
            "errors": [{"message": "GraphQL error"}]
        })
        mock_response._response = Mock()
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        shadow_api = ShadowItAPI(mock_executor)
        result, response, err = shadow_api.get_apps(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_shadow_it_summary_request_error(self, fs):
        """Test get_shadow_it_summary handles request creation errors correctly"""
        from zscaler.zinsights.shadow_it import ShadowItAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        shadow_api = ShadowItAPI(mock_executor)
        result, response, err = shadow_api.get_shadow_it_summary(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_shadow_it_summary_execute_error(self, fs):
        """Test get_shadow_it_summary handles execution errors correctly"""
        from zscaler.zinsights.shadow_it import ShadowItAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        shadow_api = ShadowItAPI(mock_executor)
        result, response, err = shadow_api.get_shadow_it_summary(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_shadow_it_summary_graphql_error(self, fs):
        """Test get_shadow_it_summary handles GraphQL errors correctly"""
        from zscaler.zinsights.shadow_it import ShadowItAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response with GraphQL error
        mock_response = Mock()
        mock_response.get_body = Mock(return_value={
            "errors": [{"message": "GraphQL error"}]
        })
        mock_response._response = Mock()
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        shadow_api = ShadowItAPI(mock_executor)
        result, response, err = shadow_api.get_shadow_it_summary(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_extract_graphql_response_exception(self, fs):
        """Test _extract_graphql_response handles exceptions correctly"""
        from zscaler.zinsights.shadow_it import ShadowItAPI
        
        mock_executor = Mock()
        shadow_api = ShadowItAPI(mock_executor)
        
        # Mock response that raises an exception
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        
        result, response, err = shadow_api._extract_graphql_response(
            mock_response, "http://test.com", "SHADOW_IT", "apps"
        )
        
        assert result is None
        assert err is not None


class TestIoTUnit:
    """
    Unit Tests for the ZInsights IoT API to increase coverage
    """

    def test_get_device_stats_request_error(self, fs):
        """Test get_device_stats handles request creation errors correctly"""
        from zscaler.zinsights.iot import IotAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        iot_api = IotAPI(mock_executor)
        result, response, err = iot_api.get_device_stats(limit=10)
        
        assert result is None
        assert err is not None

    def test_get_device_stats_execute_error(self, fs):
        """Test get_device_stats handles execution errors correctly"""
        from zscaler.zinsights.iot import IotAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        iot_api = IotAPI(mock_executor)
        result, response, err = iot_api.get_device_stats(limit=10)
        
        assert result is None
        assert err is not None

    def test_get_device_stats_graphql_error(self, fs):
        """Test get_device_stats handles GraphQL errors correctly"""
        from zscaler.zinsights.iot import IotAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response with GraphQL error
        mock_response = Mock()
        mock_response.get_body = Mock(return_value={
            "errors": [{"message": "GraphQL error"}]
        })
        mock_response._response = Mock()
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        iot_api = IotAPI(mock_executor)
        result, response, err = iot_api.get_device_stats(limit=10)
        
        assert result is None
        assert err is not None

    def test_get_device_stats_exception(self, fs):
        """Test get_device_stats handles exceptions in response parsing correctly"""
        from zscaler.zinsights.iot import IotAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that raises an exception during get_body
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        iot_api = IotAPI(mock_executor)
        result, response, err = iot_api.get_device_stats(limit=10)
        
        assert result is None
        assert err is not None


class TestWebTrafficUnit:
    """
    Unit Tests for the ZInsights Web Traffic API to increase coverage
    """

    def test_get_traffic_by_location_request_error(self, fs):
        """Test get_traffic_by_location handles request creation errors correctly"""
        from zscaler.zinsights.web_traffic import WebTrafficAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        web_api = WebTrafficAPI(mock_executor)
        result, response, err = web_api.get_traffic_by_location(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_traffic_by_location_execute_error(self, fs):
        """Test get_traffic_by_location handles execution errors correctly"""
        from zscaler.zinsights.web_traffic import WebTrafficAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        web_api = WebTrafficAPI(mock_executor)
        result, response, err = web_api.get_traffic_by_location(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_protocols_request_error(self, fs):
        """Test get_protocols handles request creation errors correctly"""
        from zscaler.zinsights.web_traffic import WebTrafficAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        web_api = WebTrafficAPI(mock_executor)
        result, response, err = web_api.get_protocols(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_protocols_execute_error(self, fs):
        """Test get_protocols handles execution errors correctly"""
        from zscaler.zinsights.web_traffic import WebTrafficAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        web_api = WebTrafficAPI(mock_executor)
        result, response, err = web_api.get_protocols(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_threat_super_categories_request_error(self, fs):
        """Test get_threat_super_categories handles request creation errors correctly"""
        from zscaler.zinsights.web_traffic import WebTrafficAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        web_api = WebTrafficAPI(mock_executor)
        result, response, err = web_api.get_threat_super_categories(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_threat_class_request_error(self, fs):
        """Test get_threat_class handles request creation errors correctly"""
        from zscaler.zinsights.web_traffic import WebTrafficAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        web_api = WebTrafficAPI(mock_executor)
        result, response, err = web_api.get_threat_class(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_no_grouping_request_error(self, fs):
        """Test get_no_grouping handles request creation errors correctly"""
        from zscaler.zinsights.web_traffic import WebTrafficAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        web_api = WebTrafficAPI(mock_executor)
        result, response, err = web_api.get_no_grouping(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None


class TestFirewallUnit:
    """
    Unit Tests for the ZInsights Firewall API to increase coverage
    """

    def test_get_traffic_by_action_request_error(self, fs):
        """Test get_traffic_by_action handles request creation errors correctly"""
        from zscaler.zinsights.firewall import FirewallAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        fw_api = FirewallAPI(mock_executor)
        result, response, err = fw_api.get_traffic_by_action(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_traffic_by_action_execute_error(self, fs):
        """Test get_traffic_by_action handles execution errors correctly"""
        from zscaler.zinsights.firewall import FirewallAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        fw_api = FirewallAPI(mock_executor)
        result, response, err = fw_api.get_traffic_by_action(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_traffic_by_location_request_error(self, fs):
        """Test get_traffic_by_location handles request creation errors correctly"""
        from zscaler.zinsights.firewall import FirewallAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        fw_api = FirewallAPI(mock_executor)
        result, response, err = fw_api.get_traffic_by_location(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_network_services_request_error(self, fs):
        """Test get_network_services handles request creation errors correctly"""
        from zscaler.zinsights.firewall import FirewallAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        fw_api = FirewallAPI(mock_executor)
        result, response, err = fw_api.get_network_services(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None


class TestCyberSecurityUnit:
    """
    Unit Tests for the ZInsights Cyber Security API to increase coverage
    """

    def test_get_incidents_request_error(self, fs):
        """Test get_incidents handles request creation errors correctly"""
        from zscaler.zinsights.cyber_security import CyberSecurityAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        cyber_api = CyberSecurityAPI(mock_executor)
        result, response, err = cyber_api.get_incidents(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_incidents_execute_error(self, fs):
        """Test get_incidents handles execution errors correctly"""
        from zscaler.zinsights.cyber_security import CyberSecurityAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        cyber_api = CyberSecurityAPI(mock_executor)
        result, response, err = cyber_api.get_incidents(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None


class TestSaasSecurityUnit:
    """
    Unit Tests for the ZInsights SaaS Security API to increase coverage
    """

    def test_get_casb_app_report_request_error(self, fs):
        """Test get_casb_app_report handles request creation errors correctly"""
        from zscaler.zinsights.saas_security import SaasSecurityAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        saas_api = SaasSecurityAPI(mock_executor)
        result, response, err = saas_api.get_casb_app_report(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

    def test_get_casb_app_report_execute_error(self, fs):
        """Test get_casb_app_report handles execution errors correctly"""
        from zscaler.zinsights.saas_security import SaasSecurityAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        saas_api = SaasSecurityAPI(mock_executor)
        result, response, err = saas_api.get_casb_app_report(
            start_time=int(time.time() * 1000) - 86400000,
            end_time=int(time.time() * 1000)
        )
        
        assert result is None
        assert err is not None

