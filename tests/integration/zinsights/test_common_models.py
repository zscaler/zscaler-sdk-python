"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import pytest
from zscaler.zinsights.models.common import (
    WebReportEntry, WebReportEntryWithId, TrendDataPoint,
    CyberSecurityIncident, CasbIncident, IoTDeviceStat,
    ShadowITApp, FirewallReportEntry, RiskScoreEvent
)


class TestCommonModels:
    """
    Tests for Z-Insights common response models
    """

    def test_web_report_entry(self):
        config = {"name": "Test Location", "total": 1000, "trend": []}
        entry = WebReportEntry(config)
        assert entry.name == "Test Location"
        assert entry.total == 1000
        assert entry.trend == []
        
        # Test request_format
        formatted = entry.request_format()
        assert "name" in formatted
        assert "total" in formatted

    def test_web_report_entry_empty(self):
        entry = WebReportEntry()
        assert entry.name is None
        assert entry.total is None

    def test_web_report_entry_with_id(self):
        config = {"id": 123, "name": "Test Entry", "total": 5000}
        entry = WebReportEntryWithId(config)
        assert entry.id == 123
        assert entry.name == "Test Entry"
        assert entry.total == 5000
        
        formatted = entry.request_format()
        assert "id" in formatted

    def test_trend_data_point(self):
        config = {"time_stamp": 1234567890, "value": 500}
        trend = TrendDataPoint(config)
        assert trend.time_stamp == 1234567890
        assert trend.value == 500
        
        formatted = trend.request_format()
        assert "time_stamp" in formatted

    def test_cyber_security_incident(self):
        config = {"app": "TestApp", "name": "Malware", "total": 10}
        incident = CyberSecurityIncident(config)
        assert incident.app == "TestApp"
        assert incident.name == "Malware"
        assert incident.total == 10
        
        formatted = incident.request_format()
        assert "app" in formatted

    def test_casb_incident(self):
        config = {"time_stamp": 1234567890, "policy": "DLP Policy", "incident_type": "DLP"}
        incident = CasbIncident(config)
        assert incident.time_stamp == 1234567890
        assert incident.policy == "DLP Policy"
        assert incident.incident_type == "DLP"
        
        formatted = incident.request_format()
        assert "policy" in formatted

    def test_iot_device_stat(self):
        config = {"category": "Camera", "type": "IP Camera", "device_count": 50}
        stat = IoTDeviceStat(config)
        assert stat.category == "Camera"
        assert stat.type == "IP Camera"
        assert stat.device_count == 50
        
        formatted = stat.request_format()
        assert "category" in formatted

    def test_shadow_it_app(self):
        config = {"name": "Dropbox", "total": 1000, "risk_score": 8, "category": "File Sharing"}
        app = ShadowITApp(config)
        assert app.name == "Dropbox"
        assert app.total == 1000
        assert app.risk_score == 8
        assert app.category == "File Sharing"
        
        formatted = app.request_format()
        assert "name" in formatted

    def test_firewall_report_entry(self):
        config = {"name": "ALLOW", "total": 10000}
        entry = FirewallReportEntry(config)
        assert entry.name == "ALLOW"
        assert entry.total == 10000
        
        formatted = entry.request_format()
        assert "name" in formatted

    def test_risk_score_event(self):
        config = {
            "time_stamp": 1234567890,
            "threats_blocked_count": 100,
            "suspicious_activity_count": 50,
            "active_infection_count": 5,
            "score": 75
        }
        event = RiskScoreEvent(config)
        assert event.time_stamp == 1234567890
        assert event.threats_blocked_count == 100
        assert event.suspicious_activity_count == 50
        assert event.active_infection_count == 5
        assert event.score == 75
        
        formatted = event.request_format()
        assert "score" in formatted

