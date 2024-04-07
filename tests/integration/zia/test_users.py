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


class TestUsers:
    """
    Integration Tests for the User Management
    """
          
    @pytest.mark.asyncio
    async def test_user_departments(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        try:
            # List all departments
            depts = client.users.list_departments()
            assert isinstance(depts, list), "Expected a list of departments"
            if depts:  # If there are any departments
                # Select the first department for further testing
                first_dept = depts[0]
                department_id = first_dept.get("id")

                # Fetch the selected department by its ID
                try:
                    fetched_dept = client.users.get_department(department_id)
                    assert fetched_dept is not None, "Expected a valid department object"
                    assert (
                        fetched_dept.get("id") == department_id
                    ), "Mismatch in department ID"
                except Exception as exc:
                    errors.append(f"Fetching department by ID failed: {exc}")

                # Attempt to retrieve the department by name
                try:
                    dept_name = fetched_dept.get("name")
                    dept_by_name = client.users.get_dept_by_name(dept_name)
                    assert (
                        dept_by_name is not None
                    ), "Expected a valid department object when searching by name"
                    assert (
                        dept_by_name.get("id") == department_id
                    ), "Mismatch in department ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching department by name failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing departments failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during departments test: {errors}"


    @pytest.mark.asyncio
    async def test_user_groups(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all departments
            groups = client.users.list_groups()
            assert isinstance(groups, list), "Expected a list of departments"
            if groups:  # If there are any departments
                # Select the first group for further testing
                first_group = groups[0]
                group_id = first_group.get("id")

                # Fetch the selected group by its ID
                try:
                    fetched_group = client.users.get_group(group_id)
                    assert fetched_group is not None, "Expected a valid group object"
                    assert (
                        fetched_group.get("id") == group_id
                    ), "Mismatch in group ID"
                except Exception as exc:
                    errors.append(f"Fetching group by ID failed: {exc}")

                # Attempt to retrieve the group by name
                try:
                    group_name = fetched_group.get("name")
                    group_by_name = client.users.get_group_by_name(group_name)
                    assert (
                        group_name is not None
                    ), "Expected a valid group object when searching by name"
                    assert (
                        group_by_name.get("id") == group_id
                    ), "Mismatch in group ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching group by name failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing groups failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during groups test: {errors}"
