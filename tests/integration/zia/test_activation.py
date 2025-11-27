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

import pytest
from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestActivation:
    """
    Integration Tests for the ZIA Activation.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_activation(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Step 1: Check current activation status
        try:
            config_status, _, error = client.zia.activate.status()
            assert error is None, f"Error retrieving activation status: {error}"
            assert hasattr(config_status, "status"), "Missing 'status' attribute in Activation object"
            assert config_status.status in ["ACTIVE", "PENDING"], f"Unexpected activation status: {config_status.status}"
        except Exception as exc:
            errors.append(f"Activation status check failed: {exc}")

        # Step 2: Activate configuration
        try:
            config_activation, _, error = client.zia.activate.activate()
            assert error is None, f"Error during activation: {error}"
            assert hasattr(config_activation, "status"), "Missing 'status' attribute in Activation object"
            assert config_activation.status in [
                "ACTIVE",
                "PENDING",
            ], f"Unexpected activation result: {config_activation.status}"
        except Exception as exc:
            errors.append(f"Activation trigger failed: {exc}")

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during activation operations test:\n{chr(10).join(errors)}"
