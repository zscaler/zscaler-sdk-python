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
        names = TestNameGenerator("app_segment")
        name = names.name       # "tests-app-segment"
        desc = names.description  # "Test App Segment"
        updated_name = names.updated_name  # "tests-app-segment-updated"
    """
    
    def __init__(self, resource_type: str, suffix: str = ""):
        """
        Initialize with a resource type identifier.
        
        Args:
            resource_type: A descriptive string for the resource (e.g., "app_segment", "server_group")
            suffix: Optional suffix for uniqueness (e.g., "1", "alt")
        """
        self.resource_type = resource_type.lower().replace("_", "-")
        self.suffix = f"-{suffix}" if suffix else ""
        
    @property
    def name(self) -> str:
        """Returns deterministic test name like 'tests-app-segment'"""
        return f"tests-{self.resource_type}{self.suffix}"
    
    @property
    def updated_name(self) -> str:
        """Returns deterministic updated name like 'tests-app-segment-updated'"""
        return f"tests-{self.resource_type}{self.suffix}-updated"
    
    @property
    def description(self) -> str:
        """Returns deterministic description like 'Test App Segment'"""
        words = self.resource_type.replace("-", " ").title()
        return f"Test {words}{self.suffix}"
    
    @property
    def updated_description(self) -> str:
        """Returns deterministic updated description"""
        return f"{self.description} Updated"


class MockZPAClient(ZscalerClient):
    def __init__(self, fs, config=None):
        """
        Initialize the MockZPAClient with support for environment variables and
        optional inline config.

        Args:
            fs: Fixture to pause/resume the filesystem mock for pyfakefs.
            config: Optional dictionary containing client configuration (clientId, clientSecret, etc.).
        """
        # If config is not provided, initialize it as an empty dictionary
        config = config or {}

        # Check if we're in VCR playback mode (MOCK_TESTS=true)
        mock_tests = os.getenv("MOCK_TESTS", "true").strip().lower() != "false"

        # Fetch credentials from environment variables, allowing them to be overridden by the config dictionary
        clientId = config.get("clientId", os.getenv("ZSCALER_CLIENT_ID"))
        clientSecret = config.get("clientSecret", os.getenv("ZSCALER_CLIENT_SECRET"))
        customerId = config.get("customerId", os.getenv("ZPA_CUSTOMER_ID"))
        vanityDomain = config.get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "PRODUCTION"))

        # In VCR playback mode, provide dummy credentials if real ones aren't available
        # IMPORTANT: Use the same customer ID that was used during cassette recording
        # to ensure VCR path matching works correctly
        if mock_tests:
            clientId = clientId or "dummy_client_id"
            clientSecret = clientSecret or "dummy_client_secret"
            # Use the customer ID from recorded cassettes for VCR playback
            customerId = customerId or "216196257331281920"
            vanityDomain = vanityDomain or "dummy_vanity_domain"

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
