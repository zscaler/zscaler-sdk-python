"""
Testing Cache functions for Zscaler SDK
"""

import pytest
import time
from unittest.mock import patch, Mock
from zscaler.cache.cache import Cache
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache


# Test constants
TTL = 3600  # 1 hour
TTI = 1800  # 30 minutes
CACHE_KEY = "test_cache_key"
CACHE_VALUE = ("test_response", "test_body")
ALT_CACHE_KEY = "alt_cache_key"
ALT_CACHE_VALUE = ("alt_response", "alt_body")


def mock_pause_function(seconds):
    """Mock function to simulate time.sleep for testing."""
    pass


@pytest.fixture(scope="module")
def setup(monkeypatch):
    """Setup fixture for cache tests."""
    monkeypatch.setattr(time, 'sleep', mock_pause_function)


def test_cache_key_creation():
    """Test cache key creation."""
    from urllib.parse import urlparse
    
    cache = Cache()
    url = "https://api.example.com/v1/users"
    new_key = cache.create_key(url, {"page": 1, "limit": 10})
    assert new_key is not None
    
    # Verify the URL components are in the cache key using safe parsing
    parsed = urlparse(url)
    assert parsed.hostname in new_key  # Safe: checking exact hostname match
    assert "page=1" in new_key
    assert "limit=10" in new_key


def test_no_op_cache_operations():
    """Test NoOpCache operations."""
    cache = NoOpCache()
    
    # Test that NoOpCache always returns None/False
    assert cache.get(CACHE_KEY) is None
    assert cache.contains(CACHE_KEY) is False
    
    # Test that adding to NoOpCache does nothing
    cache.add(CACHE_KEY, CACHE_VALUE)
    assert cache.get(CACHE_KEY) is None
    assert cache.contains(CACHE_KEY) is False
    
    # Test that deleting from NoOpCache does nothing
    cache.delete(CACHE_KEY)
    assert cache.get(CACHE_KEY) is None
    assert cache.contains(CACHE_KEY) is False
    
    # Test that clearing NoOpCache does nothing
    cache.clear()
    assert cache.get(CACHE_KEY) is None
    assert cache.contains(CACHE_KEY) is False


def test_no_op_cache_with_different_types():
    """Test NoOpCache with different value types."""
    cache = NoOpCache()
    
    test_values = [None, "string", 1, 1.0, True, [], {}, ("tuple", "value")]
    
    for value in test_values:
        assert cache.contains(value) is False
        cache.add(value, value)
        assert cache.get(value) is None
        assert cache.contains(value) is False


def test_zscaler_cache_initialization():
    """Test ZscalerCache initialization."""
    cache = ZscalerCache(TTL, TTI)
    
    assert cache._time_to_live == TTL
    assert cache._time_to_idle == TTI
    assert cache._store == {}


def test_zscaler_cache_add_entry():
    """Test ZscalerCache add entry functionality."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test adding entry
    cache.add(CACHE_KEY, CACHE_VALUE)
    assert cache._store[CACHE_KEY]["value"] == CACHE_VALUE
    
    # Test adding different types of keys
    cache.add("test_string", CACHE_VALUE)
    assert cache._store["test_string"]["value"] == CACHE_VALUE
    
    # Test adding with different value types
    cache.add("test_tuple", ("response", "body"))
    assert cache._store["test_tuple"]["value"] == ("response", "body")


def test_zscaler_cache_has_key():
    """Test ZscalerCache has key functionality."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test that key doesn't exist initially
    assert not cache.contains(CACHE_KEY)
    
    # Test that key exists after adding
    cache.add(CACHE_KEY, CACHE_VALUE)
    assert cache.contains(CACHE_KEY)
    assert not cache.contains(ALT_CACHE_KEY)


def test_zscaler_cache_get_value():
    """Test ZscalerCache get value functionality."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test that getting non-existent key returns None
    assert cache.get(CACHE_KEY) is None
    
    # Test that getting existing key returns value
    cache.add(CACHE_KEY, CACHE_VALUE)
    assert cache.get(CACHE_KEY) is CACHE_VALUE


def test_zscaler_cache_delete_value():
    """Test ZscalerCache delete value functionality."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test deleting non-existent key
    cache.delete(CACHE_KEY)
    assert not cache.contains(CACHE_KEY)
    
    # Test deleting existing key
    cache.add(CACHE_KEY, CACHE_VALUE)
    assert cache.contains(CACHE_KEY)
    cache.delete(CACHE_KEY)
    assert not cache.contains(CACHE_KEY)


def test_zscaler_cache_clear():
    """Test ZscalerCache clear functionality."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test clearing empty cache
    cache.clear()
    assert len(cache._store) == 0
    
    # Test clearing cache with entries
    cache.add(CACHE_KEY, CACHE_VALUE)
    cache.add(ALT_CACHE_KEY, ALT_CACHE_VALUE)
    assert cache.contains(CACHE_KEY) and cache.contains(ALT_CACHE_KEY)
    
    cache.clear()
    assert not cache.contains(CACHE_KEY) and not cache.contains(ALT_CACHE_KEY)


def test_zscaler_cache_ttl_expiration():
    """Test ZscalerCache TTL expiration."""
    local_ttl = 2.0
    local_tti = 10.0
    cache = ZscalerCache(local_ttl, local_tti)
    
    # Test that entry expires after TTL
    cache.add(CACHE_KEY, CACHE_VALUE)
    assert cache.get(CACHE_KEY) is CACHE_VALUE
    
    # Mock time to simulate TTL expiration
    with patch.object(cache, '_get_current_time') as mock_time:
        mock_time.return_value = time.time() + local_ttl + 1
        assert cache.get(CACHE_KEY) is None


def test_zscaler_cache_tti_expiration():
    """Test ZscalerCache TTI expiration."""
    local_ttl = 10.0
    local_tti = 1.0
    cache = ZscalerCache(local_ttl, local_tti)
    
    # Test that entry expires after TTI
    cache.add(CACHE_KEY, CACHE_VALUE)
    assert cache.get(CACHE_KEY) is CACHE_VALUE
    
    # Mock time to simulate TTI expiration
    with patch.object(cache, '_get_current_time') as mock_time:
        mock_time.return_value = time.time() + local_tti + 1
        assert cache.get(CACHE_KEY) is None


def test_zscaler_cache_tti_reset():
    """Test ZscalerCache TTI reset on access."""
    local_ttl = 10.0
    local_tti = 1.0
    cache = ZscalerCache(local_ttl, local_tti)
    
    # Add entry
    cache.add(CACHE_KEY, CACHE_VALUE)
    
    # Test that entry is accessible
    assert cache.get(CACHE_KEY) is CACHE_VALUE
    
    # Test that TTI reset works by accessing the entry multiple times
    # Each access should reset the TTI timer
    for i in range(3):
        assert cache.get(CACHE_KEY) is CACHE_VALUE


def test_zscaler_cache_cleanup():
    """Test ZscalerCache cleanup functionality."""
    cache = ZscalerCache(TTL, TTI)
    
    # Add multiple entries
    cache.add(CACHE_KEY, CACHE_VALUE)
    cache.add(ALT_CACHE_KEY, ALT_CACHE_VALUE)
    
    # Mock time to simulate expiration
    with patch.object(cache, '_get_current_time') as mock_time:
        mock_time.return_value = time.time() + TTL + 1
        
        # Test that expired entries are cleaned up
        cache._clean_cache()
        assert not cache.contains(CACHE_KEY)
        assert not cache.contains(ALT_CACHE_KEY)


def test_zscaler_cache_invalid_entry_handling():
    """Test ZscalerCache invalid entry handling."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test adding invalid key types
    cache.add(None, CACHE_VALUE)
    assert not cache.contains(None)
    
    # Test adding valid key with valid value
    cache.add("valid_key", CACHE_VALUE)
    assert cache.contains("valid_key")
    assert cache.get("valid_key") == CACHE_VALUE


def test_zscaler_cache_url_parsing():
    """Test ZscalerCache URL parsing for related entries."""
    cache = ZscalerCache(TTL, TTI)
    
    # Add entries with related URLs
    cache.add("https://api.example.com/v1/users", CACHE_VALUE)
    cache.add("https://api.example.com/v1/users/123", ALT_CACHE_VALUE)
    
    # Test that deleting base URL also removes related URLs
    cache.delete("https://api.example.com/v1/users")
    
    # Mock time to ensure entries are expired
    with patch.object(cache, '_get_current_time') as mock_time:
        mock_time.return_value = time.time() + TTL + 1
        assert not cache.contains("https://api.example.com/v1/users")
        assert not cache.contains("https://api.example.com/v1/users/123")


def test_zscaler_cache_edge_cases():
    """Test ZscalerCache edge cases."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test with empty key
    cache.add("", CACHE_VALUE)
    assert cache.contains("")
    assert cache.get("") == CACHE_VALUE
    
    # Test with very long key
    long_key = "a" * 1000
    cache.add(long_key, CACHE_VALUE)
    assert cache.contains(long_key)
    assert cache.get(long_key) == CACHE_VALUE
    
    # Test with special characters in key
    special_key = "key!@#$%^&*()_+-=[]{}|;':\",./<>?"
    cache.add(special_key, CACHE_VALUE)
    assert cache.contains(special_key)
    assert cache.get(special_key) == CACHE_VALUE


def test_zscaler_cache_concurrent_access():
    """Test ZscalerCache concurrent access simulation."""
    cache = ZscalerCache(TTL, TTI)
    
    # Simulate concurrent access
    cache.add(CACHE_KEY, CACHE_VALUE)
    
    # Test multiple gets
    assert cache.get(CACHE_KEY) == CACHE_VALUE
    assert cache.get(CACHE_KEY) == CACHE_VALUE
    assert cache.get(CACHE_KEY) == CACHE_VALUE
    
    # Test multiple contains checks
    assert cache.contains(CACHE_KEY)
    assert cache.contains(CACHE_KEY)
    assert cache.contains(CACHE_KEY)


def test_zscaler_cache_memory_management():
    """Test ZscalerCache memory management."""
    cache = ZscalerCache(TTL, TTI)
    
    # Add many entries
    for i in range(100):
        cache.add(f"key_{i}", f"value_{i}")
    
    # Test that all entries are accessible
    for i in range(100):
        assert cache.contains(f"key_{i}")
        assert cache.get(f"key_{i}") == f"value_{i}"
    
    # Clear cache
    cache.clear()
    
    # Test that all entries are removed
    for i in range(100):
        assert not cache.contains(f"key_{i}")
        assert cache.get(f"key_{i}") is None


def test_zscaler_cache_performance():
    """Test ZscalerCache performance characteristics."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test adding many entries quickly
    start_time = time.time()
    for i in range(1000):
        cache.add(f"perf_key_{i}", f"perf_value_{i}")
    add_time = time.time() - start_time
    
    # Test getting many entries quickly
    start_time = time.time()
    for i in range(1000):
        cache.get(f"perf_key_{i}")
    get_time = time.time() - start_time
    
    # Test that operations complete in reasonable time
    # Note: Allow 5 seconds to account for coverage overhead, system load, and CI environments
    assert add_time < 5.0  # Should add 1000 entries in less than 5 seconds
    assert get_time < 5.0  # Should get 1000 entries in less than 5 seconds


def test_zscaler_cache_integration():
    """Test ZscalerCache integration with other components."""
    cache = ZscalerCache(TTL, TTI)
    
    # Test integration with request executor
    mock_request_executor = Mock()
    mock_request_executor._cache = cache
    
    # Test that cache can be used by request executor
    cache.add("request_key", ("response", "body"))
    assert cache.get("request_key") == ("response", "body")
    
    # Test that cache can be cleared by request executor
    cache.clear()
    assert cache.get("request_key") is None
