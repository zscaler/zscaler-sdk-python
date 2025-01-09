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
            try:
                control_group_name = "Protocol Issues"
                control_groups, _, err = client.zpa.inspection.list_predef_controls(
                    query_params={"search": "controlGroup", "search_field": control_group_name}
                )
                if err or not control_groups:
                    errors.append(f"Failed to fetch predefined controls for group {control_group_name}: {err}")
                    return

                # Extract predefined controls from the specified control group
                predefined_controls = []
                for group in control_groups:
                    if group.control_group == control_group_name:
                        for control in group.predefined_inspection_controls:
                            predefined_controls.append(
                                (control["id"], control["defaultAction"])  # Tuple format (id, action)
                            )
            except Exception as exc:
                errors.append(f"Error fetching predefined controls: {exc}")
                return

            # Create a new app protection security profile with predefined controls
            try:
                created_profile, _, err = client.zpa.inspection.add_profile(
                    name=profile_name,
                    paranoia_level=1,
                    predef_controls=predefined_controls,
                    incarnation_number=6,
                    global_control_actions=["PREDEFINED:PASS", "CUSTOM:NONE", "OVERRIDE_ACTION:COMMON"],
                    control_info_resource={
                        "control_type": "CUSTOM"
                    },
                    common_global_override_actions_config={
                        "PREDEF_CNTRL_GLOBAL_ACTION": "PASS",
                        "IS_OVERRIDE_ACTION_COMMON": "TRUE"
                    }
                )
                if err or not created_profile:
                    errors.append("App protection security profile creation failed or returned unexpected data")
                    return

                profile_id = created_profile.id
                assert profile_id is not None  # Asserting that a non-null ID is returned
            except Exception as exc:
                errors.append(f"Error creating profile: {exc}")
                return

            # Update the app protection security profile
            try:
                updated_name = profile_name + " Updated"
                client.zpa.inspection.update_profile(
                    profile_id, name=updated_name,
                    global_control_actions=["PREDEFINED:PASS", "CUSTOM:NONE", "OVERRIDE_ACTION:COMMON"],
                    control_info_resource={
                        "control_type": "CUSTOM"
                    },
                    common_global_override_actions_config={
                        "PREDEF_CNTRL_GLOBAL_ACTION": "PASS",
                        "IS_OVERRIDE_ACTION_COMMON": "TRUE"
                    }
                )
            except Exception as exc:
                errors.append(f"Error updating profile: {exc}")
                return

            # Update the app protection security profile
            try:
                updated_name = profile_name + " Updated"
                client.zpa.inspection.update_profile_and_controls(
                    profile_id, name=updated_name,
                    global_control_actions=["PREDEFINED:PASS", "CUSTOM:NONE", "OVERRIDE_ACTION:COMMON"],
                    control_info_resource={
                        "control_type": "CUSTOM"
                    },
                    common_global_override_actions_config={
                        "PREDEF_CNTRL_GLOBAL_ACTION": "PASS",
                        "IS_OVERRIDE_ACTION_COMMON": "TRUE"
                    }
                )
            except Exception as exc:
                errors.append(f"Error updating profile: {exc}")
                return

            # Fetch the updated profile
            try:
                updated_profile, _, err = client.zpa.inspection.get_profile(profile_id)
                if err or not updated_profile:
                    errors.append(f"Failed to retrieve updated profile: {err}")
                    return
                assert updated_profile.name == updated_name  # Verify update by checking the updated attribute
            except Exception as exc:
                errors.append(f"Error fetching updated profile: {exc}")
                return

            # List app protection security profiles and ensure the updated profile is in the list
            try:
                profiles_list, _, err = client.zpa.inspection.list_profiles()
                if err:
                    errors.append(f"Failed to list profiles: {err}")
                    return
                assert any(profile.id == profile_id for profile in profiles_list)
            except Exception as exc:
                errors.append(f"Error listing profiles: {exc}")
                return

        finally:
            # Cleanup resources
            if profile_id:
                try:
                    client.zpa.inspection.delete_profile(profile_id=profile_id)
                except Exception as exc:
                    errors.append(f"Deleting app protection security profile failed: {exc}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during the app protection security profile lifecycle test: {errors}"
