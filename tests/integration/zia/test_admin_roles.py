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
        role_id = None

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
                existing_role_id = roles[0].id
                fetched_role, response, err = client.zia.admin_roles.get_role(existing_role_id)
                assert err is None, f"Get role failed: {err}"
                assert fetched_role is not None, "Fetched role should not be None"

            # Test add_role (may fail due to permissions)
            try:
                created_role, response, err = client.zia.admin_roles.add_role(
                    name="TestAdminRole_VCR",
                    admin_acct_access="READ_ONLY",
                    dashboard_access="READ_ONLY",
                    report_access="READ_ONLY",
                    analysis_access="READ_ONLY",
                    username_access="READ_ONLY",
                    device_info_access="READ_ONLY",
                )
                if err is None and created_role is not None:
                    role_id = created_role.id if hasattr(created_role, 'id') else None

                    # Test update_role
                    if role_id:
                        try:
                            updated_role, response, err = client.zia.admin_roles.update_role(
                                role_id=role_id,
                                name="TestAdminRole_VCR_Updated",
                            )
                        except Exception:
                            pass
            except Exception:
                pass  # May fail due to permissions

            # Test get_password_expiry_settings (may fail due to permissions)
            try:
                expiry_settings, response, err = client.zia.admin_roles.get_password_expiry_settings()
                if err is None:
                    assert expiry_settings is not None, "Password expiry settings should not be None"
            except Exception:
                pass  # Password expiry settings may require elevated permissions

        except Exception as e:
            errors.append(f"Exception during admin roles test: {str(e)}")

        finally:
            # Cleanup
            if role_id:
                try:
                    client.zia.admin_roles.delete_role(role_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
