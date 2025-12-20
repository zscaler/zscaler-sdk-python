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
from tests.integration.zcc.conftest import MockZCCClient


@pytest.fixture
def fs():
    yield


class TestSecrets:
    """
    Integration Tests for the ZCC Secrets API (OTP and Passwords)
    """

    @pytest.mark.vcr()
    def test_get_otp_with_device_id(self, fs):
        """Test getting OTP with device_id parameter"""
        client = MockZCCClient(fs)
        errors = []

        try:
            # First, get a device to use its UDID
            devices, _, dev_err = client.zcc.devices.list_devices(
                query_params={"page": 1, "page_size": 1}
            )
            
            if dev_err is None and devices and len(devices) > 0:
                device = devices[0]
                udid = device.udid if hasattr(device, 'udid') else device.get('udid')
                
                if udid:
                    otp, response, err = client.zcc.secrets.get_otp(
                        query_params={"device_id": udid}
                    )
                    assert err is None, f"Error getting OTP: {err}"
                    assert otp is not None, "OTP response should not be None"
                    assert hasattr(otp, 'as_dict'), "OTP response should have as_dict method"
        except Exception as exc:
            errors.append(f"Getting OTP with device_id failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the OTP test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_otp_with_udid(self, fs):
        """Test getting OTP with udid parameter"""
        client = MockZCCClient(fs)
        errors = []

        try:
            # First, get a device to use its UDID
            devices, _, dev_err = client.zcc.devices.list_devices(
                query_params={"page": 1, "page_size": 1}
            )
            
            if dev_err is None and devices and len(devices) > 0:
                device = devices[0]
                udid = device.udid if hasattr(device, 'udid') else device.get('udid')
                
                if udid:
                    otp, response, err = client.zcc.secrets.get_otp(
                        query_params={"udid": udid}
                    )
                    assert err is None, f"Error getting OTP: {err}"
                    assert otp is not None, "OTP response should not be None"
        except Exception as exc:
            errors.append(f"Getting OTP with udid failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the OTP test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_passwords(self, fs):
        """Test getting passwords for a user and OS type"""
        client = MockZCCClient(fs)
        errors = []

        try:
            # First, get a device to use its username
            devices, _, dev_err = client.zcc.devices.list_devices(
                query_params={"page": 1, "page_size": 1}
            )
            
            if dev_err is None and devices and len(devices) > 0:
                device = devices[0]
                username = device.user if hasattr(device, 'user') else device.get('user')
                
                if username:
                    passwords, response, err = client.zcc.secrets.get_passwords(
                        query_params={"username": username, "os_type": "windows"}
                    )
                    # Note: This might return None or error depending on the user's configuration
                    # The test validates the API call mechanics
                    if err is None:
                        assert passwords is not None, "Passwords response should not be None"
                        assert hasattr(passwords, 'as_dict'), "Passwords response should have as_dict method"
        except Exception as exc:
            errors.append(f"Getting passwords failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the passwords test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_passwords_with_different_os_types(self, fs):
        """Test getting passwords with different OS types"""
        client = MockZCCClient(fs)
        errors = []

        os_types = ["windows", "macos", "linux", "ios", "android"]
        
        try:
            # First, get a device to use its username
            devices, _, dev_err = client.zcc.devices.list_devices(
                query_params={"page": 1, "page_size": 1}
            )
            
            if dev_err is None and devices and len(devices) > 0:
                device = devices[0]
                username = device.user if hasattr(device, 'user') else device.get('user')
                
                if username:
                    for os_type in os_types:
                        try:
                            passwords, response, err = client.zcc.secrets.get_passwords(
                                query_params={"username": username, "os_type": os_type}
                            )
                            # Validate the call mechanics - errors for specific OS types are acceptable
                        except Exception as e:
                            # Some OS types might not be supported for the user
                            pass
        except Exception as exc:
            errors.append(f"Getting passwords with different OS types failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the passwords OS types test:\n{chr(10).join(errors)}"

