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
    Integration Tests for the Machine Groups
    """

    @pytest.mark.asyncio
    async def test_machine_groups(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all machine groups
            machine_groups = client.machine_groups.list_groups()
            assert isinstance(machine_groups, list), "Expected a list of machine groups"
            if machine_groups:  # If there are any machine groups
                # Select the first machine group for further testing
                first_group = machine_groups[0]
                group_id = first_group.get("id")

                # Fetch the selected machine group by its ID
                fetched_group = client.machine_groups.get_group(group_id)
                assert (
                    fetched_group is not None
                ), "Expected a valid machine group object"
                assert (
                    fetched_group.get("id") == group_id
                ), "Mismatch in machine group ID"

                # Attempt to retrieve the machine group by name
                group_name = first_group.get("name")
                group_by_name = client.machine_groups.get_machine_group_by_name(
                    group_name
                )
                assert (
                    group_by_name is not None
                ), "Expected a valid machine group object when searching by name"
                assert (
                    group_by_name.get("id") == group_id
                ), "Mismatch in machine group ID when searching by name"
        except Exception as exc:
            errors.append(exc)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during machine groups test: {errors}"