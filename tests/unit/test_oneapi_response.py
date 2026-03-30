"""
Testing OneAPI Response for Zscaler SDK
"""

import pytest
import json
import uuid
from unittest.mock import Mock, patch, MagicMock
from zscaler.oneapi_response import ZscalerAPIResponse


def test_zscaler_api_response_initialization():
    """Test ZscalerAPIResponse initialization."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response._url == "https://api.example.com/test"
    assert response._headers == {"Authorization": "Bearer token"}
    assert response._params == {"page": 1, "limit": 10}
    assert response._status == 200
    assert response._service_type == "zpa"
    assert response._page == 1
    assert response._items_fetched == 1
    assert response._pages_fetched == 1


def test_zscaler_api_response_initialization_with_data_type():
    """Test ZscalerAPIResponse initialization with data type."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    class TestModel:
        def __init__(self, data):
            self.id = data.get("id")
            self.name = data.get("name")

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
        data_type=TestModel,
    )

    assert response._type == TestModel
    assert response._status == 200


def test_zscaler_api_response_initialization_with_all_entries():
    """Test ZscalerAPIResponse initialization with all_entries flag."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
        all_entries=True,
    )

    assert response._params.get("allEntries") is True


def test_zscaler_api_response_initialization_with_sorting():
    """Test ZscalerAPIResponse initialization with sorting parameters."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
        sort_order="asc",
        sort_by="name",
        sort_dir="asc",
    )

    assert response._params.get("sortOrder") == "asc"
    assert response._params.get("sortBy") == "name"
    assert response._params.get("sortDir") == "asc"


def test_zscaler_api_response_initialization_with_time_range():
    """Test ZscalerAPIResponse initialization with time range parameters."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
        start_time="2024-01-01T00:00:00Z",
        end_time="2024-01-31T23:59:59Z",
    )

    assert response._params.get("startTime") == "2024-01-01T00:00:00Z"
    assert response._params.get("endTime") == "2024-01-31T23:59:59Z"


def test_validate_page_size():
    """Test page size validation for different service types."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    # Test ZPA service
    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    # Test with valid page size
    validated_size = response.validate_page_size(50, "zpa")
    assert validated_size == 50

    # Test with page size exceeding max
    validated_size = response.validate_page_size(1000, "zpa")
    assert validated_size == 500  # Max for ZPA

    # Test with page size below min
    validated_size = response.validate_page_size(0, "zdx")
    assert validated_size == 1  # Min for ZDX

    # Test with None page size - should return None to let API use its default
    validated_size = response.validate_page_size(None, "zia")
    assert validated_size is None  # Don't override API defaults


def test_get_headers():
    """Test getting response headers."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json", "X-Rate-Limit": "100"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    headers = response.get_headers()
    assert headers == {"Content-Type": "application/json", "X-Rate-Limit": "100"}


def test_get_body():
    """Test getting response body."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    body = response.get_body()
    assert body == {"list": [{"id": 1, "name": "test"}]}


def test_get_status():
    """Test getting response status code."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    status = response.get_status()
    assert status == 200


def test_build_json_response_zpa():
    """Test building JSON response for ZPA service."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}], "totalPages": 5, "totalCount": 25}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response._list == [{"id": 1, "name": "test"}]
    assert response._total_pages == 5
    assert response._total_count == 25


def test_build_json_response_zdx():
    """Test building JSON response for ZDX service."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"items": [{"id": 1, "name": "test"}], "next_offset": "abc123"}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zdx",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response._list == [{"id": 1, "name": "test"}]
    assert response._next_offset == "abc123"


def test_build_json_response_zidentity():
    """Test building JSON response for Zidentity service."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"records": [{"id": 1, "name": "test"}], "next_link": "https://api.example.com/next", "prev_link": "https://api.example.com/prev", "results_total": 100, "pageOffset": 0, "pageSize": 10}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zidentity",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response._list == [{"id": 1, "name": "test"}]
    assert response._next_link == "https://api.example.com/next"
    assert response._prev_link == "https://api.example.com/prev"
    assert response._results_total == 100
    assert response._page_offset == 0
    assert response._page_size == 10


def test_build_json_response_zcc():
    """Test building JSON response for ZCC service."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    # Test with single object
    response_body = '{"id": 1, "name": "test"}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zcc",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response._list == [{"id": 1, "name": "test"}]

    # Test with list of objects
    response_body = '[{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zcc",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response._list == [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]


def test_build_json_response_zia():
    """Test building JSON response for ZIA service."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    # Test with list response
    response_body = '[{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zia",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response._list == [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]


def test_get_results():
    """Test getting results from response."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    results = response.get_results()
    assert results == [{"id": 1, "name": "test"}]


def test_get_results_with_data_type():
    """Test getting results with data type wrapping."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    # For ZCC, the response body is a single object that gets wrapped in a list
    response_body = '{"id": 1, "name": "test"}'

    class TestModel:
        def __init__(self, data):
            self.id = data.get("id")
            self.name = data.get("name")

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zcc",
        res_details=mock_res_details,
        response_body=response_body,
        data_type=TestModel,
    )

    results = response.get_results()
    assert len(results) == 1
    assert isinstance(results[0], TestModel)
    assert results[0].id == 1
    assert results[0].name == "test"


def test_has_next_zpa():
    """Test has_next for ZPA service."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    # Test with more pages
    response_body = '{"list": [{"id": 1, "name": "test"}], "totalPages": 5, "totalCount": 25}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response.has_next() is True

    # Test with no more pages
    response._page = 5
    assert response.has_next() is False


def test_has_next_zdx():
    """Test has_next for ZDX service."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    # Test with next offset
    response_body = '{"items": [{"id": 1, "name": "test"}], "next_offset": "abc123"}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zdx",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response.has_next() is True

    # Test with no next offset
    response._next_offset = None
    assert response.has_next() is False


def test_has_next_zidentity():
    """Test has_next for Zidentity service."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    # Test with next link
    response_body = '{"records": [{"id": 1, "name": "test"}], "next_link": "https://api.example.com/next"}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zidentity",
        res_details=mock_res_details,
        response_body=response_body,
    )

    assert response.has_next() is True

    # Test with no next link
    response._next_link = None
    assert response.has_next() is False


def test_has_next_zia_zcc():
    """Test has_next for ZIA/ZCC services."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    # ZIA returns flat JSON arrays for paginated list endpoints.
    # _is_flat_list_response must be False so pagination can proceed.
    response_body = '[{"id": 1, "name": "test"}]'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zia",
        res_details=mock_res_details,
        response_body=response_body,
    )

    # ZIA flat list responses SHOULD allow pagination
    assert response._is_flat_list_response is False
    assert response.has_next() is True  # Got results → might have more

    # With explicit pageSize and fewer results than limit → no more pages
    req_with_size = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"pageSize": 10},
    }
    response_partial = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req_with_size,
        service_type="zia",
        res_details=mock_res_details,
        response_body=response_body,
    )
    # Simulate being on page 2 so the limit-based heuristic applies
    response_partial._pages_fetched = 2
    # 1 result < limit 10, so no more pages
    assert response_partial.has_next() is False

    # Test with no results
    response_empty = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req_with_size,
        service_type="zia",
        res_details=mock_res_details,
        response_body="[]",
    )
    assert response_empty.has_next() is False


def test_next_zpa():
    """Test next method for ZPA service."""
    mock_request_executor = Mock()
    mock_request_executor.fire_request.return_value = (None, None, '{"list": [{"id": 2, "name": "test2"}]}', None)

    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}], "totalPages": 5, "totalCount": 25}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    results, next_response, error = response.next()

    assert results == [{"id": 2, "name": "test2"}]
    assert next_response == response
    assert error is None


def test_next_zdx():
    """Test next method for ZDX service."""
    mock_request_executor = Mock()
    mock_request_executor.fire_request.return_value = (
        None,
        None,
        '{"items": [{"id": 2, "name": "test2"}], "next_offset": "def456"}',
        None,
    )

    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"items": [{"id": 1, "name": "test"}], "next_offset": "abc123"}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zdx",
        res_details=mock_res_details,
        response_body=response_body,
    )

    results, next_response, error = response.next()

    assert results == [{"id": 2, "name": "test2"}]
    assert next_response == response
    assert error is None


def test_next_zidentity():
    """Test next method for Zidentity service."""
    mock_request_executor = Mock()
    mock_request_executor.fire_request.return_value = (
        None,
        None,
        '{"records": [{"id": 2, "name": "test2"}], "next_link": "https://api.example.com/next2"}',
        None,
    )

    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"records": [{"id": 1, "name": "test"}], "next_link": "https://api.example.com/next"}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zidentity",
        res_details=mock_res_details,
        response_body=response_body,
    )

    results, next_response, error = response.next()

    assert results == [{"id": 2, "name": "test2"}]
    assert next_response == response
    assert error is None


def test_next_zia():
    """Test next method for ZIA service with paginated response."""
    mock_request_executor = Mock()
    mock_request_executor.fire_request.return_value = (None, None, '{"list": [{"id": 2, "name": "test2"}]}', None)

    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    # Use dict response format (paginated) instead of flat list
    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zia",
        res_details=mock_res_details,
        response_body=response_body,
    )

    # Dict responses support pagination
    assert response._is_flat_list_response is False

    results, next_response, error = response.next()

    assert results == [{"id": 2, "name": "test2"}]
    assert next_response == response
    assert error is None


def test_next_zia_flat_list_pagination():
    """Test that ZIA flat list responses DO support pagination."""
    mock_request_executor = Mock()

    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"pageSize": 10},
    }

    # ZIA returns flat list for paginated endpoints
    response_body = json.dumps([{"id": i} for i in range(10)])

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zia",
        res_details=mock_res_details,
        response_body=response_body,
    )

    # ZIA flat lists must NOT be marked as non-paginated
    assert response._is_flat_list_response is False
    assert response._limit == 10
    assert response.has_next() is True  # full page → might have more

    # Empty ZIA response → no more pages
    empty_resp = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zia",
        res_details=mock_res_details,
        response_body="[]",
    )
    assert empty_resp.has_next() is False
    with pytest.raises(StopIteration):
        empty_resp.next()


def test_next_no_more_pages():
    """Test next method when no more pages are available."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}], "totalPages": 1, "totalCount": 1}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    with pytest.raises(StopIteration):
        response.next()


def test_next_with_error():
    """Test next method when an error occurs."""
    mock_request_executor = Mock()
    mock_request_executor.fire_request.return_value = (None, None, None, "Network error")

    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}], "totalPages": 5, "totalCount": 25}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    results, next_response, error = response.next()

    assert results is None
    assert next_response == response
    assert error == "Network error"


def test_next_with_empty_results():
    """Test next method when results are empty."""
    mock_request_executor = Mock()
    mock_request_executor.fire_request.return_value = (None, None, '{"list": []}', None)

    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}], "totalPages": 5, "totalCount": 25}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    results, next_response, error = response.next()

    assert results is None
    assert next_response == response
    assert error is None


def test_next_with_data_type():
    """Test next method with data type wrapping."""
    mock_request_executor = Mock()
    mock_request_executor.fire_request.return_value = (None, None, '{"list": [{"id": 2, "name": "test2"}]}', None)

    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}], "totalPages": 5, "totalCount": 25}'

    class TestModel:
        def __init__(self, data):
            self.id = data.get("id")
            self.name = data.get("name")

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
        data_type=TestModel,
    )

    results, next_response, error = response.next()

    assert len(results) == 1
    assert isinstance(results[0], TestModel)
    assert results[0].id == 2
    assert results[0].name == "test2"
    assert next_response == response
    assert error is None


def test_str_representation():
    """Test string representation of response."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    str_repr = str(response)
    assert "id" in str_repr
    assert "name" in str_repr
    assert "test" in str_repr


def test_str_representation_with_error():
    """Test string representation when there's an error."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    # Mock get_results to raise an exception
    with patch.object(response, "get_results", side_effect=Exception("Test error")):
        str_repr = str(response)
        assert "error displaying results" in str_repr
        assert "Test error" in str_repr


def test_service_page_limits():
    """Test service page limits constants."""
    limits = ZscalerAPIResponse.SERVICE_PAGE_LIMITS

    assert "zpa" in limits
    assert "zia" in limits
    assert "zdx" in limits

    # Test ZPA limits
    assert limits["zpa"]["default"] == 100
    assert limits["zpa"]["max"] == 500

    # Test ZIA limits
    assert limits["zia"]["default"] == 500
    assert limits["zia"]["max"] == 10000

    # Test ZDX limits
    assert limits["zdx"]["default"] == 10
    assert limits["zdx"]["min"] == 1


def test_validate_page_size_edge_cases():
    """Test page size validation with edge cases."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="zpa",
        res_details=mock_res_details,
        response_body=response_body,
    )

    # Test with negative page size
    validated_size = response.validate_page_size(-5, "zpa")
    assert validated_size == 1

    # Test with very large page size
    validated_size = response.validate_page_size(999999, "zpa")
    assert validated_size == 500

    # Test with string page size
    validated_size = response.validate_page_size("50", "zpa")
    assert validated_size == 50

    # Test with float page size
    validated_size = response.validate_page_size(50.5, "zpa")
    assert validated_size == 50


def test_validate_page_size_unknown_service():
    """Test page size validation for unknown service type."""
    mock_request_executor = Mock()
    mock_res_details = Mock()
    mock_res_details.headers = {"Content-Type": "application/json"}
    mock_res_details.status_code = 200

    req = {
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1, "limit": 10},
    }

    response_body = '{"list": [{"id": 1, "name": "test"}]}'

    response = ZscalerAPIResponse(
        request_executor=mock_request_executor,
        req=req,
        service_type="unknown",
        res_details=mock_res_details,
        response_body=response_body,
    )

    # Test with None page size - should return None to let API use its default
    validated_size = response.validate_page_size(None, "unknown")
    assert validated_size is None  # Don't override API defaults

    # Test with page size exceeding max
    validated_size = response.validate_page_size(1000, "unknown")
    assert validated_size == 100  # Max for unknown service


# ---------------------------------------------------------------------------
# JMESPath .search() tests
# ---------------------------------------------------------------------------


def _make_response(body_str, service_type="zpa"):
    """Helper to build a ZscalerAPIResponse for search tests."""
    mock_executor = Mock()
    mock_res = Mock()
    mock_res.headers = {"Content-Type": "application/json"}
    mock_res.status_code = 200
    req = {
        "url": "https://api.example.com/test",
        "headers": {},
        "params": {},
    }
    return ZscalerAPIResponse(
        request_executor=mock_executor,
        req=req,
        service_type=service_type,
        res_details=mock_res,
        response_body=body_str,
    )


def test_search_filter_on_flat_list():
    """search() filters items from a flat-list response (ZIA-style)."""
    body = json.dumps(
        [
            {"id": 1, "name": "Alice", "adminUser": True},
            {"id": 2, "name": "Bob", "adminUser": False},
            {"id": 3, "name": "Carol", "adminUser": True},
        ]
    )
    resp = _make_response(body, service_type="zia")
    admins = resp.search("[?adminUser==`true`]")
    assert len(admins) == 2
    assert all(u["adminUser"] for u in admins)


def test_search_projection_on_flat_list():
    """search() can project (select) specific fields."""
    body = json.dumps(
        [
            {"id": 1, "name": "Alice", "email": "alice@z.com"},
            {"id": 2, "name": "Bob", "email": "bob@z.com"},
        ]
    )
    resp = _make_response(body, service_type="zia")
    names = resp.search("[*].name")
    assert names == ["Alice", "Bob"]


def test_search_filter_and_projection():
    """search() filters and projects in a single expression."""
    body = json.dumps(
        [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Carol", "role": "admin"},
        ]
    )
    resp = _make_response(body, service_type="zia")
    result = resp.search("[?role=='admin'].{name: name, id: id}")
    assert result == [
        {"name": "Alice", "id": 1},
        {"name": "Carol", "id": 3},
    ]


def test_search_on_dict_with_list_key():
    """search() works against dict responses (e.g. ZPA 'list' key)."""
    body = json.dumps(
        {
            "list": [
                {"id": 1, "name": "AppA", "enabled": True},
                {"id": 2, "name": "AppB", "enabled": False},
            ],
            "totalPages": 1,
            "totalCount": 2,
        }
    )
    resp = _make_response(body, service_type="zpa")
    enabled = resp.search("list[?enabled==`true`]")
    assert len(enabled) == 1
    assert enabled[0]["name"] == "AppA"


def test_search_on_zdx_items():
    """search() can filter items inside ZDX 'items' key."""
    body = json.dumps(
        {
            "items": [
                {"software_name": "Zscaler Client Connector", "vendor": "Zscaler", "device_total": 100},
                {"software_name": "Chrome", "vendor": "Google", "device_total": 250},
                {"software_name": "Zscaler Digital Experience", "vendor": "Zscaler", "device_total": 50},
            ],
            "next_offset": "abc123",
        }
    )
    resp = _make_response(body, service_type="zdx")
    result = resp.search("items[?vendor=='Zscaler'].{name: software_name, devices: device_total}")
    assert len(result) == 2
    assert result[0] == {"name": "Zscaler Client Connector", "devices": 100}
    assert result[1] == {"name": "Zscaler Digital Experience", "devices": 50}


def test_search_on_zbi_reports():
    """search() works on ZBI responses with 'reports' key."""
    body = json.dumps(
        {
            "reportType": "APPLICATION",
            "reports": [
                {"id": "r1", "status": "COMPLETED"},
                {"id": "r2", "status": "PENDING"},
                {"id": "r3", "status": "COMPLETED"},
            ],
        }
    )
    resp = _make_response(body, service_type="bi")
    completed = resp.search("reports[?status=='COMPLETED']")
    assert len(completed) == 2


def test_search_no_match_returns_empty():
    """search() returns [] when nothing matches."""
    body = json.dumps(
        [
            {"id": 1, "name": "Alice"},
        ]
    )
    resp = _make_response(body, service_type="zia")
    result = resp.search("[?name=='Nobody']")
    assert result == []


def test_search_scalar_result_wrapped_in_list():
    """A JMESPath expression that returns a scalar wraps it in a list."""
    body = json.dumps(
        {
            "list": [{"id": 1}, {"id": 2}],
            "totalPages": 1,
            "totalCount": 2,
        }
    )
    resp = _make_response(body, service_type="zpa")
    result = resp.search("totalCount")
    assert result == [2]


def test_search_invalid_expression_raises():
    """An invalid JMESPath expression raises ParseError."""
    import jmespath

    body = json.dumps([{"id": 1}])
    resp = _make_response(body, service_type="zia")
    with pytest.raises(jmespath.exceptions.ParseError):
        resp.search("[invalid!!")


def test_search_length_function():
    """search() supports JMESPath built-in functions like length()."""
    body = json.dumps(
        [
            {"id": 1, "tags": ["a", "b"]},
            {"id": 2, "tags": ["a"]},
            {"id": 3, "tags": ["a", "b", "c"]},
        ]
    )
    resp = _make_response(body, service_type="zia")
    result = resp.search("[?length(tags) > `1`].id")
    assert sorted(result) == [1, 3]
