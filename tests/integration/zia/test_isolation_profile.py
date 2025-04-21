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


class TestIsolationProfile:
    """
    Integration Tests for the Isolation Profile
    """

    def test_isolation_profile(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            # Step 1: List all isolation profiles
            profiles, _, error = client.zia.cloud_browser_isolation.list_isolation_profiles()
            assert error is None, f"List Isolation Profiles Error: {error}"
            assert isinstance(profiles, list), "Expected a list of profiles"

            if profiles:
                # Step 2: Select first profile (could be extended later)
                first_profile = profiles[0]
                profile_id = first_profile.id  # ✅ Model-based access

                # Optionally: validate field
                assert profile_id is not None, "Profile ID should not be None"

        except Exception as exc:
            errors.append(f"Listing profiles failed: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
