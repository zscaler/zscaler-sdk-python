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

import time
import datetime
from unittest.mock import Mock
from typing import Dict, Any, Optional


class MockRateLimitResponse:
    """Mock response for rate limiting scenarios."""
    
    def __init__(self, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        self.status_code = status_code
        self.headers = headers or {}
        self.text = "{}"
        self.json = lambda: {}
        self.raise_for_status = Mock()


class MockHTTP429Response:
    """Mock 429 Too Many Requests response."""
    
    def __init__(self, retry_after: Optional[str] = None, x_rate_limit_reset: Optional[str] = None):
        self.status_code = 429
        self.headers = {}
        self.text = '{"error": "Rate limit exceeded"}'
        self.json = lambda: {"error": "Rate limit exceeded"}
        self.raise_for_status = Mock(side_effect=Exception("429 Too Many Requests"))
        
        if retry_after:
            self.headers["Retry-After"] = retry_after
        if x_rate_limit_reset:
            self.headers["X-RateLimit-Reset"] = x_rate_limit_reset


class MockHTTP429WithRetryAfter:
    """Mock 429 response with Retry-After header."""
    
    def __init__(self, retry_after_seconds: int = 60):
        self.status_code = 429
        self.headers = {"Retry-After": str(retry_after_seconds)}
        self.text = '{"error": "Rate limit exceeded"}'
        self.json = lambda: {"error": "Rate limit exceeded"}
        self.raise_for_status = Mock(side_effect=Exception("429 Too Many Requests"))


class MockHTTP429WithXRateLimitReset:
    """Mock 429 response with X-RateLimit-Reset header."""
    
    def __init__(self, reset_timestamp: Optional[float] = None):
        if reset_timestamp is None:
            reset_timestamp = time.time() + 60  # 60 seconds from now
        
        self.status_code = 429
        self.headers = {"X-RateLimit-Reset": str(int(reset_timestamp))}
        self.text = '{"error": "Rate limit exceeded"}'
        self.json = lambda: {"error": "Rate limit exceeded"}
        self.raise_for_status = Mock(side_effect=Exception("429 Too Many Requests"))


class MockHTTP429ConcurrentLimit:
    """Mock 429 response indicating concurrent rate limit (ZCC specific)."""
    
    def __init__(self):
        self.status_code = 429
        self.headers = {
            "X-Rate-Limit-Limit": "0",
            "X-Rate-Limit-Remaining": "0",
            "X-Rate-Limit-Retry-After-Seconds": "60"
        }
        self.text = '{"error": "Concurrent rate limit exceeded"}'
        self.json = lambda: {"error": "Concurrent rate limit exceeded"}
        self.raise_for_status = Mock(side_effect=Exception("429 Too Many Requests"))


class MockHTTP429MissingHeaders:
    """Mock 429 response with missing rate limit headers."""
    
    def __init__(self):
        self.status_code = 429
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"error": "Rate limit exceeded"}'
        self.json = lambda: {"error": "Rate limit exceeded"}
        self.raise_for_status = Mock(side_effect=Exception("429 Too Many Requests"))


class MockHTTP429MultipleXReset:
    """Mock 429 response with multiple X-RateLimit-Reset headers."""
    
    def __init__(self):
        now = time.time()
        self.status_code = 429
        self.headers = {
            "X-RateLimit-Reset": f"{int(now + 1)},{int(now + 2)}",  # Multiple values
            "Date": datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        }
        self.text = '{"error": "Rate limit exceeded"}'
        self.json = lambda: {"error": "Rate limit exceeded"}
        self.raise_for_status = Mock(side_effect=Exception("429 Too Many Requests"))


class MockHTTP429InvalidHeaders:
    """Mock 429 response with invalid header values."""
    
    def __init__(self):
        self.status_code = 429
        self.headers = {
            "Retry-After": "invalid",
            "X-RateLimit-Reset": "not_a_number"
        }
        self.text = '{"error": "Rate limit exceeded"}'
        self.json = lambda: {"error": "Rate limit exceeded"}
        self.raise_for_status = Mock(side_effect=Exception("429 Too Many Requests"))


class MockHTTP200Response:
    """Mock successful 200 response."""
    
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        self.status_code = 200
        self.headers = headers or {"Content-Type": "application/json"}
        self.text = '{"data": "success"}'
        self.json = lambda: {"data": "success"}
        self.raise_for_status = Mock()


class MockHTTP500Response:
    """Mock 500 Internal Server Error response."""
    
    def __init__(self):
        self.status_code = 500
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"error": "Internal server error"}'
        self.json = lambda: {"error": "Internal server error"}
        self.raise_for_status = Mock(side_effect=Exception("500 Internal Server Error"))


class MockHTTP503Response:
    """Mock 503 Service Unavailable response."""
    
    def __init__(self):
        self.status_code = 503
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"error": "Service unavailable"}'
        self.json = lambda: {"error": "Service unavailable"}
        self.raise_for_status = Mock(side_effect=Exception("503 Service Unavailable"))


class MockRateLimitApproachingResponse:
    """Mock response indicating rate limit is approaching (proactive backoff)."""
    
    def __init__(self, remaining: int = 1, limit: int = 100):
        self.status_code = 200
        self.headers = {
            "X-Ratelimit-Remaining-Second": str(remaining),
            "X-Ratelimit-Limit-Second": str(limit),
            "Content-Type": "application/json"
        }
        self.text = '{"data": "success"}'
        self.json = lambda: {"data": "success"}
        self.raise_for_status = Mock()


class MockRequestExecutor:
    """Mock RequestExecutor for testing."""
    
    def __init__(self, config: Dict[str, Any]):
        self._config = config
        self._max_retries = config.get("client", {}).get("rateLimit", {}).get("maxRetries", 3)
        self._remaining_threshold = config.get("client", {}).get("rateLimit", {}).get("remainingThreshold", 2)
        self._max_retry_seconds = config.get("client", {}).get("rateLimit", {}).get("maxRetrySeconds", 300)
    
    def get_retry_after(self, headers: Dict[str, str], logger: Mock) -> Optional[int]:
        """Mock implementation of get_retry_after method."""
        retry_limit_reset_header = (
            headers.get("x-ratelimit-reset") or 
            headers.get("X-RateLimit-Reset") or
            headers.get("RateLimit-Reset") or
            headers.get("X-Rate-Limit-Retry-After-Seconds") or
            headers.get("X-Rate-Limit-Remaining")
        )
        retry_after = headers.get("Retry-After") or headers.get("retry-after")

        backoff = None

        if retry_after:
            try:
                backoff = int(retry_after.strip("s")) + 1
            except ValueError:
                logger.error(f"Error parsing Retry-After header: {retry_after}")
                return None

        elif retry_limit_reset_header is not None:
            try:
                backoff = float(retry_limit_reset_header) + 1
            except ValueError:
                logger.error(f"Error parsing x-ratelimit-reset header: {retry_limit_reset_header}")
                return None
        else:
            logger.error("Missing Retry-After and X-Rate-Limit-Reset headers.")
            return None

        # Check against maxRetrySeconds
        if self._max_retry_seconds is not None and backoff > self._max_retry_seconds:
            backoff = self._max_retry_seconds

        return int(backoff)


# Test data constants
TEST_CLIENT_ID = "test_client_id"
TEST_CLIENT_SECRET = "test_client_secret"
TEST_API_TOKEN = "test_api_token"
TEST_ORG_URL = "https://test.zscaler.com"
TEST_CLOUD = "zscaler"

# Default test configuration
DEFAULT_TEST_CONFIG = {
    "client": {
        "rateLimit": {
            "maxRetries": 3,
            "remainingThreshold": 2,
            "maxRetrySeconds": 300
        }
    }
}

class MockHTTP400Response:
    """Mock 400 Bad Request response."""
    
    def __init__(self):
        self.status_code = 400
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"error": "Bad Request"}'
        self.json = lambda: {"error": "Bad Request"}
        self.raise_for_status = Mock(side_effect=Exception("400 Bad Request"))


class MockHTTP401Response:
    """Mock 401 Unauthorized response."""
    
    def __init__(self):
        self.status_code = 401
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"error": "Unauthorized"}'
        self.json = lambda: {"error": "Unauthorized"}
        self.raise_for_status = Mock(side_effect=Exception("401 Unauthorized"))


class MockHTTP403Response:
    """Mock 403 Forbidden response."""
    
    def __init__(self):
        self.status_code = 403
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"error": "Forbidden"}'
        self.json = lambda: {"error": "Forbidden"}
        self.raise_for_status = Mock(side_effect=Exception("403 Forbidden"))


class MockHTTP404Response:
    """Mock 404 Not Found response."""
    
    def __init__(self):
        self.status_code = 404
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"error": "Not Found"}'
        self.json = lambda: {"error": "Not Found"}
        self.raise_for_status = Mock(side_effect=Exception("404 Not Found"))


# Rate limiting test scenarios
RATE_LIMIT_SCENARIOS = {
    "retry_after_60": {"Retry-After": "60"},
    "x_rate_limit_reset": {"X-RateLimit-Reset": str(int(time.time() + 60))},
    "zcc_headers": {"X-Rate-Limit-Retry-After-Seconds": "30"},
    "missing_headers": {},
    "invalid_headers": {"Retry-After": "invalid", "X-RateLimit-Reset": "not_a_number"},
    "multiple_x_reset": {"X-RateLimit-Reset": f"{int(time.time() + 1)},{int(time.time() + 2)}"},
    "concurrent_limit": {
        "X-Rate-Limit-Limit": "0",
        "X-Rate-Limit-Remaining": "0",
        "X-Rate-Limit-Retry-After-Seconds": "60"
    }
}
