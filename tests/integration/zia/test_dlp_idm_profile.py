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


class TestDLPIDMProfile:
    """
    Integration Tests for the DLP IDM Profile
    """

    @pytest.mark.vcr()
    def test_dlp_idm_profile(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            # Step 1: List all IDM profiles
            profiles = client.zia.dlp_resources.list_dlp_idm_profiles()
            assert isinstance(profiles, list), "Expected a list of IDM profiles"

            if profiles:
                # Step 2: Select first profile
                first_profile = profiles[0]
                profile_id = first_profile.profile_id

                # Step 3: Fetch by ID
                try:
                    fetched_profile = client.zia.dlp_resources.get_dlp_idm_profiles(profile_id)
                    assert fetched_profile is not None, "Expected a valid profile object"
                    assert fetched_profile.profile_id == profile_id, "Mismatch in profile ID"
                except Exception as exc:
                    errors.append(f"Fetching profile by ID failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing profiles failed: {exc}")

        # Final assertion
        if errors:
            pytest.fail(f"Test failed with errors: {errors}")
