"""
Unit tests for ZIA Traffic Static IP check_static_ip method.

Tests the validation behavior for checking if an IP address is available.
"""

import pytest
from unittest.mock import Mock, MagicMock
from zscaler.zia.traffic_static_ip import TrafficStaticIPAPI


class TestCheckStaticIP:
    """Test check_static_ip method."""

    def test_check_static_ip_valid_ip_available(self):
        """Test check_static_ip when IP is valid and available (HTTP 200 SUCCESS)."""
        # Setup
        mock_executor = Mock()
        api = TrafficStaticIPAPI(mock_executor)
        
        # Mock the raw response for HTTP 200 with "SUCCESS" text
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "SUCCESS"
        
        # Mock execute to return raw response with no error
        # Even though the response is non-JSON, we get the raw response
        mock_executor.execute.return_value = (mock_response, None)
        mock_executor.create_request.return_value = ({}, None)
        
        # Test
        is_valid, response, error = api.check_static_ip("203.0.113.11")
        
        # Assertions
        assert is_valid is True
        assert response is None
        assert error is None

    def test_check_static_ip_duplicate_ip(self):
        """Test check_static_ip when IP already exists (HTTP 409 DUPLICATE_ITEM)."""
        # Setup
        mock_executor = Mock()
        api = TrafficStaticIPAPI(mock_executor)
        
        # Mock the raw response for HTTP 409
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.text = '{"code":"DUPLICATE_ITEM","message":"Invalid IP inetAddress : - This IP 104.238.235.235 is already associated with current organization."}'
        
        # Mock error object that would be created
        mock_error = {
            "status": 409,
            "code": "DUPLICATE_ITEM",
            "message": "Invalid IP inetAddress : - This IP 104.238.235.235 is already associated with current organization."
        }
        
        # Mock execute to return raw response with error
        mock_executor.execute.return_value = (mock_response, mock_error)
        mock_executor.create_request.return_value = ({}, None)
        
        # Test
        is_valid, response, error = api.check_static_ip("104.238.235.235")
        
        # Assertions
        assert is_valid is False
        assert response == mock_response
        assert error == mock_error

    def test_check_static_ip_network_error(self):
        """Test check_static_ip when there's a network error."""
        # Setup
        mock_executor = Mock()
        api = TrafficStaticIPAPI(mock_executor)
        
        # Mock network error - no response
        mock_error = "Network timeout"
        mock_executor.execute.return_value = (None, mock_error)
        mock_executor.create_request.return_value = ({}, None)
        
        # Test
        is_valid, response, error = api.check_static_ip("203.0.113.11")
        
        # Assertions
        assert is_valid is False
        assert response is None
        assert error == mock_error

    def test_check_static_ip_create_request_error(self):
        """Test check_static_ip when request creation fails."""
        # Setup
        mock_executor = Mock()
        api = TrafficStaticIPAPI(mock_executor)
        
        # Mock request creation error
        mock_error = "Invalid endpoint"
        mock_executor.create_request.return_value = (None, mock_error)
        
        # Test
        is_valid, response, error = api.check_static_ip("203.0.113.11")
        
        # Assertions
        assert is_valid is False
        assert response is None
        assert error == mock_error

    def test_check_static_ip_unexpected_status_code(self):
        """Test check_static_ip with unexpected status code."""
        # Setup
        mock_executor = Mock()
        api = TrafficStaticIPAPI(mock_executor)
        
        # Mock unexpected response (e.g., 500 server error)
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        mock_error = "Server error"
        mock_executor.execute.return_value = (mock_response, mock_error)
        mock_executor.create_request.return_value = ({}, None)
        
        # Test
        is_valid, response, error = api.check_static_ip("203.0.113.11")
        
        # Assertions
        assert is_valid is False
        assert response == mock_response
        assert error == mock_error

    def test_check_static_ip_malformed_success_response(self):
        """Test check_static_ip when HTTP 200 but body is not 'SUCCESS'."""
        # Setup
        mock_executor = Mock()
        api = TrafficStaticIPAPI(mock_executor)
        
        # Mock response with HTTP 200 but unexpected body
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "UNEXPECTED_BODY"
        
        mock_executor.execute.return_value = (mock_response, None)
        mock_executor.create_request.return_value = ({}, None)
        
        # Test
        is_valid, response, error = api.check_static_ip("203.0.113.11")
        
        # Assertions
        assert is_valid is False
        assert response == mock_response
        assert "Unexpected response" in str(error)

    def test_check_static_ip_case_insensitive_success(self):
        """Test check_static_ip handles case variations of SUCCESS."""
        # Setup
        mock_executor = Mock()
        api = TrafficStaticIPAPI(mock_executor)
        
        for success_text in ["SUCCESS", "success", "Success"]:
            # Mock the raw response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = success_text
            
            mock_executor.execute.return_value = (mock_response, None)
            mock_executor.create_request.return_value = ({}, None)
            
            # Test
            is_valid, response, error = api.check_static_ip("203.0.113.11")
            
            # Assertions
            assert is_valid is True, f"Failed for '{success_text}'"
            assert response is None
            assert error is None

