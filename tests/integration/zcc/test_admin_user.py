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
from tests.integration.zcc.conftest import MockZCCClient


@pytest.fixture
def fs():
    yield


class TestAdminUser:
    """
    Integration Tests for the ZCC Admin User API
    """

    @pytest.mark.vcr()
    def test_list_admin_users(self, fs):
        """Test listing admin users"""
        client = MockZCCClient(fs)
        errors = []

        try:
            admin_users, response, err = client.zcc.admin_user.list_admin_users()
            assert err is None, f"Error listing admin users: {err}"
            assert isinstance(admin_users, list), "Expected a list of admin users"
            
            # Verify response structure if we have users
            if admin_users:
                user = admin_users[0]
                assert hasattr(user, 'as_dict'), "Admin user should have as_dict method"
        except Exception as exc:
            errors.append(f"Listing admin users failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the admin user test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_admin_users_with_pagination(self, fs):
        """Test listing admin users with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            admin_users, response, err = client.zcc.admin_user.list_admin_users(
                query_params={"page": 1, "page_size": 5}
            )
            assert err is None, f"Error listing admin users with pagination: {err}"
            assert isinstance(admin_users, list), "Expected a list of admin users"
            assert len(admin_users) <= 5, "Page size limit should be respected"
        except Exception as exc:
            errors.append(f"Listing admin users with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated admin user test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_admin_user_sync_info(self, fs):
        """Test getting admin user sync information"""
        client = MockZCCClient(fs)
        errors = []

        try:
            sync_info, response, err = client.zcc.admin_user.get_admin_user_sync_info()
            assert err is None, f"Error getting admin user sync info: {err}"
            assert sync_info is not None, "Sync info should not be None"
            assert hasattr(sync_info, 'as_dict'), "Sync info should have as_dict method"
        except Exception as exc:
            errors.append(f"Getting admin user sync info failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the sync info test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_admin_roles(self, fs):
        """Test listing admin roles"""
        client = MockZCCClient(fs)
        errors = []

        try:
            admin_roles, response, err = client.zcc.admin_user.list_admin_roles()
            assert err is None, f"Error listing admin roles: {err}"
            assert isinstance(admin_roles, list), "Expected a list of admin roles"
            
            # Verify response structure if we have roles
            if admin_roles:
                role = admin_roles[0]
                assert hasattr(role, 'as_dict'), "Admin role should have as_dict method"
        except Exception as exc:
            errors.append(f"Listing admin roles failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the admin roles test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_admin_roles_with_pagination(self, fs):
        """Test listing admin roles with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            admin_roles, response, err = client.zcc.admin_user.list_admin_roles(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"Error listing admin roles with pagination: {err}"
            assert isinstance(admin_roles, list), "Expected a list of admin roles"
        except Exception as exc:
            errors.append(f"Listing admin roles with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated admin roles test:\n{chr(10).join(errors)}"

