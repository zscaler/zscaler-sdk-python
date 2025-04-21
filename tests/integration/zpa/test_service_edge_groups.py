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


class TestServiceEdgeGroup:
    """
    Integration Tests for the Service Edge Group
    """

    def test_service_edge_group(self, fs):
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
        version_profile_id = "0"
        is_public = "TRUE"
        group_id = None

        try:
            # Create a new service edge group
            created_group, _, err = client.zpa.service_edge_group.add_service_edge_group(
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
                is_public=is_public,
            )
            assert err is None, f"Error creating service edge group: {err}"
            assert created_group is not None
            assert created_group.name == group_name
            assert created_group.description == group_description
            assert created_group.enabled is True

            group_id = created_group.id  # Capture the group ID for later use
        except Exception as exc:
            errors.append(f"Failed to create service edge group: {exc}")

        try:
            if group_id:
                # Retrieve the created service edge group by ID
                retrieved_group, _, err = client.zpa.service_edge_group.get_service_edge_group(group_id)
                assert err is None, f"Error fetching group: {err}"
                assert retrieved_group.id == group_id
                assert retrieved_group.name == group_name

                # Update the service edge group
                updated_name = group_name + " Updated"
                _, _, err = client.zpa.service_edge_group.update_service_edge_group(group_id, name=updated_name)
                assert err is None, f"Error updating group: {err}"

                updated_group, _, err = client.zpa.service_edge_group.get_service_edge_group(group_id)
                assert err is None, f"Error fetching updated group: {err}"
                assert updated_group.name == updated_name

                # List service edge group and ensure the updated group is in the list
                groups_list, _, err = client.zpa.service_edge_group.list_service_edge_groups()
                assert err is None, f"Error listing groups: {err}"
                assert any(group.id == group_id for group in groups_list)
        except Exception as exc:
            errors.append(exc)

        finally:
            # Cleanup: Delete the service edge group if it was created
            if group_id:
                try:
                    delete_response, _, err = client.zpa.service_edge_group.delete_service_edge_group(group_id)
                    assert err is None, f"Error deleting group: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for service edge group ID {group_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the service edge group lifecycle test: {errors}"
