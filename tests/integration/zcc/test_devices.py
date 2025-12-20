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
import os
from tests.integration.zcc.conftest import MockZCCClient


@pytest.fixture
def fs():
    yield


class TestDevice:
    """
    Integration Tests for the ZCC Devices
    """

    #     def test_download_devices(self, fs):
    #         client = MockZCCClient(fs)
    #         errors = []

    #         test_file_1 = "test_devices.csv"
    #         test_file_2 = "all_devices.csv"

    #         try:
    #             # Test 1: Download with filters
    #             try:
    #                 downloaded_file, response, err = None, None, None
    #                 try:
    #                     downloaded_file = client.zcc.devices.download_devices(
    #                         filename=test_file_1,
    #                         os_types=["windows", "macos"],
    #                         registration_types=["registered"]
    #                     )
    #                 except Exception as exc:
    #                     err = str(exc)

    #                 assert downloaded_file == test_file_1, "Filename mismatch"
    #                 assert os.path.exists(downloaded_file), "File not found after download"
    #                 assert err is None, f"Error downloading devices with filters: {err}"
    #             except Exception as exc:
    #                 errors.append(f"Download with filters failed: {exc}")

    #             # Test 2: Download without filters
    #             try:
    #                 downloaded_file, response, err = None, None, None
    #                 try:
    #                     downloaded_file = client.zcc.devices.download_devices(filename=test_file_2)
    #                 except Exception as exc:
    #                     err = str(exc)

    #                 assert downloaded_file == test_file_2, "Filename mismatch"
    #                 assert os.path.exists(downloaded_file), "File not found after download"
    #                 assert err is None, f"Error downloading devices without filters: {err}"
    #             except Exception as exc:
    #                 errors.append(f"Download without filters failed: {exc}")

    #         finally:
    #             for file in [test_file_1, test_file_2]:
    #                 try:
    #                     if os.path.exists(file):
    #                         os.remove(file)
    #                 except Exception as exc:
    #                     errors.append(f"Cleanup failed for {file}: {exc}")

    #         assert not errors, f"Errors occurred during the ZCC device download test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_devices(self, fs):
        client = MockZCCClient(fs)
        errors = []

        try:
            # Test case: List devices with a specific OS type
            try:
                devices, _, err = client.zcc.devices.list_devices(query_params={"os_type": "windows", "page": 1, "page_size": 10})
                assert err is None, f"Error occurred while listing with OS filter: {err}"
                assert isinstance(devices, list), "Expected a list of devices"
                assert len(devices) <= 10, "Page size limit exceeded"
            except Exception as exc:
                errors.append(f"Listing devices with specific OS type failed: {exc}")

            # Test case: List devices without any filters
            try:
                devices, _, err = client.zcc.devices.list_devices()
                assert err is None, f"Error occurred while listing all devices: {err}"
                assert isinstance(devices, list), "Expected a list of devices"
            except Exception as exc:
                errors.append(f"Listing all devices failed: {exc}")

        finally:
            assert len(errors) == 0, f"Errors occurred during the list devices test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_devices_with_username(self, fs):
        """Test listing devices filtered by username"""
        client = MockZCCClient(fs)
        errors = []

        try:
            # Use a test username - this should be a valid username in the test environment
            # The VCR cassette will record the actual response
            test_username = "adam.ashcroft@securitygeek.io"
            
            devices, _, err = client.zcc.devices.list_devices(
                query_params={"username": test_username, "page": 1, "page_size": 10}
            )
            assert err is None, f"Error occurred while listing devices by username: {err}"
            assert isinstance(devices, list), "Expected a list of devices"
        except Exception as exc:
            errors.append(f"Listing devices by username failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the list devices by username test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_devices_with_different_os_types(self, fs):
        """Test listing devices with different OS types"""
        client = MockZCCClient(fs)
        errors = []

        os_types = ["windows", "macos", "ios", "android", "linux"]

        for os_type in os_types:
            try:
                devices, _, err = client.zcc.devices.list_devices(
                    query_params={"os_type": os_type, "page": 1, "page_size": 5}
                )
                assert err is None, f"Error occurred while listing devices for {os_type}: {err}"
                assert isinstance(devices, list), f"Expected a list of devices for {os_type}"
            except Exception as exc:
                errors.append(f"Listing devices for OS type {os_type} failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the list devices OS types test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_device_details(self, fs):
        """Test getting device details"""
        client = MockZCCClient(fs)
        errors = []

        try:
            # First get a device to use its identifier
            devices, _, err = client.zcc.devices.list_devices(query_params={"page": 1, "page_size": 1})
            if err is None and devices and len(devices) > 0:
                device = devices[0]
                username = device.user if hasattr(device, 'user') else device.get('user')
                udid = device.udid if hasattr(device, 'udid') else device.get('udid')
                
                if username:
                    details, _, err = client.zcc.devices.get_device_details(
                        query_params={"username": username}
                    )
                    if err is None:
                        assert details is not None, "Device details should not be None"
                        assert hasattr(details, 'as_dict'), "Device details should have as_dict method"
                
                if udid:
                    details, _, err = client.zcc.devices.get_device_details(
                        query_params={"udid": udid}
                    )
                    if err is None:
                        assert details is not None, "Device details should not be None"
        except Exception as exc:
            errors.append(f"Getting device details failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the get device details test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_device_cleanup_info(self, fs):
        """Test getting device cleanup information"""
        client = MockZCCClient(fs)
        errors = []

        try:
            cleanup_info, response, err = client.zcc.devices.get_device_cleanup_info()
            assert err is None, f"Error getting device cleanup info: {err}"
            # Cleanup info can be None or a list/object
        except Exception as exc:
            errors.append(f"Getting device cleanup info failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the get device cleanup info test:\n{chr(10).join(errors)}"
