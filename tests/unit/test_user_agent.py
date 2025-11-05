"""
Unit tests for Zscaler SDK User Agent functionality.

Tests user agent string construction and formatting.
"""

import pytest
import platform
import re
from unittest.mock import patch
from zscaler.user_agent import UserAgent
from zscaler import __version__ as VERSION


class TestUserAgentInitialization:
    """Test UserAgent class initialization."""

    def test_user_agent_initialization_without_extra(self):
        """Test UserAgent can be initialized without extra string."""
        ua = UserAgent()
        assert ua is not None
        assert ua._user_agent_string is not None

    def test_user_agent_initialization_with_extra(self):
        """Test UserAgent can be initialized with extra string."""
        extra = "custom-app/1.0"
        ua = UserAgent(user_agent_extra=extra)
        assert ua is not None
        assert extra in ua._user_agent_string

    def test_user_agent_initialization_with_none_extra(self):
        """Test UserAgent handles None as extra parameter."""
        ua = UserAgent(user_agent_extra=None)
        assert ua is not None
        assert ua._user_agent_string is not None


class TestUserAgentStringFormat:
    """Test user agent string formatting and content."""

    def test_user_agent_contains_sdk_name(self):
        """Test user agent string contains SDK name."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        assert "zscaler-sdk-python" in ua_string
        assert ua_string.startswith("zscaler-sdk-python/")

    def test_user_agent_contains_version(self):
        """Test user agent string contains SDK version."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        assert VERSION in ua_string
        assert f"zscaler-sdk-python/{VERSION}" in ua_string

    def test_user_agent_contains_python_version(self):
        """Test user agent string contains Python version."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        python_version = platform.python_version()
        assert python_version in ua_string
        assert f"python/{python_version}" in ua_string

    def test_user_agent_contains_os_info(self):
        """Test user agent string contains OS information."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        os_name = platform.system()
        os_version = platform.release()
        
        assert os_name in ua_string
        assert os_version in ua_string
        assert f"{os_name}/{os_version}" in ua_string

    def test_user_agent_format_structure(self):
        """Test user agent string follows expected format."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        # Expected format: "zscaler-sdk-python/VERSION python/PY_VERSION OS/OS_VERSION"
        parts = ua_string.split()
        
        assert len(parts) >= 3
        assert parts[0].startswith("zscaler-sdk-python/")
        assert parts[1].startswith("python/")
        # OS part could be "Darwin/24.6.0" or "Linux/5.x.x" etc.
        assert "/" in parts[2]

    def test_user_agent_with_extra_appended_correctly(self):
        """Test extra user agent info is appended at the end."""
        extra = "terraform/1.5.0"
        ua = UserAgent(user_agent_extra=extra)
        ua_string = ua.get_user_agent_string()
        
        assert ua_string.endswith(extra)
        assert f" {extra}" in ua_string

    def test_user_agent_get_method_returns_string(self):
        """Test get_user_agent_string returns a string."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        assert isinstance(ua_string, str)
        assert len(ua_string) > 0


class TestUserAgentClassAttributes:
    """Test UserAgent class attributes."""

    def test_sdk_name_constant(self):
        """Test SDK_NAME class constant."""
        assert UserAgent.SDK_NAME == "zscaler-sdk-python"
        assert isinstance(UserAgent.SDK_NAME, str)

    def test_python_constant(self):
        """Test PYTHON class constant."""
        assert UserAgent.PYTHON == "python"
        assert isinstance(UserAgent.PYTHON, str)


class TestUserAgentEdgeCases:
    """Test edge cases for UserAgent."""

    def test_user_agent_with_empty_string_extra(self):
        """Test UserAgent with empty string as extra."""
        ua = UserAgent(user_agent_extra="")
        ua_string = ua.get_user_agent_string()
        
        # Should still contain base components
        assert "zscaler-sdk-python" in ua_string
        assert "python/" in ua_string

    def test_user_agent_with_special_characters_in_extra(self):
        """Test UserAgent with special characters in extra."""
        extra = "app/1.0 (build-123) custom-tag"
        ua = UserAgent(user_agent_extra=extra)
        ua_string = ua.get_user_agent_string()
        
        assert extra in ua_string

    def test_user_agent_multiple_instances(self):
        """Test multiple UserAgent instances are independent."""
        ua1 = UserAgent(user_agent_extra="app1/1.0")
        ua2 = UserAgent(user_agent_extra="app2/2.0")
        
        ua1_string = ua1.get_user_agent_string()
        ua2_string = ua2.get_user_agent_string()
        
        assert "app1/1.0" in ua1_string
        assert "app1/1.0" not in ua2_string
        assert "app2/2.0" in ua2_string
        assert "app2/2.0" not in ua1_string

    def test_user_agent_immutable_after_creation(self):
        """Test user agent string doesn't change after creation."""
        ua = UserAgent()
        ua_string1 = ua.get_user_agent_string()
        ua_string2 = ua.get_user_agent_string()
        
        assert ua_string1 == ua_string2


class TestUserAgentPlatformVariations:
    """Test UserAgent across different platform scenarios."""

    @patch('platform.python_version')
    @patch('platform.system')
    @patch('platform.release')
    def test_user_agent_with_mocked_platform(self, mock_release, mock_system, mock_python_version):
        """Test UserAgent with mocked platform information."""
        mock_python_version.return_value = "3.11.0"
        mock_system.return_value = "Linux"
        mock_release.return_value = "5.15.0"
        
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        assert "python/3.11.0" in ua_string
        assert "Linux/5.15.0" in ua_string

    @patch('platform.python_version')
    @patch('platform.system')
    @patch('platform.release')
    def test_user_agent_windows_platform(self, mock_release, mock_system, mock_python_version):
        """Test UserAgent on Windows platform."""
        mock_python_version.return_value = "3.10.5"
        mock_system.return_value = "Windows"
        mock_release.return_value = "10"
        
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        assert "Windows/10" in ua_string

    @patch('platform.python_version')
    @patch('platform.system')
    @patch('platform.release')
    def test_user_agent_darwin_platform(self, mock_release, mock_system, mock_python_version):
        """Test UserAgent on macOS (Darwin) platform."""
        mock_python_version.return_value = "3.9.7"
        mock_system.return_value = "Darwin"
        mock_release.return_value = "21.6.0"
        
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        assert "Darwin/21.6.0" in ua_string


class TestUserAgentIntegration:
    """Test UserAgent integration scenarios."""

    def test_user_agent_version_matches_package_version(self):
        """Test that user agent includes the actual package version."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        # Verify the version format (e.g., "1.8.4")
        assert re.search(r'\d+\.\d+\.\d+', ua_string)
        assert f"zscaler-sdk-python/{VERSION}" in ua_string

    def test_user_agent_realistic_format(self):
        """Test user agent has realistic format for HTTP headers."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        # Should be a single line, no newlines
        assert "\n" not in ua_string
        assert "\r" not in ua_string
        
        # Should be reasonable length (not too long for HTTP headers)
        assert len(ua_string) < 500
        
        # Should contain forward slashes for versioning
        assert ua_string.count("/") >= 3

    def test_user_agent_with_terraform_integration(self):
        """Test user agent when used with Terraform provider."""
        extra = "terraform-provider-zscaler/1.0.0"
        ua = UserAgent(user_agent_extra=extra)
        ua_string = ua.get_user_agent_string()
        
        assert "terraform-provider-zscaler/1.0.0" in ua_string
        assert "zscaler-sdk-python" in ua_string

    def test_user_agent_no_sensitive_information(self):
        """Test user agent doesn't contain sensitive information."""
        ua = UserAgent()
        ua_string = ua.get_user_agent_string()
        
        # Should not contain common sensitive patterns
        assert "password" not in ua_string.lower()
        assert "secret" not in ua_string.lower()
        assert "key" not in ua_string.lower()
        assert "token" not in ua_string.lower()


class TestPartnerIdHeader:
    """
    Test x-partner-id header functionality.
    
    Note: This is not part of the UserAgent class itself, but tests the
    partnerId configuration feature that automatically adds the x-partner-id
    header to all API requests when partnerId is provided in the configuration.
    This feature is implemented in RequestExecutor and is tested here for
    completeness alongside user agent functionality.
    """

    def test_partner_id_header_in_request_executor(self):
        """Test that x-partner-id header is added when partnerId is in config."""
        from zscaler.request_executor import RequestExecutor
        from zscaler.cache.no_op_cache import NoOpCache
        
        config = {
            "client": {
                "requestTimeout": 240,
                "rateLimit": {"maxRetries": 2},
                "cloud": "production",
                "service": "zia",
                "partnerId": "542585sdsdw"
            }
        }
        
        cache = NoOpCache()
        executor = RequestExecutor(config, cache)
        
        # Check that header is in default headers
        default_headers = executor.get_default_headers()
        assert "x-partner-id" in default_headers
        assert default_headers["x-partner-id"] == "542585sdsdw"

    def test_partner_id_header_not_added_when_not_provided(self):
        """Test that x-partner-id header is NOT added when partnerId is not in config."""
        from zscaler.request_executor import RequestExecutor
        from zscaler.cache.no_op_cache import NoOpCache
        
        config = {
            "client": {
                "requestTimeout": 240,
                "rateLimit": {"maxRetries": 2},
                "cloud": "production",
                "service": "zia"
            }
        }
        
        cache = NoOpCache()
        executor = RequestExecutor(config, cache)
        
        # Check that header is NOT in default headers
        default_headers = executor.get_default_headers()
        assert "x-partner-id" not in default_headers

    def test_partner_id_header_value_matches_config(self):
        """Test that x-partner-id header value matches the partnerId from config."""
        from zscaler.request_executor import RequestExecutor
        from zscaler.cache.no_op_cache import NoOpCache
        
        partner_id = "test-partner-id-12345"
        config = {
            "client": {
                "requestTimeout": 240,
                "rateLimit": {"maxRetries": 2},
                "cloud": "production",
                "service": "zia",
                "partnerId": partner_id
            }
        }
        
        cache = NoOpCache()
        executor = RequestExecutor(config, cache)
        
        # Check that header value matches
        default_headers = executor.get_default_headers()
        assert default_headers["x-partner-id"] == partner_id

    def test_partner_id_header_in_prepared_headers(self):
        """Test that x-partner-id header is included in prepared headers."""
        from zscaler.request_executor import RequestExecutor
        from zscaler.cache.no_op_cache import NoOpCache
        from unittest.mock import Mock, patch
        
        config = {
            "client": {
                "requestTimeout": 240,
                "rateLimit": {"maxRetries": 2},
                "cloud": "production",
                "service": "zia",
                "partnerId": "test-partner-123"
            }
        }
        
        cache = NoOpCache()
        executor = RequestExecutor(config, cache)
        
        # Mock OAuth to avoid authentication issues
        mock_oauth = Mock()
        mock_oauth._get_access_token.return_value = "mock-token"
        with patch.object(executor, '_oauth', mock_oauth):
            headers = executor._prepare_headers({}, "/zia/api/v1/test")
            
            assert "x-partner-id" in headers
            assert headers["x-partner-id"] == "test-partner-123"

