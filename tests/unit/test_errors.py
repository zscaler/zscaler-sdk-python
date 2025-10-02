"""
Unit tests for Zscaler SDK error classes.

Tests error initialization, formatting, and serialization.
"""

import pytest
import json
from unittest.mock import Mock
from zscaler.errors.error import Error
from zscaler.errors.http_error import HTTPError
from zscaler.errors.zscaler_api_error import ZscalerAPIError
from zscaler.errors.response_checker import check_response_for_error


class TestBaseError:
    """Test base Error class."""

    def test_error_initialization(self):
        """Test Error class can be instantiated."""
        error = Error()
        assert error is not None
        assert hasattr(error, 'message')

    def test_error_default_message(self):
        """Test Error has empty message by default."""
        error = Error()
        assert error.message == ""

    def test_error_repr(self):
        """Test Error __repr__ returns dict-like string."""
        error = Error()
        error.message = "Test error"
        repr_str = repr(error)
        
        assert "message" in repr_str
        assert "Test error" in repr_str

    def test_error_message_can_be_set(self):
        """Test Error message attribute can be modified."""
        error = Error()
        error.message = "Custom error message"
        assert error.message == "Custom error message"


class TestHTTPError:
    """Test HTTPError class."""

    def test_http_error_initialization(self):
        """Test HTTPError can be instantiated."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {"Content-Type": "application/json"}
        
        error = HTTPError("https://api.example.com/test", mock_response, "Not Found")
        
        assert error is not None
        assert isinstance(error, Exception)

    def test_http_error_attributes(self):
        """Test HTTPError stores all required attributes."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.headers = {"Content-Type": "application/json", "X-Request-Id": "123"}
        
        url = "https://api.example.com/test"
        body = "Internal Server Error"
        
        error = HTTPError(url, mock_response, body)
        
        assert error.status_code == 500
        assert error.url == url
        assert error.response_headers == {"Content-Type": "application/json", "X-Request-Id": "123"}
        assert "HTTP 500" in error.message
        assert "Internal Server Error" in error.message

    def test_http_error_str_representation(self):
        """Test HTTPError __str__ returns message."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {}
        
        error = HTTPError("https://api.example.com/test", mock_response, "Not Found")
        error_str = str(error)
        
        assert "HTTP 404" in error_str
        assert "Not Found" in error_str

    def test_http_error_is_exception(self):
        """Test HTTPError is a proper exception."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        error = HTTPError("https://api.example.com/test", mock_response, "Bad Request")
        
        # Should be raisable
        with pytest.raises(HTTPError):
            raise error

    def test_http_error_with_different_status_codes(self):
        """Test HTTPError with various status codes."""
        test_cases = [
            (400, "Bad Request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not Found"),
            (500, "Internal Server Error"),
            (503, "Service Unavailable"),
        ]
        
        for status_code, body in test_cases:
            mock_response = Mock()
            mock_response.status_code = status_code
            mock_response.headers = {}
            
            error = HTTPError("https://api.example.com/test", mock_response, body)
            assert error.status_code == status_code
            assert f"HTTP {status_code}" in error.message


class TestZscalerAPIError:
    """Test ZscalerAPIError class."""

    def test_zscaler_api_error_initialization(self):
        """Test ZscalerAPIError can be instantiated."""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.headers = {}
        
        response_body = {
            "code": "DUPLICATE_ITEM",
            "message": "Item already exists"
        }
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error is not None
        assert isinstance(error, Exception)

    def test_zscaler_api_error_with_code_and_message(self):
        """Test ZscalerAPIError extracts code and message."""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.headers = {}
        
        response_body = {
            "code": "DUPLICATE_ITEM",
            "message": "Invalid IP inetAddress : - This IP is already associated with current organization."
        }
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error.error_code == "DUPLICATE_ITEM"
        assert error.error_message == "Invalid IP inetAddress : - This IP is already associated with current organization."
        assert error.status_code == 409

    def test_zscaler_api_error_with_id_instead_of_code(self):
        """Test ZscalerAPIError handles 'id' field as error code."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        response_body = {
            "id": "ERROR_ID_123",
            "reason": "Bad request reason"
        }
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error.error_code == "ERROR_ID_123"
        assert error.error_message == "Bad request reason"

    def test_zscaler_api_error_str_representation(self):
        """Test ZscalerAPIError __str__ returns JSON."""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.headers = {}
        
        response_body = {
            "code": "DUPLICATE_ITEM",
            "message": "Item already exists"
        }
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        error_str = str(error)
        
        # Should be valid JSON
        parsed = json.loads(error_str)
        assert parsed["status"] == 409
        assert parsed["code"] == "DUPLICATE_ITEM"
        assert parsed["message"] == "Item already exists"
        assert parsed["url"] == "https://api.example.com/test"

    def test_zscaler_api_error_repr(self):
        """Test ZscalerAPIError __repr__ returns same as __str__."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {}
        
        response_body = {"code": "NOT_FOUND", "message": "Resource not found"}
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert repr(error) == str(error)

    def test_zscaler_api_error_with_params(self):
        """Test ZscalerAPIError handles params field."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        response_body = {
            "code": "INVALID_INPUT",
            "message": "Validation failed",
            "params": ["field1", "field2"]
        }
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error.params == ["field1", "field2"]
        assert "Parameters" in error.message
        assert "field1" in error.message

    def test_zscaler_api_error_with_path(self):
        """Test ZscalerAPIError handles path field."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        response_body = {
            "code": "INVALID_PATH",
            "message": "Invalid request path",
            "path": "/api/v1/users"
        }
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error.path == "/api/v1/users"
        error_str = str(error)
        parsed = json.loads(error_str)
        assert parsed["path"] == "/api/v1/users"

    def test_zscaler_api_error_with_service_type(self):
        """Test ZscalerAPIError handles service_type parameter."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        response_body = {"code": "ERROR", "message": "Test error"}
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body, service_type="ZPA")
        
        assert error.service_type == "zpa"

    def test_zscaler_api_error_with_non_dict_response_body(self):
        """Test ZscalerAPIError handles non-dict response body."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.headers = {}
        
        # Non-dict response body (plain string)
        response_body = "Internal Server Error"
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error.error_message == "Internal Server Error"
        assert "HTTP 500" in error.message

    def test_zscaler_api_error_with_nested_params(self):
        """Test ZscalerAPIError handles nested params (lists within lists)."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        response_body = {
            "code": "VALIDATION_ERROR",
            "message": "Multiple validation errors",
            "params": [["field1", "error1"], ["field2", "error2"], "simple_param"]
        }
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert "Parameters" in error.message
        # Should handle nested lists gracefully


class TestResponseChecker:
    """Test response_checker.check_response_for_error function."""

    def test_check_response_success_json(self):
        """Test check_response_for_error with successful JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        
        response_body = '{"id": 123, "name": "test"}'
        
        result, error = check_response_for_error("https://api.example.com/test", mock_response, response_body)
        
        assert error is None
        assert result == {"id": 123, "name": "test"}

    def test_check_response_success_plain_text(self):
        """Test check_response_for_error with successful plain text response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain"}
        
        response_body = "SUCCESS"
        
        result, error = check_response_for_error("https://api.example.com/test", mock_response, response_body)
        
        assert error is None
        assert result == "SUCCESS"

    def test_check_response_error_json(self):
        """Test check_response_for_error with JSON error response."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {"Content-Type": "application/json"}
        
        response_body = '{"code": "NOT_FOUND", "message": "Resource not found"}'
        
        result, error = check_response_for_error("https://api.example.com/test", mock_response, response_body)
        
        assert result is None
        assert error is not None
        assert isinstance(error, ZscalerAPIError)

    def test_check_response_malformed_json(self):
        """Test check_response_for_error with malformed JSON."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        
        response_body = "{ invalid json"
        
        result, error = check_response_for_error("https://api.example.com/test", mock_response, response_body)
        
        # Should handle malformed JSON gracefully
        assert error is not None

    def test_check_response_non_response_object(self):
        """Test check_response_for_error with non-response object."""
        # Pass something that doesn't have 'headers' attribute
        non_response = {"data": "test"}
        
        result, error = check_response_for_error("https://api.example.com/test", non_response, "body")
        
        # Should skip check and return as-is
        assert result == non_response
        assert error is None

    def test_check_response_no_content_type_header(self):
        """Test check_response_for_error when Content-Type header is missing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}  # No Content-Type
        
        response_body = '{"id": 123}'
        
        result, error = check_response_for_error("https://api.example.com/test", mock_response, response_body)
        
        # Should handle missing Content-Type
        assert result is not None or error is not None

    def test_check_response_various_status_codes(self):
        """Test check_response_for_error with various HTTP status codes."""
        test_cases = [
            (200, True),   # OK
            (201, True),   # Created
            (204, True),   # No Content
            (400, False),  # Bad Request
            (401, False),  # Unauthorized
            (403, False),  # Forbidden
            (404, False),  # Not Found
            (409, False),  # Conflict
            (429, False),  # Too Many Requests
            (500, False),  # Internal Server Error
            (503, False),  # Service Unavailable
        ]
        
        for status_code, should_succeed in test_cases:
            mock_response = Mock()
            mock_response.status_code = status_code
            mock_response.headers = {"Content-Type": "application/json"}
            
            if should_succeed:
                response_body = '{"success": true}'
            else:
                response_body = '{"code": "ERROR", "message": "Error occurred"}'
            
            result, error = check_response_for_error("https://api.example.com/test", mock_response, response_body)
            
            if should_succeed:
                assert error is None, f"Status {status_code} should not have error"
                assert result is not None
            else:
                assert error is not None, f"Status {status_code} should have error"


class TestErrorEdgeCases:
    """Test edge cases for error handling."""

    def test_http_error_with_empty_body(self):
        """Test HTTPError with empty response body."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.headers = {}
        
        error = HTTPError("https://api.example.com/test", mock_response, "")
        
        assert error.status_code == 500
        assert "HTTP 500" in error.message

    def test_zscaler_api_error_missing_optional_fields(self):
        """Test ZscalerAPIError when optional fields are missing."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        # Minimal response body
        response_body = {}
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error.status_code == 400
        assert error.error_code is None
        assert error.error_message is None
        assert error.params == []
        assert error.path is None

    def test_zscaler_api_error_with_only_code(self):
        """Test ZscalerAPIError with only error code."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        response_body = {"code": "ERROR_CODE"}
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error.error_code == "ERROR_CODE"
        assert "ERROR_CODE" in error.message

    def test_zscaler_api_error_with_only_message(self):
        """Test ZscalerAPIError with only error message."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        response_body = {"message": "Something went wrong"}
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        assert error.error_message == "Something went wrong"
        assert "Something went wrong" in error.message


class TestErrorIntegration:
    """Test error classes in realistic scenarios."""

    def test_error_can_be_raised_and_caught(self):
        """Test errors can be raised and caught properly."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {}
        
        error = HTTPError("https://api.example.com/test", mock_response, "Not Found")
        
        with pytest.raises(HTTPError) as exc_info:
            raise error
        
        assert "HTTP 404" in str(exc_info.value)

    def test_zscaler_api_error_serialization(self):
        """Test ZscalerAPIError can be serialized to JSON."""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.headers = {"X-Request-Id": "abc123"}
        
        response_body = {
            "code": "DUPLICATE_ITEM",
            "message": "Duplicate entry",
            "path": "/api/v1/resource"
        }
        
        error = ZscalerAPIError("https://api.example.com/test", mock_response, response_body)
        
        # Convert to JSON and back
        error_json = str(error)
        parsed = json.loads(error_json)
        
        assert parsed["status"] == 409
        assert parsed["code"] == "DUPLICATE_ITEM"
        assert parsed["message"] == "Duplicate entry"
        assert parsed["path"] == "/api/v1/resource"
        assert parsed["url"] == "https://api.example.com/test"

    def test_error_types_hierarchy(self):
        """Test that all error types inherit from Exception."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {}
        
        http_error = HTTPError("https://api.example.com/test", mock_response, "Error")
        api_error = ZscalerAPIError("https://api.example.com/test", mock_response, {"code": "ERROR"})
        
        assert isinstance(http_error, Exception)
        assert isinstance(api_error, Exception)

