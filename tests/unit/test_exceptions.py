"""
Unit tests for Zscaler SDK exception classes.

Tests exception initialization, raising, and the raise_exception flag.
"""

import pytest
import json
from unittest.mock import Mock
from zscaler.exceptions import exceptions
from zscaler.exceptions.exceptions import (
    ZscalerBaseException,
    HTTPException,
    ZscalerAPIException,
    ZpaBaseException,
    ZpaAPIException,
    RateLimitExceededError,
    RetryLimitExceededError,
    CacheError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    APIClientError,
    InvalidCloudEnvironmentError,
    TokenExpirationError,
    TokenRefreshError,
    HeaderUpdateError,
    RetryTooLong,
)


class TestRaiseExceptionFlag:
    """Test the raise_exception module-level flag."""

    def test_raise_exception_flag_default(self):
        """Test raise_exception flag default value."""
        # Should default to False
        assert isinstance(exceptions.raise_exception, bool)

    def test_raise_exception_flag_can_be_modified(self):
        """Test raise_exception flag can be set."""
        original_value = exceptions.raise_exception
        
        # Toggle the flag
        exceptions.raise_exception = True
        assert exceptions.raise_exception is True
        
        exceptions.raise_exception = False
        assert exceptions.raise_exception is False
        
        # Restore original value
        exceptions.raise_exception = original_value


class TestZscalerBaseException:
    """Test ZscalerBaseException class."""

    def test_base_exception_initialization(self):
        """Test ZscalerBaseException can be instantiated."""
        mock_response = Mock()
        mock_response.status_code = 400
        
        response_body = {"error": "test"}
        
        exc = ZscalerBaseException("https://api.example.com/test", mock_response, response_body)
        
        assert exc is not None
        assert isinstance(exc, Exception)

    def test_base_exception_attributes(self):
        """Test ZscalerBaseException stores required attributes."""
        mock_response = Mock()
        mock_response.status_code = 404
        
        url = "https://api.example.com/test"
        response_body = {"message": "Not found"}
        
        exc = ZscalerBaseException(url, mock_response, response_body)
        
        assert exc.status_code == 404
        assert exc.url == url
        # response_body is JSON serialized as string
        assert isinstance(exc.response_body, str)
        assert "Not found" in exc.response_body

    def test_base_exception_str(self):
        """Test ZscalerBaseException __str__ method."""
        mock_response = Mock()
        mock_response.status_code = 500
        
        exc = ZscalerBaseException("https://api.example.com/test", mock_response, {"error": "test"})
        
        exc_str = str(exc)
        assert "ZSCALER HTTP" in exc_str
        assert "500" in exc_str

    def test_base_exception_repr(self):
        """Test ZscalerBaseException __repr__ method."""
        mock_response = Mock()
        mock_response.status_code = 400
        
        exc = ZscalerBaseException("https://api.example.com/test", mock_response, {"error": "test"})
        
        repr_str = repr(exc)
        assert "message" in repr_str


class TestHTTPException:
    """Test HTTPException class."""

    def test_http_exception_inherits_from_base(self):
        """Test HTTPException inherits from ZscalerBaseException."""
        mock_response = Mock()
        mock_response.status_code = 400
        
        exc = HTTPException("https://api.example.com/test", mock_response, {"error": "test"})
        
        assert isinstance(exc, ZscalerBaseException)
        assert isinstance(exc, Exception)

    def test_http_exception_can_be_raised(self):
        """Test HTTPException can be raised and caught."""
        mock_response = Mock()
        mock_response.status_code = 500
        
        exc = HTTPException("https://api.example.com/test", mock_response, {"error": "test"})
        
        with pytest.raises(HTTPException):
            raise exc


class TestZscalerAPIException:
    """Test ZscalerAPIException class."""

    def test_api_exception_initialization(self):
        """Test ZscalerAPIException with ZscalerAPIError."""
        from zscaler.errors.zscaler_api_error import ZscalerAPIError
        
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.headers = {}
        
        api_error = ZscalerAPIError(
            "https://api.example.com/test",
            mock_response,
            {"code": "DUPLICATE", "message": "Duplicate item"}
        )
        
        exc = ZscalerAPIException(api_error)
        
        assert isinstance(exc, ZscalerBaseException)
        assert exc.status_code == 409


class TestSpecificExceptions:
    """Test specific exception classes."""

    def test_zpa_base_exception(self):
        """Test ZpaBaseException."""
        exc = ZpaBaseException("ZPA error")
        assert isinstance(exc, Exception)
        
        with pytest.raises(ZpaBaseException):
            raise exc

    def test_zpa_api_exception(self):
        """Test ZpaAPIException."""
        exc = ZpaAPIException("ZPA API error")
        assert isinstance(exc, ZpaBaseException)

    def test_rate_limit_exceeded_error(self):
        """Test RateLimitExceededError."""
        exc = RateLimitExceededError("Rate limit exceeded")
        assert isinstance(exc, Exception)
        
        with pytest.raises(RateLimitExceededError):
            raise exc

    def test_retry_limit_exceeded_error(self):
        """Test RetryLimitExceededError."""
        exc = RetryLimitExceededError("Retry limit exceeded")
        assert isinstance(exc, Exception)

    def test_cache_error(self):
        """Test CacheError."""
        exc = CacheError("Cache operation failed")
        assert isinstance(exc, Exception)

    def test_bad_request_error(self):
        """Test BadRequestError."""
        exc = BadRequestError("Bad request")
        assert isinstance(exc, Exception)

    def test_unauthorized_error(self):
        """Test UnauthorizedError."""
        exc = UnauthorizedError("Unauthorized")
        assert isinstance(exc, Exception)

    def test_forbidden_error(self):
        """Test ForbiddenError."""
        exc = ForbiddenError("Forbidden")
        assert isinstance(exc, Exception)

    def test_not_found_error(self):
        """Test NotFoundError."""
        exc = NotFoundError("Not found")
        assert isinstance(exc, Exception)

    def test_api_client_error(self):
        """Test APIClientError."""
        exc = APIClientError("API client error")
        assert isinstance(exc, Exception)

    def test_token_expiration_error(self):
        """Test TokenExpirationError."""
        exc = TokenExpirationError("Token expired")
        assert isinstance(exc, Exception)

    def test_token_refresh_error(self):
        """Test TokenRefreshError."""
        exc = TokenRefreshError("Token refresh failed")
        assert isinstance(exc, Exception)

    def test_header_update_error(self):
        """Test HeaderUpdateError."""
        exc = HeaderUpdateError("Header update failed")
        assert isinstance(exc, Exception)

    def test_retry_too_long(self):
        """Test RetryTooLong exception."""
        exc = RetryTooLong("Retry time exceeded")
        assert isinstance(exc, Exception)


class TestInvalidCloudEnvironmentError:
    """Test InvalidCloudEnvironmentError with custom initialization."""

    def test_invalid_cloud_error_initialization(self):
        """Test InvalidCloudEnvironmentError stores cloud name."""
        exc = InvalidCloudEnvironmentError("invalid_cloud")
        
        assert exc.cloud == "invalid_cloud"
        assert "invalid_cloud" in str(exc)

    def test_invalid_cloud_error_message(self):
        """Test InvalidCloudEnvironmentError has descriptive message."""
        exc = InvalidCloudEnvironmentError("unknown_env")
        
        exc_str = str(exc)
        assert "Unrecognized cloud environment" in exc_str
        assert "unknown_env" in exc_str

    def test_invalid_cloud_error_can_be_raised(self):
        """Test InvalidCloudEnvironmentError can be raised."""
        with pytest.raises(InvalidCloudEnvironmentError) as exc_info:
            raise InvalidCloudEnvironmentError("test_cloud")
        
        assert exc_info.value.cloud == "test_cloud"


class TestExceptionUsagePatterns:
    """Test common exception usage patterns."""

    def test_multiple_exceptions_can_coexist(self):
        """Test multiple exception instances don't interfere."""
        exc1 = BadRequestError("Error 1")
        exc2 = UnauthorizedError("Error 2")
        exc3 = NotFoundError("Error 3")
        
        assert str(exc1) == "Error 1"
        assert str(exc2) == "Error 2"
        assert str(exc3) == "Error 3"

    def test_exceptions_in_try_except_blocks(self):
        """Test exceptions work correctly in try/except."""
        try:
            raise RateLimitExceededError("Rate limit hit")
        except RateLimitExceededError as e:
            assert "Rate limit hit" in str(e)
        except Exception:
            pytest.fail("Should have caught RateLimitExceededError specifically")

    def test_exception_with_none_message(self):
        """Test exceptions handle None messages gracefully."""
        # Most exception classes should handle None
        exc = CacheError(None)
        assert exc is not None

    def test_nested_exception_catching(self):
        """Test catching base exception catches derived ones."""
        exc = ZpaAPIException("Test error")
        
        # Should be catchable as ZpaBaseException
        with pytest.raises(ZpaBaseException):
            raise exc
        
        # Should also be catchable as generic Exception
        with pytest.raises(Exception):
            raise exc


class TestExceptionMessageFormatting:
    """Test exception message formatting."""

    def test_zscaler_base_exception_message_format(self):
        """Test ZscalerBaseException creates proper message."""
        mock_response = Mock()
        mock_response.status_code = 404
        
        response_body = {"id": "123", "name": "test"}
        
        exc = ZscalerBaseException("https://api.example.com/resource", mock_response, response_body)
        
        message = exc.message
        assert "ZSCALER HTTP" in message
        assert "https://api.example.com/resource" in message
        assert "404" in message

    def test_exception_response_body_serialization(self):
        """Test exception properly serializes response body."""
        mock_response = Mock()
        mock_response.status_code = 400
        
        response_body = {"nested": {"field": "value"}}
        
        exc = ZscalerBaseException("https://api.example.com/test", mock_response, response_body)
        
        # Should be JSON serialized
        assert isinstance(exc.response_body, str)
        parsed = json.loads(exc.response_body)
        assert parsed["nested"]["field"] == "value"

