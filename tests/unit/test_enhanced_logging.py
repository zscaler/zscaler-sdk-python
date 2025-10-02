# """
# Tests for Enhanced Logging System using ZscalerLogger
# """

# import pytest
# import json
# import time
# import logging
# import os
# from unittest.mock import Mock, patch, MagicMock
# from zscaler.logger import ZscalerLogger, setup_logging, dump_request, dump_response


# class TestZscalerLogger:
#     """Test ZscalerLogger class."""
    
#     def test_zscaler_logger_defaults(self):
#         """Test ZscalerLogger with default values."""
#         logger = ZscalerLogger()
        
#         assert logger.logger_name == "zscaler-sdk-python"
#         assert logger.enabled is True
#         assert logger.verbose is False
#         assert logger.logging_format == "basic"
#         assert logger.custom_formatter is None
#         assert logger.session_uuid is not None
#         assert logger.logger is not None
    
#     def test_zscaler_logger_custom_config(self):
#         """Test ZscalerLogger with custom configuration."""
#         def custom_formatter(log_type, data):
#             return f"Custom {log_type}: {data['url']}"
        
#         logger = ZscalerLogger(
#             logger_name="test-logger",
#             enabled=True,
#             verbose=True,
#             logging_format="custom",
#             custom_formatter=custom_formatter
#         )
        
#         assert logger.logger_name == "test-logger"
#         assert logger.enabled is True
#         assert logger.verbose is True
#         assert logger.logging_format == "custom"
#         assert logger.custom_formatter is custom_formatter
#         assert logger.logger is not None
    
#     def test_zscaler_logger_disabled(self):
#         """Test ZscalerLogger when logging is disabled."""
#         logger = ZscalerLogger(enabled=False)
        
#         assert logger.enabled is False
#         assert logger.logger is not None
#         # When disabled, it should have a NullHandler, but there might be other handlers from previous tests
#         null_handlers = [h for h in logger.logger.handlers if isinstance(h, logging.NullHandler)]
#         assert len(null_handlers) >= 1
    
#     def test_generate_request_uuid(self):
#         """Test request UUID generation."""
#         logger = ZscalerLogger()
#         uuid1 = logger.generate_request_uuid()
#         uuid2 = logger.generate_request_uuid()
        
#         assert uuid1 != uuid2
#         assert len(uuid1) == 36  # UUID4 format
#         assert len(uuid2) == 36
    
#     def test_generate_session_uuid(self):
#         """Test session UUID generation."""
#         logger = ZscalerLogger()
#         uuid1 = logger.generate_session_uuid()
#         uuid2 = logger.generate_session_uuid()
        
#         assert uuid1 != uuid2
#         assert len(uuid1) == 36  # UUID4 format
#         assert len(uuid2) == 36
    
#     def test_configure_component(self):
#         """Test component configuration."""
#         logger = ZscalerLogger()
#         component = Mock()
        
#         logger.configure_component(component)
        
#         assert component.logger == logger.logger
#         assert component.logging_enabled == logger.enabled
#         assert component.logging_format == logger.logging_format
#         assert component.sdk_logger == logger
    
#     def test_from_config(self):
#         """Test creating logger from config object."""
#         config = Mock()
#         config.logging = Mock()
#         config.logging.enabled = True
#         config.logging.verbose = True
#         config.logging.logging_format = "json"
#         config.logging.custom_formatter = None
        
#         logger = ZscalerLogger.from_config(config)
        
#         assert logger is not None
#         assert logger.enabled is True
#         assert logger.verbose is True
#         assert logger.logging_format == "json"
    
#     def test_from_config_disabled(self):
#         """Test creating logger from config when logging is disabled."""
#         config = Mock()
#         config.logging = Mock()
#         config.logging.enabled = False
        
#         logger = ZscalerLogger.from_config(config)
        
#         assert logger is None
    
#     def test_setup_from_config(self):
#         """Test setup from config."""
#         config = Mock()
#         config.logging = Mock()
#         config.logging.enabled = True
#         config.logging.verbose = True
#         config.logging.logging_format = "basic"
#         config.logging.custom_formatter = None
        
#         sdk_logger, logger, enabled = ZscalerLogger.setup_from_config(config)
        
#         assert sdk_logger is not None
#         assert logger is not None
#         assert enabled is True
#         assert hasattr(config, '_sdk_logger')
#         assert config._sdk_logger == sdk_logger


# class TestZscalerLoggerLogging:
#     """Test ZscalerLogger logging functionality."""
    
#     def test_dump_request_basic(self):
#         """Test basic request logging."""
#         logger = ZscalerLogger(logging_format="basic")
        
#         with patch.object(logger.logger, 'info') as mock_info:
#             logger.dump_request(
#                 url="https://api.example.com/test",
#                 method="GET",
#                 json_data={"key": "value"},
#                 params={"page": 1},
#                 headers={"Authorization": "Bearer token", "X-Custom": "Value"},
#                 request_uuid="test-uuid-123",
#                 body=True
#             )
            
#             mock_info.assert_called_once()
#             call_args = mock_info.call_args[0][0]
#             assert "ZSCALER SDK REQUEST" in call_args
#             assert "GET https://api.example.com/test?page=1" in call_args
#             assert "X-Custom: Value" in call_args
#             assert "Authorization" not in call_args  # Should be filtered
    
#     def test_dump_request_structured(self):
#         """Test structured request logging."""
#         logger = ZscalerLogger(logging_format="json")
        
#         with patch.object(logger.logger, 'info') as mock_info:
#             logger.dump_request_structured(
#                 url="https://api.example.com/test",
#                 method="POST",
#                 json_data={"data": "payload"},
#                 params={"filter": "active"},
#                 headers={"Authorization": "Bearer token", "X-Client-ID": "123"},
#                 request_uuid="json-uuid-456",
#                 body=True
#             )
            
#             mock_info.assert_called_once()
#             call_args = mock_info.call_args[0][0]
#             assert call_args == "API request initiated"
            
#             # Check extra data
#             extra_data = mock_info.call_args[1]['extra']
#             assert extra_data['http_method'] == "POST"
#             assert extra_data['url'] == "https://api.example.com/test"
#             assert extra_data['headers']['X-Client-ID'] == "123"
#             assert extra_data['headers']['Authorization'] == "*** REDACTED ***"
    
#     def test_dump_response_basic(self):
#         """Test basic response logging."""
#         logger = ZscalerLogger(logging_format="basic")
#         mock_resp = Mock()
#         mock_resp.status_code = 200
#         mock_resp.headers = {"Content-Type": "application/json", "X-Response-Header": "RespValue"}
#         mock_resp.text = '{"status": "success"}'
        
#         with patch.object(logger.logger, 'info') as mock_info:
#             logger.dump_response(
#                 url="https://api.example.com/test",
#                 method="GET",
#                 response=mock_resp,
#                 params={"page": 1},
#                 request_uuid="test-uuid-123",
#                 start_time=time.time() - 0.1,
#                 from_cache=False
#             )
            
#             mock_info.assert_called_once()
#             call_args = mock_info.call_args[0][0]
#             assert "ZSCALER SDK RESPONSE" in call_args
#             assert "GET https://api.example.com/test?page=1" in call_args
#             assert "X-Response-Header: RespValue" in call_args
#             assert "DURATION:" in call_args
    
#     def test_dump_response_structured(self):
#         """Test structured response logging."""
#         logger = ZscalerLogger(logging_format="json")
#         mock_resp = Mock()
#         mock_resp.status_code = 200
#         mock_resp.headers = {"Content-Type": "application/json", "X-RateLimit": "100"}
#         mock_resp.text = '{"items": [1, 2, 3]}'
#         # Mock the request attribute to avoid the Mock.keys() error
#         mock_resp.request = Mock()
#         mock_resp.request.headers = {}
        
#         with patch.object(logger.logger, 'info') as mock_info:
#             logger.dump_response_structured(
#                 url="https://api.example.com/test",
#                 method="GET",
#                 response=mock_resp,
#                 params={"limit": 10},
#                 request_uuid="json-resp-789",
#                 start_time=time.time() - 0.5,
#                 from_cache=True
#             )
            
#             mock_info.assert_called_once()
#             call_args = mock_info.call_args[0][0]
#             assert call_args == "API response received"
            
#             # Check extra data
#             extra_data = mock_info.call_args[1]['extra']
#             assert extra_data['http_method'] == "GET"
#             assert extra_data['url'] == "https://api.example.com/test"
#             assert extra_data['status_code'] == 200
#             assert extra_data['from_cache'] is True
#             assert extra_data['duration'] > 0
    
#     def test_log_request_unified(self):
#         """Test unified request logging method."""
#         logger = ZscalerLogger(logging_format="json")
        
#         with patch.object(logger, 'dump_request_structured') as mock_structured:
#             logger.log_request(
#                 url="https://api.example.com/test",
#                 method="GET",
#                 json_data={"key": "value"},
#                 params={"page": 1},
#                 headers={"Authorization": "Bearer token"},
#                 request_uuid="test-uuid-123",
#                 body=True
#             )
            
#             mock_structured.assert_called_once()
    
#     def test_log_response_unified(self):
#         """Test unified response logging method."""
#         logger = ZscalerLogger(logging_format="json")
#         mock_resp = Mock()
        
#         with patch.object(logger, 'dump_response_structured') as mock_structured:
#             logger.log_response(
#                 url="https://api.example.com/test",
#                 method="GET",
#                 response=mock_resp,
#                 params={"page": 1},
#                 request_uuid="test-uuid-123",
#                 start_time=time.time() - 0.1,
#                 from_cache=False
#             )
            
#             mock_structured.assert_called_once()
    
#     def test_redact_sensitive_data(self):
#         """Test sensitive data redaction."""
#         logger = ZscalerLogger()
        
#         # Test dict redaction
#         data = {
#             "access_token": "secret123",
#             "client_secret": "secret456",
#             "normal_field": "value",
#             "nested": {
#                 "password": "secret789",
#                 "normal": "value"
#             }
#         }
        
#         redacted = logger._redact_sensitive_data(data)
        
#         assert redacted["access_token"] == "*** REDACTED ***"
#         assert redacted["client_secret"] == "*** REDACTED ***"
#         assert redacted["normal_field"] == "value"
#         assert redacted["nested"]["password"] == "*** REDACTED ***"
#         assert redacted["nested"]["normal"] == "value"
        
#         # Test list redaction
#         list_data = [{"token": "secret"}, {"normal": "value"}]
#         redacted_list = logger._redact_sensitive_data(list_data)
        
#         assert redacted_list[0]["token"] == "*** REDACTED ***"
#         assert redacted_list[1]["normal"] == "value"
        
#         # Test string redaction
#         json_string = '{"access_token": "secret123", "normal": "value"}'
#         redacted_string = logger._redact_sensitive_data(json_string)
        
#         assert "*** REDACTED ***" in redacted_string
#         assert "secret123" not in redacted_string
#         assert "normal" in redacted_string


# class TestLegacyCompatibility:
#     """Test backward compatibility with legacy logging."""
    
#     def test_setup_logging_legacy(self):
#         """Test legacy setup_logging function."""
#         os.environ["ZSCALER_SDK_LOG"] = "true"
#         os.environ["ZSCALER_SDK_VERBOSE"] = "true"
        
#         logger = setup_logging("test-legacy", enabled=True, verbose=True)
        
#         assert logger.level == logging.DEBUG
#         assert len(logger.handlers) > 0
#         assert isinstance(logger.handlers[0], logging.StreamHandler)
#         assert isinstance(logger.handlers[0].formatter, logging.Formatter)
#         assert logger.handlers[0].formatter._fmt == "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"
    
#     def test_setup_logging_enhanced(self):
#         """Test enhanced setup_logging function."""
#         config = {"enabled": True, "logging_format": "json", "verbose": True}
#         logger = setup_logging("test-enhanced", logging_config=config)
        
#         assert logger.level == logging.DEBUG
#         assert len(logger.handlers) > 0
#         # The stream handler should use the simple message formatter for JSON
#         assert logger.handlers[0].formatter._fmt == "%(message)s"
    
#     def test_dump_request_legacy(self):
#         """Test legacy dump_request function."""
#         logger = logging.getLogger("test-legacy")
#         logger.handlers.clear()
#         logger.addHandler(logging.StreamHandler())
        
#         with patch.object(logger, 'info') as mock_info:
#             dump_request(
#                 logger,
#                 "https://api.example.com/legacy",
#                 "GET",
#                 {"data": "legacy"},
#                 {"param": 1},
#                 {"Auth": "Bearer"},
#                 "legacy-uuid",
#                 True
#             )
            
#             mock_info.assert_called_once()
#             call_args = mock_info.call_args[0][0]
#             assert "---[ ZSCALER SDK REQUEST | ID:legacy-uuid ]" in call_args
#             assert "GET https://api.example.com/legacy?param=1" in call_args
#             assert '{"data": "legacy"}' in call_args
    
#     def test_dump_response_legacy(self):
#         """Test legacy dump_response function."""
#         logger = logging.getLogger("test-legacy")
#         logger.handlers.clear()
#         logger.addHandler(logging.StreamHandler())
        
#         mock_resp = Mock()
#         mock_resp.status_code = 200
#         mock_resp.headers = {"Content-Type": "application/json"}
#         mock_resp.text = '{"status": "ok"}'
#         start_time = time.time() - 0.1
        
#         with patch.object(logger, 'info') as mock_info:
#             dump_response(
#                 logger,
#                 "https://api.example.com/legacy",
#                 "GET",
#                 mock_resp,
#                 {"param": 1},
#                 "legacy-resp-uuid",
#                 start_time,
#                 False
#             )
            
#             mock_info.assert_called_once()
#             call_args = mock_info.call_args[0][0]
#             assert "---[ ZSCALER SDK RESPONSE | ID:legacy-resp-uuid" in call_args
#             assert "GET https://api.example.com/legacy?param=1" in call_args
#             assert '{"status": "ok"}' in call_args


# class TestIntegration:
#     """Integration tests for enhanced logging."""
    
#     def test_end_to_end_basic_logging(self):
#         """Test end-to-end basic logging."""
#         logger = ZscalerLogger(
#             enabled=True,
#             verbose=True,
#             logging_format="basic"
#         )
        
#         # Test request logging
#         with patch.object(logger.logger, 'info') as mock_info:
#             logger.log_request(
#                 "https://api.example.com/test",
#                 "GET",
#                 {"key": "value"},
#                 {"page": 1},
#                 {"Authorization": "Bearer token"},
#                 "test-uuid",
#                 True
#             )
#             mock_info.assert_called_once()
#             call_args = mock_info.call_args[0][0]
#             assert "ZSCALER SDK REQUEST" in call_args
    
#     def test_end_to_end_json_logging(self):
#         """Test end-to-end JSON logging."""
#         logger = ZscalerLogger(
#             enabled=True,
#             verbose=False,
#             logging_format="json"
#         )
        
#         # Test request logging
#         with patch.object(logger.logger, 'info') as mock_info:
#             logger.log_request(
#                 "https://api.example.com/test",
#                 "GET",
#                 {"key": "value"},
#                 {"page": 1},
#                 {"Authorization": "Bearer token"},
#                 "test-uuid",
#                 True
#             )
#             mock_info.assert_called_once()
#             call_args = mock_info.call_args[0][0]
#             assert call_args == "API request initiated"
    
#     def test_end_to_end_custom_logging(self):
#         """Test end-to-end custom logging."""
#         def custom_formatter(log_type, data):
#             return f"Custom {log_type}: {data['url']}"
        
#         logger = ZscalerLogger(
#             enabled=True,
#             verbose=True,
#             logging_format="custom",
#             custom_formatter=custom_formatter
#         )
        
#         # Test request logging - custom formatter is used in dump_request_structured
#         with patch.object(logger, 'dump_request_structured') as mock_structured:
#             logger.log_request(
#                 "https://api.example.com/test",
#                 "GET",
#                 {"key": "value"},
#                 {"page": 1},
#                 {"Authorization": "Bearer token"},
#                 "test-uuid",
#                 True
#             )
#             mock_structured.assert_called_once()
            
#             # Test the custom formatter directly
#             result = custom_formatter("request", {"url": "https://api.example.com/test"})
#             assert result == "Custom request: https://api.example.com/test"
