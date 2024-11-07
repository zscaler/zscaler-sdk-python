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


@pytest.fixture
def fs():
    yield


class TestLocationGroup:
    """
    Integration Tests for the Location Group.
    """

    def test_location_group(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        group_id = None

        try:
            # List all groups
            groups = client.locations.list_location_groups()
            assert isinstance(groups, list), "Expected a list of groups"

            # Use lite version to list location groups with minimal details
            try:
                lite_groups = client.locations.list_location_groups_lite()
                assert isinstance(lite_groups, list), "Expected a lite list of groups"
            except Exception as exc:
                errors.append(f"Listing lite groups failed: {exc}")

            if groups:  # If there are any groups
                # Select the first group for further testing
                first_group = groups[0]
                group_id = first_group.get("id")

                # Fetch the selected group by its ID
                try:
                    fetched_group = client.locations.get_location_group_by_id(group_id)
                    assert fetched_group is not None, "Expected a valid group object"
                    assert fetched_group.get("id") == group_id, "Mismatch in group ID"
                except Exception as exc:
                    errors.append(f"Fetching group by ID failed: {exc}")

                # Fetch lite version by ID
                try:
                    fetched_lite_group = client.locations.get_location_group_lite_by_id(group_id)
                    assert fetched_lite_group is not None, "Expected a valid lite group object"
                    assert fetched_lite_group.get("id") == group_id, "Mismatch in lite group ID"
                except Exception as exc:
                    errors.append(f"Fetching lite group by ID failed: {exc}")

            # Use lite version to list location groups with minimal details
            try:
                lite_count = client.locations.list_location_groups_count()
                assert isinstance(lite_count, int), "Expected the count of all groups to be an integer"
            except Exception as exc:
                errors.append(f"Listing the count of all groups failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing groups failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during groups test: {errors}"
