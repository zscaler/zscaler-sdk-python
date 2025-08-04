import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestPrivateCloudGroup:
    """
    Integration Tests for the private cloud group
    """

    def test_private_cloud_group(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        group_id = None  # Initialize group_id

        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_enabled = True
        city_country = "San Jose, US"
        country_code = "US"
        latitude = "37.33874"
        longitude = "-121.8852525"
        location = "San Jose, CA, USA"
        upgrade_day = "MONDAY"
        upgrade_time_in_secs = "25200"
        override_version_profile = True
        version_profile_id = "0"

        try:
            # Create a new private cloud group
            created_group, _, err = client.zpa.private_cloud_group.add_cloud_group(
                name=group_name,
                description=group_description,
                enabled=group_enabled,
                city_country=city_country,
                country_code=country_code,
                latitude=latitude,
                longitude=longitude,
                location=location,
                upgrade_day=upgrade_day,
                upgrade_time_in_secs=upgrade_time_in_secs,
                override_version_profile=override_version_profile,
                version_profile_id=version_profile_id
            )
            assert err is None, f"Error creating private cloud group: {err}"
            assert created_group is not None
            assert created_group.name == group_name
            assert created_group.description == group_description
            assert created_group.enabled is True

            group_id = created_group.id
        except Exception as exc:
            errors.append(exc)

        try:
            if group_id:
                # Retrieve the created private cloud group by ID
                retrieved_group, _, err = client.zpa.private_cloud_group.get_cloud_group(group_id)
                assert err is None, f"Error fetching group: {err}"
                assert retrieved_group.id == group_id
                assert retrieved_group.name == group_name

                # Update the private cloud group
                updated_name = group_name + " Updated"
                _, _, err = client.zpa.private_cloud_group.update_cloud_group(
                    group_id, 
                    name=updated_name
                )
                assert err is None, f"Error updating group: {err}"

                updated_group, _, err = client.zpa.private_cloud_group.get_cloud_group(group_id)
                assert err is None, f"Error fetching updated group: {err}"
                assert updated_group.name == updated_name

                # List private cloud group and ensure the updated group is in the list
                groups_list, _, err = client.zpa.private_cloud_group.list_cloud_groups()
                assert err is None, f"Error listing groups: {err}"
                assert any(group.id == group_id for group in groups_list)
        except Exception as exc:
            errors.append(exc)

        finally:
            # Cleanup: Delete the private cloud group if it was created
            if group_id:
                try:
                    delete_response, _, err = client.zpa.private_cloud_group.delete_cloud_group(group_id)
                    assert err is None, f"Error deleting group: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for private cloud group ID {group_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the private cloud group lifecycle test: {errors}"
