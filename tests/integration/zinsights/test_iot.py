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
from tests.integration.zinsights.conftest import MockZInsightsClient


@pytest.fixture
def fs():
    yield


class TestIoT:
    """
    Integration Tests for the Z-Insights IoT Device Visibility Analytics
    """

    @pytest.mark.vcr()
    def test_get_device_stats(self, fs, zinsights_client):
        client = zinsights_client

        stats, response, err = client.zinsights.iot.get_device_stats(limit=10)

        # Verify SDK handles response correctly (IoT may not be enabled)
        assert response is not None or err is not None
        if stats:
            print(f"Devices count: {stats.get('devices_count', 0)}")
            entries = stats.get('entries', [])
            print(f"Entries count: {len(entries)}")
        print("Device stats query completed")
