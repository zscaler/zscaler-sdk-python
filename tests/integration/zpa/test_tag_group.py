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
from zscaler.zpa.models.tag_group import TagGroup


@pytest.fixture
def fs():
    yield


class TestTagGroup:
    """
    Integration Tests for the Tag Group resource.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_tag_group_lifecycle(self, fs):
        client = MockZPAClient(fs)
        errors = []

        group_name = "tests-tg-" + generate_random_string()
        group_description = "tests-tg-" + generate_random_string()
        group_id = None

        try:
            # Create tag group (tags can be empty)
            tag_group = TagGroup(
                {
                    "name": group_name,
                    "description": group_description,
                    "tags": [],
                }
            )
            created_group, _, err = client.zpa.tag_group.create_tag_group(tag_group)
            assert err is None, f"Error creating tag group: {err}"
            assert created_group is not None
            assert created_group.name == group_name
            assert created_group.description == group_description

            group_id = created_group.id
        except Exception as exc:
            errors.append(f"Error during tag group creation: {exc}")

        try:
            if group_id:
                # Get by ID
                retrieved_group, _, err = client.zpa.tag_group.get_tag_group(group_id)
                assert err is None, f"Error fetching tag group: {err}"
                assert retrieved_group.id == group_id
                assert retrieved_group.name == group_name

                # Update
                updated_name = group_name + " Updated"
                updated_group = TagGroup(
                    {
                        "id": group_id,
                        "name": updated_name,
                        "description": group_description,
                        "tags": [],
                    }
                )
                _, _, err = client.zpa.tag_group.update_tag_group(group_id, updated_group)
                assert err is None, f"Error updating tag group: {err}"

                # Get by name
                got_by_name, _, err = client.zpa.tag_group.get_tag_group_by_name(updated_name)
                assert err is None, f"Error fetching tag group by name: {err}"
                assert got_by_name.id == group_id
                assert got_by_name.name == updated_name

                # List tag groups
                groups_list, _, err = client.zpa.tag_group.list_tag_groups()
                assert err is None, f"Error listing tag groups: {err}"
                assert any(g.id == group_id for g in groups_list)
        except Exception as exc:
            errors.append(f"Tag group operation failed: {exc}")

        finally:
            if group_id:
                try:
                    _, _, err = client.zpa.tag_group.delete_tag_group(group_id)
                    assert err is None, f"Error deleting tag group: {err}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for tag group ID {group_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during the tag group lifecycle test: {errors}"
