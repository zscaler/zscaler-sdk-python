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


@pytest.fixture
def fs():
    yield


class TestMachineGroups:
    """
    Integration Tests for the Machine Groups.
    """

    def test_machine_groups(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        # Attempt to list all machine groups
        try:
            machine_groups = client.machine_groups.list_groups()
            assert isinstance(machine_groups, list), "Expected a list of machine groups"
        except Exception as exc:
            errors.append(f"Listing machine groups failed: {str(exc)}")

        # Process each machine group if the list is not empty
        if machine_groups:
            for first_group in machine_groups:
                group_id = first_group.get("id")

                # Fetch the selected machine group by its ID
                try:
                    fetched_group = client.machine_groups.get_group(group_id)
                    assert fetched_group is not None, "Expected a valid machine group object"
                    assert fetched_group.get("id") == group_id, "Mismatch in machine group ID"
                except Exception as exc:
                    errors.append(f"Fetching machine group by ID failed: {str(exc)}")

                # Attempt to retrieve the machine group by name
                try:
                    group_name = first_group.get("name")
                    group_by_name = client.machine_groups.get_machine_group_by_name(group_name)
                    assert group_by_name is not None, "Expected a valid machine group object when searching by name"
                    assert group_by_name.get("id") == group_id, "Mismatch in machine group ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching machine group by name failed: {str(exc)}")

                # Once we've tested one group, exit the loop to avoid redundant testing
                break

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during machine group operations test: {errors}"
