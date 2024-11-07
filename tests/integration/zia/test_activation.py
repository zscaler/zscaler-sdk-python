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


import pytest
from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestActivation:
    """
    Integration Tests for the ZIA Activation
    """

    def test_activation(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        # Test Config Status
        try:
            config_status = client.activate.status()
            # Allow for both "ACTIVE" and "PENDING" statuses
            assert config_status in ["ACTIVE", "PENDING"], f"Unexpected configuration status: {config_status}"
        except Exception as exc:
            errors.append(f"Config status check failed: {exc}")

        # Test Config Activation
        try:
            config_activation = client.activate.activate()
            # Assuming the activation process might also return "PENDING" immediately after activation request
            assert config_activation in [
                "ACTIVE",
                "PENDING",
            ], f"Unexpected configuration activation status: {config_activation}"
        except Exception as exc:
            errors.append(f"Config activation failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during activation operations test: {errors}"
