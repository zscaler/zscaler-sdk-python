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
from tests.test_utils import generate_random_password, generate_random_string


@pytest.fixture
def fs():
    yield


class TestUsers:
    """
    Integration Tests for the User Management
    """

    def test_users(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        user_id = None

        try:
            # Retrieve role ID
            try:
                # Retrieve the first department's ID
                departments = client.users.list_departments(search="A000")
                department_id = departments[0]["id"] if departments else None
                assert department_id, "No departments available for assignment"
            except Exception as exc:
                errors.append(f"Department retrieval failed: {exc}")

            try:
                # Retrieve the first group's ID
                groups = client.users.list_groups(search="A000")
                group_id = groups[0]["id"] if groups else None
                assert group_id, "No groups available for assignment"
            except Exception as exc:
                errors.append(f"Group retrieval failed: {exc}")

            # Create User Account
            if department_id and group_id:
                try:
                    created_user = client.users.add_user(
                        name="tests-" + generate_random_string(),
                        email="tests-" + generate_random_string() + "@bd-hashicorp.com",
                        password=generate_random_password(),
                        groups=[{"id": group_id}],
                        department=({"id": department_id}),
                    )
                    user_id = created_user.get("id", None)
                    assert user_id, "User account creation failed"
                except Exception as exc:
                    errors.append(f"User creation failed: {exc}")

            if user_id:
                try:
                    # Fetch and verify the user
                    retrieved_user = client.users.get_user(user_id)
                    assert retrieved_user["id"] == user_id, "Incorrect user account retrieved"
                except Exception as exc:
                    errors.append(f"Retrieving User Account failed: {exc}")

            # Update the User Account
            if user_id:
                try:
                    updated_password = generate_random_password()  # Generate a new password
                    client.users.update_user(
                        user_id,
                        password=updated_password,
                    )
                except Exception as exc:
                    errors.append(f"Updating User Account password failed: {exc}")

        finally:
            # Cleanup: Attempt to delete the user
            if user_id:
                try:
                    delete_status = client.users.delete_user(user_id)
                    assert delete_status == 204, "User Account deletion failed"
                except Exception as exc:
                    errors.append(f"Deleting User Account failed: {exc}")

            if errors:
                raise AssertionError("Errors occurred during the user management test: " + "; ".join(errors))

    def test_user_departments(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List departments with optional parameters
            depts = client.users.list_departments(page_size=2, max_pages=1)
            assert len(depts) <= 2, "More departments returned than expected with page_size=2"
            assert isinstance(depts, list), "Expected a list of departments"
            if depts:  # If there are any departments
                # Select the first department for further testing
                first_dept = depts[0]
                department_id = first_dept.get("id")

                # Fetch the selected department by its ID
                fetched_dept = client.users.get_department(department_id)
                assert fetched_dept is not None, "Expected a valid department object"
                assert fetched_dept.get("id") == department_id, "Mismatch in department ID"

                # Attempt to retrieve the department by name
                dept_name = fetched_dept.get("name")
                dept_by_name = client.users.get_dept_by_name(dept_name)
                assert dept_by_name is not None, "Expected a valid department object when searching by name"
                assert dept_by_name.get("id") == department_id, "Mismatch in department ID when searching by name"

        except Exception as exc:
            errors.append(f"Test failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during departments test: {errors}"

    def test_user_groups(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List groups with optional parameters
            groups = client.users.list_groups(page_size=2, max_pages=1, sort_order="ASC")
            assert len(groups) <= 2, "More groups returned than expected with page_size=2"
            assert isinstance(groups, list), "Expected a list of groups"
            if groups:
                first_group = groups[0]
                group_id = first_group.get("id")

                # Fetch the selected group by its ID
                fetched_group = client.users.get_group(group_id)
                assert fetched_group is not None, "Expected a valid group object"
                assert fetched_group.get("id") == group_id, "Mismatch in group ID"

                # Attempt to retrieve the group by name
                group_name = fetched_group.get("name")
                group_by_name = client.users.get_group_by_name(group_name)
                assert group_by_name is not None, "Expected a valid group object when searching by name"
                assert group_by_name.get("id") == group_id, "Mismatch in group ID when searching by name"

        except Exception as exc:
            errors.append(f"Test failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during groups test: {errors}"
