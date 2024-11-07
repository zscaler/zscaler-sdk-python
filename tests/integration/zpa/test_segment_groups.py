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


class TestSegmentGroup:
    """
    Integration Tests for the Segment Group
    """

    def test_segment_group(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        segment_group_name = "tests-" + generate_random_string()
        segment_group_description = "tests-" + generate_random_string()

        try:
            # Create a new segment group
            created_group = client.segment_groups.add_group(
                name=segment_group_name,
                description=segment_group_description,
                enabled=True,
            )
            assert created_group is not None
            assert created_group.name == segment_group_name
            assert created_group.description == segment_group_description
            assert created_group.enabled is True

            group_id = created_group.id
        except Exception as exc:
            errors.append(exc)

        try:
            # Retrieve the created segment group by ID
            retrieved_group = client.segment_groups.get_group(group_id)
            assert retrieved_group.id == group_id
            assert retrieved_group.name == segment_group_name
        except Exception as exc:
            errors.append(exc)

        try:
            # Update the segment group
            updated_name = segment_group_name + " Updated"
            client.segment_groups.update_group(group_id, name=updated_name)

            updated_group = client.segment_groups.get_group(group_id)
            assert updated_group.name == updated_name
        except Exception as exc:
            errors.append(exc)

        try:
            # Update the segment group
            updated_name = segment_group_name + " Updated"
            client.segment_groups.update_group_v2(group_id, name=updated_name)

            updated_group = client.segment_groups.get_group(group_id)
            assert updated_group.name == updated_name
        except Exception as exc:
            errors.append(exc)

        try:
            # List segment groups and ensure the updated group is in the list
            groups_list = client.segment_groups.list_groups()
            assert any(group.id == group_id for group in groups_list)
        except Exception as exc:
            errors.append(exc)

        try:
            # Search for the segment group by name
            search_result = client.segment_groups.get_segment_group_by_name(updated_name)
            assert search_result is not None
            assert search_result.id == group_id
        except Exception as exc:
            errors.append(exc)

        try:
            # Delete the segment group
            delete_response_code = client.segment_groups.delete_group(group_id)
            assert str(delete_response_code) == "204"
        except Exception as exc:
            errors.append(exc)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the segment group lifecycle test: {errors}"
