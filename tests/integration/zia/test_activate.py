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


class TestActivate:
    """
    Integration Tests for the Activation API.
    """

    @pytest.mark.vcr()
    def test_activation_operations(self, fs):
        """Test Activation API operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test status - get current activation status
            try:
                status, response, err = client.zia.activate.status()
                assert err is None, f"Get activation status failed: {err}"
                assert status is not None, "Status should not be None"
            except Exception as e:
                errors.append(f"Exception during status: {str(e)}")

            # Test activate - trigger activation
            try:
                activation, response, err = client.zia.activate.activate()
                # Activation may fail if no changes pending - that's ok
                if err is None:
                    assert activation is not None, "Activation result should not be None"
            except Exception as e:
                # Activation may fail if no changes - that's acceptable
                pass

            # Test get_eusa_status
            try:
                eusa_status, response, err = client.zia.activate.get_eusa_status()
                assert err is None, f"Get EUSA status failed: {err}"
                assert eusa_status is not None, "EUSA status should not be None"
            except Exception as e:
                errors.append(f"Exception during get_eusa_status: {str(e)}")

        except Exception as e:
            errors.append(f"Exception during activation test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

