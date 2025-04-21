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


class TestSegmentGroup:
    """
    Integration Tests for the Segment Group
    """

    def test_segment_group(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        segment_group_name = "tests-" + generate_random_string()
        segment_group_description = "tests-" + generate_random_string()
        group_id = None  # Initialize group_id

        try:
            # Create a new segment group
            created_group, _, err = client.zpa.segment_groups.add_group(
                name=segment_group_name,
                description=segment_group_description,
                enabled=True,
            )
            assert err is None, f"Error creating group: {err}"
            assert created_group is not None
            assert created_group.name == segment_group_name
            assert created_group.description == segment_group_description
            assert created_group.enabled is True

            group_id = created_group.id  # Capture the group_id for later use
        except Exception as exc:
            errors.append(f"Error during segment group creation: {exc}")

        try:
            if group_id:
                # Retrieve the created segment group by ID
                retrieved_group, _, err = client.zpa.segment_groups.get_group(group_id)
                assert err is None, f"Error fetching group: {err}"
                assert retrieved_group.id == group_id
                assert retrieved_group.name == segment_group_name

                # Update the segment group
                updated_name = segment_group_name + " Updated"
                _, _, err = client.zpa.segment_groups.update_group(group_id, name=updated_name)
                assert err is None, f"Error updating group: {err}"

                updated_group, _, err = client.zpa.segment_groups.get_group(group_id)
                assert err is None, f"Error fetching updated group: {err}"
                assert updated_group.name == updated_name

                # List segment groups and ensure the updated group is in the list
                groups_list, _, err = client.zpa.segment_groups.list_groups()
                assert err is None, f"Error listing groups: {err}"
                assert any(group.id == group_id for group in groups_list)
        except Exception as exc:
            errors.append(f"Segment group operation failed: {exc}")

        finally:
            # Cleanup: Delete the segment group if it was created
            if group_id:
                try:
                    delete_response, _, err = client.zpa.segment_groups.delete_group(group_id)
                    assert err is None, f"Error deleting group: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for segment group ID {group_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the segment group lifecycle test: {errors}"
