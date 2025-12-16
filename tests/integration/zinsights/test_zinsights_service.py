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


@pytest.fixture
def fs():
    yield


class TestZInsightsService:
    """
    Tests for the Z-Insights Service properties (no VCR needed)
    """

    def test_web_traffic_property(self, zinsights_client):
        """Test that web_traffic property returns WebTrafficAPI instance"""
        client = zinsights_client
        web_traffic_api = client.zinsights.web_traffic
        assert web_traffic_api is not None
        assert hasattr(web_traffic_api, 'get_traffic_by_location')
        assert hasattr(web_traffic_api, 'get_protocols')

    def test_saas_security_property(self, zinsights_client):
        """Test that saas_security property returns SaasSecurityAPI instance"""
        client = zinsights_client
        saas_security_api = client.zinsights.saas_security
        assert saas_security_api is not None
        assert hasattr(saas_security_api, 'get_casb_app_report')

    def test_cyber_security_property(self, zinsights_client):
        """Test that cyber_security property returns CyberSecurityAPI instance"""
        client = zinsights_client
        cyber_security_api = client.zinsights.cyber_security
        assert cyber_security_api is not None
        assert hasattr(cyber_security_api, 'get_incidents')
        assert hasattr(cyber_security_api, 'get_incidents_by_location')

    def test_firewall_property(self, zinsights_client):
        """Test that firewall property returns FirewallAPI instance"""
        client = zinsights_client
        firewall_api = client.zinsights.firewall
        assert firewall_api is not None
        assert hasattr(firewall_api, 'get_traffic_by_action')
        assert hasattr(firewall_api, 'get_network_services')

    def test_iot_property(self, zinsights_client):
        """Test that iot property returns IotAPI instance"""
        client = zinsights_client
        iot_api = client.zinsights.iot
        assert iot_api is not None
        assert hasattr(iot_api, 'get_device_stats')

    def test_shadow_it_property(self, zinsights_client):
        """Test that shadow_it property returns ShadowItAPI instance"""
        client = zinsights_client
        shadow_it_api = client.zinsights.shadow_it
        assert shadow_it_api is not None
        assert hasattr(shadow_it_api, 'get_apps')
        assert hasattr(shadow_it_api, 'get_shadow_it_summary')
