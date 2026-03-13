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

from zscaler.oneapi_client import LegacyZTBClient
from tests.test_utils import reset_vcr_counters

PYTEST_MOCK_CLIENT = "pytest_mock_client"


@pytest.fixture(autouse=True, scope="function")
def reset_counters_per_test():
    """
    Reset VCR counters before each test function.

    Ensures deterministic values during recording and playback.
    """
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
    def site_id(self) -> str:
        """Deterministic site ID for ransomware kill tests."""
        return f"tests-{self.resource_type}{self.suffix}"


@pytest.fixture(scope="function")
def ztb_client():
    """Provide MockZTBClient for integration tests."""
    return MockZTBClient()


class MockZTBClient(LegacyZTBClient):
    """
    ZTB client for integration tests with VCR support.

    Uses dummy credentials when MOCK_TESTS=true (playback).
    Uses env vars ZTB_API_KEY, ZTB_CLOUD, ZTB_OVERRIDE_URL when recording.
    """

    def __init__(self, config=None):
        config = config or {}
        mock_tests = os.getenv("MOCK_TESTS", "true").strip().lower() != "false"

        api_key = config.get("api_key", os.getenv("ZTB_API_KEY"))
        cloud = config.get("cloud", os.getenv("ZTB_CLOUD"))
        override_url = config.get("override_url", os.getenv("ZTB_OVERRIDE_URL"))

        if mock_tests:
            api_key = api_key or "dummy_api_key_for_vcr_playback"
            # Use test URL that matches VCR cassette sanitization (tests/conftest.py)
            override_url = override_url or "https://ztb.test.zscaler.com"
            cloud = cloud or "ztb"

        client_config = {
            "api_key": api_key,
            "cloud": cloud,
            "override_url": override_url,
            "timeout": config.get("timeout", 30),
            "max_retries": config.get("max_retries", 3),
            "logging": config.get("logging", {"enabled": False, "verbose": False}),
        }
        super().__init__(client_config)
