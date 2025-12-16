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
import time
from zscaler import ZscalerClient
from tests.test_utils import reset_vcr_counters

PYTEST_MOCK_CLIENT = "pytest_mock_client"


@pytest.fixture(autouse=True, scope="function")
def reset_counters_per_test():
    """
    Reset VCR counters before each test function.
    """
    reset_vcr_counters()
    yield


@pytest.fixture(scope="function")
def zinsights_client(fs):
    return MockZInsightsClient(fs)


def get_time_range(days: int = 7):
    """
    Get time range for Z-Insights queries.
    
    Note: Z-Insights API requires end_time to be at least 1 day before current time.
    """
    # End time is 1 day ago (API requirement)
    end_time = int(time.time() * 1000) - (1 * 24 * 60 * 60 * 1000)
    # Start time is 'days' days before end_time
    start_time = end_time - (days * 24 * 60 * 60 * 1000)
    return start_time, end_time


class MockZInsightsClient(ZscalerClient):
    def __init__(self, fs, config=None):
        """
        Initialize the MockZInsightsClient with support for environment variables and
        optional inline config.

        Args:
            fs: Fixture to pause/resume the filesystem mock for pyfakefs.
            config: Optional dictionary containing client configuration.
        """
        # If config is not provided, initialize it as an empty dictionary
        config = config or {}

        # Check if we're in VCR playback mode (MOCK_TESTS=true means use cassettes)
        mock_tests = os.getenv("MOCK_TESTS", "true").strip().lower() != "false"

        # Fetch credentials from environment variables
        clientId = config.get("clientId", os.getenv("ZSCALER_CLIENT_ID"))
        clientSecret = config.get("clientSecret", os.getenv("ZSCALER_CLIENT_SECRET"))
        customerId = config.get("customerId", os.getenv("ZPA_CUSTOMER_ID"))
        vanityDomain = config.get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "beta"))

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
            "logging": {"enabled": logging_config.get("enabled", False), "verbose": logging_config.get("verbose", False)},
        }

        # Check if we are running in a pytest mock environment with pyfakefs
        if PYTEST_MOCK_CLIENT in os.environ and fs is not None:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)

