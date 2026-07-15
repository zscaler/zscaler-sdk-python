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

from zscaler.zins.zins_service import ZInsService


@pytest.fixture
def fs():
    yield


class TestZInsService:
    """
    Tests for the Z-Ins service properties (no VCR needed)
    """

    def test_zins_service_import(self):
        """ZInsService is exposed from zscaler.zins.zins_service."""
        assert ZInsService.__name__ == "ZInsService"

    def test_web_traffic_property(self, zins_client):
        """Test that web_traffic property returns WebTrafficAPI instance"""
        client = zins_client
        web_traffic_api = client.zins.web_traffic
        assert web_traffic_api is not None
        assert hasattr(web_traffic_api, "get_traffic_by_location")
        assert hasattr(web_traffic_api, "get_protocols")

    def test_saas_security_property(self, zins_client):
        """Test that saas_security property returns SaasSecurityAPI instance"""
        client = zins_client
        saas_security_api = client.zins.saas_security
        assert saas_security_api is not None
        assert hasattr(saas_security_api, "get_casb_app_report")

    def test_cyber_security_property(self, zins_client):
        """Test that cyber_security property returns CyberSecurityAPI instance"""
        client = zins_client
        cyber_security_api = client.zins.cyber_security
        assert cyber_security_api is not None
        assert hasattr(cyber_security_api, "get_incidents")
        assert hasattr(cyber_security_api, "get_incidents_by_location")

    def test_firewall_property(self, zins_client):
        """Test that firewall property returns FirewallAPI instance"""
        client = zins_client
        firewall_api = client.zins.firewall
        assert firewall_api is not None
        assert hasattr(firewall_api, "get_traffic_by_action")
        assert hasattr(firewall_api, "get_network_services")

    def test_iot_property(self, zins_client):
        """Test that iot property returns IotAPI instance"""
        client = zins_client
        iot_api = client.zins.iot
        assert iot_api is not None
        assert hasattr(iot_api, "get_device_stats")

    def test_shadow_it_property(self, zins_client):
        """Test that shadow_it property returns ShadowItAPI instance"""
        client = zins_client
        shadow_it_api = client.zins.shadow_it
        assert shadow_it_api is not None
        assert hasattr(shadow_it_api, "get_apps")
        assert hasattr(shadow_it_api, "get_shadow_it_summary")
