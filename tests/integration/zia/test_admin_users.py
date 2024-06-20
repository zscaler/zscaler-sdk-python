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


class TestAdminUsers:
    """
    Integration Tests for the Admin User Management
    """

    def test_admin_users(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        user_id = None

        try:
            # Retrieve role ID
            try:
                roles = client.admin_and_role_management.list_roles()
                assert isinstance(roles, list), "Expected a list of roles"
                role_id = roles[0].get("id") if roles else None
                assert role_id, "No roles available for assignment"
            except Exception as exc:
                errors.append(f"Listing roles failed: {str(exc)}")

            # Retrieve department IDs
            try:
                departments = client.users.list_departments()
                assert isinstance(departments, list), "Expected a list of departments"
                scope_ids = [departments[0]["id"], departments[1]["id"]] if len(departments) > 1 else []
                assert len(scope_ids) == 2, "Insufficient departments available for assignment"
            except Exception as exc:
                errors.append(f"Department retrieval failed: {exc}")

            # Create Admin User Account
            if role_id and scope_ids:
                try:
                    created_user = client.admin_and_role_management.add_user(
                        name="tests-" + generate_random_string(),
                        login_name="tests-" + generate_random_string() + "@bd-hashicorp.com",
                        email="tests-" + generate_random_string() + "@bd-hashicorp.com",
                        password=generate_random_password(),
                        admin_scope="department",
                        role_id=role_id,
                        scope_ids=scope_ids,
                    )
                    user_id = created_user.get("id", None)
                    assert user_id, "User account creation failed"
                except Exception as exc:
                    errors.append(f"Admin User creation failed: {exc}")

            # Fetch and verify the user
            if user_id:
                try:
                    retrieved_user = client.admin_and_role_management.get_user(user_id)
                    assert retrieved_user["id"] == user_id, "Incorrect admin user account retrieved"
                except Exception as exc:
                    errors.append(f"Retrieving User Account failed: {exc}")

            # Update the User Account
            if user_id:
                try:
                    updated_password = generate_random_password()  # Generate a new password
                    client.admin_and_role_management.update_user(
                        user_id,
                        password=updated_password,
                    )
                except Exception as exc:
                    errors.append(f"Updating User Account password failed: {exc}")

        finally:
            # Cleanup: Attempt to delete the network services
            if user_id:
                try:
                    delete_status = client.admin_and_role_management.delete_user(user_id)
                    assert delete_status == 204, "User Account deletion failed"
                except Exception as exc:
                    errors.append(f"Deleting User Account failed: {exc}")

            if errors:
                raise AssertionError("Errors occurred during the user management test: " + "; ".join(errors))
