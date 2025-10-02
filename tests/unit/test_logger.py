"""
Unit tests for Zscaler SDK logger functionality.

Tests logger setup, configuration, and log level handling.
"""

import logging
import os
import pytest
from zscaler.logger import (
    setup_logging, 
    LOG_FORMAT, 
    _sanitize_for_logging, 
    _sanitize_plaintext_for_logging,
    SENSITIVE_FIELDS, 
    SENSITIVE_HEADERS
)


class TestLoggerSetup:
    """Test logger setup functionality."""

    def teardown_method(self):
        """Clean up logger after each test."""
        # Remove all handlers from the logger
        logger = logging.getLogger("zscaler-sdk-python")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Reset environment variables
        if "ZSCALER_SDK_LOG" in os.environ:
            del os.environ["ZSCALER_SDK_LOG"]
        if "ZSCALER_SDK_VERBOSE" in os.environ:
            del os.environ["ZSCALER_SDK_VERBOSE"]
        if "LOG_TO_FILE" in os.environ:
            del os.environ["LOG_TO_FILE"]

    @pytest.mark.parametrize(
        "log_level,verbose",
        [
            (logging.INFO, False),
            (logging.DEBUG, True),
            (logging.WARNING, False),
            (logging.ERROR, False),
        ],
    )
    def test_logger_level_set_correctly_with_verbose_param(self, log_level, verbose):
        """Test logger is set to correct level based on verbose parameter."""
        setup_logging(logger_name="zscaler-sdk-python", enabled=True, verbose=verbose)
        
        logger = logging.getLogger("zscaler-sdk-python")
        if verbose:
            assert logger.level == logging.DEBUG
        else:
            assert logger.level == logging.INFO

    def test_logger_disabled_by_default(self):
        """Test logger is disabled when enabled=False."""
        setup_logging(logger_name="zscaler-sdk-python", enabled=False)
        
        logger = logging.getLogger("zscaler-sdk-python")
        # When disabled, should have NullHandler
        assert any(isinstance(h, logging.NullHandler) for h in logger.handlers)

    def test_logger_enabled_with_environment_variable(self):
        """Test logger can be enabled via environment variable."""
        os.environ["ZSCALER_SDK_LOG"] = "true"
        setup_logging(logger_name="zscaler-sdk-python")
        
        logger = logging.getLogger("zscaler-sdk-python")
        assert logger.level in [logging.INFO, logging.DEBUG]

    def test_logger_verbose_with_environment_variable(self):
        """Test logger verbose mode via environment variable."""
        os.environ["ZSCALER_SDK_LOG"] = "true"
        os.environ["ZSCALER_SDK_VERBOSE"] = "true"
        setup_logging(logger_name="zscaler-sdk-python")
        
        logger = logging.getLogger("zscaler-sdk-python")
        assert logger.level == logging.DEBUG

    def test_logger_info_level_when_not_verbose(self):
        """Test logger uses INFO level when verbose is False."""
        os.environ["ZSCALER_SDK_LOG"] = "true"
        os.environ["ZSCALER_SDK_VERBOSE"] = "false"
        setup_logging(logger_name="zscaler-sdk-python")
        
        logger = logging.getLogger("zscaler-sdk-python")
        assert logger.level == logging.INFO

    def test_logger_has_stream_handler_when_enabled(self):
        """Test logger has StreamHandler when enabled."""
        setup_logging(logger_name="zscaler-sdk-python", enabled=True)
        
        logger = logging.getLogger("zscaler-sdk-python")
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

    def test_logger_handler_has_correct_formatter(self):
        """Test logger handler uses correct format."""
        setup_logging(logger_name="zscaler-sdk-python", enabled=True)
        
        logger = logging.getLogger("zscaler-sdk-python")
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        
        assert len(stream_handlers) > 0
        handler = stream_handlers[0]
        if handler.formatter:
            assert LOG_FORMAT in handler.formatter._fmt

    def test_logger_custom_name(self):
        """Test logger can be created with custom name."""
        custom_name = "custom-zscaler-logger"
        setup_logging(logger_name=custom_name, enabled=True)
        
        logger = logging.getLogger(custom_name)
        assert logger is not None
        assert logger.level in [logging.INFO, logging.DEBUG]

    def test_logger_handlers_removed_on_reconfiguration(self):
        """Test existing handlers are removed when reconfiguring logger."""
        # Setup logger first time
        setup_logging(logger_name="zscaler-sdk-python", enabled=True, verbose=False)
        logger = logging.getLogger("zscaler-sdk-python")
        initial_handler_count = len(logger.handlers)
        
        # Setup logger second time
        setup_logging(logger_name="zscaler-sdk-python", enabled=True, verbose=True)
        final_handler_count = len(logger.handlers)
        
        # Should not have duplicate handlers
        assert final_handler_count <= initial_handler_count + 1

    def test_logger_with_file_handler_environment_variable(self):
        """Test logger can add FileHandler via environment variable."""
        os.environ["ZSCALER_SDK_LOG"] = "true"
        os.environ["LOG_TO_FILE"] = "true"
        os.environ["LOG_FILE_PATH"] = "/tmp/test_zscaler_sdk.log"
        
        setup_logging(logger_name="zscaler-sdk-python")
        
        logger = logging.getLogger("zscaler-sdk-python")
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        
        # Clean up
        for handler in file_handlers:
            handler.close()
            logger.removeHandler(handler)
        
        # FileHandler should be present
        assert len(file_handlers) > 0


class TestLoggerEdgeCases:
    """Test edge cases for logger functionality."""

    def teardown_method(self):
        """Clean up logger after each test."""
        logger = logging.getLogger("zscaler-sdk-python")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        if "ZSCALER_SDK_LOG" in os.environ:
            del os.environ["ZSCALER_SDK_LOG"]
        if "ZSCALER_SDK_VERBOSE" in os.environ:
            del os.environ["ZSCALER_SDK_VERBOSE"]

    def test_logger_with_none_parameters(self):
        """Test logger handles None parameters gracefully."""
        setup_logging(logger_name="zscaler-sdk-python", enabled=None, verbose=None)
        logger = logging.getLogger("zscaler-sdk-python")
        assert logger is not None

    def test_logger_environment_variable_case_insensitive(self):
        """Test environment variables are case insensitive."""
        os.environ["ZSCALER_SDK_LOG"] = "TRUE"
        setup_logging(logger_name="zscaler-sdk-python")
        logger = logging.getLogger("zscaler-sdk-python")
        assert logger.level in [logging.INFO, logging.DEBUG]

    def test_logger_with_invalid_environment_variable(self):
        """Test logger handles invalid environment variable values."""
        os.environ["ZSCALER_SDK_LOG"] = "invalid_value"
        setup_logging(logger_name="zscaler-sdk-python")
        
        # Should default to disabled
        logger = logging.getLogger("zscaler-sdk-python")
        assert any(isinstance(h, logging.NullHandler) for h in logger.handlers)

    def test_logger_format_constant(self):
        """Test LOG_FORMAT constant is properly defined."""
        assert LOG_FORMAT is not None
        assert isinstance(LOG_FORMAT, str)
        assert "%(asctime)s" in LOG_FORMAT
        assert "%(name)s" in LOG_FORMAT
        assert "%(levelname)s" in LOG_FORMAT
        assert "%(message)s" in LOG_FORMAT


class TestLoggerIntegration:
    """Test logger integration scenarios."""

    def teardown_method(self):
        """Clean up logger after each test."""
        logger = logging.getLogger("zscaler-sdk-python")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    def test_logger_multiple_setup_calls(self):
        """Test logger can be setup multiple times without issues."""
        setup_logging(logger_name="zscaler-sdk-python", enabled=True, verbose=False)
        setup_logging(logger_name="zscaler-sdk-python", enabled=True, verbose=True)
        setup_logging(logger_name="zscaler-sdk-python", enabled=True, verbose=False)
        
        logger = logging.getLogger("zscaler-sdk-python")
        assert logger.level == logging.INFO

    def test_logger_can_log_messages(self):
        """Test logger can actually log messages."""
        setup_logging(logger_name="zscaler-sdk-python", enabled=True, verbose=True)
        logger = logging.getLogger("zscaler-sdk-python")
        
        # This should not raise any exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        assert True  # If we get here, logging worked

    def test_logger_disabled_does_not_log(self):
        """Test disabled logger does not produce output."""
        setup_logging(logger_name="zscaler-sdk-python", enabled=False)
        logger = logging.getLogger("zscaler-sdk-python")
        
        # With NullHandler, this should not produce output
        logger.info("This should not appear")
        
        # Verify NullHandler is present
        assert any(isinstance(h, logging.NullHandler) for h in logger.handlers)


class TestSensitiveDataSanitization:
    """Test sensitive data sanitization for logging."""

    def test_sanitize_dict_with_password(self):
        """Test _sanitize_for_logging masks password in dict."""
        data = {"username": "admin", "password": "secret123"}
        sanitized = _sanitize_for_logging(data)
        
        assert sanitized["username"] == "admin"
        assert sanitized["password"] == "***REDACTED***"

    def test_sanitize_dict_with_api_key(self):
        """Test _sanitize_for_logging masks API keys."""
        data = {"api_key": "key123", "apiKey": "key456", "name": "test"}
        sanitized = _sanitize_for_logging(data)
        
        assert sanitized["api_key"] == "***REDACTED***"
        assert sanitized["apiKey"] == "***REDACTED***"
        assert sanitized["name"] == "test"

    def test_sanitize_dict_with_client_secret(self):
        """Test _sanitize_for_logging masks client secrets."""
        data = {"clientId": "id123", "clientSecret": "secret456", "client_secret": "secret789"}
        sanitized = _sanitize_for_logging(data)
        
        assert sanitized["clientId"] == "id123"
        assert sanitized["clientSecret"] == "***REDACTED***"
        assert sanitized["client_secret"] == "***REDACTED***"

    def test_sanitize_nested_dict(self):
        """Test _sanitize_for_logging handles nested dicts."""
        data = {
            "user": {
                "name": "admin",
                "password": "secret123"
            },
            "config": {
                "api_key": "key456"
            }
        }
        sanitized = _sanitize_for_logging(data)
        
        assert sanitized["user"]["name"] == "admin"
        assert sanitized["user"]["password"] == "***REDACTED***"
        assert sanitized["config"]["api_key"] == "***REDACTED***"

    def test_sanitize_list_of_dicts(self):
        """Test _sanitize_for_logging handles lists of dicts."""
        data = [
            {"name": "user1", "password": "pass1"},
            {"name": "user2", "token": "token2"}
        ]
        sanitized = _sanitize_for_logging(data)
        
        assert sanitized[0]["name"] == "user1"
        assert sanitized[0]["password"] == "***REDACTED***"
        assert sanitized[1]["name"] == "user2"
        assert sanitized[1]["token"] == "***REDACTED***"

    def test_sanitize_case_insensitive(self):
        """Test _sanitize_for_logging is case-insensitive."""
        data = {
            "Password": "secret1",
            "PASSWORD": "secret2",
            "ApiKey": "key1",
            "APIKEY": "key2"
        }
        sanitized = _sanitize_for_logging(data)
        
        # All variations should be redacted
        assert sanitized["Password"] == "***REDACTED***"
        assert sanitized["PASSWORD"] == "***REDACTED***"
        assert sanitized["ApiKey"] == "***REDACTED***"
        assert sanitized["APIKEY"] == "***REDACTED***"

    def test_sanitize_non_sensitive_fields(self):
        """Test _sanitize_for_logging preserves non-sensitive fields."""
        data = {
            "id": "123",
            "name": "TestUser",
            "email": "test@example.com",
            "created_at": "2025-10-01",
            "enabled": True,
            "count": 42
        }
        sanitized = _sanitize_for_logging(data)
        
        # All non-sensitive fields should be preserved
        assert sanitized == data

    def test_sanitize_empty_dict(self):
        """Test _sanitize_for_logging handles empty dict."""
        data = {}
        sanitized = _sanitize_for_logging(data)
        assert sanitized == {}

    def test_sanitize_none_values(self):
        """Test _sanitize_for_logging handles None values."""
        data = {"password": None, "name": "test"}
        sanitized = _sanitize_for_logging(data)
        
        # None password should still be redacted
        assert sanitized["password"] == "***REDACTED***"
        assert sanitized["name"] == "test"

    def test_sanitize_non_dict_non_list(self):
        """Test _sanitize_for_logging handles primitives."""
        assert _sanitize_for_logging("string") == "string"
        assert _sanitize_for_logging(123) == 123
        assert _sanitize_for_logging(True) is True
        assert _sanitize_for_logging(None) is None

    def test_sensitive_fields_constant(self):
        """Test SENSITIVE_FIELDS constant is properly defined."""
        assert isinstance(SENSITIVE_FIELDS, set)
        assert "password" in SENSITIVE_FIELDS
        assert "api_key" in SENSITIVE_FIELDS
        assert "clientSecret" in SENSITIVE_FIELDS
        assert "access_token" in SENSITIVE_FIELDS

    def test_sensitive_headers_constant(self):
        """Test SENSITIVE_HEADERS constant is properly defined."""
        assert isinstance(SENSITIVE_HEADERS, set)
        assert "authorization" in SENSITIVE_HEADERS
        assert "x-api-key" in SENSITIVE_HEADERS
        assert "client-secret" in SENSITIVE_HEADERS


class TestPlaintextSanitization:
    """Test plaintext sanitization for logging."""

    def test_sanitize_plaintext_with_password(self):
        """Test _sanitize_plaintext_for_logging masks passwords in text."""
        text = '{"username":"admin","password":"secret123"}'
        sanitized = _sanitize_plaintext_for_logging(text)
        
        assert "admin" in sanitized
        assert "secret123" not in sanitized
        assert "***REDACTED***" in sanitized

    def test_sanitize_plaintext_with_api_key(self):
        """Test _sanitize_plaintext_for_logging masks API keys."""
        text = '{"api_key":"key123","name":"test"}'
        sanitized = _sanitize_plaintext_for_logging(text)
        
        assert "key123" not in sanitized
        assert "***REDACTED***" in sanitized
        assert "test" in sanitized

    def test_sanitize_plaintext_with_client_secret(self):
        """Test _sanitize_plaintext_for_logging masks client secrets."""
        text = '{"clientId":"id123","clientSecret":"secret456"}'
        sanitized = _sanitize_plaintext_for_logging(text)
        
        assert "id123" in sanitized
        assert "secret456" not in sanitized
        assert "***REDACTED***" in sanitized

    def test_sanitize_plaintext_with_access_token(self):
        """Test _sanitize_plaintext_for_logging masks access tokens."""
        text = '{"access_token":"token123"}'
        sanitized = _sanitize_plaintext_for_logging(text)
        
        assert "token123" not in sanitized
        assert "***REDACTED***" in sanitized

    def test_sanitize_plaintext_case_insensitive(self):
        """Test _sanitize_plaintext_for_logging is case-insensitive."""
        text = '{"Password":"pass1","PASSWORD":"pass2","ApiKey":"key1"}'
        sanitized = _sanitize_plaintext_for_logging(text)
        
        assert "pass1" not in sanitized
        assert "pass2" not in sanitized
        assert "key1" not in sanitized
        assert sanitized.count("***REDACTED***") >= 3

    def test_sanitize_plaintext_preserves_non_sensitive(self):
        """Test _sanitize_plaintext_for_logging preserves non-sensitive data."""
        text = '{"id":"123","name":"TestUser","email":"test@example.com"}'
        sanitized = _sanitize_plaintext_for_logging(text)
        
        # Non-sensitive fields should be preserved
        assert "123" in sanitized
        assert "TestUser" in sanitized
        assert "test@example.com" in sanitized

    def test_sanitize_plaintext_with_non_string(self):
        """Test _sanitize_plaintext_for_logging handles non-strings."""
        assert _sanitize_plaintext_for_logging(123) == 123
        assert _sanitize_plaintext_for_logging(None) is None
        assert _sanitize_plaintext_for_logging(True) is True

    def test_sanitize_plaintext_success_message(self):
        """Test _sanitize_plaintext_for_logging preserves simple success messages."""
        text = "SUCCESS"
        sanitized = _sanitize_plaintext_for_logging(text)
        assert sanitized == "SUCCESS"

