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
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAppProtectionProfile:
    """
    Integration Tests for the App Protection Profile
    """

    def test_app_protection_profile(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        profile_name = "tests-" + generate_random_string()
        profile_id = None  # Define profile_id here to ensure it's accessible throughout

        try:
            # Fetch predefined controls by control group name
            control_group_name = "Protocol Issues"
            control_group = client.inspection.get_predef_control_group_by_name(control_group_name)
            predefined_controls = [
                (control["id"], control["default_action"]) for control in control_group["predefined_inspection_controls"]
            ]

            # Create a new app protection security profile with predefined controls
            created_profile = client.inspection.add_profile(
                name=profile_name,
                paranoia_level=1,
                predef_controls_version="OWASP_CRS/3.3.0",
                predef_controls=predefined_controls,
            )
            if created_profile and "id" in created_profile:
                profile_id = created_profile.id
                assert profile_id is not None  # Asserting that a non-null ID is returned
            else:
                errors.append("App protection security profile creation failed or returned unexpected data")

            # Assuming profile_id is valid and the profile was created successfully
            if profile_id:
                # Update the app protection security profile
                updated_name = profile_name + " Updated"
                client.inspection.update_profile(profile_id, name=updated_name)
                updated_profile = client.inspection.get_profile(profile_id)
                assert updated_profile.name == updated_name  # Verify update by checking the updated attribute

                # List app protection security profiles and ensure the updated profile is in the list
                profiles_list = client.inspection.list_profiles()
                assert any(profile.id == profile_id for profile in profiles_list)

        except Exception as exc:
            errors.append(exc)

        finally:
            # Cleanup resources
            if profile_id:
                try:
                    client.inspection.delete_profile(profile_id=profile_id)
                except Exception as exc:
                    errors.append(f"Deleting app protection security profile failed: {exc}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during the app protection security profile lifecycle test: {errors}"
