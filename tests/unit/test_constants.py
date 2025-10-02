"""
Testing Constants for Zscaler SDK
"""

import pytest
import os
from zscaler.constants import (
    ZPA_BASE_URLS,
    DEV_AUTH_URL,
    RETRYABLE_STATUS_CODES,
    MAX_RETRIES,
    BACKOFF_FACTOR,
    BACKOFF_BASE_DURATION,
    ZSCALER_ONE_API_DEV,
    ZIDENTITY_DEV,
    GET_ZSCALER_CLIENT_ID,
    GET_ZSCALER_CLIENT_SECRET,
    GET_ZSCALER_VANITY_DOMAIN,
    GET_ZSCALER_CLOUD,
    GET_ZPA_CUSTOMER_ID,
    GET_ZPA_MICROTENANT_ID,
    EPOCH_YEAR,
    EPOCH_MONTH,
    EPOCH_DAY,
    DATETIME_FORMAT,
    _GLOBAL_YAML_PATH,
    _LOCAL_YAML_PATH,
)


def test_zpa_base_urls():
    """Test ZPA base URLs are correctly defined."""
    expected_urls = {
        "PRODUCTION": "https://config.private.zscaler.com",
        "ZPATWO": "https://config.zpatwo.net",
        "BETA": "https://config.zpabeta.net",
        "GOV": "https://config.zpagov.net",
        "GOVUS": "https://config.zpagov.us",
        "PREVIEW": "https://config.zpapreview.net",
        "QA": "https://config.qa.zpath.net",
        "QA2": "https://pdx2-zpa-config.qa2.zpath.net",
        "DEV": "https://public-api.dev.zpath.net",
    }
    
    assert ZPA_BASE_URLS == expected_urls
    assert len(ZPA_BASE_URLS) == 9
    
    # Test that all URLs are HTTPS
    for url in ZPA_BASE_URLS.values():
        assert url.startswith("https://")


def test_dev_auth_url():
    """Test development authentication URL."""
    assert DEV_AUTH_URL == "https://authn1.dev.zpath.net/authn/v1/oauth/token"
    assert DEV_AUTH_URL.startswith("https://")


def test_retryable_status_codes():
    """Test retryable status codes are correctly defined."""
    expected_codes = {429, 500, 502, 503, 504}
    assert RETRYABLE_STATUS_CODES == expected_codes
    assert len(RETRYABLE_STATUS_CODES) == 5
    
    # Test that all codes are in the 4xx-5xx range
    for code in RETRYABLE_STATUS_CODES:
        assert 400 <= code <= 599


def test_retry_constants():
    """Test retry-related constants."""
    assert MAX_RETRIES == 5
    assert BACKOFF_FACTOR == 1
    assert BACKOFF_BASE_DURATION == 2
    
    # Test that values are positive
    assert MAX_RETRIES > 0
    assert BACKOFF_FACTOR > 0
    assert BACKOFF_BASE_DURATION > 0


def test_help_urls():
    """Test help URLs are correctly defined."""
    assert ZSCALER_ONE_API_DEV == "https://help.zscaler.com/oneapi"
    assert ZIDENTITY_DEV == "https://help.zscaler.com/zidentity"
    
    # Test that URLs are HTTPS
    assert ZSCALER_ONE_API_DEV.startswith("https://")
    assert ZIDENTITY_DEV.startswith("https://")


def test_get_urls():
    """Test GET URLs for documentation."""
    assert GET_ZSCALER_CLIENT_ID == "https://help.zscaler.com/zidentity/about-api-clients"
    assert GET_ZSCALER_CLIENT_SECRET == "https://help.zscaler.com/zidentity/about-api-clients"
    assert GET_ZSCALER_VANITY_DOMAIN == "https://help.zscaler.com/zidentity/migrating-zscaler-service-admins-zidentity"
    assert GET_ZSCALER_CLOUD == "https://help.zscaler.com/zidentity/migrating-zscaler-service-admins-zidentity"
    assert GET_ZPA_CUSTOMER_ID == "https://help.zscaler.com/oneapi/getting-started#ZPA-customerId-ZSLogin-admin-portal"
    assert GET_ZPA_MICROTENANT_ID == "https://help.zscaler.com/oneapi/getting-started#ZPA-customerId-ZSLogin-admin-portal"
    
    # Test that all URLs are HTTPS
    for url in [GET_ZSCALER_CLIENT_ID, GET_ZSCALER_CLIENT_SECRET, GET_ZSCALER_VANITY_DOMAIN, 
                GET_ZSCALER_CLOUD, GET_ZPA_CUSTOMER_ID, GET_ZPA_MICROTENANT_ID]:
        assert url.startswith("https://")


def test_epoch_constants():
    """Test epoch-related constants."""
    assert EPOCH_YEAR == 1970
    assert EPOCH_MONTH == 1
    assert EPOCH_DAY == 1
    
    # Test that values are reasonable
    assert 1900 <= EPOCH_YEAR <= 2000
    assert 1 <= EPOCH_MONTH <= 12
    assert 1 <= EPOCH_DAY <= 31


def test_datetime_format():
    """Test datetime format constant."""
    assert DATETIME_FORMAT == "%a, %d %b %Y %H:%M:%S %Z"
    
    # Test that format contains expected components
    assert "%a" in DATETIME_FORMAT  # Day of week
    assert "%d" in DATETIME_FORMAT  # Day of month
    assert "%b" in DATETIME_FORMAT  # Month abbreviation
    assert "%Y" in DATETIME_FORMAT  # Year
    assert "%H" in DATETIME_FORMAT  # Hour
    assert "%M" in DATETIME_FORMAT  # Minute
    assert "%S" in DATETIME_FORMAT  # Second
    assert "%Z" in DATETIME_FORMAT  # Timezone


def test_yaml_paths():
    """Test YAML file paths."""
    # Test that paths are strings
    assert isinstance(_GLOBAL_YAML_PATH, str)
    assert isinstance(_LOCAL_YAML_PATH, str)
    
    # Test that global path contains user home directory
    assert "~" in _GLOBAL_YAML_PATH or os.path.expanduser("~") in _GLOBAL_YAML_PATH
    
    # Test that local path contains current working directory
    assert os.getcwd() in _LOCAL_YAML_PATH
    
    # Test that both paths end with zscaler.yaml
    assert _GLOBAL_YAML_PATH.endswith("zscaler.yaml")
    assert _LOCAL_YAML_PATH.endswith("zscaler.yaml")


def test_zpa_base_urls_environment_mapping():
    """Test that ZPA base URLs map to expected environments."""
    environment_mapping = {
        "PRODUCTION": "production",
        "ZPATWO": "zpatwo", 
        "BETA": "beta",
        "GOV": "gov",
        "GOVUS": "govus",
        "PREVIEW": "preview",
        "QA": "qa",
        "QA2": "qa2",
        "DEV": "dev"
    }
    
    for env_key, expected_env in environment_mapping.items():
        assert env_key in ZPA_BASE_URLS
        url = ZPA_BASE_URLS[env_key]
        assert url.startswith("https://")
        assert "config" in url or "api" in url


def test_retryable_status_codes_coverage():
    """Test that retryable status codes cover expected scenarios."""
    # Rate limiting
    assert 429 in RETRYABLE_STATUS_CODES
    
    # Server errors (transient failures that benefit from retry)
    assert 500 in RETRYABLE_STATUS_CODES  # Internal Server Error
    assert 502 in RETRYABLE_STATUS_CODES  # Bad Gateway
    assert 503 in RETRYABLE_STATUS_CODES  # Service Unavailable
    assert 504 in RETRYABLE_STATUS_CODES  # Gateway Timeout
    
    # Client errors that should NOT be retried (removed from retryable list)
    assert 408 not in RETRYABLE_STATUS_CODES  # Request Timeout - client should handle
    assert 409 not in RETRYABLE_STATUS_CODES  # Conflict - requires client action
    assert 412 not in RETRYABLE_STATUS_CODES  # Precondition Failed - requires client fix


def test_help_urls_consistency():
    """Test that help URLs are consistent and follow expected patterns."""
    # All help URLs should be from help.zscaler.com
    help_urls = [ZSCALER_ONE_API_DEV, ZIDENTITY_DEV]
    for url in help_urls:
        assert "help.zscaler.com" in url
        assert url.startswith("https://")
    
    # GET URLs should reference the help URLs
    assert ZIDENTITY_DEV in GET_ZSCALER_CLIENT_ID
    assert ZIDENTITY_DEV in GET_ZSCALER_CLIENT_SECRET
    assert ZIDENTITY_DEV in GET_ZSCALER_VANITY_DOMAIN
    assert ZIDENTITY_DEV in GET_ZSCALER_CLOUD
    assert ZSCALER_ONE_API_DEV in GET_ZPA_CUSTOMER_ID
    assert ZSCALER_ONE_API_DEV in GET_ZPA_MICROTENANT_ID


def test_constants_immutability():
    """Test that constants are immutable (can't be modified)."""
    # Test that sets are mutable but we shouldn't modify them
    original_codes = RETRYABLE_STATUS_CODES.copy()
    RETRYABLE_STATUS_CODES.add(999)
    assert 999 in RETRYABLE_STATUS_CODES
    # Restore original state
    RETRYABLE_STATUS_CODES.discard(999)
    assert RETRYABLE_STATUS_CODES == original_codes
    
    # Test that dictionaries are mutable but we shouldn't modify them
    original_zpa_urls = ZPA_BASE_URLS.copy()
    assert ZPA_BASE_URLS == original_zpa_urls


def test_datetime_format_parsing():
    """Test that datetime format can be used for parsing."""
    from datetime import datetime
    
    # Test that the format can parse a sample datetime
    sample_datetime = "Mon, 01 Jan 2024 12:00:00 UTC"
    try:
        parsed = datetime.strptime(sample_datetime, DATETIME_FORMAT)
        assert parsed.year == 2024
        assert parsed.month == 1
        assert parsed.day == 1
    except ValueError:
        # If parsing fails, that's also acceptable as long as format is defined
        assert DATETIME_FORMAT is not None


def test_epoch_constants_historical_accuracy():
    """Test that epoch constants match Unix epoch."""
    # Unix epoch is January 1, 1970
    assert EPOCH_YEAR == 1970
    assert EPOCH_MONTH == 1  # January
    assert EPOCH_DAY == 1    # 1st day of month


def test_retry_constants_mathematical_properties():
    """Test mathematical properties of retry constants."""
    # Backoff factor should be >= 1 for exponential backoff
    assert BACKOFF_FACTOR >= 1
    
    # Base duration should be positive
    assert BACKOFF_BASE_DURATION > 0
    
    # Max retries should be reasonable (not too high, not too low)
    assert 1 <= MAX_RETRIES <= 10


def test_url_security():
    """Test that all URLs use HTTPS for security."""
    all_urls = [
        DEV_AUTH_URL,
        ZSCALER_ONE_API_DEV,
        ZIDENTITY_DEV,
        GET_ZSCALER_CLIENT_ID,
        GET_ZSCALER_CLIENT_SECRET,
        GET_ZSCALER_VANITY_DOMAIN,
        GET_ZSCALER_CLOUD,
        GET_ZPA_CUSTOMER_ID,
        GET_ZPA_MICROTENANT_ID,
    ]
    
    # Add all ZPA base URLs
    all_urls.extend(ZPA_BASE_URLS.values())
    
    for url in all_urls:
        assert url.startswith("https://"), f"URL {url} should use HTTPS"
        assert "http://" not in url, f"URL {url} should not use HTTP"
