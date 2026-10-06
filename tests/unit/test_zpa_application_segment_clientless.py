"""
Testing ZPA application segment update with Browser Access (clientless) apps
"""

from unittest.mock import Mock, patch

from zscaler.zpa.application_segment import ApplicationSegmentAPI
from zscaler.zpa.models.application_segment import AppSegmentByType

SEGMENT_ID = "72058304855090128"


def _update(clientless_app_ids, by_type):
    executor = Mock()
    executor.create_request.return_value = ({}, None)
    response = Mock()
    response.get_body.return_value = {}
    executor.execute.return_value = (response, None)

    api = ApplicationSegmentAPI(executor, {"client": {"customerId": "1234567890"}})
    with patch("zscaler.zpa.application_segment.ApplicationSegmentByTypeAPI") as by_type_api:
        by_type_api.return_value.get_segments_by_type.return_value = (
            [AppSegmentByType(item) for item in by_type],
            None,
            None,
        )
        result = api.update_segment(SEGMENT_ID, name="segment-a", clientless_app_ids=clientless_app_ids)
    return result, executor


def test_update_segment_matches_clientless_apps_by_domain():
    by_type = [
        {"id": "72058304855099001", "appId": SEGMENT_ID, "domain": "app1.example.com"},
        {"id": "72058304855099002", "appId": SEGMENT_ID, "domain": "app2.example.com"},
        {"id": "72058304855099003", "appId": "72058304855090999", "domain": "app1.example.com"},
    ]
    apps = [
        {"name": "app2.example.com", "domain": "app2.example.com"},
        {"name": "app1.example.com", "domain": "app1.example.com"},
    ]

    (segment, _, err), executor = _update(apps, by_type)

    assert err is None
    body = executor.create_request.call_args.args[2]
    assert [(app["id"], app["appId"]) for app in body["clientlessApps"]] == [
        ("72058304855099002", SEGMENT_ID),
        ("72058304855099001", SEGMENT_ID),
    ]


def test_update_segment_reports_unmatched_clientless_domain():
    by_type = [{"id": "72058304855099001", "appId": SEGMENT_ID, "domain": "app1.example.com"}]

    (segment, _, err), executor = _update([{"domain": "missing.example.com"}], by_type)

    assert segment is None
    assert err == "Error: No matching clientless App found for domain 'missing.example.com' in existing segments."
    executor.create_request.assert_not_called()
