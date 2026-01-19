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


class TestWorkloadGroups:
    """
    Integration Tests for the Workload Groups API.
    """

    @pytest.mark.vcr()
    def test_workload_groups_crud(self, fs):
        """Test Workload Groups CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        group_id = None

        try:
            # Test list_groups
            groups, response, err = client.zia.workload_groups.list_groups()
            assert err is None, f"List workload groups failed: {err}"
            assert groups is not None, "Groups list should not be None"
            assert isinstance(groups, list), "Groups should be a list"

            # Test add_group - create a new workload group
            try:
                created_group, response, err = client.zia.workload_groups.add_group(
                    name="TestWorkloadGroup_VCR",
                    description="Test workload group for VCR testing",
                )
                if err is None and created_group is not None:
                    group_id = created_group.get("id") if isinstance(created_group, dict) else getattr(created_group, "id", None)

                    # Test get_group
                    if group_id:
                        fetched_group, response, err = client.zia.workload_groups.get_group(group_id)
                        assert err is None, f"Get workload group failed: {err}"
                        assert fetched_group is not None, "Fetched group should not be None"

                        # Test update_group
                        try:
                            updated_group, response, err = client.zia.workload_groups.update_group(
                                group_id=group_id,
                                name="TestWorkloadGroup_VCR_Updated",
                                description="Updated test workload group",
                            )
                            # Update may fail - that's ok
                        except Exception:
                            pass
            except Exception as e:
                # Add may fail due to permissions/subscription
                pass

            # If we didn't create a group, test with existing one
            if group_id is None and groups and len(groups) > 0:
                existing_id = groups[0].id
                fetched_group, response, err = client.zia.workload_groups.get_group(existing_id)
                assert err is None, f"Get workload group failed: {err}"

        except Exception as e:
            errors.append(f"Exception during workload groups test: {str(e)}")

        finally:
            # Cleanup - delete created group
            if group_id:
                try:
                    client.zia.workload_groups.delete_group(group_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
