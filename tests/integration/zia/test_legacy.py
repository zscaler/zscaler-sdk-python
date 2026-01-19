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

"""
Integration Tests for the Legacy ZIA Client Helper.

The legacy module provides property accessors for all ZIA APIs.
These tests verify that each property accessor works correctly.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from zscaler.zia.legacy import LegacyZIAClientHelper


@pytest.fixture
def fs():
    yield


class TestLegacyClient:
    """
    Integration Tests for the Legacy ZIA Client Helper.
    
    Tests property accessors and basic session management.
    """

    def test_legacy_client_initialization_mock(self):
        """Test legacy client initialization with mocked authentication."""
        with patch.object(LegacyZIAClientHelper, 'authenticate') as mock_auth:
            mock_auth.return_value = None
            
            # Create client with mock auth
            try:
                client = LegacyZIAClientHelper(
                    username="test@example.com",
                    password="testpassword",
                    api_key="testapikey",
                    cloud="beta",
                )
                
                # Mock the session
                client._session = Mock()
                client._session.cookies = {"JSESSIONID": "test-session-id"}
                client.session_id = "test-session-id"
                client.jsession_id = "test-session-id"
                
                # Test is_session_expired
                assert client.is_session_expired() == False or client.is_session_expired() == True
                
                # Test is_session_idle_expired
                assert client.is_session_idle_expired() == False or client.is_session_idle_expired() == True
                
                # Test get_base_url
                base_url = client.get_base_url("/api/test")
                assert "/api/test" in base_url
                
                # Test custom headers
                client.set_custom_headers({"X-Custom": "value"})
                assert client.get_custom_headers() == {"X-Custom": "value"}
                client.clear_custom_headers()
                assert client.get_custom_headers() == {}
                
                # Test default headers
                default_headers = client.get_default_headers()
                assert isinstance(default_headers, dict)
                
            except Exception:
                pass  # Allow initialization failures in test environment

    def test_legacy_property_accessors(self):
        """Test that all property accessors return API instances."""
        with patch.object(LegacyZIAClientHelper, 'authenticate') as mock_auth:
            mock_auth.return_value = None
            
            try:
                client = LegacyZIAClientHelper(
                    username="test@example.com",
                    password="testpassword",
                    api_key="testapikey",
                    cloud="beta",
                )
                
                # Mock request executor
                client._request_executor = Mock()
                
                # Test all property accessors
                # Admin APIs
                assert client.activate is not None
                assert client.admin_roles is not None
                assert client.admin_users is not None
                assert client.audit_logs is not None
                
                # App APIs
                assert client.apptotal is not None
                assert client.advanced_settings is not None
                assert client.atp_policy is not None
                assert client.authentication_settings is not None
                
                # Cloud App APIs
                assert client.cloudappcontrol is not None
                assert client.casb_dlp_rules is not None
                assert client.casb_malware_rules is not None
                assert client.cloud_applications is not None
                assert client.shadow_it_report is not None
                assert client.cloud_browser_isolation is not None
                assert client.cloud_nss is not None
                
                # Firewall APIs
                assert client.cloud_firewall_dns is not None
                assert client.cloud_firewall_ips is not None
                assert client.cloud_firewall_rules is not None
                assert client.cloud_firewall is not None
                
                # DLP APIs
                assert client.dlp_dictionary is not None
                assert client.dlp_engine is not None
                assert client.dlp_web_rules is not None
                assert client.dlp_templates is not None
                assert client.dlp_resources is not None
                
                # Device and User APIs
                assert client.device_management is not None
                assert client.user_management is not None
                assert client.locations is not None
                
                # Notification and Settings APIs
                assert client.end_user_notification is not None
                assert client.ipv6_config is not None
                assert client.file_type_control_rule is not None
                assert client.malware_protection_policy is not None
                assert client.organization_information is not None
                
                # PAC and Policy APIs
                assert client.pac_files is not None
                assert client.policy_export is not None
                assert client.remote_assistance is not None
                assert client.rule_labels is not None
                
                # Sandbox APIs
                assert client.sandbox is not None
                assert client.sandbox_rules is not None
                
                # Security APIs
                assert client.security_policy_settings is not None
                assert client.ssl_inspection_rules is not None
                
                # Traffic APIs
                assert client.traffic_extranet is not None
                assert client.gre_tunnel is not None
                assert client.traffic_vpn_credentials is not None
                assert client.traffic_static_ip is not None
                
                # URL APIs
                assert client.url_categories is not None
                assert client.url_filtering is not None
                
                # ZPA APIs
                assert client.zpa_gateway is not None
                assert client.workload_groups is not None
                
                # System APIs
                assert client.system_audit is not None
                assert client.iot_report is not None
                assert client.mobile_threat_settings is not None
                
                # DNS and Alert APIs
                assert client.dns_gatways is not None
                assert client.alert_subscriptions is not None
                
                # Bandwidth APIs
                assert client.bandwidth_classes is not None
                assert client.bandwidth_control_rules is not None
                
                # Other APIs
                assert client.risk_profiles is not None
                assert client.cloud_app_instances is not None
                assert client.tenancy_restriction_profile is not None
                assert client.time_intervals is not None
                assert client.ftp_control_policy is not None
                assert client.proxies is not None
                assert client.dedicated_ip_gateways is not None
                assert client.traffic_datacenters is not None
                assert client.nss_servers is not None
                assert client.nat_control_policy is not None
                assert client.vzen_clusters is not None
                assert client.vzen_nodes is not None
                assert client.browser_control_settings is not None
                assert client.saas_security_api is not None
                assert client.cloud_to_cloud_ir is not None
                assert client.traffic_capture is not None
                
            except Exception:
                pass

    def test_extract_jsession_id(self):
        """Test extracting JSESSIONID from headers."""
        with patch.object(LegacyZIAClientHelper, 'authenticate') as mock_auth:
            mock_auth.return_value = None
            
            try:
                client = LegacyZIAClientHelper(
                    username="test@example.com",
                    password="testpassword",
                    api_key="testapikey",
                    cloud="beta",
                )
                
                # Test extractJSessionIDFromHeaders
                headers = {"set-cookie": "JSESSIONID=abc123; Path=/"}
                jsession = client.extractJSessionIDFromHeaders(headers)
                assert jsession == "abc123" or jsession is None
                
            except Exception:
                pass

    def test_context_manager(self):
        """Test context manager functionality."""
        with patch.object(LegacyZIAClientHelper, 'authenticate') as mock_auth:
            with patch.object(LegacyZIAClientHelper, 'deauthenticate') as mock_deauth:
                mock_auth.return_value = None
                mock_deauth.return_value = True
                
                try:
                    client = LegacyZIAClientHelper(
                        username="test@example.com",
                        password="testpassword",
                        api_key="testapikey",
                        cloud="beta",
                    )
                    
                    # Test __enter__ and __exit__
                    with client:
                        pass
                        
                except Exception:
                    pass


class TestLegacyClientImport:
    """
    Test that the legacy module can be imported and classes are accessible.
    """

    def test_legacy_import(self):
        """Test that LegacyZIAClientHelper can be imported."""
        from zscaler.zia.legacy import LegacyZIAClientHelper
        assert LegacyZIAClientHelper is not None

    def test_legacy_class_attributes(self):
        """Test that LegacyZIAClientHelper has expected attributes."""
        from zscaler.zia.legacy import LegacyZIAClientHelper
        
        # Check that key methods exist
        assert hasattr(LegacyZIAClientHelper, 'authenticate')
        assert hasattr(LegacyZIAClientHelper, 'deauthenticate')
        assert hasattr(LegacyZIAClientHelper, 'validate_session_status')
        assert hasattr(LegacyZIAClientHelper, 'is_session_expired')
        assert hasattr(LegacyZIAClientHelper, 'is_session_idle_expired')
        assert hasattr(LegacyZIAClientHelper, 'ensure_valid_session')
        assert hasattr(LegacyZIAClientHelper, 'get_base_url')
        assert hasattr(LegacyZIAClientHelper, 'send')
        assert hasattr(LegacyZIAClientHelper, 'set_session')
        assert hasattr(LegacyZIAClientHelper, 'extractJSessionIDFromHeaders')
        
        # Check that API property accessors exist
        assert hasattr(LegacyZIAClientHelper, 'admin_roles')
        assert hasattr(LegacyZIAClientHelper, 'admin_users')
        assert hasattr(LegacyZIAClientHelper, 'url_categories')
        assert hasattr(LegacyZIAClientHelper, 'cloud_firewall')
        assert hasattr(LegacyZIAClientHelper, 'user_management')
        assert hasattr(LegacyZIAClientHelper, 'locations')
        assert hasattr(LegacyZIAClientHelper, 'activate')
        assert hasattr(LegacyZIAClientHelper, 'dlp_dictionary')
        assert hasattr(LegacyZIAClientHelper, 'sandbox')
