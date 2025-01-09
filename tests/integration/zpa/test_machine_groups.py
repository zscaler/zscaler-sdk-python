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


@pytest.fixture
def fs():
    yield


class TestMachineGroups:
    """
    Integration Tests for the Machine Groups.
    """

    def test_machine_group(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        group_id = None

        # List all machine groups
        try:
            groups_response, _, err = client.zpa.machine_groups.list_machine_groups()  # Correctly unpack the tuple
            assert err is None, f"Error listing machine groups: {err}"
            assert isinstance(groups_response, list), "Expected a list of machine groups"
            if groups_response:  # If there are any machine groups, proceed with further operations
                first_group = groups_response[0]
                group_id = first_group.id  # Access the 'id' attribute using dot notation
                assert group_id is not None, "Machine Group ID should not be None"
        except Exception as exc:
            errors.append(f"Listing machine groups failed: {str(exc)}")
            
        if group_id:
            # Fetch the selected machine group by its ID
            try:
                fetched_group, _, err = client.zpa.machine_groups.get_group(group_id)
                assert err is None, f"Error fetching machine group by ID: {err}"
                assert fetched_group is not None, "Expected a valid machine group object"
                assert fetched_group.id == group_id, "Mismatch in machine group ID"  # Use dot notation for object access
            except Exception as exc:
                errors.append(f"Fetching machine group by ID failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during machine group operations test: {errors}"
