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

from tests.test_utils import reset_vcr_counters
from zscaler import ZscalerClient

PYTEST_MOCK_CLIENT = "pytest_mock_client"


@pytest.fixture(autouse=True, scope="function")
def reset_counters_per_test():
    """
    Reset VCR counters before each test function.

    This ensures that generate_random_string() and generate_random_ip()
    return the same deterministic values during both recording and playback.
    """
    reset_vcr_counters()
    yield


@pytest.fixture(scope="function")
def aiguard_client(fs):
    return MockAIGuardClient(fs)


class MockAIGuardClient(ZscalerClient):
    """
    Mock client for the Zscaler AI Guard service.

    AI Guard is OneAPI-only (no legacy client), so this mirrors the OneAPI
    ``ZscalerClient`` bootstrap used by the other OneAPI services (e.g. ZINS,
    ZMS) and does not require a customer id.
    """

    def __init__(self, fs, config=None):
        """
        Initialize the MockAIGuardClient with support for environment variables
        and optional inline config.

        Args:
            fs: Fixture to pause/resume the filesystem mock for pyfakefs.
            config: Optional dictionary containing client configuration
                (clientId, clientSecret, vanityDomain, cloud).
        """
        config = config or {}

        # VCR playback mode (MOCK_TESTS=true means use recorded cassettes).
        mock_tests = os.getenv("MOCK_TESTS", "true").strip().lower() != "false"

        clientId = config.get("clientId", os.getenv("ZSCALER_CLIENT_ID"))
        clientSecret = config.get("clientSecret", os.getenv("ZSCALER_CLIENT_SECRET"))
        vanityDomain = config.get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "beta"))

        # In playback mode, fall back to dummy credentials when real ones are absent.
        if mock_tests:
            clientId = clientId or "dummy_client_id"
            clientSecret = clientSecret or "dummy_client_secret"
            vanityDomain = vanityDomain or "dummy_vanity_domain"

        logging_config = config.get("logging", {"enabled": False, "verbose": False})

        client_config = {
            "clientId": clientId,
            "clientSecret": clientSecret,
            "vanityDomain": vanityDomain,
            "cloud": cloud,
            "logging": {"enabled": logging_config.get("enabled", False), "verbose": logging_config.get("verbose", False)},
        }

        if PYTEST_MOCK_CLIENT in os.environ and fs is not None:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)
