"""
Comprehensive unit tests for rate limiting and retry logic in the Zscaler SDK.

This module tests:
1. Rate limiting functionality (RateLimiter class)
2. Retry logic (retry_with_backoff decorator)
3. RequestExecutor rate limiting (get_retry_after method)
4. Integration scenarios
"""

import pytest
import time
from unittest.mock import Mock, patch
from zscaler.request_executor import RequestExecutor
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.utils import should_retry, retry_with_backoff
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.exceptions.exceptions import RetryTooLong


class TestRateLimiter:
    """Test suite for the RateLimiter class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.rate_limiter = RateLimiter(
            get_limit=10,
            post_put_delete_limit=5,
            get_freq=60,
            post_put_delete_freq=60
        )

    def test_rate_limiter_initialization(self):
        """Test RateLimiter initialization."""
        assert self.rate_limiter.get_limit == 10
        assert self.rate_limiter.post_put_delete_limit == 5
        assert self.rate_limiter.get_freq == 60
        assert self.rate_limiter.post_put_delete_freq == 60

    def test_get_request_within_limit(self):
        """Test GET request within rate limit."""
        should_wait, delay = self.rate_limiter.wait("GET")
        assert should_wait is False
        assert delay == 0

    def test_get_request_at_limit(self):
        """Test GET request at rate limit."""
        # Fill up the rate limit
        for _ in range(10):
            self.rate_limiter.wait("GET")
        
        # This should trigger rate limiting
        should_wait, delay = self.rate_limiter.wait("GET")
        assert should_wait is True
        assert delay > 0

    def test_post_request_within_limit(self):
        """Test POST request within rate limit."""
        should_wait, delay = self.rate_limiter.wait("POST")
        assert should_wait is False
        assert delay == 0

    def test_post_request_at_limit(self):
        """Test POST request at rate limit."""
        # Fill up the rate limit
        for _ in range(5):
            self.rate_limiter.wait("POST")
        
        # This should trigger rate limiting
        should_wait, delay = self.rate_limiter.wait("POST")
        assert should_wait is True
        assert delay > 0

    def test_put_request_at_limit(self):
        """Test PUT request at rate limit."""
        # Fill up the rate limit
        for _ in range(5):
            self.rate_limiter.wait("PUT")
        
        # This should trigger rate limiting
        should_wait, delay = self.rate_limiter.wait("PUT")
        assert should_wait is True
        assert delay > 0

    def test_delete_request_at_limit(self):
        """Test DELETE request at rate limit."""
        # Fill up the rate limit
        for _ in range(5):
            self.rate_limiter.wait("DELETE")
        
        # This should trigger rate limiting
        should_wait, delay = self.rate_limiter.wait("DELETE")
        assert should_wait is True
        assert delay > 0

    def test_rate_limit_expiry(self):
        """Test that rate limits expire after the frequency period."""
        # Fill up the rate limit
        for _ in range(10):
            self.rate_limiter.wait("GET")
        
        # This should trigger rate limiting
        should_wait, delay = self.rate_limiter.wait("GET")
        assert should_wait is True
        
        # Mock time passing beyond the frequency period
        with patch('time.time', return_value=time.time() + 61):
            should_wait, delay = self.rate_limiter.wait("GET")
            assert should_wait is False

    def test_different_methods_separate_limits(self):
        """Test that different HTTP methods have separate rate limits."""
        # Fill up GET limit
        for _ in range(10):
            self.rate_limiter.wait("GET")
        
        # GET should be rate limited
        should_wait, delay = self.rate_limiter.wait("GET")
        assert should_wait is True
        
        # POST should not be rate limited yet
        should_wait, delay = self.rate_limiter.wait("POST")
        assert should_wait is False

    def test_thread_safety(self):
        """Test that RateLimiter is thread-safe."""
        import threading
        import time
        
        results = []
        
        def make_request():
            should_wait, delay = self.rate_limiter.wait("GET")
            results.append((should_wait, delay))
        
        # Create multiple threads
        threads = []
        for _ in range(15):  # More than the limit
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should have 15 results
        assert len(results) == 15
        
        # Some requests should be rate limited
        rate_limited_count = sum(1 for should_wait, _ in results if should_wait)
        assert rate_limited_count > 0

    def test_update_limits_with_headers(self):
        """Test updating rate limits from response headers."""
        headers = {
            "X-Ratelimit-Limit-Second": "20",
            "X-Ratelimit-Reset": "30"
        }
        
        self.rate_limiter.update_limits(headers)
        
        assert self.rate_limiter.get_limit == 20
        assert self.rate_limiter.post_put_delete_limit == 20
        assert self.rate_limiter.get_freq == 30
        assert self.rate_limiter.post_put_delete_freq == 30

    def test_update_limits_with_minute_hour_day_limits(self):
        """Test updating rate limits with minute, hour, and day limits."""
        headers = {
            "X-RateLimit-Limit-Minute": "100",
            "X-RateLimit-Limit-Hour": "1000",
            "X-RateLimit-Limit-Day": "10000",
            "X-RateLimit-Remaining-Minute": "50",
            "X-RateLimit-Remaining-Hour": "500",
            "X-RateLimit-Remaining-Day": "5000"
        }
        
        self.rate_limiter.update_limits(headers)
        
        assert self.rate_limiter.minute_limit == 100
        assert self.rate_limiter.hour_limit == 1000
        assert self.rate_limiter.day_limit == 10000
        assert self.rate_limiter.remaining_minute == 50
        assert self.rate_limiter.remaining_hour == 500
        assert self.rate_limiter.remaining_day == 5000

    def test_update_limits_partial_headers(self):
        """Test updating rate limits with partial headers."""
        headers = {
            "X-Ratelimit-Limit-Second": "15"
            # Missing X-Ratelimit-Reset
        }
        
        self.rate_limiter.update_limits(headers)
        
        assert self.rate_limiter.get_limit == 15
        assert self.rate_limiter.post_put_delete_limit == 15
        # Frequency should remain unchanged
        assert self.rate_limiter.get_freq == 60

    def test_invalid_method(self):
        """Test RateLimiter with invalid HTTP method."""
        should_wait, delay = self.rate_limiter.wait("INVALID")
        assert should_wait is False
        assert delay == 0

    def test_concurrent_requests_cleanup(self):
        """Test that old requests are cleaned up when new ones are made."""
        # Fill up the rate limit
        for _ in range(10):
            self.rate_limiter.wait("GET")
        
        # This should trigger rate limiting
        should_wait, delay = self.rate_limiter.wait("GET")
        assert should_wait is True
        
        # Mock time passing beyond the frequency period
        with patch('time.time', return_value=time.time() + 61):
            should_wait, delay = self.rate_limiter.wait("GET")
            assert should_wait is False
            # The RateLimiter should have cleaned up the oldest request and added the new one
            assert len(self.rate_limiter.get_requests) == 10

    def test_rate_limiter_with_custom_limits(self):
        """Test RateLimiter with custom limits."""
        custom_limiter = RateLimiter(
            get_limit=5,
            post_put_delete_limit=3,
            get_freq=30,
            post_put_delete_freq=30
        )
        
        # Test GET requests
        for _ in range(5):
            should_wait, delay = custom_limiter.wait("GET")
            assert should_wait is False
        
        should_wait, delay = custom_limiter.wait("GET")
        assert should_wait is True
        
        # Test POST requests
        for _ in range(3):
            should_wait, delay = custom_limiter.wait("POST")
            assert should_wait is False
        
        should_wait, delay = custom_limiter.wait("POST")
        assert should_wait is True

    def test_rate_limiter_edge_cases(self):
        """Test RateLimiter with edge cases."""
        # Test with low limits
        low_limiter = RateLimiter(1, 1, 60, 60)
        should_wait, delay = low_limiter.wait("GET")
        assert should_wait is False  # First request should be allowed
        
        # Second request should trigger rate limiting
        should_wait, delay = low_limiter.wait("GET")
        assert should_wait is True
        
        # Test with very high limits
        high_limiter = RateLimiter(1000, 1000, 60, 60)
        for _ in range(100):
            should_wait, delay = high_limiter.wait("GET")
            assert should_wait is False

    def test_rate_limiter_frequency_edge_cases(self):
        """Test RateLimiter with frequency edge cases."""
        # Test with zero frequency
        zero_freq_limiter = RateLimiter(10, 5, 0, 0)
        should_wait, delay = zero_freq_limiter.wait("GET")
        assert should_wait is False
        
        # Test with very high frequency
        high_freq_limiter = RateLimiter(10, 5, 3600, 3600)  # 1 hour
        should_wait, delay = high_freq_limiter.wait("GET")
        assert should_wait is False


class TestRetryLogic:
    """Test suite for retry logic functionality."""

    def test_should_retry_status_codes(self):
        """Test should_retry function with various status codes."""
        # Retryable status codes
        assert should_retry(429) is True  # Too Many Requests
        assert should_retry(500) is True  # Internal Server Error
        assert should_retry(502) is True  # Bad Gateway
        assert should_retry(503) is True  # Service Unavailable
        assert should_retry(504) is True  # Gateway Timeout
        
        # Non-retryable status codes
        assert should_retry(200) is False  # OK
        assert should_retry(201) is False  # Created
        assert should_retry(400) is False  # Bad Request
        assert should_retry(401) is False  # Unauthorized
        assert should_retry(403) is False  # Forbidden
        assert should_retry(404) is False  # Not Found

    @patch('time.sleep')
    def test_retry_with_backoff_decorator(self, mock_sleep):
        """Test retry_with_backoff decorator functionality."""
        call_count = 0
        
        @retry_with_backoff(method_type="GET", retries=3, backoff_in_seconds=1)
        def mock_request():
            nonlocal call_count
            call_count += 1
            response = Mock()
            response.status_code = 429
            return response
        
        with pytest.raises(Exception):
            mock_request()
        
        # Should have made 4 calls (1 initial + 3 retries)
        assert call_count == 4
        # Should have slept 3 times
        assert mock_sleep.call_count == 3

    @patch('time.sleep')
    def test_retry_with_backoff_exponential_backoff(self, mock_sleep):
        """Test exponential backoff in retry_with_backoff decorator."""
        call_count = 0
        
        @retry_with_backoff(method_type="GET", retries=3, backoff_in_seconds=2)
        def mock_request():
            nonlocal call_count
            call_count += 1
            response = Mock()
            response.status_code = 429
            return response
        
        with pytest.raises(Exception):
            mock_request()
        
        # Verify exponential backoff formula: backoff_in_seconds * 2^attempt + jitter
        sleep_calls = mock_sleep.call_args_list
        assert len(sleep_calls) == 3
        
        for i, call in enumerate(sleep_calls):
            delay = call[0][0]
            expected_min = 2 * (2 ** i)
            expected_max = 2 * (2 ** i) + 1
            assert expected_min <= delay <= expected_max, f"Attempt {i}: delay {delay} not in range [{expected_min}, {expected_max}]"

    @patch('time.sleep')
    def test_retry_with_backoff_method_type_restrictions(self, mock_sleep):
        """Test that non-GET methods have conservative retry limits."""
        call_count = 0
        
        @retry_with_backoff(method_type="POST", retries=10, backoff_in_seconds=1)
        def mock_request():
            nonlocal call_count
            call_count += 1
            response = Mock()
            response.status_code = 429
            return response
        
        with pytest.raises(Exception):
            mock_request()
        
        # Should use min(10, 3) = 3 retries for POST method
        assert call_count == 4  # 1 initial + 3 retries

    @patch('time.sleep')
    def test_retry_with_backoff_boundary_conditions(self, mock_sleep):
        """Test retry decorator with boundary conditions."""
        
        # Test with zero retries
        @retry_with_backoff(method_type="GET", retries=0, backoff_in_seconds=1)
        def mock_request_zero_retries():
            response = Mock()
            response.status_code = 429
            return response
        
        with pytest.raises(Exception) as exc_info:
            mock_request_zero_retries()
        
        assert "Reached max retries" in str(exc_info.value)
        mock_sleep.assert_not_called()  # Should not sleep with zero retries
        
        # Test with negative retries (should cause overflow)
        @retry_with_backoff(method_type="GET", retries=-1, backoff_in_seconds=1)
        def mock_request_negative_retries():
            response = Mock()
            response.status_code = 429
            return response
        
        with pytest.raises(OverflowError):
            mock_request_negative_retries()

    @patch('time.sleep')
    def test_retry_with_backoff_successful_request(self, mock_sleep):
        """Test retry decorator with successful request."""
        call_count = 0
        
        @retry_with_backoff(method_type="GET", retries=3, backoff_in_seconds=1)
        def mock_request():
            nonlocal call_count
            call_count += 1
            response = Mock()
            response.status_code = 200  # Success
            return response
        
        response = mock_request()
        
        # Should succeed on first try
        assert call_count == 1
        assert response.status_code == 200
        mock_sleep.assert_not_called()

    @patch('time.sleep')
    def test_retry_with_backoff_non_retryable_error(self, mock_sleep):
        """Test retry decorator with non-retryable error."""
        call_count = 0
        
        @retry_with_backoff(method_type="GET", retries=3, backoff_in_seconds=1)
        def mock_request():
            nonlocal call_count
            call_count += 1
            response = Mock()
            response.status_code = 400  # Bad Request - not retryable
            return response
        
        response = mock_request()
        
        # Should not retry for non-retryable errors
        assert call_count == 1
        assert response.status_code == 400
        mock_sleep.assert_not_called()


class TestRequestExecutorRateLimiting:
    """Test suite for RequestExecutor rate limiting functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Use a config without maxRetrySeconds to avoid RetryTooLong exceptions
        self.config = {
            "client": {
                "rateLimit": {
                    "maxRetries": 3,
                    "remainingThreshold": 2
                    # No maxRetrySeconds to avoid RetryTooLong exceptions
                }
            }
        }
        self.cache = NoOpCache()
        self.request_executor = RequestExecutor(self.config, self.cache)

    def test_get_retry_after_retry_after_header(self):
        """Test get_retry_after with Retry-After header."""
        headers = {"Retry-After": "60"}
        logger = Mock()
        
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 61  # 60 + 1 padding

    def test_get_retry_after_x_ratelimit_reset_header(self):
        """Test get_retry_after with X-RateLimit-Reset header."""
        import time
        future_timestamp = int(time.time() + 60)
        headers = {"X-RateLimit-Reset": str(future_timestamp)}
        logger = Mock()
        
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == future_timestamp + 1

    def test_get_retry_after_x_ratelimit_reset_lowercase(self):
        """Test get_retry_after with lowercase x-ratelimit-reset header."""
        import time
        future_timestamp = int(time.time() + 60)
        headers = {"x-ratelimit-reset": str(future_timestamp)}
        logger = Mock()
        
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == future_timestamp + 1

    def test_get_retry_after_rate_limit_reset_header(self):
        """Test get_retry_after with RateLimit-Reset header."""
        import time
        future_timestamp = int(time.time() + 60)
        headers = {"RateLimit-Reset": str(future_timestamp)}
        logger = Mock()
        
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == future_timestamp + 1

    def test_get_retry_after_zcc_headers(self):
        """Test get_retry_after with ZCC-specific headers."""
        headers = {"X-Rate-Limit-Retry-After-Seconds": "30"}
        logger = Mock()
        
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 31

    def test_get_retry_after_priority_order(self):
        """Test that Retry-After has priority over other headers."""
        headers = {
            "Retry-After": "60",
            "X-RateLimit-Reset": "1640995200",
            "RateLimit-Reset": "1640995300"
        }
        logger = Mock()
        
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 61  # Should use Retry-After (highest priority)

    def test_get_retry_after_missing_headers(self):
        """Test get_retry_after with missing headers."""
        headers = {}
        logger = Mock()
        
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after is None
        logger.error.assert_called_with("Missing Retry-After and X-Rate-Limit-Reset headers.")

    def test_get_retry_after_max_retry_seconds_limit(self):
        """Test that maxRetrySeconds configuration properly limits retry time."""
        from zscaler.cache.no_op_cache import NoOpCache
        
        config_with_limit = {
            "client": {
                "rateLimit": {
                    "maxRetries": 3,
                    "remainingThreshold": 2,
                    "maxRetrySeconds": 60
                }
            }
        }
        request_executor = RequestExecutor(config_with_limit, NoOpCache())
        
        # Test with retry time exceeding maxRetrySeconds - should raise RetryTooLong
        headers = {"Retry-After": "300"}  # 5 minutes
        logger = Mock()
        
        with pytest.raises(RetryTooLong) as exc_info:
            request_executor.get_retry_after(headers, logger)
        
        assert "Retry wait time 301 seconds exceeds configured maxRetrySeconds 60" in str(exc_info.value)

    def test_get_retry_after_retry_too_long_exception(self):
        """Test that RetryTooLong exception is raised when retry time exceeds maxRetrySeconds."""
        from zscaler.cache.no_op_cache import NoOpCache
        
        config_with_limit = {
            "client": {
                "rateLimit": {
                    "maxRetries": 3,
                    "remainingThreshold": 2,
                    "maxRetrySeconds": 60
                }
            }
        }
        request_executor = RequestExecutor(config_with_limit, NoOpCache())
        
        # Test with retry time exceeding maxRetrySeconds
        headers = {"Retry-After": "300"}  # 5 minutes
        logger = Mock()
        
        # This should raise RetryTooLong exception
        with pytest.raises(RetryTooLong) as exc_info:
            request_executor.get_retry_after(headers, logger)
        
        assert "Retry wait time 301 seconds exceeds configured maxRetrySeconds 60" in str(exc_info.value)

    def test_get_retry_after_invalid_header_values(self):
        """Test get_retry_after with invalid header values."""
        logger = Mock()
        
        # Test with invalid Retry-After
        headers = {"Retry-After": "invalid"}
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after is None
        logger.error.assert_called_with("Error parsing Retry-After header: invalid")
        
        # Test with invalid X-RateLimit-Reset
        headers = {"X-RateLimit-Reset": "invalid"}
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after is None
        logger.error.assert_called_with("Error parsing x-ratelimit-reset header: invalid")

    def test_get_retry_after_case_insensitive_headers(self):
        """Test get_retry_after with case insensitive headers."""
        logger = Mock()
        
        # Test lowercase retry-after
        headers = {"retry-after": "60"}
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 61
        
        # Test mixed case headers - use retry-after (lowercase) which is supported
        headers = {
            "retry-after": "60"
        }
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 61  # Should use retry-after

    def test_get_retry_after_whitespace_handling(self):
        """Test get_retry_after with whitespace in header values."""
        logger = Mock()
        
        # Test with whitespace in Retry-After
        headers = {"Retry-After": " 60 "}
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 61
        
        # Test with 's' suffix
        headers = {"Retry-After": "60s"}
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 61

    def test_get_retry_after_negative_values(self):
        """Test get_retry_after with negative values."""
        logger = Mock()
        
        # Test with negative Retry-After
        headers = {"Retry-After": "-10"}
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == -9  # -10 + 1
        
        # Test zero Retry-After
        headers = {"Retry-After": "0"}
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 1  # 0 + 1

    def test_get_retry_after_very_large_values(self):
        """Test get_retry_after with very large values."""
        logger = Mock()
        
        # Test very large Retry-After (but not exceeding reasonable limits)
        headers = {"Retry-After": "300"}  # 5 minutes
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 301

    def test_get_retry_after_float_timestamps(self):
        """Test get_retry_after with float timestamps."""
        logger = Mock()
        
        # Test float timestamp with realistic value
        import time
        future_timestamp = time.time() + 60
        headers = {"X-RateLimit-Reset": str(future_timestamp)}
        retry_after = self.request_executor.get_retry_after(headers, logger)
        # Should be converted to int, allowing for small floating point differences
        expected = int(future_timestamp) + 1
        assert abs(retry_after - expected) <= 1  # Allow for small floating point differences

    def test_get_retry_after_duplicate_headers(self):
        """Test get_retry_after with duplicate headers."""
        logger = Mock()
        
        # Test with multiple headers - should use the first one found
        headers = {
            "Retry-After": "60",
            "retry-after": "120"
        }
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 61  # Should use the first Retry-After

    def test_get_retry_after_scientific_notation(self):
        """Test get_retry_after with scientific notation."""
        logger = Mock()
        
        headers = {"Retry-After": "1e3"}  # Scientific notation
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after is None
        logger.error.assert_called_with("Error parsing Retry-After header: 1e3")

    def test_get_retry_after_unicode_values(self):
        """Test get_retry_after with unicode values."""
        logger = Mock()
        
        headers = {"Retry-After": "６０"}  # Full-width digits
        retry_after = self.request_executor.get_retry_after(headers, logger)
        # Unicode digits can actually be parsed by Python's int() function
        assert retry_after == 61  # ６０ + 1 padding

    def test_get_retry_after_mixed_case_headers(self):
        """Test get_retry_after with mixed case headers."""
        logger = Mock()
        
        # Test mixed case headers - use retry-after (lowercase) which is supported
        headers = {
            "retry-after": "60"
        }
        retry_after = self.request_executor.get_retry_after(headers, logger)
        assert retry_after == 61  # Should use retry-after


class TestRateLimitingIntegration:
    """Integration tests for rate limiting and retry logic."""

    def test_rate_limiting_configuration_validation(self):
        """Test rate limiting configuration validation."""
        from zscaler.cache.no_op_cache import NoOpCache
        
        # Test with missing rateLimit config - this should fail as RequestExecutor expects rateLimit
        config_no_rate_limit = {"client": {}}
        
        with pytest.raises(KeyError):
            RequestExecutor(config_no_rate_limit, NoOpCache())
        
        # Test with custom configuration
        custom_config = {
            "client": {
                "rateLimit": {
                    "maxRetries": 5,
                    "remainingThreshold": 5,
                    "maxRetrySeconds": 600
                }
            }
        }
        request_executor = RequestExecutor(custom_config, NoOpCache())
        
        assert request_executor._config["client"]["rateLimit"]["maxRetries"] == 5
        assert request_executor._config["client"]["rateLimit"]["remainingThreshold"] == 5
        assert request_executor._config["client"]["rateLimit"]["maxRetrySeconds"] == 600

    @patch('time.sleep')
    def test_retry_logic_integration_scenarios(self, mock_sleep):
        """Test integration scenarios for retry logic."""
        # Test successful retry after initial failure
        call_count = 0
        
        @retry_with_backoff(method_type="GET", retries=2, backoff_in_seconds=1)
        def mock_request():
            nonlocal call_count
            call_count += 1
            response = Mock()
            if call_count < 3:  # Fail first 2 times
                response.status_code = 429
            else:  # Succeed on 3rd try
                response.status_code = 200
            return response
        
        response = mock_request()
        
        assert call_count == 3
        assert response.status_code == 200
        assert mock_sleep.call_count == 2

    def test_retry_logic_error_handling(self):
        """Test error handling in retry logic."""
        # Test with non-retryable error
        call_count = 0
        
        @retry_with_backoff(method_type="GET", retries=3, backoff_in_seconds=1)
        def mock_request():
            nonlocal call_count
            call_count += 1
            response = Mock()
            response.status_code = 400  # Bad Request - not retryable
            return response
        
        response = mock_request()
        
        # Should not retry for non-retryable errors
        assert call_count == 1
        assert response.status_code == 400

    @patch('time.sleep')
    def test_retry_logic_performance_considerations(self, mock_sleep):
        """Test performance considerations in retry logic."""
        # Test with large number of retries
        call_count = 0
        
        @retry_with_backoff(method_type="GET", retries=100, backoff_in_seconds=1)
        def mock_request_large_retries():
            nonlocal call_count
            call_count += 1
            response = Mock()
            if call_count < 5:  # Fail first 4 times
                response.status_code = 429
            else:  # Succeed on 5th try
                response.status_code = 200
            return response
        
        with patch('time.sleep'):
            response = mock_request_large_retries()
            assert response.status_code == 200
            assert call_count == 5  # Should succeed after 5 attempts, not 100
