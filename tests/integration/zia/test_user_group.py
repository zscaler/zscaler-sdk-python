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
import random


@pytest.fixture
def fs():
    yield


class TestUserGroup:
    """
    Integration Tests for the User Group
    """

    def test_user_groups(self, fs):
        client = MockZIAClient(fs)
        errors = []
        group_id = None
        update_group = None

        try:
            # Test: Add Group
            try:
                create_group, _, error = client.zia.user_management.add_group(
                    name=f"NewGroup_{random.randint(1000, 10000)}",
                    comments=f"NewGroup_{random.randint(1000, 10000)}",
                )
                assert error is None, f"Add Group Error: {error}"
                assert create_group is not None, "Group creation failed."
                group_id = create_group.id
            except Exception as e:
                errors.append(f"Exception during add_group: {str(e)}")

            # Test: Update Group
            try:
                if group_id:
                    update_group, _, error = client.zia.user_management.update_group(
                        group_id=group_id,
                        name=f"UpdateGroup_{random.randint(1000, 10000)}",
                        comments=f"UpdateGroup_{random.randint(1000, 10000)}",
                    )
                    assert error is None, f"Update Group Error: {error}"
                    assert update_group is not None, "Group update returned None."
            except Exception as e:
                errors.append(f"Exception during update_group: {str(e)}")

            # Test: Get Group
            try:
                if update_group:
                    grp, _, error = client.zia.user_management.get_group(update_group.id)
                    assert error is None, f"Get Group Error: {error}"
                    assert grp.id == group_id, "Retrieved group ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_group: {str(e)}")

            # Test: List Groups
            try:
                if update_group:
                    grps, _, error = client.zia.user_management.list_groups(query_params={"search": update_group.name})
                    assert error is None, f"List Groups Error: {error}"
                    assert grps is not None and isinstance(grps, list), "No groups found or invalid format."
            except Exception as e:
                errors.append(f"Exception during list_groups: {str(e)}")

        finally:
            # Ensure Group cleanup
            try:
                if update_group:
                    _, _, error = client.zia.user_management.delete_group(update_group.id)
                    assert error is None, f"Delete Group Error: {error}"
            except Exception as e:
                errors.append(f"Exception during delete_group: {str(e)}")

        # Final Assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
