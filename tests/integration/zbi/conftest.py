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

import os

import pytest

from tests.test_utils import reset_vcr_counters
from zscaler import ZscalerClient

PYTEST_MOCK_CLIENT = "pytest_mock_client"


@pytest.fixture(autouse=True, scope="function")
def reset_counters_per_test():
    """Reset VCR counters before each test function."""
    reset_vcr_counters()
    yield


class NameGenerator:
    """Generates deterministic test names for VCR-based testing."""

    def __init__(self, resource_type: str, suffix: str = ""):
        self.resource_type = resource_type.lower().replace("_", "-")
        self.suffix = f"-{suffix}" if suffix else ""

    @property
    def name(self) -> str:
        return f"tests-{self.resource_type}{self.suffix}"

    @property
    def updated_name(self) -> str:
        return f"tests-{self.resource_type}{self.suffix}-updated"

    @property
    def description(self) -> str:
        words = self.resource_type.replace("-", " ").title()
        return f"Test {words}{self.suffix}"


class MockZBIClient(ZscalerClient):
    def __init__(self, fs, config=None):
        """
        Initialize the MockZBIClient with support for environment
        variables and optional inline config.

        Args:
            fs: Fixture to pause/resume the filesystem mock for pyfakefs.
            config: Optional dictionary containing client configuration.
        """
        config = config or {}

        mock_tests = os.getenv("MOCK_TESTS", "true").strip().lower() != "false"

        clientId = config.get("clientId", os.getenv("ZSCALER_CLIENT_ID"))
        clientSecret = config.get("clientSecret", os.getenv("ZSCALER_CLIENT_SECRET"))
        customerId = config.get("customerId", os.getenv("ZPA_CUSTOMER_ID"))
        vanityDomain = config.get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "PRODUCTION"))

        if mock_tests:
            clientId = clientId or "dummy_client_id"
            clientSecret = clientSecret or "dummy_client_secret"
            customerId = customerId or "dummy_customer_id"
            vanityDomain = vanityDomain or "dummy_vanity_domain"

        logging_config = config.get("logging", {"enabled": False, "verbose": False})

        client_config = {
            "clientId": clientId,
            "clientSecret": clientSecret,
            "customerId": customerId,
            "vanityDomain": vanityDomain,
            "cloud": cloud,
            "logging": {
                "enabled": logging_config.get("enabled", True),
                "verbose": logging_config.get("verbose", True),
            },
        }

        if PYTEST_MOCK_CLIENT in os.environ and fs is not None:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)


@pytest.fixture
def zbi_client(fs):
    """Return a Zscaler client for ZBI integration tests."""
    return MockZBIClient(fs)
