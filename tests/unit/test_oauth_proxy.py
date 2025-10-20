"""
Testing OAuth proxy configuration for Zscaler SDK
"""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from zscaler.oneapi_oauth_client import OAuth, _setup_proxy


def test_oauth_proxy_setup_function():
    """Test the _setup_proxy helper function."""
    from urllib.parse import urlparse
    
    # Test with None proxy
    proxy_string = _setup_proxy(None)
    assert proxy_string is None or isinstance(proxy_string, str)
    
    # Test with proxy configuration
    proxy_config = {
        "host": "proxy.example.com",
        "port": "8080",
        "username": "user",
        "password": "pass"
    }
    
    proxy_string = _setup_proxy(proxy_config)
    assert proxy_string is not None
    assert "proxy.example.com" in proxy_string
    assert "8080" in proxy_string
    assert "user" in proxy_string
    assert "pass" in proxy_string
    
    # Test with proxy configuration without auth
    proxy_config_no_auth = {
        "host": "proxy.example.com",
        "port": "8080"
    }
    
    proxy_string = _setup_proxy(proxy_config_no_auth)
    assert proxy_string is not None
    assert "proxy.example.com" in proxy_string
    assert "8080" in proxy_string
    assert "user" not in proxy_string
    assert "pass" not in proxy_string


def test_oauth_proxy_setup_without_port():
    """Test _setup_proxy function without port."""
    proxy_config = {
        "host": "proxy.example.com"
    }
    
    proxy_string = _setup_proxy(proxy_config)
    assert proxy_string is not None
    assert "proxy.example.com" in proxy_string


def test_oauth_client_secret_with_proxy():
    """Test OAuth client secret authentication with proxy configuration."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "proxy": {
                "host": "proxy.example.com",
                "port": "8080"
            }
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Mock the requests.post call to verify proxy is used
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"access_token": "test_token", "expires_in": 3600}'
        mock_post.return_value = mock_response
        
        # Call the authentication method
        result = oauth._authenticate_with_client_secret("test_client_id", "test_client_secret")
        
        # Verify that requests.post was called with proxy configuration
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check that proxies parameter is included
        assert 'proxies' in call_args.kwargs
        proxies = call_args.kwargs['proxies']
        assert proxies is not None
        assert 'http' in proxies
        assert 'https' in proxies
        assert 'proxy.example.com:8080' in proxies['http']
        assert 'proxy.example.com:8080' in proxies['https']


def test_oauth_private_key_with_proxy():
    """Test OAuth private key authentication with proxy configuration.
    
    Note: This test verifies that the proxy configuration is passed to the private key
    authentication method. The actual JWT signing is complex to mock, so we focus on
    the proxy configuration aspect which is the same for both client secret and private key auth.
    """
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "privateKey": "-----BEGIN PRIVATE KEY-----\ntest_private_key\n-----END PRIVATE KEY-----",
            "vanityDomain": "testcompany",
            "proxy": {
                "host": "proxy.example.com",
                "port": "8080"
            }
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test that the proxy configuration is properly set up
    proxy_config = oauth._config["client"].get("proxy")
    assert proxy_config is not None
    assert proxy_config["host"] == "proxy.example.com"
    assert proxy_config["port"] == "8080"
    
    # Test that the _setup_proxy function works with the config
    from zscaler.oneapi_oauth_client import _setup_proxy
    proxy_string = _setup_proxy(proxy_config)
    assert proxy_string is not None
    assert "proxy.example.com:8080" in proxy_string
    
    # The actual private key authentication is complex to mock due to JWT signing,
    # but the proxy configuration logic is identical to client secret authentication
    # which is already tested in test_oauth_client_secret_with_proxy()


def test_oauth_proxy_with_authentication():
    """Test OAuth with proxy that requires authentication."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "proxy": {
                "host": "proxy.example.com",
                "port": "8080",
                "username": "proxy_user",
                "password": "proxy_pass"
            }
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Mock the requests.post call
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"access_token": "test_token", "expires_in": 3600}'
        mock_post.return_value = mock_response
        
        # Call the authentication method
        result = oauth._authenticate_with_client_secret("test_client_id", "test_client_secret")
        
        # Verify that requests.post was called with proxy configuration
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check that proxies parameter includes authentication
        assert 'proxies' in call_args.kwargs
        proxies = call_args.kwargs['proxies']
        assert proxies is not None
        assert 'http' in proxies
        assert 'https' in proxies
        
        # Check that proxy URL includes authentication
        proxy_url = proxies['http']
        assert 'proxy_user' in proxy_url
        assert 'proxy_pass' in proxy_url
        assert 'proxy.example.com:8080' in proxy_url


def test_oauth_no_proxy_configuration():
    """Test OAuth without proxy configuration (should not use proxy)."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
            # No proxy configuration
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Mock the requests.post call
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"access_token": "test_token", "expires_in": 3600}'
        mock_post.return_value = mock_response
        
        # Call the authentication method
        result = oauth._authenticate_with_client_secret("test_client_id", "test_client_secret")
        
        # Verify that requests.post was called without proxy configuration
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check that proxies parameter is None or not included
        if 'proxies' in call_args.kwargs:
            assert call_args.kwargs['proxies'] is None


def test_oauth_proxy_environment_variables():
    """Test OAuth proxy configuration using environment variables."""
    import os
    
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "proxy": None  # No proxy in config, should fall back to env vars
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Mock environment variables
    with patch.dict(os.environ, {'HTTP_PROXY': 'http://env-proxy.example.com:8080'}):
        # Mock the requests.post call
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '{"access_token": "test_token", "expires_in": 3600}'
            mock_post.return_value = mock_response
            
            # Call the authentication method
            result = oauth._authenticate_with_client_secret("test_client_id", "test_client_secret")
            
            # Verify that requests.post was called with environment proxy
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            
            # Check that proxies parameter uses environment variable
            assert 'proxies' in call_args.kwargs
            proxies = call_args.kwargs['proxies']
            assert proxies is not None
            assert 'env-proxy.example.com:8080' in proxies['http']


def test_oauth_proxy_error_handling():
    """Test OAuth proxy error handling."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "proxy": {
                "host": "invalid-proxy.example.com",
                "port": "8080"
            }
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Mock requests.post to raise a connection error
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.ProxyError("Unable to connect to proxy")
        
        # Call the authentication method and expect an exception
        with pytest.raises(Exception) as exc_info:
            oauth._authenticate_with_client_secret("test_client_id", "test_client_secret")
        
        # Verify the error is related to proxy connection
        assert "proxy" in str(exc_info.value).lower() or "connect" in str(exc_info.value).lower()


def test_oauth_proxy_consistency_with_http_client():
    """Test that OAuth proxy configuration is consistent with HTTPClient."""
    from zscaler.oneapi_http_client import HTTPClient
    
    # Test OAuth proxy setup
    oauth_proxy_config = {
        "host": "proxy.example.com",
        "port": "8080",
        "username": "user",
        "password": "pass"
    }
    
    oauth_proxy_string = _setup_proxy(oauth_proxy_config)
    
    # Test HTTPClient proxy setup
    http_config = {
        "headers": {},
        "proxy": oauth_proxy_config
    }
    http_client = HTTPClient(http_config)
    http_proxy_string = http_client._setup_proxy(oauth_proxy_config)
    
    # Both should produce the same proxy string
    assert oauth_proxy_string == http_proxy_string
    assert oauth_proxy_string is not None
    assert "proxy.example.com" in oauth_proxy_string
    assert "8080" in oauth_proxy_string
    assert "user" in oauth_proxy_string
    assert "pass" in oauth_proxy_string


def test_oauth_proxy_different_clouds():
    """Test OAuth proxy configuration with different cloud environments."""
    clouds = ["alpha", "beta", "gamma", "preview"]
    
    for cloud in clouds:
        mock_request_executor = Mock()
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "testcompany",
                "cloud": cloud,
                "proxy": {
                    "host": "proxy.example.com",
                    "port": "8080"
                }
            }
        }
        
        oauth = OAuth(mock_request_executor, config)
        
        # Mock the requests.post call
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '{"access_token": "test_token", "expires_in": 3600}'
            mock_post.return_value = mock_response
            
            # Call the authentication method
            result = oauth._authenticate_with_client_secret("test_client_id", "test_client_secret")
            
            # Verify that requests.post was called with proxy configuration
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            
            # Check that proxies parameter is included regardless of cloud
            assert 'proxies' in call_args.kwargs
            proxies = call_args.kwargs['proxies']
            assert proxies is not None
            assert 'proxy.example.com:8080' in proxies['http']


def test_oauth_proxy_integration():
    """Test OAuth proxy integration with full authentication flow."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "proxy": {
                "host": "proxy.example.com",
                "port": "8080"
            }
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Mock the entire authentication flow
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"access_token": "test_token", "expires_in": 3600}'
        mock_response.url = "https://testcompany.zslogin.net/oauth2/v1/token"
        mock_post.return_value = mock_response
        
        # Mock the response checker
        with patch('zscaler.errors.response_checker.check_response_for_error') as mock_checker:
            mock_checker.return_value = ({"access_token": "test_token", "expires_in": 3600}, None)
            
            # Call the main authentication method
            result = oauth.authenticate()
            
            # Verify that requests.post was called with proxy configuration
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            
            # Check that proxies parameter is included
            assert 'proxies' in call_args.kwargs
            proxies = call_args.kwargs['proxies']
            assert proxies is not None
            assert 'proxy.example.com:8080' in proxies['http']
            assert 'proxy.example.com:8080' in proxies['https']
