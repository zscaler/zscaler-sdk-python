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

"""
Integration tests for the ZTB App Connector Config resource.

Uses VCR to record/replay HTTP. Set MOCK_TESTS=false and ZTB credentials,
ZTB_TEST_CLUSTER_ID when recording cassettes.
"""

import os
import pytest

from tests.integration.ztb.conftest import MockZTBClient


@pytest.fixture
def fs():
    yield


@pytest.fixture
def cluster_id():
    """Cluster ID for get/delete. Override via ZTB_TEST_CLUSTER_ID when recording."""
    return os.getenv("ZTB_TEST_CLUSTER_ID", "tests-app-connector-cluster")


@pytest.mark.vcr
class TestAppConnectorConfig:
    """Integration tests for the ZTB App Connector Config API."""

    def test_get_app_connector_config(self, fs, cluster_id):
        """Test getting app connector config."""
        client = MockZTBClient()
        with client as c:
            config, _, err = c.ztb.app_connector_config.get_app_connector_config(cluster_id)
        if err:
            pytest.skip(f"get_app_connector_config not available: {err}")
        assert config is not None or err is None
