"""
Testing ZIA Shadow IT report export requests
"""

from unittest.mock import Mock

import pytest

from zscaler.zia.shadow_it_report import ShadowITAPI

CSV = "Application,Risk\nGithub,3\n"


def _api(execute_error=None):
    executor = Mock()
    executor.create_request.return_value = ({}, None)
    response = Mock()
    response.get_body.return_value = CSV
    executor.execute.return_value = (None if execute_error else response, execute_error)
    return ShadowITAPI(executor), executor, response


def test_export_shadow_it_report_sends_payload():
    api, executor, response = _api()

    report, resp, err = api.export_shadow_it_report(duration="LAST_7_DAYS", app_name="Github")

    method, url, body, headers = executor.create_request.call_args.args
    assert method == "POST"
    assert url.endswith("/shadowIT/applications/export")
    assert body == {"duration": "LAST_7_DAYS", "app_name": "Github"}
    assert headers == {"Accept": "text/csv"}
    assert (report, resp, err) == (CSV, response, None)


def test_export_shadow_it_csv_sends_payload():
    api, executor, response = _api()

    report, resp, err = api.export_shadow_it_csv(
        application="Github", entity="USER", duration="LAST_15_DAYS", users=["1001", "1002"]
    )

    method, url, body, headers = executor.create_request.call_args.args
    assert method == "POST"
    assert url.endswith("/shadowIT/applications/USER/exportCsv")
    assert body == {
        "application": "Github",
        "duration": "LAST_15_DAYS",
        "users": [{"id": "1001"}, {"id": "1002"}],
    }
    assert (report, resp, err) == (CSV, response, None)


@pytest.mark.parametrize(
    "method, args",
    [
        ("export_shadow_it_report", ()),
        ("export_shadow_it_csv", ("Github", "USER")),
    ],
)
def test_export_errors_are_returned(method, args):
    error = Exception("boom")
    api, _, _ = _api(execute_error=error)

    assert getattr(api, method)(*args) == (None, None, error)
