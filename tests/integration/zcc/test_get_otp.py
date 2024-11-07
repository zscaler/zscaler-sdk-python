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


class TestSecrets:
    """
    Integration Tests for the ZCC OTP Secrets
    """

    # def test_get_otp(self, fs):
    #     client = MockZCCClient(fs)
    #     errors = []

    #     try:
    #         # Test case: List devices and retrieve OTP for a specific device
    #         try:
    #             # List all devices
    #             devices = client.devices.list_devices()
    #             assert isinstance(devices, list), "Expected a list of devices"

    #             # Export the 'udid' attribute of the first device in the list
    #             if devices:
    #                 udid = devices[0].get('udid')
    #                 assert udid is not None, "UDID not found in the device data"

    #                 # Invoke the get_otp method using the udid
    #                 otp_response = client.secrets.get_otp(device_id=udid)

    #                 # Check that all expected OTP fields are present
    #                 expected_otp_fields = [
    #                     'logout_otp',
    #                     'revert_otp',
    #                     'uninstall_otp',
    #                     'exit_otp',
    #                     'zia_disable_otp',
    #                     'zpa_disable_otp',
    #                     'zdx_disable_otp'
    #                 ]

    #                 for field in expected_otp_fields:
    #                     assert field in otp_response, f"{field} not found in the response"

    #             else:
    #                 errors.append("No devices found to test OTP retrieval.")

    #         except Exception as exc:
    #             errors.append(f"Listing devices or retrieving OTP failed: {exc}")

    #     # Assert that no errors occurred during the test
    #     finally:
    #         assert len(errors) == 0, f"Errors occurred during the get OTP test: {errors}"

    def test_get_passwords(self, fs):
        client = MockZCCClient(fs)
        errors = []

        try:
            # Test case: List devices and retrieve passwords for the first device
            try:
                # List all devices
                devices = client.devices.list_devices()
                assert isinstance(devices, list), "Expected a list of devices"

                # Ensure we have devices to test with
                if devices:
                    for device in devices:

                        # Extract 'user' attribute from the device
                        username = device.get("user")
                        assert username is not None, "Username not found in the device data"

                        # Invoke the get_passwords method using the extracted username and os_type as 'macos'
                        try:
                            password_response = client.secrets.get_passwords(username=username, os_type="windows")
                            assert isinstance(password_response, dict), "Expected a dictionary containing passwords"
                        except Exception as exc:
                            errors.append(f"Retrieving passwords for user {username} failed: {exc}")

                else:
                    errors.append("No devices found to test password retrieval.")

            except Exception as exc:
                errors.append(f"Listing devices failed: {exc}")

        # Assert that no errors occurred during the test
        finally:
            assert len(errors) == 0, f"Errors occurred during the password test: {errors}"
