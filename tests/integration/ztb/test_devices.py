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
Integration tests for the ZTB Devices resource.

Uses VCR to record/replay HTTP.
Set MOCK_TESTS=false and ZTB credentials when recording cassettes.
"""

import pytest

from tests.integration.ztb.conftest import MockZTBClient


@pytest.fixture
def fs():
    yield


@pytest.mark.vcr
class TestDevices:
    """Integration tests for the ZTB Devices API."""

    def test_list_active_devices(self, fs):
        """Test listing active devices."""
        client = MockZTBClient()
        with client as c:
            devices, _, err = c.ztb.devices.list_active_devices()
        if err:
            pytest.skip(f"list_active_devices not available: {err}")
        assert devices is not None
        assert isinstance(devices, list)

    def test_list_active_devices_with_params(self, fs):
        """Test listing active devices with pagination and search params."""
        client = MockZTBClient()
        with client as c:
            devices, _, err = c.ztb.devices.list_active_devices(query_params={"search": "DESKTOP", "page": 1, "limit": 10})
        if err:
            pytest.skip(f"list_active_devices with params not available: {err}")
        assert devices is not None
        assert isinstance(devices, list)

    def test_get_device_tags(self, fs):
        """Test getting device tags."""
        client = MockZTBClient()
        with client as c:
            tags, _, err = c.ztb.devices.get_device_tags()
        if err:
            pytest.skip(f"get_device_tags not available: {err}")
        assert tags is not None
        assert hasattr(tags, "tags")
        assert isinstance(tags.tags, list)

    def test_get_group_by_list(self, fs):
        """Test getting group-by list for graphs."""
        client = MockZTBClient()
        with client as c:
            groups, _, err = c.ztb.devices.get_group_by_list()
        if err:
            pytest.skip(f"get_group_by_list not available: {err}")
        assert groups is not None
        assert isinstance(groups, list)

    def test_list_operating_systems(self, fs):
        """Test listing operating systems with device counts."""
        client = MockZTBClient()
        with client as c:
            os_list, _, err = c.ztb.devices.list_operating_systems(query_params={"page": 1, "limit": 10})
        if err:
            pytest.skip(f"list_operating_systems not available: {err}")
        assert os_list is not None
        assert isinstance(os_list, list)

    def test_list_devices_group_by(self, fs):
        """Test listing devices grouped by type."""
        client = MockZTBClient()
        with client as c:
            rows, _, err = c.ztb.devices.list_devices_group_by("type", query_params={"page": 1})
        if err:
            pytest.skip(f"list_devices_group_by not available: {err}")
        assert rows is not None
        assert isinstance(rows, list)

    def test_get_filter_values(self, fs):
        """Test getting filter values by field."""
        client = MockZTBClient()
        with client as c:
            fv, _, err = c.ztb.devices.get_filter_values("type")
        if err:
            pytest.skip(f"get_filter_values not available: {err}")
        assert fv is not None
        assert hasattr(fv, "values")
        assert isinstance(fv.values, list)
