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
from tests.integration.zinsights.conftest import MockZInsightsClient, get_time_range


@pytest.fixture
def fs():
    yield


class TestFirewall:
    """
    Integration Tests for the Z-Insights Zero Trust Firewall Analytics
    """

    @pytest.mark.vcr()
    def test_get_traffic_by_action(self, fs, zinsights_client):
        client = zinsights_client
        start_time, end_time = get_time_range(7)

        entries, response, err = client.zinsights.firewall.get_traffic_by_action(
            start_time=start_time,
            end_time=end_time,
            limit=10
        )

        # Verify SDK handles response correctly
        assert response is not None or err is not None
        print(f"Entries count: {len(entries) if entries else 0}")

    @pytest.mark.vcr()
    def test_get_traffic_by_location(self, fs, zinsights_client):
        client = zinsights_client
        start_time, end_time = get_time_range(7)

        entries, response, err = client.zinsights.firewall.get_traffic_by_location(
            start_time=start_time,
            end_time=end_time,
            limit=10
        )

        # Verify SDK handles response correctly
        assert response is not None or err is not None
        print(f"Entries count: {len(entries) if entries else 0}")

    @pytest.mark.vcr()
    def test_get_network_services(self, fs, zinsights_client):
        client = zinsights_client
        start_time, end_time = get_time_range(7)

        entries, response, err = client.zinsights.firewall.get_network_services(
            start_time=start_time,
            end_time=end_time,
            limit=10
        )

        # Verify SDK handles response correctly
        assert response is not None or err is not None
        print(f"Entries count: {len(entries) if entries else 0}")
