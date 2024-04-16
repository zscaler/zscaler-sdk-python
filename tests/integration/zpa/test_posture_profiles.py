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

    @pytest.mark.asyncio
    async def test_posture_profile(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        # Attempt to list all posture profiles
        try:
            posture_profile = client.posture_profiles.list_profiles()
            assert isinstance(
                posture_profile, list
            ), "Expected a list of posture profiles"
        except Exception as exc:
            errors.append(f"Listing posture profiles failed: {str(exc)}")

        # Process each posture profile if the list is not empty
        if posture_profile:
            for first_profile in posture_profile:
                profile_id = first_profile.get("id")

                # Fetch the selected posture profile by its ID
                try:
                    fetched_profile = client.posture_profiles.get_profile(profile_id)
                    assert (
                        fetched_profile is not None
                    ), "Expected a valid posture profile object"
                    assert (
                        fetched_profile.get("id") == profile_id
                    ), "Mismatch in posture profile ID"
                except Exception as exc:
                    errors.append(f"Fetching posture profile by ID failed: {str(exc)}")

                # Attempt to retrieve the posture profile by name
                try:
                    profile_name = first_profile.get("name")
                    profile_by_name = client.posture_profiles.get_profile_by_name(
                        profile_name
                    )
                    assert (
                        profile_by_name is not None
                    ), "Expected a valid posture profile object when searching by name"
                    assert (
                        profile_by_name.get("id") == profile_id
                    ), "Mismatch in posture profile ID when searching by name"
                except Exception as exc:
                    errors.append(
                        f"Fetching posture profile by name failed: {str(exc)}"
                    )

                # Once we've tested one profile, exit the loop to avoid redundant testing
                break

        # Assert that no errors occurred during the test
        assert (
            len(errors) == 0
        ), f"Errors occurred during posture profile operations test: {errors}"
