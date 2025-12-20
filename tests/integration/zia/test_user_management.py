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


class TestUserManagement:
    """
    Integration Tests for the User Management API.
    """

    @pytest.mark.vcr()
    def test_user_management_operations(self, fs):
        """Test User Management operations - list/get for users, CRUD for groups and departments."""
        client = MockZIAClient(fs)
        errors = []
        created_group_id = None
        created_dept_id = None

        try:
            # ============ USERS (List/Get only) ============
            # Test list_users
            users, response, err = client.zia.user_management.list_users()
            assert err is None, f"List users failed: {err}"
            assert users is not None, "Users list should not be None"
            assert isinstance(users, list), "Users should be a list"

            # Test list_user_references
            users_ref, response, err = client.zia.user_management.list_user_references()
            assert err is None, f"List user references failed: {err}"

            # Test get_user with first user if available
            if users and len(users) > 0:
                user_id = users[0].id
                fetched_user, response, err = client.zia.user_management.get_user(user_id)
                assert err is None, f"Get user failed: {err}"
                assert fetched_user is not None, "Fetched user should not be None"

            # ============ GROUPS (Full CRUD) ============
            # Test list_groups
            groups, response, err = client.zia.user_management.list_groups()
            assert err is None, f"List groups failed: {err}"
            assert groups is not None, "Groups list should not be None"

            # Test get_group with first group if available
            if groups and len(groups) > 0:
                group_id = groups[0].id
                fetched_group, response, err = client.zia.user_management.get_group(group_id)
                assert err is None, f"Get group failed: {err}"
                assert fetched_group is not None, "Fetched group should not be None"

            # Test add_group
            added_group, response, err = client.zia.user_management.add_group(name="TestGroup_VCR_Integration")
            if err is None and added_group:
                created_group_id = added_group.id

                # Test update_group
                updated_group, response, err = client.zia.user_management.update_group(
                    group_id=created_group_id, name="TestGroup_VCR_Integration_Updated"
                )
                if err is None:
                    assert updated_group is not None, "Updated group should not be None"

            # ============ DEPARTMENTS (Full CRUD) ============
            # Test list_departments
            departments, response, err = client.zia.user_management.list_departments()
            assert err is None, f"List departments failed: {err}"
            assert departments is not None, "Departments list should not be None"

            # Test get_department with first department if available
            if departments and len(departments) > 0:
                dept_id = departments[0].id
                fetched_dept, response, err = client.zia.user_management.get_department(dept_id)
                assert err is None, f"Get department failed: {err}"
                assert fetched_dept is not None, "Fetched department should not be None"

            # Test add_department
            added_dept, response, err = client.zia.user_management.add_department(name="TestDept_VCR_Integration")
            if err is None and added_dept:
                created_dept_id = added_dept.id

                # Test update_department
                updated_dept, response, err = client.zia.user_management.update_department(
                    department_id=created_dept_id, name="TestDept_VCR_Integration_Updated"
                )
                if err is None:
                    assert updated_dept is not None, "Updated department should not be None"

        except Exception as e:
            errors.append(f"Exception during user management test: {str(e)}")

        finally:
            # Cleanup: delete created group
            if created_group_id:
                try:
                    client.zia.user_management.delete_group(group_id=created_group_id)
                except Exception:
                    pass

            # Cleanup: delete created department
            if created_dept_id:
                try:
                    client.zia.user_management.delete_department(deparment_id=created_dept_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
