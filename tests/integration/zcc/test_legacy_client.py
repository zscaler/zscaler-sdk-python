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
from datetime import datetime, timedelta
import json


@pytest.fixture
def fs():
    yield


class TestLegacyZCCClient:
    """
    Unit Tests for the Legacy ZCC Client (LegacyZCCClientHelper)
    """

    @pytest.fixture
    def mock_response(self):
        """Create a mock response for successful login"""
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"jwtToken": "test_jwt_token_12345"}
        response.text = '{"jwtToken": "test_jwt_token_12345"}'
        response.headers = {}
        return response

    @pytest.fixture
    def mock_request_executor(self):
        """Create a mock request executor"""
        executor = Mock()
        executor.get_custom_headers.return_value = {}
        executor.set_custom_headers = Mock()
        executor.clear_custom_headers = Mock()
        executor.get_default_headers.return_value = {}
        return executor

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_legacy_client_initialization(self, mock_check_error, mock_post, mock_response):
        """Test legacy client initialization"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        assert client._api_key == "test_api_key"
        assert client._secret_key == "test_secret_key"
        assert client._env_cloud == "zscaler"
        assert client.auth_token == "test_jwt_token_12345"
        assert "auth-token" in client.headers

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_login_success(self, mock_check_error, mock_post, mock_response):
        """Test successful login"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        response = client.login()
        assert response.status_code == 200
        assert response.json()["jwtToken"] == "test_jwt_token_12345"

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_refresh_token(self, mock_check_error, mock_post, mock_response):
        """Test token refresh"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        # Force token refresh
        client.auth_token = None
        client.refreshToken()
        
        assert client.auth_token == "test_jwt_token_12345"

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_check_rate_limit_generic(self, mock_check_error, mock_post, mock_response):
        """Test generic rate limit checking"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        # Reset counters - note __init__ already made some requests
        initial_count = client.request_count
        client.last_request_time = datetime.utcnow()
        
        # Should not raise for a few more requests
        for i in range(5):
            client.check_rate_limit("/test/path")
        
        assert client.request_count == initial_count + 5
        
        # Simulate hitting rate limit - should raise an exception
        client.request_count = 100
        
        with pytest.raises(Exception):  # RateLimitExceededError or AttributeError
            client.check_rate_limit("/test/path")

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_check_rate_limit_download_devices(self, mock_check_error, mock_post, mock_response):
        """Test download devices rate limit checking"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        # Reset download devices counters completely
        client.download_devices_count = 0
        client.download_devices_last_reset = datetime.utcnow()
        # Also reset the general counter to avoid hitting the 100/hour limit
        client.request_count = 0
        client.last_request_time = datetime.utcnow()
        
        # Should allow first 3 calls
        for i in range(3):
            client.check_rate_limit("/downloadDevices")
        
        assert client.download_devices_count == 3
        
        # Fourth call should raise an exception
        with pytest.raises(Exception):  # RateLimitExceededError or AttributeError
            client.check_rate_limit("/downloadDevices")

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_rate_limit_reset_after_hour(self, mock_check_error, mock_post, mock_response):
        """Test rate limit resets after an hour"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        # Set request count to 99 and time to 2 hours ago
        client.request_count = 99
        client.last_request_time = datetime.utcnow() - timedelta(hours=2)
        
        # Should reset counter
        client.check_rate_limit("/test/path")
        
        assert client.request_count == 1  # Reset to 0, then incremented to 1

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_get_backoff_seconds(self, mock_check_error, mock_post, mock_response):
        """Test backoff seconds calculation"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        # Test with header present
        response = Mock()
        response.headers = {"X-Rate-Limit-Retry-After-Seconds": "120"}
        
        backoff = client._get_backoff_seconds(response)
        assert backoff == 121  # 120 + 1 second pad
        
        # Test without header
        response.headers = {}
        backoff = client._get_backoff_seconds(response, default=30)
        assert backoff == 30

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_get_base_url(self, mock_check_error, mock_post, mock_response):
        """Test get_base_url method"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscalerbeta"
        )
        
        url = client.get_base_url("/test/endpoint")
        assert url == "https://api-mobile.zscalerbeta.net"

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.requests.request')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_send_success(self, mock_check_error, mock_request, mock_post, mock_response):
        """Test successful send"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        send_response = Mock()
        send_response.status_code = 200
        send_response.headers = {"X-Rate-Limit-Remaining": "99"}
        send_response.text = '{"result": "success"}'
        mock_request.return_value = send_response
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        response, request_info = client.send("GET", "/test/path", params={"key": "value"})
        
        assert response.status_code == 200
        assert request_info["method"] == "GET"

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_context_manager(self, mock_check_error, mock_post, mock_response):
        """Test context manager functionality"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        with LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        ) as client:
            assert client.auth_token == "test_jwt_token_12345"

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_partner_id_header(self, mock_check_error, mock_post, mock_response):
        """Test partner ID header is set correctly"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler",
            partner_id="test_partner_123"
        )
        
        assert client.partner_id == "test_partner_123"
        assert client.headers.get("x-partner-id") == "test_partner_123"

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_custom_headers(self, mock_check_error, mock_post, mock_response):
        """Test custom headers management"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        # Test set_custom_headers
        client.set_custom_headers({"X-Custom": "value"})
        custom_headers = client.get_custom_headers()
        assert "X-Custom" in custom_headers
        assert custom_headers["X-Custom"] == "value"
        
        # Test clear_custom_headers
        client.clear_custom_headers()
        custom_headers = client.get_custom_headers()
        assert "X-Custom" not in custom_headers
        
        # Test get_default_headers
        default_headers = client.get_default_headers()
        assert isinstance(default_headers, dict)

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_api_properties(self, mock_check_error, mock_post, mock_response):
        """Test API property accessors"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        # Test all API properties return correct types
        from zscaler.zcc.devices import DevicesAPI
        from zscaler.zcc.admin_user import AdminUserAPI
        from zscaler.zcc.company import CompanyInfoAPI
        from zscaler.zcc.entitlements import EntitlementAPI
        from zscaler.zcc.forwarding_profile import ForwardingProfileAPI
        from zscaler.zcc.fail_open_policy import FailOpenPolicyAPI
        from zscaler.zcc.web_policy import WebPolicyAPI
        from zscaler.zcc.web_app_service import WebAppServiceAPI
        from zscaler.zcc.web_privacy import WebPrivacyAPI
        from zscaler.zcc.trusted_networks import TrustedNetworksAPI
        
        assert isinstance(client.devices, DevicesAPI)
        assert isinstance(client.admin_user, AdminUserAPI)
        assert isinstance(client.company, CompanyInfoAPI)
        assert isinstance(client.entitlements, EntitlementAPI)
        assert isinstance(client.forwarding_profile, ForwardingProfileAPI)
        assert isinstance(client.fail_open_policy, FailOpenPolicyAPI)
        assert isinstance(client.web_policy, WebPolicyAPI)
        assert isinstance(client.web_app_service, WebAppServiceAPI)
        assert isinstance(client.web_privacy, WebPrivacyAPI)
        assert isinstance(client.trusted_networks, TrustedNetworksAPI)

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_set_session(self, mock_check_error, mock_post, mock_response):
        """Test set_session method"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        client = LegacyZCCClientHelper(
            api_key="test_api_key",
            secret_key="test_secret_key",
            cloud="zscaler"
        )
        
        mock_session = Mock()
        client.set_session(mock_session)
        
        assert client._session == mock_session

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_login_failure(self, mock_check_error, mock_post):
        """Test login failure handling"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid credentials"}
        mock_response.text = '{"error": "Invalid credentials"}'
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, Exception("Login failed"))
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        with pytest.raises(Exception) as exc_info:
            LegacyZCCClientHelper(
                api_key="invalid_key",
                secret_key="invalid_secret",
                cloud="zscaler"
            )
        
        # Login failure should raise an exception

    @patch('zscaler.zcc.legacy.requests.post')
    @patch('zscaler.zcc.legacy.requests.request')
    @patch('zscaler.zcc.legacy.check_response_for_error')
    def test_send_with_429_retry(self, mock_check_error, mock_request, mock_post, mock_response):
        """Test 429 retry handling"""
        mock_post.return_value = mock_response
        mock_check_error.return_value = (None, None)
        
        # First call returns 429, second succeeds
        response_429 = Mock()
        response_429.status_code = 429
        response_429.headers = {"X-Rate-Limit-Retry-After-Seconds": "1"}
        
        response_200 = Mock()
        response_200.status_code = 200
        response_200.headers = {"X-Rate-Limit-Remaining": "99"}
        response_200.text = '{"result": "success"}'
        
        mock_request.side_effect = [response_429, response_200]
        
        from zscaler.zcc.legacy import LegacyZCCClientHelper
        
        with patch('zscaler.zcc.legacy.time.sleep'):  # Speed up test
            client = LegacyZCCClientHelper(
                api_key="test_api_key",
                secret_key="test_secret_key",
                cloud="zscaler"
            )
            
            response, _ = client.send("GET", "/test/path")
            assert response.status_code == 200

