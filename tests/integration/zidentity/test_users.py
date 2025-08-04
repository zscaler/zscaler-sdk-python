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

from tests.integration.zidentity.conftest import MockZIdentityClient
import random


@pytest.fixture
def fs():
    yield


class TestUsers:
    """
    Integration Tests for the Users
    """

    def test_users(self, fs):
        client = MockZIdentityClient(fs)
        errors = []
        user_id = None
        update_user = None

        try:
            # Test: Add Group
            try:
                create_group, _, error = client.zidentity.users.add_user(
                    login_name="john.doe@securitygeek.io",
                    display_name="John Doe",
                    first_name='John',
                    last_name='Doe',
                    primary_email='john.doe@securitygeek.io',
                    secondary_email='jdoe@acme.com',
                    status=True,
                )
                assert error is None, f"Add User Error: {error}"
                assert create_group is not None, "User creation failed."
                user_id = create_group.id
            except Exception as e:
                errors.append(f"Exception during add_user: {str(e)}")

            # Test: Update User
            try:
                if user_id:
                    update_user, _, error = client.zidentity.users.update_user(
                        user_id=user_id,
                        login_name="john.doe@securitygeek.io",
                        display_name="John Doe",
                        first_name='John',
                        last_name='Doe',
                        primary_email='john.doe@securitygeek.io',
                        secondary_email='jdoe1@acme.com',
                        status=True,
                    )
                    assert error is None, f"Update User Error: {error}"
                    assert update_user is not None, "User update returned None."
            except Exception as e:
                errors.append(f"Exception during update_user: {str(e)}")

            # Test: Get Group
            try:
                if update_user:
                    user, _, error = client.zidentity.users.get_user(update_user.id)
                    assert error is None, f"Get User Error: {error}"
                    assert user.id == user_id, "Retrieved User ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_user: {str(e)}")

            # Test: List Groups
            try:
                if update_user:
                    users, _, error = client.zidentity.users.list_users()
                    assert error is None, f"List Users Error: {error}"
                    assert users is not None and isinstance(users, list), "No groups found or invalid format."
            except Exception as e:
                errors.append(f"Exception during list_users: {str(e)}")

        finally:
            # Cleanup: Delete the portal if it was created
            if user_id:
                try:
                    delete_response, _, err = client.zidentity.users.delete_user(user_id)
                    assert err is None, f"Error deleting portal: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for portal ID {user_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the portal lifecycle test: {errors}"