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
from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestAdvancedSettings:
    """
    Integration Tests for the Advanced Settings
    """

    def test_advanced_settings(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Test 1: Retrieve Advanced Settings
        try:
            settings, response, err = client.zia.advanced_settings.get_advanced_settings()
            assert settings is not None, "Failed to retrieve advanced settings - No data returned."
            assert err is None, f"Error retrieving advanced settings: {err}"
            assert response.get_status() == 200, f"Unexpected status code: {response.get_status()}"
        except Exception as exc:
            errors.append(f"Retrieve Advanced Settings failed: {exc}")

        # Test 2: Update Advanced Settings
        try:
            # Toggle multiple advanced settings for testing
            settings.enable_office365 = not settings.enable_office365
            settings.log_internal_ip = not settings.log_internal_ip
            settings.ui_session_timeout = settings.ui_session_timeout + 3600 if settings.ui_session_timeout else 3600
            settings.block_http_tunnel_on_non_http_ports = not settings.block_http_tunnel_on_non_http_ports
            settings.block_connect_host_sni_mismatch = not settings.block_connect_host_sni_mismatch

            # Update API call
            updated_settings, response, err = client.zia.advanced_settings.update_advanced_settings(settings)
            
            assert updated_settings is not None, "Failed to update advanced settings - No data returned."
            assert err is None, f"Error updating advanced settings: {err}"
            assert response.get_status() == 200, f"Unexpected status code: {response.get_status()}"

            # Validate that changes were successfully applied
            assert updated_settings.enable_office365 == settings.enable_office365, (
                "Failed to update `enable_office365` - Value mismatch."
            )
            assert updated_settings.log_internal_ip == settings.log_internal_ip, (
                "Failed to update `log_internal_ip` - Value mismatch."
            )
            assert updated_settings.ui_session_timeout == settings.ui_session_timeout, (
                "Failed to update `ui_session_timeout` - Value mismatch."
            )
            assert updated_settings.block_http_tunnel_on_non_http_ports == settings.block_http_tunnel_on_non_http_ports, (
                "Failed to update `block_http_tunnel_on_non_http_ports` - Value mismatch."
            )
            assert updated_settings.block_connect_host_sni_mismatch == settings.block_connect_host_sni_mismatch, (
                "Failed to update `block_connect_host_sni_mismatch` - Value mismatch."
            )

        except Exception as exc:
            errors.append(f"Update Advanced Settings failed: {exc}")

        # Final Test Assertion: Ensure No Errors Occurred
        assert len(errors) == 0, f"Errors occurred during Advanced Settings tests: {errors}"
