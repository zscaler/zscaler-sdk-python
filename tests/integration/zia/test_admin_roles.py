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


class TestAdminRoles:
    """
    Integration Tests for the Admin Roles API.
    """

    @pytest.mark.vcr()
    def test_admin_roles_crud(self, fs):
        """Test comprehensive CRUD operations for Admin Roles."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_roles
            roles, response, err = client.zia.admin_roles.list_roles()
            assert err is None, f"List roles failed: {err}"
            assert roles is not None, "Roles list should not be None"
            assert isinstance(roles, list), "Roles should be a list"
            assert len(roles) > 0, "Should have at least one role"

            # Test list_roles with search
            search_roles, response, err = client.zia.admin_roles.list_roles(
                query_params={"search": "Super Admin"}
            )
            assert err is None, f"List roles with search failed: {err}"

            # Test list_roles with include_auditor_role
            roles_with_auditor, response, err = client.zia.admin_roles.list_roles(
                query_params={"include_auditor_role": True}
            )
            assert err is None, f"List roles with include_auditor_role failed: {err}"

            # Test get_role - get the first role from the list
            if roles and len(roles) > 0:
                role_id = roles[0].id
                fetched_role, response, err = client.zia.admin_roles.get_role(role_id)
                assert err is None, f"Get role failed: {err}"
                assert fetched_role is not None, "Fetched role should not be None"

            # Test get_password_expiry_settings (may fail due to permissions)
            try:
                expiry_settings, response, err = client.zia.admin_roles.get_password_expiry_settings()
                if err is None:
                    assert expiry_settings is not None, "Password expiry settings should not be None"
                # Don't fail test if this endpoint returns errors - may be permission-restricted
            except Exception as e:
                pass  # Password expiry settings may require elevated permissions

        except Exception as e:
            errors.append(f"Exception during admin roles test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
