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
from unittest.mock import Mock, MagicMock


@pytest.fixture
def fs():
    yield


class TestPolicyDetectionUnit:
    """Unit Tests for the AIGuard Policy Detection API to increase coverage"""

    def test_execute_policy_request_error(self, fs):
        """Test execute_policy handles request creation errors correctly"""
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        policy_api = PolicyDetectionAPI(mock_executor)
        result, response, err = policy_api.execute_policy(
            content="test",
            direction="IN"
        )
        
        assert result is None
        assert err is not None

    def test_execute_policy_execute_error(self, fs):
        """Test execute_policy handles execution errors correctly"""
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        policy_api = PolicyDetectionAPI(mock_executor)
        result, response, err = policy_api.execute_policy(
            content="test",
            direction="IN"
        )
        
        assert result is None
        assert err is not None

    def test_execute_policy_parsing_error(self, fs):
        """Test execute_policy handles parsing errors correctly"""
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        policy_api = PolicyDetectionAPI(mock_executor)
        result, response, err = policy_api.execute_policy(
            content="test",
            direction="IN"
        )
        
        assert result is None
        assert err is not None

    def test_resolve_and_execute_policy_request_error(self, fs):
        """Test resolve_and_execute_policy handles request creation errors correctly"""
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        policy_api = PolicyDetectionAPI(mock_executor)
        result, response, err = policy_api.resolve_and_execute_policy(
            content="test",
            direction="IN"
        )
        
        assert result is None
        assert err is not None

    def test_resolve_and_execute_policy_execute_error(self, fs):
        """Test resolve_and_execute_policy handles execution errors correctly"""
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        policy_api = PolicyDetectionAPI(mock_executor)
        result, response, err = policy_api.resolve_and_execute_policy(
            content="test",
            direction="IN"
        )
        
        assert result is None
        assert err is not None

    def test_resolve_and_execute_policy_parsing_error(self, fs):
        """Test resolve_and_execute_policy handles parsing errors correctly"""
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        policy_api = PolicyDetectionAPI(mock_executor)
        result, response, err = policy_api.resolve_and_execute_policy(
            content="test",
            direction="IN"
        )
        
        assert result is None
        assert err is not None


class TestModelsUnit:
    """Unit Tests for AIGuard models"""

    def test_content_hash_creation(self, fs):
        """Test ContentHash model creation"""
        from zscaler.zaiguard.models.policy_detection import ContentHash
        
        # Test with data
        hash_obj = ContentHash({"hashType": "SHA256", "hashValue": "abc123"})
        assert hash_obj.hash_type == "SHA256"
        assert hash_obj.hash_value == "abc123"
        
        # Test without data
        empty_hash = ContentHash()
        assert empty_hash.hash_type is None
        assert empty_hash.hash_value is None
        
        # Test request_format
        format_dict = hash_obj.request_format()
        assert format_dict["hashType"] == "SHA256"
        assert format_dict["hashValue"] == "abc123"

    def test_detector_response_creation(self, fs):
        """Test DetectorResponse model creation"""
        from zscaler.zaiguard.models.policy_detection import DetectorResponse
        
        # Test with full data
        detector = DetectorResponse({
            "statusCode": 200,
            "errorMsg": None,
            "triggered": True,
            "action": "BLOCK",
            "latency": 150,
            "deviceType": "test",
            "details": {"key": "value"},
            "severity": "HIGH",
            "contentHash": {"hashType": "SHA256", "hashValue": "xyz"}
        })
        
        assert detector.status_code == 200
        assert detector.triggered is True
        assert detector.action == "BLOCK"
        assert detector.severity == "HIGH"
        assert detector.content_hash is not None
        assert detector.content_hash.hash_type == "SHA256"
        
        # Test without data
        empty_detector = DetectorResponse()
        assert empty_detector.triggered is None
        assert empty_detector.action is None

    def test_rate_limit_throttling_detail_creation(self, fs):
        """Test RateLimitThrottlingDetail model creation"""
        from zscaler.zaiguard.models.policy_detection import RateLimitThrottlingDetail
        
        # Test with data
        throttle = RateLimitThrottlingDetail({
            "rlcId": 12345,
            "metric": "rq",
            "retryAfterMillis": 5000
        })
        
        assert throttle.rlc_id == 12345
        assert throttle.metric == "rq"
        assert throttle.retry_after_millis == 5000
        
        # Test request_format
        format_dict = throttle.request_format()
        assert format_dict["rlcId"] == 12345
        assert format_dict["metric"] == "rq"
        assert format_dict["retryAfterMillis"] == 5000

    def test_execute_policy_request_creation(self, fs):
        """Test ExecuteDetectionsPolicyRequest model creation"""
        from zscaler.zaiguard.models.policy_detection import ExecuteDetectionsPolicyRequest
        
        # Test with full data
        request_obj = ExecuteDetectionsPolicyRequest({
            "transactionId": "abc-123",
            "content": "test content",
            "direction": "IN",
            "policyId": 12345
        })
        
        assert request_obj.transaction_id == "abc-123"
        assert request_obj.content == "test content"
        assert request_obj.direction == "IN"
        assert request_obj.policy_id == 12345
        
        # Test request_format
        format_dict = request_obj.request_format()
        assert format_dict["transactionId"] == "abc-123"
        assert format_dict["content"] == "test content"

    def test_execute_policy_response_creation(self, fs):
        """Test ExecuteDetectionsPolicyResponse model creation"""
        from zscaler.zaiguard.models.policy_detection import ExecuteDetectionsPolicyResponse
        
        # Test with nested objects
        response_obj = ExecuteDetectionsPolicyResponse({
            "transactionId": "xyz-789",
            "statusCode": 200,
            "action": "ALLOW",
            "severity": "LOW",
            "direction": "OUT",
            "detectorResponses": {
                "detector1": {
                    "statusCode": 200,
                    "triggered": False,
                    "action": "ALLOW"
                }
            },
            "throttlingDetails": [
                {
                    "rlcId": 999,
                    "metric": "rq",
                    "retryAfterMillis": 1000
                }
            ]
        })
        
        assert response_obj.transaction_id == "xyz-789"
        assert response_obj.action == "ALLOW"
        assert "detector1" in response_obj.detector_responses
        assert len(response_obj.throttling_details) == 1
        assert response_obj.throttling_details[0].metric == "rq"

    def test_resolve_and_execute_response_creation(self, fs):
        """Test ResolveAndExecuteDetectionsPolicyResponse model creation"""
        from zscaler.zaiguard.models.policy_detection import ResolveAndExecuteDetectionsPolicyResponse
        
        # Test with policy metadata
        response_obj = ResolveAndExecuteDetectionsPolicyResponse({
            "transactionId": "policy-123",
            "statusCode": 200,
            "action": "DETECT",
            "direction": "IN",
            "policyId": 555,
            "policyName": "Test Policy",
            "policyVersion": "1.0",
            "detectorResponses": {},
            "throttlingDetails": []
        })
        
        assert response_obj.transaction_id == "policy-123"
        assert response_obj.policy_id == 555
        assert response_obj.policy_name == "Test Policy"
        assert response_obj.policy_version == "1.0"
        
        # Test request_format
        format_dict = response_obj.request_format()
        assert format_dict["policyId"] == 555
        assert format_dict["policyName"] == "Test Policy"


class TestZGuardServiceUnit:
    """Unit Tests for the ZGuard Service to increase coverage"""

    def test_zguard_service_properties(self, fs):
        """Test ZGuardService property accessors"""
        from zscaler.zaiguard.zaiguard_service import ZGuardService
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI
        
        mock_executor = Mock()
        
        service = ZGuardService(mock_executor)
        
        # Test that policy_detection property returns correct type
        assert isinstance(service.policy_detection, PolicyDetectionAPI)
        
        # Verify it uses the correct executor
        assert service.policy_detection._request_executor == mock_executor


class TestLegacyClientUnit:
    """Unit Tests for the Legacy AIGuard Client"""

    def test_legacy_client_initialization(self, fs):
        """Test LegacyZGuardClientHelper initialization"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        # Test with API key
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        assert client.api_key == "test_api_key"
        assert client.env_cloud == "us1"
        assert client.url == "https://api.us1.zseclipse.net"
        assert client.auto_retry_on_rate_limit is True
        assert client.max_rate_limit_retries == 3

    def test_legacy_client_missing_api_key(self, fs):
        """Test that missing API key raises ValueError"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        with pytest.raises(ValueError, match="API key is required"):
            LegacyZGuardClientHelper(cloud="us1")

    def test_legacy_client_custom_url(self, fs):
        """Test LegacyZGuardClientHelper with custom override URL"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        custom_url = "https://custom.api.example.com"
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1",
            override_url=custom_url
        )
        
        assert client.url == custom_url

    def test_legacy_client_rate_limit_config(self, fs):
        """Test LegacyZGuardClientHelper rate limit configuration"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1",
            auto_retry_on_rate_limit=False,
            max_rate_limit_retries=5
        )
        
        assert client.auto_retry_on_rate_limit is False
        assert client.max_rate_limit_retries == 5

    def test_get_base_url(self, fs):
        """Test get_base_url method"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        base_url = client.get_base_url()
        assert base_url == "https://api.us1.zseclipse.net"

    def test_get_rate_limit_stats(self, fs):
        """Test get_rate_limit_stats method"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        stats = client.get_rate_limit_stats()
        
        assert isinstance(stats, dict)
        assert "total_throttles" in stats
        assert "request_count_throttles" in stats
        assert "content_size_throttles" in stats
        assert "currently_limited" in stats
        
        # Initial stats should be zero
        assert stats["total_throttles"] == 0
        assert stats["request_count_throttles"] == 0
        assert stats["content_size_throttles"] == 0
        assert stats["currently_limited"] is False

    def test_reset_rate_limit_stats(self, fs):
        """Test reset_rate_limit_stats method"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        # Manually increment counters
        client._total_throttles = 5
        client._rq_throttles = 3
        client._cs_throttles = 2
        
        # Reset stats
        client.reset_rate_limit_stats()
        
        # Verify reset
        stats = client.get_rate_limit_stats()
        assert stats["total_throttles"] == 0
        assert stats["request_count_throttles"] == 0
        assert stats["content_size_throttles"] == 0

    def test_clear_rate_limits(self, fs):
        """Test clear_rate_limits method"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        import time
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        # Set rate limit wait times
        future_time = time.time() + 10
        client._request_count_wait_until = future_time
        client._content_size_wait_until = future_time
        
        # Should be currently limited
        stats_before = client.get_rate_limit_stats()
        assert stats_before["currently_limited"] is True
        
        # Clear limits
        client.clear_rate_limits()
        
        # Should no longer be limited
        stats_after = client.get_rate_limit_stats()
        assert stats_after["currently_limited"] is False
        assert client._request_count_wait_until == 0
        assert client._content_size_wait_until == 0

    def test_handle_throttling_details_rq_metric(self, fs):
        """Test _handle_throttling_details with rq (request count) metric"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        from zscaler.zaiguard.models.policy_detection import RateLimitThrottlingDetail
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1",
            auto_retry_on_rate_limit=False  # Disable auto-retry for testing
        )
        
        throttle = RateLimitThrottlingDetail({
            "rlcId": 123,
            "metric": "rq",
            "retryAfterMillis": 5000
        })
        
        # Handle throttling
        was_throttled = client._handle_throttling_details([throttle])
        
        assert was_throttled is True
        stats = client.get_rate_limit_stats()
        assert stats["total_throttles"] == 1
        assert stats["request_count_throttles"] == 1
        assert stats["content_size_throttles"] == 0

    def test_handle_throttling_details_cs_metric(self, fs):
        """Test _handle_throttling_details with cs (content size) metric"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        from zscaler.zaiguard.models.policy_detection import RateLimitThrottlingDetail
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1",
            auto_retry_on_rate_limit=False
        )
        
        throttle = RateLimitThrottlingDetail({
            "rlcId": 456,
            "metric": "cs",
            "retryAfterMillis": 3000
        })
        
        # Handle throttling
        was_throttled = client._handle_throttling_details([throttle])
        
        assert was_throttled is True
        stats = client.get_rate_limit_stats()
        assert stats["total_throttles"] == 1
        assert stats["request_count_throttles"] == 0
        assert stats["content_size_throttles"] == 1

    def test_handle_throttling_details_multiple(self, fs):
        """Test _handle_throttling_details with multiple throttles"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        from zscaler.zaiguard.models.policy_detection import RateLimitThrottlingDetail
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1",
            auto_retry_on_rate_limit=False
        )
        
        throttles = [
            RateLimitThrottlingDetail({
                "rlcId": 111,
                "metric": "rq",
                "retryAfterMillis": 5000
            }),
            RateLimitThrottlingDetail({
                "rlcId": 222,
                "metric": "cs",
                "retryAfterMillis": 3000
            })
        ]
        
        # Handle throttling
        was_throttled = client._handle_throttling_details(throttles)
        
        assert was_throttled is True
        stats = client.get_rate_limit_stats()
        assert stats["total_throttles"] == 2
        assert stats["request_count_throttles"] == 1
        assert stats["content_size_throttles"] == 1

    def test_handle_throttling_details_empty_list(self, fs):
        """Test _handle_throttling_details with empty list"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        # Handle empty throttling list
        was_throttled = client._handle_throttling_details([])
        
        assert was_throttled is False
        stats = client.get_rate_limit_stats()
        assert stats["total_throttles"] == 0

    def test_set_auth_header(self, fs):
        """Test set_auth_header method"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        import requests
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key_12345",
            cloud="us1"
        )
        
        # Create a test request
        req = requests.Request(method="POST", url="https://api.us1.zseclipse.net/v1/test")
        prepared = req.prepare()
        
        # Set auth header
        prepared = client.set_auth_header(prepared)
        
        # Verify Authorization header
        assert "Authorization" in prepared.headers
        assert prepared.headers["Authorization"] == "Bearer test_api_key_12345"
        
        # Verify other headers
        assert "Content-Type" in prepared.headers or prepared.body is None
        assert "User-Agent" in prepared.headers

    def test_policy_detection_property(self, fs):
        """Test policy_detection property accessor"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        # Access policy_detection property
        policy_api = client.policy_detection
        
        # Verify it returns the correct type
        assert isinstance(policy_api, PolicyDetectionAPI)

    def test_custom_headers_methods(self, fs):
        """Test custom headers management methods"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        # Test that methods exist and can be called
        # (actual functionality tested through request_executor)
        try:
            client.set_custom_headers({"X-Custom": "value"})
            client.get_custom_headers()
            client.get_default_headers()
            client.clear_custom_headers()
        except AttributeError:
            pytest.fail("Custom header methods should be available")


class TestRateLimitingLogic:
    """Unit Tests for rate limiting logic"""

    def test_should_wait_before_request_no_limit(self, fs):
        """Test _should_wait_before_request returns None when no limits active"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        wait_time = client._should_wait_before_request()
        assert wait_time is None

    def test_should_wait_before_request_with_limit(self, fs):
        """Test _should_wait_before_request returns wait time when limited"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        import time
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        # Set a rate limit 2 seconds in the future
        client._request_count_wait_until = time.time() + 2
        
        wait_time = client._should_wait_before_request()
        assert wait_time is not None
        assert wait_time > 0
        assert wait_time <= 2.1  # Allow small margin for execution time

    def test_wait_if_rate_limited(self, fs):
        """Test _wait_if_rate_limited method"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        import time
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        # No rate limit - should not wait
        waited = client._wait_if_rate_limited()
        assert waited is False
        
        # Set a very short rate limit (0.1 seconds)
        client._request_count_wait_until = time.time() + 0.1
        
        start_time = time.time()
        waited = client._wait_if_rate_limited()
        elapsed = time.time() - start_time
        
        assert waited is True
        assert elapsed >= 0.09  # Should have waited at least 0.09 seconds

    def test_thread_safety(self, fs):
        """Test that rate limiting operations are thread-safe"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        from zscaler.zaiguard.models.policy_detection import RateLimitThrottlingDetail
        import threading
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1",
            auto_retry_on_rate_limit=False
        )
        
        def increment_throttles():
            throttle = RateLimitThrottlingDetail({
                "metric": "rq",
                "retryAfterMillis": 100
            })
            client._handle_throttling_details([throttle])
        
        # Run multiple threads incrementing throttles
        threads = [threading.Thread(target=increment_throttles) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Verify all increments were counted (thread-safe)
        stats = client.get_rate_limit_stats()
        assert stats["total_throttles"] == 10

    def test_get_jsessionid(self, fs):
        """Test get_jsessionid returns None for AIGuard"""
        from zscaler.zaiguard.legacy import LegacyZGuardClientHelper
        import requests
        
        client = LegacyZGuardClientHelper(
            api_key="test_api_key",
            cloud="us1"
        )
        
        req = requests.Request(method="GET", url="https://api.us1.zseclipse.net/v1/test")
        prepared = req.prepare()
        
        session_id = client.get_jsessionid(prepared)
        assert session_id is None, "AIGuard should not use JSESSIONID"
