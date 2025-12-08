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
    Integration Tests for the Advanced Settings.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_advanced_settings_workflow(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Step 1: Retrieve current settings
        try:
            current_settings = client.zia.advanced_settings.get_advanced_settings()
            assert hasattr(current_settings, "enable_office365"), "Missing expected attribute: enable_office365"
        except Exception as exc:
            errors.append(f"Failed to retrieve advanced settings: {exc}")

        # Step 2: Update advanced settings with valid fields only
        try:
            updated_settings = client.zia.advanced_settings.update_advanced_settings(
                auth_bypass_apps=[],
                auth_bypass_urls=[".newexample1.com", ".newexample2.com"],
                dns_resolution_on_transparent_proxy_apps=["CHATGPT_AI"],
                kerberos_bypass_url_categories=["ADULT_SEX_EDUCATION", "ADULT_THEMES"],
                basic_bypass_url_categories=["NONE"],
                http_range_header_remove_url_categories=["NONE"],
                kerberos_bypass_urls=["test1.com"],
                kerberos_bypass_apps=[],
                dns_resolution_on_transparent_proxy_urls=["test1.com", "test2.com"],
                enable_dns_resolution_on_transparent_proxy=True,
                enable_evaluate_policy_on_global_ssl_bypass=True,
                enable_office365=True,
                log_internal_ip=True,
                enforce_surrogate_ip_for_windows_app=True,
                track_http_tunnel_on_http_ports=True,
                block_http_tunnel_on_non_http_ports=False,
                block_domain_fronting_on_host_header=False,
                zscaler_client_connector_1_and_pac_road_warrior_in_firewall=True,
                cascade_url_filtering=True,
                enable_policy_for_unauthenticated_traffic=True,
                block_non_compliant_http_request_on_http_ports=True,
                enable_admin_rank_access=True,
                # http2_nonbrowser_traffic_enabled=True,
                ecs_for_all_enabled=False,
                dynamic_user_risk_enabled=False,
                block_connect_host_sni_mismatch=False,
                prefer_sni_over_conn_host=False,
                sipa_xff_header_enabled=False,
                block_non_http_on_http_port_enabled=True,
                ui_session_timeout=300,
            )
            assert hasattr(updated_settings, "enable_office365"), "Missing expected attribute after update"

        except Exception as exc:
            errors.append(f"Failed to update advanced settings: {exc}")

        assert len(errors) == 0, f"Errors occurred during advanced settings test:\n{chr(10).join(errors)}"
