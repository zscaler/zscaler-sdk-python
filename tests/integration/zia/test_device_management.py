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


class TestDeviceManagement:
    """
    Integration Tests for the Device Management API.
    """

    @pytest.mark.vcr()
    def test_device_management_operations(self, fs):
        """Test Device Management operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_device_groups
            device_groups, response, err = client.zia.device_management.list_device_groups()
            assert err is None, f"List device groups failed: {err}"
            assert device_groups is not None, "Device groups list should not be None"
            assert isinstance(device_groups, list), "Device groups should be a list"

            # Test list_devices
            devices, response, err = client.zia.device_management.list_devices()
            assert err is None, f"List devices failed: {err}"
            assert devices is not None, "Devices list should not be None"
            assert isinstance(devices, list), "Devices should be a list"

            # Test list_device_lite
            devices_lite, response, err = client.zia.device_management.list_device_lite()
            assert err is None, f"List devices lite failed: {err}"
            assert devices_lite is not None, "Devices lite list should not be None"

        except Exception as e:
            errors.append(f"Exception during device management test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
