"""
Testing ZPA application segment ``server_group_ids`` → ``serverGroups`` mapping
"""

from unittest.mock import Mock

import pytest

from zscaler.zpa.app_segments_ba import ApplicationSegmentBAAPI
from zscaler.zpa.app_segments_ba_v2 import AppSegmentsBAV2API
from zscaler.zpa.app_segments_inspection import AppSegmentsInspectionAPI
from zscaler.zpa.app_segments_pra import AppSegmentsPRAAPI
from zscaler.zpa.application_segment import ApplicationSegmentAPI

SEGMENT_ID = "72058304855089379"
SERVER_GROUP_ID = "72058304855090128"

SEGMENT_METHODS = [
    (ApplicationSegmentAPI, "add_segment", ()),
    (ApplicationSegmentAPI, "update_segment", (SEGMENT_ID,)),
    (ApplicationSegmentBAAPI, "add_segment_ba", ()),
    (ApplicationSegmentBAAPI, "update_segment_ba", (SEGMENT_ID,)),
    (AppSegmentsBAV2API, "add_segment_ba", ()),
    (AppSegmentsBAV2API, "update_segment_ba", (SEGMENT_ID,)),
    (AppSegmentsInspectionAPI, "add_segment_inspection", ()),
    (AppSegmentsInspectionAPI, "update_segment_inspection", (SEGMENT_ID,)),
    (AppSegmentsPRAAPI, "add_segment_pra", ()),
    (AppSegmentsPRAAPI, "update_segment_pra", (SEGMENT_ID,)),
]


def _build_body(api_cls, method, args, server_group_ids):
    """Invoke a segment method and return the body it passed to create_request."""
    executor = Mock()
    executor.create_request.return_value = (None, "short-circuit")
    api = api_cls(executor, {"client": {"customerId": "1234567890"}})

    getattr(api, method)(*args, name="app.example.com", server_group_ids=server_group_ids)

    call = executor.create_request.call_args
    return call.kwargs["body"] if "body" in call.kwargs else call.args[2]


@pytest.mark.parametrize(
    "server_group_ids, expected",
    [
        ([SERVER_GROUP_ID], [{"id": SERVER_GROUP_ID}]),
        ([], []),
    ],
    ids=["list", "empty-list"],
)
@pytest.mark.parametrize("api_cls, method, args", SEGMENT_METHODS, ids=[f"{c.__name__}.{m}" for c, m, _ in SEGMENT_METHODS])
def test_server_group_ids_mapped_to_server_groups(api_cls, method, args, server_group_ids, expected):
    body = _build_body(api_cls, method, args, server_group_ids)

    assert body["serverGroups"] == expected
    assert "server_group_ids" not in body


@pytest.mark.parametrize("api_cls, method, args", SEGMENT_METHODS, ids=[f"{c.__name__}.{m}" for c, m, _ in SEGMENT_METHODS])
def test_server_group_ids_none_is_omitted(api_cls, method, args):
    body = _build_body(api_cls, method, args, None)

    assert "serverGroups" not in body
    assert "server_group_ids" not in body
