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

# Deterministic search string for VCR - scopes list to avoid recording hundreds of profiles
VCR_LIST_SEARCH = "UpdatedEmailProfile_VCR_Integration"


@pytest.fixture
def fs():
    yield


class TestEmailProfiles:
    """
    Integration Tests for the ZIA Email Profiles.

    These tests use VCR to record and replay HTTP interactions.
    - First run with MOCK_TESTS=false records cassettes
    - Subsequent runs use recorded cassettes (no API calls)

    Uses a scoped search in list_email_profiles to avoid recording tenant-wide data.
    """

    @pytest.mark.vcr()
    def test_email_profiles_lifecycle(self, fs):
        """Test complete email profile CRUD lifecycle with a single resource."""
        client = MockZIAClient(fs)
        errors = []
        profile_id = None
        update_profile = None

        try:
            # Test: Add Email Profile (deterministic name for VCR)
            try:
                create_profile, _, error = client.zia.email_profiles.add_email_profile(
                    name="TestEmailProfile_VCR_Integration",
                    description="Test Description for VCR",
                    emails=["john.doe@example.com", "mary.jane@example.com"],
                )
                assert error is None, f"Add Email Profile Error: {error}"
                assert create_profile is not None, "Email profile creation failed."
                assert create_profile.name == "TestEmailProfile_VCR_Integration", "Created name mismatch."
                profile_id = create_profile.id
            except Exception as e:
                errors.append(f"Exception during add_email_profile: {str(e)}")

            # Test: Update Email Profile
            try:
                if profile_id:
                    update_profile, _, error = client.zia.email_profiles.update_email_profile(
                        profile_id=profile_id,
                        name="UpdatedEmailProfile_VCR_Integration",
                        description="Updated Description for VCR",
                        emails=["john.doe@example.com", "mary.jane@example.com"],
                    )
                    assert error is None, f"Update Email Profile Error: {error}"
                    assert update_profile is not None, "Email profile update returned None."
                    assert update_profile.name == "UpdatedEmailProfile_VCR_Integration", "Updated name mismatch."
            except Exception as e:
                errors.append(f"Exception during update_email_profile: {str(e)}")

            # Test: Get Email Profile
            try:
                if update_profile:
                    profile, _, error = client.zia.email_profiles.get_email_profile(update_profile.id)
                    assert error is None, f"Get Email Profile Error: {error}"
                    assert profile.id == profile_id, "Retrieved email profile ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_email_profile: {str(e)}")

            # Test: List Email Profiles (scoped search - finds our profile before delete)
            try:
                if update_profile:
                    profiles, _, error = client.zia.email_profiles.list_email_profiles(
                        query_params={"search": update_profile.name}
                    )
                    assert error is None, f"List Email Profiles Error: {error}"
                    assert profiles is not None and isinstance(profiles, list), "No profiles found or invalid format."
            except Exception as e:
                errors.append(f"Exception during list_email_profiles: {str(e)}")

        finally:
            # Ensure email profile cleanup
            try:
                if update_profile:
                    _, _, error = client.zia.email_profiles.delete_email_profile(update_profile.id)
                    assert error is None, f"Delete Email Profile Error: {error}"
            except Exception as e:
                errors.append(f"Exception during delete_email_profile: {str(e)}")

        # Final Assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")

    @pytest.mark.vcr()
    def test_list_email_profiles(self, fs):
        """Test listing email profiles with scoped search (VCR-friendly)."""
        client = MockZIAClient(fs)

        # Use scoped search to avoid fetching all tenant profiles - returns [] or few results
        profiles, _, error = client.zia.email_profiles.list_email_profiles(query_params={"search": VCR_LIST_SEARCH})
        assert error is None, f"List Email Profiles Error: {error}"
        assert profiles is not None, "Email profiles list is None"
        assert isinstance(profiles, list), "Email profiles is not a list"
