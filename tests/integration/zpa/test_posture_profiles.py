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

from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestPostureProfile:
    """
    Integration Tests for the Posture Profile.
    """

    def test_posture_profile(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        # Attempt to list all posture profiles
        try:
            posture_profiles = client.posture_profiles.list_profiles()
            assert isinstance(posture_profiles, list), "Expected a list of posture profiles"
            assert len(posture_profiles) > 0, "No posture profiles found"
        except Exception as exc:
            errors.append(f"Listing posture profiles failed: {str(exc)}")

        if posture_profiles:
            first_profile = posture_profiles[0]
            profile_id = first_profile.get("id")

            # Fetch the selected posture profile by its ID
            try:
                fetched_profile = client.posture_profiles.get_profile(profile_id)
                assert fetched_profile is not None, "Expected a valid posture profile object"
                assert fetched_profile.get("id") == profile_id, "Mismatch in posture profile ID"
            except Exception as exc:
                errors.append(f"Fetching posture profile by ID failed: {str(exc)}")

            # Attempt to retrieve the posture profile by name
            try:
                profile_name = first_profile.get("name")
                profile_by_name = client.posture_profiles.get_profile_by_name(profile_name)
                assert profile_by_name is not None, "Expected a valid posture profile object when searching by name"
                assert profile_by_name.get("id") == profile_id, "Mismatch in posture profile ID when searching by name"
            except Exception as exc:
                errors.append(f"Fetching posture profile by name failed: {str(exc)}")

            # Test get_udid_by_profile_name function
            try:
                profile_udid = client.posture_profiles.get_udid_by_profile_name(profile_name)
                assert profile_udid is not None, "Expected a valid UDID when searching by profile name"
                assert profile_udid == first_profile.get("posture_udid"), "Mismatch in posture UDID when searching by name"
            except Exception as exc:
                errors.append(f"Fetching UDID by profile name failed: {str(exc)}")

            # Test get_name_by_posture_udid function
            try:
                returned_name = client.posture_profiles.get_name_by_posture_udid(profile_udid)
                assert returned_name is not None, "Expected a valid profile name when searching by UDID"
                assert returned_name == profile_name, "Mismatch in profile name when searching by UDID"
            except Exception as exc:
                errors.append(f"Fetching name by posture UDID failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during posture profile operations test: {'; '.join(errors)}"
