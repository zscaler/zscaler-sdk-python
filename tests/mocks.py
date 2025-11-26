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
Mock client helpers for VCR-based testing.

This module provides mock client classes that work with VCR cassettes
for recorded HTTP playback.

Usage:
    from tests.mocks import MockZscalerClient

    class TestMyResource:
        @pytest.mark.vcr()
        def test_something(self, fs):
            client = MockZscalerClient(fs)
            # Test code here - uses cassettes when MOCK_TESTS=true
"""

import os

from zscaler import ZscalerClient
from zscaler.oneapi_client import LegacyZIAClient

PYTEST_MOCK_CLIENT = "pytest_mock_client"
MOCK_TESTS = "MOCK_TESTS"

# Default configuration for mock testing (used when MOCK_TESTS=true)
MOCK_CONFIG = {
    "clientId": "test-client-id",
    "clientSecret": "test-client-secret",
    "customerId": "1234567890",
    "vanityDomain": "test.zslogin.net",
    "cloud": "PRODUCTION",
    "logging": {"enabled": False, "verbose": False},
}

# Legacy ZIA mock configuration
MOCK_LEGACY_ZIA_CONFIG = {
    "username": "test@zscaler.com",
    "password": "test-password",
    "api_key": "test-api-key",
    "cloud": "zscaler.net",
    "logging": {"enabled": False, "verbose": False},
}


def is_mock_tests_flag_true():
    """
    Check if running in mock test mode.

    Returns True by default (use cassettes).
    Set MOCK_TESTS=false to use real APIs.
    """
    return os.environ.get(MOCK_TESTS, "true").strip().lower() != "false"


class MockZscalerClient(ZscalerClient):
    """
    Mock Zscaler client for VCR testing.

    When MOCK_TESTS=true (default), uses mock configuration and cassettes.
    When MOCK_TESTS=false, uses real credentials from environment.

    Args:
        fs: Optional pyfakefs fixture for filesystem mocking
        config: Optional config override dictionary
    """

    def __init__(self, fs=None, config=None):
        """
        Initialize mock client.

        Args:
            fs: Optional pyfakefs fixture for filesystem mocking
            config: Optional config override dictionary
        """
        if is_mock_tests_flag_true():
            # Use mock configuration for VCR playback
            client_config = config or MOCK_CONFIG.copy()
        else:
            # Use real credentials from environment for recording
            client_config = config or {
                "clientId": os.getenv("ZSCALER_CLIENT_ID"),
                "clientSecret": os.getenv("ZSCALER_CLIENT_SECRET"),
                "customerId": os.getenv("ZPA_CUSTOMER_ID"),
                "vanityDomain": os.getenv("ZSCALER_VANITY_DOMAIN"),
                "cloud": os.getenv("ZSCALER_CLOUD", "PRODUCTION"),
                "logging": {"enabled": True, "verbose": True},
            }

        if PYTEST_MOCK_CLIENT in os.environ and fs:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)


class MockLegacyZIAClient(LegacyZIAClient):
    """
    Mock Legacy ZIA client for VCR testing.

    When MOCK_TESTS=true (default), uses mock configuration and cassettes.
    When MOCK_TESTS=false, uses real credentials from environment.
    """

    def __init__(self, fs=None, config=None):
        """
        Initialize mock legacy ZIA client.

        Args:
            fs: Optional pyfakefs fixture for filesystem mocking
            config: Optional config override dictionary
        """
        if is_mock_tests_flag_true():
            # Use mock configuration for VCR playback
            client_config = config or MOCK_LEGACY_ZIA_CONFIG.copy()
        else:
            # Use real credentials from environment for recording
            client_config = config or {
                "username": os.getenv("ZIA_USERNAME"),
                "password": os.getenv("ZIA_PASSWORD"),
                "api_key": os.getenv("ZIA_API_KEY"),
                "cloud": os.getenv("ZIA_CLOUD"),
                "logging": {"enabled": True, "verbose": True},
            }

        if PYTEST_MOCK_CLIENT in os.environ and fs:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)


# Aliases for backwards compatibility with existing tests
MockZIAClient = MockZscalerClient
MockZPAClient = MockZscalerClient
MockZCCClient = MockZscalerClient
MockZDXClient = MockZscalerClient
MockZTWClient = MockZscalerClient
MockZWAClient = MockZscalerClient
MockZIdentityClient = MockZscalerClient

