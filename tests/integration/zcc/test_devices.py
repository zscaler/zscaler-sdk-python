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
