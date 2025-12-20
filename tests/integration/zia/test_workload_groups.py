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
        """Test Workload Groups operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_groups
            groups, response, err = client.zia.workload_groups.list_groups()
            assert err is None, f"List workload groups failed: {err}"
            assert groups is not None, "Groups list should not be None"
            assert isinstance(groups, list), "Groups should be a list"

            # Test get_group with first group if available
            if groups and len(groups) > 0:
                group_id = groups[0].id
                fetched_group, response, err = client.zia.workload_groups.get_group(group_id)
                assert err is None, f"Get workload group failed: {err}"
                assert fetched_group is not None, "Fetched group should not be None"

        except Exception as e:
            errors.append(f"Exception during workload groups test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
