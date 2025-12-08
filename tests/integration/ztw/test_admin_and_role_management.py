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
from tests.integration.ztw.conftest import MockZTWClient


@pytest.fixture
def fs():
    yield


class TestAdminRole:
    """
    Integration Tests for the admin roles
    """

    @pytest.mark.vcr()
    def test_admin_role_management(self, fs):
        client = MockZTWClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all roles
            roles = client.ztw.admin_roles.list_roles()
            assert isinstance(roles, list), "Expected a list of roles"
            if roles:  # If there are any roles
                # Select the first role for further testing
                first_role = roles[0]
                role_id = first_role.id if hasattr(first_role, 'id') else first_role.get("id")

        except Exception as exc:
            errors.append(f"Listing roles failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during roles test: {errors}"
