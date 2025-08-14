"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import pytest
import time
import json
from unittest.mock import Mock, patch
from zscaler.oneapi_oauth_client import OAuth
from zscaler.cache.zscaler_cache import ZscalerCache


class MockRequestExecutor:
    """Mock request executor for testing OAuth functionality"""
    def __init__(self):
        self._default_headers = {}


class TestEnhancedOAuthClient:
    """
    Integration Tests for the Enhanced OAuth Client
    """

    def test_oauth_initialization_without_cache(self, fs):
        """Test OAuth client initialization without caching"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Verify initialization
        assert oauth._access_token is None
        assert oauth._token_expires_at is None
        assert oauth._token_issued_at is None
        assert oauth._cache is None
        assert oauth._cache_enabled() is False
        assert oauth._cache_key == "oauth_token_test_client_id_test.zscaler.com_production"

    def test_oauth_initialization_with_cache(self, fs):
        """Test OAuth client initialization with caching enabled"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            },
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Verify initialization with cache
        assert oauth._access_token is None
        assert oauth._token_expires_at is None
        assert oauth._token_issued_at is None
        assert oauth._cache is not None
        assert isinstance(oauth._cache, ZscalerCache)
        assert oauth._cache_enabled() is True
        assert oauth._cache_key == "oauth_token_test_client_id_test.zscaler.com_production"

    def test_cache_key_generation(self, fs):
        """Test cache key generation for different configurations"""
        # Test OneAPI configuration
        config_oneapi = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth_oneapi = OAuth(request_executor, config_oneapi)
        
        expected_key_oneapi = "oauth_token_test_client_id_test.zscaler.com_production"
        assert oauth_oneapi._cache_key == expected_key_oneapi
        
        # Test legacy configuration (should handle gracefully)
        config_legacy = {
            "client": {
                "username": "test_user",
                "api_key": "test_api_key",
                "cloud": "production"
            }
        }
        
        oauth_legacy = OAuth(request_executor, config_legacy)
        expected_key_legacy = "oauth_token_legacy_test_user_test_api_key_production"
        assert oauth_legacy._cache_key == expected_key_legacy

    def test_token_expiration_logic(self, fs):
        """Test token expiration logic"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Test with no token
        assert oauth._is_token_expired() is True
        
        # Test with expired token
        oauth._token_expires_at = time.time() - 3600  # Expired 1 hour ago
        assert oauth._is_token_expired() is True
        
        # Test with valid token
        oauth._token_expires_at = time.time() + 3600  # Valid for 1 hour
        assert oauth._is_token_expired() is False
        
        # Test with cached token data
        cached_token_data = {
            'access_token': 'test_token',
            'expires_at': time.time() + 3600,
            'issued_at': time.time()
        }
        assert oauth._is_token_expired(cached_token_data) is False
        
        # Test with expired cached token
        cached_token_data['expires_at'] = time.time() - 3600
        assert oauth._is_token_expired(cached_token_data) is True

    def test_cache_functionality(self, fs):
        """Test cache functionality"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            },
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Test caching a token
        test_token = "test_access_token_12345"
        expires_at = time.time() + 3600
        oauth._cache_token(test_token, expires_at)
        
        # Test retrieving from cache
        cached_token = oauth._get_cached_token()
        assert cached_token is not None
        assert cached_token['access_token'] == test_token
        assert cached_token['expires_at'] == expires_at
        assert 'issued_at' in cached_token
        
        # Test cache enabled check
        assert oauth._cache_enabled() is True

    def test_token_info_retrieval(self, fs):
        """Test token information retrieval"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            },
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Test token info without token
        token_info = oauth.get_token_info()
        assert token_info['has_token'] is False
        assert token_info['expires_at'] is None
        assert token_info['issued_at'] is None
        assert token_info['is_expired'] is True
        assert token_info['time_until_expiry'] is None
        assert token_info['cached'] is False
        
        # Test token info with token
        oauth._access_token = "test_token"
        oauth._token_expires_at = time.time() + 3600
        oauth._token_issued_at = time.time()
        
        token_info = oauth.get_token_info()
        assert token_info['has_token'] is True
        assert token_info['expires_at'] == oauth._token_expires_at
        assert token_info['issued_at'] == oauth._token_issued_at
        assert token_info['is_expired'] is False
        assert token_info['time_until_expiry'] > 0
        # Note: cached field behavior depends on implementation
        assert 'cached' in token_info

    def test_clear_access_token(self, fs):
        """Test clearing access token"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            },
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Set up token and cache
        oauth._access_token = "test_token"
        oauth._token_expires_at = time.time() + 3600
        oauth._token_issued_at = time.time()
        oauth._cache_token("test_token", oauth._token_expires_at)
        
        # Verify token exists
        assert oauth._access_token == "test_token"
        assert oauth._get_cached_token() is not None
        
        # Clear token
        oauth.clear_access_token()
        
        # Verify token is cleared
        assert oauth._access_token is None
        assert oauth._token_expires_at is None
        assert oauth._token_issued_at is None
        assert oauth._get_cached_token() is None

    def test_legacy_client_handling(self, fs):
        """Test handling of legacy client configurations"""
        config = {
            "client": {
                "username": "test_user",
                "api_key": "test_api_key",
                "cloud": "production"
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Verify legacy client is handled gracefully
        assert oauth._get_access_token() is None
        
        # Test authenticate method with legacy config
        with pytest.raises(ValueError, match="OAuth authentication not available for legacy client configurations"):
            oauth.authenticate()

    def test_cache_with_different_ttl_tti(self, fs):
        """Test cache initialization with different TTL/TTI values"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            },
            "cache": {
                "enabled": True,
                "defaultTtl": 7200,  # 2 hours
                "defaultTti": 3600   # 1 hour
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Verify cache is created with custom TTL/TTI
        assert oauth._cache is not None
        assert isinstance(oauth._cache, ZscalerCache)
        assert oauth._cache_enabled() is True

    def test_singleton_pattern(self, fs):
        """Test OAuth singleton pattern"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            }
        }
        
        request_executor1 = MockRequestExecutor()
        request_executor2 = MockRequestExecutor()
        
        oauth1 = OAuth(request_executor1, config)
        oauth2 = OAuth(request_executor2, config)
        
        # Verify singleton pattern (same config should return same instance)
        assert oauth1 is oauth2
        
        # Test with different config
        config2 = {
            "client": {
                "clientId": "test_client_id_2",  # Different client ID
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            }
        }
        
        oauth3 = OAuth(request_executor1, config2)
        
        # Different config should create different instance
        assert oauth1 is not oauth3

    def test_error_handling(self, fs):
        """Test error handling in OAuth client"""
        config = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "vanityDomain": "test.zscaler.com",
                "cloud": "production"
            },
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            }
        }
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config)
        
        # Test with invalid cache data
        with patch.object(oauth._cache, 'get', return_value="invalid_data"):
            cached_token = oauth._get_cached_token()
            assert cached_token is None
        
        # Test cache error handling
        with patch.object(oauth._cache, 'get', side_effect=Exception("Cache error")):
            cached_token = oauth._get_cached_token()
            assert cached_token is None

    def test_configuration_validation(self, fs):
        """Test configuration validation"""
        # Test with missing client configuration
        config_invalid = {}
        
        request_executor = MockRequestExecutor()
        oauth = OAuth(request_executor, config_invalid)
        
        # Should handle gracefully
        assert oauth._cache_key == "oauth_token_legacy_unknown_unknown_production"
        
        # Test with partial client configuration (missing vanityDomain)
        config_partial = {
            "client": {
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
                "cloud": "production"
                # Missing vanityDomain
            }
        }
        
        # This should raise a KeyError since vanityDomain is required
        with pytest.raises(KeyError, match="vanityDomain"):
            oauth_partial = OAuth(request_executor, config_partial) 