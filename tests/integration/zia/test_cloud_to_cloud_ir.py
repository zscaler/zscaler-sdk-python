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


class TestCloudToCloudIR:
    """
    Integration Tests for the Cloud to Cloud IR API.
    """

    @pytest.mark.vcr()
    def test_cloud_to_cloud_ir_operations(self, fs):
        """Test Cloud to Cloud IR operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_cloud_to_cloud_ir
            c2c_list, response, err = client.zia.cloud_to_cloud_ir.list_cloud_to_cloud_ir()
            assert err is None, f"List cloud to cloud IR failed: {err}"
            assert c2c_list is not None, "C2C list should not be None"
            assert isinstance(c2c_list, list), "C2C list should be a list"

            # Test list_cloud_to_cloud_ir_lite
            c2c_lite, response, err = client.zia.cloud_to_cloud_ir.list_cloud_to_cloud_ir_lite()
            assert err is None, f"List cloud to cloud IR lite failed: {err}"

            # Test list_c2c_count
            c2c_count, response, err = client.zia.cloud_to_cloud_ir.list_c2c_count()
            assert err is None, f"List C2C count failed: {err}"

            # Test get_cloud_to_cloud_ir with first item if available
            if c2c_list and len(c2c_list) > 0:
                c2c_id = c2c_list[0].id
                fetched_c2c, response, err = client.zia.cloud_to_cloud_ir.get_cloud_to_cloud_ir(c2c_id)
                assert err is None, f"Get cloud to cloud IR failed: {err}"
                assert fetched_c2c is not None, "Fetched C2C should not be None"

        except Exception as e:
            errors.append(f"Exception during cloud to cloud IR test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
