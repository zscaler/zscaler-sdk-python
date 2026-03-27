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


def get_customer_id() -> str:
    """Return the customer ID from env or a dummy for VCR playback."""
    cid = os.getenv("ZPA_CUSTOMER_ID")
    if not cid:
        mock_tests = os.getenv("MOCK_TESTS", "true").strip().lower() != "false"
        if mock_tests:
            return "dummy_customer_id"
    return cid or "dummy_customer_id"


@pytest.fixture(autouse=True, scope="function")
def reset_counters_per_test():
    """
    Reset VCR counters before each test function.
    """
    reset_vcr_counters()
    yield


@pytest.fixture(scope="function")
def zms_client(fs):
    return MockZMSClient(fs)


class MockZMSClient(ZscalerClient):
    def __init__(self, fs, config=None):
        """
        Initialize the MockZMSClient with support for environment variables and
        optional inline config.

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
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "beta"))

        if mock_tests:
            clientId = clientId or "dummy_client_id"
            clientSecret = clientSecret or "dummy_client_secret"
            vanityDomain = vanityDomain or "dummy_vanity_domain"
            customerId = customerId or "dummy_customer_id"

        logging_config = config.get("logging", {"enabled": False, "verbose": False})

        client_config = {
            "clientId": clientId,
            "clientSecret": clientSecret,
            "customerId": customerId,
            "vanityDomain": vanityDomain,
            "cloud": cloud,
            "logging": {
                "enabled": logging_config.get("enabled", False),
                "verbose": logging_config.get("verbose", False),
            },
        }

        if PYTEST_MOCK_CLIENT in os.environ and fs is not None:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)
