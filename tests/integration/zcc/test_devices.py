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

    def test_download_devices(self, fs):
        client = MockZCCClient(fs)
        errors = []

        try:
            # Test case: Download devices with specific OS types and registration types
            try:
                filename = client.devices.download_devices(
                    filename="test_devices.csv", os_types=["windows", "macos"], registration_types=["registered"]
                )
                assert filename == "test_devices.csv", "Filename mismatch"
                assert os.path.exists(filename), "File not found after download"
            except Exception as exc:
                errors.append(f"Download devices with specific filters failed: {exc}")

            # Test case: Download devices without specifying any filters
            try:
                filename = client.devices.download_devices(filename="all_devices.csv")
                assert filename == "all_devices.csv", "Filename mismatch"
                assert os.path.exists(filename), "File not found after download"
            except Exception as exc:
                errors.append(f"Download all devices failed: {exc}")

        finally:
            # Cleanup: Remove any downloaded files
            try:
                os.remove("test_devices.csv")
                os.remove("all_devices.csv")
            except Exception as exc:
                errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the download devices test: {errors}"

    def test_list_devices(self, fs):
        client = MockZCCClient(fs)
        errors = []

        try:
            # Test case: List devices with a specific OS type
            # try:
            #     devices = client.devices.list_devices(os_type="windows", page=1, page_size=10)
            #     assert isinstance(devices, list), "Expected a list of devices"
            #     assert len(devices) <= 10, "Page size limit exceeded"
            # except Exception as exc:
            #     errors.append(f"Listing devices with specific OS type failed: {exc}")

            # Test case: List devices without any filters
            try:
                devices = client.devices.list_devices()
                assert isinstance(devices, list), "Expected a list of devices"
            except Exception as exc:
                errors.append(f"Listing all devices failed: {exc}")

        # Assert that no errors occurred during the test
        finally:
            assert len(errors) == 0, f"Errors occurred during the list devices test: {errors}"
