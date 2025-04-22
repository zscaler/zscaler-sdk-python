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


class TestPostureProfiles:
    """
    Integration Tests for the Posture Profiles.
    """

    def test_posture_profile(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        profile_id = None
        profile_name = None
        profile_udid = None

        # List all posture profiles
        try:
            profile_response, _, err = client.zpa.posture_profiles.list_posture_profiles()
            assert err is None, f"Error listing posture profiles: {err}"
            assert isinstance(profile_response, list), "Expected a list of posture profiles"
            if profile_response:
                first_profile = profile_response[0]
                profile_id = first_profile.id
                profile_name = first_profile.name
                profile_udid = first_profile.posture_udid
                assert profile_id is not None, "Posture Profile ID should not be None"
        except Exception as exc:
            errors.append(f"Listing posture profiles failed: {str(exc)}")

        if profile_id:
            # Fetch the selected posture profile by its ID
            try:
                fetched_group, _, err = client.zpa.posture_profiles.get_profile(profile_id)
                assert err is None, f"Error fetching posture profile by ID: {err}"
                assert fetched_group is not None, "Expected a valid posture profile object"
                assert fetched_group.id == profile_id, "Mismatch in posture profile ID"
            except Exception as exc:
                errors.append(f"Fetching posture profile by ID failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during posture profile operations test: {errors}"
