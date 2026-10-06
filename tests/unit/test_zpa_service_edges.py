"""
Testing ZPA Service Edge API return shapes
"""

from unittest.mock import Mock

import pytest

from zscaler.zpa.models.service_edges import ServiceEdge
from zscaler.zpa.service_edges import ServiceEdgeControllerAPI

EDGE_ID = "72058304855099500"


def _api(body=None, create_error=None, execute_error=None):
    executor = Mock()
    executor.create_request.return_value = (None if create_error else {}, create_error)
    response = Mock()
    response.get_body.return_value = body or {}
    executor.execute.return_value = (None if execute_error else response, execute_error)
    return ServiceEdgeControllerAPI(executor, {"client": {"customerId": "1234567890"}}), response


def test_get_service_edge_returns_tuple():
    api, response = _api(body={"id": EDGE_ID, "name": "edge-a", "enabled": True})

    edge, resp, err = api.get_service_edge(EDGE_ID)

    assert err is None
    assert resp is response
    assert isinstance(edge, ServiceEdge)
    assert edge.id == EDGE_ID
    assert edge.name == "edge-a"


@pytest.mark.parametrize(
    "method, args",
    [
        ("get_service_edge", (EDGE_ID,)),
        ("delete_service_edge", (EDGE_ID,)),
        ("bulk_delete_service_edges", ([EDGE_ID],)),
    ],
)
def test_service_edge_errors_are_returned(method, args):
    error = Exception("boom")

    api, _ = _api(create_error=error)
    assert getattr(api, method)(*args) == (None, None, error)

    api, _ = _api(execute_error=error)
    assert getattr(api, method)(*args) == (None, None, error)


@pytest.mark.parametrize(
    "method, args",
    [
        ("delete_service_edge", (EDGE_ID,)),
        ("bulk_delete_service_edges", ([EDGE_ID],)),
    ],
)
def test_service_edge_deletes_return_tuple(method, args):
    api, response = _api()

    assert getattr(api, method)(*args) == (None, response, None)
