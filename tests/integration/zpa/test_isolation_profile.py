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

from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestIsolationProfile:
    """
    Integration Tests for the Isolation Profile.
    """

    def test_isolation_profile(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        # Attempt to list all isolation profiles
        try:
            isolation_profiles, _, err = client.zpa.cbi_zpa_profile.list_isolation_profiles()
            assert err is None, f"Expected a list of isolation profiles: {err}"
            assert isinstance(isolation_profiles, list), "Expected a list of isolation profiles"
        except Exception as exc:
            errors.append(f"Listing isolation profiles failed: {str(exc)}")

        # Attempt to list all isolation profiles
        try:
            isolation_profiles, _, err = client.zpa.cbi_zpa_profile.list_cbi_zpa_profiles()
            assert err is None, f"Expected a list of isolation profiles: {err}"
            assert isinstance(isolation_profiles, list), "Expected a list of isolation profiles"
        except Exception as exc:
            errors.append(f"Listing isolation profiles failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during isolation profile operations test: {errors}"
