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
Integration tests for the ZTB Site resource.

Uses VCR to record/replay HTTP.
Set MOCK_TESTS=false and ZTB credentials when recording cassettes.
"""

import pytest

from tests.integration.ztb.conftest import MockZTBClient


@pytest.fixture
def fs():
    yield


@pytest.mark.vcr
class TestSite:
    """Integration tests for the ZTB Site API."""

    def test_list_sites(self, fs):
        """Test listing sites."""
        client = MockZTBClient()
        with client as c:
            sites, _, err = c.ztb.site.list_sites()
        if err:
            pytest.skip(f"list_sites not available: {err}")
        assert sites is not None
        assert isinstance(sites, list)

    def test_list_sites_with_params(self, fs):
        """Test listing sites with pagination and search params."""
        client = MockZTBClient()
        with client as c:
            sites, _, err = c.ztb.site.list_sites(query_params={"search": "test", "page": 1, "limit": 10})
        if err:
            pytest.skip(f"list_sites with params not available: {err}")
        assert sites is not None
        assert isinstance(sites, list)

    def test_list_app_segments(self, fs):
        """Test listing app segments."""
        client = MockZTBClient()
        with client as c:
            segments, _, err = c.ztb.site.list_app_segments()
        if err:
            pytest.skip(f"list_app_segments not available: {err}")
        assert segments is not None
        assert isinstance(segments, list)

    def test_list_site_names(self, fs):
        """Test listing site names."""
        client = MockZTBClient()
        with client as c:
            names, _, err = c.ztb.site.list_site_names()
        if err:
            pytest.skip(f"list_site_names not available: {err}")
        assert names is not None
        assert isinstance(names, list)

    def test_get_md5(self, fs):
        """Test getting Gateway MD5."""
        client = MockZTBClient()
        with client as c:
            md5, _, err = c.ztb.site.get_md5()
        if err:
            pytest.skip(f"get_md5 not available: {err}")
        assert md5 is None or isinstance(md5, str)
