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


class TestIsolationProfile:
    """
    Integration Tests for the Isolation Profile
    """

    def test_isolation_profile(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all profiles
            profiles = client.isolation_profile.list_isolation_profiles()
            assert isinstance(profiles, list), "Expected a list of profiles"
            if profiles:  # If there are any profiles
                # Select the first profile for further testing
                first_profile = profiles[0]
                profile_id = first_profile.get("id")

                # Fetch the selected profile by its ID
                try:
                    fetched_profile = client.isolation_profile.get_profiles_by_id(profile_id)
                    assert fetched_profile is not None, "Expected a valid profile object"
                    assert fetched_profile.get("id") == profile_id, "Mismatch in profile ID"
                except Exception as exc:
                    errors.append(f"Fetching profile by ID failed: {exc}")

                # Attempt to retrieve the profile by name
                try:
                    profile_name = first_profile.get("name")
                    profile_by_name = client.isolation_profile.get_profiles_by_name(profile_name)
                    assert profile_by_name is not None, "Expected a valid profile object when searching by name"
                    assert profile_by_name.get("id") == profile_id, "Mismatch in profile ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching profile by name failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing profiles failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during profiles test: {errors}"
