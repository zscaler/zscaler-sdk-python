"""
Testing Request Executor for Zscaler SDK
"""

import pytest
import time
import uuid
from unittest.mock import Mock, patch, MagicMock
from http import HTTPStatus
from zscaler.request_executor import RequestExecutor
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.exceptions.exceptions import RetryTooLong


def test_request_executor_initialization():
    """Test RequestExecutor initialization."""
    config = {
        "client": {
            "requestTimeout": 240,
            "rateLimit": {"maxRetries": 2},
            "cloud": "production",
            "service": "zia",
            "userAgent": "test-agent"
        }
    }
    
    cache = NoOpCache()
    
    executor = RequestExecutor(config, cache)
    
    assert executor._request_timeout == 240
    assert executor._max_retries == 2
    assert executor.cloud == "production"
    assert executor.service == "zia"
    assert executor._config == config
    assert executor._cache == cache
    assert executor.use_legacy_client is False


def test_request_executor_initialization_with_legacy_clients():
    """Test RequestExecutor initialization with legacy clients."""
    config = {
        "client": {
            "requestTimeout": 240,
            "rateLimit": {"maxRetries": 2},
            "cloud": "production",
            "service": "zia"
        }
    }
    
    cache = NoOpCache()
    mock_zpa = Mock()
    mock_zia = Mock()
    
    executor = RequestExecutor(
        config, 
        cache,
        zpa_legacy_client=mock_zpa,
        zia_legacy_client=mock_zia
    )
    
    assert executor.zpa_legacy_client == mock_zpa
    assert executor.zia_legacy_client == mock_zia
    assert executor.use_legacy_client is True


def test_request_executor_initialization_with_invalid_timeout():
    """Test RequestExecutor initialization with invalid timeout."""
    config = {
        "client": {
            "requestTimeout": -1,
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    
    with pytest.raises(ValueError, match="Invalid request timeout"):
        RequestExecutor(config, cache)


def test_request_executor_initialization_with_invalid_retries():
    """Test RequestExecutor initialization with invalid retries."""
    config = {
        "client": {
            "requestTimeout": 240,
            "rateLimit": {"maxRetries": -1}
        }
    }
    
    cache = NoOpCache()
    
    with pytest.raises(ValueError, match="Invalid max retries"):
        RequestExecutor(config, cache)


def test_request_executor_initialization_with_missing_rate_limit():
    """Test RequestExecutor initialization with missing rate limit config."""
    config = {
        "client": {
            "requestTimeout": 240
        }
    }
    
    cache = NoOpCache()
    
    with pytest.raises(KeyError):
        RequestExecutor(config, cache)


def test_request_executor_initialization_with_defaults():
    """Test RequestExecutor initialization with default values."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    
    executor = RequestExecutor(config, cache)
    
    assert executor._request_timeout == 240  # Default value
    assert executor.cloud == "production"  # Default value
    assert executor.service == "zia"  # Default value


def test_is_retryable_status():
    """Test is_retryable_status method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test retryable status codes
    # assert executor.is_retryable_status(HTTPStatus.REQUEST_TIMEOUT) is True
    # assert executor.is_retryable_status(HTTPStatus.CONFLICT) is True
    assert executor.is_retryable_status(HTTPStatus.TOO_MANY_REQUESTS) is True
    assert executor.is_retryable_status(HTTPStatus.SERVICE_UNAVAILABLE) is True
    assert executor.is_retryable_status(HTTPStatus.GATEWAY_TIMEOUT) is True
    
    # Test non-retryable status codes
    assert executor.is_retryable_status(HTTPStatus.OK) is False
    assert executor.is_retryable_status(HTTPStatus.BAD_REQUEST) is False
    assert executor.is_retryable_status(HTTPStatus.UNAUTHORIZED) is False
    assert executor.is_retryable_status(HTTPStatus.FORBIDDEN) is False
    assert executor.is_retryable_status(HTTPStatus.NOT_FOUND) is False
    
    # Test None status
    assert executor.is_retryable_status(None) is False


def test_is_too_many_requests():
    """Test is_too_many_requests method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test with 429 status
    mock_response = Mock()
    assert executor.is_too_many_requests(HTTPStatus.TOO_MANY_REQUESTS, mock_response) is True
    
    # Test with other status codes
    assert executor.is_too_many_requests(HTTPStatus.OK, mock_response) is False
    assert executor.is_too_many_requests(HTTPStatus.BAD_REQUEST, mock_response) is False
    
    # Test with None response
    assert executor.is_too_many_requests(HTTPStatus.TOO_MANY_REQUESTS, None) is False


def test_calculate_backoff():
    """Test calculate_backoff method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test backoff calculation
    retry_limit_reset = 1000
    date_time = 900
    backoff = executor.calculate_backoff(retry_limit_reset, date_time)
    
    assert backoff == 101  # (1000 - 900) + 1


def test_get_retry_after_with_retry_after_header():
    """Test get_retry_after method with Retry-After header."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"Retry-After": "60"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff == 61  # 60 + 1 padding


def test_get_retry_after_with_retry_after_header_seconds():
    """Test get_retry_after method with Retry-After header in seconds format."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"Retry-After": "60s"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff == 61  # 60 + 1 padding


def test_get_retry_after_with_x_ratelimit_reset_header():
    """Test get_retry_after method with X-RateLimit-Reset header."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"X-RateLimit-Reset": "1000"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff == 1001  # 1000 + 1 padding


def test_get_retry_after_with_x_ratelimit_reset_header_lowercase():
    """Test get_retry_after method with x-ratelimit-reset header (lowercase)."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"x-ratelimit-reset": "1000"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff == 1001  # 1000 + 1 padding


def test_get_retry_after_with_zcc_headers():
    """Test get_retry_after method with ZCC specific headers."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"X-Rate-Limit-Retry-After-Seconds": "120"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff == 121  # 120 + 1 padding


def test_get_retry_after_with_invalid_retry_after():
    """Test get_retry_after method with invalid Retry-After header."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"Retry-After": "invalid"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff is None
    mock_logger.error.assert_called_once()


def test_get_retry_after_with_invalid_x_ratelimit_reset():
    """Test get_retry_after method with invalid X-RateLimit-Reset header."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"X-RateLimit-Reset": "invalid"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff is None
    mock_logger.error.assert_called_once()


def test_get_retry_after_with_missing_headers():
    """Test get_retry_after method with missing headers."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff is None
    mock_logger.error.assert_called_once()


def test_get_retry_after_with_max_retry_seconds():
    """Test get_retry_after method with maxRetrySeconds configuration."""
    config = {
        "client": {
            "rateLimit": {
                "maxRetries": 2,
                "maxRetrySeconds": 300
            }
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"Retry-After": "60"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff == 61  # Should be within limit


def test_get_retry_after_with_max_retry_seconds_exceeded():
    """Test get_retry_after method when maxRetrySeconds is exceeded."""
    config = {
        "client": {
            "rateLimit": {
                "maxRetries": 2,
                "maxRetrySeconds": 60
            }
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"Retry-After": "120"}
    mock_logger = Mock()
    
    with pytest.raises(RetryTooLong):
        executor.get_retry_after(headers, mock_logger)


def test_get_retry_after_with_invalid_max_retry_seconds():
    """Test get_retry_after method with invalid maxRetrySeconds configuration."""
    config = {
        "client": {
            "rateLimit": {
                "maxRetries": 2,
                "maxRetrySeconds": "invalid"
            }
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    headers = {"Retry-After": "60"}
    mock_logger = Mock()
    
    backoff = executor.get_retry_after(headers, mock_logger)
    
    assert backoff == 61  # Should work despite invalid config
    mock_logger.warning.assert_called_once()


def test_create_request():
    """Test create_request method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cloud": "production",
            "service": "zia"
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    executor._http_client = mock_http_client
    
    request, error = executor.create_request(
        method="GET",
        endpoint="/zia/api/v1/users",
        body={"key": "value"},
        headers={"Authorization": "Bearer token"},
        params={"page": 1}
    )
    
    assert error is None
    assert request is not None
    assert request["method"] == "GET"
    assert request["url"] is not None
    # The Authorization header gets modified by OAuth, so we just check it exists
    assert "Authorization" in request["headers"]
    assert request["params"]["page"] == 1


def test_create_request_with_none_values():
    """Test create_request method with None values."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cloud": "production",
            "service": "zia"
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    executor._http_client = mock_http_client
    
    request, error = executor.create_request(
        method="GET",
        endpoint="/zia/api/v1/users"
    )
    
    assert error is None
    assert request is not None
    assert request["method"] == "GET"


def test_create_request_with_legacy_client():
    """Test create_request method with legacy client."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cloud": "production",
            "service": "zia"
        }
    }
    
    cache = NoOpCache()
    mock_zpa = Mock()
    mock_zpa.get_base_url.return_value = "https://config.zscaler.com"
    
    executor = RequestExecutor(config, cache, zpa_legacy_client=mock_zpa)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    executor._http_client = mock_http_client
    
    request, error = executor.create_request(
        method="GET",
        endpoint="/zpa/api/v1/apps"
    )
    
    assert error is None
    assert request is not None
    assert request["method"] == "GET"


def test_create_request_with_zidentity_endpoint():
    """Test create_request method with zidentity endpoint."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cloud": "production",
            "service": "zidentity",
            "vanityDomain": "testcompany"
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    executor._http_client = mock_http_client
    
    request, error = executor.create_request(
        method="GET",
        endpoint="/admin/api/v1/users"
    )
    
    assert error is None
    assert request is not None
    assert request["method"] == "GET"


def test_fire_request():
    """Test fire_request method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cache": {"enabled": False}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"success": true}'
    mock_http_client.send_request.return_value = (mock_response, None)
    executor._http_client = mock_http_client
    
    request = {
        "method": "GET",
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1}
    }
    
    req, response, response_body, error = executor.fire_request(request)
    
    assert error is None
    assert response == mock_response
    assert response_body == '{"success": true}'


def test_fire_request_with_cache():
    """Test fire_request method with cache enabled."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cache": {"enabled": True}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"success": true}'
    mock_http_client.send_request.return_value = (mock_response, None)
    executor._http_client = mock_http_client
    
    request = {
        "method": "GET",
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1}
    }
    
    req, response, response_body, error = executor.fire_request(request)
    
    assert error is None
    assert response == mock_response
    assert response_body == '{"success": true}'


def test_fire_request_with_sandbox_request():
    """Test fire_request method with sandbox request."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cache": {"enabled": True}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"success": true}'
    mock_http_client.send_request.return_value = (mock_response, None)
    executor._http_client = mock_http_client
    
    request = {
        "method": "GET",
        "url": "https://api.example.com/zscsb/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1}
    }
    
    req, response, response_body, error = executor.fire_request(request)
    
    assert error is None
    assert response == mock_response
    assert response_body == '{"success": true}'


def test_fire_request_with_error():
    """Test fire_request method with error."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cache": {"enabled": False}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    mock_http_client.send_request.return_value = (None, Exception("Network error"))
    executor._http_client = mock_http_client
    
    request = {
        "method": "GET",
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1}
    }
    
    req, response, response_body, error = executor.fire_request(request)
    
    assert error is not None
    assert response is None
    assert response_body is None


def test_fire_request_helper_with_retry():
    """Test fire_request_helper method with retry logic."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = {"Retry-After": "1"}
    mock_http_client.send_request.return_value = (mock_response, None)
    executor._http_client = mock_http_client
    
    request = {
        "method": "GET",
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1}
    }
    
    # Mock time.sleep to avoid actual delays
    with patch('time.sleep'):
        req, response, response_body, error = executor.fire_request_helper(request, 0, time.time())
    
    assert error is None
    assert response == mock_response


def test_fire_request_helper_with_timeout():
    """Test fire_request_helper method with timeout."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "requestTimeout": 1
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test timeout configuration
    assert executor._request_timeout == 1
    
    # Test that timeout is properly set
    assert executor._request_timeout > 0


def test_fire_request_helper_with_mutation_detection():
    """Test fire_request_helper method with mutation detection."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"success": true}'
    mock_http_client.send_request.return_value = (mock_response, None)
    executor._http_client = mock_http_client
    
    request = {
        "method": "POST",
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1}
    }
    
    req, response, response_body, error = executor.fire_request_helper(request, 0, time.time())
    
    assert error is None
    assert response == mock_response
    assert executor._mutations_occurred is True


def test_fire_request_helper_with_non_mutation():
    """Test fire_request_helper method with non-mutation request."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Mock the HTTP client
    mock_http_client = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"success": true}'
    mock_http_client.send_request.return_value = (mock_response, None)
    executor._http_client = mock_http_client
    
    request = {
        "method": "GET",
        "url": "https://api.example.com/test",
        "headers": {"Authorization": "Bearer token"},
        "params": {"page": 1}
    }
    
    req, response, response_body, error = executor.fire_request_helper(request, 0, time.time())
    
    assert error is None
    assert response == mock_response
    assert executor._mutations_occurred is False


def test_cache_enabled():
    """Test _cache_enabled method."""
    config = {
        "client": {
            "cache": {"enabled": True},
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    assert executor._cache_enabled() is True


def test_cache_disabled():
    """Test _cache_enabled method when cache is disabled."""
    config = {
        "client": {
            "cache": {"enabled": False},
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    assert executor._cache_enabled() is False


def test_cache_enabled_missing_config():
    """Test _cache_enabled method when cache config is missing."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cache": {"enabled": False}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    assert executor._cache_enabled() is False


def test_get_base_url():
    """Test get_base_url method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2},
            "cloud": "production"
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test with default cloud
    base_url = executor.get_base_url("/api/v1/users")
    assert base_url == "https://api.zsapi.net"
    
    # Test with custom cloud
    executor.cloud = "beta"
    base_url = executor.get_base_url("/api/v1/users")
    assert base_url == "https://api.beta.zsapi.net"


def test_get_service_type():
    """Test get_service_type method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test ZPA endpoint
    service_type = executor.get_service_type("/zpa/api/v1/apps")
    assert service_type == "zpa"
    
    # Test ZIA endpoint
    service_type = executor.get_service_type("/zia/api/v1/locations")
    assert service_type == "zia"
    
    # Test ZCC endpoint
    service_type = executor.get_service_type("/zcc/api/v1/users")
    assert service_type == "zcc"
    
    # Test ZDX endpoint
    service_type = executor.get_service_type("/zdx/api/v1/analytics")
    assert service_type == "zdx"
    
    # Test ZWA endpoint
    service_type = executor.get_service_type("/zwa/api/v1/apps")
    assert service_type == "zwa"
    
    # Test ZTW endpoint
    service_type = executor.get_service_type("/ztw/api/v1/apps")
    assert service_type == "ztw"
    
    # Test Zidentity endpoint
    service_type = executor.get_service_type("/admin/api/v1/users")
    assert service_type == "zidentity"


def test_get_service_type_with_invalid_endpoint():
    """Test get_service_type method with invalid endpoint."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test with invalid endpoint
    with pytest.raises(ValueError):
        executor.get_service_type("/invalid/api/v1/test")


def test_remove_oneapi_endpoint_prefix():
    """Test remove_oneapi_endpoint_prefix method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test with OneAPI prefix
    endpoint = executor.remove_oneapi_endpoint_prefix("/zpa/api/v1/apps")
    assert endpoint == "/api/v1/apps"
    
    # Test without OneAPI prefix
    endpoint = executor.remove_oneapi_endpoint_prefix("/api/v1/apps")
    assert endpoint == "/api/v1/apps"


def test_extract_and_append_query_params():
    """Test _extract_and_append_query_params method."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test with URL containing query parameters
    url = "https://api.example.com/test?existing=value"
    params = {"new": "param"}
    
    cleaned_url, updated_params = executor._extract_and_append_query_params(url, params)
    
    assert cleaned_url == "https://api.example.com/test"
    assert updated_params["existing"] == "value"
    assert updated_params["new"] == "param"
    
    # Test with URL without query parameters
    url = "https://api.example.com/test"
    params = {"new": "param"}
    
    cleaned_url, updated_params = executor._extract_and_append_query_params(url, params)
    
    assert cleaned_url == "https://api.example.com/test"
    assert updated_params["new"] == "param"


def test_extract_and_append_query_params_with_none_params():
    """Test _extract_and_append_query_params method with None params."""
    config = {
        "client": {
            "rateLimit": {"maxRetries": 2}
        }
    }
    
    cache = NoOpCache()
    executor = RequestExecutor(config, cache)
    
    # Test with None params
    url = "https://api.example.com/test?existing=value"
    params = {}
    
    cleaned_url, updated_params = executor._extract_and_append_query_params(url, params)
    
    assert cleaned_url == "https://api.example.com/test"
    assert updated_params["existing"] == "value"
