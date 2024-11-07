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


class TestAdminRole:
    """
    Integration Tests for the admin roles
    """

    def test_admin_role_management(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all roles
            roles = client.admin_and_role_management.list_roles()
            assert isinstance(roles, list), "Expected a list of roles"
            if roles:  # If there are any roles
                # Select the first role for further testing
                first_role = roles[0]
                role_id = first_role.get("id")

                # Fetch the selected role by its ID
                try:
                    fetched_role = client.admin_and_role_management.get_role(role_id)
                    assert fetched_role is not None, "Expected a valid role object"
                    assert fetched_role.get("id") == role_id, "Mismatch in role ID"
                except Exception as exc:
                    errors.append(f"Fetching role by ID failed: {exc}")

                # Attempt to retrieve the role by name
                try:
                    role_name = first_role.get("name")
                    role_by_name = client.admin_and_role_management.get_roles_by_name(role_name)
                    assert role_by_name is not None, "Expected a valid role object when searching by name"
                    assert role_by_name.get("id") == role_id, "Mismatch in role ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching role by name failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing roles failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during roles test: {errors}"
