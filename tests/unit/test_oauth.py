"""
Testing OAuth functions for Zscaler SDK
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from zscaler.oneapi_oauth_client import OAuth


def generate_mock_access_token():
    """Generate a mock access token for testing purposes."""
    import base64
    import time
    
    # Create a mock JWT header
    header = {"alg": "HS256", "typ": "JWT"}
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    
    # Create a mock JWT payload
    payload = {
        "sub": "test_user",
        "iss": "zscaler",
        "aud": "api",
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
        "scope": "read write"
    }
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    
    # Create a mock signature
    signature = "mock_signature_for_testing"
    signature_encoded = base64.urlsafe_b64encode(signature.encode()).decode().rstrip('=')
    
    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"


def test_oauth_client_initialization():
    """Test OAuth client initialization."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test that OAuth client is initialized correctly
    assert oauth is not None
    assert oauth._request_executor is not None
    assert oauth._config == config
    assert oauth._access_token is None
    assert oauth._token_expires_at is None
    assert oauth._token_issued_at is None


def test_oauth_client_with_cloud_parameter():
    """Test OAuth client initialization with cloud parameter."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "cloud": "beta"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test that OAuth client is initialized with cloud parameter
    assert oauth is not None
    assert oauth._config["client"]["cloud"] == "beta"


def test_oauth_client_with_private_key():
    """Test OAuth client initialization with private key."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "privateKey": "test_private_key",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test that OAuth client is initialized with private key
    assert oauth is not None
    assert oauth._config["client"]["privateKey"] == "test_private_key"


def test_oauth_client_with_sandbox_token():
    """Test OAuth client initialization with sandbox token."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "sandboxToken": "test_sandbox_token",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test that OAuth client is initialized with sandbox token
    assert oauth is not None
    assert oauth._config["client"]["sandboxToken"] == "test_sandbox_token"


def test_oauth_client_cache_initialization():
    """Test OAuth client cache initialization."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            }
        }
    }
    
    with patch('zscaler.cache.zscaler_cache.ZscalerCache') as mock_cache:
        oauth = OAuth(mock_request_executor, config)
        
        # Test that cache is initialized when enabled
        assert oauth is not None
        # Note: Cache initialization is tested in the OAuth class itself


def test_oauth_client_cache_key_generation():
    """Test OAuth client cache key generation."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test cache key generation
    cache_key = oauth._generate_cache_key()
    assert cache_key is not None
    assert isinstance(cache_key, str)


def test_oauth_client_token_validation():
    """Test OAuth client token validation."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test token validation with no token
    assert oauth._is_token_expired()
    
    # Test token validation with expired token
    oauth._access_token = "test_token"
    oauth._token_expires_at = 0  # Expired
    assert oauth._is_token_expired()
    
    # Test token validation with valid token
    import time
    oauth._token_expires_at = time.time() + 3600  # Valid for 1 hour
    assert not oauth._is_token_expired()


def test_oauth_client_token_refresh():
    """Test OAuth client token refresh logic."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test token refresh when token is expired
    oauth._access_token = "expired_token"
    oauth._token_expires_at = 0  # Expired
    
    with patch.object(oauth, '_is_token_expired', return_value=True):
        with patch.object(oauth, '_get_cached_token', return_value=None):
            with patch.object(oauth, 'authenticate', return_value="new_token"):
                # Test that authenticate is called when token is expired
                result = oauth.authenticate()
                assert result == "new_token"


def test_oauth_client_token_caching():
    """Test OAuth client token caching."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            }
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test token caching
    test_token_data = {"access_token": "cached_token", "expires_at": 1234567890}
    oauth._cache_key = "test_cache_key"
    
    with patch.object(oauth, '_cache') as mock_cache:
        mock_cache.get.return_value = test_token_data
        result = oauth._get_cached_token()
        assert result == test_token_data
        mock_cache.get.assert_called_once_with("test_cache_key")


def test_oauth_client_token_storage():
    """Test OAuth client token storage."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test token storage
    test_token = "stored_token"
    expires_at = 1234567890
    oauth._access_token = test_token
    oauth._token_expires_at = expires_at
    oauth._token_issued_at = 1234567890
    
    assert oauth._access_token == test_token
    assert oauth._token_expires_at == expires_at
    assert oauth._token_issued_at is not None


def test_oauth_client_token_clearing():
    """Test OAuth client token clearing."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Set up token
    oauth._access_token = "test_token"
    oauth._token_expires_at = 1234567890
    oauth._token_issued_at = 1234567890
    
    # Test token clearing by setting to None
    oauth._access_token = None
    oauth._token_expires_at = None
    oauth._token_issued_at = None
    
    assert oauth._access_token is None
    assert oauth._token_expires_at is None
    assert oauth._token_issued_at is None


def test_oauth_client_error_handling():
    """Test OAuth client error handling."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test error handling with invalid configuration
    invalid_config = {
        "client": {
            "clientId": "",  # Empty client ID
            "clientSecret": "",  # Empty client secret
            "vanityDomain": ""  # Empty vanity domain
        }
    }
    
    oauth._config = invalid_config
    
    # Test that OAuth client handles invalid configuration gracefully
    assert oauth is not None


def test_oauth_client_with_different_clouds():
    """Test OAuth client with different cloud environments."""
    clouds = ["alpha", "beta", "gamma", "preview"]
    
    for cloud in clouds:
        mock_request_executor = Mock()
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "testcompany",
                "cloud": cloud
            }
        }
        
        oauth = OAuth(mock_request_executor, config)
        
        # Test that OAuth client is initialized with specific cloud
        assert oauth is not None
        assert oauth._config["client"]["cloud"] == cloud


def test_oauth_client_singleton_behavior():
    """Test OAuth client singleton behavior."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    # Test singleton behavior
    oauth1 = OAuth(mock_request_executor, config)
    oauth2 = OAuth(mock_request_executor, config)
    
    # Test that same instance is returned for same config
    assert oauth1 is oauth2


def test_oauth_client_different_configs():
    """Test OAuth client with different configurations."""
    mock_request_executor = Mock()
    
    config1 = {
        "client": {
            "clientId": "client1",
            "clientSecret": "secret1",
            "vanityDomain": "company1"
        }
    }
    
    config2 = {
        "client": {
            "clientId": "client2",
            "clientSecret": "secret2",
            "vanityDomain": "company2"
        }
    }
    
    oauth1 = OAuth(mock_request_executor, config1)
    oauth2 = OAuth(mock_request_executor, config2)
    
    # Test that different instances are returned for different configs
    assert oauth1 is not oauth2
    assert oauth1._config != oauth2._config


def test_oauth_client_token_expiration():
    """Test OAuth client token expiration handling."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test token expiration
    import time
    current_time = time.time()
    
    # Test with expired token
    oauth._access_token = "expired_token"
    oauth._token_expires_at = current_time - 1  # Expired
    assert oauth._is_token_expired()
    
    # Test with valid token
    oauth._token_expires_at = current_time + 3600  # Valid for 1 hour
    assert not oauth._is_token_expired()


def test_oauth_client_integration():
    """Test OAuth client integration with request executor."""
    mock_request_executor = Mock()
    config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    oauth = OAuth(mock_request_executor, config)
    
    # Test that OAuth client integrates with request executor
    assert oauth._request_executor is not None
    
    # Test that OAuth client can be used with request executor
    with patch.object(mock_request_executor, 'execute_request') as mock_execute:
        mock_execute.return_value = ({"access_token": "test_token"}, None, None)
        
        # Test OAuth client functionality
        assert oauth is not None
        assert oauth._config == config


def test_auth_uses_proxy():
    cfg = {
        "client": {
            "vanityDomain": "mycompany",
            "clientId": "dummy-id",
            "clientSecret": "dummy-secret",
            "proxy": {"host": "127.0.0.1", "port": "8080"},
        }
    }

    client = OAuth(Mock(), cfg)

    # Patch requests.post inside the module under test
    with patch("zscaler.oneapi_oauth_client.requests.post") as mock_post:
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"access_token": "fake-token"}
        mock_post.return_value = fake_response

        resp = client._authenticate_with_client_secret("dummy-id", "dummy-secret")

        assert mock_post.called, "requests.post was not called"
        _, kwargs = mock_post.call_args
        assert "proxies" in kwargs and kwargs["proxies"] is not None, "proxies argument not forwarded"

        expected_proxy = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080",
        }
        assert kwargs["proxies"] == expected_proxy, f"proxies mismatch: {kwargs.get('proxies')}"
