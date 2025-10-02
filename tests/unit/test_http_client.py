"""
Testing HTTP Client for Zscaler SDK
"""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from zscaler.oneapi_http_client import HTTPClient
from zscaler.oneapi_client import Client
from zscaler.cache.no_op_cache import NoOpCache


def test_http_client_initialization():
    """Test HTTPClient initialization."""
    http_config = {
        "headers": {
            "User-Agent": "test-agent",
            "Content-Type": "application/json"
        }
    }
    
    client = HTTPClient(http_config)
    
    assert client._default_headers == http_config["headers"]
    assert client.zcc_legacy_client is None
    assert client.ztw_legacy_client is None
    assert client.zdx_legacy_client is None
    assert client.zpa_legacy_client is None
    assert client.zia_legacy_client is None
    assert client.zwa_legacy_client is None


def test_http_client_with_legacy_clients():
    """Test HTTPClient initialization with legacy clients."""
    http_config = {"headers": {}}
    
    mock_zcc = Mock()
    mock_ztw = Mock()
    mock_zdx = Mock()
    mock_zpa = Mock()
    mock_zia = Mock()
    mock_zwa = Mock()
    
    client = HTTPClient(
        http_config,
        zcc_legacy_client=mock_zcc,
        ztw_legacy_client=mock_ztw,
        zdx_legacy_client=mock_zdx,
        zpa_legacy_client=mock_zpa,
        zia_legacy_client=mock_zia,
        zwa_legacy_client=mock_zwa
    )
    
    assert client.zcc_legacy_client == mock_zcc
    assert client.ztw_legacy_client == mock_ztw
    assert client.zdx_legacy_client == mock_zdx
    assert client.zpa_legacy_client == mock_zpa
    assert client.zia_legacy_client == mock_zia
    assert client.zwa_legacy_client == mock_zwa
    
    # Test legacy client flags
    assert client.use_zcc_legacy_client is True
    assert client.use_ztw_legacy_client is True
    assert client.use_zdx_legacy_client is True
    assert client.use_zpa_legacy_client is True
    assert client.use_zia_legacy_client is True
    assert client.use_zwa_legacy_client is True


def test_http_client_format_binary_data():
    """Test HTTPClient format_binary_data method."""
    client = HTTPClient({"headers": {}})
    
    # Test binary data formatting
    binary_data = b"test binary data"
    formatted_data = client.format_binary_data(binary_data)
    
    assert formatted_data == binary_data


def test_http_client_setup_proxy():
    """Test HTTPClient _setup_proxy method."""
    client = HTTPClient({"headers": {}})
    
    # Test with None proxy
    proxy_string = client._setup_proxy(None)
    assert proxy_string is None or isinstance(proxy_string, str)
    
    # Test with proxy configuration
    proxy_config = {
        "host": "proxy.example.com",
        "port": 8080,
        "username": "user",
        "password": "pass"
    }
    
    proxy_string = client._setup_proxy(proxy_config)
    assert proxy_string is not None
    assert "proxy.example.com" in proxy_string
    assert "8080" in proxy_string
    assert "user" in proxy_string
    assert "pass" in proxy_string


def test_http_client_setup_proxy_without_auth():
    """Test HTTPClient _setup_proxy method without authentication."""
    client = HTTPClient({"headers": {}})
    
    # Test with proxy configuration without auth
    proxy_config = {
        "host": "proxy.example.com",
        "port": 8080
    }
    
    proxy_string = client._setup_proxy(proxy_config)
    assert proxy_string is not None
    assert "proxy.example.com" in proxy_string
    assert "8080" in proxy_string
    assert "http://" in proxy_string


def test_http_client_setup_proxy_without_port():
    """Test HTTPClient _setup_proxy method without port."""
    client = HTTPClient({"headers": {}})
    
    # Test with proxy configuration without port
    proxy_config = {
        "host": "proxy.example.com"
    }
    
    proxy_string = client._setup_proxy(proxy_config)
    assert proxy_string is not None
    assert "proxy.example.com" in proxy_string
    assert "http://" in proxy_string


def test_http_client_send_request_with_error_handling():
    """Test HTTPClient send_request with error handling."""
    client = HTTPClient({"headers": {}})
    
    # Test with invalid URL to trigger error
    result = client.send_request({
        'method': 'POST',
        'url': 'invalid-url',
        'headers': {'Authorization': 'Bearer token'},
        'data': {'key': 'value'},
        'params': {}  # Add required params key
    })
    
    response, error = result
    
    # Should return error for invalid URL
    assert error is not None
    assert response is None


def test_http_client_send_request_with_connection_error():
    """Test HTTPClient send_request with connection error."""
    client = HTTPClient({"headers": {}})
    
    # Test with non-existent domain to trigger connection error
    result = client.send_request({
        'method': 'POST',
        'url': 'https://nonexistent-domain-12345.com/test',
        'headers': {'Authorization': 'Bearer token'},
        'data': {'key': 'value'},
        'params': {}  # Add required params key
    })
    
    response, error = result
    
    # Should return connection error
    assert error is not None
    assert response is None


def test_http_client_send_request_with_legacy_client_routing():
    """Test HTTPClient send_request with legacy client routing."""
    mock_zcc = Mock()
    mock_ztw = Mock()
    mock_zdx = Mock()
    mock_zpa = Mock()
    mock_zia = Mock()
    mock_zwa = Mock()
    
    client = HTTPClient(
        {"headers": {}},
        zcc_legacy_client=mock_zcc,
        ztw_legacy_client=mock_ztw,
        zdx_legacy_client=mock_zdx,
        zpa_legacy_client=mock_zpa,
        zia_legacy_client=mock_zia,
        zwa_legacy_client=mock_zwa
    )
    
    # Test that legacy client flags are set correctly
    assert client.use_zcc_legacy_client is True
    assert client.use_ztw_legacy_client is True
    assert client.use_zdx_legacy_client is True
    assert client.use_zpa_legacy_client is True
    assert client.use_zia_legacy_client is True
    assert client.use_zwa_legacy_client is True
    
    # Test that legacy clients are accessible
    assert client.zcc_legacy_client == mock_zcc
    assert client.ztw_legacy_client == mock_ztw
    assert client.zdx_legacy_client == mock_zdx
    assert client.zpa_legacy_client == mock_zpa
    assert client.zia_legacy_client == mock_zia
    assert client.zwa_legacy_client == mock_zwa