import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAppConnectorGroup:
    """
    Integration Tests for the app connector group
    """

    def test_app_connector_group(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        group_id = None  # Initialize group_id
        
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
            created_group, _, err = client.zpa.app_connector_groups.add_connector_group(
                name=group_name,
                description=group_description,
                group_enabled=group_enabled,
                latitude=latitude,
                longitude=longitude,
                location=location,
                upgrade_day=upgrade_day,
                upgrade_time_in_secs=upgrade_time_in_secs,
                override_version_profile=override_version_profile,
                version_profile_name=version_profile_name,
                version_profile_id=version_profile_id,
                dns_query_type=dns_query_type,
                pra_enabled=pra_enabled,
                tcp_quick_ack_app=tcp_quick_ack_app,
                tcp_quick_ack_assistant=tcp_quick_ack_assistant,
                tcp_quick_ack_read_assistant=tcp_quick_ack_read_assistant,
            )
            assert err is None, f"Error creating app connector group: {err}"
            assert created_group is not None
            assert created_group.name == group_name
            assert created_group.description == group_description
            assert created_group.enabled is True

            group_id = created_group.id
        except Exception as exc:
            errors.append(exc)

        try:
            if group_id:
                # Retrieve the created app connector group by ID
                retrieved_group, _, err = client.zpa.app_connector_groups.get_connector_group(group_id)
                assert err is None, f"Error fetching group: {err}"
                assert retrieved_group.id == group_id
                assert retrieved_group.name == group_name

                # Update the app connector group
                updated_name = group_name + " Updated"
                _, _, err = client.zpa.app_connector_groups.update_connector_group(group_id, name=updated_name)
                assert err is None, f"Error updating group: {err}"

                updated_group, _, err = client.zpa.app_connector_groups.get_connector_group(group_id)
                assert err is None, f"Error fetching updated group: {err}"
                assert updated_group.name == updated_name

                # List app connector group and ensure the updated group is in the list
                groups_list, _, err = client.zpa.app_connector_groups.list_connector_groups()
                assert err is None, f"Error listing groups: {err}"
                assert any(group.id == group_id for group in groups_list)
        except Exception as exc:
            errors.append(exc)

        finally:
            # Cleanup: Delete the app connector group if it was created
            if group_id:
                try:
                    delete_response, _, err = client.zpa.app_connector_groups.delete_connector_group(group_id)
                    assert err is None, f"Error deleting group: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for app connector group ID {group_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the app connector group lifecycle test: {errors}"
