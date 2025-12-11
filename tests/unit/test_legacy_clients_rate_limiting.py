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
Unit tests for rate limiting functionality in legacy clients.

This module tests the 429 rate limiting behavior for each legacy client:
- ZPA Legacy Client
- ZIA Legacy Client
- ZCC Legacy Client
- ZDX Legacy Client
- ZTW Legacy Client
- ZWA Legacy Client

Each client should properly handle 429 responses with appropriate retry logic.
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from typing import Dict, Any


# =============================================================================
# Mock Response Classes
# =============================================================================

class MockResponse:
    """Mock HTTP response for testing."""
    
    def __init__(
        self,
        status_code: int = 200,
        headers: Dict[str, str] = None,
        text: str = '{"data": "success"}',
        json_data: Dict[str, Any] = None
    ):
        self.status_code = status_code
        self.headers = headers or {"Content-Type": "application/json"}
        self.text = text
        self._json_data = json_data or {"data": "success"}
    
    def json(self):
        return self._json_data


class Mock429Response(MockResponse):
    """Mock 429 Too Many Requests response."""
    
    def __init__(self, retry_after: str = None, retry_after_lowercase: str = None):
        headers = {"Content-Type": "application/json"}
        if retry_after:
            headers["Retry-After"] = retry_after
        if retry_after_lowercase:
            headers["retry-after"] = retry_after_lowercase
        super().__init__(
            status_code=429,
            headers=headers,
            text='{"error": "Rate limit exceeded"}',
            json_data={"error": "Rate limit exceeded"}
        )


class Mock200Response(MockResponse):
    """Mock successful 200 response."""
    
    def __init__(self, json_data: Dict[str, Any] = None):
        super().__init__(
            status_code=200,
            headers={"Content-Type": "application/json"},
            text='{"data": "success"}',
            json_data=json_data or {"data": "success"}
        )


# =============================================================================
# ZPA Legacy Client Tests
# =============================================================================

class TestZPALegacyClientRateLimiting:
    """Test rate limiting in ZPA Legacy Client."""

    def test_429_with_retry_after_header(self):
        """Test ZPA legacy client handles 429 with Retry-After header."""
        with patch('zscaler.zpa.legacy.requests') as mock_requests, \
             patch('zscaler.zpa.legacy.check_response_for_error') as mock_check_error:
            
            from zscaler.zpa.legacy import LegacyZPAClientHelper
            
            # Mock login response
            mock_login_response = Mock200Response(json_data={"access_token": "test_token"})
            mock_requests.post.return_value = mock_login_response
            mock_check_error.return_value = ({"access_token": "test_token"}, None)
            
            # Initialize client
            client = LegacyZPAClientHelper(
                client_id="test_client_id",
                client_secret="test_client_secret",
                customer_id="test_customer_id",
                cloud="PRODUCTION"
            )
            
            # Reset the mock for the actual test
            mock_requests.request.reset_mock()
            
            # First call returns 429, second call returns 200
            mock_requests.request.side_effect = [
                Mock429Response(retry_after="2"),
                Mock200Response()
            ]
            
            with patch('zscaler.zpa.legacy.LegacyZPAClientHelper.send') as mock_send:
                # Test the actual retry logic by calling the real implementation
                pass
            
            # Directly test the send method behavior
            mock_requests.request.side_effect = [
                Mock429Response(retry_after="2"),
                Mock200Response()
            ]
            
            with patch.object(client, 'refreshToken'):
                with patch('time.sleep') as mock_sleep:
                    response, request_info = client.send("GET", "/test/endpoint")
            
            # Should have retried after sleeping
            mock_sleep.assert_called_once_with(2)
            assert response.status_code == 200
            assert mock_requests.request.call_count == 2

    def test_429_with_lowercase_retry_after_header(self):
        """Test ZPA legacy client handles 429 with lowercase retry-after header."""
        with patch('zscaler.zpa.legacy.requests') as mock_requests, \
             patch('zscaler.zpa.legacy.check_response_for_error') as mock_check_error:
            
            from zscaler.zpa.legacy import LegacyZPAClientHelper
            
            mock_login_response = Mock200Response(json_data={"access_token": "test_token"})
            mock_requests.post.return_value = mock_login_response
            mock_check_error.return_value = ({"access_token": "test_token"}, None)
            
            client = LegacyZPAClientHelper(
                client_id="test_client_id",
                client_secret="test_client_secret",
                customer_id="test_customer_id",
                cloud="PRODUCTION"
            )
            
            mock_requests.request.reset_mock()
            mock_requests.request.side_effect = [
                Mock429Response(retry_after_lowercase="3"),
                Mock200Response()
            ]
            
            with patch.object(client, 'refreshToken'):
                with patch('time.sleep') as mock_sleep:
                    response, request_info = client.send("GET", "/test/endpoint")
            
            mock_sleep.assert_called_once_with(3)
            assert response.status_code == 200

    def test_429_without_retry_after_uses_default(self):
        """Test ZPA legacy client uses default 2 seconds when Retry-After header missing."""
        with patch('zscaler.zpa.legacy.requests') as mock_requests, \
             patch('zscaler.zpa.legacy.check_response_for_error') as mock_check_error:
            
            from zscaler.zpa.legacy import LegacyZPAClientHelper
            
            mock_login_response = Mock200Response(json_data={"access_token": "test_token"})
            mock_requests.post.return_value = mock_login_response
            mock_check_error.return_value = ({"access_token": "test_token"}, None)
            
            client = LegacyZPAClientHelper(
                client_id="test_client_id",
                client_secret="test_client_secret",
                customer_id="test_customer_id",
                cloud="PRODUCTION"
            )
            
            mock_requests.request.reset_mock()
            mock_requests.request.side_effect = [
                Mock429Response(),  # No retry-after header
                Mock200Response()
            ]
            
            with patch.object(client, 'refreshToken'):
                with patch('time.sleep') as mock_sleep:
                    response, request_info = client.send("GET", "/test/endpoint")
            
            # Should use default 2 seconds
            mock_sleep.assert_called_once_with(2)
            assert response.status_code == 200

    def test_429_multiple_retries(self):
        """Test ZPA legacy client retries multiple times on repeated 429."""
        with patch('zscaler.zpa.legacy.requests') as mock_requests, \
             patch('zscaler.zpa.legacy.check_response_for_error') as mock_check_error:
            
            from zscaler.zpa.legacy import LegacyZPAClientHelper
            
            mock_login_response = Mock200Response(json_data={"access_token": "test_token"})
            mock_requests.post.return_value = mock_login_response
            mock_check_error.return_value = ({"access_token": "test_token"}, None)
            
            client = LegacyZPAClientHelper(
                client_id="test_client_id",
                client_secret="test_client_secret",
                customer_id="test_customer_id",
                cloud="PRODUCTION"
            )
            
            mock_requests.request.reset_mock()
            mock_requests.request.side_effect = [
                Mock429Response(retry_after="1"),
                Mock429Response(retry_after="1"),
                Mock429Response(retry_after="1"),
                Mock200Response()
            ]
            
            with patch.object(client, 'refreshToken'):
                with patch('time.sleep') as mock_sleep:
                    response, request_info = client.send("GET", "/test/endpoint")
            
            assert mock_sleep.call_count == 3
            assert response.status_code == 200
            assert mock_requests.request.call_count == 4

    def test_429_max_retries_exceeded(self):
        """Test ZPA legacy client raises after max retries exceeded."""
        with patch('zscaler.zpa.legacy.requests') as mock_requests, \
             patch('zscaler.zpa.legacy.check_response_for_error') as mock_check_error:
            
            from zscaler.zpa.legacy import LegacyZPAClientHelper
            
            mock_login_response = Mock200Response(json_data={"access_token": "test_token"})
            mock_requests.post.return_value = mock_login_response
            mock_check_error.return_value = ({"access_token": "test_token"}, None)
            
            client = LegacyZPAClientHelper(
                client_id="test_client_id",
                client_secret="test_client_secret",
                customer_id="test_customer_id",
                cloud="PRODUCTION"
            )
            
            mock_requests.request.reset_mock()
            # All 429s - should exhaust retries (5 max)
            mock_requests.request.side_effect = [
                Mock429Response(retry_after="1"),
                Mock429Response(retry_after="1"),
                Mock429Response(retry_after="1"),
                Mock429Response(retry_after="1"),
                Mock429Response(retry_after="1"),
            ]
            
            with patch.object(client, 'refreshToken'):
                with patch('time.sleep'):
                    with pytest.raises(ValueError, match="maximum retries"):
                        client.send("GET", "/test/endpoint")


# =============================================================================
# ZIA Legacy Client Tests
# =============================================================================

class TestZIALegacyClientRateLimiting:
    """Test rate limiting in ZIA Legacy Client."""

    def test_429_with_retry_after_header(self):
        """Test ZIA legacy client handles 429 with Retry-After header."""
        with patch('zscaler.zia.legacy.requests') as mock_requests, \
             patch('zscaler.zia.legacy.check_response_for_error') as mock_check_error, \
             patch('zscaler.zia.legacy.obfuscate_api_key') as mock_obfuscate:
            
            from zscaler.zia.legacy import LegacyZIAClientHelper
            
            # Mock auth response with session cookie
            mock_auth_response = Mock200Response(json_data={"authType": "ADMIN_LOGIN"})
            mock_auth_response.headers = {
                "Content-Type": "application/json",
                "Set-Cookie": "JSESSIONID=test_session_id; Path=/; Secure; HttpOnly"
            }
            mock_requests.post.return_value = mock_auth_response
            mock_check_error.return_value = ({"authType": "ADMIN_LOGIN"}, None)
            # Return dict with 'key' and 'timestamp' keys
            mock_obfuscate.return_value = {"key": "obfuscated_key", "timestamp": "123456"}
            
            client = LegacyZIAClientHelper(
                username="test_user",
                password="test_password",
                api_key="test_api_key",
                cloud="zscaler"
            )
            
            mock_requests.request.reset_mock()
            mock_requests.request.side_effect = [
                Mock429Response(retry_after="2"),
                Mock200Response()
            ]
            
            with patch.object(client, 'ensure_valid_session'):
                with patch('zscaler.zia.legacy.sleep') as mock_sleep:
                    response, request_info = client.send("GET", "/test/endpoint")
            
            mock_sleep.assert_called_once_with(2)
            assert response.status_code == 200
            assert mock_requests.request.call_count == 2

    def test_429_without_retry_after_uses_default(self):
        """Test ZIA legacy client uses default 2 seconds when Retry-After missing."""
        with patch('zscaler.zia.legacy.requests') as mock_requests, \
             patch('zscaler.zia.legacy.check_response_for_error') as mock_check_error, \
             patch('zscaler.zia.legacy.obfuscate_api_key') as mock_obfuscate:
            
            from zscaler.zia.legacy import LegacyZIAClientHelper
            
            mock_auth_response = Mock200Response(json_data={"authType": "ADMIN_LOGIN"})
            mock_auth_response.headers = {
                "Content-Type": "application/json",
                "Set-Cookie": "JSESSIONID=test_session_id; Path=/; Secure; HttpOnly"
            }
            mock_requests.post.return_value = mock_auth_response
            mock_check_error.return_value = ({"authType": "ADMIN_LOGIN"}, None)
            mock_obfuscate.return_value = {"key": "obfuscated_key", "timestamp": "123456"}
            
            client = LegacyZIAClientHelper(
                username="test_user",
                password="test_password",
                api_key="test_api_key",
                cloud="zscaler"
            )
            
            mock_requests.request.reset_mock()
            mock_requests.request.side_effect = [
                Mock429Response(),
                Mock200Response()
            ]
            
            with patch.object(client, 'ensure_valid_session'):
                with patch('zscaler.zia.legacy.sleep') as mock_sleep:
                    response, request_info = client.send("GET", "/test/endpoint")
            
            mock_sleep.assert_called_once_with(2)
            assert response.status_code == 200


# =============================================================================
# ZTW Legacy Client Tests
# =============================================================================

class TestZTWLegacyClientRateLimiting:
    """Test rate limiting in ZTW Legacy Client."""

    def test_429_with_retry_after_header(self):
        """Test ZTW legacy client handles 429 with Retry-After header."""
        with patch('zscaler.ztw.legacy.requests') as mock_requests, \
             patch('zscaler.ztw.legacy.check_response_for_error') as mock_check_error, \
             patch('zscaler.ztw.legacy.obfuscate_api_key') as mock_obfuscate:
            
            from zscaler.ztw.legacy import LegacyZTWClientHelper
            
            mock_auth_response = Mock200Response(json_data={"authType": "ADMIN_LOGIN"})
            mock_auth_response.headers = {
                "Content-Type": "application/json",
                "Set-Cookie": "JSESSIONID=test_session_id; Path=/; Secure; HttpOnly"
            }
            mock_requests.post.return_value = mock_auth_response
            mock_check_error.return_value = ({"authType": "ADMIN_LOGIN"}, None)
            mock_obfuscate.return_value = {"key": "obfuscated_key", "timestamp": "123456"}
            
            client = LegacyZTWClientHelper(
                username="test_user",
                password="test_password",
                api_key="test_api_key",
                cloud="zscaler"
            )
            
            mock_requests.request.reset_mock()
            mock_requests.request.side_effect = [
                Mock429Response(retry_after="2"),
                Mock200Response()
            ]
            
            # ZTW doesn't have ensure_valid_session, just run the send directly
            with patch('zscaler.ztw.legacy.sleep') as mock_sleep:
                response, request_info = client.send("GET", "/test/endpoint")
            
            mock_sleep.assert_called_once_with(2)
            assert response.status_code == 200


# =============================================================================
# Cross-Client Consistency Tests
# =============================================================================

class TestLegacyClientRateLimitingConsistency:
    """Test that all legacy clients handle rate limiting consistently."""

    def test_all_legacy_clients_have_429_handling(self):
        """Verify all legacy clients implement 429 handling."""
        from zscaler.zpa.legacy import LegacyZPAClientHelper
        from zscaler.zia.legacy import LegacyZIAClientHelper
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        from zscaler.zdx.legacy import LegacyZDXClientHelper
        from zscaler.ztw.legacy import LegacyZTWClientHelper
        from zscaler.zwa.legacy import LegacyZWAClientHelper
        
        # All clients should have a 'send' method
        assert hasattr(LegacyZPAClientHelper, 'send')
        assert hasattr(LegacyZIAClientHelper, 'send')
        assert hasattr(LegacyZCCClientHelper, 'send')
        assert hasattr(LegacyZDXClientHelper, 'send')
        assert hasattr(LegacyZTWClientHelper, 'send')
        assert hasattr(LegacyZWAClientHelper, 'send')
        
        # Verify the send method signature includes rate limiting logic
        import inspect
        
        # Check ZPA has retry loop (contains 'status_code == 429')
        zpa_source = inspect.getsource(LegacyZPAClientHelper.send)
        assert '429' in zpa_source, "ZPA legacy client should handle 429"
        assert 'retry' in zpa_source.lower() or 'attempts' in zpa_source.lower(), \
            "ZPA legacy client should have retry logic"
        
        # Check ZIA has retry loop
        zia_source = inspect.getsource(LegacyZIAClientHelper.send)
        assert '429' in zia_source, "ZIA legacy client should handle 429"
        assert 'Retry-After' in zia_source, "ZIA should use Retry-After header"
        
        # Check ZCC has retry loop
        zcc_source = inspect.getsource(LegacyZCCClientHelper.send)
        assert '429' in zcc_source, "ZCC legacy client should handle 429"
        
        # Check ZDX has 429 handling in _get_with_rate_limiting method (not in send)
        # ZDX handles 429 during rate-limited requests, not in the main send method
        zdx_rate_limit_source = inspect.getsource(LegacyZDXClientHelper._get_with_rate_limiting)
        assert '429' in zdx_rate_limit_source, "ZDX legacy client should handle 429 in _get_with_rate_limiting"
        
        # Check ZTW has retry loop
        ztw_source = inspect.getsource(LegacyZTWClientHelper.send)
        assert '429' in ztw_source, "ZTW legacy client should handle 429"
        assert 'Retry-After' in ztw_source, "ZTW should use Retry-After header"
        
        # Check ZWA has 429 handling in _get_with_rate_limiting method
        # ZWA handles 429 during rate-limited requests
        zwa_rate_limit_source = inspect.getsource(LegacyZWAClientHelper._get_with_rate_limiting)
        assert '429' in zwa_rate_limit_source, "ZWA legacy client should handle 429 in _get_with_rate_limiting"

    def test_zpa_handles_both_retry_after_header_cases(self):
        """Verify ZPA handles both 'Retry-After' and 'retry-after' headers."""
        import inspect
        from zscaler.zpa.legacy import LegacyZPAClientHelper
        
        zpa_source = inspect.getsource(LegacyZPAClientHelper.send)
        
        # Should check for lowercase (ZPA specific)
        assert 'retry-after' in zpa_source.lower(), \
            "ZPA should handle lowercase retry-after header"
        # Should also check for uppercase (fallback)
        assert 'Retry-After' in zpa_source, \
            "ZPA should handle uppercase Retry-After header as fallback"


# =============================================================================
# Unit Tests for Specific Rate Limiting Behavior
# =============================================================================

class TestZPARateLimitingDetails:
    """Detailed tests for ZPA rate limiting implementation."""

    def test_retry_after_parsing_integer(self):
        """Test parsing integer Retry-After value."""
        with patch('zscaler.zpa.legacy.requests') as mock_requests, \
             patch('zscaler.zpa.legacy.check_response_for_error') as mock_check_error:
            
            from zscaler.zpa.legacy import LegacyZPAClientHelper
            
            mock_login_response = Mock200Response(json_data={"access_token": "test_token"})
            mock_requests.post.return_value = mock_login_response
            mock_check_error.return_value = ({"access_token": "test_token"}, None)
            
            client = LegacyZPAClientHelper(
                client_id="test_client_id",
                client_secret="test_client_secret",
                customer_id="test_customer_id",
                cloud="PRODUCTION"
            )
            
            mock_requests.request.reset_mock()
            
            # Test with integer string
            mock_requests.request.side_effect = [
                Mock429Response(retry_after="10"),
                Mock200Response()
            ]
            
            with patch.object(client, 'refreshToken'):
                with patch('time.sleep') as mock_sleep:
                    response, _ = client.send("GET", "/test/endpoint")
            
            mock_sleep.assert_called_with(10)

    def test_both_header_variants_checked(self):
        """Test that both retry-after and Retry-After headers are checked."""
        with patch('zscaler.zpa.legacy.requests') as mock_requests, \
             patch('zscaler.zpa.legacy.check_response_for_error') as mock_check_error:
            
            from zscaler.zpa.legacy import LegacyZPAClientHelper
            
            mock_login_response = Mock200Response(json_data={"access_token": "test_token"})
            mock_requests.post.return_value = mock_login_response
            mock_check_error.return_value = ({"access_token": "test_token"}, None)
            
            client = LegacyZPAClientHelper(
                client_id="test_client_id",
                client_secret="test_client_secret",
                customer_id="test_customer_id",
                cloud="PRODUCTION"
            )
            
            mock_requests.request.reset_mock()
            
            # Create response with only lowercase header
            response_429 = Mock429Response()
            response_429.headers["retry-after"] = "5"
            
            mock_requests.request.side_effect = [
                response_429,
                Mock200Response()
            ]
            
            with patch.object(client, 'refreshToken'):
                with patch('time.sleep') as mock_sleep:
                    response, _ = client.send("GET", "/test/endpoint")
            
            # Should use the lowercase header value
            mock_sleep.assert_called_with(5)


class TestZIARateLimitingDetails:
    """Detailed tests for ZIA rate limiting implementation."""

    def test_zia_retry_loop_structure(self):
        """Verify ZIA has proper retry loop with max attempts."""
        import inspect
        from zscaler.zia.legacy import LegacyZIAClientHelper
        
        zia_source = inspect.getsource(LegacyZIAClientHelper.send)
        
        # Should have a while loop with attempts
        assert 'while' in zia_source, "ZIA should have a while loop for retries"
        assert 'attempts' in zia_source, "ZIA should track attempts"
        assert '< 5' in zia_source or '<= 4' in zia_source or 'attempts < 5' in zia_source, \
            "ZIA should have max 5 attempts"
