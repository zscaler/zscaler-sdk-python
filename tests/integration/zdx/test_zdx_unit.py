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


class TestAdminUnit:
    """Unit Tests for the ZDX Admin API to increase coverage"""

    def test_list_departments_request_error(self, fs):
        """Test list_departments handles request creation errors correctly"""
        from zscaler.zdx.admin import AdminAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        admin_api = AdminAPI(mock_executor)
        result, response, err = admin_api.list_departments()
        
        assert result is None
        assert err is not None

    def test_list_departments_execute_error(self, fs):
        """Test list_departments handles execution errors correctly"""
        from zscaler.zdx.admin import AdminAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        admin_api = AdminAPI(mock_executor)
        result, response, err = admin_api.list_departments()
        
        assert result is None
        assert err is not None

    def test_list_departments_parsing_error(self, fs):
        """Test list_departments handles parsing errors correctly"""
        from zscaler.zdx.admin import AdminAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        admin_api = AdminAPI(mock_executor)
        result, response, err = admin_api.list_departments()
        
        assert result is None
        assert err is not None

    def test_list_locations_request_error(self, fs):
        """Test list_locations handles request creation errors correctly"""
        from zscaler.zdx.admin import AdminAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        admin_api = AdminAPI(mock_executor)
        result, response, err = admin_api.list_locations()
        
        assert result is None
        assert err is not None

    def test_list_locations_execute_error(self, fs):
        """Test list_locations handles execution errors correctly"""
        from zscaler.zdx.admin import AdminAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        admin_api = AdminAPI(mock_executor)
        result, response, err = admin_api.list_locations()
        
        assert result is None
        assert err is not None

    def test_list_locations_parsing_error(self, fs):
        """Test list_locations handles parsing errors correctly"""
        from zscaler.zdx.admin import AdminAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        admin_api = AdminAPI(mock_executor)
        result, response, err = admin_api.list_locations()
        
        assert result is None
        assert err is not None


class TestAlertsUnit:
    """Unit Tests for the ZDX Alerts API to increase coverage"""

    def test_list_ongoing_request_error(self, fs):
        """Test list_ongoing handles request creation errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_ongoing()
        
        assert result is None
        assert err is not None

    def test_list_ongoing_execute_error(self, fs):
        """Test list_ongoing handles execution errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_ongoing()
        
        assert result is None
        assert err is not None

    def test_list_ongoing_parsing_error(self, fs):
        """Test list_ongoing handles parsing errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_ongoing()
        
        assert result is None
        assert err is not None

    def test_get_alert_request_error(self, fs):
        """Test get_alert handles request creation errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.get_alert(alert_id="123")
        
        assert result is None
        assert err is not None

    def test_get_alert_execute_error(self, fs):
        """Test get_alert handles execution errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.get_alert(alert_id="123")
        
        assert result is None
        assert err is not None

    def test_get_alert_parsing_error(self, fs):
        """Test get_alert handles parsing errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.get_alert(alert_id="123")
        
        assert result is None
        assert err is not None

    def test_list_historical_request_error(self, fs):
        """Test list_historical handles request creation errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_historical()
        
        assert result is None
        assert err is not None

    def test_list_historical_execute_error(self, fs):
        """Test list_historical handles execution errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_historical()
        
        assert result is None
        assert err is not None

    def test_list_affected_devices_request_error(self, fs):
        """Test list_affected_devices handles request creation errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_affected_devices(alert_id="123")
        
        assert result is None
        assert err is not None

    def test_list_affected_devices_execute_error(self, fs):
        """Test list_affected_devices handles execution errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_affected_devices(alert_id="123")
        
        assert result is None
        assert err is not None


class TestAppsUnit:
    """Unit Tests for the ZDX Apps API to increase coverage"""

    def test_list_apps_request_error(self, fs):
        """Test list_apps handles request creation errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.list_apps()
        
        assert result is None
        assert err is not None

    def test_list_apps_execute_error(self, fs):
        """Test list_apps handles execution errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.list_apps()
        
        assert result is None
        assert err is not None

    def test_list_apps_parsing_error(self, fs):
        """Test list_apps handles parsing errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.list_apps()
        
        assert result is None
        assert err is not None

    def test_get_app_request_error(self, fs):
        """Test get_app handles request creation errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_execute_error(self, fs):
        """Test get_app handles execution errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_score_request_error(self, fs):
        """Test get_app_score handles request creation errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_score(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_metrics_request_error(self, fs):
        """Test get_app_metrics handles request creation errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_metrics(app_id="123")
        
        assert result is None
        assert err is not None

    def test_list_app_users_request_error(self, fs):
        """Test list_app_users handles request creation errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.list_app_users(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_user_request_error(self, fs):
        """Test get_app_user handles request creation errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_user(app_id="123", user_id="456")
        
        assert result is None
        assert err is not None


class TestDevicesUnit:
    """Unit Tests for the ZDX Devices API to increase coverage"""

    def test_list_devices_request_error(self, fs):
        """Test list_devices handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_devices()
        
        assert result is None
        assert err is not None

    def test_list_devices_execute_error(self, fs):
        """Test list_devices handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_devices()
        
        assert result is None
        assert err is not None

    def test_list_devices_parsing_error(self, fs):
        """Test list_devices handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_devices()
        
        assert result is None
        assert err is not None

    def test_get_device_request_error(self, fs):
        """Test get_device handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_device_apps_request_error(self, fs):
        """Test get_device_apps handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device_apps(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_device_app_request_error(self, fs):
        """Test get_device_app handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device_app(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_web_probes_request_error(self, fs):
        """Test get_web_probes handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_web_probes(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_web_probe_request_error(self, fs):
        """Test get_web_probe handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_web_probe(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_list_cloudpath_probes_request_error(self, fs):
        """Test list_cloudpath_probes handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_cloudpath_probes(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_cloudpath_probe_request_error(self, fs):
        """Test get_cloudpath_probe handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_cloudpath_probe(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_get_cloudpath_request_error(self, fs):
        """Test get_cloudpath handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_cloudpath(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_get_call_quality_metrics_request_error(self, fs):
        """Test get_call_quality_metrics handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_call_quality_metrics(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_health_metrics_request_error(self, fs):
        """Test get_health_metrics handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_health_metrics(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_events_request_error(self, fs):
        """Test get_events handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_events(device_id="123")
        
        assert result is None
        assert err is not None

    def test_list_geolocations_request_error(self, fs):
        """Test list_geolocations handles request creation errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_geolocations()
        
        assert result is None
        assert err is not None


class TestInventoryUnit:
    """Unit Tests for the ZDX Inventory API to increase coverage"""

    def test_list_softwares_request_error(self, fs):
        """Test list_softwares handles request creation errors correctly"""
        from zscaler.zdx.inventory import InventoryAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        inventory_api = InventoryAPI(mock_executor)
        result, response, err = inventory_api.list_softwares()
        
        assert result is None
        assert err is not None

    def test_list_softwares_execute_error(self, fs):
        """Test list_softwares handles execution errors correctly"""
        from zscaler.zdx.inventory import InventoryAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        inventory_api = InventoryAPI(mock_executor)
        result, response, err = inventory_api.list_softwares()
        
        assert result is None
        assert err is not None

    def test_list_softwares_parsing_error(self, fs):
        """Test list_softwares handles parsing errors correctly"""
        from zscaler.zdx.inventory import InventoryAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        inventory_api = InventoryAPI(mock_executor)
        result, response, err = inventory_api.list_softwares()
        
        assert result is None
        assert err is not None

    def test_list_software_keys_request_error(self, fs):
        """Test list_software_keys handles request creation errors correctly"""
        from zscaler.zdx.inventory import InventoryAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        inventory_api = InventoryAPI(mock_executor)
        result, response, err = inventory_api.list_software_keys(software_key="test")
        
        assert result is None
        assert err is not None

    def test_list_software_keys_execute_error(self, fs):
        """Test list_software_keys handles execution errors correctly"""
        from zscaler.zdx.inventory import InventoryAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        inventory_api = InventoryAPI(mock_executor)
        result, response, err = inventory_api.list_software_keys(software_key="test")
        
        assert result is None
        assert err is not None


class TestTroubleshootingUnit:
    """Unit Tests for the ZDX Troubleshooting API to increase coverage"""

    def test_list_deeptraces_request_error(self, fs):
        """Test list_deeptraces handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.list_deeptraces(device_id="123")
        
        assert result is None
        assert err is not None

    def test_list_deeptraces_execute_error(self, fs):
        """Test list_deeptraces handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.list_deeptraces(device_id="123")
        
        assert result is None
        assert err is not None

    def test_list_deeptraces_parsing_error(self, fs):
        """Test list_deeptraces handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.list_deeptraces(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_request_error(self, fs):
        """Test get_deeptrace handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_execute_error(self, fs):
        """Test get_deeptrace handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_start_deeptrace_request_error(self, fs):
        """Test start_deeptrace handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.start_deeptrace(device_id="123")
        
        assert result is None
        assert err is not None

    def test_start_deeptrace_execute_error(self, fs):
        """Test start_deeptrace handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.start_deeptrace(device_id="123")
        
        assert result is None
        assert err is not None

    def test_delete_deeptrace_request_error(self, fs):
        """Test delete_deeptrace handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.delete_deeptrace(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_delete_deeptrace_execute_error(self, fs):
        """Test delete_deeptrace handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.delete_deeptrace(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_list_top_processes_request_error(self, fs):
        """Test list_top_processes handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.list_top_processes(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_webprobe_metrics_request_error(self, fs):
        """Test get_deeptrace_webprobe_metrics handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_webprobe_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_cloudpath_metrics_request_error(self, fs):
        """Test get_deeptrace_cloudpath_metrics handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_cloudpath_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_cloudpath_request_error(self, fs):
        """Test get_deeptrace_cloudpath handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_cloudpath(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_health_metrics_request_error(self, fs):
        """Test get_deeptrace_health_metrics handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_health_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_events_request_error(self, fs):
        """Test get_deeptrace_events handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_events(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_start_analysis_request_error(self, fs):
        """Test start_analysis handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.start_analysis(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_analysis_request_error(self, fs):
        """Test get_analysis handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_analysis(analysis_id="123")
        
        assert result is None
        assert err is not None

    def test_delete_analysis_request_error(self, fs):
        """Test delete_analysis handles request creation errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.delete_analysis(analysis_id="123")
        
        assert result is None
        assert err is not None


class TestUsersUnit:
    """Unit Tests for the ZDX Users API to increase coverage"""

    def test_list_users_request_error(self, fs):
        """Test list_users handles request creation errors correctly"""
        from zscaler.zdx.users import UsersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_users()
        
        assert result is None
        assert err is not None

    def test_list_users_execute_error(self, fs):
        """Test list_users handles execution errors correctly"""
        from zscaler.zdx.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_users()
        
        assert result is None
        assert err is not None

    def test_list_users_parsing_error(self, fs):
        """Test list_users handles parsing errors correctly"""
        from zscaler.zdx.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_users()
        
        assert result is None
        assert err is not None

    def test_get_user_request_error(self, fs):
        """Test get_user handles request creation errors correctly"""
        from zscaler.zdx.users import UsersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.get_user(user_id="123")
        
        assert result is None
        assert err is not None

    def test_get_user_execute_error(self, fs):
        """Test get_user handles execution errors correctly"""
        from zscaler.zdx.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.get_user(user_id="123")
        
        assert result is None
        assert err is not None


class TestSnapshotUnit:
    """Unit Tests for the ZDX Snapshot API to increase coverage"""

    def test_share_snapshot_request_error(self, fs):
        """Test share_snapshot handles request creation errors correctly"""
        from zscaler.zdx.snapshot import SnapshotAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        snapshot_api = SnapshotAPI(mock_executor)
        result, response, err = snapshot_api.share_snapshot(name="test", alert_id="123")
        
        assert result is None
        assert err is not None

    def test_share_snapshot_execute_error(self, fs):
        """Test share_snapshot handles execution errors correctly"""
        from zscaler.zdx.snapshot import SnapshotAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        snapshot_api = SnapshotAPI(mock_executor)
        result, response, err = snapshot_api.share_snapshot(name="test", alert_id="123")
        
        assert result is None
        assert err is not None

    def test_share_snapshot_parsing_error(self, fs):
        """Test share_snapshot handles parsing errors correctly"""
        from zscaler.zdx.snapshot import SnapshotAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        snapshot_api = SnapshotAPI(mock_executor)
        result, response, err = snapshot_api.share_snapshot(name="test", alert_id="123")
        
        assert result is None
        assert err is not None


class TestDevicesExtendedUnit:
    """Extended Unit Tests for the ZDX Devices API to increase coverage"""

    def test_get_device_execute_error(self, fs):
        """Test get_device handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_device_parsing_error(self, fs):
        """Test get_device handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_device_apps_execute_error(self, fs):
        """Test get_device_apps handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device_apps(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_device_app_execute_error(self, fs):
        """Test get_device_app handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device_app(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_web_probes_execute_error(self, fs):
        """Test get_web_probes handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_web_probes(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_web_probes_parsing_error(self, fs):
        """Test get_web_probes handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_web_probes(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_web_probe_execute_error(self, fs):
        """Test get_web_probe handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_web_probe(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_list_cloudpath_probes_execute_error(self, fs):
        """Test list_cloudpath_probes handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_cloudpath_probes(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_cloudpath_probe_execute_error(self, fs):
        """Test get_cloudpath_probe handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_cloudpath_probe(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_get_cloudpath_execute_error(self, fs):
        """Test get_cloudpath handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_cloudpath(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_get_call_quality_metrics_execute_error(self, fs):
        """Test get_call_quality_metrics handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_call_quality_metrics(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_health_metrics_execute_error(self, fs):
        """Test get_health_metrics handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_health_metrics(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_events_execute_error(self, fs):
        """Test get_events handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_events(device_id="123")
        
        assert result is None
        assert err is not None

    def test_list_geolocations_execute_error(self, fs):
        """Test list_geolocations handles execution errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_geolocations()
        
        assert result is None
        assert err is not None


class TestAppsExtendedUnit:
    """Extended Unit Tests for the ZDX Apps API to increase coverage"""

    def test_get_app_parsing_error(self, fs):
        """Test get_app handles parsing errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_score_execute_error(self, fs):
        """Test get_app_score handles execution errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_score(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_score_parsing_error(self, fs):
        """Test get_app_score handles parsing errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_score(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_metrics_execute_error(self, fs):
        """Test get_app_metrics handles execution errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_metrics(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_metrics_parsing_error(self, fs):
        """Test get_app_metrics handles parsing errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_metrics(app_id="123")
        
        assert result is None
        assert err is not None

    def test_list_app_users_execute_error(self, fs):
        """Test list_app_users handles execution errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.list_app_users(app_id="123")
        
        assert result is None
        assert err is not None

    def test_list_app_users_parsing_error(self, fs):
        """Test list_app_users handles parsing errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.list_app_users(app_id="123")
        
        assert result is None
        assert err is not None

    def test_get_app_user_execute_error(self, fs):
        """Test get_app_user handles execution errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_user(app_id="123", user_id="456")
        
        assert result is None
        assert err is not None

    def test_get_app_user_parsing_error(self, fs):
        """Test get_app_user handles parsing errors correctly"""
        from zscaler.zdx.apps import AppsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        apps_api = AppsAPI(mock_executor)
        result, response, err = apps_api.get_app_user(app_id="123", user_id="456")
        
        assert result is None
        assert err is not None


class TestTroubleshootingExtendedUnit:
    """Extended Unit Tests for the ZDX Troubleshooting API to increase coverage"""

    def test_get_deeptrace_parsing_error(self, fs):
        """Test get_deeptrace handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_start_deeptrace_parsing_error(self, fs):
        """Test start_deeptrace handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.start_deeptrace(device_id="123")
        
        assert result is None
        assert err is not None

    def test_list_top_processes_execute_error(self, fs):
        """Test list_top_processes handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.list_top_processes(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_list_top_processes_parsing_error(self, fs):
        """Test list_top_processes handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.list_top_processes(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_webprobe_metrics_execute_error(self, fs):
        """Test get_deeptrace_webprobe_metrics handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_webprobe_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_cloudpath_metrics_execute_error(self, fs):
        """Test get_deeptrace_cloudpath_metrics handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_cloudpath_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_cloudpath_execute_error(self, fs):
        """Test get_deeptrace_cloudpath handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_cloudpath(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_health_metrics_execute_error(self, fs):
        """Test get_deeptrace_health_metrics handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_health_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_events_execute_error(self, fs):
        """Test get_deeptrace_events handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_events(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_start_analysis_execute_error(self, fs):
        """Test start_analysis handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.start_analysis(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_start_analysis_parsing_error(self, fs):
        """Test start_analysis handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.start_analysis(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_analysis_execute_error(self, fs):
        """Test get_analysis handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_analysis(analysis_id="123")
        
        assert result is None
        assert err is not None

    def test_get_analysis_parsing_error(self, fs):
        """Test get_analysis handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_analysis(analysis_id="123")
        
        assert result is None
        assert err is not None

    def test_delete_analysis_execute_error(self, fs):
        """Test delete_analysis handles execution errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.delete_analysis(analysis_id="123")
        
        assert result is None
        assert err is not None


class TestDevicesParsingErrors:
    """Tests for Devices API parsing errors to increase coverage"""

    def test_get_device_apps_parsing_error(self, fs):
        """Test get_device_apps handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device_apps(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_device_app_parsing_error(self, fs):
        """Test get_device_app handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_device_app(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_web_probe_parsing_error(self, fs):
        """Test get_web_probe handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_web_probe(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_list_cloudpath_probes_parsing_error(self, fs):
        """Test list_cloudpath_probes handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_cloudpath_probes(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_cloudpath_probe_parsing_error(self, fs):
        """Test get_cloudpath_probe handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_cloudpath_probe(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_get_cloudpath_parsing_error(self, fs):
        """Test get_cloudpath handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_cloudpath(device_id="123", app_id="456", probe_id="789")
        
        assert result is None
        assert err is not None

    def test_get_call_quality_metrics_parsing_error(self, fs):
        """Test get_call_quality_metrics handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_call_quality_metrics(device_id="123", app_id="456")
        
        assert result is None
        assert err is not None

    def test_get_health_metrics_parsing_error(self, fs):
        """Test get_health_metrics handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_health_metrics(device_id="123")
        
        assert result is None
        assert err is not None

    def test_get_events_parsing_error(self, fs):
        """Test get_events handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.get_events(device_id="123")
        
        assert result is None
        assert err is not None

    def test_list_geolocations_parsing_error(self, fs):
        """Test list_geolocations handles parsing errors correctly"""
        from zscaler.zdx.devices import DevicesAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        devices_api = DevicesAPI(mock_executor)
        result, response, err = devices_api.list_geolocations()
        
        assert result is None
        assert err is not None


class TestTroubleshootingParsingErrors:
    """Tests for Troubleshooting API parsing errors to increase coverage"""

    def test_get_deeptrace_webprobe_metrics_parsing_error(self, fs):
        """Test get_deeptrace_webprobe_metrics handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_webprobe_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_cloudpath_metrics_parsing_error(self, fs):
        """Test get_deeptrace_cloudpath_metrics handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_cloudpath_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_cloudpath_parsing_error(self, fs):
        """Test get_deeptrace_cloudpath handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_cloudpath(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_health_metrics_parsing_error(self, fs):
        """Test get_deeptrace_health_metrics handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_health_metrics(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None

    def test_get_deeptrace_events_parsing_error(self, fs):
        """Test get_deeptrace_events handles parsing errors correctly"""
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        troubleshooting_api = TroubleshootingAPI(mock_executor)
        result, response, err = troubleshooting_api.get_deeptrace_events(device_id="123", trace_id="456")
        
        assert result is None
        assert err is not None


class TestAlertsExtendedUnit:
    """Extended Unit Tests for the ZDX Alerts API to increase coverage"""

    def test_list_historical_parsing_error(self, fs):
        """Test list_historical handles parsing errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_historical()
        
        assert result is None
        assert err is not None

    def test_list_affected_devices_parsing_error(self, fs):
        """Test list_affected_devices handles parsing errors correctly"""
        from zscaler.zdx.alerts import AlertsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        alerts_api = AlertsAPI(mock_executor)
        result, response, err = alerts_api.list_affected_devices(alert_id="123")
        
        assert result is None
        assert err is not None


class TestZDXServiceUnit:
    """Unit Tests for the ZDX Service to increase coverage"""

    def test_zdx_service_properties(self, fs):
        """Test ZDXService property accessors"""
        from zscaler.zdx.zdx_service import ZDXService
        from zscaler.zdx.admin import AdminAPI
        from zscaler.zdx.alerts import AlertsAPI
        from zscaler.zdx.apps import AppsAPI
        from zscaler.zdx.devices import DevicesAPI
        from zscaler.zdx.inventory import InventoryAPI
        from zscaler.zdx.troubleshooting import TroubleshootingAPI
        from zscaler.zdx.users import UsersAPI
        from zscaler.zdx.snapshot import SnapshotAPI
        
        mock_client = Mock()
        mock_client._request_executor = Mock()
        
        service = ZDXService(mock_client)
        
        # Test all API properties return correct types
        assert isinstance(service.admin, AdminAPI)
        assert isinstance(service.alerts, AlertsAPI)
        assert isinstance(service.apps, AppsAPI)
        assert isinstance(service.devices, DevicesAPI)
        assert isinstance(service.inventory, InventoryAPI)
        assert isinstance(service.troubleshooting, TroubleshootingAPI)
        assert isinstance(service.users, UsersAPI)
        assert isinstance(service.snapshot, SnapshotAPI)

