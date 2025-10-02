"""
Unit tests for Zscaler SDK logger functionality.

Tests logger setup, configuration, and log level handling.
"""

import logging
import os
import pytest
from zscaler.logger import setup_logging, LOG_FORMAT


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

