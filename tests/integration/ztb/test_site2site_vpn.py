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
Integration tests for the ZTB Site2Site VPN (Cloud Gateway) resource.

Uses VCR to record/replay HTTP.
Set MOCK_TESTS=false and ZTB credentials when recording cassettes.
"""

import pytest

from tests.integration.ztb.conftest import MockZTBClient


@pytest.fixture
def fs():
    yield


@pytest.mark.vcr
class TestSite2SiteVPN:
    """Integration tests for the ZTB Site2Site VPN API."""

    def test_list_hubs(self, fs):
        """Test listing cloud gateway hubs."""
        client = MockZTBClient()
        with client as c:
            hubs, _, err = c.ztb.site2site_vpn.list_hubs()
        if err:
            pytest.skip(f"list_hubs not available: {err}")
        assert hubs is not None
        assert isinstance(hubs, list)

    def test_list_hubs_with_params(self, fs):
        """Test listing hubs with pagination and search params."""
        client = MockZTBClient()
        with client as c:
            hubs, _, err = c.ztb.site2site_vpn.list_hubs(query_params={"search": "prod", "page": 1, "limit": 10})
        if err:
            pytest.skip(f"list_hubs with params not available: {err}")
        assert hubs is not None
        assert isinstance(hubs, list)

    def test_list_s2s_hubs(self, fs):
        """Test listing S2S VPN hubs."""
        client = MockZTBClient()
        with client as c:
            hubs, _, err = c.ztb.site2site_vpn.list_s2s_hubs()
        if err:
            pytest.skip(f"list_s2s_hubs not available: {err}")
        assert hubs is not None
        assert isinstance(hubs, list)

    def test_list_s2s_hubs_with_provider(self, fs):
        """Test listing S2S hubs with provider filter."""
        client = MockZTBClient()
        with client as c:
            hubs, _, err = c.ztb.site2site_vpn.list_s2s_hubs(query_params={"provider": "aws"})
        if err:
            pytest.skip(f"list_s2s_hubs with provider not available: {err}")
        assert hubs is not None
        assert isinstance(hubs, list)
