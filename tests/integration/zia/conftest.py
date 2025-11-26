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

from zscaler import ZscalerClient
from zscaler.oneapi_client import LegacyZIAClient
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


class TestNameGenerator:
    """
    Generates deterministic test names for VCR-based testing.
    
    Instead of using random names (which break VCR playback), this class
    provides consistent, predictable names that work with recorded cassettes.
    
    Usage:
        names = TestNameGenerator("rule_labels")
        name = names.name       # "tests-rule-labels"
        desc = names.description  # "Test Rule Labels"
        updated_name = names.updated_name  # "tests-rule-labels-updated"
    """
    
    def __init__(self, resource_type: str, suffix: str = ""):
        """
        Initialize with a resource type identifier.
        
        Args:
            resource_type: A descriptive string for the resource (e.g., "firewall_rule", "static_ip")
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
    
    def with_suffix(self, suffix: str) -> "TestNameGenerator":
        """Returns a new generator with an additional suffix."""
        new_suffix = f"{self.suffix.lstrip('-')}-{suffix}" if self.suffix else suffix
        return TestNameGenerator(self.resource_type, new_suffix)
    
    @staticmethod
    def generate_urls(count: int = 5, domain: str = "vcr-test.com") -> list:
        """
        Generate deterministic test URLs for VCR testing.
        
        Args:
            count: Number of URLs to generate
            domain: Domain suffix for the URLs
            
        Returns:
            List of deterministic test URLs
        """
        return [f"vcr-test-url-{i}.{domain}" for i in range(1, count + 1)]
    
    @staticmethod
    def generate_ips(count: int = 5, base: str = "192.168.100") -> list:
        """
        Generate deterministic test IP addresses for VCR testing.
        
        Args:
            count: Number of IPs to generate
            base: First three octets of the IP
            
        Returns:
            List of deterministic test IPs
        """
        return [f"{base}.{i}" for i in range(1, count + 1)]


class MockZIAClient(ZscalerClient):
    def __init__(self, fs, config=None):
        """
        Initialize the MockZIAClient with support for environment variables and
        optional inline config.

        Args:
            fs: Fixture to pause/resume the filesystem mock for pyfakefs.
            config: Optional dictionary containing client configuration (clientId, clientSecret, etc.).
        """
        # If config is not provided, initialize it as an empty dictionary
        config = config or {}

        # Check if we're in VCR playback mode (MOCK_TESTS=true means use cassettes)
        mock_tests = os.getenv("MOCK_TESTS", "true").strip().lower() != "false"

        # Fetch credentials from environment variables, allowing them to be overridden by the config dictionary
        # In playback mode (MOCK_TESTS=true), use dummy credentials if not provided
        clientId = config.get("clientId", os.getenv("ZSCALER_CLIENT_ID"))
        clientSecret = config.get("clientSecret", os.getenv("ZSCALER_CLIENT_SECRET"))
        customerId = config.get("customerId", os.getenv("ZPA_CUSTOMER_ID"))
        vanityDomain = config.get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "PRODUCTION"))

        # In VCR playback mode, use dummy credentials if real ones aren't provided
        if mock_tests:
            clientId = clientId or "dummy_client_id"
            clientSecret = clientSecret or "dummy_client_secret"
            vanityDomain = vanityDomain or "dummy_vanity_domain"
            customerId = customerId or "dummy_customer_id"

        # Extract logging configuration or use defaults
        logging_config = config.get("logging", {"enabled": False, "verbose": False})

        # Set up the client config dictionary
        client_config = {
            "clientId": clientId,
            "clientSecret": clientSecret,
            "customerId": customerId,
            "vanityDomain": vanityDomain,
            "cloud": cloud,
            "logging": {"enabled": logging_config.get("enabled", True), "verbose": logging_config.get("verbose", True)},
        }

        # Check if we are running in a pytest mock environment with pyfakefs
        if PYTEST_MOCK_CLIENT in os.environ and fs is not None:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)


class MockLegacyZIAClient(LegacyZIAClient):
    def __init__(self, fs, config=None):
        """
        Initialize the MockZIAClient with support for environment variables and
        optional inline config.

        Args:
            fs: Fixture to pause/resume the filesystem mock for pyfakefs.
            config: Optional dictionary containing client configuration (clientId, clientSecret, etc.).
        """
        # If config is not provided, initialize it as an empty dictionary
        config = config or {}

        # Fetch credentials from environment variables, allowing them to be overridden by the config dictionary
        username = config.get("username", os.getenv("ZIA_USERNAME"))
        password = config.get("password", os.getenv("ZIA_PASSWORD"))
        api_key = config.get("api_key", os.getenv("ZIA_API_KEY"))
        cloud = config.get("cloud", os.getenv("ZIA_CLOUD"))

        # Extract logging configuration or use defaults
        logging_config = config.get("logging", {"enabled": False, "verbose": False})

        # Set up the client config dictionary
        client_config = {
            "username": username,
            "password": password,
            "api_key": api_key,
            "cloud": cloud,
            "logging": {"enabled": logging_config.get("enabled", True), "verbose": logging_config.get("verbose", True)},
        }

        # Check if we are running in a pytest mock environment with pyfakefs
        if PYTEST_MOCK_CLIENT in os.environ and fs is not None:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)
