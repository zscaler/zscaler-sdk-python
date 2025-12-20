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


class TestCloudBrowserIsolation:
    """
    Integration Tests for the Cloud Browser Isolation API.
    """

    @pytest.mark.vcr()
    def test_cloud_browser_isolation_operations(self, fs):
        """Test Cloud Browser Isolation operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_isolation_profiles
            profiles, response, err = client.zia.cloud_browser_isolation.list_isolation_profiles()
            assert err is None, f"List isolation profiles failed: {err}"
            assert profiles is not None, "Profiles should not be None"
            assert isinstance(profiles, list), "Profiles should be a list"

        except Exception as e:
            errors.append(f"Exception during cloud browser isolation test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

