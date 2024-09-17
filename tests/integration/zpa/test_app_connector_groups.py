import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAppConnectorGroup:
    """
    Integration Tests for the App Connector Group
    """

    def test_app_connector_group(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_enabled = True
        latitude = "37.33874"
        longitude = "-121.8852525"
        location = "San Jose, CA, USA"
        upgrade_day = "SUNDAY"
        upgrade_time_in_secs = "66600"
        override_version_profile = True
        version_profile_name = "Default"
        version_profile_id = "0"
        dns_query_type = "IPV4_IPV6"
        pra_enabled = True
        tcp_quick_ack_app = True
        tcp_quick_ack_assistant = True
        tcp_quick_ack_read_assistant = True

        try:
            # Create a new app connector group
            created_group = client.connectors.add_connector_group(
                name=group_name,
                description=group_description,
                enabled=group_enabled,
                latitude=latitude,
                longitude=longitude,
                location=location,
                upgrade_day=upgrade_day,
                upgrade_time_in_secs=upgrade_time_in_secs,
                override_version_profile=override_version_profile,
                version_profile_id=version_profile_id,
                version_profile_name=version_profile_name,
                dns_query_type=dns_query_type,
                pra_enabled=pra_enabled,
                tcp_quick_ack_app=tcp_quick_ack_app,
                tcp_quick_ack_assistant=tcp_quick_ack_assistant,
                tcp_quick_ack_read_assistant=tcp_quick_ack_read_assistant,
            )
            assert created_group is not None
            assert created_group.name == group_name
            assert created_group.description == group_description
            assert created_group.enabled == group_enabled

            group_id = created_group.id
        except Exception as exc:
            errors.append(f"Failed to create app connector group: {exc}")

        if group_id:
            try:
                # Retrieve the created app connector group by ID
                retrieved_group = client.connectors.get_connector_group(group_id)
                assert retrieved_group.id == group_id
                assert retrieved_group.name == group_name
            except Exception as exc:
                errors.append(f"Failed to retrieve app connector group: {exc}")

        try:
            # Update the app connector group
            updated_name = group_name + " Updated"
            client.connectors.update_connector_group(group_id, name=updated_name)

            updated_group = client.connectors.get_connector_group(group_id)
            assert updated_group.name == updated_name
        except Exception as exc:
            errors.append(f"Failed to update app connector group: {exc}")

        try:
            # List app connector group and ensure the updated group is in the list
            groups_list = client.connectors.list_connector_groups()
            assert any(group.id == group_id for group in groups_list)
        except Exception as exc:
            errors.append(f"Failed to list app connector group: {exc}")

        try:
            # Search for the app connector group by name
            search_result = client.connectors.get_connector_group_by_name(updated_name)
            assert search_result is not None
            assert search_result.id == group_id
        except Exception as exc:
            errors.append(f"Failed to search for app connector group by name: {exc}")

        finally:
            # Cleanup: Delete the app connector group if it was created
            if group_id:
                try:
                    delete_response_code = client.connectors.delete_connector_group(group_id)
                    assert str(delete_response_code) == "204", f"Failed to delete app connector group with ID {group_id}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for app connector group ID {group_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the app connector group lifecycle test: {errors}"

class TestCustomerVersionProfile:
    def test_version_profiles(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        # Step 1: Test to retrieve all version profiles without any filters
        try:
            profiles = client.connectors.list_version_profiles()
            assert isinstance(profiles, list), "Expected a list of version profiles"
            assert len(profiles) > 0, "Expected non-empty list of profiles"
        except AssertionError as e:
            errors.append(f"Error retrieving all profiles: {str(e)}")

        # Profile names to test
        profile_names = ["Default", "Previous Default", "New Release"]

        # Step 2: Test to retrieve version profiles by specific names
        for profile_name in profile_names:
            try:
                profiles_by_name = client.connectors.list_version_profiles(search=profile_name)
                found_profiles = [profile for profile in profiles_by_name if profile.get('name') == profile_name]
                assert found_profiles, f"No profiles found with the name {profile_name}"
            except AssertionError as e:
                errors.append(f"Error retrieving profile by name '{profile_name}': {str(e)}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during the tests: {errors}"

