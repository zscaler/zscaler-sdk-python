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

"""Unit tests for ZBI model classes."""

import pytest

from zscaler.zbi.models.custom_apps import CustomApp, Signature
from zscaler.zbi.models.report_configs import (
    BackfillParams,
    DeliveryInformation,
    ReportConfig,
    ScheduleParams,
)


class TestSignatureModel:
    """Tests for the Signature model."""

    def test_init_with_config(self):
        sig = Signature({"type": "HOST", "matchLevel": "EXACT", "value": "example.com"})
        assert sig.type == "HOST"
        assert sig.match_level == "EXACT"
        assert sig.value == "example.com"

    def test_init_empty(self):
        sig = Signature()
        assert sig.type is None
        assert sig.match_level is None
        assert sig.value is None

    def test_request_format(self):
        sig = Signature(
            {
                "type": "URL",
                "matchLevel": "CONTAINS",
                "value": "example.com/path",
            }
        )
        rf = sig.request_format()
        assert rf["type"] == "URL"
        assert rf["matchLevel"] == "CONTAINS"
        assert rf["value"] == "example.com/path"


class TestCustomAppModel:
    """Tests for the CustomApp model."""

    def test_init_with_full_config(self):
        app = CustomApp(
            {
                "id": 101,
                "name": "Salesforce CRM",
                "associatedAppName": "Salesforce",
                "associatedAppCategory": "CRM",
                "description": "Tracks Salesforce traffic",
                "signatures": [
                    {
                        "type": "HOST",
                        "matchLevel": "EXACT",
                        "value": "login.salesforce.com",
                    },
                    {
                        "type": "URL",
                        "matchLevel": "CONTAINS",
                        "value": "salesforce.com/dashboard",
                    },
                ],
            }
        )
        assert app.id == 101
        assert app.name == "Salesforce CRM"
        assert app.associated_app_name == "Salesforce"
        assert app.associated_app_category == "CRM"
        assert app.description == "Tracks Salesforce traffic"
        assert len(app.signatures) == 2
        assert isinstance(app.signatures[0], Signature)
        assert app.signatures[0].type == "HOST"
        assert app.signatures[1].match_level == "CONTAINS"

    def test_init_empty(self):
        app = CustomApp()
        assert app.id is None
        assert app.name is None
        assert app.associated_app_name is None
        assert app.associated_app_category is None
        assert app.description is None
        assert app.signatures == []

    def test_init_with_null_optional_fields(self):
        app = CustomApp(
            {
                "id": 102,
                "name": "Test",
                "associatedAppName": None,
                "associatedAppCategory": None,
                "description": "Desc",
                "signatures": [],
            }
        )
        assert app.associated_app_name is None
        assert app.associated_app_category is None
        assert app.signatures == []

    def test_request_format(self):
        app = CustomApp(
            {
                "id": 101,
                "name": "Test",
                "associatedAppName": "App",
                "associatedAppCategory": "Cat",
                "description": "Desc",
                "signatures": [
                    {
                        "type": "HOST",
                        "matchLevel": "EXACT",
                        "value": "x.com",
                    }
                ],
            }
        )
        rf = app.request_format()
        assert rf["id"] == 101
        assert rf["name"] == "Test"
        assert rf["associatedAppName"] == "App"
        assert rf["associatedAppCategory"] == "Cat"
        assert rf["description"] == "Desc"
        assert len(rf["signatures"]) == 1
        assert rf["signatures"][0]["type"] == "HOST"


class TestDeliveryInformationModel:
    """Tests for the DeliveryInformation model."""

    def test_init_with_config(self):
        di = DeliveryInformation(
            {
                "delivery_method": "EMAIL",
                "emails": ["a@b.com", "c@d.com"],
            }
        )
        assert di.delivery_method == "EMAIL"
        assert len(di.emails) == 2

    def test_init_empty(self):
        di = DeliveryInformation()
        assert di.delivery_method is None
        assert di.emails == []

    def test_request_format(self):
        di = DeliveryInformation(
            {
                "delivery_method": "EMAIL",
                "emails": ["x@y.com"],
            }
        )
        rf = di.request_format()
        assert rf["delivery_method"] == "EMAIL"
        assert rf["emails"] == ["x@y.com"]


class TestScheduleParamsModel:
    """Tests for the ScheduleParams model."""

    def test_init_with_config(self):
        sp = ScheduleParams(
            {
                "timezone": "UTC",
                "frequency": "WEEKLY",
                "weekday": "MON",
            }
        )
        assert sp.timezone == "UTC"
        assert sp.frequency == "WEEKLY"
        assert sp.weekday == "MON"

    def test_init_daily_no_weekday(self):
        sp = ScheduleParams({"timezone": "UTC", "frequency": "DAILY"})
        assert sp.frequency == "DAILY"
        assert sp.weekday is None

    def test_init_empty(self):
        sp = ScheduleParams()
        assert sp.timezone is None
        assert sp.frequency is None
        assert sp.weekday is None


class TestBackfillParamsModel:
    """Tests for the BackfillParams model."""

    def test_init_with_config(self):
        bp = BackfillParams(
            {
                "timezone": "UTC",
                "stime": 1746057600,
                "etime": 1751327999,
            }
        )
        assert bp.timezone == "UTC"
        assert bp.stime == 1746057600
        assert bp.etime == 1751327999

    def test_init_empty(self):
        bp = BackfillParams()
        assert bp.timezone is None
        assert bp.stime is None
        assert bp.etime is None


class TestReportConfigModel:
    """Tests for the ReportConfig model."""

    def test_init_scheduled_report(self):
        cfg = ReportConfig(
            {
                "id": 1,
                "name": "Daily USERS report",
                "sub_type": "USERS",
                "enabled": True,
                "custom_ids": [1234],
                "delivery_information": [
                    {
                        "delivery_method": "EMAIL",
                        "emails": ["a@b.com"],
                    }
                ],
                "schedule_params": {
                    "timezone": "UTC",
                    "frequency": "DAILY",
                },
                "status": "SCHEDULED_SUCCESS",
                "nextRuntime": 1772640000,
                "custom_apps": [
                    {
                        "id": 1234,
                        "name": "App",
                        "signatures": [],
                    }
                ],
            }
        )
        assert cfg.id == 1
        assert cfg.name == "Daily USERS report"
        assert cfg.sub_type == "USERS"
        assert cfg.enabled is True
        assert cfg.custom_ids == [1234]
        assert len(cfg.delivery_information) == 1
        assert isinstance(cfg.delivery_information[0], DeliveryInformation)
        assert isinstance(cfg.schedule_params, ScheduleParams)
        assert cfg.schedule_params.frequency == "DAILY"
        assert cfg.backfill_params is None
        assert cfg.status == "SCHEDULED_SUCCESS"
        assert cfg.next_runtime == 1772640000
        assert len(cfg.custom_apps) == 1
        assert isinstance(cfg.custom_apps[0], CustomApp)

    def test_init_backfill_report(self):
        cfg = ReportConfig(
            {
                "id": 2,
                "name": "Backfill report",
                "sub_type": "OVERVIEW",
                "enabled": True,
                "custom_ids": [1234],
                "delivery_information": [
                    {
                        "delivery_method": "EMAIL",
                        "emails": ["a@b.com"],
                    }
                ],
                "backfill_params": {
                    "timezone": "UTC",
                    "stime": 1746057600,
                    "etime": 1751327999,
                },
                "status": "ACCEPTED",
            }
        )
        assert cfg.schedule_params is None
        assert isinstance(cfg.backfill_params, BackfillParams)
        assert cfg.backfill_params.stime == 1746057600

    def test_init_empty(self):
        cfg = ReportConfig()
        assert cfg.id is None
        assert cfg.name is None
        assert cfg.sub_type is None
        assert cfg.enabled is None
        assert cfg.custom_ids == []
        assert cfg.delivery_information == []
        assert cfg.schedule_params is None
        assert cfg.backfill_params is None
        assert cfg.custom_apps == []

    def test_request_format(self):
        cfg = ReportConfig(
            {
                "id": 1,
                "name": "Test",
                "sub_type": "USERS",
                "enabled": True,
                "custom_ids": [100],
                "delivery_information": [
                    {
                        "delivery_method": "EMAIL",
                        "emails": ["x@y.com"],
                    }
                ],
                "schedule_params": {
                    "timezone": "UTC",
                    "frequency": "DAILY",
                },
            }
        )
        rf = cfg.request_format()
        assert rf["id"] == 1
        assert rf["name"] == "Test"
        assert rf["sub_type"] == "USERS"
        assert rf["enabled"] is True
        assert rf["custom_ids"] == [100]
        assert len(rf["delivery_information"]) == 1
        assert rf["schedule_params"]["timezone"] == "UTC"
        assert rf["backfill_params"] is None
