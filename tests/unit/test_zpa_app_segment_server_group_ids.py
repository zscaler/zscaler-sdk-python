"""
Unit tests for optional ``server_group_ids`` handling in the ZPA application
segment resources.

Passing ``server_group_ids=None`` -- the natural result of forwarding an
optional keyword argument whose default is ``None``, i.e. a partial update that
does not intend to change server groups -- used to raise
``TypeError: 'NoneType' object is not iterable`` inside the SDK before any
request was built. ``None`` must mean "not supplied", while an explicitly
supplied list (including an empty one) must still be sent as ``serverGroups``.
"""

import pytest

from zscaler.zpa.app_segments_ba import ApplicationSegmentBAAPI
from zscaler.zpa.app_segments_ba_v2 import AppSegmentsBAV2API
from zscaler.zpa.app_segments_inspection import AppSegmentsInspectionAPI
from zscaler.zpa.app_segments_pra import AppSegmentsPRAAPI
from zscaler.zpa.application_segment import ApplicationSegmentAPI

CONFIG = {"client": {"customerId": "1234567890"}}

SEGMENT_ID = "72058304855089379"
SERVER_GROUP_ID = "72058304855090128"


class CapturingExecutor:
    """Captures the body the SDK built, then short-circuits before any HTTP."""

    def __init__(self):
        self.body = None

    def create_request(self, method, endpoint, body=None, headers=None, params=None, **kwargs):
        self.body = body
        return None, "short-circuit"


# Every add/update entry point that reformats ``server_group_ids`` into ``serverGroups``.
SEGMENT_METHODS = [
    (ApplicationSegmentAPI, "add_segment", ()),
    (ApplicationSegmentAPI, "update_segment", (SEGMENT_ID,)),
    (ApplicationSegmentAPI, "add_segment_provision", ()),
    (AppSegmentsBAV2API, "add_segment_ba", ()),
    (AppSegmentsBAV2API, "update_segment_ba", (SEGMENT_ID,)),
    (ApplicationSegmentBAAPI, "add_segment_ba", ()),
    (ApplicationSegmentBAAPI, "update_segment_ba", (SEGMENT_ID,)),
    (AppSegmentsInspectionAPI, "add_segment_inspection", ()),
    (AppSegmentsInspectionAPI, "update_segment_inspection", (SEGMENT_ID,)),
    (AppSegmentsPRAAPI, "add_segment_pra", ()),
    (AppSegmentsPRAAPI, "update_segment_pra", (SEGMENT_ID,)),
]

METHOD_IDS = [f"{api_cls.__name__}.{method}" for api_cls, method, _ in SEGMENT_METHODS]


def build_body(api_cls, method, args, **kwargs):
    """Invoke a segment method and return the request body it assembled."""
    executor = CapturingExecutor()
    api = api_cls(executor, CONFIG)
    getattr(api, method)(*args, **kwargs)
    return executor.body


@pytest.mark.parametrize(("api_cls", "method", "args"), SEGMENT_METHODS, ids=METHOD_IDS)
def test_none_server_group_ids_is_treated_as_not_supplied(api_cls, method, args):
    body = build_body(api_cls, method, args, name="app.example.com", server_group_ids=None)

    assert "serverGroups" not in body
    assert "server_group_ids" not in body


@pytest.mark.parametrize(("api_cls", "method", "args"), SEGMENT_METHODS, ids=METHOD_IDS)
def test_server_group_ids_list_is_reformatted(api_cls, method, args):
    body = build_body(api_cls, method, args, name="app.example.com", server_group_ids=[SERVER_GROUP_ID])

    assert body["serverGroups"] == [{"id": SERVER_GROUP_ID}]
    assert "server_group_ids" not in body


@pytest.mark.parametrize(("api_cls", "method", "args"), SEGMENT_METHODS, ids=METHOD_IDS)
def test_empty_server_group_ids_is_still_sent(api_cls, method, args):
    body = build_body(api_cls, method, args, name="app.example.com", server_group_ids=[])

    assert body["serverGroups"] == []
