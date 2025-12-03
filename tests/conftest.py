# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Global pytest configuration for VCR-based testing.

This module configures VCR (Video Cassette Recorder) for recording and
replaying HTTP interactions in tests, eliminating the need for live API
access during test execution.

Usage:
    - MOCK_TESTS=true (default): Use recorded cassettes
    - MOCK_TESTS=false: Use real API (for recording or live testing)
    - pytest --record-mode=rewrite: Re-record all cassettes
"""

import os
import re
from functools import wraps

import pytest

# Try to import VCR - graceful fallback if not installed
try:
    from pytest_recording._vcr import use_cassette

    HAS_VCR = True
except ImportError:
    HAS_VCR = False

# Constants for test configuration
PYTEST_MOCK_CLIENT = "pytest_mock_client"
PYTEST_RE_RECORD = "record_mode"
MOCK_TESTS = "MOCK_TESTS"

# Test URLs to replace real Zscaler URLs in cassettes
TEST_URLS = {
    "base": "https://api.test.zscaler.com",
    "zia": "https://zsapi.test.zscaler.com",
    "zpa": "https://config.test.zscaler.com",
    "zcc": "https://mobile.test.zscaler.com",
    "zdx": "https://zdx.test.zscaler.com",
    "zidentity": "https://identity.test.zscaler.com",
    "zeasm": "https://easm.test.zscaler.com",
}

# Regex patterns for Zscaler service URLs (string version)
URL_PATTERNS = {
    "zia": r"https://zsapi[a-z0-9-]*\.zscaler[a-z]*\.net",
    "zia_alt": r"https://[a-z0-9-]+\.zsapi\.zscaler[a-z]*\.net",
    "zpa": r"https://config\.private\.zscaler\.com",
    "zpa_alt": r"https://[a-z0-9-]+\.private\.zscaler\.com",
    "zcc": r"https://api-mobile\.zscaler\.net",
    "zdx": r"https://api\.zdxcloud\.net",
    "zidentity": r"https://[a-z0-9-]+\.zslogin\.net",
    "zeasm": r"https://api\.zsapi\.net",
}

# Binary versions for response body sanitization
URL_PATTERNS_BYTES = {k: v.encode() for k, v in URL_PATTERNS.items()}
TEST_URLS_BYTES = {k: v.encode() for k, v in TEST_URLS.items()}


def stub_sleep(func):
    """Decorator to speed up time.sleep function used in any methods under test."""
    import time
    from time import sleep

    def newsleep(seconds):
        sleep_speed_factor = 10.0
        sleep(seconds / sleep_speed_factor)

    time.sleep = newsleep

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def is_mock_tests_flag_true():
    """
    Check if tests should use recorded cassettes.

    Returns True by default (use cassettes).
    Set MOCK_TESTS=false to use real APIs.
    """
    return os.environ.get(MOCK_TESTS, "true").strip().lower() != "false"


def before_record_request(request):
    """
    Sanitize HTTP request before recording to cassette.

    - Replaces real Zscaler URLs with test URLs
    - Redacts authorization headers
    - Removes sensitive query parameters
    """
    # Sanitize URLs - map patterns to appropriate test URLs
    pattern_to_test_url = {
        "zia": TEST_URLS["zia"],
        "zia_alt": TEST_URLS["zia"],
        "zpa": TEST_URLS["zpa"],
        "zpa_alt": TEST_URLS["zpa"],
        "zcc": TEST_URLS["zcc"],
        "zdx": TEST_URLS["zdx"],
        "zidentity": TEST_URLS["zidentity"],
        "zeasm": TEST_URLS["zeasm"],
    }

    for service, pattern in URL_PATTERNS.items():
        test_url = pattern_to_test_url.get(service, TEST_URLS["base"])
        request.uri = re.sub(pattern, test_url, request.uri)

    # Sanitize Authorization header
    if "authorization" in request.headers:
        auth = str(request.headers["authorization"])
        if "Bearer" in auth:
            request.headers["authorization"] = "Bearer REDACTED_TOKEN"
        else:
            request.headers["authorization"] = "REDACTED"

    # Sanitize any API keys in headers
    sensitive_headers = ["x-api-key", "x-zscloud-customer-id", "cookie"]
    for key in sensitive_headers:
        if key in request.headers:
            request.headers[key] = "REDACTED"

    # Sanitize request body (for OAuth token requests and credential payloads)
    if request.body:
        body = request.body
        if isinstance(body, bytes):
            body = re.sub(rb'client_secret=[^&"]*', b'client_secret=REDACTED', body)
            body = re.sub(rb'"client_secret"\s*:\s*"[^"]*"', b'"client_secret":"REDACTED"', body)
            body = re.sub(rb'"password"\s*:\s*"[^"]*"', b'"password":"REDACTED"', body)
            body = re.sub(rb'"apiKey"\s*:\s*"[^"]*"', b'"apiKey":"REDACTED"', body)
            body = re.sub(rb'"api_key"\s*:\s*"[^"]*"', b'"api_key":"REDACTED"', body)
            body = re.sub(rb'"preSharedKey"\s*:\s*"[^"]*"', b'"preSharedKey":"REDACTED"', body)
            body = re.sub(rb'"pre_shared_key"\s*:\s*"[^"]*"', b'"pre_shared_key":"REDACTED"', body)
            body = re.sub(rb'"psk"\s*:\s*"[^"]*"', b'"psk":"REDACTED"', body)
        else:
            body = re.sub(r'client_secret=[^&"]*', 'client_secret=REDACTED', body)
            body = re.sub(r'"client_secret"\s*:\s*"[^"]*"', '"client_secret":"REDACTED"', body)
            body = re.sub(r'"password"\s*:\s*"[^"]*"', '"password":"REDACTED"', body)
            body = re.sub(r'"apiKey"\s*:\s*"[^"]*"', '"apiKey":"REDACTED"', body)
            body = re.sub(r'"api_key"\s*:\s*"[^"]*"', '"api_key":"REDACTED"', body)
            body = re.sub(r'"preSharedKey"\s*:\s*"[^"]*"', '"preSharedKey":"REDACTED"', body)
            body = re.sub(r'"pre_shared_key"\s*:\s*"[^"]*"', '"pre_shared_key":"REDACTED"', body)
            body = re.sub(r'"psk"\s*:\s*"[^"]*"', '"psk":"REDACTED"', body)
        request.body = body

    return request


def before_record_response(response):
    """
    Sanitize HTTP response before recording to cassette.

    - Replaces real Zscaler URLs in response body
    - Redacts bearer tokens and JWT tokens
    - Removes sensitive headers
    """
    if "body" in response and "string" in response["body"]:
        body = response["body"]["string"]

        # Map patterns to test URLs for bytes
        pattern_to_test_url_bytes = {
            "zia": TEST_URLS_BYTES["zia"],
            "zia_alt": TEST_URLS_BYTES["zia"],
            "zpa": TEST_URLS_BYTES["zpa"],
            "zpa_alt": TEST_URLS_BYTES["zpa"],
            "zcc": TEST_URLS_BYTES["zcc"],
            "zdx": TEST_URLS_BYTES["zdx"],
            "zidentity": TEST_URLS_BYTES["zidentity"],
            "zeasm": TEST_URLS_BYTES["zeasm"],
        }

        # Handle bytes body
        if isinstance(body, bytes):
            # Redact JWT tokens (they start with eyJ)
            body = re.sub(rb'"access_token"\s*:\s*"[^"]*"', b'"access_token":"REDACTED_TOKEN"', body)
            body = re.sub(rb'"token"\s*:\s*"[^"]*"', b'"token":"REDACTED_TOKEN"', body)
            body = re.sub(rb'eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*', b'REDACTED_JWT_TOKEN', body)
            # Redact password and API key fields
            body = re.sub(rb'"password"\s*:\s*"[^"]*"', b'"password":"REDACTED"', body)
            body = re.sub(rb'"apiKey"\s*:\s*"[^"]*"', b'"apiKey":"REDACTED"', body)
            body = re.sub(rb'"api_key"\s*:\s*"[^"]*"', b'"api_key":"REDACTED"', body)
            body = re.sub(rb'"client_secret"\s*:\s*"[^"]*"', b'"client_secret":"REDACTED"', body)
            # Redact pre-shared keys
            body = re.sub(rb'"preSharedKey"\s*:\s*"[^"]*"', b'"preSharedKey":"REDACTED"', body)
            body = re.sub(rb'"pre_shared_key"\s*:\s*"[^"]*"', b'"pre_shared_key":"REDACTED"', body)
            body = re.sub(rb'"psk"\s*:\s*"[^"]*"', b'"psk":"REDACTED"', body)
            # Redact private keys (RSA, EC, etc.)
            body = re.sub(rb'-----BEGIN[A-Z ]*PRIVATE KEY-----[^-]+-----END[A-Z ]*PRIVATE KEY-----', b'-----BEGIN PRIVATE KEY-----REDACTED-----END PRIVATE KEY-----', body)
            body = re.sub(rb'"privateKey"\s*:\s*"[^"]*"', b'"privateKey":"REDACTED"', body)
            body = re.sub(rb'"private_key"\s*:\s*"[^"]*"', b'"private_key":"REDACTED"', body)

            # Redact any email-like values (anything with @ in a quoted string)
            body = re.sub(rb'"[^"]*@[^"]*"', b'"REDACTED"', body)

            for service, pattern in URL_PATTERNS_BYTES.items():
                test_url = pattern_to_test_url_bytes.get(service, TEST_URLS_BYTES["base"])
                body = re.sub(pattern, test_url, body)
        else:
            # Redact JWT tokens (they start with eyJ)
            body = re.sub(r'"access_token"\s*:\s*"[^"]*"', '"access_token":"REDACTED_TOKEN"', body)
            body = re.sub(r'"token"\s*:\s*"[^"]*"', '"token":"REDACTED_TOKEN"', body)
            body = re.sub(r'eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*', 'REDACTED_JWT_TOKEN', body)
            # Redact password and API key fields
            body = re.sub(r'"password"\s*:\s*"[^"]*"', '"password":"REDACTED"', body)
            body = re.sub(r'"apiKey"\s*:\s*"[^"]*"', '"apiKey":"REDACTED"', body)
            body = re.sub(r'"api_key"\s*:\s*"[^"]*"', '"api_key":"REDACTED"', body)
            body = re.sub(r'"client_secret"\s*:\s*"[^"]*"', '"client_secret":"REDACTED"', body)
            # Redact pre-shared keys
            body = re.sub(r'"preSharedKey"\s*:\s*"[^"]*"', '"preSharedKey":"REDACTED"', body)
            body = re.sub(r'"pre_shared_key"\s*:\s*"[^"]*"', '"pre_shared_key":"REDACTED"', body)
            body = re.sub(r'"psk"\s*:\s*"[^"]*"', '"psk":"REDACTED"', body)
            # Redact private keys (RSA, EC, etc.)
            body = re.sub(r'-----BEGIN[A-Z ]*PRIVATE KEY-----[^-]+-----END[A-Z ]*PRIVATE KEY-----', '-----BEGIN PRIVATE KEY-----REDACTED-----END PRIVATE KEY-----', body)
            body = re.sub(r'"privateKey"\s*:\s*"[^"]*"', '"privateKey":"REDACTED"', body)
            body = re.sub(r'"private_key"\s*:\s*"[^"]*"', '"private_key":"REDACTED"', body)

            # Redact any email-like values (anything with @ in a quoted string)
            body = re.sub(r'"[^"]*@[^"]*"', '"REDACTED"', body)

            pattern_to_test_url = {
                "zia": TEST_URLS["zia"],
                "zia_alt": TEST_URLS["zia"],
                "zpa": TEST_URLS["zpa"],
                "zpa_alt": TEST_URLS["zpa"],
                "zcc": TEST_URLS["zcc"],
                "zdx": TEST_URLS["zdx"],
                "zidentity": TEST_URLS["zidentity"],
                "zeasm": TEST_URLS["zeasm"],
            }
            for service, pattern in URL_PATTERNS.items():
                test_url = pattern_to_test_url.get(service, TEST_URLS["base"])
                body = re.sub(pattern, test_url, body)

        response["body"]["string"] = body

    # Remove sensitive response headers
    sensitive_headers = ["set-cookie", "x-zscloud-customer-id"]
    for header in sensitive_headers:
        if header in response.get("headers", {}):
            response["headers"][header] = ["REDACTED"]

    return response


if HAS_VCR:

    @pytest.fixture(autouse=True)
    def vcr(request, vcr_markers, vcr_cassette_dir, record_mode, pytestconfig):
        """
        Automatically install a cassette for tests marked with @pytest.mark.vcr().
        
        VCR is active for both:
        - MOCK_TESTS=true (playback mode, record_mode="none")
        - MOCK_TESTS=false (recording mode, record_mode="new_episodes")
        """
        if vcr_markers:
            config = request.getfixturevalue("vcr_config")
            default_cassette = request.getfixturevalue("default_cassette_name")
            with use_cassette(
                default_cassette,
                vcr_cassette_dir,
                record_mode,
                vcr_markers,
                config,
                pytestconfig,
            ) as cassette:
                yield cassette
        else:
            yield None


@pytest.fixture(scope="module")
def vcr_config():
    """VCR configuration for request/response sanitization."""
    # Use "none" for playback-only (MOCK_TESTS=true), "new_episodes" for recording
    # When MOCK_TESTS=true (default), we don't want any real API calls
    # When MOCK_TESTS=false, we allow recording new requests
    mode = "none" if is_mock_tests_flag_true() else "new_episodes"
    
    return {
        "before_record_request": before_record_request,
        "before_record_response": before_record_response,
        "filter_headers": [
            "authorization",
            "cookie",
            "set-cookie",
            "x-zscloud-customer-id",
            "x-api-key",
        ],
        "filter_post_data_parameters": [
            ("client_secret", "REDACTED"),
            ("apiKey", "REDACTED"),
            ("password", "REDACTED"),
        ],
        "match_on": ["method", "path", "query"],
        "record_mode": mode,
    }


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    """
    Configure cassette directory to be 'cassettes/' relative to the test file.

    This ensures cassettes are stored in:
    - tests/integration/zia/cassettes/
    - tests/integration/zpa/cassettes/
    - etc.
    """
    # Get the directory of the test file
    test_dir = os.path.dirname(request.fspath)
    cassette_dir = os.path.join(test_dir, "cassettes")

    # Create the directory if it doesn't exist
    os.makedirs(cassette_dir, exist_ok=True)

    return cassette_dir


@pytest.fixture(scope="class")
def default_cassette_name(request):
    """
    Configure cassette naming to use one file per test class.

    Instead of: TestClassName.test_method_name.yaml
    We get:     TestClassName.yaml

    This consolidates all HTTP interactions from a test class into a single cassette.
    """
    # Get the test class name (e.g., "TestAdminRole")
    if request.cls:
        return request.cls.__name__
    else:
        # Fallback to module name for function-based tests
        return request.module.__name__.split(".")[-1]


def pytest_generate_tests(metafunc):
    """Set mock client environment variable during cassette rewriting."""
    record_mode = metafunc.config.getoption(PYTEST_RE_RECORD, default=None)
    if record_mode == "rewrite":
        os.environ[PYTEST_MOCK_CLIENT] = "1"


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Clean up environment variables after test session."""

    def clean_up_env_vars():
        if PYTEST_MOCK_CLIENT in os.environ:
            del os.environ[PYTEST_MOCK_CLIENT]

    request.addfinalizer(clean_up_env_vars)
