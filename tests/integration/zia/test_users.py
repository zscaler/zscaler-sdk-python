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


class TestUsers:
    """
    Integration Tests for the User Management.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_list_users(self, fs):
        """Test listing users."""
        client = MockZIAClient(fs)

        users, _, error = client.zia.user_management.list_users()
        assert error is None, f"Error listing users: {error}"
        assert users is not None, "Users list is None"
        assert isinstance(users, list), "Users is not a list"

    @pytest.mark.vcr()
    def test_list_departments(self, fs):
        """Test listing departments."""
        client = MockZIAClient(fs)

        departments, _, error = client.zia.user_management.list_departments()
        assert error is None, f"Error listing departments: {error}"
        assert departments is not None, "Departments list is None"
        assert isinstance(departments, list), "Departments is not a list"

    @pytest.mark.vcr()
    def test_list_groups(self, fs):
        """Test listing user groups."""
        client = MockZIAClient(fs)

        groups, _, error = client.zia.user_management.list_groups()
        assert error is None, f"Error listing groups: {error}"
        assert groups is not None, "Groups list is None"
        assert isinstance(groups, list), "Groups is not a list"
