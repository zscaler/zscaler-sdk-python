"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import os
import pytest
from zscaler.oneapi_client import LegacyZGuardClient
from tests.test_utils import reset_vcr_counters

PYTEST_MOCK_CLIENT = "pytest_mock_client"


@pytest.fixture(autouse=True, scope="function")
def reset_counters_per_test():
    """
    Reset VCR counters before each test function.
    
    This ensures that generate_random_string() and generate_random_ip()
    return the same deterministic values during both recording and playback.
    Each test starts with counter at 0, so the same sequence is generated.
    """
    reset_vcr_counters()
    yield


class NameGenerator:
    """
    Generates deterministic test names for VCR-based testing.
    
    Instead of using random names (which break VCR playback), this class
    provides consistent, predictable names that work with recorded cassettes.
    
    Usage:
        names = NameGenerator("policy_detection")
        name = names.name       # "tests-policy-detection"
        desc = names.description  # "Test Policy Detection"
    """
    
    def __init__(self, resource_type: str, suffix: str = ""):
        """
        Initialize with a resource type identifier.
        
        Args:
            resource_type: A descriptive string for the resource (e.g., "policy_detection")
            suffix: Optional suffix for uniqueness (e.g., "1", "alt")
        """
        self.resource_type = resource_type.lower().replace("_", "-")
        self.suffix = f"-{suffix}" if suffix else ""
        
    @property
    def name(self) -> str:
        """Returns the base test name."""
        return f"tests-{self.resource_type}{self.suffix}"
    
    @property
    def description(self) -> str:
        """Returns a human-readable description."""
        readable = self.resource_type.replace("-", " ").title()
        return f"Test {readable}{self.suffix}"
    
    @property
    def updated_name(self) -> str:
        """Returns the name for update operations."""
        return f"tests-{self.resource_type}{self.suffix}-updated"
    
    @property
    def updated_description(self) -> str:
        """Returns the description for update operations."""
        readable = self.resource_type.replace("-", " ").title()
        return f"Updated Test {readable}{self.suffix}"
    
    def with_suffix(self, suffix: str) -> "NameGenerator":
        """Returns a new generator with an additional suffix."""
        new_suffix = f"{self.suffix.lstrip('-')}-{suffix}" if self.suffix else suffix
        return NameGenerator(self.resource_type, new_suffix)


@pytest.fixture(scope="function")
def zguard_client():
    return MockZGuardClient()


class MockZGuardClient(LegacyZGuardClient):
    def __init__(self, config=None):
        """
        Initialize the MockZGuardClient with support for environment variables and
        optional inline config.

        Args:
            config: Optional dictionary containing client configuration (api_key, cloud, etc.).
        """
        # If config is not provided, initialize it as an empty dictionary
        config = config or {}

        # Check if we're in VCR playback mode (MOCK_TESTS=true means use cassettes)
        mock_tests = os.getenv("MOCK_TESTS", "true").strip().lower() != "false"

        # Fetch credentials from environment variables, allowing them to be overridden by the config dictionary
        # In playback mode (MOCK_TESTS=true), use dummy credentials if not provided
        api_key = config.get("api_key", os.getenv("AIGUARD_API_KEY"))
        cloud = config.get("cloud", os.getenv("AIGUARD_CLOUD", "us1"))

        # In VCR playback mode, use dummy credentials if real ones aren't provided
        if mock_tests:
            api_key = api_key or "dummy_api_key_for_testing"

        # Extract logging configuration or use defaults
        logging_config = config.get("logging", {"enabled": False, "verbose": False})

        # Set up the client config dictionary
        client_config = {
            "api_key": api_key,
            "cloud": cloud,
            "timeout": config.get("timeout", 30),
            "auto_retry_on_rate_limit": config.get("auto_retry_on_rate_limit", True),
            "max_rate_limit_retries": config.get("max_rate_limit_retries", 3),
            "logging": {"enabled": logging_config.get("enabled", True), "verbose": logging_config.get("verbose", True)},
        }

        # Initialize the client
        super().__init__(client_config)
    
    def get_rate_limit_stats(self):
        """Expose rate limit stats from the legacy client helper."""
        if hasattr(self, '_request_executor') and hasattr(self._request_executor, 'zguard_legacy_client'):
            return self._request_executor.zguard_legacy_client.get_rate_limit_stats()
        return {"total_throttles": 0, "request_count_throttles": 0, "content_size_throttles": 0, "currently_limited": False}
    
    def reset_rate_limit_stats(self):
        """Reset rate limit stats from the legacy client helper."""
        if hasattr(self, '_request_executor') and hasattr(self._request_executor, 'zguard_legacy_client'):
            self._request_executor.zguard_legacy_client.reset_rate_limit_stats()
    
    def clear_rate_limits(self):
        """Clear rate limits from the legacy client helper."""
        if hasattr(self, '_request_executor') and hasattr(self._request_executor, 'zguard_legacy_client'):
            self._request_executor.zguard_legacy_client.clear_rate_limits()
