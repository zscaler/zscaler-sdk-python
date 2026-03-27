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

"""Unit tests for ZBI API client classes."""

from unittest.mock import MagicMock, Mock

import pytest

from zscaler.zbi.custom_apps import CustomAppsAPI
from zscaler.zbi.models.custom_apps import CustomApp
from zscaler.zbi.models.report_configs import ReportConfig
from zscaler.zbi.report_configs import ReportConfigsAPI
from zscaler.zbi.reports import ReportsAPI
from zscaler.zbi.zbi_service import ZBIService


def _mock_response(status_code=200, body=None, results=None):
    """Create a mock response object."""
    resp = Mock()
    resp.status = status_code
    resp.status_code = status_code
    resp.get_body.return_value = body or {}
    resp.get_results.return_value = results or []
    resp.headers = {"Content-Type": "application/json"}
    return resp


def _mock_executor(response=None, error=None):
    """Create a mock request executor."""
    executor = Mock()
    request_obj = Mock()
    executor.create_request.return_value = (request_obj, None)
    executor.execute.return_value = (response, error)
    return executor


class TestZBIService:
    """Tests for ZBIService."""

    def test_service_has_custom_apps(self):
        executor = Mock()
        svc = ZBIService(executor)
        assert isinstance(svc.custom_apps, CustomAppsAPI)

    def test_service_has_report_configs(self):
        executor = Mock()
        svc = ZBIService(executor)
        assert isinstance(svc.report_configs, ReportConfigsAPI)

    def test_service_has_reports(self):
        executor = Mock()
        svc = ZBIService(executor)
        assert isinstance(svc.reports, ReportsAPI)


class TestCustomAppsClient:
    """Tests for CustomAppsAPI client."""

    def test_list_custom_apps_success(self):
        app_data = [
            {
                "id": 101,
                "name": "Test App",
                "associatedAppName": "Test",
                "associatedAppCategory": "Cat",
                "description": "Desc",
                "signatures": [],
            }
        ]
        resp = _mock_response(results=app_data)
        executor = _mock_executor(response=resp)

        api = CustomAppsAPI(executor)
        apps, response, error = api.list_custom_apps()

        assert error is None
        assert len(apps) == 1
        assert isinstance(apps[0], CustomApp)
        assert apps[0].id == 101

    def test_list_custom_apps_error(self):
        mock_error = Exception("API Error")
        executor = _mock_executor(error=mock_error)

        api = CustomAppsAPI(executor)
        apps, response, error = api.list_custom_apps()

        assert apps is None
        assert error is mock_error

    def test_get_custom_app_success(self):
        app_data = [
            {
                "id": 101,
                "name": "Test App",
                "signatures": [],
            }
        ]
        resp = _mock_response(results=app_data)
        executor = _mock_executor(response=resp)

        api = CustomAppsAPI(executor)
        app, response, error = api.get_custom_app(101)

        assert error is None
        assert app is not None
        assert app.id == 101

    def test_create_custom_app_success(self):
        app_data = [
            {
                "id": 102,
                "name": "New App",
                "description": "Created",
                "signatures": [
                    {
                        "type": "HOST",
                        "matchLevel": "EXACT",
                        "value": "example.com",
                    }
                ],
            }
        ]
        resp = _mock_response(status_code=201, results=app_data)
        executor = _mock_executor(response=resp)

        api = CustomAppsAPI(executor)
        app, response, error = api.create_custom_app(
            name="New App",
            description="Created",
            signatures=[
                {
                    "type": "HOST",
                    "matchLevel": "EXACT",
                    "value": "example.com",
                }
            ],
        )

        assert error is None
        assert app is not None
        assert app.id == 102

    def test_update_custom_app_success(self):
        body = {
            "id": 101,
            "name": "Updated",
            "description": "Updated desc",
            "signatures": [],
        }
        resp = _mock_response(body=body)
        executor = _mock_executor(response=resp)

        api = CustomAppsAPI(executor)
        app, response, error = api.update_custom_app(101, name="Updated", description="Updated desc")

        assert error is None
        assert app is not None
        assert app.name == "Updated"

    def test_delete_custom_app_success(self):
        resp = _mock_response(status_code=200)
        executor = _mock_executor(response=resp)

        api = CustomAppsAPI(executor)
        status, response, error = api.delete_custom_app(101)

        assert error is None
        assert status == 200

    def test_create_request_error(self):
        executor = Mock()
        executor.create_request.return_value = (
            None,
            Exception("Request creation failed"),
        )

        api = CustomAppsAPI(executor)
        result, response, error = api.list_custom_apps()

        assert result is None
        assert response is None
        assert str(error) == "Request creation failed"


class TestReportConfigsClient:
    """Tests for ReportConfigsAPI client."""

    def test_list_report_configs_success(self):
        cfg_data = [
            {
                "id": 1,
                "name": "Daily report",
                "subType": "USERS",
                "enabled": True,
                "customIds": [100],
                "deliveryInformation": [
                    {
                        "deliveryMethod": "EMAIL",
                        "emails": ["a@b.com"],
                    }
                ],
                "scheduleParams": {
                    "timezone": "UTC",
                    "frequency": "DAILY",
                },
                "status": "SCHEDULED_SUCCESS",
            }
        ]
        resp = _mock_response(results=cfg_data)
        executor = _mock_executor(response=resp)

        api = ReportConfigsAPI(executor)
        configs, response, error = api.list_report_configs()

        assert error is None
        assert len(configs) == 1
        assert isinstance(configs[0], ReportConfig)
        assert configs[0].sub_type == "USERS"

    def test_create_report_config_success(self):
        cfg_data = [
            {
                "id": 1,
                "name": "New Config",
                "sub_type": "USERS",
                "enabled": True,
                "custom_ids": [100],
                "status": "ACCEPTED",
            }
        ]
        resp = _mock_response(status_code=201, results=cfg_data)
        executor = _mock_executor(response=resp)

        api = ReportConfigsAPI(executor)
        cfg, response, error = api.create_report_config(
            name="New Config",
            sub_type="USERS",
            enabled=True,
            custom_ids=[100],
        )

        assert error is None
        assert cfg is not None
        assert cfg.id == 1

    def test_update_report_config_success(self):
        body = {
            "id": 1,
            "name": "Updated Config",
            "sub_type": "USERS",
            "enabled": True,
            "custom_ids": [100],
            "status": "UPDATED",
        }
        resp = _mock_response(body=body)
        executor = _mock_executor(response=resp)

        api = ReportConfigsAPI(executor)
        cfg, response, error = api.update_report_config(1, name="Updated Config")

        assert error is None
        assert cfg is not None
        assert cfg.name == "Updated Config"

    def test_delete_report_config_success(self):
        resp = _mock_response(status_code=200)
        executor = _mock_executor(response=resp)

        api = ReportConfigsAPI(executor)
        status, response, error = api.delete_report_config(1)

        assert error is None
        assert status == 200


class TestReportsClient:
    """Tests for ReportsAPI client."""

    def test_list_reports_success(self):
        report_data = [
            {"fileName": "report1.csv", "reportType": "APPLICATION"},
            {"fileName": "report2.csv", "reportType": "DATA_EXPLORER"},
        ]
        resp = _mock_response(results=report_data)
        executor = _mock_executor(response=resp)

        api = ReportsAPI(executor)
        reports, response, error = api.list_reports(query_params={"reportType": "APPLICATION"})

        assert error is None
        assert len(reports) == 2

    def test_list_reports_error(self):
        mock_error = Exception("List failed")
        executor = _mock_executor(error=mock_error)

        api = ReportsAPI(executor)
        reports, response, error = api.list_reports()

        assert reports is None
        assert error is mock_error

    def test_download_report_validates_file_name(self):
        executor = Mock()
        api = ReportsAPI(executor)

        with pytest.raises(ValueError, match="file_name is required"):
            api.download_report(
                file_name="",
                report_type="APPLICATION",
            )

    def test_download_report_validates_report_type(self):
        executor = Mock()
        api = ReportsAPI(executor)

        with pytest.raises(ValueError, match="report_type must be one of"):
            api.download_report(
                file_name="test.csv",
                report_type="INVALID",
            )

    def test_download_report_validates_sub_type(self):
        executor = Mock()
        api = ReportsAPI(executor)

        with pytest.raises(ValueError, match="sub_type must be one of"):
            api.download_report(
                file_name="test.csv",
                report_type="APPLICATION",
                sub_type="INVALID",
            )
