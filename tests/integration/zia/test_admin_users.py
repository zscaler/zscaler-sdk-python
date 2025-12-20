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

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestAdminUsers:
    """
    Integration Tests for the Admin Users.
    
    Note: For Zidentity-enabled tenants, admin user endpoints may return empty lists.
    """

    @pytest.mark.vcr()
    def test_admin_users(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            # Step 1: List admin users
            try:
                users, _, error = client.zia.admin_users.list_admin_users()
                assert error is None, f"Error listing admin users: {error}"
                assert users is not None, "Admin user list is None"
                # Note: For Zidentity-enabled tenants, this might return an empty list
            except Exception as exc:
                errors.append(f"Failed to list admin users: {exc}")

            # Step 2: List admin users with include_auditor_users parameter
            try:
                users_with_auditor, _, error = client.zia.admin_users.list_admin_users(
                    query_params={"include_auditor_users": True}
                )
                assert error is None, f"Error listing admin users with auditor: {error}"
                assert users_with_auditor is not None, "Admin users with auditor list is None"
            except Exception as exc:
                errors.append(f"Failed to list admin users with auditor parameter: {exc}")

            # Step 3: Get a specific admin user by ID (if any users exist)
            try:
                if users and len(users) > 0:
                    first_user_id = users[0].id
                    user, _, error = client.zia.admin_users.get_admin_user(first_user_id)
                    assert error is None, f"Error getting admin user by ID: {error}"
                    assert user is not None, "Admin user is None"
                    assert user.id == first_user_id, "Admin user ID mismatch"
            except Exception as exc:
                errors.append(f"Failed to get admin user by ID: {exc}")

        except Exception as exc:
            errors.append(f"Unexpected error: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
