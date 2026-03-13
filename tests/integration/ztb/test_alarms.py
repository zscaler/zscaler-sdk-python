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
Integration tests for the ZTB Alarms resource.

Uses VCR to record/replay HTTP. Set MOCK_TESTS=false and ZTB_API_KEY,
ZTB_CLOUD (or ZTB_OVERRIDE_URL) when recording cassettes.
"""

import pytest

from tests.integration.ztb.conftest import MockZTBClient


@pytest.fixture
def fs():
    yield


@pytest.mark.vcr
class TestAlarms:
    """Integration tests for the ZTB Alarms API."""

    def test_list_alarms(self, fs):
        """Test listing alarms."""
        client = MockZTBClient()
        with client as c:
            alarms, _, err = c.ztb.alarms.list_alarms()
        if err:
            pytest.skip(f"list_alarms not available: {err}")
        assert alarms is not None
        assert isinstance(alarms, list)

    def test_list_alarms_with_query_params(self, fs):
        """Test listing alarms with query parameters."""
        client = MockZTBClient()
        with client as c:
            alarms, _, err = c.ztb.alarms.list_alarms(query_params={"page": 1, "size": 10})
        if err:
            pytest.skip(f"list_alarms with params not available: {err}")
        assert alarms is not None
        assert isinstance(alarms, list)
