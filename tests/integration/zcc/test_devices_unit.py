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
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def fs():
    yield


class TestDevicesUnit:
    """
    Unit Tests for the ZCC Devices API to increase coverage
    """

    @pytest.fixture
    def mock_request_executor(self):
        """Create a mock request executor"""
        executor = Mock()
        executor.create_request = Mock(return_value=(Mock(), None))
        executor.execute = Mock(return_value=(Mock(), None))
        return executor

    def test_download_devices_invalid_os_type(self, fs):
        """Test download devices with invalid OS type raises error"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        devices_api = DevicesAPI(mock_executor)
        
        # Test with invalid os_type - should raise ValueError
        with pytest.raises(ValueError):
            devices_api.download_devices(
                query_params={"os_types": ["invalid_os"]},
                filename="test.csv"
            )

    def test_download_devices_invalid_registration_type(self, fs):
        """Test download devices with invalid registration type raises error"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        devices_api = DevicesAPI(mock_executor)
        
        # Test with invalid registration_type - should raise ValueError
        with pytest.raises(ValueError):
            devices_api.download_devices(
                query_params={"registration_types": ["invalid_reg"]},
                filename="test.csv"
            )

    def test_download_service_status_invalid_os_type(self, fs):
        """Test download service status with invalid OS type raises error"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        devices_api = DevicesAPI(mock_executor)
        
        with pytest.raises(ValueError):
            devices_api.download_service_status(
                query_params={"os_types": ["invalid_os"]},
                filename="test.csv"
            )

    def test_download_service_status_invalid_registration_type(self, fs):
        """Test download service status with invalid registration type raises error"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        devices_api = DevicesAPI(mock_executor)
        
        with pytest.raises(ValueError):
            devices_api.download_service_status(
                query_params={"registration_types": ["invalid_reg"]},
                filename="test.csv"
            )

    def test_list_devices_with_error(self, fs):
        """Test list devices handles errors correctly"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_devices()
        
        assert result is None
        assert err is not None

    def test_get_device_cleanup_info_with_error(self, fs):
        """Test get device cleanup info handles errors correctly"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device_cleanup_info()
        
        assert result is None
        assert err is not None

    def test_get_device_details_with_error(self, fs):
        """Test get device details handles errors correctly"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device_details()
        
        assert result is None
        assert err is not None

    def test_update_device_cleanup_info_with_error(self, fs):
        """Test update device cleanup info handles errors correctly"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.update_device_cleanup_info(active=1)
        
        assert result is None
        assert err is not None

    def test_remove_devices_with_error(self, fs):
        """Test remove devices handles errors correctly"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.remove_devices(udids=["test"])
        
        assert result is None
        assert err is not None

    def test_force_remove_devices_with_error(self, fs):
        """Test force remove devices handles errors correctly"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.force_remove_devices(udids=["test"])
        
        assert result is None
        assert err is not None

    def test_remove_machine_tunnel_with_error(self, fs):
        """Test remove machine tunnel handles errors correctly"""
        from zscaler.zcc.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.remove_machine_tunnel(host_names=["test"])
        
        assert result is None
        assert err is not None


class TestWebPolicyUnit:
    """
    Unit Tests for the ZCC Web Policy API to increase coverage
    """

    def test_list_by_company_with_error(self, fs):
        """Test list by company handles errors correctly"""
        from zscaler.zcc.web_policy import WebPolicyAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        policy_api = WebPolicyAPI(mock_executor)
        result, response, err = policy_api.list_by_company()
        
        assert result is None
        assert err is not None

    def test_activate_web_policy_with_error(self, fs):
        """Test activate web policy handles errors correctly"""
        from zscaler.zcc.web_policy import WebPolicyAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        policy_api = WebPolicyAPI(mock_executor)
        result, response, err = policy_api.activate_web_policy(device_type=3, policy_id=1)
        
        assert result is None
        assert err is not None

    def test_web_policy_edit_with_error(self, fs):
        """Test web policy edit handles errors correctly"""
        from zscaler.zcc.web_policy import WebPolicyAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        policy_api = WebPolicyAPI(mock_executor)
        result, response, err = policy_api.web_policy_edit(name="test")
        
        assert result is None
        assert err is not None

    def test_delete_web_policy_with_error(self, fs):
        """Test delete web policy handles errors correctly"""
        from zscaler.zcc.web_policy import WebPolicyAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        policy_api = WebPolicyAPI(mock_executor)
        result, response, err = policy_api.delete_web_policy(policy_id=1)
        
        assert result is None
        assert err is not None


class TestAdminUserUnit:
    """
    Unit Tests for the ZCC Admin User API to increase coverage
    """

    def test_list_admin_users_with_error(self, fs):
        """Test list admin users handles errors correctly"""
        from zscaler.zcc.admin_user import AdminUserAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        admin_api = AdminUserAPI(mock_executor)
        result, response, err = admin_api.list_admin_users()
        
        assert result is None
        assert err is not None

    def test_get_admin_user_sync_info_with_error(self, fs):
        """Test get admin user sync info handles errors correctly"""
        from zscaler.zcc.admin_user import AdminUserAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        admin_api = AdminUserAPI(mock_executor)
        result, response, err = admin_api.get_admin_user_sync_info()
        
        assert result is None
        assert err is not None

    def test_list_admin_roles_with_error(self, fs):
        """Test list admin roles handles errors correctly"""
        from zscaler.zcc.admin_user import AdminUserAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        admin_api = AdminUserAPI(mock_executor)
        result, response, err = admin_api.list_admin_roles()
        
        assert result is None
        assert err is not None

    def test_sync_zia_zdx_admin_users_with_error(self, fs):
        """Test sync zia zdx admin users handles errors correctly"""
        from zscaler.zcc.admin_user import AdminUserAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        admin_api = AdminUserAPI(mock_executor)
        result, response, err = admin_api.sync_zia_zdx_admin_users()
        
        assert result is None
        assert err is not None

    def test_sync_zpa_admin_users_with_error(self, fs):
        """Test sync zpa admin users handles errors correctly"""
        from zscaler.zcc.admin_user import AdminUserAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        admin_api = AdminUserAPI(mock_executor)
        result, response, err = admin_api.sync_zpa_admin_users()
        
        assert result is None
        assert err is not None


class TestEntitlementsUnit:
    """
    Unit Tests for the ZCC Entitlements API to increase coverage
    """

    def test_get_zdx_group_entitlements_with_error(self, fs):
        """Test get zdx group entitlements handles errors correctly"""
        from zscaler.zcc.entitlements import EntitlementAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.get_zdx_group_entitlements()
        
        assert result is None
        assert err is not None

    def test_get_zpa_group_entitlements_with_error(self, fs):
        """Test get zpa group entitlements handles errors correctly"""
        from zscaler.zcc.entitlements import EntitlementAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.get_zpa_group_entitlements()
        
        assert result is None
        assert err is not None

    def test_update_zdx_group_entitlement_with_error(self, fs):
        """Test update zdx group entitlement handles errors correctly"""
        from zscaler.zcc.entitlements import EntitlementAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.update_zdx_group_entitlement()
        
        assert result is None
        assert err is not None

    def test_update_zpa_group_entitlement_with_error(self, fs):
        """Test update zpa group entitlement handles errors correctly"""
        from zscaler.zcc.entitlements import EntitlementAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Test error")))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.update_zpa_group_entitlement()
        
        assert result is None
        assert err is not None

