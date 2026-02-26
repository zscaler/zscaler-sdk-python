"""
Unit tests for the ZTB (Zero Trust Branch) client.

Tests:
  1. Auth header always uses Bearer format.
  2. URL constructed from cloud name: https://{cloud}-api.goairgap.com
  3. Override URL takes precedence over cloud-derived URL.
  4. Missing cloud raises ValueError.
  5. 429 Retry-After parsing for values like "0 seconds" and "2".
  6. Exponential backoff on 5xx transient errors.
  7. Network error retries.
  8. Token provider callable support.
  9. LegacyZTBClient construction via oneapi_client.
"""

import logging
import os
import pytest
from unittest.mock import Mock, patch, MagicMock, call
import requests

from zscaler.ztb.legacy import LegacyZTBClientHelper


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_response(status_code=200, json_data=None, headers=None, text=""):
    """Create a mock requests.Response."""
    resp = Mock(spec=requests.Response)
    resp.status_code = status_code
    resp.headers = headers or {}
    resp.text = text or ""
    if json_data is not None:
        resp.json.return_value = json_data
        resp.text = str(json_data)
    return resp


def _build_client(**overrides):
    """Build a LegacyZTBClientHelper with sane test defaults."""
    defaults = {
        "token": "test-jwt-token",
        "cloud": "zscalerbd-api",
        "timeout": 10,
        "max_retries": 3,
    }
    # Allow cloud=None to be passed explicitly for missing-cloud tests
    for k, v in overrides.items():
        defaults[k] = v
    with patch("zscaler.request_executor.RequestExecutor"):
        return LegacyZTBClientHelper(**defaults)


# ===========================================================================
# Test: Auth header formation (always Bearer)
# ===========================================================================

class TestAuthHeaderFormation:

    def test_bearer_prefix_added_automatically(self):
        client = _build_client(token="my-jwt")
        assert client._build_auth_header_value() == "Bearer my-jwt"

    def test_does_not_double_prefix(self):
        client = _build_client(token="Bearer already-prefixed")
        assert client._build_auth_header_value() == "Bearer already-prefixed"

    def test_case_insensitive_prefix_detection(self):
        client = _build_client(token="bearer lowercased")
        assert client._build_auth_header_value() == "bearer lowercased"

    @patch("requests.request")
    def test_send_sets_bearer_authorization_header(self, mock_request):
        client = _build_client(token="my-jwt")
        mock_resp = _make_response(200, json_data={"ok": True})
        mock_request.return_value = mock_resp

        with patch("zscaler.ztb.legacy.check_response_for_error", return_value=({"ok": True}, None)):
            resp, ctx = client.send("GET", "/api/v2/alarm")

        _, kwargs = mock_request.call_args
        assert kwargs["headers"]["Authorization"] == "Bearer my-jwt"


# ===========================================================================
# Test: URL resolution from cloud name
# ===========================================================================

class TestURLResolution:

    def test_url_built_from_cloud(self):
        client = _build_client(cloud="zscalerbd-api")
        assert client.url == "https://zscalerbd-api.goairgap.com"
        assert client.get_base_url() == "https://zscalerbd-api.goairgap.com"

    def test_url_built_from_different_cloud(self):
        client = _build_client(cloud="mytenant-api")
        assert client.url == "https://mytenant-api.goairgap.com"

    def test_override_url_takes_precedence(self):
        client = _build_client(cloud="zscalerbd-api", override_url="https://custom.example.com")
        assert client.url == "https://custom.example.com"

    @patch.dict(os.environ, {"ZTB_OVERRIDE_URL": "https://env-override.goairgap.com"})
    def test_override_url_env_var(self):
        client = _build_client(cloud="zscalerbd-api")
        assert client.url == "https://env-override.goairgap.com"

    def test_override_url_kwarg_beats_env(self):
        with patch.dict(os.environ, {"ZTB_OVERRIDE_URL": "https://env.goairgap.com"}):
            client = _build_client(cloud="zscalerbd-api", override_url="https://kwarg.goairgap.com")
            assert client.url == "https://kwarg.goairgap.com"

    @patch.dict(os.environ, {"ZTB_CLOUD": "fromenv-api"}, clear=False)
    def test_cloud_from_env_var(self):
        client = _build_client(cloud=None)
        assert client.url == "https://fromenv-api.goairgap.com"

    def test_missing_cloud_raises(self):
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("ZTB_CLOUD", None)
            os.environ.pop("ZTB_TOKEN", None)
            with pytest.raises(ValueError, match="Cloud environment must be set"):
                _build_client(cloud=None)

    @patch("requests.request")
    def test_send_builds_correct_url(self, mock_request):
        client = _build_client(cloud="zscalerbd-api")
        mock_resp = _make_response(200, json_data={})
        mock_request.return_value = mock_resp

        with patch("zscaler.ztb.legacy.check_response_for_error", return_value=({}, None)):
            client.send("GET", "/api/v2/alarm")

        _, kwargs = mock_request.call_args
        assert kwargs["url"] == "https://zscalerbd-api.goairgap.com/api/v2/alarm"

    @patch("requests.request")
    def test_send_strips_leading_slash_correctly(self, mock_request):
        client = _build_client(cloud="zscalerbd-api")
        mock_resp = _make_response(200, json_data={})
        mock_request.return_value = mock_resp

        with patch("zscaler.ztb.legacy.check_response_for_error", return_value=({}, None)):
            client.send("GET", "api/v2/alarm")

        _, kwargs = mock_request.call_args
        assert kwargs["url"] == "https://zscalerbd-api.goairgap.com/api/v2/alarm"


# ===========================================================================
# Test: 429 handling and Retry-After parsing
# ===========================================================================

class TestRetryAfterParsing:

    def test_parse_retry_after_integer_string(self):
        result = LegacyZTBClientHelper._parse_retry_after({"Retry-After": "2"}, attempt=0)
        assert result == 2

    def test_parse_retry_after_zero_seconds_string(self):
        result = LegacyZTBClientHelper._parse_retry_after({"Retry-After": "0 seconds"}, attempt=0)
        assert result == 1

    def test_parse_retry_after_with_seconds_suffix(self):
        result = LegacyZTBClientHelper._parse_retry_after({"Retry-After": "5 seconds"}, attempt=0)
        assert result == 5

    def test_parse_retry_after_missing_header_falls_back_to_backoff(self):
        result = LegacyZTBClientHelper._parse_retry_after({}, attempt=0)
        assert 1 <= result <= 1.25

    def test_parse_retry_after_case_insensitive(self):
        result = LegacyZTBClientHelper._parse_retry_after({"retry-after": "3"}, attempt=0)
        assert result == 3

    def test_parse_retry_after_invalid_value_falls_back(self):
        result = LegacyZTBClientHelper._parse_retry_after({"Retry-After": "not-a-number"}, attempt=0)
        assert result >= 1

    @patch("requests.request")
    @patch("zscaler.ztb.legacy.sleep")
    def test_429_retries_with_retry_after(self, mock_sleep, mock_request):
        client = _build_client(max_retries=3)

        resp_429 = _make_response(429, headers={"Retry-After": "2"})
        resp_200 = _make_response(200, json_data={"alarms": []})
        mock_request.side_effect = [resp_429, resp_200]

        with patch("zscaler.ztb.legacy.check_response_for_error", return_value=({"alarms": []}, None)):
            resp, ctx = client.send("GET", "/api/v2/alarm")

        assert resp.status_code == 200
        mock_sleep.assert_called_once_with(2)

    @patch("requests.request")
    @patch("zscaler.ztb.legacy.sleep")
    def test_429_exhausts_retries(self, mock_sleep, mock_request):
        client = _build_client(max_retries=2)

        resp_429 = _make_response(429, headers={"Retry-After": "1"})
        mock_request.return_value = resp_429

        with pytest.raises(ValueError, match="maximum retries"):
            client.send("GET", "/api/v2/alarm")

        assert mock_sleep.call_count == 3


# ===========================================================================
# Test: 5xx transient error retries
# ===========================================================================

class TestTransientErrorRetries:

    @patch("requests.request")
    @patch("zscaler.ztb.legacy.sleep")
    def test_502_retries_then_succeeds(self, mock_sleep, mock_request):
        client = _build_client(max_retries=3)

        resp_502 = _make_response(502)
        resp_200 = _make_response(200, json_data={"ok": True})
        mock_request.side_effect = [resp_502, resp_200]

        with patch("zscaler.ztb.legacy.check_response_for_error", return_value=({"ok": True}, None)):
            resp, ctx = client.send("GET", "/api/v2/alarm")

        assert resp.status_code == 200
        assert mock_sleep.call_count == 1

    @patch("requests.request")
    @patch("zscaler.ztb.legacy.sleep")
    def test_503_retries(self, mock_sleep, mock_request):
        client = _build_client(max_retries=2)

        resp_503 = _make_response(503)
        mock_request.return_value = resp_503

        with pytest.raises(ValueError, match="maximum retries"):
            client.send("GET", "/api/v2/alarm")

    @patch("requests.request")
    @patch("zscaler.ztb.legacy.sleep")
    def test_504_retries(self, mock_sleep, mock_request):
        client = _build_client(max_retries=1)

        resp_504 = _make_response(504)
        resp_200 = _make_response(200, json_data={})
        mock_request.side_effect = [resp_504, resp_200]

        with patch("zscaler.ztb.legacy.check_response_for_error", return_value=({}, None)):
            resp, ctx = client.send("GET", "/api/v2/alarm")

        assert resp.status_code == 200


# ===========================================================================
# Test: Network error retries
# ===========================================================================

class TestNetworkErrorRetries:

    @patch("requests.request")
    @patch("zscaler.ztb.legacy.sleep")
    def test_connection_error_retries(self, mock_sleep, mock_request):
        client = _build_client(max_retries=2)

        mock_request.side_effect = [
            requests.ConnectionError("Connection refused"),
            _make_response(200, json_data={"ok": True}),
        ]

        with patch("zscaler.ztb.legacy.check_response_for_error", return_value=({"ok": True}, None)):
            resp, ctx = client.send("GET", "/api/v2/alarm")

        assert resp.status_code == 200
        assert mock_sleep.call_count == 1

    @patch("requests.request")
    @patch("zscaler.ztb.legacy.sleep")
    def test_network_error_exhausts_retries(self, mock_sleep, mock_request):
        client = _build_client(max_retries=2)
        mock_request.side_effect = requests.ConnectionError("Connection refused")

        with pytest.raises(requests.ConnectionError):
            client.send("GET", "/api/v2/alarm")

        assert mock_sleep.call_count == 2


# ===========================================================================
# Test: Token provider
# ===========================================================================

class TestTokenProvider:

    def test_token_provider_callable(self):
        provider = Mock(return_value="dynamic-token")
        client = _build_client(token=None, token_provider=provider)
        assert client._get_token() == "dynamic-token"
        provider.assert_called_once()

    def test_token_provider_empty_raises(self):
        provider = Mock(return_value="")
        client = _build_client(token=None, token_provider=provider)
        with pytest.raises(ValueError, match="empty token"):
            client._get_token()

    def test_static_token_preferred_over_none_provider(self):
        client = _build_client(token="static-token", token_provider=None)
        assert client._get_token() == "static-token"

    def test_token_provider_takes_precedence_over_static(self):
        provider = Mock(return_value="dynamic")
        client = _build_client(token="static", token_provider=provider)
        assert client._get_token() == "dynamic"

    def test_no_token_and_no_provider_raises(self):
        with pytest.raises(ValueError, match="token is required"):
            with patch.dict(os.environ, {}, clear=True):
                os.environ.pop("ZTB_TOKEN", None)
                _build_client(token=None, token_provider=None)


# ===========================================================================
# Test: Exponential backoff calculation
# ===========================================================================

class TestExponentialBackoff:

    def test_attempt_0(self):
        for _ in range(20):
            val = LegacyZTBClientHelper._exponential_backoff(0)
            assert 1 <= val <= 1.25

    def test_attempt_increases(self):
        vals = [LegacyZTBClientHelper._exponential_backoff(i) for i in range(6)]
        assert vals[-1] <= 30

    def test_capped_at_max(self):
        for _ in range(20):
            val = LegacyZTBClientHelper._exponential_backoff(100)
            assert val <= 30


# ===========================================================================
# Test: No JSESSIONID logic present
# ===========================================================================

class TestNoJSessionID:

    def test_no_jsessionid_attribute(self):
        client = _build_client()
        assert not hasattr(client, "session_id")
        assert not hasattr(client, "extractJSessionIDFromHeaders")

    def test_no_session_cookie_in_send(self):
        client = _build_client()
        headers = client.headers.copy()
        assert "Cookie" not in headers
        assert "JSESSIONID" not in str(headers)


# ===========================================================================
# Test: LegacyZTBClient (oneapi_client entrypoint)
# ===========================================================================

class TestLegacyZTBClientEntrypoint:

    @patch("zscaler.request_executor.RequestExecutor")
    def test_legacy_ztb_client_construction(self, mock_executor):
        from zscaler.oneapi_client import LegacyZTBClient

        config = {
            "token": "my-token",
            "cloud": "zscalerbd-api",
        }
        client = LegacyZTBClient(config)
        assert client.use_legacy_client is True
        assert isinstance(client.ztb_legacy_client, LegacyZTBClientHelper)
        assert client.ztb_legacy_client.url == "https://zscalerbd-api.goairgap.com"

    @patch("zscaler.request_executor.RequestExecutor")
    @patch.dict(os.environ, {"ZTB_TOKEN": "env-token", "ZTB_CLOUD": "envcloud-api"})
    def test_legacy_ztb_client_from_env(self, mock_executor):
        from zscaler.oneapi_client import LegacyZTBClient

        client = LegacyZTBClient({})
        assert client.ztb_legacy_client.token == "env-token"
        assert client.ztb_legacy_client.url == "https://envcloud-api.goairgap.com"

    @patch("zscaler.request_executor.RequestExecutor")
    def test_legacy_ztb_client_with_override_url(self, mock_executor):
        from zscaler.oneapi_client import LegacyZTBClient

        config = {
            "token": "my-token",
            "cloud": "zscalerbd-api",
            "override_url": "https://custom.example.com",
        }
        client = LegacyZTBClient(config)
        assert client.ztb_legacy_client.url == "https://custom.example.com"


# ===========================================================================
# Test: Context manager
# ===========================================================================

class TestContextManager:

    def test_context_manager_enters_and_exits(self):
        client = _build_client()
        with client as c:
            assert c is client


# ===========================================================================
# Test: Headers
# ===========================================================================

class TestHeaders:

    def test_default_headers_include_content_type(self):
        client = _build_client()
        assert client.headers["Content-Type"] == "application/json"
        assert client.headers["Accept"] == "application/json"
        assert "User-Agent" in client.headers

    def test_partner_id_header_set(self):
        client = _build_client(partner_id="partner-123")
        assert client.headers["x-partner-id"] == "partner-123"

    def test_partner_id_header_absent_by_default(self):
        client = _build_client()
        assert "x-partner-id" not in client.headers

    @patch("requests.request")
    def test_custom_headers_merged_in_send(self, mock_request):
        client = _build_client()
        mock_resp = _make_response(200, json_data={})
        mock_request.return_value = mock_resp

        with patch("zscaler.ztb.legacy.check_response_for_error", return_value=({}, None)):
            client.send("GET", "/api/v2/alarm", headers={"X-Custom": "value"})

        _, kwargs = mock_request.call_args
        assert kwargs["headers"]["X-Custom"] == "value"
        assert kwargs["headers"]["Content-Type"] == "application/json"
